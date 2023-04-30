import discord
from discord import app_commands
import json

bws_unit_data_file = 'bws/unitdata.json'
bws_item_data_file = 'bws/itemdata.json'


class UnitButton(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx

    async def on_timeout(self) -> None:
        message = await self.ctx.original_response()
        for i in self.children:
            i.disabled = True
        await message.edit(view=self)

    @discord.ui.button(label='Stats', style=discord.ButtonStyle.blurple, disabled=True)
    async def stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(bws_unit_data_file, 'r') as f:
            unit_json = json.load(f)
            name = interaction.message.embeds[0].to_dict()["title"].lower()
            embed = get_unit_stats_embed(unit_json[name])
            embed.set_thumbnail(url='attachment://' + unit_json[name]['portrait'])
            button_promo = [x for x in self.children if x.label == 'Requirements'][0]
            button_promo.disabled = False
            button.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Requirements', style=discord.ButtonStyle.blurple)
    async def promotion(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(bws_unit_data_file, 'r') as f:
            unit_json = json.load(f)
            name = interaction.message.embeds[0].to_dict()["title"].lower()
            embed = get_unit_requirement_embed(unit_json[name])
            embed.set_thumbnail(url='attachment://' + unit_json[name]['portrait'])
            button_stats = [x for x in self.children if x.label == 'Stats'][0]
            button_stats.disabled = False
            button.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)


async def unit(interaction: discord.Interaction, name: str):
    with open(bws_unit_data_file, 'r') as f:
        unit_json = json.load(f)
        name = name.lower()
        view = UnitButton(interaction)
        if name in unit_json:
            embed = get_unit_stats_embed(unit_json[name])
            portrait = discord.File('bws/images/' + unit_json[name]['portrait'], filename=unit_json[name]['portrait'])
            embed.set_thumbnail(url='attachment://' + unit_json[name]['portrait'])
            await interaction.response.send_message(embed=embed, file=portrait, view=view)
        else:
            await interaction.response.send_message('That unit does not exist', ephemeral=True)


def get_unit_name_choices(ctx: str) -> list[app_commands.Choice]:
    with open(bws_unit_data_file, 'r') as f:
        unit_names = list(json.load(f).keys())
        choices = []
        for name in unit_names:
            if (ctx.lower() in name.lower()) and (len(choices) < 25):
                choices.append(app_commands.Choice(name=name.title(), value=name))
    return choices


def get_unit_stats_embed(unit_json: json) -> discord.Embed:
    embed = discord.Embed(title=unit_json['name'])
    embed.add_field(name='', value='Lvl ' + unit_json['lvl'] + ' ' + unit_json['class'], inline=False)
    bases = ''
    for base in unit_json['base']:
        match base:
            case 'hp':
                bases += 'HP ' + str(unit_json['base'][base]) + ' | '
            case _:
                bases += base.title() + ' ' + str(unit_json['base'][base]) + ' | '
    bases = bases[:-3]
    embed.add_field(name='Bases', value=bases, inline=False)
    if unit_json['growth']:
        growths = ''
        for growth in unit_json['growth']:
            match growth:
                case 'hp':
                    growths += 'HP ' + str(unit_json['growth'][growth]) + '% | '
                case _:
                    growths += growth.title() + ' ' + str(unit_json['growth'][growth]) + '% | '
        growths = growths[:-3]
        if unit_json['bracket']:
            growths += '\n'
            for stat in unit_json['bracket']:
                match stat:
                    case 'hp':
                        growths += 'HP ' + unit_json['bracket'][stat] + ' | '
                    case _:
                        growths += stat.title() + ' ' + unit_json['bracket'][stat] + ' | '
            growths = growths[:-3]
        embed.add_field(name='Growths', value=growths, inline=False)
        if unit_json['promo']:
            promotion = '**' + unit_json['promo']['promo'] + '**\n'
            for stat in unit_json['promo']['bonus']:
                match stat:
                    case 'hp':
                        promotion += 'HP +' + str(unit_json['promo']['bonus'][stat]) + ' | '
                    case _:
                        promotion += stat.title() + ' +' + str(unit_json['promo']['bonus'][stat]) + ' | '
            promotion = promotion[:-3] + '\n'
            for weapon in unit_json['promo']['weapon']:
                promotion += weapon + ' ' + \
                             unit_json['promo']['weapon'][weapon]['base'] + ' ' + \
                             '(' + unit_json['promo']['weapon'][weapon]['growth'] + '%) | '
            promotion = promotion[:-3]
            embed.add_field(name='Promotion', value=promotion, inline=False)
        skills_text = ''
        for skill in unit_json['skill']:
            skills_text += skill + '\n'
        embed.add_field(name='Skills', value=skills_text, inline=True)
        wrank_text = ''
        for rank in unit_json['rank']:
            match rank:
                case 'Sword':
                    wrank_text += '<:bws_sword:1101227974671470652> Sword ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'Spear':
                    wrank_text += '<:bws_spear:1101227953548972133> Spear ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'Knife':
                    wrank_text += '<:bws_knife:1101227906350469141> Knife ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'Axe':
                    wrank_text += '<:bws_axe:1101227837840687114> Axe ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'Bow':
                    wrank_text += '<:bws_bow:1101227856077529200> Bow ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'Crossbow':
                    wrank_text += '<:bws_crossbow:1101227872053624932> Crossbow ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'Fire':
                    wrank_text += '<:bws_fire:1101227895650799679> Fire ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'Thunder':
                    wrank_text += '<:bws_thunder:1101227993248043028> Thunder ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'Wind':
                    wrank_text += '<:bws_wind:1101228008418836540> Wind ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'Light':
                    wrank_text += '<:bws_light:1101227919239553094> Light ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'Dark':
                    wrank_text += '<:bws_dark:1101227885588660364> Dark ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'S Shield':
                    wrank_text += '<:bws_sshield:1101227964269609131> S Shield ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'M Shield':
                    wrank_text += '<:bws_mshield:1101227941221892207> M Shield ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
                case 'L Shield':
                    wrank_text += '<:bws_lshield:1101227930861973595> L Shield ' + str(unit_json['rank'][rank]['base']) + \
                                  ' (' + str(unit_json['rank'][rank]['growth']) + '%) \n'
        wrank_text = wrank_text[:-1]
        embed.add_field(name='Weapon Skills', value=wrank_text, inline=True)
    return embed


def get_unit_requirement_embed(unit_json: json):
    embed = discord.Embed(title=str(unit_json['name']))
    recruitment = ''
    if unit_json['misc']['recruit']:
        recruitment += unit_json['misc']['recruit']
        embed.add_field(name='Recruitment', value=recruitment, inline=False)
    promotion = ''
    if unit_json['misc']['promo']:
        promotion += unit_json['misc']['promo']
        embed.add_field(name='Promotion', value=promotion, inline=False)
    preferentials = ''
    if unit_json['misc']['prf']:
        preferentials += unit_json['misc']['prf']
        embed.add_field(name='Preferentials', value=preferentials, inline=False)
    return embed


async def item(interaction: discord.Interaction, name: str):
    with open(bws_item_data_file, 'r') as f:
        item_json = json.load(f)
        if name in item_json:
            embed = get_item_stats_embed(item_json[name])
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message('That item does not exist', ephemeral=True)


def get_item_name_choices(ctx: str) -> list[app_commands.Choice]:
    with open(bws_item_data_file, 'r') as f:
        item_json = list(json.load(f).keys())
        choices = []
        for name in item_json:
            if (ctx.lower() in name.lower()) and (len(choices) < 25):
                choices.append(app_commands.Choice(name=name, value=name))
    return choices


def get_item_stats_embed(item_json: json):
    embed = discord.Embed(title=item_json['name'])
    stats = ''
    for value in item_json:
        match value:
            case 'might':
                stats += 'Mt ' + item_json['might'] + ' | '
            case 'def':
                stats += 'Def ' + str(item_json['def']) + ' | '
            case 'hit':
                stats += 'Hit ' + str(item_json['hit'] * 10) + ' | '
            case 'weight':
                stats += 'Wt ' + str(item_json['weight']) + ' | '
            case 'rank':
                stats += 'Rank ' + str(item_json['rank']) + ' | '
            case 'range':
                stats += 'Rng ' + item_json['range'] + ' | '
    stats = stats[:-3] + '\n'
    for value in item_json:
        match value:
            case 'durability':
                stats += 'Durability ' + item_json['durability'] + ' | '
            case 'usecount':
                stats += 'Uses ' + str(item_json['usecount']) + ' | '
            case 'cost':
                stats += 'Cost ' + str(item_json['cost']) + ' D. | '
            case 'prf':
                stats += item_json['prf'] + ' Prf | '
    stats = stats[:-3]
    embed.add_field(name='', value=stats, inline=False)
    for value in item_json:
        match value:
            case 'effect':
                effect = item_json['effect']
                embed.add_field(name='Notes:', value=effect, inline=False)
    return embed
