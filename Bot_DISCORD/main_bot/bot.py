import asyncio
import nacl
import requests
from bs4 import BeautifulSoup
import re
import discord
import youtube_dl
from discord.ext import commands
import os

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))
next_music = []
ban = {}
flag = True

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    global ban, flag
    list = ['бля', 'блять', 'сука', 'нахуй', "на хуй", "пизда", "ебал", "ебать", "на xуй", "на хyй", "на xyй", "нa хуй",
            "нa xуй", "нa хyй", "нa xyй", 'cука', 'сyка', 'сукa', 'cyка', 'cукa', 'cyкa', 'сyкa', "бздун", 'бзднуть',
            'бздюх','блудилище','выпердеть','высраться','выссаться','говно','говенка','говноед','говномес','говночист',
            'говяга','говнюк','говняный','говна пирога','глиномес','изговнять','гнида','гнидас','гнидазавр',
            'гниданидзе','гондон','гондольер','даун','даунитто','дерьмо','дерьмодемон','дерьмище','дрисня','дрист',
            'дристануть','обдристаться','дерьмак','дристун','дрочить','дрочила','суходрочер','дебил','дебилоид',
            'дрочка','драчун','задрот','дцпшник','елда','елдаклык','елдище','жопа','жопошник','залупа','залупиться',
            'залупинец','засеря','засранец','засрать','защеканец','изговнять','идиот','изосрать','курва','кретин',
            'кретиноид','курвырь','лезбуха','лох','минетчица','мокрощелка','мудак','мудень','мудила','мудозвон',
            'мудацкая','мудасраная дерьмопроелдина','мусор','педрик','пердеж','пердение','пердельник','пердун',
            'пидор','пидорасина','пидорормитна','пидорюга','педерастер','педобратва','дружки педигрипал','писька',
            'писюн','спидозный пес','ссаная псина','спидораковый','срать','спермер','спермобак','спермодун','срака',
            'сракаборец','сракалюб','срун','сучара','сучище','титьки','трипер','хер','херня','херовина','хероед',
            'охереть','пошел на хер','хитрожопый','хрен моржовый','шлюха','шлюшидзе']

    if message.author == bot.user:
        return

    if flag == True:
        for i in list:
            if i in message.content.lower() and message.author not in ban:
                await message.delete()
                ban[message.author] = 1
                await message.channel.send(f'❌ Ай ай ай {message.author}! А здесь материться нельзя! Это пока {ban[message.author]} случай. На третий раз ЗАБАНЮ!')
                break

            if i in message.content.lower() and ban[message.author] < 2:
                await message.delete()
                ban[message.author] += 1
                await message.channel.send(f'❌ Ай ай ай {message.author}! А здесь материться нельзя! Это пока {ban[message.author]} случай. На третий раз ЗАБАНЮ!')
                break

            if i in message.content.lower() and ban[message.author] == 2:
                await message.delete()
                await message.author.ban(reason='Нецензурное выражение.')
                await message.channel.send(f'БАН {message.author}! Причина: нецензурное выражение.')
                del ban[message.author]
                break

    if flag == False:
        pass

    await bot.process_commands(message)

@bot.command()
async def status(ctx):
    global ban
    if ctx.message.author not in ban:
        await ctx.send('У вас нет предупреждений. Вы очень галантный и вежливый пользователь. Продолжайте в том-же духе! ☺')
    else:
        await ctx.send(f'{ctx.message.author}, у вас на счету {ban[ctx.message.author]} предупреждения. Будет 3 и вас забанят, так что будьте аккуратны в выражениях.')

@bot.command()
async def clear(ctx, limit=None):
    if limit == None and ctx.message.author.guild_permissions.manage_messages == True:
        await ctx.channel.purge()

    if limit != None and ctx.message.author.guild_permissions.manage_messages == True:
        await ctx.channel.purge(limit=int(limit)+1)

    if ctx.message.author.guild_permissions.manage_messages == False:
        await ctx.send('❌ У вас нет такого права.')

@bot.command()
async def pause(ctx: commands.Context):
    ctx.voice_client.pause()
    await ctx.send('⏹ Для того чтобы продолжить напишите !resume')

@bot.command()
async def resume(ctx: commands.Context):
    ctx.voice_client.resume()
    await ctx.send('⏯ Для того чтобы поставить на паузу напишите !pause')

@bot.command()
async def stop(ctx: commands.Context):
    global next_music
    next_music.clear()
    await ctx.voice_client.disconnect()

@bot.command()
async def list(ctx):
    global next_music
    if len(next_music) == 0:
        await ctx.send('❌ Сейчас список музыки пуст.')
    for i in range(0, len(next_music)):
        await ctx.send(f'{i+1} - {next_music[i]}')

@bot.command()
async def add(ctx, *, name_music):
    global next_music
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
    }

    req = requests.get(f"https://www.youtube.com/results?search_query={name_music}", headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    n = re.search(r'"videoId":"(\w+)"', str(soup.find('body').find_all('script')[13].text)).group()[11:-1]
    next_music.append(f'https://www.youtube.com/watch?v={n}')
    await ctx.send('✅ Музыка успешно добавлена.')

@bot.command()
async def skip(ctx):
    global next_music

    if len(next_music) == 0:
        await ctx.send('❌ Сейчас в списке нет следующих компазиций.')

    else:
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send('❌ Сначала подключись к голосовому.')
        else:
            try:
                await ctx.voice_client.disconnect()
            except:
                pass
            await ctx.send('⏭')
            await ctx.message.author.voice.channel.connect(reconnect=True)
            video = next_music.pop(0)
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            print(voice)
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(video, download=False)
            URL = info['formats'][0]['url']
            try:
                os.chdir(r'ffmpeg\bin')
            except:
                pass
            voice.play(discord.player.FFmpegPCMAudio(executable=fr"{os.getcwd()}\ffmpeg.exe", source=URL,
                                          **FFMPEG_OPTIONS))
            voice.is_playing()
            await ctx.send(f"✅ Сейчас играет: {video}")

@bot.command()
async def play(ctx, *, name_song):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
    }

    req = requests.get(f"https://www.youtube.com/results?search_query={name_song}", headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    n = re.search(r'"videoId":"(\w+)"', str(soup.find('body').find_all('script')[13].text)).group()[11:-1]
    video = f'https://www.youtube.com/watch?v={n}'
    try:
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send('❌ Сначала подключись к голосовому.')

        else:
            await ctx.message.author.voice.channel.connect(reconnect=True)
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            print(voice)
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(video, download=False)
            URL = info['formats'][0]['url']
            try:
                os.chdir(r'ffmpeg\bin')
            except:
                pass
            voice.play(discord.player.FFmpegPCMAudio(executable=fr"{os.getcwd()}\ffmpeg.exe", source=URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            await ctx.send(f"✅ Сейчас играет: {video}")
    except discord.errors.ClientException:
        await ctx.send("❌ Музыка уже играет. Если хотите добавить в очередь, напишите - !add 'название музыки'")

@bot.command()
async def antimat(ctx):
    global flag, ban
    count = 0

    if flag == False and ctx.message.author.guild_permissions.administrator == True and count == 0:
        flag = True
        count += 1
        await ctx.send(f'Пользователь {ctx.message.author} ВКЛЮЧИЛ контроль за сквернословными. Теперь чат под строгим надзором!')

    if flag == True and ctx.message.author.guild_permissions.administrator == True and count == 0:
        flag = False
        ban = {}
        count += 1
        await ctx.send(f'Пользователь {ctx.message.author} ОТКЛЮЧИЛ контроль за сквернословными. Теперь в чатах можно материться.')

    if ctx.message.author.guild_permissions.administrator == False:
        await ctx.send('❌ У вас нет такого права.')

@bot.command()
async def menu(ctx):
    await ctx.send("☺ Привет! Я test-bot. Вот список моих команд:\n"
                   "> • !clear <число (необязательно)> -  отчистка всего чата или нескольких сообщений. ⚠ Только АДМИНИСТРАТОРАМ и МОДЕРАТОРАМ сервера!\n"
                   "> • !play <название музыки> - включает музыку с YouTube.\n"
                   "> • !antimat - ОТКЛЮЧАЕТ или ВКЛЮЧАЕТ контроль за нецензурные выражения. ⚠ Только АДМИНИСТРАТОРАМ сервера!\n"
                   "> • !pause - ставит музыку на паузу.\n"
                   "> • !resume - воспраизводит музыку с момента паузы.\n"
                   "> • !stop - останавливает музыку.\n"
                   "> • !add - добавить музыку в очередь.\n"
                   "> • !skip - пропустить текущую музыку.\n"
                   "> • !list - показывает список следующих копазиций.")

bot.run('Your token')