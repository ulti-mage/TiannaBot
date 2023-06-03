import typing

import discord
from discord import app_commands
from discord.ext import commands
import json
import bws
import trs

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

bws_unit_data_file = 'bws/unitdata.json'
bws_item_data_file = 'bws/itemdata.json'
bws_skill_data_file = 'bws/skilldata.json'
bws_furniture_data_file = 'bws/furnituredata.json'
bws_food_data_file = 'bws/fooddata.json'

trs_unit_data_file = 'trs/unitdata.json'
trs_class_data_file = 'trs/classdata.json'
trs_item_data_file = 'trs/itemdata.json'
trs_skill_data_file = 'trs/skilldata.json'


def get_name_choices(ctx: str, file: str) -> list[app_commands.Choice]:
    with open(file, 'r') as f:
        name_json = json.load(f)
        choices = []
        for k in name_json:
            if (ctx.lower() in name_json[k]['name'].lower()) and (len(choices) < 25):
                choices.append(app_commands.Choice(name=name_json[k]['name'], value=name_json[k]['name']))
    return choices


class General(app_commands.Group):

    @app_commands.command(name='help', description="This is the Help Command")
    async def tiannahelp(self, interaction: discord.Interaction):
        helpembed = discord.Embed(title="TiannaBot")
        helpembed.add_field(name='', value='This bot displays information for Berwick Saga and TearRing Saga.\n\n'
                                           'It only supports slash commands and you can see all avaiable ones '
                                           'by typing `/`.', inline=False)
        links = '[GitHub](https://github.com/ulti-mage/TiannaBot)\n' \
                '[Discord](https://discord.gg/g5r3qdYfFj)\n' \
                '[Bot Invite Link](https://discord.com/api/oauth2/authorize?client_id=1099678821084581919&permissions=274878220288&scope=bot)'
        helpembed.add_field(name='Links:', value=links, inline=False)
        await interaction.response.send_message(embed=helpembed)


bot.tree.add_command(General(name='tianna', description='General TiannaBot commands'))


class Berwick(app_commands.Group):
    @app_commands.command(name='unit', description='Get Berwick Saga unit data')
    async def unit(self, interaction: discord.Interaction, name: str, level: typing.Optional[int] = None,
                   promoted: typing.Optional[bool] = None):
        await bws.unit(interaction, name, level, promoted)

    @unit.autocomplete('name')
    async def unit_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, bws_unit_data_file)

    @app_commands.command(name='item', description='Get Berwick Saga item data')
    async def item(self, interaction: discord.Interaction, name: str):
        await bws.item(interaction, name)

    @item.autocomplete('name')
    async def item_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, bws_item_data_file)

    @app_commands.command(name='skill', description='Get Berwick Saga skill data')
    async def skill(self, interaction: discord.Interaction, name: str):
        await bws.skill(interaction, name)

    @skill.autocomplete('name')
    async def skill_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, bws_skill_data_file)

    @app_commands.command(name='furniture', description='Get Berwick Saga furniture data')
    async def furniture(self, interaction: discord.Interaction, name: str):
        await bws.furniture(interaction, name)

    @furniture.autocomplete('name')
    async def furniture_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, bws_furniture_data_file)

    @app_commands.command(name='food', description='Get Berwick Saga food data')
    async def food(self, interaction: discord.Interaction, name: str):
        await bws.food(interaction, name)

    @food.autocomplete('name')
    async def food_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, bws_food_data_file)


bot.tree.add_command(Berwick(name='bws', description='Berwick Data'))


class TearRing(app_commands.Group):

    @app_commands.command(name='unit', description='Get TearRing Saga unit data')
    async def unitdata(self, interaction: discord.Interaction, name: str,
                       personal: typing.Optional[bool] = False,
                       classname: typing.Optional[str] = None,
                       level: typing.Optional[int] = None,
                       promoted: typing.Optional[bool] = None,
                       reeve: typing.Optional[bool] = False,
                       salia: typing.Optional[bool] = False):
        await trs.unit(interaction, name, personal, classname, level, promoted, reeve, salia)

    @unitdata.autocomplete('name')
    async def unit_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, trs_unit_data_file)

    @unitdata.autocomplete('classname')
    async def class_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, trs_class_data_file)

    @app_commands.command(name='class', description='Get TearRing Saga class data')
    async def classdata(self, interaction: discord.Interaction, name: str):
        await trs.classdata(interaction, name)

    @classdata.autocomplete('name')
    async def class_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, trs_class_data_file)

    @app_commands.command(name='skill', description='Get TearRing Saga skill data')
    async def skilldata(self, interaction: discord.Interaction, name: str):
        await trs.skill(interaction, name)

    @skilldata.autocomplete('name')
    async def skill_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, trs_skill_data_file)

    @app_commands.command(name='item', description='Get TearRing Saga item data')
    async def itemdata(self, interaction: discord.Interaction, name: str):
        await trs.item(interaction, name)

    @itemdata.autocomplete('name')
    async def skill_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, trs_item_data_file)


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
