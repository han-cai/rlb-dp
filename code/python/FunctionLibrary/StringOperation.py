import time


def getTime():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def getStringList(list):
	str_list = []
	for item in list:
		str_list.append(str(item))
	return str_list
