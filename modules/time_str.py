def seconds_to_str(sec: int):

	sec = sec % (24 * 3600)
	hour = sec // 3600
	sec %= 3600
	min = sec // 60
	sec %= 60
	
	return "%02d:%02d:%02d" % (hour, min, sec)
