import discord
import json

vs1_unit_data_file = 'vs1/unitdata.json'
vs1_class_data_file = 'vs1/classdata.json'
vs1_item_data_file = 'vs1/itemdata.json'
vs1_skill_data_file = 'vs1/skilldata.json'


def get_unit_json(ctx: str) -> json:
    with open(vs1_unit_data_file, 'r') as f:
        unit_json = json.load(f)
        for k in unit_json:
            if unit_json[k]['name'].lower() == ctx.lower():
                return unit_json[k]
        for k in unit_json:
            if k.lower().startswith(ctx.lower()):
                return unit_json[k]
        return None


def get_class_json(ctx: str) -> json:
    with open(vs1_class_data_file, 'r') as f:
        class_json = json.load(f)
        for k in class_json:
            if class_json[k]['name'].lower() == ctx.lower():
                return class_json[k]
        for k in class_json:
            if (k == ctx) or (class_json[k]['name'].lower().startswith(ctx.lower())):
                return class_json[k]
        return None


def get_item_json(ctx: str) -> json:
    with open(vs1_item_data_file, 'r') as f:
        item_json = json.load(f)
        for k in item_json:
            if item_json[k]['name'].lower() == ctx.lower():
                return item_json[k]
        for k in item_json:
            if (k == ctx) or (item_json[k]['name'].lower().startswith(ctx.lower())):
                return item_json[k]
        return None


def get_skill_json(ctx: str) -> json:
    with open(vs1_skill_data_file, 'r') as f:
        skill_json = json.load(f)
        for k in skill_json:
            if skill_json[k]['name'].lower() == ctx.lower():
                return skill_json[k]
        for k in skill_json:
            if (k == ctx) or (skill_json[k]['name'].lower().startswith(ctx.lower())):
                return skill_json[k]
        return None


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
        embed = get_unit_stats_embed(unit_json, base_class_json, False, False, False)
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

    @discord.ui.button(label='Reclass', style=discord.ButtonStyle.blurple, custom_id='reclass')
    async def reclass(self, interaction: discord.Interaction, button: discord.ui.Button):
        name = interaction.message.embeds[0].to_dict()["title"].lower()
        unit_json = get_unit_json(name)
        embed = get_unit_reclass_embed(unit_json)
        embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
        for i in self.children:
            if i.label != 'Reclass':
                i.disabled = False
        button.disabled = True
        button.custom_id = 'Reclass'
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


async def unit(interaction: discord.Interaction, name: str, level: str,
               veldland: bool, frallian: bool, prison: bool):
    unit_json = get_unit_json(name)
    if unit_json is None:
        await interaction.response.send_message('That unit does not exist', ephemeral=True)
    else:
        view = UnitButton(interaction)

        if ('recievesupport' not in unit_json) and ('givesupport' not in unit_json):
            for x in range(len(view.children)):
                if view.children[x].label == 'Supports':
                    view.remove_item(view.children[x])
                    break

        if 'reclass' not in unit_json:
            for x in range(len(view.children)):
                if view.children[x].label == 'Reclass':
                    view.remove_item(view.children[x])
                    break

        if level is None:
            base_class_json = get_class_json(unit_json['class'])
            embed = get_unit_stats_embed(unit_json, base_class_json, veldland, frallian, prison)
            portrait = discord.File('vs1/portraits/' + unit_json['portrait'], filename=unit_json['portrait'])
            embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
            await interaction.response.send_message(embed=embed, file=portrait, view=view)
        else:
            if level is None:
                level = ''
            base_class_json = get_class_json(unit_json['class'])
            embed = get_unit_level_embed(unit_json, level, base_class_json, veldland, frallian, prison)
            portrait = discord.File('vs1/portraits/' + unit_json['portrait'], filename=unit_json['portrait'])
            embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
            await interaction.response.send_message(embed=embed, file=portrait)


def get_unit_stats_embed(unit_json: json, base_class: json,
                         veldland: bool, frallian: bool, prison: bool) -> discord.Embed:
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
    header = 'Lvl ' + str(unit_json['lvl']) + ' ' + base_class['name']
    embed.add_field(name='', value=header, inline=False)

    bases = ''
    for base in unit_json['base']:
        val = unit_json['base'][base]
        match base:
            case 'hp':
                if base in base_class['cap']:
                    if val >= base_class['cap'][base]:
                        bases += 'HP **' + str(base_class['cap'][base]) + '** | '
                    else:
                        bases += 'HP ' + str(unit_json['base'][base]) + ' | '
                else:
                    bases += 'HP ' + str(unit_json['base'][base]) + ' | '
            case _:
                if base in base_class['cap']:
                    if val >= base_class['cap'][base]:
                        bases += base.title() + ' **' + str(base_class['cap'][base]) + '** | '
                    else:
                        bases += base.title() + ' ' + str(unit_json['base'][base]) + ' | '
                else:
                    bases += base.title() + ' ' + str(unit_json['base'][base]) + ' | '
    bases = bases[:-3]
    embed.add_field(name='Bases', value=bases, inline=False)

    growths = ''
    growthname = 'Growths'
    darkhorse = False

    for skill in unit_json['skill']:
        if skill == 'Dark Horse':
            growthname += ' +Dark Horse'
            darkhorse = True

    if veldland:
        growthname += ' +Veldlands Accolade'
    if frallian:
        growthname += ' +Frallian Accolade'
    if prison:
        growthname += ' +Prison Accolade'

    for stat in ['hp', 'str', 'mag', 'dex', 'agi', 'luck', 'prof', 'def', 'res', 'mob']:
        bonus = 0
        if veldland and stat in ['def', 'res']:
            bonus += 10
        if frallian and stat in ['dex', 'agi']:
            bonus += 10
        if prison and stat in ['str', 'mag']:
            bonus += 10
        if darkhorse and stat in ['hp', 'str', 'mag', 'dex', 'agi', 'luck', 'prof', 'def', 'res']:
            bonus += 10

        if stat in unit_json['growth']:

            if stat == 'hp':
                growths += 'HP ' + str(unit_json['growth']['hp'] + bonus) + '% | '
            else:
                growths += stat.title() + ' ' + str(unit_json['growth'][stat] + bonus) + '% | '

        else:

            if stat == 'hp':
                if bonus > 0:
                    growths += 'HP ?+' + str(bonus) + '% | '
                else:
                    growths += 'HP ?% | '
            else:
                if bonus > 0:
                    growths += stat.title() + ' ?+' + str(bonus) + '% | '
                else:
                    growths += stat.title() + ' ?% | '

    growths = growths[:-3]

    embed.add_field(name=growthname, value=growths, inline=False)

    promotionwrank = ''
    if 'promo' in unit_json:
        promo_class = get_class_json(unit_json['promo']['name'])
        promotext = '**' + promo_class['name'] + '**\n'
        for stat in unit_json['promo']['bonus']:
            match stat:
                case 'hp':
                    promotext += 'HP +' + str(unit_json['promo']['bonus'][stat]) + ' | '
                case _:
                    promotext += stat.title() + ' +' + str(unit_json['promo']['bonus'][stat]) + ' | '
        promotext = promotext[:-3]

        if 'weapon' in unit_json['promo']:
            for weapon in unit_json['promo']['weapon']:
                promotionwrank += weapon + ' | '

            promotext += '\n+' + promotionwrank[:-3]

        embed.add_field(name='Promotion', value=promotext, inline=False)

    skills_text = ''
    for skill in unit_json['skill']:
        skills_text += skill + '\n'
    embed.add_field(name='Skills', value=skills_text, inline=True)

    weapons = ''
    for rank in unit_json['weapon']:
        weapons += rank + '\n'
    embed.add_field(name='Weapons', value=weapons, inline=True)
    return embed


def get_unit_level_embed(unit_json: json, level: str, base_class: json,
                         veldland: bool, frallian: bool, prison: bool) -> discord.Embed:
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)

    promoted = False
    promo_class = None
    promolvl = None

    if 'promo' in unit_json:
        promo_class = get_class_json(unit_json['promo']['name'])
        if level.find('/') > 0:
            promolvl = max(min(int(level[level.find('/') + 1:]), 20), 1)
            promoted = True
        elif level.find(',') > 0:
            promolvl = max(min(int(level[level.find(',') + 1:]), 20), 1)
            promoted = True

    if level.find('/') > 0:
        baselvl = max(min(int(level[:level.find('/')]), 20), unit_json['lvl'])
    elif level.find(',') > 0:
        baselvl = max(min(int(level[:level.find(',')]), 20), unit_json['lvl'])
    else:
        baselvl = max(min(int(level), 20), unit_json['lvl'])

    header = '**Lvl ' + str(unit_json['lvl']) + '** '
    if level != unit_json['lvl']:
        header += '**-> ' + str(baselvl) + '** '
    header += base_class['name']
    if 'promo' in unit_json and promolvl is not None:
        header += ' **=>** ' + promo_class['name'] + ' **Lvl 1**'
        if promolvl > 1:
            header += ' **-> ' + str(promolvl) + '**'
    embed.add_field(name='', value=header, inline=False)

    darkhorse = False
    for s in unit_json['skill']:
        if s == 'Dark Horse':
            darkhorse = True

    if veldland or frallian or prison or darkhorse:
        accolade = ''
        if darkhorse:
            accolade += 'Dark Horse | '
        if veldland:
            accolade += 'Veldlands Accolade | '
        if frallian:
            accolade += 'Frallian Accolade | '
        if prison:
            accolade += 'Prison Accolade | '
        accolade = accolade[:-3]
        embed.add_field(name='', value=accolade, inline=False)

    if promolvl is None:
        promoinc = 0
    else:
        promoinc = promolvl - 1

    lvlinc = baselvl - unit_json['lvl'] + promoinc

    valstr = ''

    for stat in unit_json['base']:
        bonus = 0
        if veldland and stat in ['def', 'res']:
            bonus += 10
        if frallian and stat in ['dex', 'agi']:
            bonus += 10
        if prison and stat in ['str', 'mag']:
            bonus += 10
        if darkhorse and stat in ['hp', 'str', 'mag', 'dex', 'agi', 'luck', 'prof', 'def', 'res']:
            bonus += 10

        promobonus = 0
        if promoted:
            if stat in unit_json['promo']['bonus']:
                promobonus = unit_json['promo']['bonus'][stat]

        if stat in unit_json['growth']:
            val = round(round(((unit_json['growth'][stat] + bonus) / 100), 2) * lvlinc + unit_json['base'][stat] +
                        promobonus, 2)

            if promoted:
                if stat in promo_class['cap']:

                    if val >= promo_class['cap'][stat]:
                        if stat == 'hp':
                            valstr += 'HP **' + str(promo_class['cap'][stat]) + '** | '
                        else:
                            valstr += stat.title() + ' **' + str(promo_class['cap'][stat]) + '** | '

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
                if stat in base_class['cap']:

                    if val >= base_class['cap'][stat]:
                        if stat == 'hp':
                            valstr += 'HP **' + str(base_class['cap'][stat]) + '** | '
                        else:
                            valstr += stat.title() + ' **' + str(base_class['cap'][stat]) + '** | '

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
            if stat == 'hp':
                valstr += 'HP ' + str(unit_json['base'][stat]) + '+? | '
            else:
                valstr += stat.title() + ' ' + str(unit_json['base'][stat]) + '+? | '

    valstr = valstr[:-3]
    embed.add_field(name='Stats', value=valstr, inline=False)
    return embed


def get_unit_reclass_embed(unit_json: json):
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
    reclass = ''
    for c in unit_json['reclass']:
        class_json = get_class_json(unit_json['reclass'][c]['name'])
        reclass += '**' + class_json['name'] + '**\n'
        for stat in unit_json['reclass'][c]['bonus']:
            if unit_json['reclass'][c]['bonus'][stat] > 0:
                valstr = '+' + str(unit_json['reclass'][c]['bonus'][stat])
            else:
                valstr = str(unit_json['reclass'][c]['bonus'][stat])
            match stat:
                case 'hp':
                    reclass += 'HP ' + valstr + ' | '
                case _:
                    reclass += stat.title() + ' ' + valstr + ' | '
        reclass = reclass[:-3] + '\n'
        if 'weapon' in unit_json['reclass'][c]:
            for weapon in unit_json['reclass'][c]['weapon']:
                reclass += weapon + ', '
            reclass = reclass[:-2] + '\n'
        reclass += 'Condition: ' + unit_json['reclass'][c]['condition'] + '\n\n'
    embed.add_field(name='Reclass', value=reclass, inline=False)
    return embed


def get_unit_support_embed(unit_json: json):
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)

    givensupport = ''
    if 'givesupport' in unit_json:
        for u in unit_json['givesupport']:
            givensupport += '**' + u + '**\n'
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
            recievesupport += '**' + u + '**\n'
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


async def classdata(interaction: discord.Interaction, name: str):
    class_json = get_class_json(name)
    if class_json is None:
        await interaction.response.send_message('That class does not exist', ephemeral=True)
    else:
        embed = get_class_data_embed(class_json)
        await interaction.response.send_message(embed=embed)


def get_class_data_embed(class_json: json):
    embed = discord.Embed(title=class_json['name'], color=0x8a428a)

    caps = ''
    for cap in class_json['cap']:
        match cap:
            case 'hp':
                caps += 'HP ' + str(class_json['cap'][cap]) + ' | '
            case _:
                caps += cap.title() + ' ' + str(class_json['cap'][cap]) + ' | '
    caps = caps[:-3]
    embed.add_field(name='Caps', value=caps, inline=False)

    weapons = ''
    for weapon in class_json['weapon']:
        weapons += weapon + '\n'
    embed.add_field(name='Weapons', value=weapons, inline=True)

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
