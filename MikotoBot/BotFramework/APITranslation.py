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


'''
	This file is due to bad experiences relying directly on a Discord Library. 
	This file basically is a translation layer between the bot framework and the Library.
	In short should the libary/API change, or a new one be needed, all interactions with it it
	are in more or less one place for easy fixing.
	This translator is pre-coded for Discord.py (https://github.com/Rapptz/discord.py).
'''
import asyncio

import discord
from .Testing import TestingClient


class APITranslator:
	def __init__(self, bot, testing, platform):
		self.bot = bot
		self.testing = testing
		self.platform = platform
		if self.testing:
			self.client = TestingClient(bot)
			self.version = self.client.version
		elif platform == "discord":
			self.client = DiscordClient(bot, loop=self.bot.loop)
			self.version = "{} {}.{}.{}".format(discord.version_info[3], 
				discord.version_info[0], discord.version_info[1], 
				discord.version_info[2])
			self.APIRaw = discord
		else:
			raise 
	
	#Platform Checks
	def discordC(self):
		if self.platform.lower() == "discord":
			return True
		else:
			return False
	
	
	#Basic Translations
	def run(self, token):
		try:
			if self.discordC():
				self.discordRun(token)
			else:
				self.client.run(token)
		except asyncio.CancelledError:
			pass
	
	def discordRun(self, token):
		async def runner():
			await self.client.start(token)
		#self.bot.loop.create_task(runner())
		try:
			self.bot.loop.run_until_complete(runner())
		finally:
			self.bot.loop.run_until_complete(self.bot.loop.shutdown_asyncgens())
			self.bot.loop.close()
		
	async def discordStop(self):
		await self.client.close()
		print("Discord Closed!")
			
	
	async def waitUntilReady(self):
		return await self.client.wait_until_ready()
	
	def getUser(self, userID, message):
		return message.server.discordServer.get_member(userID)
	def getLowUser(self, userID):
		return self.client.get_user(userID)
	
	#Game Related Discord Stuff
	def getGame(self, userID, message):
		if self.discordC:
			memberObject = self.getUser(userID, message)
			if memberObject != None:
				gameName = memberObject.activity.name
				gameURL = None
				gameType = memberObject.activity.type
				game = {"Name":gameName,"Type":gameType,"URL":gameURL}
			else:
				game = None
			return game
		else:
			return None
	
	async def changeStartGame(self):
		if self.discordC:
			gameSettings = self.bot.settings["game"]
			game = discord.Game(name=gameSettings["Name"], 
			url=gameSettings["URL"], type=gameSettings["Type"])
			await self.client.change_presence(activity=game)
			
	async def changeGame(self, gameName):
		if self.discordC:
			if gameName == None:
				game = None
			else:
				game = discord.Game(name=gameName, url=None, 
					type=None)
			await self.client.change_presence(activity=game)
	
	#Message Related Stuff
	async def sendMessage(self, channelID, message):
		if self.discordC:
			channel = self.client.get_channel(channelID)
			await channel.send(message)
		else:
			print("Unknown Platform Message: {}".format(message))
	
	async def getHistory(self, channel, *, limit=100, before=None, after=None, around=None, oldest_first=None):
		if self.discordC:
			return channel.history(limit=limit, before=before, 
				after=after, around=around, oldest_first=oldest_first)
		else:
			return None
	
	#Permissions
	def modCheck(self, message):
		if self.discordC:
			perms = message.author.discordAuthor.permissions_in(message.channel._discordChannel)
			if perms.manage_messages():
				return True
			else:
				return False
	
	def adminCheck(self, message):
		if self.discordC:
			perms = perms = message.author.discordAuthor.permissions_in(message.channel._discordChannel)
			if perms.manage_channels():
				return True
			else:
				return False

class DiscordClient(discord.Client):
	def __init__(self, bot, *, loop=None, **options):
		self.bot = bot
		super().__init__(loop=loop, **options)
	async def on_ready(self):
		self.bot.name = self.user.name
		self.bot.id = self.user.id
		await self.bot.bot_ready()
	async def on_message(self, disMessage):
		message = MessageObject(disMessage, self.bot)
		await self.bot.on_message(message)
		
class MessageObject():
	def __init__(self, message, bot=None):
		self.author = UserObject(message.author, bot)
		self.text = message.content
		self.embeds = message.embeds
		self.channel = ChannelObject(message.channel)
		self.server = self.channel.server
		self.id = message.id
		self.attachments = []
		for attach in message.attachments:
			self.attachments.append(AttachmentObject(attach))

class AttachmentObject():
	def __init__(self, attachment):
		self.id = attachment.id
		self.size = attachment.size
		self.height = attachment.height
		self.width = attachment.width
		self.filename = attachment.filename
		self.url = attachment.url

class ChannelObject():
	def __init__(self, channel):
		self.name = channel.name
		self.server = ServerObject(channel.guild)
		self.id = channel.id
		self.catID = channel.category_id
		self.topic = channel.topic
		self._discordChannel = channel
	
	def history(self, *, limit=100, before=None, after=None, around=None, oldest_first=None):
		return self._discordChannel.history(limit=limit)
		

class ServerObject():
	def __init__(self, server):
		self.name = server.name
		self.id = server.id
		self.ownerID = server.owner_id
		self.unavailable = server.unavailable
		self.discordServer = server

class UserObject():
	def __init__(self, member, bot=None):
		self.name = member.name #The User name
		self.id = member.id #The ID Number
		self.discrim = member.discriminator #The #8139
		self.bot = member.bot #Bool if bot account
		self.system = member.system #Bool if user is system user (Discord)
		self.roles = member.roles
		self.discordAuthor = member
		self.discordNick = member.nick #Nickname set on Discord server
		if bot != None: #Checks for a custom nickname set in bot
			nickList = bot.otherVars["customNicks"]
			if self.id in nickList:
				randNick = [random.choice(nickList), self.discordNick]
				self.nick = random.choice(randNick)
			else:
				self.nick = self.discordNick
		else:
			self.nick = self.discordNick

		

		
