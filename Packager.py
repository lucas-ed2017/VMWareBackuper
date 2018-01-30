from os import system

class Packager(object):

	def __init__(self, fileToCompress, destFile):
		self.fileToCompress = fileToCompress
		self.destFile = destFile

	def compress(self):
		try:
			system("tar -cf " + self.destFile + " " + self.fileToCompress)
		except Exception as e:
			print(e)
			raise