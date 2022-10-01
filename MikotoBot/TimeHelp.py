import datetime
import pytz

class Time:
	def __init__(self):
		pass
	def getTime(self):
		now = datetime.datetime.now()
		hour = str(now.hour)
		minute = str(now.minute)
		second = str(now.second)
		year = str(now.year)
		month = str(now.month)
		day = str(now.day)
		time = ("{m}/{d}/{y}, {h}:{min}:{s}".format(m=month, d=day, y=year, h=hour, 
			min=minute, s=second))
		return time
	
	def getTimeStandard(self):
		now = datetime.datetime.now()
		hour = self.standardizedTime(now.hour)
		minute = self.standardizedTime(now.minute)
		second = self.standardizedTime(now.second)
		year = self.standardizedTime(now.year)
		month = self.standardizedTime(now.month)
		day = self.standardizedTime(now.day)
		time = ("{m}/{d}/{y}, {h}:{min}:{s}".format(m=month, d=day, y=year, h=hour, 
			min=minute, s=second))
		return time
	
	def getDate(self):
		now = datetime.datetime.now()
		year = str(now.year)
		month = str(now.month)
		day = str(now.day)
		time = ("{m}/{d}/{y}".format(m=month,d=day,y=year))
		return time
	
	def getTime12Hour(self):
		now = datetime.datetime.now()
		hour, halfday = self.time12HourConvert(now.hour)
		minute = self.standardizedTime(now.minute)
		second = self.standardizedTime(now.second)
		year = str(now.year)
		month = self.standardizedTime(now.month)
		day = self.standardizedTime(now.day)
		time = ("{m}/{d}/{y}, {h}:{min}:{s} {hd} EST".format(m=month, d=day, y=year, 
			h=hour, min=minute, s=second, hd=halfday))
		return time
	
	def timeMath(self, **times):
		utc = times.get("utc", False)
		if utc:
			now = datetime.datetime.utcnow()
		else:
			now = datetime.datetime.now()
		secondDif = times.get("second",0)
		minuteDif = times.get("minute",0)
		hourDif = times.get("hour",0)
		dayDif = times.get("day",0)
		nowDifDateTime = datetime.timedelta(days=dayDif, minutes=minuteDif, 
			seconds=secondDif, hours=hourDif)
		difference = now - nowDifDateTime
		hour, halfday = self.time12HourConvert(difference.hour)
		minute = self.standardizedTime(difference.minute)
		second = self.standardizedTime(difference.second)
		year = str(difference.year)
		month = str(difference.month)
		day = str(difference.day)
		time = ("{m}/{d}/{y}, {h}:{min}:{s} {hd}".format(m=month, d=day, y=year, h=hour, 
			min=minute, s=second, hd=halfday))
		return time
	
	def getPartTime(self, toGet):
		valid = ["hour","minute","second","year","month","day"]
		now = datetime.datetime.now()
		hour = str(now.hour)
		minute = str(now.minute)
		second = str(now.second)
		year = str(now.year)
		month = str(now.month)
		day = str(now.day)
		if toGet in valid:
			return eval(toGet)
		else:
			raise NameError("Invalid Time")
	
	def timeZonedNow(self, timeZone):
		now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
		localDateTime = now.astimezone(pytz.timezone(timeZone))
		hour, halfday = self.time12HourConvert(localDateTime.hour)
		minute = self.standardizedTime(localDateTime.minute)
		second = self.standardizedTime(localDateTime.second)
		year = str(localDateTime.year)
		month = self.standardizedTime(localDateTime.month)
		day = self.standardizedTime(localDateTime.day)
		time = ("{m}/{d}/{y}, {h}:{min}:{s} {hd}".format(m=month, d=day, y=year, 
			h=hour, min=minute, s=second, hd=halfday))
		return time
	
	def time12HourConvert(self, hour):
		if hour > 12:
			hour = str(hour - 12)
			halfday = "PM"
		elif hour == 0:
			hour = "12"
			halfday = "AM"
		elif hour == 12:
			hour = "12"
			halfday = "PM"
		else:
			hour = str(hour)
			halfday = "AM"
		if int(hour) < 10:
			hour = "0" + hour
		return hour, halfday
	
	def standardizedTime(self, time):
		if int(time) < 10:
			time = "0{}".format(time)
		else:
			time = str(time)
		return time
