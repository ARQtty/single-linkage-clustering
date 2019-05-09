from tkinter import Tk, Canvas, Frame, BOTH
import queue

from graphics import treeMethods


stdSize = (600, 300)


class TreeVisualizer(Frame):
  
    def __init__(self, parentWindow, tree=None, points=None, size=stdSize):
        Frame.__init__(self, parentWindow)   
        self.parentWindow = parentWindow       
        self.width = size[0]
        self.height = size[1]
        self.initUI()

        # Один Node - корень дерева кластеров (Для построения от верха вниз)
        # Такой объект возвращает модель классификатора. 
        self.tree = tree
        if tree:
            self.maxDepth = max(treeMethods.depthOfChildren(self.tree))

        # Массив Node-ов  (Для построения дерева снизу вверх)
        # Рисуется по этому формату данных. 
        # Переделать
        self.points = points
        
        self.draw()


    def initUI(self):
        self.parentWindow.title("Agglomerative hierarchical single-linkage clustering")        
        self.pack(fill=BOTH, expand=1)


    def draw(self):
        # Приведение возможных типов входных данных к единому виду для отрисовки
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
            margin = 0.05
            absLenX = self.width*(1 - margin)
            locLenX = maxP - leastP
            return int(absLenX/locLenX * (x - leastP)) + self.width*(margin/2)

        def loc2absY(level):
            absLenY = self.height
            locLenY = 1
            p = self.points[0]
            while p.parent:
                p = p.parent
            locLenY = max(treeMethods.depthOfChildren(p))+1
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



def show(tree=None, points=None, wSize=stdSize):
    root = Tk()
    
    if tree:
        ex = TreeVisualizer(root, tree=tree, size=wSize)
    elif points:
        ex = TreeVisualizer(root, points=points, size=wSize)
    else:
        raise Exception("Не переданы данные для визуализации")

    root.geometry("%dx%d" % wSize)
    root.mainloop()