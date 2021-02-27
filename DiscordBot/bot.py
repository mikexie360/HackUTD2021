import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    printf(f'{member} has joined the server.')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms. ')

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = [
        'Yes',
        'Maybe',
        'No'
    ]
    await ctx.send(f'Question: {question} \nAnswer: {random.choice(responses)}')

client.run('Token')


