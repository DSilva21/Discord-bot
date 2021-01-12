import discord
client = discord.Client()


@client.event
async def on_ready():  # 봇이 준비가 되면 1회 실행되는 부분
    print(client.user.id)
    print("ready")
    game = discord.Game("디스코드")
    await client.change_presence(status=discord.Status.online, activity=game)



@client.event
async def on_message(message):  # 메시지가 들어 올 때마다 가동되는 구문.
    if message.content.startswith("!안녕"):
        await message.channel.send("안녕하세요")  # 이 구문은 메시지가 보내진 채널에 메시지를 보내는 구문입니다.




client.run("Nzk4MDgzMTkyMzI1NTM3ODIy.X_v25A.Y5PgSAm1eHh70vVD8cRNCNianmQ")