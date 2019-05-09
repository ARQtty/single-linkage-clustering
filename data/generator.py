import random



def randomGenerator(n, lborder=0, rborder=40):
	points = [random.randint(lborder, rborder) for x in range(n)]
	return points


def badCaseGenerator(n, lborder=0, rborder=20):
	points = [x for x in range(lborder, rborder//2)]
	points += [rborder//2+2]
	points += [x for x in range(rborder//2+2 + 2, rborder)]
	return points