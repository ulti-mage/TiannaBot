import discord
from discord import app_commands
import json

trs_unit_data_file = 'trs/unitdata.json'
trs_class_data_file = 'trs/classdata.json'
trs_item_data_file = 'trs/itemdata.json'
trs_skill_data_file = 'trs/skilldata.json'


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
        name = interaction.message.embeds[0].to_dict()["title"].lower()
        unit_json = get_unit_json(name)
        base_class_json = get_class_json(unit_json['class'])
        promo_class_json = promo2_class_json = None
        if 'promo' in unit_json:
            promo_class_json = get_class_json(unit_json['promo']['promo'])
        if 'promo2' in unit_json:
            promo2_class_json = get_class_json(unit_json['promo2']['promo'])
        embed = get_unit_stats_embed(unit_json, False, base_class_json, False, False, False,
                                     promo_class_json, promo2_class_json)
        embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
        for i in self.children:
            if i.label != 'Stats':
                i.disabled = False
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Supports', style=discord.ButtonStyle.blurple)
    async def support(self, interaction: discord.Interaction, button: discord.ui.Button):
        name = interaction.message.embeds[0].to_dict()["title"].lower()
        unit_json = get_unit_json(name)
        embed = get_unit_support_embed(unit_json)
        embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
        for i in self.children:
            if i.label != 'Supports':
                i.disabled = False
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Other', style=discord.ButtonStyle.blurple)
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        name = interaction.message.embeds[0].to_dict()["title"].lower()
        unit_json = get_unit_json(name)
        embed = get_unit_requirement_embed(unit_json)
        embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
        for i in self.children:
            if i.label != 'Other':
                i.disabled = False
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)


async def unit(interaction: discord.Interaction, name: str, personal: bool, classname: str, level: int,
               promoted: bool, reeve: bool, salia: bool):
    unit_json = get_unit_json(name)
    view = UnitButton(interaction)
    if unit_json is None:
        await interaction.response.send_message('That unit does not exist', ephemeral=True)
    else:

        promo_class_json = promo2_class_json = None
        alternate_class_flag = False

        if classname is None:
            base_class_json = get_class_json(unit_json['class'])
            if 'promo' in unit_json:
                promo_class_json = get_class_json(unit_json['promo']['promo'])
            if 'promo2' in unit_json:
                promo2_class_json = get_class_json(unit_json['promo2']['promo'])
        else:
            alternate_class_flag = True
            base_class_json = get_class_json(classname)

        if base_class_json is None:
            await interaction.response.send_message('That class does not exist', ephemeral=True)
        else:
            if level is None and promoted is None and classname is None \
                    and promoted is None and reeve is False and salia is False:
                embed = get_unit_stats_embed(unit_json, False, base_class_json, False,
                                             False, False, promo_class_json, promo2_class_json)
                portrait = discord.File('trs/images/' + unit_json['portrait'], filename=unit_json['portrait'])
                embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
                await interaction.response.send_message(embed=embed, file=portrait, view=view)
            elif level is None and promoted is None:
                embed = get_unit_stats_embed(unit_json, personal, base_class_json, alternate_class_flag,
                                             reeve, salia, promo_class_json, promo2_class_json)
                portrait = discord.File('trs/images/' + unit_json['portrait'], filename=unit_json['portrait'])
                embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
                await interaction.response.send_message(embed=embed, file=portrait)
            else:
                if level is None:
                    level = 0
                embed = get_unit_level_embed(unit_json, personal, base_class_json, alternate_class_flag, level,
                                             promoted, reeve, salia)
                portrait = discord.File('trs/images/' + unit_json['portrait'], filename=unit_json['portrait'])
                embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
                await interaction.response.send_message(embed=embed, file=portrait)


def get_unit_json(name: str) -> json:
    with open(trs_unit_data_file, 'r') as f:
        unit_json = json.load(f)
        for k in unit_json:
            if k.lower().startswith(name.lower()):
                return unit_json[k]
        return None


def get_class_json(ctx: str) -> json:
    with open(trs_class_data_file, 'r') as f:
        class_json = json.load(f)
        for k in class_json:
            if class_json[k]['name'].lower() == ctx.lower():
                return class_json[k]
        for k in class_json:
            if (k == ctx) or (class_json[k]['name'].lower().startswith(ctx.lower())):
                return class_json[k]
        return None


def get_unit_stats_embed(unit_json: json, personal: bool, base_class: json, alternate_class_flag: bool,
                         reeve: bool, salia: bool, promo_class=None, promo2_class=None) -> discord.Embed:
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
    header = 'Lvl ' + str(unit_json['lvl']) + ' ' + base_class['name']
    if personal:
        header += '\n **Personal Stats**'
    embed.add_field(name='', value=header, inline=False)

    bases = ''
    for base in unit_json['base']:
        if personal:
            val = unit_json['base'][base]
        else:
            val = unit_json['base'][base] + base_class['base'][base]
        match base:
            case 'hp':
                if val >= 60:
                    bases += 'HP **60** | '
                else:
                    bases += 'HP ' + str(val) + ' | '
            case 'luck':
                if val >= 30:
                    bases += 'Luck **30** | '
                else:
                    bases += 'Luck ' + str(val) + ' | '
            case 'move':
                if val >= 12:
                    bases += 'Move **12** | '
                elif base_class == 'ballistician' or base_class == 'catapulter':
                    bases += 'Move **0** | '
                else:
                    bases += 'Move ' + str(val) + ' | '
            case _:
                if personal and val >= 15:
                    bases += base.title() + ' **15** | '
                elif not personal and val >= base_class['base'][base] + 15:
                    bases += base.title() + ' **' + str(base_class['base'][base] + 15) + '** | '
                else:
                    bases += base.title() + ' ' + str(val) + ' | '
    bases = bases[:-3]
    embed.add_field(name='Bases', value=bases, inline=False)

    growthname = 'Growths'
    if reeve or salia:
        if reeve:
            growthname += ' + Reeve Codex'
        if salia:
            growthname += ' + Salia Codex'

    if unit_json['growth']:
        growths = ''
        for growth in unit_json['growth']:
            bonus = 0
            match growth:
                case 'hp':
                    if reeve:
                        bonus = 10
                    growths += 'HP ' + str(unit_json['growth'][growth] + bonus) + '% | '
                case _:
                    if (reeve and growth in ['luck', 'mag', 'mst']) or (
                            salia and growth in ['str', 'skl', 'spd', 'def']):
                        bonus = 10
                    growths += growth.title() + ' ' + str(unit_json['growth'][growth] + bonus) + '% | '
        growths = growths[:-3]
        embed.add_field(name=growthname, value=growths, inline=False)

    if promo_class is not None:
        promotext = '**' + promo_class['name'] + '**\n'
        promotionwrank = ''

        for stat in promo_class['base']:
            val = promo_class['base'][stat] - base_class['base'][stat]
            if val > 0:
                valstr = '+' + str(val)
            else:
                valstr = str(val)
            if val != 0:
                match stat:
                    case 'hp':
                        promotext += 'HP ' + valstr + ' | '
                    case _:
                        promotext += stat.title() + ' ' + valstr + ' | '
        promotext = promotext[:-3]

        if 'weapon' in unit_json['promo']:
            for weapon in unit_json['promo']['weapon']:
                promotionwrank += weapon + ' | '

            promotext += '\n+' + promotionwrank[:-3]

        if promo2_class is not None:
            promotext += '\n**' + promo2_class['name'] + '**\n'
            promotionwrank = ''

            for stat in promo2_class['base']:
                val = promo2_class['base'][stat] - promo_class['base'][stat]
                if val > 0:
                    valstr = '+' + str(val)
                else:
                    valstr = str(val)
                if val != 0:
                    match stat:
                        case 'hp':
                            promotext += 'HP ' + valstr + ' | '
                        case _:
                            promotext += stat.title() + ' ' + valstr + ' | '
            promotext = promotext[:-3]

            if 'weapon' in unit_json['promo2']:
                for weapon in unit_json['promo2']['weapon']:
                    promotionwrank += weapon + ' | '

                promotext += '\n+' + promotionwrank[:-3]

        embed.add_field(name='Promotion', value=promotext, inline=False)

    skills_text = ''
    if alternate_class_flag:
        for skill in base_class['skill']:
            skills_text += skill + '\n'
    else:
        for skill in unit_json['skill']:
            skills_text += skill + '\n'

    embed.add_field(name='Skills', value=skills_text, inline=True)

    weapons = ''
    if alternate_class_flag:
        for rank in base_class['weapon']:
            weapons += rank + '\n'
    else:
        for rank in unit_json['weapon']:
            weapons += rank + '\n'

    embed.add_field(name='Weapons', value=weapons, inline=True)
    return embed


def get_unit_level_embed(unit_json: json, personal: bool, base_class: json, alternate_class_flag: bool, level: int,
                         promoted: bool, reeve: bool, salia: bool):
    promo_class = None
    if 'promo' in unit_json:
        promo_class = get_class_json(unit_json['promo']['promo'])

    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
    level = max(min(level, 40), unit_json['lvl'])
    levelstr = '**Lvl ' + str(unit_json['lvl']) + '** '
    if level != unit_json['lvl']:
        levelstr += '**-> ' + str(level) + '** '
    levelstr += base_class['name']
    if promoted and 'promo' in unit_json and not alternate_class_flag:
        levelstr += ' -> ' + promo_class['name']
    embed.add_field(name='', value=levelstr, inline=False)

    header = ''
    if personal:
        header += '\n **Personal Stats**'
    embed.add_field(name='', value=header, inline=False)

    if reeve or salia:
        codex = ''
        if reeve:
            codex += 'Reeve Codex | '
        if salia:
            codex += 'Salia Codex | '
        codex = codex[:-3]
        embed.add_field(name='', value=codex, inline=False)

    lvlinc = level - unit_json['lvl']
    stats = ''
    for stat in unit_json['base']:
        match stat:
            case 'hp':
                boost = 0
                if reeve:
                    boost = 10
                val = ((unit_json['growth'][stat] + boost) * lvlinc + (unit_json['base'][stat] * 100)) / 100
                if not personal:
                    val += base_class['base'][stat]
                if promoted and 'promo' in unit_json:
                    val += promo_class['base'][stat] - base_class['base'][stat]
                if val >= 60:
                    stats += 'HP **60** | '
                else:
                    stats += 'HP ' + str(val) + ' | '

            case _:
                boost = 0
                if (reeve and stat in ['luck', 'mag', 'mst']) or (salia and stat in ['str', 'skl', 'spd', 'def']):
                    boost = 10
                val = ((unit_json['growth'][stat] + boost) * lvlinc + (unit_json['base'][stat] * 100)) / 100
                if not personal:
                    val += base_class['base'][stat]
                if promoted and 'promo' in unit_json:
                    val += promo_class['base'][stat] - base_class['base'][stat]

                if stat == 'luck':
                    if val >= 30:
                        stats += stat.title() + ' **30** | '
                    else:
                        stats += stat.title() + ' ' + str(val) + ' | '
                elif stat == 'move':
                    if base_class['name'] == 'Ballistician' or base_class['name'] == 'Catapulter':
                        stats += stat.title() + ' **0** | '
                    elif val >= 12:
                        stats += stat.title() + ' **12** | '
                    else:
                        stats += stat.title() + ' ' + str(val) + ' | '
                else:
                    if personal:
                        if val >= 15:
                            stats += stat.title() + ' **15** | '
                        else:
                            stats += stat.title() + ' **' + str(val) + '** | '
                    else:
                        if promoted:
                            if val >= promo_class['base'][stat] + 15:
                                stats += stat.title() + ' **' + str(promo_class['base'][stat] + 15) + '** | '
                            else:
                                stats += stat.title() + ' ' + str(val) + ' | '
                        else:
                            if val >= base_class['base'][stat] + 15:
                                stats += stat.title() + ' **' + str(base_class['base'][stat] + 15) + '** | '
                            else:
                                stats += stat.title() + ' ' + str(val) + ' | '
    stats = stats[:-3]
    embed.add_field(name='Stats', value=stats, inline=False)
    return embed


def get_unit_requirement_embed(unit_json: json):
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
    recruitment = ''
    if 'recruit' in unit_json:
        recruitment += unit_json['recruit']
        embed.add_field(name='Recruitment', value=recruitment, inline=False)
    title = ''
    if 'title' in unit_json:
        for t in unit_json['title']:
            title += t + '\n'
        embed.add_field(name='Titles', value=title, inline=False)
    preferentials = ''
    if 'prf' in unit_json:
        preferentials += unit_json['prf']
        embed.add_field(name='Preferentials', value=preferentials, inline=False)
    return embed


def get_unit_support_embed(unit_json: json):
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
    givensupport = ''
    if 'givesupport' in unit_json:
        for support in unit_json['givesupport']:
            givensupport += '**' + support + ':**\n'
            givensupport += 'Base: ' + str(unit_json['givesupport'][support]['base']) + '\n'
            if 'increase' in unit_json['givesupport'][support]:
                givensupport += '\n'
                for increase in unit_json['givesupport'][support]['increase']:
                    givensupport += '*Bonus + ' + str(unit_json['givesupport'][support]['increase'][increase]['bonus']) + '*\n'
                    givensupport += '*' + unit_json['givesupport'][support]['increase'][increase]['note'] + '*\n'
            givensupport += '\n'
        embed.add_field(name='Given Supports', value=givensupport, inline=True)

    recievedsupport = ''
    if 'recievesupport' in unit_json:
        for support in unit_json['recievesupport']:
            recievedsupport += '**' + support + ':**\n'
            recievedsupport += 'Base: ' + str(unit_json['recievesupport'][support]['base']) + '\n'
            if 'increase' in unit_json['recievesupport'][support]:
                recievedsupport += '\n'
                for increase in unit_json['recievesupport'][support]['increase']:
                    recievedsupport += '*Bonus + ' + str(unit_json['recievesupport'][support]['increase'][increase]['bonus']) + '*\n'
                    recievedsupport += '*' + unit_json['recievesupport'][support]['increase'][increase]['note'] + '*\n'
            recievedsupport += '\n'
        embed.add_field(name='Recieved Supports', value=recievedsupport, inline=True)

    if givensupport == '' and recievedsupport == '':
        embed.add_field(name='', value='Absolutely nobody likes this unit. Has no supports.', inline=False)
    else:
        embed.set_footer(text='Supports grant a Hit, Avoid, Crit and Crit Avoid bonus within 3 spaces')
    return embed


async def classdata(interaction: discord.Interaction, name: str):
    with open(trs_class_data_file, 'r') as f:
        class_json = json.load(f)
        found = False
        for k in class_json:
            if class_json[k]['name'].lower().startswith(name.lower()):
                found = True
                embed = get_class_data_embed(class_json[k])
                await interaction.response.send_message(embed=embed)
                break
        if not found:
            await interaction.response.send_message('That class does not exist', ephemeral=True)


def get_class_data_embed(class_json: json):
    embed = discord.Embed(title=class_json['name'], color=0x8a428a)

    bases = ''
    for base in class_json['base']:
        match base:
            case 'hp':
                bases += 'HP ' + str(class_json['base'][base]) + ' | '
            case _:
                bases += base.title() + ' ' + str(class_json['base'][base]) + ' | '
    bases = bases[:-3]
    if 'dismount' in class_json:
        bases += '\n **Dismount:** '
        for stat in class_json['dismount']:
            if class_json['dismount'][stat] != 0:
                bases += stat.title() + ' ' + str(class_json['dismount'][stat]) + ' | '
        bases = bases[:-3]
    embed.add_field(name='Bases', value=bases, inline=False)

    caps = ''
    for base in class_json['base']:
        match base:
            case 'hp':
                caps += 'HP 60 | '
            case 'luck':
                caps += 'Luck 30 | '
            case 'move':
                if class_json['name'] == 'Ballistician' or class_json['name'] == 'Catapulter':
                    caps += 'Move 0 | '
                else:
                    caps += 'Move 12 | '
            case _:
                caps += base.title() + ' ' + str(class_json['base'][base] + 15) + ' | '
    caps = caps[:-3]
    embed.add_field(name='Caps', value=caps, inline=False)

    skills = ''
    for skill in class_json['skill']:
        skills += skill + '\n'
    embed.add_field(name='Skills', value=skills, inline=True)

    weapons = ''
    for weapon in class_json['weapon']:
        weapons += weapon + '\n'
    embed.add_field(name='Weapons', value=weapons, inline=True)

    if 'drop' in class_json:
        embed.set_footer(text='0.5% chance drop for: ' + class_json['drop'])

    return embed


async def skill(interaction: discord.Interaction, name: str):
    with open(trs_skill_data_file, 'r') as f:
        skill_json = json.load(f)
        found = False
        for k in skill_json:
            if k.lower().startswith(name.lower()):
                embed = get_skill_data_embed(skill_json[k])
                await interaction.response.send_message(embed=embed)
                found = True
                break
        if not found:
            await interaction.response.send_message('That skill does not exist', ephemeral=True)


def get_skill_data_embed(skill_json: json) -> discord.Embed:
    embed = discord.Embed(title=skill_json['name'], color=0x8a428a)
    info = ''
    for value in skill_json:
        match value:
            case 'activation':
                info += '\n**Activation: **' + skill_json['activation']
    embed.add_field(name='', value=info, inline=False)
    embed.add_field(name='', value=skill_json['description'], inline=False)
    return embed


async def item(interaction: discord.Interaction, name: str):
    with open(trs_item_data_file, 'r') as f:
        item_json = json.load(f)
        found = False
        for k in item_json:
            if item_json[k]['name'].lower() == name.lower():
                embed = get_item_stats_embed(item_json[k])
                await interaction.response.send_message(embed=embed)
                found = True
                break
        if not found:
            for k in item_json:
                if k.lower().startswith(name.lower()):
                    embed = get_item_stats_embed(item_json[k])
                    await interaction.response.send_message(embed=embed)
                    found = True
                    break
        if not found:
            await interaction.response.send_message('That item does not exist', ephemeral=True)


def get_item_stats_embed(item_json: json):
    embed = discord.Embed(title=item_json['name'], color=0x8a428a)
    stats = item_json['type'] + '  \n'
    for value in item_json:
        match value:
            case 'might':
                stats += 'Mt ' + str(item_json['might']) + ' | '
            case 'hit':
                stats += 'Hit ' + str(item_json['hit']) + ' | '
            case 'crit':
                stats += 'Crit ' + str(item_json['crit']) + ' | '
            case 'weight':
                stats += 'Wt ' + str(item_json['weight']) + ' | '
            case 'mst':
                if item_json['mst']:
                    stats += 'Mst ' + str(item_json['mst']) + ' | '
                else:
                    stats += 'Mst - | '
    stats = stats[:-3] + '\n'
    for value in item_json:
        match value:
            case 'range':
                stats += 'Rng ' + item_json['range'] + ' | '
            case 'durability':
                if item_json['durability']:
                    stats += 'Durability ' + str(item_json['durability']) + ' | '
                else:
                    stats += 'Durability - | '
            case 'cost':
                if item_json['cost']:
                    stats += 'Cost ' + str(item_json['cost']) + ' G. | '
    stats = stats[:-3]
    embed.add_field(name='', value=stats, inline=False)
    note = ''
    if item_json['type'] == 'Bow':
        note = 'Effective against fliers\n'
    if 'note' in item_json:
        note += item_json['note']
    if note != '':
        embed.add_field(name='Notes:', value=note, inline=False)
    return embed
