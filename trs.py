import discord
from discord import app_commands
import json

trs_unit_data_file = 'trs/unitdata.json'


def get_unit_name_list(ctx: str) -> list[app_commands.Choice]:
    with open(trs_unit_data_file, 'r') as f:
        unit_names = list(json.load(f).keys())
        choices = []
        for name in unit_names:
            if (ctx.lower() in name.lower()) and (len(choices) < 25):
                choices.append(app_commands.Choice(name=name.title(), value=name))
    return choices
