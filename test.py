import discord
import datetime
import asyncio
import time
import random

from discord.ext import commands
from discord.ext import tasks

TOKEN = ""

bot = commands.Bot(command_prefix='!')  # 명령어 접두사는 !  디스코드 봇 객체

saving = []
ids = []


def setEmbed(Title, Footer, Description, Color, Thumbnail, **kwargs):
    embed = discord.Embed(title=Title, description=Description, color=Color)
    # embed.set_author(name=Name, icon_url=Icon_Url)
    embed.set_thumbnail(url=Thumbnail)
    for x in kwargs.keys():
        embed.add_field(name=x, value=kwargs[x], inline=Inline)
    embed.set_footer(text=Footer)
    return embed


save_embed = setEmbed(Title="경뿌 연탐정보", Footer="`by 만빵`", Description="`연탐 목록`", Color=0xff0000,
                      Thumbnail="https://cdn.discordapp.com/attachments/798083672477138990/798755603374931968/image.PNG"
                      )


# 정보 저장함수
def save_data(place, start, fin, cnt, saved_time, timer, userid):
    saving.append([place, start, fin, cnt, saved_time, timer, userid])


def save_id(server_id, channel_id):
    for x in range(len(ids)):
        if ids[x][0] == server_id:
            return
    ids.append([server_id, channel_id])


# 시간 알리미
"""
@tasks.loop(seconds=1)
async def flag_notice_12():
    if datetime.datetime.now().hour == 12 and datetime.datetime.now().minute == 0 and datetime.datetime.now().second == 0:
        await bot.get_guild(798083672477138987).get_channel(798083672477138990).send(
            "현재 {}시 플래그 시간입니다.".format(datetime.datetime.utcnow().hour + 9, datetime.datetime.utcnow().minute),
            tts=True)
        time.sleep(1)
"""


@tasks.loop(seconds=1)
async def alimi():
    remove_flag = 0
    remove_index = []
    same = []
    flag = 0
    for i in range(len(saving)):

        if saving[i][1] == 0:  # start가 0이면 -1이 되므로 60으로 변환
            saving[i][1] = 60
            flag += 1

        if ((datetime.datetime.now().minute == int(saving[i][1] - 1)) and datetime.datetime.now().second == 0) or \
                ((datetime.datetime.now().minute == int(saving[i][2] - 1)) and datetime.datetime.now().second == 0):

            if flag == 1:
                saving[i][1] = 0

            for t in range(len(ids)):  # 동작중인 서버에 메시지 뿌림
                await bot.get_guild(ids[t][0]).get_channel(ids[t][1]).send(f'```{saving[i][0]} 경뿌 1분전```',
                                                                           tts=True)

        if saving[i][1] == 60:
            saving[i][1] = 0

        if ((datetime.datetime.now().minute == int(saving[i][1])) and datetime.datetime.now().second == 0) or \
                ((datetime.datetime.now().minute == int(saving[i][2])) and datetime.datetime.now().second == 0):
            saving[i][3] -= 1  # cnt
            saving[i][4] += 1  # saved_time
            save_embed.set_field_at(i, name="%s " % str(saving[i][0]),
                                    value="```diff\n!%d:\n- %s분 ,%s분, %s회 연탐 남았습니다!\n(%d/%s)```" % (i + 1,
                                                                                                    str(saving[i][1]),
                                                                                                    str(saving[i][2]),
                                                                                                    str(saving[i][3]),
                                                                                                    saving[i][4],
                                                                                                    str(saving[i][5])),
                                    inline=False)

            if saving[i][3] == 0:  # cnt=0이되면 연탐 정보 삭제
                for t in range(len(ids)):
                    await bot.get_guild(ids[t][0]).get_channel(ids[t][1]).send(f'{saving[i][0]} 경뿌 종료')
                save_embed.remove_field(i)
                remove_index.append(i)

    if len(remove_index) >= 1:
        for x in range(len(remove_index)):
            saving.pop(remove_index[x])


@bot.event
async def on_ready():  # 봇이 준비가 되면 1회 실행되는 부분
    print(bot.user.id)
    print("ready")
    game = discord.Game("디스코드")
    print(f'{bot.user} online!')

    await bot.change_presence(status=discord.Status.online, activity=game)

    alimi.start()


@bot.event
async def on_message(message):
    # 이벤트 기반으로 명령사용 가능
    await bot.process_commands(message)
    # 봇이 입력한 메시지라면 무시하고 넘어간다.
    if message.author == bot.user:
        return None

    if message.content.startswith("안녕"):
        await message.channel.send("안녕하세요")  # 이 구문은 메시지가 보내진 채널에 메시지를 보내는 구문입니다.

    server = message.guild.id
    channel = message.channel.id
    save_id(server, channel)


@bot.event
async def on_member_join(ctx):
    await ctx.send("ㅎㅇ")

@bot.command(name='리스트')
async def show_list(ctx):
    await ctx.send(saving)


@bot.command(name='안녕')
async def hello(ctx):
    await ctx.send("안녕하세요")


@bot.command(name='시간')
async def time_now(ctx):
    embed = discord.Embed(title="현재 시간", description="`현재 시간을 알려드립니다`",
                          color=0xff0000, timestamp=datetime.datetime.utcnow())
    await ctx.send(embed=embed)


@bot.command(name="연탐")
async def save_time(ctx, txt, start: int, fin: int, cnt: int):
    server = ctx.guild.id
    channel = ctx.channel.id
    save_id(server, channel)
    userid = ctx.message.author

    x = start - fin
    if abs(x) == 30:
        saved_time = 0

        save_data(txt, start, fin, cnt, saved_time, cnt, userid)
        l = len(saving)
        save_embed.add_field(name="%s" % str(saving[l - 1][0]),
                             value="```diff\n!%d:\n- %s분 ,%s분, %s회 연탐 남았습니다!\n(%d/%s)```" % (l,
                                                                                             str(saving[l - 1][1]),
                                                                                             str(saving[l - 1][2]),
                                                                                             str(saving[l - 1][3]), 0,
                                                                                             str(saving[l - 1][3])),
                             inline=False)
        await ctx.send(f'{txt} {start}분~{fin}분 경뿌 {cnt}연탐 저장되었습니다')
    else:
        await ctx.send("잘못된 입력입니다.")


@save_time.error
async def save_time_error(ctx, error):
    await ctx.send("!연탐 (장소) (시작시간) (끝시간) (횟수) 로 적어주세요")


@bot.command(name="출력")
async def show_id(ctx):
    for x in range(len(ids)):
        await ctx.send(f'server id: {ids[x][0]}  channel id: {ids[x][1]}')


@bot.command(name="알려줘")
async def show_time1(ctx):
    timenow = datetime.datetime.utcnow().minute
    for x in range(len(saving)):  # 번호를 붙혀서 업데이트
        a = saving[x][1]+60-timenow
        b = saving[x][2]+60-timenow

        if a > 60:
            a = a-60
        if b > 60:
            b = b-60
            
        if a > b:
            tmax = b
        else:
            tmax = a

        name = str(saving[x][6])

        save_embed.set_field_at(x, name="%s " % str(saving[x][0]),
                                value="```diff\n!%d:\n- %s분 ,%s분, %s회 연탐, %d분 남았습니다!\n(%d/%s) added by %s```" % (x + 1,
                                                                                                     str(saving[x][1]),
                                                                                                     str(saving[x][2]),
                                                                                                     str(saving[x][3]),
                                                                                                     tmax,
                                                                                                     saving[x][4],
                                                                                                     str(saving[x][5]),
                                                                                                     name[:-5]),
                                inline=False)
    await ctx.send(embed=save_embed)


@bot.command(name="삭제")
async def delete(ctx, index: int):
    if index <= 0:
        await ctx.send("1이상의 정수를 입력하세요")
        return
    if index > len(saving):
        await ctx.send("저장된 공간보다 큰 숫자는 입력이 불가능합니다")
        return
    save_embed.remove_field(index - 1)  # 입력된 인덱스 삭제
    saving.pop(index - 1)
    await ctx.send(f'{index} 번 연탐 정보 삭제.')
    for x in range(len(saving)):  # 번호를 붙혀서 업데이트
        save_embed.set_field_at(x, name="%s " % str(saving[x][0]),
                                value="```diff\n!%d:\n- %s분 ,%s분, %s회 연탐 남았습니다!\n(%d/%s)```" % (x + 1,
                                                                                                str(saving[x][1]),
                                                                                                str(saving[x][2]),
                                                                                                str(saving[x][3]),
                                                                                                saving[x][4],
                                                                                                str(saving[x][5])),
                                inline=False)
    # await ctx.send(embed=save_embed)


@delete.error
async def delete_error(ctx, error):
    await ctx.send("!삭제 (삭제할 번호) 식으로 입력해주십시오")


bot.run(TOKEN)
