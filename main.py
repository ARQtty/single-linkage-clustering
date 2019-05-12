import classifier
import graphics.gui as gui
import data.generator as generator


def readFromFile(filename):
	data = []
	with open(filename, "r") as fin:
		data = [int(x) for x in fin.readline().split()]
	return data





#data = readFromFile("data/data.txt")
#data = generator.badCaseGenerator(None)
data = generator.randomIntGenerator(15, rborder=40)

tree = classifier.fitFast(data)
gui.show(tree=tree, wSize=(900, 500))
