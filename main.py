
Prefix = '2FA!' #Prefix der aber komplet egal ist und nur für den syntax hier ist

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

@bot.command
async def Test(ctx):
    print('test')
@slash.slash(name='ping',description='get the ping of the bot')
async def ping(ctx):
    embed = discord.Embed(title=f'@{ctx.author} ping: {round(bot.latency * 1000)}ms')
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
bot.run(get_config("Token"))#Token Ist das einzige in der config deswegen hier nicht drinnen da das Token Sowiso nicht gezeigt werden sollte
