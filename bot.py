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
        helpembed.add_field(name='', value='This bot displays information for Berwick Saga and TearRing Saga.\n\n'
                                           'It only supports slash commands and you can see all avaiable ones '
                                           'by typing `/`.', inline=False)
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
        await bws.item(interaction, item)

    @item.autocomplete('item')
    async def item_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return bws.get_item_name_choices(current)

    @app_commands.command(name='skill', description='Get Berwick Saga skill data')
    async def skill(self, interaction: discord.Interaction, skill: str):
        await bws.skill(interaction, skill)

    @skill.autocomplete('skill')
    async def skill_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return bws.get_skill_name_choices(current)

    @app_commands.command(name='furniture', description='Get Berwick Saga furniture data')
    async def furniture(self, interaction: discord.Interaction, furniture: str):
        await bws.furniture(interaction, furniture)

    @furniture.autocomplete('furniture')
    async def furniture_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return bws.get_furniture_name_choices(current)

    @app_commands.command(name='food', description='Get Berwick Saga food data')
    async def food(self, interaction: discord.Interaction, food: str):
        await bws.food(interaction, food)

    @food.autocomplete('food')
    async def food_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return bws.get_food_name_choices(current)


bot.tree.add_command(Berwick(name='bws', description='Berwick Data'))


class TearRing(app_commands.Group):

    @app_commands.command(name='unit', description='Get TearRing Saga unit data')
    async def unit(self, interaction: discord.Interaction, unit: str):
        await trs.unit(interaction, unit)

    @unit.autocomplete('unit')
    async def unit_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return trs.get_unit_name_choices(current)


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
