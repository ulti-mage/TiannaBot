import discord
from discord import app_commands
import json

bws_unit_data_file = 'bws/unitdata.json'
bws_item_data_file = 'bws/itemdata.json'
bws_skill_data_file = 'bws/skilldata.json'
bws_furniture_data_file = 'bws/furnituredata.json'
bws_food_data_file = 'bws/fooddata.json'


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
            for i in self.children:
                if i.label != 'Stats':
                    i.disabled = False
            button.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Other', style=discord.ButtonStyle.blurple)
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(bws_unit_data_file, 'r') as f:
            unit_json = json.load(f)
            name = interaction.message.embeds[0].to_dict()["title"].lower()
            embed = get_unit_requirement_embed(unit_json[name])
            embed.set_thumbnail(url='attachment://' + unit_json[name]['portrait'])
            for i in self.children:
                if i.label != 'Other':
                    i.disabled = False
            button.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)


async def unit(interaction: discord.Interaction, name: str):
    with open(bws_unit_data_file, 'r') as f:
        unit_json = json.load(f)
        view = UnitButton(interaction)
        found = False
        for k in unit_json:
            if k.lower().startswith(name.lower()):
                embed = get_unit_stats_embed(unit_json[k])
                portrait = discord.File('bws/images/' + unit_json[k]['portrait'], filename=unit_json[k]['portrait'])
                embed.set_thumbnail(url='attachment://' + unit_json[k]['portrait'])
                await interaction.response.send_message(embed=embed, file=portrait, view=view)
                found = True
                break
        if not found:
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
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
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
            promotionwrank = ''
            for stat in unit_json['promo']['bonus']:
                match stat:
                    case 'hp':
                        promotion += 'HP +' + str(unit_json['promo']['bonus'][stat]) + ' | '
                    case _:
                        promotion += stat.title() + ' +' + str(unit_json['promo']['bonus'][stat]) + ' | '
            promotion = promotion[:-3]
            for weapon in unit_json['promo']['weapon']:
                promotionwrank += weapon + ' ' + \
                             unit_json['promo']['weapon'][weapon]['base'] + ' ' + \
                             '(' + unit_json['promo']['weapon'][weapon]['growth'] + '%) | '
            promotionwrank = promotionwrank[:-3]
            embed.add_field(name='Promotion', value=promotion + '\n' + promotionwrank, inline=False)
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
    embed = discord.Embed(title=unit_json['name'], color=0x8a428a)
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
        found = False
        for k in item_json:
            if k.lower().startswith(name.lower()):
                embed = get_item_stats_embed(item_json[k])
                await interaction.response.send_message(embed=embed)
                found = True
                break
        if not found:
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
    embed = discord.Embed(title=item_json['name'], color=0x8a428a)
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


async def skill(interaction: discord.Interaction, name: str):
    with open(bws_skill_data_file, 'r') as f:
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


def get_skill_name_choices(ctx: str) -> list[app_commands.Choice]:
    with open(bws_skill_data_file, 'r') as f:
        skill_json = list(json.load(f).keys())
        choices = []
        for name in skill_json:
            if (ctx.lower() in name.lower()) and (len(choices) < 25):
                choices.append(app_commands.Choice(name=name, value=name))
    return choices


def get_skill_data_embed(skill_json: json) -> discord.Embed:
    embed = discord.Embed(title=skill_json['name'], color=0x8a428a)
    info = ''
    for value in skill_json:
        match value:
            case 'type':
                info += '**Type: **' + skill_json['type']
            case 'chance':
                info += '\n**Chance: **' + skill_json['chance']
    embed.add_field(name='', value=info, inline=False)
    embed.add_field(name='', value=skill_json['description'], inline=False)
    return embed


async def furniture(interaction: discord.Interaction, name: str):
    with open(bws_furniture_data_file, 'r') as f:
        furniture_json = json.load(f)
        found = False
        if name == 'explain':
            embed = discord.Embed(color=0x8a428a)
            image = discord.File('bws/images/explain.png', filename='explain.png')
            embed.set_image(url='attachment://' + 'explain.png')
            await interaction.response.send_message(embed=embed, file=image)
        for k in furniture_json:
            if k.lower().startswith(name.lower()):
                embed = get_furniture_data_embed(furniture_json[k])
                await interaction.response.send_message(embed=embed)
                found = True
                break
        if not found:
            await interaction.response.send_message('That furniture does not exist', ephemeral=True)


def get_furniture_name_choices(ctx: str) -> list[app_commands.Choice]:
    with open(bws_furniture_data_file, 'r') as f:
        furniture_json = list(json.load(f).keys())
        choices = []
        for name in furniture_json:
            if (ctx.lower() in name.lower()) and (len(choices) < 25):
                choices.append(app_commands.Choice(name=name, value=name))
    return choices


def get_furniture_data_embed(furniture_json: json) -> discord.Embed:
    embed = discord.Embed(title=furniture_json['name'], color=0x8a428a)
    embed.add_field(name='', value=furniture_json['description'], inline=False)
    for value in furniture_json:
        match value:
            case 'cost':
                embed.add_field(name='', value='Cost: ' + str(furniture_json['cost']) + ' D.', inline=False)
    return embed


class FoodButton(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx

    async def on_timeout(self) -> None:
        message = await self.ctx.original_response()
        for i in self.children:
            i.disabled = True
        await message.edit(view=self)

    @discord.ui.button(label='Liked', style=discord.ButtonStyle.blurple, disabled=True)
    async def liked(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(bws_food_data_file, 'r') as f:
            food_json = json.load(f)
            name = interaction.message.embeds[0].to_dict()["title"].lower()
            embed = get_food_liked_embed(food_json[name.title()])
            for x in self.children:
                if x.label != 'Liked':
                    x.disabled = False
            button.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Neutral', style=discord.ButtonStyle.blurple)
    async def neutral(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(bws_food_data_file, 'r') as f:
            food_json = json.load(f)
            name = interaction.message.embeds[0].to_dict()["title"].lower()
            embed = get_food_neutral_embed(food_json[name.title()])
            for x in self.children:
                if x.label != 'Neutral':
                    x.disabled = False
            button.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Disliked', style=discord.ButtonStyle.blurple)
    async def disliked(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(bws_food_data_file, 'r') as f:
            food_json = json.load(f)
            name = interaction.message.embeds[0].to_dict()["title"].lower()
            embed = get_food_disliked_embed(food_json[name.title()])
            for x in self.children:
                if x.label != 'Disliked':
                    x.disabled = False
            button.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)


async def food(interaction: discord.Interaction, name: str):
    with open(bws_food_data_file, 'r') as f:
        food_json = json.load(f)
        view = FoodButton(interaction)
        found = False
        for k in food_json:
            if k.lower().startswith(name.lower()):
                embed = get_food_liked_embed(food_json[k])
                await interaction.response.send_message(embed=embed, view=view)
                found = True
                break
        if not found:
            await interaction.response.send_message('That food does not exist', ephemeral=True)


def get_food_name_choices(ctx: str) -> list[app_commands.Choice]:
    with open(bws_food_data_file, 'r') as f:
        food_json = list(json.load(f).keys())
        choices = []
        for name in food_json:
            if (ctx.lower() in name.lower()) and (len(choices) < 25):
                choices.append(app_commands.Choice(name=name, value=name))
    return choices


def get_food_liked_embed(food_json: json) -> discord.Embed:
    embed = discord.Embed(title=food_json['name'], color=0x8a428a)
    embed.add_field(name='Bonus', value=food_json['likedbonus'], inline=False)
    embed.add_field(name='Rank', value=food_json['rank'], inline=True)
    embed.add_field(name='Price', value=str(food_json['price']) + ' D.', inline=True)
    embed.add_field(name='Liked by:', value=food_json['likedunits'], inline=False)
    return embed


def get_food_neutral_embed(food_json: json) -> discord.Embed:
    embed = discord.Embed(title=food_json['name'], color=0x8a428a)
    embed.add_field(name='Bonus', value=food_json['neutralbonus'], inline=False)
    embed.add_field(name='Rank', value=food_json['rank'], inline=True)
    embed.add_field(name='Price', value=str(food_json['price']) + ' D.', inline=True)
    embed.add_field(name='Indifferent:', value=food_json['neutralunits'], inline=False)
    return embed


def get_food_disliked_embed(food_json: json) -> discord.Embed:
    embed = discord.Embed(title=food_json['name'], color=0x8a428a)
    embed.add_field(name='Bonus', value=food_json['dislikedbonus'], inline=False)
    embed.add_field(name='Rank', value=food_json['rank'], inline=True)
    embed.add_field(name='Price', value=str(food_json['price']) + ' D.', inline=True)
    embed.add_field(name='Disliked by:', value=food_json['dislikedunits'], inline=False)
    return embed
