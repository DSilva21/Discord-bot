import discord
import datetime
import asyncio
import time
import random

from discord.ext import commands
from discord.ext import tasks

TOKEN = 

bot = commands.Bot(command_prefix='!')  # 명령어 접두사는 !  디스코드 봇 객체

saving = []


def setEmbed(Title, Footer, Name, Icon_Url, Description, Color, Inline, Thumbnail, **kwargs):
    embed = discord.Embed(title=Title, description=Description, color=Color)
    embed.set_author(name=Name, icon_url=Icon_Url)
    embed.set_thumbnail(url=Thumbnail)
    for x in kwargs.keys():
        embed.add_field(name=x, value=kwargs[x], inline=Inline)
    embed.set_footer(text=Footer)
    return embed


sample = setEmbed(Title="테스트 임베드", Footer="이것은 푸터입니다.", Description="이것은 Embed입니다.", Color=0xff0000,
                  Name="만빵", Icon_Url="https://cdn.discordapp.com/attachments/"
                                      "798083672477138990/798755603374931968/image.PNG",
                  Inline=False,
                  Thumbnail="https://cdn.discordapp.com/attachments/798083672477138990/798755603374931968/image.PNG",
                  이것은_필드_1입니다="필드의 값입니다.",
                  이것은_필드_4입니다="필드의 값입니다.")

save_embed = setEmbed(Title="경뿌 연탐정보", Footer="연탐알리미.", Description="저장된 연탐목록 입니다.", Color=0xff0000,
                      Name="만빵", Icon_Url="https://cdn.discordapp.com/attachments/"
                                          "798083672477138990/798755603374931968/image.PNG",
                      Inline=False,
                      Thumbnail="https://cdn.discordapp.com/attachments/798083672477138990/798755603374931968/image.PNG"
                      )


# 정보 저장함수
def save_data(place, start, fin, cnt, saved_time):
    saving.append([place, start, fin, cnt, saved_time])



"""
embed1 = discord.Embed(title="테스트", description="Embed 테스트", color=0xff0000)
embed1.set_author(name="만빵", icon_url="https://cdn.discordapp.com/attachments/"
                                       "798083672477138990/798755603374931968/image.PNG")
embed1.set_thumbnail(url= "https://cdn.discordapp.com/attachments/798083672477138990/798755603374931968/image.PNG")
embed1.add_field(name="필드1", value="필드1의 값", inline=False)
embed1.add_field(name="필드2", value="필드2의 값", inline=False)
embed1.set_footer(text="푸터")"""

"""
@tasks.loop(seconds=3600)
async def my_background_task():
    await bot.get_guild(798083672477138987).get_channel(798083672477138990).send("hi")
    await asyncio.sleep(600)
"""


# 시간 알리미
@tasks.loop(seconds=1)
async def notice():
    if datetime.datetime.now().minute == 32 and datetime.datetime.now().second == 0:
        await bot.get_guild(798083672477138987).get_channel(798083672477138990).send("현재 {}시 {}분 입니다.".format(datetime.datetime.now().hour, datetime.datetime.now().minute), tts=True)
        time.sleep(1)


@tasks.loop(seconds=1)
async def alimi():
    saving_len = len(saving)
    remove_flag = 0
    remove_index = []
    for i in range(saving_len):
        if ((datetime.datetime.now().minute == int(saving[i][1]-1)) and datetime.datetime.now().second == 0) or \
                ((datetime.datetime.now().minute == int(saving[i][2]-1)) and datetime.datetime.now().second == 0):
            saving[i][3] -= 1
            await bot.get_guild(798083672477138987).get_channel(798083672477138990).send(f'{saving[i][0]} 경뿌 1분전', tts=True)
            if saving[i][3] == 0:
                save_embed.remove_field(i)
                remove_index.append(i)
                await bot.get_guild(798083672477138987).get_channel(798083672477138990).send(f'{saving[i][0]} 경뿌 종료')
                time.sleep(1)

    if len(remove_index) >= 1:
        for x in range(len(remove_index)):
            saving.pop(remove_index[x])
            time.sleep(1)





@bot.event
async def on_ready():  # 봇이 준비가 되면 1회 실행되는 부분
    print(bot.user.id)
    print("ready")
    game = discord.Game("디스코드")
    print(f'{bot.user} online!')
    await bot.change_presence(status=discord.Status.online, activity=game)
    notice.start()
    alimi.start()
    # my_background_task.start()



@bot.event
async def on_message(message):
    # 이벤트 기반으로 명령사용 가능
    await bot.process_commands(message)
    # 봇이 입력한 메시지라면 무시하고 넘어간다.
    if message.author == bot.user:
        return None

    if message.content.startswith("안녕"):
        await message.channel.send("안녕하세요")  # 이 구문은 메시지가 보내진 채널에 메시지를 보내는 구문입니다.

    if message.content.startswith("음성"):
        txt = saving[0][0]
        await message.channel.send(f'{txt} 경뿌 1분전', tts=True)


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


@bot.command(name='테스트')
async def test_embed(ctx):
    await ctx.send(embed=sample)


@bot.command(name="알람")
async def alarm(ctx, sleep_time: int):
    await ctx.send(f'알람 {sleep_time}초 카운트 시작')
    await asyncio.sleep(sleep_time)
    await ctx.send(f'알람 {sleep_time}초 끝')


@alarm.error
async def alarm_error(ctx, error):
    await ctx.send("알람 입력 숫자를 쓰세요")


@bot.command(name="연탐")
async def save_time(ctx, txt, start: int, fin: int, cnt: int):
    x = start-fin
    if abs(x) == 30:
        saved_time = datetime.datetime.now()
        save_data(txt, start, fin, cnt, saved_time)
        i = len(saving)
        save_embed.add_field(name="%s " % str(saving[i - 1][0]),
                             value="%s분 ,%s분 %s회 연탐입니다. " % (
                             str(saving[i - 1][1]), str(saving[i - 1][2]), str(saving[i - 1][3])),
                             inline=False)
        await ctx.send(f'{txt} {start}분~{fin}분 경뿌 {cnt}연탐 저장되었습니다')
    else:
        await ctx.send("잘못된 입력입니다.")


@save_time.error
async def save_time_error(ctx, error):
    await ctx.send("!연탐 (장소) (시작시간) (끝시간) (횟수) 로 적어주세요")


@bot.command(name="알려줘")
async def show_time1(ctx):
    await ctx.send(embed=save_embed)


@bot.command(name="삭제")
async def delete(ctx):
    save_embed.remove_field(0)  # 가장 처음 정보 삭제중
    await ctx.send("연탐 정보 삭제.")
    await ctx.send(embed=save_embed)


@bot.command(name="음성")
async def say(ctx):
    txt = saving[0][0]
    await ctx.send(f'{txt} 경뿌 1분전 ', tts=True)


bot.run(TOKEN)


