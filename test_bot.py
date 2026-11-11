"""Offline check of which emote files the bot picks per season. Never connects to Discord.

Run: python test_bot.py   (needs requirements.txt installed; bot.py imports discord)
"""
import os

from bot import MAX_EMOTE_BYTES, select_emotes

FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emotes")


def rel(path):
    return os.path.relpath(path, FOLDER).replace(os.sep, "/")


base, seasonal = select_emotes(FOLDER, "base")
fall, _ = select_emotes(FOLDER, "fall")
winter, _ = select_emotes(FOLDER, "winter")

# animated/ is read
assert rel(base["catjam"]) == "base/animated/catjam.gif"
# base never pulls from an overlay
assert all(rel(p).startswith("base/") for p in base.values())
# overlays win for their names, base fills the rest
assert rel(fall["ratjam"]) == "fall/animated/ratjam.gif"
assert rel(winter["ratjam"]) == "winter/animated/ratjam.gif"
assert rel(fall["comfycat"]) == "fall/comfycat.png"
assert rel(winter["apes"]) == "winter/apes.png"
assert rel(fall["apes"]) == "base/apes.png"
assert rel(winter["bigbrain"]) == "base/bigbrain.png"
# every season holds the full base set
assert set(base) <= set(fall) and set(base) <= set(winter)
# swap list: names with any overlay version, so going back to base restores them
assert {"ratjam", "comfycat", "apes"} <= seasonal
assert "bigbrain" not in seasonal and "catjam" not in seasonal
# every overlay feeds the swap list, not just one (sweaty is fall-only, apes winter-only)
assert "sweaty" in seasonal and "apes" in seasonal
# the cap is Discord's 256 KB
assert MAX_EMOTE_BYTES == 256 * 1024
# nothing in the library is over Discord's cap
for season in (base, fall, winter):
    for path in season.values():
        assert os.path.getsize(path) <= MAX_EMOTE_BYTES, path

print(f"OK: base {len(base)}, fall {len(fall)}, winter {len(winter)}, seasonal {len(seasonal)}")
