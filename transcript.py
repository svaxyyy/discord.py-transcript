import discord
from discord.ext import commands
import json
import asyncio
import chat_exporter
import io
from io import *







intents = discord.Intents.default()
intents.members = True




# json


def load():
    with open("database/json/bot_config.json", "r") as file:
        return json.load(file)


data = load()

client = commands.Bot(command_prefix=data["prefix"], intents=intents)
client.remove_command("help")




@client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))



@client.command()
async def save(ctx, limit: int):
    loading_embed = discord.Embed(color = 0xffffff)
    loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
    msg = await ctx.send(embed=loading_embed)
    transcript = await chat_exporter.export(ctx.channel, limit, "Europe/Berlin")

    if transcript is None:
        return

    transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html")
    await ctx.send(file=transcript_file)
    await msg.delete()


@client.command()
async def fastsave(ctx):
    loading_embed = discord.Embed(color = 0xffffff)
    loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
    msg = await ctx.send(embed=loading_embed)
    await chat_exporter.quick_export(ctx)
    await msg.delete()

@client.command()
async def purge(ctx, tz_info): # !purge berlin
    deleted_messages = await ctx.channel.purge()

    transcript = await chat_exporter.raw_export(ctx.channel, deleted_messages, tz_info)

    if transcript is None:
        return

    transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html")
    loading_embed = discord.Embed(color = 0xffffff)
    loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
    msg = await ctx.send(embed=loading_embed)
    await ctx.send(file=transcript_file)
    await msg.delete()



client.run(data["token"])