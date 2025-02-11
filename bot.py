import sys
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# Load environment variables from the .env file
load_dotenv()

# Retrieve configuration from the .env file
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
EMOJI_FOLDER = os.getenv("EMOJI_FOLDER", "emotes")  # Main folder is "emotes"
CURRENT_SEASON = os.getenv("CURRENT_SEASON", "base")  # Default set to base; change seasons via .env  with e.g., "winter", "fall", or "base"

# Construct the full path to the current season's emote folder
EMOJI_PATH = os.path.join(EMOJI_FOLDER, CURRENT_SEASON)

# Configure Discord intents
intents = discord.Intents.default()
intents.guilds = True

# Create the bot instance (pod) with a command prefix and the specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("POD-042 (pod) has connected to Discord!")
    
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("Error: Could not find the guild. Check that GUILD_ID is correct.")
        await bot.close()
        return

    # Locate the text channel named "general"
    general_channel = discord.utils.get(guild.text_channels, name="general")
    
    # If a command-line argument is provided, send that message and exit.
    if len(sys.argv) > 1:
        message_content = " ".join(sys.argv[1:])
        if general_channel:
            try:
                await general_channel.send(message_content)
                print(f"Sent message: {message_content}")
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print("General channel not found. No message sent.")
        await bot.close()
        return

    # Otherwise, proceed with the emote update operation.
    if general_channel:
        try:
            await general_channel.send(f"**[OPERATION INITIATED]** Update Emotes for *'{CURRENT_SEASON}'* in progress. Taking control...")
            print("Sent start message to #general")
        except Exception as e:
            print(f"Error sending start message: {e}")
    else:
        print("General channel not found. No start message sent.")
    
    print(f"Processing emotes from folder: {EMOJI_PATH}")
    
    if not os.path.exists(EMOJI_PATH):
        print(f"Error: The folder {EMOJI_PATH} does not exist.")
        await bot.close()
        return

    # Iterate over each image file in the seasonal folder
    for filename in os.listdir(EMOJI_PATH):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            emote_name, _ = os.path.splitext(filename)
            image_path = os.path.join(EMOJI_PATH, filename)
            try:
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

            # Check if an emote with the same name already exists in the guild
            existing_emote = discord.utils.get(guild.emojis, name=emote_name)
            if existing_emote:
                try:
                    await existing_emote.delete(reason="Updating emote asset")
                    print(f"Deleted emote: {emote_name}")
                except Exception as e:
                    print(f"Error deleting emote {emote_name}: {e}")

            try:
                # Use create_custom_emoji (as your environment appears to support this)
                new_emote = await guild.create_custom_emoji(name=emote_name, image=image_data, reason="Updating emote asset")
                print(f"Created emote: {new_emote}")
                # Optional: Delay to help mitigate rate limits.
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Error creating emote {emote_name}: {e}")

    # After processing, send a completion message to #general and then close the bot.
    if general_channel:
        try:
            await general_channel.send("**[OPERATION COMPLETE]** All targeted emote assets updated. Returning control to command.")
            print("Sent completion message to #general")
        except Exception as e:
            print(f"Error sending completion message: {e}")
    else:
        print("General channel not found. No completion message sent.")

    await bot.close()

bot.run(TOKEN)
