# -*- coding: utf-8 -*-
import pygame, math as m, palette, Image, ImageDraw

class Mandel:

	def __init__(self):
		self.x = 400
		self.y = 300
		self.focusx = -0.5
		self.focusy = 0.0
		self.magnify = 1.0
		self.bound = 100
		self.setup()
		self.backgroundColour = (30, 30, 30)
		self.Colours = palette.Palette(1,1000)
		self.wallsizeX = 1200
		self.wallsizeY = 800
		
	def setup(self):
		self.ratio = float(self.x) / self.y
		self.minx = self.focusx - ((1.5 * self.ratio / self.magnify))
		self.miny = self.focusy - ((1.5 / self.magnify))
		self.width = 3 * self.ratio / self.magnify
		self.height = 3 / self.magnify
		self.xstep = self.width / self.x
		self.ystep = self.height / self.y
		self.updateline = 0
		self.updating = True
		self.exporting = False

	def setupWall(self):
		self.ratio = float(self.wallsizeX) / self.wallsizeY
		self.minx = self.focusx - ((1.5 * self.ratio / self.magnify))
		self.miny = self.focusy - ((1.5 / self.magnify))
		self.width = 3 * self.ratio / self.magnify
		self.height = 3 / self.magnify
		self.xstep = self.width / self.wallsizeX
		self.ystep = self.height / self.wallsizeY
		self.exportline = 0
		self.exporting = True
		self.filename = str(self.wallsizeX) + 'x_' + str(self.wallsizeY) + "y - " + str(self.magnify) + ' zoom.jpg'
		self.im = Image.new("RGB", (self.wallsizeX, self.wallsizeY), "black")
		self.wallValues = []
	
	def text(self, Screen):
		Screen.fill(self.backgroundColour, pygame.Rect(0, self.y + 1, self.x, 50))
		size = 12
		screenText = pygame.font.SysFont('Tahoma', size)
		position = 'Center: ' + str(self.focusx) + ' + ' + str(-self.focusy) + 'i'
		zoom = 'Zoom Level: ' + str(self.magnify) + 'x' + ', Bound: ' + str(self.bound)
		positionText = screenText.render(position, 1, (255, 255, 255))
		zoomText = screenText.render(zoom, 1, (255, 255, 255))
		Screen.blit(positionText, (5, self.y+5))
		Screen.blit(zoomText, (5, self.y+10+size))
		
	def eval_point(self, real, imaginary):
		p = m.sqrt((real - 0.25)**2 + imaginary**2)
		if real < p - 2*p**2 + 0.25 or (real + 1)**2 + imaginary**2 < 1.0/16:
			return (0,0,0)
		else:
			n = 0
			z = c = complex(real, imaginary)
			while n < self.bound and abs(z) < 3:
				z = c + z**2
				n += 1
			if n == self.bound:
				return (0, 0, 0)
			else:
				k = (n + 1 - m.log(m.log(abs(z)))/m.log(2)) * 10
				return self.Colours.colours[int(k%self.Colours.n)]	

	def update(self, Screen):
		if self.updateline == 0:
			self.text(Screen)	
		currenty = self.miny + self.updateline*self.ystep
		currentx = self.minx
		Screen.lock()
		currentx = self.minx
		for i in range(0, self.x):
			point = self.eval_point(currentx, currenty)
			currentx += self.xstep
			Screen.set_at((i,self.updateline), point)
		currenty += self.ystep
		Screen.unlock()
		pygame.draw.line(Screen, (255, 255, 255), (0, self.updateline+1), (self.x - 1, self.updateline+1))
		pygame.display.flip()
		if self.updateline == self.y - 1:
			self.updating = False
		else:
			self.updateline += 1

	def keypress(self, key, Screen):
		if self.exporting != True:
			if key == pygame.K_PAGEUP or key == pygame.K_PAGEDOWN:
				self.zoom(key)
			elif key == pygame.K_UP:
				self.click((self.x/2, -self.y/2))
			elif key == pygame.K_DOWN:
				self.click((self.x/2, self.y + self.y/2))
			elif key == pygame.K_LEFT:
				self.click((-self.x/2, self.y/2))
			elif key == pygame.K_RIGHT:
				self.click((self.x + self.x/2, self.y/2))
			elif key == pygame.K_HOME or key == pygame.K_END:
				self.newBound(key)
			elif key == pygame.K_1:
				if self.Colours.schemeID != 1:
					self.Colours.schemeID = 1
					self.Colours.set_colours()
					self.setup()
			elif key == pygame.K_2:
				if self.Colours.schemeID != 2:
					self.Colours.schemeID = 2
					self.Colours.set_colours()
					self.setup()
			elif key == pygame.K_x:
				if self.updating != True:
					self.export_image(Screen)
			elif key == pygame.K_w:
				if self.updating != True:
					self.setupWall()
		
	def newBound(self, key):
		if key == pygame.K_HOME:
			self.bound = self.bound + 100
			self.setup()
		else:
			if self.bound != 100:
				self.bound = self.bound - 100
				self.setup()
	
	def click(self, (X, Y)):
		self.setup()
		self.focusx = self.minx + self.xstep*X
		self.focusy = self.miny + self.ystep*Y
		self.setup()
		
	def zoom(self, key):
		if key == pygame.K_PAGEUP:
			self.magnify = self.magnify*5
		else: 
			self.magnify = self.magnify/5
		self.setup()
	
	def export_image(self, Screen):
		filename = str(self.x) + 'x_' + str(self.y) + "y - " + str(self.magnify) + ' zoom.png'
		values = []
		nextline = []
		for j in range(0, self.y):
			if j !=0:
				for k in range(0, self.x):
					Screen.set_at((k, j-1), values[-self.x+k])
			nextline = []
			for i in range(0, self.x):
				nextline += [tuple(Screen.get_at((i, j)))]
			pygame.draw.line(Screen, (255,255,255), (0, j), (self.x - 1, j))
			pygame.display.flip()
			values += nextline	
		im = Image.new('RGB', (self.x, self.y), 'black')
		im.putdata(values)
		im.save(filename)
	
	def export_wallpaper(self, Screen):
		values = []
		currenty = self.miny + self.exportline*self.ystep
		currentx = self.minx
		for i in range(0, self.wallsizeX):
			values += [self.eval_point(currentx, currenty)]
			currentx += self.xstep
		self.wallValues += values
		
		if self.exportline % 2 == 0:
			pygame.draw.line(Screen, (255,255,255), (self.exportline/2, self.y+1), (self.exportline/2, self.y+49))
			pygame.display.flip()
		
		if self.exportline == self.wallsizeY - 1:
			self.exporting = False
			self.im.putdata(self.wallValues)
			self.wallValues = []
			self.im.save(self.filename)
			self.text(Screen)
			pygame.display.flip()
		else:
			self.exportline += 1 
			
Set = Mandel()
pygame.init()
Screen = pygame.display.set_mode((Set.x, Set.y + 50))
Screen.fill(Set.backgroundColour)
pygame.draw.line(Screen, (255, 255, 255), (0, Set.y), (Set.x - 1, Set.y))
pygame.display.set_caption('Mandelbro')

running = True
clock = pygame.time.Clock()

while running == True:
	if Set.updating == True and Set.exporting == False:
		Set.update(Screen)
	elif Set.exporting == True and Set.updating == False:
		Set.export_wallpaper(Screen)
	elif Set.exporting == True and Set.updating == True:
		print "POBLEMS"
		running = False
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN and Set.exporting != True:
			Set.click(event.pos)
		elif event.type == pygame.KEYDOWN:
			Set.keypress(event.key, Screen)
			
	clock.tick(200)	

pygame.quit()