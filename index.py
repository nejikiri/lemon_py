import os
import discord

from cogs.crystal import CrystalView
from discord.ext import commands

GUILD = discord.Object(id=771811457498218519)

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
client.run('MTAxODc1MjkxMzkzOTY0NDQ0Ng.Gnjk0Z.9CTwlTpSg7w9l_Z2FL_OLcLRHi-j6evXdxcNQs')
# MTAxNzE2NDgyNjAyOTYwNDk0NQ.GASe2V.XFhPGjQF0hbbeEkpn3-SOyI5olOJqRwZXK-BCY