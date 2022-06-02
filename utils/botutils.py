import discord

intents = discord.Intents.default()
intents.members = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user.name}")

def getguild(guildid):
	return bot.get_guild(int(guildid))

def getuser(guildid, userid):
	guild = getguild(int(guildid))
	user = guild.get_member(int(userid))
	return user