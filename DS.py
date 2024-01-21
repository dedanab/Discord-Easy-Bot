#Hello Alonze <3
import discord
import datetime
from discord.ext import commands
from datetime import datetime
from pytz import timezone
from discord.ext import commands
import asyncio
import random
from discord.utils import get
import os
import langdetect
from bs4 import BeautifulSoup
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
#------------------------------------------------
intents = discord.Intents().all()
client = commands.Bot(command_prefix='/', intents=intents)
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
intents = discord.Intents.default()
intents.members = True
#------------------------------------------------

@client.command()
async def radio(ctx, folder):
    folder = folder.lower()
    if folder == 'album1':
        folder_path = 'music/album1'
    elif folder == 'album2':
        folder_path = 'music/album2'
    elif folder == 'album3':
        folder_path = 'music/album3'
    elif folder == 'album3':
        folder_path = 'music/album3'
    elif folder == 'album4':
        folder_path = 'music/album4'
    elif folder == 'album5':
        folder_path = 'music/album5'
    elif folder == 'album6':
        folder_path = 'music/album6'
    else:
        await ctx.send("Неправильное название альбома😞")
        return
    
    await ctx.send(f'Включаю радио **"{folder}"**  💎 ')
    if not ctx.message.author.voice:
        await ctx.send("Вы не подключены к голосовому каналу😟")
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await asyncio.sleep(1)
        while True:
            for file in os.listdir(folder_path):
                if file.endswith(".mp3"):
                    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
                    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"{folder_path}/{file}"))
                    voice.play(source)
                    song_name = file[:-4] # удаляем ".mp3" из названия песни
                    await ctx.send(f'Играет песня: {song_name}')
                    while voice.is_playing():
                        await asyncio.sleep(1)

@client.command()
async def off(ctx):
    await ctx.send(f'Радио выключено  :( ')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    await voice.disconnect()

@client.command()
async def next(ctx):
    await ctx.send(f'Следующая песня включена! Если у вас есть предложения по музыке, то пишите <@794874868180058122>  ;) ')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    await asyncio.sleep(1)


@client.command()
async def clear(ctx, count: int):
    if count > 500:
        await ctx.send(f'{ctx.author.mention} максимальное количество сообщений за раз - 500')
        return
    if not any(role.id == 1078663068042674207 for role in ctx.author.roles):
        await ctx.send(f'{ctx.author.mention} у вас нет нужной роли для этого!')
        return
    deleted_messages = await ctx.channel.purge(limit=count)
    await ctx.send(f'**Удалено** {len(deleted_messages)} **сообщения(ий)**')







@client.command()

@commands.has_role(1078663068042674207)
async def mute(ctx, member: discord.Member = None, duration: int = None, reason: str = None):
    if member is None:
        await ctx.send("Укажите пользователя, которому нужно выдать мут: /mute @пользователь")
        return
    
    await ctx.send(f"Установите время мута для пользователя {member.mention} (в минутах):")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        msg = await client.wait_for('message', check=check, timeout=30)
        duration = int(msg.content)
        with open('mute.txt', 'a') as file:
            file.write(f"{member.id} {duration}\n")
    except asyncio.TimeoutError:
        await ctx.send("Время ввода истекло.")
        return
    except ValueError:
        await ctx.send("Некорректный ввод времени.")
        return
    
    role = discord.utils.get(ctx.guild.roles, name="Muted") # получаем роль "Muted"
    if role is None: # если такой роли нет, создаем ее
        try:
            role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels: # запрещаем писать в каналах
                await channel.set_permissions(role, send_messages=False)
        except discord.Forbidden:
            await ctx.send("У меня нет прав для создания роли.")
            return
    
    if role in member.roles:
        await ctx.send("Этот пользователь уже замучен.")
        return
    
    try:
        await member.add_roles(role)
        await ctx.send(f"Пользователь {member.mention} замучен на {duration} минут.")
        await asyncio.sleep(duration * 60) # ждем указанное время
        await member.remove_roles(role) # снимаем мут
    except discord.Forbidden:
        await ctx.send("У меня нет прав для выдачи мута.")

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == 1110820770285899838:  # если член зашел в голосовой канал
        new_channel = await member.guild.create_voice_channel(f'{member.display_name} \ голосовой',
                                                               category=after.channel.category)
        await member.move_to(new_channel)
        await new_channel.set_permissions(member, manage_channels=True, manage_roles=True, connect=True, mute_members=True,
                                           deafen_members=True, move_members=True, view_channel=True)
    if before.channel and before.channel.name.endswith('голосовой') and not before.channel.members:  # если все покинули канал
        await before.channel.delete()


@client.command()
async def givekroll(ctx):
    role = ctx.guild.get_role(1078663879640481852)
    members = ctx.guild.members
    for member in members:
        await member.add_roles(role)
    await ctx.send('Роли выданы!')

@client.event
async def on_member_join(member):
    channel = client.get_channel(1078666324244431029)
    message = f"@{member.name}, Добро Пожаловать к нам!\nhttps://images-ext-2.discordapp.net/external/u7lkBh37fMhGAwPdOpF8TRNzitrwuIXJhtYfiGY7J1E/https/media.tenor.com/g9I23ev4eGgAAAPo/emmy-amy-poehler.mp4"
    await channel.send(message)

@client.event
async def on_member_join(member):
    channel = client.get_channel(1078666324244431029)
    await channel.send(f'{member.mention}, Добро пожаловать к нам!')
    with open('hi.gif', 'rb') as gif:
        await channel.send(file=discord.File(gif))

ROLE_ID = 1078663879640481852

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=ROLE_ID)
    await member.add_roles(role)




# Объявляем событие готовности клиента
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    # Устанавливаем активность стриминга для бота
    stream = discord.Streaming(name="Скер", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    await client.change_presence(status=discord.Status.online, activity=stream)




client.run(token='')     
