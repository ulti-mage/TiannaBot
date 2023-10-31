import discord
import json

fe3b1_unit_data_file = 'fe3/b1.json'
fe3b2_unit_data_file = 'fe3/b2.json'
bsfe_unit_data_file = 'fe3/bsfe.json'

fe3_item_data_file = 'fe3/item.json'
fe3_class_data_file = 'fe3/job.json'

shard_info = [['Aquarius', 0, 10, 10, 10, 0, 10, 0, 0],
              ['Pisces', 10, 0, 0, 0, 10, 0, 10, 10],
              ['Aries', 0, 0, 0, 0, 40, 0, 0, 0],
              ['Taurus', 5, 5, 5, 5, 5, 5, 5, 5],
              ['Gemini', 0, 30, 0, 0, 0, -10, 20, 0],
              ['Cancer', 0, -10, 0, 0, 0, 0, 50, 0],
              ['Leo', 0, 50, 0, 0, 0, 0, -10, 0],
              ['Virgo', 0, 0, 0, 0, 0, 20, -10, 30],
              ['Libra', -10, 0, 0, 40, 10, 10, 0, -10],
              ['Scorpio', 0, 20, 20, 10, -10, 0, 0, 0],
              ['Sagittarius', -10, 0, 40, 10, 0, 0, 0, 0],
              ['Capricorn', -20, 0, -10, -10, 0, 30, 10, 0],
              ['Star Sphere', 30, 30, 30, 30, 30, 30, 30, 30]]


def get_b1_unit_json(ctx: str) -> json:
    with open(fe3b1_unit_data_file, 'r') as f:
        unit_json = json.load(f)
        for k in unit_json:
            if unit_json[k]['name'].lower() == ctx.lower():
                return unit_json[k]
        for k in unit_json:
            if k.lower().startswith(ctx.lower()):
                return unit_json[k]
        return None


def get_b2_unit_json(ctx: str) -> json:
    with open(fe3b2_unit_data_file, 'r') as f:
        unit_json = json.load(f)
        for k in unit_json:
            if unit_json[k]['name'].lower() == ctx.lower():
                return unit_json[k]
        for k in unit_json:
            if k.lower().startswith(ctx.lower()):
                return unit_json[k]
        return None


def get_bsfe_unit_json(ctx: str) -> json:
    with open(bsfe_unit_data_file, 'r') as f:
        unit_json = json.load(f)
        for k in unit_json:
            if unit_json[k]['name'].lower() == ctx.lower():
                return unit_json[k]
        for k in unit_json:
            if k.lower().startswith(ctx.lower()):
                return unit_json[k]
        return None


def get_item_json(ctx: str) -> json:
    with open(fe3_item_data_file, 'r') as f:
        item_json = json.load(f)
        for k in item_json:
            if item_json[k]['name'].lower() == ctx.lower():
                return item_json[k]
        for k in item_json:
            if (k == ctx) or (item_json[k]['name'].lower().startswith(ctx.lower())):
                return item_json[k]
        return None


def get_class_json(ctx: str) -> json:
    with open(fe3_class_data_file, 'r') as f:
        skill_json = json.load(f)
        for k in skill_json:
            if skill_json[k]['name'].lower() == ctx.lower():
                return skill_json[k]
        for k in skill_json:
            if (k == ctx) or (skill_json[k]['name'].lower().startswith(ctx.lower())):
                return skill_json[k]
        return None


async def unit(interaction: discord.Interaction, name: str, level: str, personal: bool, game: str, shards = None):
    if game == 'b1':
        unit_json = get_b1_unit_json(name)
    elif game == 'b2':
        unit_json = get_b2_unit_json(name)
    else:
        unit_json = get_bsfe_unit_json(name)

    if unit_json is None:
        await interaction.response.send_message('That unit does not exist', ephemeral=True)
    else:

        shard_out_list = []
        if shards is not None:
            shard_input_list = shards.split(',')
            for shard in shard_input_list:
                shard = shard.replace(" ", "")
                for n in shard_info:
                    if shard.lower() == n[0].lower() or shard.lower() in n[0].lower():
                        shard_out_list.append(n)
                        break

        if level is None:
            base_class_json = get_class_json(unit_json['job'])
            embed = get_unit_stats_embed(unit_json, base_class_json, personal, shard_out_list)
            portrait = discord.File('fe3/images/' + unit_json['portrait'], filename=unit_json['portrait'])
            embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
            await interaction.response.send_message(embed=embed, file=portrait)
        else:
            if level is None:
                level = '1'
            base_class_json = get_class_json(unit_json['job'])
            embed = get_unit_level_embed(unit_json, level, base_class_json, personal, shard_out_list)
            portrait = discord.File('fe3/images/' + unit_json['portrait'], filename=unit_json['portrait'])
            embed.set_thumbnail(url='attachment://' + unit_json['portrait'])
            await interaction.response.send_message(embed=embed, file=portrait)


def get_unit_stats_embed(unit_json: json, base_class: json, personal: bool, shard_list: list) -> discord.Embed:
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
    header = 'Lvl ' + str(unit_json['lvl']) + ' ' + base_class['name']
    if personal:
        header += '\n **Personal Stats**'
    embed.add_field(name='', value=header, inline=False)

    if shard_list:
        shards = '**Shards:** '
        for shard in shard_list:
            shards += shard[0] + ', '
        shards = shards[:-2]
        embed.add_field(name='', value=shards, inline=False)

    bases = ''
    statlist = ['hp', 'atk', 'skl', 'spd', 'lck', 'wlv', 'def', 'res', 'mov']

    for base in statlist:
        match base:
            case 'hp':
                if unit_json['base'][base] >= 52:
                    bases += 'HP **52** | '
                else:
                    bases += 'HP ' + str(unit_json['base'][base]) + ' | '
            case 'lck' | 'wlv':
                if unit_json['base'][base] >= 20:
                    bases += base.title() + ' **20** | '
                else:
                    bases += base.title() + ' ' + str(unit_json['base'][base]) + ' | '
            case 'mov':
                if not personal:
                    if base_class['base'][base] >= 20:
                        bases += 'Mov **20** | '
                    else:
                        bases += 'Mov ' + str(base_class['base'][base]) + ' | '
            case _:
                if not personal:
                    if unit_json['base'][base] + base_class['base'][base] >= 20:
                        bases += base.title() + ' **20** | '
                    else:
                        bases += base.title() + ' ' + str(unit_json['base'][base] + base_class['base'][base]) + ' | '
                else:
                    if unit_json['base'][base] >= 20:
                        bases += base.title() + ' **20** | '
                    else:
                        bases += base.title() + ' ' + str(unit_json['base'][base]) + ' | '

    bases = bases[:-3]
    if base_class['dismount']:
        bases += '\n**Dismount:** '
        dismount_class = get_class_json(base_class['dismount'])
        for stat in dismount_class['base']:
            val = dismount_class['base'][stat] - base_class['base'][stat]
            if val < 0 and stat not in ['hp', 'wlv']:
                bases += stat.title() + ' ' + str(val) + ' | '
        bases = bases[:-3]
    embed.add_field(name='Bases', value=bases, inline=False)

    growths = ''

    shard_counter = 0
    for stat in unit_json['growth']:

        shard_counter += 1

        bonus = 0
        for shard in shard_list:
            bonus += shard[shard_counter]

        if unit_json['growth'][stat] + bonus < 0:
            total_growth = 0
        else:
            total_growth = unit_json['growth'][stat] + bonus

        if stat == 'hp':
            growths += 'HP ' + str(total_growth) + '% | '
        else:
            growths += stat.title() + ' ' + str(total_growth) + '% | '

    growths = growths[:-3]
    embed.add_field(name='Growths', value=growths, inline=False)

    weapons = ''
    for weapon in base_class['weapon']:
        weapons += weapon.title() + '  \n'

    weapons = weapons[:-3]
    embed.add_field(name='Weapons', value=weapons, inline=True)

    if unit_json['promo']:
        promo_class = get_class_json(unit_json['promo'])
        promotxt = '**' + promo_class['name'] + '**\n'

        for stat in promo_class['base']:

            val = promo_class['base'][stat] - base_class['base'][stat]
            if val > 0:
                valstr = '+' + str(val)
            else:
                valstr = str(val)

            match stat:
                case 'hp':
                    if val > 0 and promo_class['base'][stat] > unit_json['base'][stat]:
                        promotxt += 'HP Min. ' + str(promo_class['base'][stat]) + ' | '
                case 'wlv':
                    if val > 0 and promo_class['base'][stat] > unit_json['base'][stat]:
                        promotxt += 'Wlv Min. ' + str(promo_class['base'][stat]) + ' | '
                case _:
                    if val != 0:
                        promotxt += stat.title() + ' ' + valstr + ' | '

        promotxt = promotxt[:-3]
        if promo_class['dismount']:
            promotxt += '\n**Dismount: **'
            dismount_class = get_class_json(promo_class['dismount'])
            for stat in dismount_class['base']:
                val = dismount_class['base'][stat] - promo_class['base'][stat]
                if val < 0 and stat not in ['hp', 'wlv']:
                    promotxt += stat.title() + ' ' + str(val) + ' | '
            promotxt = promotxt[:-3]
        embed.add_field(name='Promotion', value=promotxt, inline=True)

    return embed


def get_unit_level_embed(unit_json: json, level: str, base_class: json, personal: bool,
                         shard_list: list) -> discord.Embed:
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)

    promoted = False
    promo_class = None
    promolvl = None

    if unit_json['promo']:
        promo_class = get_class_json(unit_json['promo'])
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
    if personal:
        header += '\n**Personal Stats**'
    embed.add_field(name='', value=header, inline=False)

    if shard_list:
        shards = 'Shards: '
        for shard in shard_list:
            shards += shard[0] + ', '
        shards = shards[:-2]
        embed.add_field(name='Shards', value=shards, inline=False)

    if promolvl is None:
        promoinc = 0
    else:
        promoinc = promolvl - 1

    baseinc = baselvl - unit_json['lvl']

    stats = ''

    shard_counter = 0

    for stat in unit_json['base']:
        shard_counter += 1

        bonus = 0
        for shard in shard_list:
            bonus += shard[shard_counter]

        if unit_json['growth'][stat] + bonus < 0:
            total_growth = 0
        else:
            total_growth = unit_json['growth'][stat] + bonus

        val = round(unit_json['base'][stat] + (total_growth * baseinc) / 100, 2)
        if stat in base_class['base'] and stat not in ['hp', 'wlv'] and not personal:
            val += base_class['base'][stat]

        if promoted:

            if stat in ['hp', 'wlv']:
                if val < promo_class['base'][stat]:
                    val = promo_class['base'][stat]
            elif stat in ['lck']:
                pass
            else:
                if base_class['base'][stat] < promo_class['base'][stat]:
                    val += promo_class['base'][stat] - base_class['base'][stat]

            val = round(val + (total_growth * promoinc) / 100, 2)

        match stat:
            case 'hp':
                if val >= 52:
                    stats += 'HP **52** | '
                else:
                    stats += 'HP ' + str(val) + ' | '
            case _:
                if val >= 20:
                    stats += stat.title() + ' **20** | '
                else:
                    stats += stat.title() + ' ' + str(val) + ' | '

    stats = stats[:-3]
    embed.add_field(name='Stats', value=stats, inline=False)

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

    bases = ''
    for base in class_json['base']:
        match base:
            case 'hp':
                bases += 'HP ' + str(class_json['base'][base]) + ' | '
            case _:
                bases += base.title() + ' ' + str(class_json['base'][base]) + ' | '
    bases = bases[:-3] + '\n **EXP:** ' + str(class_json['exp'])

    if class_json['dismount']:
        bases += '\n**Dismount:** '
        dismount_class = get_class_json(class_json['dismount'])
        for stat in dismount_class['base']:
            val = dismount_class['base'][stat] - class_json['base'][stat]
            if val < 0 and stat not in ['hp', 'wlv']:
                bases += stat.title() + ' ' + str(val) + ' | '
        bases = bases[:-3]
    embed.add_field(name='Bases', value=bases, inline=False)

    weapons = ''
    for weapon in class_json['weapon']:
        weapons += weapon.title() + '\n'
    embed.add_field(name='Weapons', value=weapons, inline=True)
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
    stats = ''
    for value in item_json['stats']:
        match value:
            case 'mt' | 'hit' | 'crit' | 'wt' | 'rng':
                stats += value.title() + ' ' + str(item_json['stats'][value]) + ' | '

    stats = stats[:-3] + '  \n'
    for value in item_json['stats']:
        match value:
            case 'wlv' | 'uses':
                stats += value.title() + ' ' + str(item_json['stats'][value]) + ' | '

    stats = stats[:-3]

    if 'price' in item_json['stats']:
        stats += '\n**Price:** ' + str(item_json['stats']['price'])

    if 'sell' in item_json['stats']:
        stats += '\n**Sell:** ' + str(item_json['stats']['sell'])

    embed.add_field(name='', value=stats, inline=False)
    if item_json['desc']:
        desc = item_json['desc']
        embed.add_field(name='Notes:', value=desc, inline=False)
    return embed
