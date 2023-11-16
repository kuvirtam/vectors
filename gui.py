import pygame as pg
from sys import exit

_KEYS = {
	# цифры
	48: "0",
	49: "1",
	50: "2",
	51: "3",
	52: "4",
	53: "5",
	54: "6",
	55: "7",
	56: "8",
	57: "9",
	# буквы
	97: "a",
	98: "b",
	99: "c",
	100: "d",
	101: "e",
	102: "f",
	103: "g",
	104: "h",
	105: "i",
	106: "j",
	107: "k",
	108: "l",
	109: "m",
	110: "n",
	111: "o",
	112: "p",
	113: "q",
	114: "r",
	115: "s",
	116: "t",
	117: "u",
	118: "v",
	119: "w",
	120: "x",
	121: "y",
	122: "z",
	# остальные
	13: "Enter",
	27: "Esc",
	32: "Space",
	8: "Backspace",
	9: "Tab",
	1073741906: "Up",
	1073741905: "Down",
	1073741904: "Left",
	1073741903: "Right",
	45: "-",
	61: "+",}

class Scene:

	def __init__(self, title, size, fps, bg=(0,0,0)):
		self.title = title
		self.size = size
		self.fps = fps
		self.bg = bg

		pg.init() 
		self.screen = pg.display.set_mode(self.size) 
		pg.display.set_caption(self.title) 
		self.screen.fill(self.bg) 
		self.clock = pg.time.Clock()

	def close(self):
		pg.display.quit()
		pg.quit()
		exit()

	def start(self):
		self.screen.fill(self.bg)
		for event in pg.event.get():
			if event.type == pg.QUIT: self.close()
			elif event.type == pg.KEYDOWN:
				try: return _KEYS[event.key]
				except: return False
		return False

	def update(self, fps):
		self.clock.tick(self.fps)
		self.fps = fps
		pg.display.update()


	def drawText(self, text, xy, size, color):
		f = pg.font.SysFont("Consolas", int(size/1.3))
		textout = f.render(str(text), 1, color)
		self.screen.blit(textout, xy)

	def drawBox(self, xy, size, color):
		pg.draw.rect(self.screen, color, xy+size)

	def drawLine(self, poses, color, close=False):
		pg.draw.lines(self.screen, color, close, poses)

	def drawDot(self, pos, r, color):
		pg.draw.circle(self.screen, color, pos, r)