import discord

bot = discord.Client(intents=discord.Intents.all())

@bot.event
async def on_ready():
	print("Bot | Ready")

def getguild(guildid):
	return bot.get_guild(int(guildid))

def getuser(guildid, userid):
	guild = getguild(int(guildid))
	user = guild.get_member(int(userid))
	return user