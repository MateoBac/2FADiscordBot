#info
#https://discord.com/api/oauth2/authorize?client_id=963812161841410058&permissions=1505922116823&scope=applications.commands%20bot
#Aktuel Deaktivirt

#Settings

Prefix = '2FA!' #Prefix der aber komplet egal ist und nur für den syntax hier ist XD

#Imports
#import save as s
import pyqrcode
import discord
from discord.ext import commands
import asyncio
from discord_slash import SlashCommand
import json
import pyotp

#init
bot = commands.Bot(command_prefix=Prefix,intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
def get_config(name):
    with open('config.json','r') as f:
        json_file = json.load(f)
    return json_file[name]
bot.remove_command('help')

#events
@bot.event
async def on_ready():
    print('Bot Ist Online')
    bot.loop.create_task(status())
async def status():
    while True:
        await bot.change_presence(status=discord.Status.online,activity=discord.Game('2FA Verify'))
        await asyncio.sleep(5)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(f'{len(set(bot.users))} Members'))
        await asyncio.sleep(5)
        await bot.change_presence(status=discord.Status.online,activity=discord.Game(f'/Fa'))
        await asyncio.sleep(5)
        await bot.change_presence(status=discord.Status.online,activity=discord.Game(f'{len(bot.guilds)} Servers'))
        await asyncio.sleep(5)
@bot.command
async def Test(ctx):
    print('test')
@slash.slash(name='Userinfo',description='get infos to a spicific user')
async def Userinfo(ctx,member:discord.Member):
    embed = discord.Embed(title=f'Userinfo to the user {member.display_name}')
    embed.add_field(name='Name:',value= f'{member.mention}',inline=True)
    embed.add_field(name='Status:',value= f'{member.status}',inline=True)
    embed.add_field(name='Server joint:',value=f'{member.joined_at}',inline=True)
    embed.add_field(name='Acc created:',value=f'{member.created_at}',inline=True)
    rollen = ''
    for role in member.roles:
        if not role.is_default():
            rollen += f'{role.mention} \r\n'
    if rollen:
        embed.add_field(name='Rollen', value=rollen, inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)
@slash.slash(name='ping',description='get the ping of the bot')
async def ping(ctx):
    embed = discord.Embed(title=f'@{ctx.author} ping: {round(bot.latency * 1000)}ms')
    await ctx.send(embed=embed)
@slash.slash(name='info',description='get infos to the bot')
async def info(ctx):
    embed = discord.Embed(name='Infos zum Bot:',description=f'The Bot von {bot.get_user(541971047776256021).mention} was createt at 13.04.2022 for a server thats have been deletet and so it became a 2FA Bot. invite the bot via https://discord.com/api/oauth2/authorize?client_id=963812161841410058&permissions=1505922116823&scope=applications.commands%20bot  Warning: This bot dont be 24/7 on yet because i dont have a server')
    await ctx.send(embed=embed)
#@slash.slash(name='Support',description='help the bot to stay online for free')
#async  def Support(ctx):
    #await ctx.send('help the bot to stay online for free: login at https://bot-hosting.net?aff=541971047776256021 thats make the bot last 1 weak longer')
@slash.slash(name='help',description='Get you help')
async def help(ctx):
    embed=discord.Embed(title='Help Menu',description='')
    embed.add_field(name='ping',value='get you the ping of the bot',inline=True)
    embed.add_field(name='userinfo',value='get infos to a spicific user',inline=True)
    embed.add_field(name='info',value='get the bot info')
    embed.add_field(name='fa', value='verify you whith you smartphone via auth app like google authenticator')
    #embed.add_field(name='Support', value='help the bot to stay online for free')
    await ctx.send(embed=embed)
@slash.slash(name='Fa',description='Test für die 2FA')
async def Fa(ctx,code=None):
    id = ctx.author.id
    try:
        file = open(f'{id}.key','r')
        temp = file.read()
        file.close()
        first = False
    except:
        try:
            await ctx.author.send('This is a Test if i can send you private messages')
        except:
            await ctx.send('please make you dms open for me')
            return
        file = open(f'{id}.key','x')
        temp = pyotp.random_base32()
        file.write(temp)
        file.close()
        first = True
    if first:
        uri = pyotp.totp.TOTP(temp).provisioning_uri(name='Mateos discord bot', issuer_name=f'{ctx.author}')
        qr = pyqrcode.create(uri)
        qr.png('qr.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
        await ctx.author.send(file=discord.File('qr.png'))
        await ctx.author.send(f'please scan this With you 2Fauth app\r\nor open this link on you handy {uri}')
        await ctx.send('check you dms')
    else:
        if code == None:
            await ctx.send('Please Enter you code')
            return
        else:
            totp = pyotp.TOTP(temp)
            if totp.now() == code:
                guild_id = str(ctx.guild.id)
                if s.load(guild_id) == []:
                    await ctx.send('the server dont have a verify yet')
                else:
                    role_id = int(s.load(guild_id)[2])
                    guild = ctx.guild
                    role = discord.utils.get(guild.roles, id=role_id)
                    await ctx.author.add_roles(role)
                    await ctx.send('Verifyed')
            else:
                await ctx.send('Invalid please try again')
@slash.slash(name='set_role',description='Set the verify rule')
async def set_role(ctx,role: discord.Role):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send('No Permission')
        return
    guild_id = ctx.guild.id
    s.save([str(guild_id),str(role.id)])
    await ctx.send(f'Verify role set to {role}')
bot.run(get_config("Token"))
