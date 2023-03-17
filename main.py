import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import datetime

load_dotenv('DiscordBot2/token.env')
token = os.getenv("TOKEN")
list_days_of_week = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"Bot is ready! {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith(bot.command_prefix):  # If message is command then delete msg
        await message.delete()
    await bot.process_commands(message)
    if message.content.lower() == 'do choroszczy?':
        await message.channel.send('Do choroszczy!')

    elif message.content.lower() == 'na badania?':
        await message.channel.send('Na badania!')


# ------------------------------------------------------------------------------San News Commands-------------

@bot.command()
async def lshelp(ctx):  # Commands
    embed = discord.Embed(title="Ustawienia",
                          description="!r- Ramówka\n!p- Dodaje program do ramówki [id] [Ilość osób] [Program]\n!u - Usuwa program z ramówki [id] [Pozycja do usunięcia]\n !c- Czyści kanał z wiadomośći [id kanału]\n !reklama- Nadaje informacje o reklamie długoterminowej [ilość dni] [treść]",
                          color=0x020080)
    await ctx.channel.send(embed=embed)


@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Director"] for role in ctx.author.roles))
async def p(ctx, message_id, message_persons, *message_text):  # Add to "ramowka"

    message = await ctx.channel.fetch_message(message_id)
    embed = message.embeds[0]
    embed.add_field(name=f"{' '.join(message_text)}", value=f"({message_persons}):", inline=False)
    await message.edit(embed=embed)


@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def r(ctx, week_start= 0): #Creat "ramówka'

    """Date to ramowka"""
    date = datetime.date.today()
    today_date = date.weekday()
    date_start_ramowka = date - datetime.timedelta(days=today_date)
    date_end_ramowka = date_start_ramowka + datetime.timedelta(days=6)

    embed = discord.Embed(title="{}".format('***RAMÓWKA***'), description=f"{date_start_ramowka.strftime('%d.%m.%Y')} - {date_end_ramowka.strftime('%d.%m.%Y')}", color=0x020080)
    embed.set_thumbnail(url="https://i.imgur.com/QZv9iSz.png")
    await ctx.channel.send(embed=embed)
    date_start_ramowka = date_start_ramowka - datetime.timedelta(days=1)

    '''Creating Embed'''
    for i in list_days_of_week:
        date_start_ramowka = date_start_ramowka + datetime.timedelta(days=1)
        embed = discord.Embed(title=f"{i} | {date_start_ramowka.strftime('%d.%m.%Y')}", description="", color=0x020080)
        await ctx.channel.send(embed=embed)


@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Director"] for role in ctx.author.roles))
async def u(ctx, message_id=0, *message_field):  # Delete message

    if message_id < 0:
        message_id = 0

    message_field = ' '.join(message_field)
    message = await ctx.channel.fetch_message(int(message_id))
    embed = message.embeds[0]
    for field in embed.fields:
        if message_field.lower() == field.name.lower():
            index = embed.fields.index(field)
            embed.remove_field(index)
            break

    await message.edit(embed=embed)


@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Director"] for role in ctx.author.roles))
async def c(ctx, message_id):  # Clear channel
    channel = bot.get_channel(int(message_id))
    await channel.purge(limit=9999999)


@bot.command()
async def reklama(ctx, days, *args): #Ads embed for SA News
    date = datetime.date.today()
    current_time = datetime.datetime.now()
    date_end_ads = date + datetime.timedelta(int(days)+1) #days to end ads
    ad_text = " ".join(args) + f"\n\n**{days}** dni, Koniec: **{date_end_ads.strftime('%d.%m.%Y')}**"
    embed = discord.Embed(title=f"Reklama {date.strftime('%d.%m')} {current_time.strftime('%H:%M')}", description=f'{ad_text}', color=0x020080)
    embed.set_thumbnail(url="https://i.imgur.com/QZv9iSz.png")
    await ctx.channel.send(embed=embed)


# ------------------------------------------------------------------------------FS COMMANDS-------------
@bot.command()
# @commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def fshelp(ctx):  # Commands
    embed = discord.Embed(title="Ustawienia",
                          description="!c- Czyści kanał z wiadomośći [id kanału]\n!fs - Mobilizacja Fire Service\n!coroner - Mobilizacja coronera\n!ems - Mobilizacja EMS",
                          color=0x020080)
    await ctx.channel.send(embed=embed)


@bot.command()
# @commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def fs(ctx):  # Fire Services mobilization
    role = ctx.guild.get_role(1079694926113144862)  # Role ID
    for x in range(0, 3):
        await ctx.channel.send(f'{role.mention} Mobilizacja!!!')

@bot.command()
# @commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def coroner(ctx):  # Coroner mobilization
    role = ctx.guild.get_role(1071873744848556073)  # Role ID
    for x in range(0, 3):
        await ctx.channel.send(f'{role.mention} Mobilizacja!!!')


@bot.command()
# @commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def ems(ctx):  # Coroner mobilization
    role = ctx.guild.get_role(1079695474988155002)  # Role ID
    for x in range(0, 3):
        await ctx.channel.send(f'{role.mention} Mobilizacja!!!')


# ------------------------------------------------------------------------------DEV COMMANDS-------------

@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Director"] for role in ctx.author.roles))
async def save(ctx):  # Save last embed, didnt work
    with open('C:/Users/kchar/PycharmProjects/DiscordBot/backups/embeds.json', 'w') as f:
        pass
    for embed in ctx.embeds:
        with open('C:/Users/kchar/PycharmProjects/DiscordBot/backups/embeds.json', 'a+') as f:
            f.write(json.dumps(embed.to_dict()) + '\n')


@bot.command()
@commands.check(
    lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Director"] for role in ctx.author.roles))
async def load(ctx):  # Load saved Embeds, didnt work!
    channel = discord.utils.get(ctx.guild.channels, name='test2')
    with open('C:/Users/kchar/PycharmProjects/DiscordBot/backups/embeds.json', 'r') as f:
        for line in f:
            embed_dict = json.loads(line)
            embed = discord.Embed.from_dict(embed_dict)
            await ctx.channel.send(embed=embed)


@bot.command()
@commands.check(
    lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Director"] for role in ctx.author.roles))
async def dev(ctx):  # Dev Commands
    embed = discord.Embed(title="Ustawienia",
                          description="!embed - pokazuje aktywne embed na kanale\n!save- zapisuje embed\n!load- wczytuje embed\nBot developed by Vetto",
                          color=0x020080)
    await ctx.channel.send(embed=embed)


@bot.command()
@commands.check(
    lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Director"] for role in ctx.author.roles))
async def path(ctx):  # Dev Commands
    embed = discord.Embed(title="path",
                          description="Naprawiono komendę !u\nZmienion jej działanie z [Numer wiadomośći] na [Nazwe wiadomości]",
                          color=0x020080)
    await ctx.channel.send(embed=embed)


@bot.command()
@commands.check(
    lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Director"] for role in ctx.author.roles))
async def embeds(ctx):
    print(discord.embeds)


# ------------------------------------------------------------------------------Reactions-------------


@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)
    embeds = message.embeds
    list_of_reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    if message.author != bot.user:
        return

    if payload.emoji.name in list_of_reactions:

        inedex = list_of_reactions.index(payload.emoji.name)  # Index emoji == embed index
        if len(embeds) > 0:
            embed = embeds[0]
            if not embed.title.split(' ')[0] in list_days_of_week:  # checking if the embed is from !r command
                await message.remove_reaction(emoji, user)
                return
            elif f'{user.mention}' in embed.fields[inedex].value.split(', ') or f'{user.mention},' in embed.fields[
                inedex].value.split(': '):
                await message.remove_reaction(emoji, user)
                return
            embed.set_field_at(index=inedex, name=embed.fields[inedex].name,
                               value=f'{embed.fields[inedex].value} {user.mention}, ', inline=False)
            await message.edit(embed=embed)
        await message.remove_reaction(emoji, user)


bot.run(token)