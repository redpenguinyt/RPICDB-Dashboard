import pymongo, os, json
from utils.botutils import bot
import utils.ytutils as yt

client = pymongo.MongoClient(os.environ['mongo_url'])
guildsdb = client.RPICDB.guilds

def getguild(guildid):
	guild = guildsdb.find_one({"_id":guildid})
	if not guild:
		addguild(guildid)
		return guildsdb.find_one({"_id":guildid})
	return guild

def addguild(guildid):
	os.system("rm config.json")
	os.system(f"wget {os.environ['cfglink']} >/dev/null 2>&1")
	config = json.load(open("config.json", encoding='utf-8'))
	
	newguild = config["defaultguild"]
	newguild["_id"] = guildid
	return guildsdb.insert_one(newguild)

def editguild(guildid, key, newvalue):
	getguild(guildid)
	guildsdb.find_one_and_update(
		{"_id":guildid},
		{"$set":{key: newvalue}}
	)

def guildexists(guildid):
	for item in bot.guilds:
		if item.id == guildid:
			return True
	return False

def postguild(guildid, formdata):
	# postresult = {}
	# for key in formdata:
	# 	postresult[key] = formdata[key]
	print(formdata)

	for key, value in formdata.items():
		if key == "channelid" and value != "":
			if not yt.getchannelbyid(value):
				continue
		if key == "isLevels" or key == "isWelcome":
			value = bool(value)
		editguild(guildid, key, value)
	
	if not "isLevels" in formdata:
		editguild(guildid, "isLevels", False)
	if not "isWelcome" in formdata:
		editguild(guildid, "isWelcome", False)
	
	return formdata