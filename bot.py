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


async def update_emotes_mode(guild):
    """Synchronize emotes from the current season folder to Discord."""
    channel = get_notification_channel(guild)

    await send_notification(
        channel,
        f"**[OPERATION INITIATED]** Updating emotes for *'{CURRENT_SEASON}'*..."
    )

    updated = 0
    failed = 0

    for filename in os.listdir(EMOJI_PATH):
        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            continue

        emote_name, _ = os.path.splitext(filename)
        image_path = os.path.join(EMOJI_PATH, filename)

        # Read image file
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
        except OSError as e:
            print(f"Failed to read {filename}: {e}")
            failed += 1
            continue

        # Delete existing emote if present
        existing = discord.utils.get(guild.emojis, name=emote_name)
        if existing:
            try:
                await existing.delete(reason="Updating emote asset")
                print(f"Deleted: {emote_name}")
            except discord.HTTPException as e:
                print(f"Failed to delete {emote_name}: {e}")
                failed += 1
                continue

        # Create new emote
        try:
            await guild.create_custom_emoji(
                name=emote_name,
                image=image_data,
                reason="Updating emote asset"
            )
            print(f"Created: {emote_name}")
            updated += 1
            await asyncio.sleep(RATE_LIMIT_DELAY)
        except discord.HTTPException as e:
            print(f"Failed to create {emote_name}: {e}")
            failed += 1

    # Send summary
    summary = f"**[OPERATION COMPLETE]** Updated {updated} emotes"
    if failed > 0:
        summary += f", {failed} failed"
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

    # Command-line message mode: python bot.py "Your message here"
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        await send_message_mode(guild, message)
    else:
        # Default: update emotes
        await update_emotes_mode(guild)

    await bot.close()


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    validate_config()
    bot.run(TOKEN)
