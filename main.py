import discord
from discord.ext import commands
import json

def read_token():
    with open("C:/Users/kchar/PycharmProjects/DiscordBot/token", 'r') as f:
        lines = f.readline()
        return lines

token = read_token()
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

#------------------------------------------------------------------------------San News Commands-------------

@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def help(ctx): #Commands
    embed = discord.Embed(title="Ustawienia",
                          description="!r- Ramówka\n!p- Dodaje program do ramówki [id] [Ilość osób] [Program]\n!u - Usuwa program z ramówki [id] [Pozycja do usunięcia]\n !c- Czyści kanał z wiadomośći [id kanału]",
                          color=0x020080)
    await ctx.channel.send(embed=embed)

@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def p(ctx, message_id, message_persons, *message_text): #Add to "ramowka"

    message = await ctx.channel.fetch_message(message_id)
    embed = message.embeds[0]
    embed.add_field(name=f"{' '.join(message_text)}", value=f"({message_persons}):", inline=False)
    await message.edit(embed=embed)

@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def r(ctx): #Creat "ramówka'
    embed = discord.Embed(title=f"**Ramówka**", description="", color=0x020080)
    await ctx.channel.send(embed=embed)

    '''Creating Embed'''
    for i in list_days_of_week:
        embed = discord.Embed(title=f"{i}", description="", color=0x020080)
        await ctx.channel.send(embed=embed)


@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def u(ctx, message_id = 0, message_index = 0): #Delete message
    if message_id > 0:
        message_id = 0

    message = await ctx.channel.fetch_message(int(message_id))
    embed = message.embeds[0]
    embed.remove_field(int(message_index))
    await message.edit(embed=embed)

@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def c(ctx, message_id): #Clear channel
    channel = bot.get_channel(int(message_id))
    await channel.purge(limit=9999999)

#------------------------------------------------------------------------------DEV COMMANDS-------------

@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def save(ctx): # Save last embed, didnt work
    with open('C:/Users/kchar/PycharmProjects/DiscordBot/backups/embeds.json', 'w') as f:
        pass
    for embed in ctx.embeds:
        with open('C:/Users/kchar/PycharmProjects/DiscordBot/backups/embeds.json', 'a+') as f:
            f.write(json.dumps(embed.to_dict()) + '\n')

@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def load(ctx):  # Load saved Embeds, didnt work!
    channel = discord.utils.get(ctx.guild.channels, name='test2')
    with open('C:/Users/kchar/PycharmProjects/DiscordBot/backups/embeds.json', 'r') as f:
        for line in f:
            embed_dict = json.loads(line)
            embed = discord.Embed.from_dict(embed_dict)
            await ctx.channel.send(embed=embed)

@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def dev(ctx): #Dev Commands
    embed = discord.Embed(title="Ustawienia", description="!embed - pokazuje aktywne embed na kanale\n!save- zapisuje embed\n!load- wczytuje embed\nBot developed by Vetto", color=0x020080)
    await ctx.channel.send(embed=embed)

@bot.command()
@commands.check(lambda ctx: any(role.name in ["Chief Executive Officer", "Executive Officer"] for role in ctx.author.roles))
async def embeds(ctx):
    print(discord.embeds)


#------------------------------------------------------------------------------Reactions-------------


@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)
    embeds = message.embeds
    list_of_reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

    if payload.emoji.name in list_of_reactions:

        inedex = list_of_reactions.index(payload.emoji.name) #Index emoji == embed index
        if len(embeds) > 0:
            embed = embeds[0]
            if not embed.title in list_days_of_week: #checking if the embed is from !r command
                await message.remove_reaction(emoji, user)
                return

            embed.set_field_at(index=inedex, name=embed.fields[inedex].name, value=f'{embed.fields[inedex].value} {user.mention}, ', inline=False)
            await message.edit(embed=embed)
        await message.remove_reaction(emoji, user)


bot.run(token)


