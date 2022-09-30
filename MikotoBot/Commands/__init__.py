from .Help import Help
from .Admin import AdminCommands
from .Commands import Commands
from .ClipCommands import ClipCommands

def commands(bot):
	bot.commandFileList = {
			"Help":Help(bot),
			"AdminCommands":AdminCommands(bot),
			"Commands":Commands(bot),
			"ClipCommands":ClipCommands(bot)
		}
