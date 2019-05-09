import classifier
import graphics as gui


def readFromFile(filename):
	data = []
	with open(filename, "r") as fin:
		data = [int(x) for x in fin.readline().split()]
	return data





data = readFromFile("data.txt")
tree = classifier.fit(data)
gui.show(tree=tree, wSize=(1500, 600))