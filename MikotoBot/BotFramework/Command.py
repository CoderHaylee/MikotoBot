'''Copyright (C) 2020  Haylee

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>'''

import argparse
import asyncio
import datetime
import inspect
import shlex

class Command:
	def __init__(self, bot, comm, subCom=False, *, alias=None, **options):
		#Creates Command Object
		self.bot = bot
		self.comm = comm
		self.desc = options.get("desc", "")
		self.type = options.get("type", "Normal")
		self.alias = self.aliases = options.get("alias", options.get("aliases", []))
		self.listed = options.get("listed", True)
		self.help = options.get("help", "No Help Given")
		self.func = options.get("func")
		self.subcommands = {}
		if not subCom:
			bot.commands[comm] = self
			for a in self.alias:
				bot.commands[a] = self
	
	def subcommand(self, *args, **kwargs):
		#Creates SubCommands
		return SubCommand(self, *args, **kwargs)
	
	def __call__(self, func):
		#Makes it usable as Decorator
		self.func = func
		return self
	
	@asyncio.coroutine
	def run(self, message):
		#Gets List of words in message
		argList = message.text.split(" ")
		errorMess=None
		if len(self.subcommands) > 0:
			if len(argList) > 1:
				newArgList = argList[1:]
				if newArgList[0].lower() in self.subcommands:
					passedMessage = " ".join(newArgList)
					message.originalText = message.text
					message.text = passedMessage
					yield from self.subcommands[newArgList[0].lower()].run(message)
				else:
					errorMess = yield from self.func(message)
			else:
				errorMess = yield from self.func(message)
		else:
			errorMess = yield from self.func(message)
		if errorMess != None:
			yield from self.commandGroupHandle(message, invalidArg=errorMess[0],
				noArg=errorMess[1])
	
	#Command Handling
	async def commandGroupHandle(self, message, invalidArg="Unknown Argument {}.", noArg="Possible Args: {}"):
		#Sends message back if an invalid Argument was given
		if len(message.text.split()) > 1:
			arg = "`{}`".format(" ".join(message.text.split()[1:]))
			await self.bot.sendMessage(message, invalidArg.format(arg))
		#Sends Error back if no argument was given
		else:
			#combine to string
			coms = ("`{}`".format("`, `".join(list(self.subcommands.keys()))))
			await self.bot.sendMessage(message, noArg.format(coms))


class SubCommand(Command):
	#SubCommand Class
	def __init__(self, parent, comm, **options):
		self.parent = parent
		self.parent.subcommands[comm] = self
		self.alias = self.aliases = options.get("alias", options.get("aliases", []))
		for a in self.alias:
			self.parent.subcommands[a] = self
		super().__init__(parent.bot, comm, True, **options)




class ComArgParse(argparse.ArgumentParser):
	def __init__(self, bot, *args, **kwargs):
		self.bot = bot
		self.hasError=False
		self.errorMessage=""
		super().__init__(*args, **kwargs)
	#Overwritten functions
	def exit(self, status=0, message=None):
		return "Exiting Due to Error:\n{}".format(message)
	def error(self, message):
		self.hasError=True
		self.errorMessage = "{}\n{}".format(self.errorMessage, message)
		raise self.ParserError
	def _print_message(self, message, file=None):
		self.hasError=True
		self.errorMessage = "{}\n{}".format(message, self.errorMessage)
	
	#Custom Functions
	def splitMessage(self, message):
		try:
			com = shlex.split(message.text)[1:]
		except ValueError as e:
			self.hasError=True
			self.errorMessage = "Error: Quotations not closed"
			raise self.SplitterError
		return com
	def parseArgs(self, message):
		self.hasError=False
		self.errorMessage=""
		try:
			command = self.splitMessage(message)
		except self.SplitterError:
			return self.errorMessage			
		try:
			parsed = self.parse_args(command)
		except:
			parsed = "Unspecified Error has occured"
		if self.hasError:
			messageBack = self.errorMessage
		else:
			messageBack = parsed
		return messageBack
	
	class SplitterError(Exception):
		pass
	class ParserError(Exception):
		pass
