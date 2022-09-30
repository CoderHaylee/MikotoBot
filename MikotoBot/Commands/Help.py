def Help(bot):
	class Help():
		@bot.command("help", aliases=["halp", "commands"], help="Do you really need help for help?")
		async def help(message):
			split = message.text.split()
			blacklistTypes = ["OwnerAdmin","Music","Admin","Hidden"]
			fullCommandList = list(bot.commands.keys())
			comList = []
			adminComList = []
			simpleCommands = []
			for com in fullCommandList:
				if bot.commands[com].type == "Admin":
					adminComList.append("`{}`".format(com))
				elif bot.commands[com].type == "Simple":
					simpleCommands.append("`{}`".format(com))
				elif bot.commands[com].type not in blacklistTypes:
					comList.append("`{}`".format(com))
			commandList = ", ".join(comList)
			adminList = ", ".join(adminComList)
			simpleCommands = ", ".join(simpleCommands)
			if len(split) > 1:
				command = " ".join(split[1:]).lower()
			else:
				await bot.sendMessage(message, "The current commands are {}, "
					"{}. Some commands need extra to run properly, type "
					"`{}help [command]` for more information on how to use "
					"that command.".format(simpleCommands, commandList, bot.commandPrefix))
				return
			if command in simpleCommands:
				await bot.sendMessage(message, "{} is a \"Simple Command\" so "
					"there is nothing to it, just type it and go"
					".".format(command.capitalize()))
			else:
				try:
					await bot.sendMessage(message, bot.commands[command].help)
				except KeyError:
					await bot.sendMessage(message, "Sorry, there is no "
						"command {}.".format(command))
