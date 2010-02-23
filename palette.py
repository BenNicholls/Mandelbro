"""
	Palette Class (palette.py)
	Last updated Jan 24, 2010
	
	Generates circular RGB colour palette with n entries. Allows for changing of
	reference colours (c1 -> c4). 
	
	TO DO:
		- Change reference colours to be based on "schemes": sets of 4 colours. Class
		  should store these schemes internally and allow for easy switching between
		  them.
		- Allow for initialization variables for colours, n
		- Current "ensure n is divisible by 4" just fudges the user defined n so it
		  works. Maybe this should instead throw an exception or something. User
		  might wonder why their n isn't being used.
"""

class Palette:

	def __init__(self, scheme, size):
		self.schemeID = scheme
		self.n = size
		self.set_colours()
	
	def generate(self):
		self.n = self.n - self.n % 4			
		self.colours = []
		k = self.n/4
		for i in range(0, k):
			r = self.c1[0] + (i * (self.c2[0] - self.c1[0]) / k)
			g = self.c1[1] + (i * (self.c2[1] - self.c1[1]) / k)
			b = self.c1[2] + (i * (self.c2[2] - self.c1[2]) / k)
			self.colours += [(int(r), int(g), int(b), 0)]
	
		for i in range(0, k):
			r = self.c2[0] + (i * (self.c3[0] - self.c2[0]) / k)
			g = self.c2[1] + (i * (self.c3[1] - self.c2[1]) / k)
			b = self.c2[2] + (i * (self.c3[2] - self.c2[2]) / k)
			self.colours += [(int(r), int(g), int(b), 0)]
		
		for i in range(0, k):
			r = self.c3[0] + (i * (self.c4[0] - self.c3[0]) / k)
			g = self.c3[1] + (i * (self.c4[1] - self.c3[1]) / k)
			b = self.c3[2] + (i * (self.c4[2] - self.c3[2]) / k)
			self.colours += [(int(r), int(g), int(b), 0)]
		
		for i in range(0, k):
			r = self.c4[0] + (i * (self.c1[0] - self.c4[0]) / k)
			g = self.c4[1] + (i * (self.c1[1] - self.c4[1]) / k)
			b = self.c4[2] + (i * (self.c1[2] - self.c4[2]) / k)
			self.colours += [(int(r), int(g), int(b), 0)]

	def set_colours(self):
		if self.schemeID == 1:
			scheme = ((25, 25, 122), (205, 133, 0), (255, 255, 255), (180, 205, 205))
		elif self.schemeID == 2:
			scheme = ((138, 54, 15), (255, 246, 143), (56, 142, 142), (255, 215, 0))
		self.c1 = scheme[0]
		self.c2 = scheme[1]
		self.c3 = scheme[2]
		self.c4 = scheme[3]
		self.generate()