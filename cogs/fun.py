import json
from urllib.request import urlopen

from discord.ext import commands

def fetch_image(query='wine', /):
    url = urlopen(f'https://api.unsplash.com/photos/random?query={query}&client_id=BXuTAPKsP6M1eAy2s0sCOEb4MV1MNx0cmIBkiGn23hg').read()
    image = json.loads(url)
    return image['urls']['regular']

class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='wine')
    async def wine(self, ctx):
        await ctx.send(fetch_image('wine'))

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))