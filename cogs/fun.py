import os
import json

from urllib.request import urlopen
from discord.ext import commands

# Load out config file
with open(os.getcwd() + '/config.json') as config:
    data = json.load(config)

def fetch_image(query='wine', /):
    unsplash_id = data['unsplash_id']
    url = urlopen(f'https://api.unsplash.com/photos/random?query={query}&client_id={unsplash_id}').read()
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