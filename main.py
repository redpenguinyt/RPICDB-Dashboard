from utils.dcutils import app, discordauth
from quart import redirect, render_template, request, url_for
from utils.botutils import bot, getguild, getuser
import utils.dbutils as db
from utils.ytutils import getchannelbyid 
import os

# Dashboard

@app.route("/")
async def home():
	logged = ""
	name = ""
	
	existingguilds = []
	newguilds = []

	if await discordauth.authorized:
		logged = True

		user = await discordauth.fetch_user()
		name = user.name

		alluserguilds = await discordauth.fetch_guilds()
		alloweduserguilds = []
		for guild in alluserguilds:
			if guild.permissions.manage_guild:
				alloweduserguilds.append(guild)
		
		for guild in alloweduserguilds:
			if db.guildexists(guild.id):
				existingguilds.append(guild)
			else:
				newguilds.append(guild)

	return await render_template(
		"index.html",
		logged=logged,
		name = name,
		existingguilds = existingguilds,
		newguilds = newguilds
	)

@app.route("/manage/<guildid>/", methods = ["POST"])
async def managepost(guildid):
	db.postguild(int(guildid), await request.form)
	return redirect(url_for('manage',guildid=guildid))

@app.route("/manage/<guildid>/", methods = ['GET'])
async def manage(guildid):
	guildid = int(guildid)
	logged = ""
	allowed = ""

	guild = {}
	channelid = ""
	channelname = "[No channel connected]"
	guildname = ""
	
	if await discordauth.authorized:
		logged = True

		guild = db.getguild(guildid)

		users = guild["users"]
		for key, value in users.items():
			user = getuser(int(guildid), int(key))
			if user:
				users[key]["name"] = user.display_name

		guildname = getguild(guildid).name

		channelid = guild["channelid"]
		if channelid:
			channel = getchannelbyid(channelid)
			if channel:
				channelname = f"({channel.snippet.title})"

		guild.pop("channelid")
		guild.pop("users")
		guild.pop("premium")
		guild.pop("_id")

		# Make sure the user is allowed to edit this guild
		guilds = await discordauth.fetch_guilds()
		for userguild in guilds:
			if userguild.id == guildid:
				if userguild.permissions.manage_guild:
					allowed = True
		
	return await render_template(
		"manage.html",
		logged = logged,
		allowed = allowed,
		guildname = guildname,
		channelid = channelid,
		channelname = channelname,
		guild = guild,
		guildid = guildid,
		users = users
	)

# Redirects

@app.route("/invite")
def invite():
	return redirect("https://rpicdb.redpenguin.repl.co/invite")

@app.route("/support")
def support():
	return redirect("https://rpicdb.redpenguin.repl.co/support")

# Run app

bot.loop.create_task(app.run_task('0.0.0.0', port=8080, use_reloader=False, debug=True))
bot.run(os.environ["discord-token"],reconnect=True)