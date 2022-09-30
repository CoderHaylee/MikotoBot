import os
import json

import BotFramework
import BackgroundTasks as BackgroundTasks
import Commands
import Settings

Support = BotFramework.Support()

class MikotoBot:
	def __init__(self, testing=False, platform=None, dev=False):
		if platform == None:
			platform = "discord"
		self.bot = BotFramework.Bot(commandPrefix="%", settings="Settings.json", 
			testing=testing, maker="Haylee", version="1.0", 
			ownerIDs=["167744970952933376"], platform=platform)
		self.bot.otherVars = self.loadOtherVars()
		self.bot.on_ready = self.on_ready
		self.bot.on_reconnect = self.on_reconnect
		self.bot.extraStop = self.extraStop
		self.bot.loop.create_task(self.backgroundTasks())
		self.commandList = Commands.commands(self.bot)
		self._runBot(dev)
		
	async def backgroundTasks(self):
		await self.bot.waitForReady()
		print("Background Connected...")
		self.background = BackgroundTasks.BackgroundTasks(self.bot)
		print("Background Starting...")
		self.background.master()
	
	async def on_ready(self):
		if self.bot.settings["Settings"]["Restarted"]:
			restarting = self.bot.settings["Settings"]["RestartChannel"]
			restartedObject = RestartObject(restarting["ServerName"], 
				restarting["ChannelName"], restarting["ServerID"], 
				restarting["ChannelID"])
			await self.bot.sendMessage(restartedObject, "Done Restarting.")
			self.bot.settings["Settings"]["Restarted"] = False
			self.bot.settings["Settings"]["RestartChannel"] = {}
			self.bot.changeSettings()
		if self.bot.settings["game"] != None:
			await self.bot.translator.changeStartGame()
	async def on_reconnect(self):
		if self.bot.settings["game"] != None:
			await self.bot.translator.changeStartGame()
	async def extraStop(self):
		await self.bot.Anime.session.close()
	
	def _runBot(self, dev=False):
		#Starts Running the bot
		if dev:
			self.bot.run(Settings.devToken)
		else:
			self.bot.run(Settings.token)
	
	def loadOtherVars(self):
		customNicks = Support.loadJson("Files/CustomNicks.json")
		clips = Support.loadJson("Files/Clips.json")
		multiClips = Support.loadJson("Files/MultiClips.json")
		loadedJson = {
				"customNicks":customNicks,
				"clips": clips,
				"multiClip": multiClips,
				"loadOtherVars":self.loadOtherVars
			}
		return loadedJson

class RestartObject():
	def __init__(self, serverName, channelName, serverID, channelID):
		#Fake Message object
		self.channel = self.DummyChannel(channelName, channelID)
		self.server = self.DummyServer(serverName, serverID)
	class DummyChannel():
		def __init__(self, channelName, channelID):
			self.name = channelName
			self.id = channelID
	class DummyServer():
		def __init__(self, serverName, serverID):
			self.name = serverName
			self.id = serverID
	
