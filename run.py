from engine import *

size = [50,50] # size of petri
automode = False # auto nextGen

# для графики
see = {
	"fps": 10, # speed of screen
	"size": 8, # size of one cell
	"text": 20, # size of text
	"norm": 5, # size of division for graph
	"values": False, # view values
	"vectors": False, # view vectors
	"graph": False, # view graph
}
# инициализация графики
display = gui.Scene("vectors", (size[0]*see["size"]*2,size[1]*see["size"]), see["fps"], (50,50,50))


# инициализация "среды"
petri = Petri(size, True)
brief = []

while True:
	key = display.start()
	# =============================================

	# обработка нажатий ---------------
	if key:
		if key == "Esc": break
		elif key == "Space":
			brief = []
			petri.fill([0,10])
		elif key == "Right" and not automode:
			petri.nextGen()
			brief.append([nval, petri.min(), aver, petri.max()])
		elif key == "Up": see["fps"] += 10
		elif key == "Down": see["fps"] -= 10
		elif key == "0": automode = False if automode else True
		elif key == "1": see["values"] = False if see["values"] else True
		elif key == "2": see["vectors"] = False if see["vectors"] else True
		elif key == "3": see["graph"] = False if see["graph"] else True
		elif key == "s": petri.save()


	# отрисовка ---------------------

	aver, nval = petri.drawValues(display, [0,0], see["size"], see["values"])
	if see["vectors"]: petri.drawVectors(display, [0,0], see["size"])

	text = [
		[(100,100,100), "[Space]Fill [Right]nextGen [0]automode({})".format(str(automode))],
		[(100,100,100), "[1]values({}) [2]vectors({}) [3]graph({})".format(str(see["values"]), str(see["vectors"]), str(see["graph"]))],
		[(100,100,100), "[Up]fps+10 [Down]fps-10"],
		False,
		[(150,150,150), "size: {}".format(size)],
		[(150,150,150), "fps: {}".format(see["fps"])],
		False,
		[(250,150,150), "min: {}".format(petri.min())],
		[(250,250,150), "average: {}".format(aver)],
		[(150,250,150), "max: {}".format(petri.max())],
		False,
		[(200,200,200), "elements: {}".format(nval)]]
	for i in range(len(text)):
		if text[i]: display.drawText(text[i][1], [size[0]*see["size"], see["text"]*i], see["text"], text[i][0])

	if see["graph"]: drawGraph(display, [size[0]*see["size"], size[1]*see["size"]], see["norm"], brief)

	# логика ---------------

	if automode: 
		petri.nextGen()
		brief.append([nval, petri.min(), aver, petri.max()])


	# =============================================
	display.update(see["fps"])