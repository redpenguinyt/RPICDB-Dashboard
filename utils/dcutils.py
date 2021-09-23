from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from quart import Quart, redirect, url_for, request
from utils.botutils import bot
import os

app = Quart("RPICDB Dashboard")
#app.secret_key=bytes(os.environ["session"],"utf-8")

app.secret_key = os.environ.get("session")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = os.environ["CLIENT_ID"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["CLIENT_SECRET"]
app.config["DISCORD_REDIRECT_URI"] = os.environ["URI"]
app.config["DISCORD_BOT_TOKEN"] = os.environ["discord-token"]

discordauth = DiscordOAuth2Session(app)

@app.route("/login/")
async def login():
	return await discordauth.create_session(scope=["identify", "guilds"])

@app.route("/logout/")
async def logout():
  discordauth.revoke()
  return redirect(url_for(".home"))

@app.route("/me/")
@requires_authorization
async def me():
	return redirect(url_for(".home"))

@app.route("/callback/")
async def callback():
	await discordauth.callback()
	try:
		return redirect(bot.url)
	except:
		return redirect(url_for(".me"))

@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
	bot.url = request.url
	return redirect(url_for(".login"))

async def getguildbyid(guildid):
	guilds = await discordauth.fetch_guilds()
	for guild in guilds:
		if guild.id == guildid:
			return guild
	return
	