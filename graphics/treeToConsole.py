def depthOfChildren(v, currDepth=0):
	lDepth = 0
	rDepth = 0

	if v.lChild:
		lDepth = max(depthOfChildren(v.lChild, currDepth)) + 1
	if v.rChild:
		rDepth = max(depthOfChildren(v.rChild, currDepth)) + 1

	return (lDepth, rDepth)


def depthOfNode(searchV, treeV):
	# print("match", searchV, treeV)
	if searchV == treeV:
		# print("!")
		return 0
	
	else:
		if treeV.lChild:
			depth = depthOfNode(searchV, treeV.lChild)
			if depth != None: return depth+1
			
		if treeV.rChild:
			depth = depthOfNode(searchV, treeV.rChild)
			if depth != None: return depth+1
		
	print("Узел ", searchV, " не найден")
	return None



class Node():
	def __init__(self, value, parent=None, lChild=None, rChild=None):
		self.value = value
		self.parent = parent
		self.lChild = lChild
		self.rChild = rChild

	def __repr__(self):
		return "<Node val=%f lCh=%s rCh=%s>" % (self.value, self.lChild!=None, self.rChild!=None)


def createParent(node1, node2):
	if node1.value > node2.value:
		node1, node2 = node2, node1

	avgValue = (node1.value + node2.value) / 2
	
	parent = Node(avgValue)
	parent.lChild = node1
	parent.rChild = node2
	node1.parent = parent
	node2.parent = parent

	return parent


nodes = [Node(x) for x in range(13)]

n23 = createParent(nodes[2], nodes[3])
n236 = createParent(n23, nodes[6])
n910 = createParent(nodes[9], nodes[10])
n1112 = createParent(nodes[11], nodes[12])
n9101112 = createParent(n910, n1112)

tree = createParent(n236, n9101112)



