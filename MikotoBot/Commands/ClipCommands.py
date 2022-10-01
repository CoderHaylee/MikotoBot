def ClipCommands(bot):
	class ClipCommands():
		def __init__(self, bot):
			self.bot = bot
			self.simpleCommands()
		def simpleCommands(self):
			clips = self.bot.otherVars["clips"]
			for clip in clips:
				clipCom = self.defineClipCom(clips[clip])
				self.bot.command(clip, func=clipCom, comType="Simple")
		def defineClipCom(self, command):
			async def clipCom(message):
				await bot.sendMessage(message, command)
			return clipCom
	return ClipCommands(bot)
