import pyyoutube, os

api = pyyoutube.Api(
	api_key=os.environ['yt_api_key']
)

def getchannelbyid(id):
	try:
		return api.get_channel_info(channel_id=id).items[0]
	except:
		return None