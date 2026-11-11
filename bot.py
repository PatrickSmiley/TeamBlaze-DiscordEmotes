import sys
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================

load_dotenv()

# Required configuration
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Optional: specific channel for notifications

# Folder settings
EMOJI_FOLDER = os.getenv("EMOJI_FOLDER", "emotes")
CURRENT_SEASON = os.getenv("CURRENT_SEASON", "base")
EMOJI_PATH = os.path.join(EMOJI_FOLDER, CURRENT_SEASON)

# Constants
RATE_LIMIT_DELAY = 2  # Seconds between API calls to avoid Discord rate limiting
SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif")
MAX_EMOTE_BYTES = 256 * 1024  # Discord's per-file cap for custom emotes
BASE_SEASON = "base"

# Bot setup
intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def validate_config():
    """Validate required configuration before starting the bot."""
    errors = []

    if not TOKEN:
        errors.append("DISCORD_TOKEN is not set in .env")
    if not GUILD_ID:
        errors.append("GUILD_ID is not set in .env")
    elif not GUILD_ID.isdigit():
        errors.append("GUILD_ID must be the numeric server ID")
    if not os.path.exists(EMOJI_PATH):
        errors.append(f"Emoji folder not found: {EMOJI_PATH}")

    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


def get_notification_channel(guild):
    """Get the channel for bot notifications.

    Uses CHANNEL_ID from .env if set, otherwise falls back to #general.
    """
    if CHANNEL_ID:
        return guild.get_channel(int(CHANNEL_ID))
    return discord.utils.get(guild.text_channels, name="general")


async def send_notification(channel, message):
    """Send a notification message to the specified channel."""
    if not channel:
        print(f"[No channel] {message}")
        return
    try:
        await channel.send(message)
        print(f"[Discord] {message}")
    except discord.HTTPException as e:
        print(f"Failed to send message: {e}")


# ==============================================================================
# CORE OPERATIONS
# ==============================================================================

async def send_message_mode(guild, message):
    """Send a custom message to the notification channel and exit."""
    channel = get_notification_channel(guild)
    await send_notification(channel, message)


def season_files(folder, season):
    """Map emote name -> file path for one season folder and its animated/ subfolder."""
    files = {}
    for sub in ("", "animated"):
        path = os.path.join(folder, season, sub)
        if not os.path.isdir(path):
            continue
        for filename in sorted(os.listdir(path)):
            full = os.path.join(path, filename)
            if os.path.isfile(full) and filename.lower().endswith(SUPPORTED_EXTENSIONS):
                files[os.path.splitext(filename)[0]] = full
    return files


def select_emotes(folder, season):
    """Return (merged, seasonal) for a season.

    merged: name -> path, the base set with the season's overlay on top.
    seasonal: names that have a version in any overlay folder (fall, winter...).
    Those are swapped on every run so switching seasons, including back to
    base, puts the right version up. Every other name is only added if missing.
    """
    overlays = [
        d for d in os.listdir(folder)
        if d != BASE_SEASON and os.path.isdir(os.path.join(folder, d))
    ]
    merged = season_files(folder, BASE_SEASON)
    if season != BASE_SEASON:
        merged.update(season_files(folder, season))
    seasonal = set()
    for overlay in overlays:
        seasonal.update(season_files(folder, overlay))
    return merged, seasonal


async def update_emotes_mode(guild):
    """Bring the guild's emotes in line with the current season.

    Missing emotes are added. Seasonal emotes are swapped: the new one is
    uploaded first and the old one deleted after, so a failed upload never
    leaves the emote missing. Files over Discord's cap are skipped.
    """
    channel = get_notification_channel(guild)

    await send_notification(
        channel,
        f"**[OPERATION INITIATED]** Updating emotes for *'{CURRENT_SEASON}'*..."
    )

    merged, seasonal = select_emotes(EMOJI_FOLDER, CURRENT_SEASON)
    added = swapped = unchanged = 0
    failed = []

    for emote_name, image_path in sorted(merged.items()):
        existing = discord.utils.get(guild.emojis, name=emote_name)
        if existing and emote_name not in seasonal:
            unchanged += 1
            continue

        try:
            size = os.path.getsize(image_path)
            if size > MAX_EMOTE_BYTES:
                print(f"Skipped {emote_name}: {image_path} is {size // 1024} KB, "
                      f"over Discord's {MAX_EMOTE_BYTES // 1024} KB cap. Existing emote left alone.")
                failed.append(emote_name)
                continue
            with open(image_path, "rb") as f:
                image_data = f.read()
        except OSError as e:
            print(f"Failed to read {image_path}: {e}")
            failed.append(emote_name)
            continue

        # Upload first; the old emote is only removed once the new one exists
        try:
            new = await guild.create_custom_emoji(
                name=emote_name,
                image=image_data,
                reason="Updating emote asset"
            )
            await asyncio.sleep(RATE_LIMIT_DELAY)
        except (discord.HTTPException, ValueError) as e:  # ValueError: unreadable image
            print(f"Failed to upload {emote_name}: {e}. Existing emote left alone.")
            failed.append(emote_name)
            continue

        if not existing:
            print(f"Added: {emote_name}")
            added += 1
            continue

        try:
            await existing.delete(reason="Replaced by updated emote asset")
            print(f"Swapped: {emote_name}")
            swapped += 1
            await asyncio.sleep(RATE_LIMIT_DELAY)
        except discord.NotFound:
            # Old one is already gone; the new upload is the only copy, keep it
            print(f"Swapped: {emote_name} (old one was already gone)")
            swapped += 1
        except discord.Forbidden as e:
            # No permission to delete the old one: take the new upload back down
            # so repeated runs never pile up duplicates
            print(f"Not allowed to delete the old {emote_name}: {e}. Kept the old one.")
            try:
                await new.delete(reason="Old emote could not be removed")
            except discord.HTTPException as e2:
                print(f"Also failed to remove the new {emote_name}: {e2}. "
                      f"Delete the duplicate by hand.")
            failed.append(emote_name)
        except discord.HTTPException as e:
            # Unknown outcome (e.g. server error): keep both rather than risk losing it
            print(f"Uploaded new {emote_name} but deleting the old one failed: {e}. "
                  f"Check for a duplicate by hand.")
            failed.append(emote_name)

    # Send summary
    summary = (f"**[OPERATION COMPLETE]** Added {added}, swapped {swapped}, "
               f"unchanged {unchanged}")
    if failed:
        summary += f", {len(failed)} failed: {', '.join(failed)}"
    await send_notification(channel, summary)


# ==============================================================================
# BOT EVENTS
# ==============================================================================

@bot.event
async def on_ready():
    """Main entry point when the bot connects to Discord."""
    print(f"POD-042 (pod) has connected to Discord!")

    guild = bot.get_guild(int(GUILD_ID))
    if not guild:
        print(f"Error: Could not find guild {GUILD_ID}")
        await bot.close()
        return

    try:
        # Command-line message mode: python bot.py "Your message here"
        if len(sys.argv) > 1:
            message = " ".join(sys.argv[1:])
            await send_message_mode(guild, message)
        else:
            # Default: update emotes
            await update_emotes_mode(guild)
    finally:
        await bot.close()


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    validate_config()
    bot.run(TOKEN)
