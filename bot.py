import typing

import discord
from discord import app_commands
from discord.ext import commands
import json
import bws
import trs
import vs1
import vs2
import fe3


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

vs1_unit_data_file = 'vs1/unitdata.json'
vs1_class_data_file = 'vs1/classdata.json'
vs1_item_data_file = 'vs1/itemdata.json'
vs1_skill_data_file = 'vs1/skilldata.json'

vs2_unit_data_file = 'vs2/unitdata.json'
vs2_item_data_file = 'vs2/itemdata.json'
vs2_skill_data_file = 'vs2/skilldata.json'

fe3b1_unit_data_file = 'fe3/b1.json'
fe3b2_unit_data_file = 'fe3/b2.json'
bsfe_unit_data_file = 'fe3/bsfe.json'

fe3_item_data_file = 'fe3/item.json'
fe3_class_data_file = 'fe3/job.json'


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
        helpembed.add_field(name='', value='This bot displays information for Berwick, TearRing and Vestaria Saga I and II.\n\n'
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


class VestariaSagaI(app_commands.Group):
    @app_commands.command(name='unit', description='Get Vestaria Saga I unit data')
    async def unitdata(self, interaction: discord.Interaction, name: str,
                       level: typing.Optional[str] = None,
                       veldland: typing.Optional[bool] = False,
                       frallian: typing.Optional[bool] = False,
                       prison: typing.Optional[bool] = False):
        await vs1.unit(interaction, name, level, veldland, frallian, prison)

    @unitdata.autocomplete('name')
    async def unit_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, vs1_unit_data_file)

    @app_commands.command(name='class', description='Get Vestaria Saga I class data')
    async def classdata(self, interaction: discord.Interaction, name: str):
        await vs1.classdata(interaction, name)

    @classdata.autocomplete('name')
    async def class_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, vs1_class_data_file)

    @app_commands.command(name='skill', description='Get Vestaria Saga I skill data')
    async def skilldata(self, interaction: discord.Interaction, name: str):
        await vs1.skill(interaction, name)

    @skilldata.autocomplete('name')
    async def skill_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, vs1_skill_data_file)

    @app_commands.command(name='item', description='Get Vestaria Saga I item data')
    async def itemdata(self, interaction: discord.Interaction, name: str):
        await vs1.item(interaction, name)

    @itemdata.autocomplete('name')
    async def skill_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, vs1_item_data_file)


bot.tree.add_command(VestariaSagaI(name='vs1', description='Vestaria Saga I Data'))


class VestariaSagaII(app_commands.Group):
    @app_commands.command(name='unit', description='Get Vestaria Saga II unit data')
    async def unitdata(self, interaction: discord.Interaction, name: str,
                       level: typing.Optional[int] = None,
                       promoted: typing.Optional[bool] = False):
        await vs2.unit(interaction, name, level, promoted)

    @unitdata.autocomplete('name')
    async def unit_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, vs2_unit_data_file)

    @app_commands.command(name='skill', description='Get Vestaria Saga II skill data')
    async def skilldata(self, interaction: discord.Interaction, name: str):
        await vs2.skill(interaction, name)

    @skilldata.autocomplete('name')
    async def skill_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, vs2_skill_data_file)

    @app_commands.command(name='item', description='Get Vestaria Saga II item data')
    async def itemdata(self, interaction: discord.Interaction, name: str):
        await vs2.item(interaction, name)

    @itemdata.autocomplete('name')
    async def skill_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, vs2_item_data_file)


bot.tree.add_command(VestariaSagaII(name='vs2', description='Vestaria Saga II Data'))


class FE3B1(app_commands.Group):
    @app_commands.command(name='unit', description='Get FE3 Book 1 unit data')
    async def unitdata(self, interaction: discord.Interaction, name: str,
                       level: typing.Optional[str] = None,
                       personal: typing.Optional[bool] = False,
                       shards: typing.Optional[str] = None):
        await fe3.unit(interaction, name, level, personal, 'b1', shards)

    @unitdata.autocomplete('name')
    async def unit_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, fe3b1_unit_data_file)


bot.tree.add_command(FE3B1(name='fe3b1', description='FE3 Book 1 Data'))


class FE3B2(app_commands.Group):
    @app_commands.command(name='unit', description='Get FE3 Book 2 unit data')
    async def unitdata(self, interaction: discord.Interaction, name: str,
                       level: typing.Optional[str] = None,
                       personal: typing.Optional[bool] = False,
                       shards: typing.Optional[str] = None):
        await fe3.unit(interaction, name, level, personal, 'b2', shards)

    @unitdata.autocomplete('name')
    async def unit_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, fe3b2_unit_data_file)


bot.tree.add_command(FE3B2(name='fe3b2', description='FE3 Book 2 Data'))


class BSFE(app_commands.Group):
    @app_commands.command(name='unit', description='Get BSFE unit data')
    async def unitdata(self, interaction: discord.Interaction, name: str,
                       level: typing.Optional[str] = None,
                       personal: typing.Optional[bool] = False):
        await fe3.unit(interaction, name, level, personal, 'bsfe')

    @unitdata.autocomplete('name')
    async def unit_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, bsfe_unit_data_file)


bot.tree.add_command(BSFE(name='bsfe', description='BSFE Data'))


class FE3(app_commands.Group):
    @app_commands.command(name='item', description='Get FE3 item data')
    async def itemdata(self, interaction: discord.Interaction, name: str):
        await fe3.item(interaction, name)

    @itemdata.autocomplete('name')
    async def skill_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, fe3_item_data_file)

    @app_commands.command(name='class', description='Get FE3 class data')
    async def classdata(self, interaction: discord.Interaction, name: str):
        await fe3.classdata(interaction, name)

    @classdata.autocomplete('name')
    async def class_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return get_name_choices(current, fe3_class_data_file)


bot.tree.add_command(FE3(name='fe3', description='FE3 Data'))





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
