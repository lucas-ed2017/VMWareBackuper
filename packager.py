from os import system

class packager(object):

	def __init__(self, fileToCompress, destFile):
		self.fileToCompress = fileToCompress
		self.destFile = destFile

	def compress(self):
		try:
			system("tar -cf \"" + self.destFile + ".tar\" \"" + self.fileToCompress + "\"")
		except Exception as e:
			print(e)
			raise
