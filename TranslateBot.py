from googletrans import Translator
import discord
import os
import json
import asyncio

def Trans(string, lang='en'):
	translator = Translator()
	a = translator.translate([string], dest=lang)
	for att in a:
		if att.src != 'en':
			return str(att.src), str(att.text)
		else:
			return False, False


TOKEN = "" # Your discord bot token here
botTitle = "Translate Bot"
translateToggle = False
client = discord.Client()

#####################################
#                                   #
#  ON MESSAGE COMMANDS STARTS HERE  #
#                                   #
#####################################
@client.event
async def on_message(message):
	global botTitle
	global translateToggle

	####################
	#                  #
	#  CORE FUNCTIONS  #
	#                  #
	####################
	#################################
	#  get servers start parameter  #
	#################################
	def getParam(serverid):
		with open('./servers/'+serverid+'/config.json') as file:
			config = json.load(file)
		file.close()
		param = config['server_info'][0]['start_param']
		return param

	# Don't want our bot talking to itself
	if message.author == client.user:
		return

	# Toggle Translation ON/OFF
	elif message.content.lower().startswith(getParam(message.server.id)+"toggle"):
		if translateToggle:
			translateToggle = False
		else:
			translateToggle = True
		await client.send_message(message.channel, "Translation is set to: " + str(translateToggle))

	# 
	elif translateToggle:
		SRC, MSG = Trans(message.content, 'en')
		if MSG != False:
			embed = discord.Embed(title='Translation', type='rich', color=0xff0000, description=str(message.author) + ' is speaking ' + SRC.upper())
			embed.add_field(name="Original Message", value=message.content)
			embed.add_field(name="English message", value=MSG, inline=False)
			await client.send_message(message.channel, embed=embed)

########################
#                      #
#  ON CLIENT START-UP  #
#                      #
########################
@client.event
async def on_ready():
	print('''##############
#  Bot Info  #
##############''')
	print('Logged in as ' + client.user.name + ":" + client.user.id)
	print('''\n################################
#  Connected Servers | Owners  #
################################''')
	servers = list(client.servers)
	numServers = len(client.servers)
	print("Connected on "+ str(numServers)+ " server(s): ")
	for x in range(len(servers)):
		serverName = str(servers[x-1].name)
		serverOwner = str(servers[x-1].owner)
		serverOwnerID = str(servers[x-1].owner.id)
		serverID = str(servers[x-1].id)

		#####################################
		#  Check for Server Configurations  #
		#####################################
		if not (os.path.exists('./servers/'+serverID)):
			# Create server directory
			os.makedirs('./servers/'+serverID)
			with open('./servers/'+serverID+'/config.json','w') as file:
				file.close()
			# Create default config JSON
			serversDict = {}
			serversDict['server_info'] = []
			servs = serversDict['server_info']
			server = {
			'server_id':serverID,'server_name':serverName,'server_owner':serverOwner,'server_owner_id':serverOwnerID,
			'start_param':'+'
			}
			servs.append(server)
			with open('./servers/'+serverID+'/config.json',"w") as file:
				json.dump(serversDict, file, indent=4, sort_keys=True)
			file.close()
		# Print currently connected servers
		print("\tServername: " + serverName + " : " + serverID + " | Owner: " + serverOwner)
	print("\n")

###########################
#                         #
#  ON CLIENT SERVER JOIN  #
#                         #
###########################
@client.event
async def on_server_join(server):
	try:
		os.system("clear")
	except:
		os.system("clear")
	print('''##############
#  Bot Info  #
##############''')
	print('Logged in as ' + client.user.name + ":" + client.user.id)
	print('''\n################################
#  Connected Servers | Owners  #
################################''')
	servers = list(client.servers)
	numServers = len(client.servers)
	print("Connected on "+ str(numServers)+ " server(s): ")
	for x in range(len(servers)):
		serverName = str(servers[x-1].name)
		serverOwner = str(servers[x-1].owner)
		serverOwnerID = str(servers[x-1].owner.id)
		serverID = str(servers[x-1].id)

		###############################################
		#  Ensure new server is configured correctly  #
		###############################################
		if not (os.path.exists('./servers/'+serverID)):
			# Create server directory
			os.makedirs('./servers/'+serverID)
			with open('./servers/'+serverID+'/config.json','w') as file:
				file.close()
			# Create default config JSON
			serversDict = {}
			serversDict['server_info'] = []
			servs = serversDict['server_info']
			server = {
			'server_id':serverID,'server_name':serverName,'server_owner':serverOwner,'server_owner_id':serverOwnerID,
			'start_param':'+'
			}
			servs.append(server)
			with open('./servers/'+serverID+'/config.json',"w") as file:
				json.dump(serversDict, file, indent=4, sort_keys=True)
			file.close()
		# Print Currently connected Servers
		print("\tServername: " + serverName + " : " + serverID + " | Owner: " + serverOwner)

	print("\n")

#############################
#                           #
#  ON CLIENT SERVER REMOVE  #
#                           #
#############################
@client.event
async def on_server_remove(server):
	# Remove Server files
	serverID = str(server.id)
	shutil.rmtree('./servers/'+serverID)
	# Continue on
	try:
		os.system("clear")
	except:
		os.system("clear")
	print('Logged in as ' + client.user.name + ":" + client.user.id)
	print('--------')
	print('''##############
#  Bot Info  #
##############''')
	print('Logged in as ' + client.user.name + ":" + client.user.id)
	print('''\n################################
#  Connected Servers | Owners  #
################################''')
	servers = list(client.servers)
	numServers = len(client.servers)
	print("Connected on "+ str(numServers)+ " server(s): ")
	for x in range(len(servers)):
		serverName = str(servers[x-1].name)
		serverOwner = str(servers[x-1].owner)
		serverOwnerID = str(servers[x-1].owner.id)
		serverID = str(servers[x-1].id)
		print("\tServername: " + serverName + " : " + serverID + " | Owner: " + serverOwner)
	print("\n")

client.run(TOKEN)
