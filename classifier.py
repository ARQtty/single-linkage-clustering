import pqdict

class TreeNode():
    # 56 bytes
    def __init__(self, value, parent=None, lChild=None, rChild=None):
        self.value = value
        self.level = 0
        self.parent = parent
        self.lChild = lChild
        self.rChild = rChild

    def __repr__(self):
        return "<Node val=%f level=%f>" % (self.value, self.level)


def createParent(node1, node2):
    if node1.value > node2.value:
        node1, node2 = node2, node1

    avgValue = (node1.value + node2.value) / 2
    
    parent = TreeNode(avgValue)
    # Для отображения на дендрограмме
    parent.level = abs(node2.value - node1.value)
    parent.lChild = node1
    parent.rChild = node2
    node1.parent = parent
    node2.parent = parent

    return parent


def fitFast(data):
    # Total: O(nlogn)
    
    distF = lambda p1, p2: abs(p1 - p2)

    dist2next = pqdict.pqdict()
    # Установка индексов и точек
    for i in range(len(data)):
        dist2next.additem(i, data[i])

    # Установка приоритетов
    for i in range(len(data)-1):
        dist2next._heap[i].prio = dist2next._heap[i+1].value - dist2next._heap[i].value
    dist2next._heap[-1].prio = float('inf')

    # Установка соседей
    for i in range(1, len(data)-1):
        dist2next._heap[i].prev_i = i-1
        dist2next._heap[i].next_i = i+1
    dist2next._heap[0].prev_i = None
    dist2next._heap[-1].next_i= None
    if len(dist2next) > 1:
        dist2next._heap[0].next_i = 1
        dist2next._heap[-1].prev_i = len(dist2next)-2
    
    # Куча строится за O(N)
    dist2next.heapify()

    # Создание объекта дендрограммы
    nodes = [TreeNode(x) for x in data]
    clastN = len(data)

    # Делает N операций объединения, получая объединяемые элементы за O(1)
    # и восстанавливая актуальность данных за 3*logn
    while clastN != 1:

        clastN -= 1

        # Первая точка из пары ближайших друг к другу удаляется из кучи
        # Вторая копируется
        minP1 = dist2next.popitem()
        minP2 = dist2next.getitem(minP1.next_i)
        
        # Обновление дендрограммы
        nodes[minP2.key] = createParent(nodes[minP1.key], nodes[minP2.key])

        # Вторая точка остаётся как нынешнее состояние кластеризованности
        # Обновляется её приоритет в куче - расстояние до следующей точки
        newClustCenter = (minP1.value + minP2.value) / 2
        dist2next.updateitem(minP2.key, new_val=newClustCenter)
        
        # Поддержка актуальности данных
        # Dist изменилась у 2 элементов
        #   + Элемент до объединяемой пары (если он есть)
        #   + Элемент, в который объединена пара 

        # Если есть точка до, то обновить её dist2next
        if (minP1.prev_i != None) and (minP1.prev_i != float("inf")):
            dist = distF(dist2next.getitem(minP2.key).value, dist2next.getitem(minP1.prev_i).value)
            dist2next.updateitem(minP1.prev_i, new_prio=dist)
            # Перелинковать 
            dist2next.updateItemLink(minP1.prev_i, newNext=minP2.key)
            dist2next.updateItemLink(minP2.key, newPrev=minP1.prev_i)
        else:
            # Если точки нет, то ссылка на предыдущий элемент пустая
            dist2next.updateItemLink(minP2.key, newPrev=float('inf'))

        # Если есть точка после объединяемых, пересчитать расстояние до неё
        if minP2.next_i == None: 
            dist = float("inf")
        else: 
            dist = distF(newClustCenter, dist2next.getitem(minP2.next_i).value)
        # И обновить приоритет
        dist2next.updateitem(minP2.key, new_prio=dist)

    return nodes[minP2.key]
