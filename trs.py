import discord
from discord import app_commands
import json

trs_unit_data_file = 'trs/unitdata.json'


async def unit(interaction: discord.Interaction, name: str):
    with open(trs_unit_data_file, 'r') as f:
        unit_json = json.load(f)
        name = name.lower()
        if name in unit_json:
            embed = get_unit_stats_embed(unit_json[name])
            portrait = discord.File('trs/images/' + unit_json[name]['portrait'], filename=unit_json[name]['portrait'])
            embed.set_thumbnail(url='attachment://' + unit_json[name]['portrait'])
            await interaction.response.send_message(embed=embed, file=portrait)
        else:
            await interaction.response.send_message('That unit does not exist', ephemeral=True)


def get_unit_name_choices(ctx: str) -> list[app_commands.Choice]:
    with open(trs_unit_data_file, 'r') as f:
        unit_names = list(json.load(f).keys())
        choices = []
        for name in unit_names:
            if (ctx.lower() in name.lower()) and (len(choices) < 25):
                choices.append(app_commands.Choice(name=name.title(), value=name))
    return choices


def get_unit_stats_embed(unit_json: json) -> discord.Embed:
    embed = discord.Embed(title=unit_json['name'])
    embed.add_field(name='', value=unit_json['job'], inline=False)
    embed.add_field(name='Bases', value=unit_json['Bases'], inline=False)
    embed.add_field(name='Growths', value=unit_json['Growths'], inline=False)
    for value in unit_json:
        match value:
            case 'Promotion':
                embed.add_field(name='Promotion', value=unit_json['Promotion'], inline=False)
            case 'Skills':
                embed.add_field(name='Skills', value=unit_json['Skills'], inline=True)
    embed.add_field(name='Weapon Ranks', value=unit_json['Weapons'], inline=True)
    return embed
