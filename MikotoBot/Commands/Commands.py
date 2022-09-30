import random


def Commands(bot):
	class Commands():
		comHelp="A Simple command to check if the bot can receive and reply to requests."
		@bot.command("test", help=comHelp)
		async def test(message):
			await bot.sendMessage(message, "Is this an Anime Test?")
		
		comHelp="Bye Bye"
		@bot.command("byebye", help=comHelp)
		async def bye(message):
			choosen = random.choice(bot.otherVars["multiClip"]["byebye"])
			await bot.sendMessage(message, choosen)
		comHelp="Night Night"
		@bot.command("night", aliases=["oyasumi"],help=comHelp)
		async def night(message):
			choosen = random.choice(bot.otherVars["multiClip"]["night"])
			await bot.sendMessage(message, choosen)
		comHelp="Morning"
		@bot.command("morning", aliases=["ohayo"], help=comHelp)
		async def night(message):
			choosen = random.choice(bot.otherVars["multiClip"]["morning"])
			await bot.sendMessage(message, choosen)
		
		
		
