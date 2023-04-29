import discord
from discord import app_commands
from discord.ext import commands
import bws
import trs

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())


class General(app_commands.Group):

    @app_commands.command(name='help', description="This is the Help Command")
    async def tiannahelp(self, interaction: discord.Interaction):
        helpembed = discord.Embed(title="TiannaBot")
        helpembed.add_field(name='', value='This bot displays information for Berwick Saga (and TearRing Saga soon)', inline=False)
        avaiable_commands = '/bws unit [name] : Get BWS unit data\n' +\
                            '/bws item [name] : Get BWS item data : NYI\n' + \
                            '/trs unit [name] : Get TRS unit data : NYI'
        helpembed.add_field(name='Avaiable Commands: (WIP)', value=avaiable_commands, inline=False)
        await interaction.response.send_message(embed=helpembed)


bot.tree.add_command(General(name='tianna', description='General TiannaBot commands'))


class Berwick(app_commands.Group):
    @app_commands.command(name='unit', description='Get Berwick Saga unit data')
    async def unit(self, interaction: discord.Interaction, unit: str):
        await bws.unit(interaction, unit)

    @unit.autocomplete('unit')
    async def unit_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return bws.get_unit_name_choices(current)

    @app_commands.command(name='item', description='Get Berwick Saga item data')
    async def item(self, interaction: discord.Interaction, item: str):
        await interaction.response.send_message(f"Item: {item}. This is not implemented yet!")


bot.tree.add_command(Berwick(name='bws', description='Berwick Data'))


class TearRing(app_commands.Group):

    @app_commands.command(name='unit', description='Get TearRing Saga unit data')
    async def unit(self, interaction: discord.Interaction, unit: str):
        await interaction.response.send_message(f"Unit: {unit}. " f"This is not implemented yet!")

    @unit.autocomplete('unit')
    async def unit_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return trs.get_unit_name_list(current)


bot.tree.add_command(TearRing(name='trs', description='TearRing Data'))


@bot.event
async def on_ready():
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

with open('TOKEN.txt') as TOKENFILE:
    TOKEN = TOKENFILE.read()

bot.run(TOKEN)
