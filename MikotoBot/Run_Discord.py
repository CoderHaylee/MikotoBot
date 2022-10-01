import argparse
import time
import subprocess
import sys
import os

#from BotFramework import Bot
import Connect

print("Python: " + str(sys.version_info[0]) + "." + str(sys.version_info[1]))
pidFile = "Bot.pid"
open(pidFile,"w").write(str(os.getpid()))
def pidEnd():
	os.remove(pidFile)
	print('\n\033[92m' + pidFile + " has been deleted.\033[0m")
def set_procname(newname):
	newname = newname.encode("utf-8")
	from ctypes import cdll, byref, create_string_buffer
	libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
	buff = create_string_buffer(len(newname)+1) #Note: One larger than the name (man prctl says that)
	buff.value = newname                 #Null terminated string as it should be
	libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious value 16 & arg[3..5] are zero as the man page says.
set_procname("MikotoBot")
parser = argparse.ArgumentParser(description="The parent Script for Mikoto Bot")
parser.add_argument("--testing", "-t", action="store_true", help="Starts the bot in test mode")
parser.add_argument("--run-once", "-1", action="store_true", help="Forces the bot to only run "
	"once and not auto restart, handy for debugging")
parser.add_argument("--platform", "-p", help="Changes platform Bot will go to.")
parser.add_argument("--dev", "-d", action="store_true", help="Uses the Dev Token instead.")

parsed = parser.parse_args()
print(parsed.platform)
try:
	bot = Connect.MikotoBot(testing=parsed.testing, dev=parsed.dev)
except SystemExit:
	print("sys.exit was used...")
except KeyboardInterrupt:
	print("Bot Interrupted")
pidEnd()
