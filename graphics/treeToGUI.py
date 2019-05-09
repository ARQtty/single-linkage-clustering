def depthOfChildren(v, currDepth=0):
    lDepth = 0
    rDepth = 0

    if v.lChild:
        lDepth = max(depthOfChildren(v.lChild, currDepth)) + 1
    if v.rChild:
        rDepth = max(depthOfChildren(v.rChild, currDepth)) + 1

    return (lDepth, rDepth)


def depthOfNode(searchV, treeV):

    if searchV == treeV:
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






# GUI

from tkinter import Tk, Canvas, Frame, BOTH
import queue

class Example(Frame):
  
    def __init__(self, parent, tree=None, points=None):
        Frame.__init__(self, parent)   
        self.parent = parent        
        self.initUI()

        self.tree = tree  # Node with ierarchial relations (building from top to bottom)
        self.points = points    # Array of Nodes  (building from bottom to top)
        if tree:
            self.maxDepth = max(depthOfChildren(self.tree))
        self.draw()


    def initUI(self):
        self.parent.title("tree")        
        self.pack(fill=BOTH, expand=1)


    def draw(self):
        if self.points == None:
            if self.tree != None:
                self.convertTreeToNodes()
                self.drawByNodes()
            else:
                raise Exception("Ошибка данных. Не предоставлено ни списка точек-кластеров, ни дерева")
        else:
            self.drawByNodes()


    def drawByNodes(self):
        canvas = Canvas(self)
        leastP = self.points[0].value
        maxP = self.points[-1].value
        dy = 10

        def loc2absX(x):
            absLenX = wv *0.9
            locLenX = maxP - leastP 
            return int(absLenX/locLenX * (x - leastP + 0.5))

        def loc2absY(level):
            absLenY = wh
            locLenY = 1
            p = self.points[0]
            while p.parent:
                p = p.parent
            locLenY = max(depthOfChildren(p))+1
            return absLenY - int(absLenY/locLenY * (level)) - 2*dy

        # Draw points
        q = queue.Queue()
        for p in self.points:
            canvas.create_text(loc2absX(p.value), loc2absY(p.level), text=str(p.value))
            if p.parent.level == 1:
                q.put(p.parent) # ДА, КЛАДЁММ ДВАЖДЫ
            canvas.create_line(loc2absX(p.value), loc2absY(p.level)-dy, loc2absX(p.value), loc2absY(p.parent.level)-dy)

        # Draw parents
        while q.qsize() > 0:
            p = q.get()
            canvas.create_text(loc2absX(p.value), loc2absY(p.level), text=str(p.value))
            canvas.create_line(loc2absX(p.lChild.value), loc2absY(p.level)-dy, loc2absX(p.value), loc2absY(p.level)-dy) # horizontal left
            canvas.create_line(loc2absX(p.rChild.value), loc2absY(p.level)-dy, loc2absX(p.value), loc2absY(p.level)-dy) # horizontal right
            # Not a root
            if p.parent:
                canvas.create_line(loc2absX(p.value), loc2absY(p.level)-dy, loc2absX(p.value), loc2absY(p.parent.level)-dy)
                q.put(p.parent)

        canvas.pack(fill=BOTH, expand=1)


    def convertTreeToNodes(self):
        self.points = []

        
        def getNode(v):
            if v.lChild:
                getNode(v.lChild)
            else:
                self.points.append(v)
                return

            if v.rChild:
                getNode(v.rChild)
            else:
                print("add p ", v.value)
                self.points.append(v)
                return

        getNode(self.tree)



 
if __name__ == '__main__':
    wv = 1500
    wh = 600



    # Data creating
    from random import randint
    nodes = [Node(randint(-30, 30)) for x in range(30)]
    #nodes = [Node(x) for x in [2,3,6,9,10,11,12, 16, 20]]
    n23 = createParent(nodes[0], nodes[1])
    n236 = createParent(n23, nodes[2])
    n910 = createParent(nodes[3], nodes[4])
    n1112 = createParent(nodes[5], nodes[6])
    n9101112 = createParent(n910, n1112)
    tree = createParent(n236, n9101112)
    


    # Clastering
    clastered = [x for x in nodes] # copy
    
    groupOperationsN = 0
    while groupOperationsN != len(nodes)-1:
        #clastering
        closestDist = float('inf')
        closestP1_index = None
        closestP2_index = None
        distF = lambda p1, p2: abs(p1.value - p2.value)
        
        for i, p1 in enumerate(clastered):
            for j, p2 in enumerate(clastered):
                if p1 != p2 and distF(p1, p2) < closestDist:
                    closestP1_index = i
                    closestP2_index = j
                    closestDist = distF(p1, p2)
        
        # Нашли ближайшие кластеры. Объединяем
        newClast = createParent(clastered[closestP1_index], clastered[closestP2_index])
        # print(clastered)
        if closestP1_index > closestP2_index:
            closestP1_index, closestP2_index = closestP2_index, closestP1_index
        # Выкинем две точки, которые объединили
        clastered = clastered[:closestP1_index] + clastered[closestP1_index+1:closestP2_index] + clastered[closestP2_index+1:]
        # Закинем точку-новый_кластер
        clastered.append(newClast)
        
        groupOperationsN += 1



    # GUI init
    root = Tk()
    #ex = Example(root, points=nodes)
    ex = Example(root, tree=clastered[0])
    root.geometry("%dx%d" % (wv, wh))
    root.mainloop()