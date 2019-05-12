class Node():
    # 56 bytes
    def __init__(self, value, parent=None, lChild=None, rChild=None):
        self.value = value
        self.level = 0
        self.parent = parent
        self.lChild = lChild
        self.rChild = rChild

    def __repr__(self):
        # return "<Node val=%f lCh=%s rCh=%s>" % (self.value, self.lChild!=None, self.rChild!=None)
        return "<Node val=%f level=%f>" % (self.value, self.level)

def createParent(node1, node2):
    if node1.value > node2.value:
        node1, node2 = node2, node1

    avgValue = (node1.value + node2.value) / 2
    
    parent = Node(avgValue)
    # Для отображения на дендрограмме
    parent.level = abs(node2.value - node1.value)
    parent.lChild = node1
    parent.rChild = node2
    node1.parent = parent
    node2.parent = parent
    print("    Creating parent", parent)

    return parent


def fit(data):
    # O(N^3)
    # Naive. Too long 
    data = [Node(x) for x in data]
    distF = lambda p1, p2: abs(p1.value - p2.value)
    finCount = 0

    while len(data) != 1:               
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
        # И закинем точку-новый_кластер
        data[minP1_index] = newClast
        data = data[:minP2_index] + data[minP2_index+1:]
        
        
    # Возвращаем корень
    return data[0]


def fitFast(data):
    # O(N^2)
    distL = [float('inf')] + [data[i] - data[i-1] for i in range(1, len(data))]
    distR = [data[i+1] - data[i] for i in range(len(data)-1)] + [float('inf')]
    
    distF = lambda p1, p2: abs(p1 - p2)

    #dist2next = [distF(data[i-1], data[i]) for i in range(1, len(data))]
    Mclust = [x for x in range(len(data))]
    MclustCenter = [x for x in data]
    ignorePoint = [False for x in range(len(data))]

    def dumpIteration():
        print("  ", end='')
        print("\n  ".join([str(x) for x in [distL, distR, Mclust, MclustCenter, ignorePoint]]))
    
    nodes = [Node(x) for x in data]
    clastN = len(data)

    while clastN != 1:
        print()
        dumpIteration()
        minDist = float('inf')
        minP1_index = None
        minP2_index = None


        # Ищем пару точек с минимальным расстоянием между собой
        # Ищем первую
        for i in range(len(data)):
            if not ignorePoint[i]:
                closestLPoint_i = i
                break
        # Ищем лучшую пару
        for i in range(closestLPoint_i+1, len(data)):
            if not ignorePoint[i]:
                closestRPoint_i = i

                # Нашли вторую проверяем на минимальность
                if distF(MclustCenter[closestLPoint_i], MclustCenter[closestRPoint_i]) < minDist:
                    minDist =  distF(MclustCenter[closestLPoint_i], MclustCenter[closestRPoint_i])
                    minP1_index = closestLPoint_i
                    minP2_index = closestRPoint_i

                # В любом случае исследуем дальше
                closestLPoint_i = closestRPoint_i


        print("best pair is ", minP1_index, minP2_index, "(%s %s) dist" % (nodes[minP1_index], nodes[minP2_index]), minDist)
        # Нашли лучшую пару. Соединяем
        clastN -= 1
        nodes[minP2_index] = createParent(nodes[minP1_index], nodes[minP2_index]) # Для представления в виде дерева
        ignorePoint[minP1_index] = True
        Mclust[minP1_index] = Mclust[minP2_index]
        MclustCenter[minP2_index] = (MclustCenter[minP2_index] + MclustCenter[minP1_index]) / 2
        #Нужно обновить distL и distR
        lNeighbour = None
        for i in range(minP1_index-1, -1, -1):
            if not ignorePoint[i]:
                lNeighbour = i
                break
        if lNeighbour:
            distR[lNeighbour] = MclustCenter[minP2_index] - MclustCenter[lNeighbour]
            distL[minP2_index] = MclustCenter[minP2_index] - MclustCenter[lNeighbour]
        else:
            distL[minP2_index] = float('inf')

        rNeighbour = None
        for i in range(minP2_index+1, len(data)):
            if not ignorePoint[i]:
                rNeighbour = i
                break
        if rNeighbour:
            distL[rNeighbour] = MclustCenter[rNeighbour] - MclustCenter[minP2_index]
            distR[minP2_index]= MclustCenter[rNeighbour] - MclustCenter[minP2_index]
        else:
            distR[minP2_index] = float('inf')

        if lNeighbour == rNeighbour == None:
            print("Maybe end. lNeighbour=rNeighbour=None")

    
    dumpIteration()
    return nodes[minP2_index]
