

def AdminCommands(bot):
	class AdminCommands():
		@bot.command("restart", type="OwnerAdmin")
		@bot.ownerOnly
		async def restart(message):
			await bot.sendMessage(message, "Restarting...")
			try:
				bot.settings["game"] = bot.translator.getGame(bot.id, message)
				bot.settings["Settings"]["RestartChannel"] = {
					"ServerName": message.server.name,
					"ChannelName": message.channel.name,
					"ServerID": message.server.id,
					"ChannelID": message.channel.id}
				bot.settings["Settings"]["Restarted"] = True
				bot.changeSettings()
			except AttributeError:
				pass
			bot.botExit("Bot Restarting")
		@bot.command("reloadjson", type="OwnerAdmin")
		@bot.ownerOnly
		async def reloadjson(message):
			bot.otherVars = bot.otherVars["loadOtherVars"]()
			await bot.sendMessage(message, "Json Reloading done")
		@bot.command("listnicks", type="OwnerAdmin")
		@bot.ownerOnly
		async def listNicks(message):
			split = message.text.split()
			try:
				userID = split [1]
			except IndexError:
				await bot.sendMessage(message, "User ID Required")
			try:
				nickList = bot.otherVars["customNicks"][userID]
			except KeyError:
				await bot.sendMessage(message, "There are no Nicks for that ID.")
			nickNames = "\n".join(nickList)
			await bot.sendMessage(message, nickNames)
		
		@bot.command("addclip", type="OwnerAdmin")
		@bot.ownerOnly
		async def addClip(message):
			split = message.text.split()
			if len(split) > 1:
				command = split[1]
				command = command.lower()
			else:
				command = None
			if len(split) > 2:
				clip = " ".join(split[2:])
			else:
				clip = None
			if (command == None) or (clip == None):
				await bot.sendMessage(message, "What should the Command "
					"({}) and the Clip ({}) be?".format(command, clip))
			else:
				if command in list(bot.commands.keys()):
					await bot.sendMessage(message, "{} is already "
						"a command.".format(command))
					return
				else:
					newClip = bot.commandFileList["ClipCommands"].defineClipCom(clip)
					bot.command(command, func=newClip, comType="Simple")
					bot.otherVars["clips"][command] = clip
					bot.support.writeJson("Files/Clips.json", bot.otherVars["clips"])
					await bot.sendMessage(message, "Clip {} added.".format(command))
		
		
		@bot.command("change", type="OwnerAdmin")
		@bot.ownerOnly
		async def change(message):
			invalidArg="I can't change {}."
			noArg="I can change {}"
			return (invalidArg, noArg)
		@change.subcommand("nickname")
		@bot.ownerOnly
		@bot.platformOnly("discord")
		async def changeNickname(message):
			selfBot = bot.translator.getUser(bot.id, message)
			perms = selfBot.permissions_in(message.channel._discordChannel)
			if perms.change_nickname:
				split = message.text.split()
				if len(split) > 1:
					nick = " ".join(split[1:])
				else:
					await bot.sendMessage(message, "What should I change my "
						"nickname to?")
					return
				if nick == "none":
					try:
						await selfBot.edit(nick=None, reason="Command "
							"Edit to None by '{}'".format(
							message.author.name))
					except bot.translator.discord.errors.HTTPException as httpError:
						httpRespond = httpError.response
						await bot.sendMessage(message, "There was an "
							"HTTP {} ({}) error"
							".".format(httpRespond.status,
							httpRespond.reason))
					await bot.sendMessage(message, "My nickname is now "
						"nothing (showing username).")
				else:
					try:
						await selfBot.edit(nick=nick, reason="Command "
							"Edit to '{}' by '{}'".format(nick, 
							message.author.name))
					except bot.translator.discord.errors.HTTPException as httpError:
						httpRespond = httpError.response
						await bot.sendMessage(message, "There was an "
							"HTTP {} ({}) error"
							".".format(httpRespond.status,
							httpRespond.reason))
					await bot.sendMessage(message, "My nickname is now "
						"{}.".format(nick))
					
			else:
				await bot.sendMessage(message, "I'm not allowed to change "
					"my nickname.")

		@bot.command("background", type="OwnerAdmin")
		@bot.ownerOnly
		async def background(message):
			invalidArg="I can't background {}."
			noArg="I can background {}"
			return (invalidArg, noArg)
		@background.subcommand("game")
		@bot.ownerOnly
		async def addGame(message):
			split = message.text.split()
			if len(split) > 1:
				action = split[1]
			else:
				await bot.sendMessage(message, "I need to know what to do.")
				return
			if len(split) > 2:
				game = " ".join(split[2:])
			else:
				await bot.sendMessage(message, "I need to know what do mess wil")
				return
			if action == "add":
				if game not in bot.settings["Settings"]["BackgroundTasks"]["AutoGame"]["games"]:
					bot.settings["Settings"]["BackgroundTasks"]["AutoGame"]["games"].append(game)
					bot.changeSettings()
					await bot.sendMessage(message, "`{}` added to game list.".format(game))
					return
				else:
					await bot.sendMessage(message, "`{}` is already in the game "
						"list.".format(game))
					return
			elif action == "remove":
				if game in bot.settings["Settings"]["BackgroundTasks"]["AutoGame"]["games"]:
					bot.settings["Settings"]["BackgroundTasks"]["AutoGame"]["games"].remove(game)
					bot.changeSettings()
					await bot.sendMessage(message, "`{}` removed to game "
						"list.".format(game))
					return
				else:
					await bot.sendMessage(message, "`{}` is not in the game "
						"list.".format(game))
					return
			else:
				await bot.sendMessage(message, "IDK how to do `{}`.".format(action))
				return














