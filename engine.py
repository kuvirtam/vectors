import gui
import json
from random import randint
from datetime import datetime as date

# открытие json и забор данных
def jsOpen(path):
	with open(path, "r", encoding="utf-8") as file:
		data = json.load(file)
	return data
# сохранение данных в json
def jsSave(path, data):
	with open(path, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False)

# нормализация индекса относительно размера массива
def n(i, size):
	while True:
		if size == 0: return 0
		elif i >= size: i -= size; continue
		elif i <= -size: i += size; continue
		else: return i

# нормализация направления
def d(n):
	if n > 0: return 1
	elif n < 0: return -1
	else: return 0

# ---------------------------------------------------------

# работа со "средой"
class Petri:

	# создание массива
	def genTable(self, size, el=0):
		table = []
		for i in range(size[0]):
			table.append([])
			for ii in range(size[1]):
				table[i].append(el)
		return table

	# ининциализация среды
	def __init__(self, size, write):
		self.size = size
		self.values = self.genTable(size, 0)
		self.vectors = self.genTable(size, [0, 0])
		self.write = write
		if write: self.story = [["init", self.values, self.vectors]]

	# сохранении поколения в историю
	def addStory(self, tip): 
		if self.write: self.story.append([tip, self.values, self.vectors])
	# сохранение истории в файл:
	def save(self): 
		jsSave("saves/{}.json".format(date.now().strftime("%Y%m%d%H%M%S")), self.story)

	# максимальная и минимальная переменная в среде 
	def max(self): return max(sum(self.values, []))
	def min(self): return min(sum(self.values, []))

	# задание и обновление переменной в конкретном месте
	def val(self, xy, value):
		self.values[n(xy[0], self.size[0])][n(xy[1], self.size[1])] = value
		self.addStory("console")
	def updv(self, xy, delta): 
		self.values[n(xy[0], self.size[0])][n(xy[1], self.size[1])] += delta
		self.addStory("console")

	# изменение направления вектора
	def dir(self, xy, vector): 
		self.vectors[n(xy[0], self.size[0])][n(xy[1], self.size[1])] = vector
		self.addStory("console")
	def dirX(self, xy, vector_x): 
		self.vectors[n(xy[0], self.size[0])][n(xy[1], self.size[1])][0] = vector_x
		self.addStory("console")
	def dirY(self, xy, vector_y): 
		self.vectors[n(xy[0], self.size[0])][n(xy[1], self.size[1])][1] = vector_y
		self.addStory("console")
	def updd(self, xy, deltas): 
		self.vectors[n(xy[0], self.size[0])][n(xy[1], self.size[1])] = [d(self.vectors[n(xy[0], self.size[0])][n(xy[1], self.size[1])][0]+deltas[0]), d(self.vectors[n(xy[0], self.size[0])][n(xy[1], self.size[1])][1]+deltas[1])]
		self.addStory("console")

	# задание переменной и направления в конкретном месте
	def set(self, xy, val, dir):
		self.val(xy, val)
		self.dir(xy, dir)

	# заполнение среды случайными данными
	def fill(self, span):
		for i in range(self.size[0]):
			for ii in range(self.size[1]):
				self.val([i,ii], randint(span[0], span[1]))
				self.dir([i,ii], [randint(-1, 1), randint(-1, 1)])
		self.addStory("console")

	# переформировать текущую среду на входную
	def inject(self, petri):
		self.values = petri.values
		self.vectors = petri.vectors

	# отрисовка переменных
	def drawValues(self, display, pos, size, valsee=False):
		nonull = 0
		aver = 0
		for i in range(self.size[0]):
			for ii in range(self.size[1]):
				t = self.values[i][ii]
				aver += t
				if t != 0: nonull += 1
				x, y = pos[0]+i*size, pos[1]+ii*size
				c = 255*(t/(self.max()+1))
				display.drawBox( [x, y], [size, size], (c,c,c))
				if valsee and t != 0: display.drawText( str(t), [x, y], size, (255-c, 255-c, 255-c))
		return (aver/(nonull+1)), nonull

	# отрисовка направлений
	def drawVectors(self, display, pos, size):
		ln = 3
		dirs = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]
		for i in range(self.size[0]):
			for ii in range(self.size[1]):
				vec = self.vectors[i][ii]
				if vec != [0,0]:
					x, y = pos[0]+i*size+int(size/2), pos[1]+ii*size+int(size/2)
					t = dirs.index(vec)
					display.drawLine([
						[x+int(size/3)*dirs[n(t-ln, len(dirs))][0], y+int(size/3)*dirs[n(t-ln, len(dirs))][1]],
						[x+int(size/3)*vec[0], y+int(size/3)*vec[1]],
						[x+int(size/3)*dirs[n(t+ln, len(dirs))][0], y+int(size/3)*dirs[n(t+ln, len(dirs))][1]],
					], (255,0,0))


	# обновление среды до следующего поколения
	def nextGen(self):
		newPetri = Petri(self.size, False)
		for i in range(self.size[0]):
			for ii in range(self.size[1]):
				if self.values[i][ii] != 0:
					x = i + self.vectors[i][ii][0]
					y = ii + self.vectors[i][ii][1]
					newPetri.updv([x,y], self.values[i][ii])
					newPetri.updd([x,y], self.vectors[i][ii])
		self.inject(newPetri)
		self.addStory("native")


def drawGraph(display, pos, norm, brief):
	for i in range(len(brief)):
		display.drawDot([pos[0]+i, pos[1]-int(brief[i][0]/norm)], 1, (255,255,255))
		display.drawDot([pos[0]+i, pos[1]-int(brief[i][1]/norm)], 1, (200,100,100))
		display.drawDot([pos[0]+i, pos[1]-int(brief[i][2]/norm)], 1, (200,200,100))
		display.drawDot([pos[0]+i, pos[1]-int(brief[i][3]/norm)], 1, (100,200,100))
