import os
import json
from traceback import print_tb
import discord

from cogs.crystal import CrystalView

# Load our config file
with open('config.json', "r") as config:
    data = json.load(config)

GUILD = discord.Object(id=data['guild'])

from discord.ext import commands

class Test(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!!", intents=discord.Intents.all())

    async def on_ready(self):
        print(f'I\'m back bitch!')
    
    async def setup_hook(self) -> None:
        self.add_view(CrystalView())
        for f in os.listdir('./cogs'):
            if f.endswith('.py'):
                await self.load_extension(f'cogs.{f[:-3]}')

client = Test()
client.run(data['token'])