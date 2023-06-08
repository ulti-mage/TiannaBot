import discord
import json
import random

vs2_unit_data_file = 'vs2/unitdata.json'
vs2_item_data_file = 'vs2/itemdata.json'
vs2_skill_data_file = 'vs2/skilldata.json'


def get_unit_json(ctx: str) -> json:
    with open(vs2_unit_data_file, 'r') as f:
        unit_json = json.load(f)
        for k in unit_json:
            if unit_json[k]['name'].lower() == ctx.lower():
                return unit_json[k]
        for k in unit_json:
            if k.lower().startswith(ctx.lower()):
                return unit_json[k]
        return None


def get_item_json(ctx: str) -> json:
    with open(vs2_item_data_file, 'r') as f:
        item_json = json.load(f)
        for k in item_json:
            if item_json[k]['name'].lower() == ctx.lower():
                return item_json[k]
        for k in item_json:
            if (k == ctx) or (item_json[k]['name'].lower().startswith(ctx.lower())):
                return item_json[k]
        return None


def get_skill_json(ctx: str) -> json:
    with open(vs2_skill_data_file, 'r') as f:
        skill_json = json.load(f)
        for k in skill_json:
            if skill_json[k]['name'].lower() == ctx.lower():
                return skill_json[k]
        for k in skill_json:
            if (k == ctx) or (skill_json[k]['name'].lower().startswith(ctx.lower())):
                return skill_json[k]
        return None


class UnitButton(discord.ui.View):
    def __init__(self, ctx, portraitfile):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.portraitfile = portraitfile

    async def on_timeout(self) -> None:
        message = await self.ctx.original_response()
        for i in self.children:
            i.disabled = True
        await message.edit(view=self)

    @discord.ui.button(label='Stats', style=discord.ButtonStyle.blurple, disabled=True)
    async def stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        name = interaction.message.embeds[0].to_dict()["title"].lower()
        unit_json = get_unit_json(name)
        embed = get_unit_stats_embed(unit_json)
        embed.set_thumbnail(url='attachment://' + self.portraitfile)
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
        embed.set_thumbnail(url='attachment://' + self.portraitfile)
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
        embed.set_thumbnail(url='attachment://' + self.portraitfile)
        for i in self.children:
            if i.label != 'Other':
                i.disabled = False
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)


async def unit(interaction: discord.Interaction, name: str, level: int, promoted: bool):
    unit_json = get_unit_json(name)
    if unit_json is None:
        await interaction.response.send_message('That unit does not exist', ephemeral=True)
    else:

        portraitfile = unit_json['portrait']
        if portraitfile == 'karajan1.png':
            if random.randint(0, 1) == 1:
                portraitfile = 'karajan1.png'
            else:
                portraitfile = 'karajan2.png'
        if portraitfile == 'abrahm1.png':
            if random.randint(0, 1) == 1:
                portraitfile = 'abrahm1.png'
            else:
                portraitfile = 'abrahm2.png'

        view = UnitButton(interaction, portraitfile)

        if ('recievesupport' not in unit_json) and ('givesupport' not in unit_json):
            for x in range(len(view.children)):
                if view.children[x].label == 'Supports':
                    view.remove_item(view.children[x])
                    break

        if level is None:
            embed = get_unit_stats_embed(unit_json)
            portrait = discord.File('vs2/portraits/' + portraitfile, filename=portraitfile)
            embed.set_thumbnail(url='attachment://' + portraitfile)
            await interaction.response.send_message(embed=embed, file=portrait, view=view)
        else:
            if level is None:
                level = ''
            embed = get_unit_level_embed(unit_json, level, promoted)
            portrait = discord.File('vs2/portraits/' + portraitfile, filename=portraitfile)
            embed.set_thumbnail(url='attachment://' + portraitfile)
            await interaction.response.send_message(embed=embed, file=portrait)


def get_unit_stats_embed(unit_json: json) -> discord.Embed:
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
    header = 'Lvl ' + str(unit_json['level']) + ' ' + unit_json['class']
    embed.add_field(name='', value=header, inline=False)

    bases = ''
    for base in unit_json['base']:
        val = unit_json['base'][base]
        match base:
            case 'hp':
                if base in unit_json['cap']:
                    if val >= unit_json['cap'][base]:
                        bases += 'HP **' + str(unit_json['cap'][base]) + '** | '
                    else:
                        bases += 'HP ' + str(unit_json['base'][base]) + ' | '
                else:
                    bases += 'HP ' + str(unit_json['base'][base]) + ' | '
            case _:
                if base in unit_json['cap']:
                    if val >= unit_json['cap'][base]:
                        bases += base.title() + ' **' + str(unit_json['cap'][base]) + '** | '
                    else:
                        bases += base.title() + ' ' + str(unit_json['base'][base]) + ' | '
                else:
                    bases += base.title() + ' ' + str(unit_json['base'][base]) + ' | '
    bases = bases[:-3]
    embed.add_field(name='Bases', value=bases, inline=False)

    growths = ''
    growthname = 'Growths'

    for stat in ['hp', 'str', 'mag', 'dex', 'agi', 'luck', 'prof', 'def', 'res', 'mob']:

        if stat in unit_json['growth']:

            if stat == 'hp':
                growths += 'HP ' + str(unit_json['growth']['hp']) + '% | '
            else:
                growths += stat.title() + ' ' + str(unit_json['growth'][stat]) + '% | '

        else:

            if stat == 'hp':
                growths += 'HP ?% | '
            else:
                growths += stat.title() + ' ?% | '

    growths = growths[:-3]

    embed.add_field(name=growthname, value=growths, inline=False)

    promotionwrank = ''
    if 'promo' in unit_json:
        promotext = '**' + unit_json['promo']['name'] + '**\n'
        for stat in unit_json['promo']['bonus']:
            if unit_json['promo']['bonus'][stat] > 0:
                valstr = '+' + str(unit_json['promo']['bonus'][stat])
            else:
                valstr = str(unit_json['promo']['bonus'][stat])
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

        if 'promo2' in unit_json:
            promotionwrank = ''
            promotext += '\n**' + unit_json['promo2']['name'] + '**\n'
            for stat in unit_json['promo2']['bonus']:
                if unit_json['promo2']['bonus'][stat] > 0:
                    valstr = '+' + str(unit_json['promo2']['bonus'][stat])
                else:
                    valstr = str(unit_json['promo2']['bonus'][stat])
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
    for s in unit_json['skill']:
        skills_text += s + '\n'
    embed.add_field(name='Skills', value=skills_text, inline=True)

    weapons = ''
    for r in unit_json['weapon']:
        weapons += r + '\n'
    embed.add_field(name='Weapons', value=weapons, inline=True)
    return embed


def get_unit_level_embed(unit_json: json, level: int, promoted: bool) -> discord.Embed:
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
    level = max(min(level, 30), unit_json['level'])
    levelstr = '**Lvl ' + str(unit_json['level']) + '** '
    if level != unit_json['level']:
        levelstr += '**-> ' + str(level) + '** '
    levelstr += unit_json['class']
    if promoted and 'promo' in unit_json:
        levelstr += ' -> ' + unit_json['promo']['name']
    embed.add_field(name='', value=levelstr, inline=False)

    lvlinc = level - unit_json['level']

    valstr = ''

    for stat in unit_json['base']:
        promobonus = 0
        if promoted and 'promo' in unit_json:
            if stat in unit_json['promo']['bonus']:
                promobonus = unit_json['promo']['bonus'][stat]

        if stat in unit_json['growth']:
            val = round(round((unit_json['growth'][stat] / 100), 2) * lvlinc + unit_json['base'][stat] + promobonus, 2)

            if promoted and 'promo' in unit_json:
                if stat in unit_json['promo']['cap']:

                    if val >= unit_json['promo']['cap'][stat]:
                        if stat == 'hp':
                            valstr += 'HP **' + str(unit_json['promo']['cap'][stat]) + '** | '
                        else:
                            valstr += stat.title() + ' **' + str(unit_json['promo']['cap'][stat]) + '** | '

                    else:
                        if stat == 'hp':
                            valstr += 'HP ' + str(val) + ' | '
                        else:
                            valstr += stat.title() + ' ' + str(val) + ' | '

                else:
                    if stat == 'hp':
                        valstr += 'HP ' + str(val) + ' | '
                    else:
                        valstr += stat.title() + ' ' + str(val) + ' | '

            else:
                if stat in unit_json['cap']:

                    if val >= unit_json['cap'][stat]:
                        if stat == 'hp':
                            valstr += 'HP **' + str(unit_json['cap'][stat]) + '** | '
                        else:
                            valstr += stat.title() + ' **' + str(unit_json['cap'][stat]) + '** | '

                    else:
                        if stat == 'hp':
                            valstr += 'HP ' + str(val) + ' | '
                        else:
                            valstr += stat.title() + ' ' + str(val) + ' | '

                else:

                    if stat == 'hp':
                        valstr += 'HP ' + str(val) + ' | '
                    else:
                        valstr += stat.title() + ' ' + str(val) + ' | '

        else:
            if promoted and 'promo' in unit_json:
                if stat in unit_json['promo']['bonus']:
                    if stat == 'hp':
                        valstr += 'HP ' + str(unit_json['base'][stat] + unit_json['promo']['bonus'][stat]) + '+? | '
                    else:
                        valstr += stat.title() + ' ' + str(unit_json['base'][stat] + unit_json['promo']['bonus'][stat]) + '+? | '
                else:
                    if stat == 'hp':
                        valstr += 'HP ' + str(unit_json['base'][stat]) + '+? | '
                    else:
                        valstr += stat.title() + ' ' + str(unit_json['base'][stat]) + '+? | '
            else:
                if stat == 'hp':
                    valstr += 'HP ' + str(unit_json['base'][stat]) + '+? | '
                else:
                    valstr += stat.title() + ' ' + str(unit_json['base'][stat]) + '+? | '

    valstr = valstr[:-3]
    embed.add_field(name='Stats', value=valstr, inline=False)
    return embed


def get_unit_support_embed(unit_json: json):
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)

    givensupport = ''
    if 'givesupport' in unit_json:
        for u in unit_json['givesupport']:
            givensupport += '**' + u + '**  \n'
            for stat in unit_json['givesupport'][u]:
                match stat:
                    case 'note':
                        pass
                    case _:
                        givensupport += stat.title() + ' ' + str(unit_json['givesupport'][u][stat]) + ' | '
            givensupport = givensupport[:-3] + '\n'
            if 'note' in unit_json['givesupport'][u]:
                givensupport += '*' + unit_json['givesupport'][u]['note'] + '*\n'
            givensupport += '\n'
        embed.add_field(name='Given Supports', value=givensupport, inline=True)

    recievesupport = ''
    if 'recievesupport' in unit_json:
        for u in unit_json['recievesupport']:
            recievesupport += '**' + u + '**  \n'
            for stat in unit_json['recievesupport'][u]:
                match stat:
                    case 'note':
                        pass
                    case _:
                        recievesupport += stat.title() + ' ' + str(unit_json['recievesupport'][u][stat]) + ' | '
            recievesupport = recievesupport[:-3] + '\n'
            if 'note' in unit_json['recievesupport'][u]:
                recievesupport += '*' + unit_json['recievesupport'][u]['note'] + '*\n'
            recievesupport += '\n'
        embed.add_field(name='Recieved Supports', value=recievesupport, inline=True)

    return embed


def get_unit_requirement_embed(unit_json: json):
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
    recruitment = ''
    if 'recruit' in unit_json:
        recruitment += unit_json['recruit']
        embed.add_field(name='Recruitment', value=recruitment, inline=False)
    preferentials = ''
    if 'prf' in unit_json:
        preferentials += unit_json['prf']
        embed.add_field(name='Preferentials', value=preferentials, inline=False)
    return embed


async def skill(interaction: discord.Interaction, name: str):
    skill_json = get_skill_json(name)
    if skill_json is None:
        await interaction.response.send_message('That skill does not exist', ephemeral=True)
    else:
        embed = get_skill_data_embed(skill_json)
        await interaction.response.send_message(embed=embed)


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
    item_json = get_item_json(name)
    if item_json is None:
        await interaction.response.send_message('That item does not exist', ephemeral=True)
    else:
        embed = get_item_stats_embed(item_json)
        await interaction.response.send_message(embed=embed)


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
            case 'prof':
                if item_json['prof']:
                    stats += 'Prof ' + str(item_json['prof']) + ' | '
                else:
                    stats += 'Prof - | '
    stats = stats[:-3] + '  \n'
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
                    stats += 'Cost ' + str(item_json['cost']) + ' D. | '
    stats = stats[:-3]
    embed.add_field(name='', value=stats, inline=False)
    if 'note' in item_json:
        note = item_json['note']
        embed.add_field(name='Notes:', value=note, inline=False)
    return embed
