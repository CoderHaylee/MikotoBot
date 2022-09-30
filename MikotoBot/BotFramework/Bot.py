'''Copyright (C) 2020  Hayleethegamer

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

import asyncio
import os
import signal
import sys

from .Logging import Logging
from .Support import Support
from .APITranslation import APITranslator
from .Command import Command, ComArgParse
APIauthor, APIversion = "Haylee", "1.6"



#Default Settings
defaultSettings = {
	"Restart":{
		"Restarted":False,
		"RestartChannel":{}
	},
	"BackgroundTasks":{
		"AutoChange":{
			"status":False,
			"time":60
		},
		"AutoGame":{
			"games":[],
			"status":False,
			"game":"",
			"time":60
		}
	},
	"NonCommandsOff":[],
	"NSFW":[],
	"Status":{
		"Name":None,
		"Type":0,
		"URL": None
	}
}

#Coloring for logs	
			
class Bot():
	def __init__(self, commandPrefix, **options):
		self.commandPrefix = commandPrefix #Sets the Command Prefix 
		self.testing = options.get("testing", False) #Enables or disables the testing Mode
		#Sets owner ID(s), if none Given, set to blank Set
		self.ownerIDs = options.get("ownerIDs", set())
		#sets where the log files are, defaults to working Directory "Logs" folder
		self.logging = Logging(options.get("logLocation", "{}/Logs/".format(os.getcwd())))
		self.logging.sysLog("Debug", "Bot Starting........")
		self.loop = asyncio.get_event_loop() #Sets up Event Loop
		self._ready = asyncio.Event() #defines Ready, will be set to True when Ready
		self._running = False
		#self.loop.create_task(self.CTRLCCheck())
		self.loop.add_signal_handler(signal.SIGINT, lambda: self.signalHandler())
		#self.loop.add_signal_handler(signal.SIGTERM, lambda: self.signalHandler())signalHandler
		self.settingsFile = options.get("settings")
		self.settings = self._loadSettings() #Loads Settings
		#Allows user to load Custom Global Variables of any kind
		self.otherVars = options.get("otherVars")
		#A Link the bot will automatically send if errors in commands occure
		self.bugReport = options.get("bugReport")
		#Sets the listed of Trusted role ID numbers, blank list if none provided
		self.trustedIDs = options.get("TrustedIDs", [])
		#Sets the blank command List for further use
		self.commands = {}
		#Com Arg Parser
		self.comArgParse = ComArgParse
		
		
		self.name = None #Bot's own Discord Username
		self.id = None #The Bot's own Discord ID Number, set later by API Translator
		self.botVersion = options.get("version", "1.0") #Bot Version
		self.botMaker = options.get("maker", "Not Provided") #Bot Version
		self.APIVersion = APIversion #API Version
		self.APIMaker = APIauthor #API Maker
		self.pythonVersion = "{}.{}.{}".format(sys.version_info[0], 
			sys.version_info[1],sys.version_info[2]) #Python Version
		
		#Sets up Translator
		self.platform = options.get("platform", None)
		self.translator = APITranslator(self, self.testing, self.platform)
		self.support = Support()
		
		
	def _loadSettings(self):
		#If no settings file given, load Defaults
		if self.settingsFile == None:
			settings = defaultSettings
			self.logging.sysLog("Debug", "Default Settings Loaded")
		else:
			#Try to load Settings file given, if failed, exit.
			try:
				settings = Support.loadJson(self, self.settingsFile)
				self.logging.sysLog("Debug", "Settings Loaded")
			except FileNotFoundError:
				self.logging.sysLog("Error", "Settings not "
					"found, Exiting.")
				self._stop()
			except ValueError:
				self.logging.sysLog("Error", "Settings file "
					"corrupted, Exiting.")
				self._stop()
		return settings
		
	def changeSettings(self):
		Support.writeJson(self, self.settingsFile, self.settings)
			
	
	#Stops the bot gracefully
	def _stop(self):
		self.logging.sysLog("Status", "Clearing Ready")
		self._ready.clear()
		for task in asyncio.Task.all_tasks():
        		task.cancel()
		asyncio.create_task(self.extraStop())
		asyncio.create_task(self.translator.discordStop())
		self.logging.sysLog("Status", "Clean up done, Closing")
		
	def signalHandler(self):
		self.logging.sysLog("Status", "Stop Signal Recieved, stopping....")
		self._stop()
	
	#Custom Exit Exception for closing bot	
	def botExit(self, message=None):
		if message == None:
			message="BotExit was called."
		self.logging.sysLog("Status", message)
		self._stop()
		#raise self.BotExit
	
	#Starts Running the bot and handles a KeyboardInterrupt
	def run(self, token):
		self._start(token)
	#Starts running the bot
	def _start(self, token):
		self.logging.sysLog("Status", "Starting...")
		self.translator.run(token)
		
	
	
	#Default Events
	@asyncio.coroutine
	def extraStop(self):
		#For Extra things that need handled when closing
		pass
	@asyncio.coroutine
	def bot_ready(self):
		if not self._running:
			#When Ready to use
			self._running = True
			self.logging.sysLog("Status", "Connected!")
			self.logging.sysLog("Status", "API Version: {} ".format(self.APIVersion))
			self.logging.sysLog("Status", "Username: {}".format(self.name))
			self.logging.sysLog("Status", "ID: {}".format(self.id))
			self.logging.sysLog("Status", "Discord.py "
				"Version: {}".format(self.translator.version))
			self.logging.sysLog("Status", "Python Version: {}".format(self.pythonVersion))
			self.logging.sysLog("Status", "Process ID: {}".format(str(os.getpid())))
			self.logging.sysLog("Status", "Ready to go!")
			self._ready.set()
			yield from self.on_ready()
		else:
			self.logging.sysLog("Status", "Reconnected/Random Re-Ready")
			yield from self.on_reconnect()
	@asyncio.coroutine
	def on_ready(self):
		#For other On Ready
		pass
	async def on_reconnect(self):
		#Reconnect event
		pass
	@asyncio.coroutine
	def on_message(self, message):
		#Chat Messages
		self.logging.messageLog(message)
		yield from self.otherCommands(message)
		yield from self.process_commands(message)
	@asyncio.coroutine
	def on_error(self,error):
		#Here but not in
		print("Ignoring exception {}".format(error))
		print(traceback.format_exc())
		yield from self._errorHandleing()
	@asyncio.coroutine
	def otherCommands(self, message):
		#A place holder for other commands that might not work with the command framework.
		pass
	@asyncio.coroutine
	def process_commands(self, message):
		#Processes command
		#If Message not from Self
		if message.author.id != self.id:
			#If Message is command.
			if message.text.startswith(self.commandPrefix):
				#Gets command's name
				commandName = message.text[len(self.commandPrefix):]
				comSplit = commandName.split(" ")
				comName = comSplit.pop(0).lower().replace("\r","")
				if comName in self.commands:
					yield from self.commands[comName].run(message)
	
	def command(self, *args, **kwargs):
		#Returns command Class
		return Command(self, *args, **kwargs)
	
	
	async def sendMessage(self, message, sentMessage):
		charLimit = 2000
		messageLimit = 3 #roughly 6000 Char Limit
		if len(sentMessage) > charLimit:
			#Split message by new line, put into groups that are under 2000 Characters
			messSplit = sentMessage.split("\n")
			messageParts = []
			messPartCount = 0
			messPart = []
			for m in messSplit:
				mCount = len(m)+1
				if messPartCount + mCount < charLimit:
					messPart.append(m)
					messPartCount += mCount
				elif messPartCount + mCount >= charLimit:
					messageParts.append(messPart)
					messPart = [m]
					messPartCount = mCount
				else:
					await self.translator.sendMessage(message.channel.id, "There was "
						"an Error Sending Message, Message Too Long Perhaps.")
			messageParts.append(messPart)
			if len(messageParts) <= messageLimit: 
				for m in messageParts:
					messF = "\n".join(m)
					print(messF)
					if len(messF) <= charLimit:
						await self.translator.sendMessage(message.channel.id, messF)
					else:
						await self.translator.sendMessage(message.channel.id, 
							"Output is over {} Characters.".format(charLimit))
			else:
				limit = charLimit * messageLimit
				await self.translator.sendMessage(message.channel.id, "Output is over "
				"{} Characters total, {} per message".format(limit, charLimit))
			
		else:
			await self.translator.sendMessage(message.channel.id, sentMessage)
	
	#Ready Helpers
	async def waitForReady(self):
		await self.translator.waitUntilReady()
		await self._ready.wait()
	
	def ready(self):
		return self._ready.is_set()
		
		
	
	#Restrictions
	#Only Mods (people with Manage Message permissions for the channel) can use these commands
	def modOnly(self, func):
		#Manage Message = mod
		async def __decorator(message):
			if self.translator.modCheck(message):
				return await func(message)
			else:
				return await self.permissionError(message)
			
	def adminOnly(self, func):
		#Manage Message = mod
		async def __decorator(message):
			if self.translator.adminCheck(message):
				#print("admin")
				#print(func)
				return await func(message)
			else:
				return await self.permissionError(message)
	#Only the Bot's owner can use commands with this restriction
	def ownerOnly(self, func):
		async def __decorator(message):
			if str(message.author.id) in self.ownerIDs:
				#print("Owner")
				#print(func)
				return await func(message)
			else:
				return await self.permissionError(message)
		return __decorator
	#Only Trusted People can use these commands
	def trustedOnly(self, func):
		async def __decorator(message):
			if self.trustedID in message.author.roles:
				return await func(message)
			else:
				return await self.permissionError(message)
		return __decorator
	#NSFW Check
	def nsfwCheck(self, func):
		async def __decorator(message):
			if str(message.channel.id) in self.settings["NSFW"]:
				return await func(message)
			else:
				await self.sendMessage(message, 
					"NSFW is disabled in this channel.")
		return __decorator
	#A Function to check if NSFW is allowed mid function rather than as a dectorator
	def nsfwMidCheck(self, message):
		if message.channel.id in self.settings["NSFW"]:
			return True
		else:
			return False
	#Commands can only be used on given platform
	def platformOnly(self, platform):
		def __platformOnly(func):
			async def __decorator(message):
				if platform.lower() == self.translator.platform:
					#print("platform")
					#print(func)
					return await func(message)
				else:
					await self.platformError(message)
			return __decorator
		return __platformOnly
	#Commands can not1 be used on given platform
	def platformExclude(self, platform):
		def __platformExclude(func):
			async def __decorator(message):
				if platform.lower() != self.translator.platform:
					return await func(message)
				else:
					await self.platformError(message)
			return __decorator
		return __platformExclude
	#Platform Error
	async def platformError(self, message):
		await self.sendMessage(message, "This command is not allowed to be used "
			"on this platform.")
	async def permissionError(self, message):
		await self.sendMessage(message, "You do not have permission to use this command.")
	
