import classifier
import graphics.gui as gui
import data.generator as generator


def readFromFile(filename):
	data = []
	with open(filename, "r") as fin:
		data = [int(x) for x in fin.readline().split()]
	return data


data = readFromFile("data/data.txt")


gui.show(classifier.fitFast(data), wSize=(800, 400))