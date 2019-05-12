import random



def randomFloatGenerator(n, lborder=0, rborder=30):
	number = lambda: random.randint(lborder, rborder)+random.random()*(rborder-lborder)
	points = sorted(list({round(number(), 1) for x in range(n)}))
	return points

def randomIntGenerator(n, lborder=0, rborder=90):
	number = lambda: random.randint(lborder, rborder)
	points = sorted(list({number() for x in range(n)}))
	return points


def badCaseGenerator(n, lborder=0, rborder=20):
	points = [x for x in range(lborder, rborder//2)]
	points += [rborder//2+2]
	points += [x for x in range(rborder//2+2 + 2, rborder)]
	return points