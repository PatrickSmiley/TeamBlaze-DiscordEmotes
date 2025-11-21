import sys
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ==============================================================================
# CONFIGURATION & SETUP
# ==============================================================================

# Load environment variables from the .env file
load_dotenv()

# --- Configuration Constants ---
# These values are pulled from your .env file.
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

# Folder settings
EMOJI_FOLDER = os.getenv("EMOJI_FOLDER", "emotes")      # Main folder containing all seasons
CURRENT_SEASON = os.getenv("CURRENT_SEASON", "base")    # Current season (e.g., "base", "winter", "fall")

# Construct the full path to the current season's emote folder
EMOJI_PATH = os.path.join(EMOJI_FOLDER, CURRENT_SEASON)

# --- Discord Setup ---
# Configure the bot's permissions (intents)
intents = discord.Intents.default()
intents.guilds = True

# Create the bot instance
# We use "!" as a prefix, though this bot is primarily event-driven.
bot = commands.Bot(command_prefix="!", intents=intents)


# ==============================================================================
# BOT EVENTS
# ==============================================================================

@bot.event
async def on_ready():
    """
    This function runs automatically when the bot successfully connects to Discord.
    It handles two main scenarios:
    1. Sending a specific message (if run with arguments).
    2. Updating server emotes based on the current season (default behavior).
    """
    print("POD-042 (pod) has connected to Discord!")
    
    # 1. Find the target Guild (Server)
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("Error: Could not find the guild. Check that GUILD_ID is correct in .env")
        await bot.close()
        return

    # 2. Find the communication channel (#general)
    # NOTE: This requires a channel literally named "general" to exist.
    general_channel = discord.utils.get(guild.text_channels, name="general")
    
    # --- SCENARIO A: Command Line Message Mode ---
    # If you ran the script like: python bot.py "Hello World"
    if len(sys.argv) > 1:
        message_content = " ".join(sys.argv[1:])
        if general_channel:
            try:
                # Send the message to Discord
                await general_channel.send(message_content)
                print(f"Sent message to Discord: {message_content}")
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print("General channel not found. No message sent.")
        
        # Exit after sending the message
        await bot.close()
        return

    # --- SCENARIO B: Emote Update Mode ---
    # This is the default behavior if no arguments are provided.
    
    # Notify Discord that we are starting
    if general_channel:
        try:
            await general_channel.send(f"**[OPERATION INITIATED]** Update Emotes for *'{CURRENT_SEASON}'* in progress. Taking control...")
            print("Sent start message to #general")
        except Exception as e:
            print(f"Error sending start message: {e}")
    else:
        print("General channel not found. No start message sent.")
    
    print(f"Processing emotes from folder: {EMOJI_PATH}")
    
    # Validate folder exists
    if not os.path.exists(EMOJI_PATH):
        print(f"Error: The folder {EMOJI_PATH} does not exist.")
        await bot.close()
        return

    # 3. Process Emotes
    # Iterate over every file in the season folder
    for filename in os.listdir(EMOJI_PATH):
        # Only process image files
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            emote_name, _ = os.path.splitext(filename)
            image_path = os.path.join(EMOJI_PATH, filename)
            
            # Read the image file
            try:
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
                continue

            # Check if emote already exists on the server
            existing_emote = discord.utils.get(guild.emojis, name=emote_name)
            
            # If it exists, DELETE it first
            if existing_emote:
                try:
                    await existing_emote.delete(reason="Updating emote asset")
                    print(f"Deleted old emote: {emote_name}")
                except Exception as e:
                    print(f"Error deleting emote {emote_name}: {e}")

            # Create the NEW emote
            try:
                new_emote = await guild.create_custom_emoji(name=emote_name, image=image_data, reason="Updating emote asset")
                print(f"Created new emote: {new_emote.name}")
                
                # IMPORTANT: Wait 2 seconds to avoid hitting Discord's rate limits
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Error creating emote {emote_name}: {e}")

    # 4. Finish Up
    # Notify Discord that we are done
    if general_channel:
        try:
            await general_channel.send("**[OPERATION COMPLETE]** All targeted emote assets updated. Returning control to command.")
            print("Sent completion message to #general")
        except Exception as e:
            print(f"Error sending completion message: {e}")
    else:
        print("General channel not found. No completion message sent.")

    # Disconnect
    await bot.close()

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    bot.run(TOKEN)
