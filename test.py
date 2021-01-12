import discord
import datetime
import time
import random

from discord.ext import commands

TOKEN = ""

bot = commands.Bot(command_prefix='!')  # 명령어 접두사는 !  디스코드 봇 객체


@bot.event
async def on_ready():  # 봇이 준비가 되면 1회 실행되는 부분
    print(bot.user.id)
    print("ready")
    game = discord.Game("디스코드")
    print(f'{bot.user} online!')
    await bot.change_presence(status=discord.Status.online, activity=game)


"""
@client.event
async def on_message(message):  # 메시지가 들어 올 때마다 가동되는 구문.
    # 봇이 입력한 메시지라면 무시하고 넘어간다.
    if message.author == client.user:
        return None

    if message.content.startswith("!안녕"):
        await message.channel.send("안녕하세요")  # 이 구문은 메시지가 보내진 채널에 메시지를 보내는 구문입니다.

    if message.content.startswith("!시간"):
        embed = discord.Embed(title="현재 시간", description="현재 시간을 알려드립니다",
                              color=0xff0000, timestamp=datetime.datetime.utcnow())

        await message.channel.send(embed=embed) """


@bot.command(name='주사위', help='주사위를 돌립니다. 입력양식: !주사위 숫자 ex) !주사위 5')  # name은 명령어의 이름 , ctx 매개변수안에는 context 객체
async def roll(ctx, number: int):
    await ctx.send(f'1에서 {number} 까지의 주사위를 굴립니다')
    await ctx.send(f'주사위 결과: {random.randint(1, int(number))}')


@roll.error
async def roll_error(ctx, error):
    await ctx.send("알맞은 명령어를 쓰세요! 입력양식: !주사위 숫자")


@bot.command(name='안녕')
async def hello(ctx):
    await ctx.send("안녕하세요")


@bot.command(name='시간')
async def time_now(ctx):
    embed = discord.Embed(title="현재 시간", description="현재 시간을 알려드립니다",
                          color=0xff0000, timestamp=datetime.datetime.utcnow())
    await ctx.send(embed=embed)

bot.run(TOKEN)
