class Node():
    def __init__(self, value, parent=None, lChild=None, rChild=None):
        self.value = value
        self.level = 0
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
    parent.level = max(node1.level, node2.level) + 1
    parent.lChild = node1
    parent.rChild = node2
    node1.parent = parent
    node2.parent = parent

    return parent


def fit(data):
    data = [Node(x) for x in data]
    distF = lambda p1, p2: abs(p1.value - p2.value)

    while len(data) != 1:
         #clastering
        minDist = float('inf')
        minP1_index = None
        minP2_index = None
        
        for i, p1 in enumerate(data):
            for j, p2 in enumerate(data):
                if p1 != p2 and distF(p1, p2) < minDist:
                    minP1_index = i
                    minP2_index = j
                    minDist = distF(p1, p2)
        
        # Нашли ближайшие кластеры. Объединяем
        newClast = createParent(data[minP1_index], data[minP2_index])
        # print(clastered)
        if minP1_index > minP2_index:
            minP1_index, minP2_index = minP2_index, minP1_index
        # Выкинем две точки, которые объединили
        data = data[:minP1_index] + data[minP1_index+1:minP2_index] + data[minP2_index+1:]
        # Закинем точку-новый_кластер
        data.append(newClast)

    # Возвращаем корень
    return data[0]