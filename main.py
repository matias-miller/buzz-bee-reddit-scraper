import os
import discord
from discord.ext import commands, tasks
import praw
import random
import asyncio
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

SUBREDDIT_NAME = "r/OMSCS"
POST_CHANNEL_ID = 123456789012345678  # Current Placeholder

@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    scheduled_post.start()

def get_trending_post():
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    posts = [post for post in subreddit.hot(limit=20) if not post.stickied]
    return random.choice(posts) if posts else None

# Scheduled posting task
@tasks.loop(hours=24)
async def scheduled_post():
    channel = bot.get_channel(POST_CHANNEL_ID)
    post = get_trending_post()
    if channel and post:
        await channel.send(f"Trending Reddit Post: [{post.title}]({post.url}) - 👍 {post.score}")

# Command to fetch a post on demand
@bot.command(name='trending')
async def trending(ctx):
    post = get_trending_post()
    if post:
        await ctx.send(f"Trending Reddit Post: [{post.title}]({post.url}) - 👍 {post.score}")
    else:
        await ctx.send("Couldn't fetch any trending posts!")

@bot.command(name='about')
async def about(ctx): # TODO
    pass

bot.run(DISCORD_TOKEN)