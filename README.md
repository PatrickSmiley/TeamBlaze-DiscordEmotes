# TeamBlaze-DiscordEmotes

Discord bot for managing seasonal custom emotes for Team Blaze.

## Features

- Batch upload/update emotes from local folders to Discord
- Seasonal emote variants (base, fall, winter)
- Send custom messages to Discord via command line
- Automatic rate limiting to avoid Discord API limits

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file with your configuration:
   ```
   DISCORD_TOKEN=your_bot_token
   GUILD_ID=your_server_id
   CHANNEL_ID=optional_notification_channel_id
   CURRENT_SEASON=base
   ```

## Usage

Update emotes for the current season:
```bash
python bot.py
```

Send a custom message to Discord:
```bash
python bot.py "Hello Team Blaze!"
```

Change seasons by updating `CURRENT_SEASON` in `.env` to `base`, `fall`, or `winter`.

## Emote Gallery

| Emote Name | Base | HD | Fall | HD | Winter | HD |
|------------|------|-----|------|-----|--------|-----|
| apes | <img src='emotes/base/apes.png' width='32px'> | Y | | | <img src='emotes/winter/apes.png' width='32px'> | Y |
| bait | <img src='emotes/base/bait.png' width='32px'> | Y | | | <img src='emotes/winter/bait.png' width='32px'> | |
| bigbrain | <img src='emotes/base/bigbrain.png' width='32px'> | Y | | | | N/A |
| blz | <img src='emotes/base/blz.png' width='32px'> | Y | | | | N/A |
| bongocat | <img src='emotes/base/bongocat.png' width='32px'> | Y | | | <img src='emotes/winter/bongocat.png' width='32px'> | N |
| bonk | <img src='emotes/base/bonk.png' width='32px'> | | | | | N/A |
| boomer | <img src='emotes/base/boomer.png' width='32px'> | Y | | | <img src='emotes/winter/boomer.png' width='32px'> | Y |
| comfycat | <img src='emotes/base/comfycat.png' width='32px'> | Y | <img src='emotes/fall/comfycat.png' width='32px'> | Y | <img src='emotes/winter/comfycat.png' width='32px'> | Y |
| comfypepo | <img src='emotes/base/comfypepo.png' width='32px'> | Y | <img src='emotes/fall/comfypepo.png' width='32px'> | Y | <img src='emotes/winter/comfypepo.png' width='32px'> | Y |
| comfyyee | <img src='emotes/base/comfyyee.png' width='32px'> | Y | | | <img src='emotes/winter/comfyyee.png' width='32px'> | Y |
| copium | <img src='emotes/base/copium.png' width='32px'> | N | | | <img src='emotes/winter/copium.png' width='32px'> | |
| dafeels | | | <img src='emotes/fall/dafeels.png' width='32px'> | N | <img src='emotes/winter/dafeels.png' width='32px'> | N |
| dankmemes | <img src='emotes/base/dankmemes.png' width='32px'> | Y | <img src='emotes/fall/dankmemes.png' width='32px'> | Y | <img src='emotes/winter/dankmemes.png' width='32px'> | Y |
| facepalm | <img src='emotes/base/facepalm.png' width='32px'> | Y | | | | N/A |
| feelsbadman | <img src='emotes/base/feelsbadman.png' width='32px'> | N | <img src='emotes/fall/feelsbadman.png' width='32px'> | N | <img src='emotes/winter/feelsbadman.png' width='32px'> | N |
| feelsgoodman | <img src='emotes/base/feelsgoodman.png' width='32px'> | N | <img src='emotes/fall/feelsgoodman.png' width='32px'> | N | <img src='emotes/winter/feelsgoodman.png' width='32px'> | N |
| gnome | <img src='emotes/base/gnome.png' width='32px'> | Y | | | <img src='emotes/winter/gnome.png' width='32px'> | Y |
| hahaa | <img src='emotes/base/hahaa.png' width='32px'> | Y | | | <img src='emotes/winter/hahaa.png' width='32px'> | Y |
| hhheheh | <img src='emotes/base/hhheheh.png' width='32px'> | Y | | | <img src='emotes/winter/hhheheh.png' width='32px'> | Y |
| hmm | <img src='emotes/base/hmm.png' width='32px'> | Y | <img src='emotes/fall/hmm.png' width='32px'> | Y | <img src='emotes/winter/hmm.png' width='32px'> | Y |
| kekw | <img src='emotes/base/kekw.png' width='32px'> | N | | | <img src='emotes/winter/kekw.png' width='32px'> | |
| loggers | <img src='emotes/base/loggers.png' width='32px'> | Y | | | | |
| lul | <img src='emotes/base/lul.png' width='32px'> | Y | | | <img src='emotes/winter/lul.png' width='32px'> | Y |
| monkas | <img src='emotes/base/monkas.png' width='32px'> | | | | <img src='emotes/winter/monkas.png' width='32px'> | |
| nobully | <img src='emotes/base/nobully.png' width='32px'> | Y | | | <img src='emotes/winter/nobully.png' width='32px'> | Y |
| overrustled | <img src='emotes/base/overrustled.png' width='32px'> | Y | | | <img src='emotes/winter/overrustled.png' width='32px'> | Y |
| pepehands | <img src='emotes/base/pepehands.png' width='32px'> | Y | <img src='emotes/fall/pepehands.png' width='32px'> | Y | <img src='emotes/winter/pepehands.png' width='32px'> | Y |
| pepejoke | <img src='emotes/base/pepejoke.png' width='32px'> | | | | | |
| pepelaugh | <img src='emotes/base/pepelaugh.png' width='32px'> | Y | <img src='emotes/fall/pepelaugh.png' width='32px'> | Y | <img src='emotes/winter/pepelaugh.png' width='32px'> | Y |
| peperat | <img src='emotes/base/peperat.png' width='32px'> | Y | | | | |
| pepohmm | <img src='emotes/base/pepohmm.png' width='32px'> | Y | <img src='emotes/fall/pepohmm.png' width='32px'> | Y | <img src='emotes/winter/pepohmm.png' width='32px'> | Y |
| pepojams | <img src='emotes/base/pepojams.png' width='32px'> | Y | | | <img src='emotes/winter/pepojams.png' width='32px'> | |
| peposlash | <img src='emotes/base/peposlash.png' width='32px'> | Y | <img src='emotes/fall/peposlash.png' width='32px'> | N | <img src='emotes/winter/peposlash.png' width='32px'> | Y |
| pepostonks | <img src='emotes/base/pepostonks.png' width='32px'> | Y | | | | |
| pepowant | <img src='emotes/base/pepowant.png' width='32px'> | Y | <img src='emotes/fall/pepowant.png' width='32px'> | N | <img src='emotes/winter/pepowant.png' width='32px'> | N |
| pepoweird | <img src='emotes/base/pepoweird.png' width='32px'> | Y | <img src='emotes/fall/pepoweird.png' width='32px'> | Y | <img src='emotes/winter/pepoweird.png' width='32px'> | Y |
| pikohh | <img src='emotes/base/pikohh.png' width='32px'> | Y | <img src='emotes/fall/pikohh.png' width='32px'> | Y | <img src='emotes/winter/pikohh.png' width='32px'> | Y |
| poggers | <img src='emotes/base/poggers.png' width='32px'> | Y | <img src='emotes/fall/poggers.png' width='32px'> | Y | <img src='emotes/winter/poggers.png' width='32px'> | Y |
| potato | <img src='emotes/base/potato.png' width='32px'> | Y | <img src='emotes/fall/potato.png' width='32px'> | Y | <img src='emotes/winter/potato.png' width='32px'> | Y |
| pepe | | | | | <img src='emotes/winter/pepe.png' width='32px'> | |
| ree | <img src='emotes/base/ree.png' width='32px'> | Y | | | <img src='emotes/winter/ree.png' width='32px'> | Y |
| sidd | <img src='emotes/base/sidd.png' width='32px'> | Y | | | | |
| surprise | <img src='emotes/base/surprise.png' width='32px'> | N | | | | |
| sweaty | <img src='emotes/base/sweaty.png' width='32px'> | Y | <img src='emotes/fall/sweaty.png' width='32px'> | | | |
| tendies | <img src='emotes/base/tendies.png' width='32px'> | Y | | | | |
| thinkies | <img src='emotes/base/thinkies.png' width='32px'> | N | <img src='emotes/fall/thinkies.png' width='32px'> | N | <img src='emotes/winter/thinkies.png' width='32px'> | N |
| whataburger | <img src='emotes/base/whataburger.png' width='32px'> | Y | | | | |
| wow | <img src='emotes/base/wow.png' width='32px'> | Y | | | <img src='emotes/winter/wow.png' width='32px'> | |
| yee | <img src='emotes/base/yee.png' width='32px'> | Y | | | <img src='emotes/winter/yee.png' width='32px'> | Y |
| yellingwoman | <img src='emotes/base/yellingwoman.png' width='32px'> | Y | | | | |
| zoomer | <img src='emotes/base/zoomer.png' width='32px'> | Y | | | <img src='emotes/winter/zoomer.png' width='32px'> | Y |

### Animated Emotes

| Emote Name | Base | Fall | Winter |
|------------|------|------|--------|
| huhh | <img src='emotes/base/animated/huhh.gif' width='32px'> | | |
| ratjam | <img src='emotes/base/animated/ratjam.gif' width='32px'> | <img src='emotes/fall/animated/ratjam.gif' width='32px'> | <img src='emotes/winter/animated/ratjam.gif' width='32px'> |
