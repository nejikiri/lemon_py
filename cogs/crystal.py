import os
import json
import random
import discord

from __init__ import selection, DB
from discord.ext import commands, tasks

# Load out config file
with open(os.getcwd() + '/config.json') as config:
    data = json.load(config)

class CrystalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    def select_crystal(self):
        path = os.getcwd() + '/crystals.json'
        with open(path) as crystals:
            data = json.load(crystals)
            crystal = random.choice(list(data['crystals']))
            return crystal['name'] + ": " + crystal['description']

    @discord.ui.button(label="View Crystal", style=discord.ButtonStyle.blurple, custom_id="crystalpersist:purple")
    async def show_crystal(self, interaction: discord.Interaction, button: discord.Button):
        selection.execute("SELECT * FROM crystal")
        result = selection.fetchall()
        for x in result:
            if x[0] == interaction.user.name and x[1] == True:
                await interaction.response.send_message("Please wait till tomorrow to use this feature.", ephemeral=True)
            elif x[0] == interaction.user.name and x[1] == False:
                update = "UPDATE crystal SET viewed = '{0}' WHERE user = '{1}'".format(1, interaction.user.name)
                selection.execute(update)
                DB.commit()
                await interaction.response.send_message(f'{self.select_crystal()}', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Button, /) -> None:
        # On error do nothing.
        return

class Crystal(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.crystal.start()
        self.delete_last_crystal_view.start()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()

    @tasks.loop(hours=24)
    async def crystal(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(int(data['guild']))
        for m in guild.members:
            update = "UPDATE crystal SET viewed = '{0}' WHERE user = '{1}'".format(0, m.name)
            selection.execute(update)
            DB.commit()
            
    @tasks.loop(hours=24)
    async def delete_last_crystal_view(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(int(data['crystal_channel']))
        async for m in channel.history(limit=1):
            if m:
                await m.delete()
                await channel.send("The crystal of the day is ready!", view=CrystalView())


async def setup(bot: commands.Bot) -> None: 
    await bot.add_cog(Crystal(bot))
