import os
import json
import random
import discord

from discord.ext import commands, tasks

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
        role = discord.utils.get(interaction.guild.roles, name="Has Viewed Crystal")
        if role in interaction.user.roles:
            await interaction.response.send_message("Please wait till tomorrow to use this feature.", ephemeral=True)
        await interaction.user.add_roles(role)
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
        channel = self.bot.get_channel(int(1018744463545339924))
        await channel.send("The crystal of the day is ready!", view=CrystalView())

    @tasks.loop(hours=24)
    async def crystal(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(int(771811457498218519))
        role = discord.utils.get(guild.roles, name="Has Viewed Crystal")
        for m in guild.members:
            if role in m.roles:
                await m.remove_roles(role)

    @tasks.loop(hours=24)
    async def delete_last_crystal_view(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(int(1018744463545339924))
        last_msg = await channel.fetch_message(channel.last_message_id)
        await last_msg.delete()
	# Post new crystal of the day view.
	await channel.send("The crystal of the day is ready!", view=CrystalView())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Crystal(bot))
