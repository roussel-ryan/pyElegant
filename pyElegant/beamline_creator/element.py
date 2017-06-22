# -*- coding: utf-8 -*-

class BeamlineElement:
	def __init__(self,name,type,parameters):
		self.name = name
		self.type = type
		self.parameters = parameters
	
	
	
	def writeElement(self):
		retString = self.name + ': ' + self.type + ','
		for name,value in self.params.items():
			retString += name + '=' + str(value) + ','
		retString = retString[:-1] + '\n'
		return retString