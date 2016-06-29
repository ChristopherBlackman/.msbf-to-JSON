import os
import json
class FileType_msbf:
  
#convert file to data if file exists
	def __init__(self, msbfPath):
		self.list = []
		if not self.__checkFile(msbfPath):
			print "-invalid file"
			return
		else:
			print "-valid file"
		self.__convert(msbfPath)
		print "-file has been instatiated"
    
    
	#can the file be opened in the current directory
	def __checkFile(self, msbfPath):
		print "-checking file"
		if not os.path.isfile(msbfPath):
			return False
		try:
			f = open(msbfPath,'r')
			f.close()
		except IOError as e:
			return False
		return True
  
	#start to convert the file
	def __convert(self, msbfPath):
		print "-converting file"
		f = open(msbfPath,'r')
		readFile = f.read()
		f.close
		
		master = []
		slave = []
		string = ""
		
		# brings data into list format
		for index in range(len(readFile)):
			#sub-cat
			if ord(readFile[index]) == 9: #tab
				slave.append(string)
				string = ""
			#new manga
			elif ord(readFile[index]) == 10: #newline
				slave.append(string)
				string = ""
				master.append(slave)
				slave = []
			else:
				string = string + readFile[index]
		self.list = master
		
		#removes inconsistent data
		for subSlave in master:
			if len(subSlave) != 5:
				master.remove(subSlave)
				print "-inconsistent item has been removed!"
	
	#saves data to a file in json format
	def outputToJson (self, outputPath):
		json_object = json.dumps(self.list,sort_keys=True)
		print "-saving data"
		try:
			f = open(outputPath,"w")
			f.write(json_object)
		except IOError as e:
			print "error writing to file, please check permissions"
			return
		print "done"
		return
		
	def toString (self):
		master = self.list
		for index in range(len(master)):
			print "--------------------"
			for s in master[index]:
				print "	",s
		return

    
data = FileType_msbf('/home/chris/Documents/git/mangaStorm/favorites.msbf')
data.outputToJson('/home/chris/Documents/git/mangaStorm/favorites')
