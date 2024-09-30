import disnake
import asyncio 
import requests
import urllib.parse
import json
from disnake.ext import commands
from modules import fox

config: dict

with open('config.json') as f:
    config = json.load(f)

print(config)

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.Bot(
    command_prefix="??",
    test_guilds=config["TEST_GUILDS"],
    command_sync_flags=command_sync_flags
)

@bot.slash_command(description="Sends a fox image!")
async def fox(inter):
    image = requests.get("https://randomfox.ca/floof/").json()["image"]
    embed = disnake.Embed()
    embed.set_image(image)
    await inter.response.send_message(embed=embed)

@bot.slash_command(description="Asks WolframAlpha")
async def wa(inter, prompt: str):
    await inter.response.defer()
    image = requests.get(f"http://api.wolframalpha.com/v1/simple?appid={config['APPID']}&i={urllib.parse.quote_plus(prompt)}")
    with open('image.jpg','wb') as f:
        f.write(image.content)
    embed = disnake.Embed()
    embed.set_image(file=disnake.File("image.jpg"))
    asyncio.sleep(15)
    await inter.followup.send(embed=embed)

bot.run(config['TOKEN'])