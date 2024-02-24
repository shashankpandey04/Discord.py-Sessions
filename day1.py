import discord
from discord.ext import commands
import requests
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents)

cat_Api = 'https://api.thecatapi.com/v1/images/search'
dog_api = 'https://api.thedogapi.com/v1/images/search'

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user}')
  await bot.tree.sync()

@bot.event
async def on_guild_join(guild):
  valid_guild_id = 1152949579407442050
  if guild.id != valid_guild_id:
    print(f"Leaving guild {guild.name} ({guild.id}) because it's not the valid guild.")
    await guild.leave()

@bot.command()
async def car(ctx):
  '''Random Cat Image'''
  api_response = requests.get(cat_Api)
  data = api_response.json()
  print(data)
  image_url = data[0]['url']
  embed = discord.Embed(title="Car Image", color=discord.Color.blue())
  embed.set_image(url=image_url)
  await ctx.send(embed=embed)

@bot.command()
async def doge(ctx):
  '''Random Doge Image'''
  api_response = requests.get(cat_Api)
  data = api_response.json()
  print(data)
  image_url = data[0]['url']
  embed = discord.Embed(title="Doge Image", color=discord.Color.blue())
  embed.set_image(url=image_url)
  await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, username):
  api_url = "https://users.roblox.com/v1/usernames/users"
  payload = {"usernames": [username], "excludeBannedUsers": True}
  response = requests.post(api_url, json=payload)
  if response.status_code == 200:
    data = response.json()["data"][0]
    embed = discord.Embed(title="User Info", color=0x00ff00)
    embed.add_field(name="Username",value=data["requestedUsername"],inline=False)
    embed.add_field(name="Display Name",value=data["displayName"],inline=False)
    embed.add_field(name="Verified Badge",value=data["hasVerifiedBadge"],inline=False)
    embed.add_field(name="User ID", value=data["id"], inline=False)
    await ctx.send(embed=embed)
  else:
    await ctx.send("Error fetching user info.")

@bot.command()
async def searchby_userid(ctx, user_id):
  api_url = f"https://users.roblox.com/v1/users/{user_id}"
  response = requests.get(api_url)
  if response.status_code == 200:
    data = response.json()
    embed = discord.Embed(title="User Info", color=0x00ff00)
    embed.add_field(name="User ID", value=data["id"], inline=False)
    embed.add_field(name="Username", value=data["name"], inline=False)
    embed.add_field(name="Display Name",value=data["displayName"],inline=False)
    embed.add_field(name="Description",value=data["description"],inline=False)
    embed.add_field(name="Is Banned", value=data["isBanned"], inline=False)
    embed.add_field(name="Has Verified Badge",value=data["hasVerifiedBadge"],inline=False)
    embed.add_field(name="Created", value=data["created"], inline=False)
    await ctx.send(embed=embed)
  else:
    await ctx.send("Error 404 ")

@bot.command()
async def avatar(ctx, user_id):
  api_url = f"https://www.roblox.com/avatar-thumbnails?params=[{{userId:{user_id}}}]"
  response = requests.get(api_url)
  if response.status_code == 200:
    try:
      data = response.json()[0]
      thumbnail_url = data["thumbnailUrl"]
      embed = discord.Embed(title="Avatar", color=0xFF00FF)
      embed.set_image(url=thumbnail_url)
      await ctx.send(embed=embed)
    except Exception as e:
      await ctx.send(f"Error parsing response: {e}")
  else:
    await ctx.send(f"Error fetching avatar: HTTP status code {response.status_code}")
    
bot.run("TOKEN")
