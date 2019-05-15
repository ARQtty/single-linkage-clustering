from tkinter import Tk, Canvas, Frame, BOTH
import math
import queue

stdSize = (600, 300)


class TreeVisualizer(Frame):
  
    def __init__(self, parentWindow, tree, size=stdSize):
        Frame.__init__(self, parentWindow)   
        self.parentWindow = parentWindow       
        self.width = size[0]
        self.height = size[1]
        self.initUI()

        # Один Node - корень дерева кластеров (Для построения сверху вниз)
        # Этот объект возвращается моделью классификатора.
        # Рисовать удобнее снизу вверз, поэтому данные предварительно конвертируются
        self.tree = tree
        self.convertTreeToNodes()
        
        self.draw()


    def initUI(self):
        self.parentWindow.title("Agglomerative hierarchical single-linkage clustering")        
        self.pack(fill=BOTH, expand=1)


    def draw(self):
        # Отрисовывает дерево на canvas
        
        canvas = Canvas(self)

        # Константы системы координат по Х
        leastP = self.points[0].value
        maxP = self.points[-1].value
        margin = 0.05
        absLenX = self.width*(1 - margin)
        locLenX = maxP - leastP
        # Константы СК по Y
        absLenY = self.height
        log = math.log1p
        dy = 10
        p = self.points[0]
        while p.parent:
            p = p.parent
        locLenY =int(p.level)+1
        k = absLenY*(1 - 2*margin) / log(locLenY)

        
        # Конвертеры системы координат
        def loc2absX(x):
            return int(absLenX/locLenX * (x - leastP)) + self.width*(margin/2)

        def loc2absY(level):
            if level == 0: level = 0.1
            return absLenY - k*log(level) - 2*dy


        # Рисует исходные данные
        q = queue.Queue()
        for p in self.points:
            canvas.create_text(loc2absX(p.value), loc2absY(p.level), text=str(p.value))
            # Чтобы не класть родительскую вершину в очередь дважды, 
            # кладём вершину в очередь только при отрисовке её правого ребёнка 
            if p.level == 0 and p.parent.rChild == p:
                q.put(p.parent)

            canvas.create_line(loc2absX(p.value), loc2absY(p.level)-dy, loc2absX(p.value), loc2absY(p.parent.level)-dy)

        # Рисует дерево кластеров над данными
        while q.qsize() > 0:
            p = q.get()
            canvas.create_text(loc2absX(p.value), loc2absY(p.level), text=str(round(p.rChild.value - p.lChild.value , 2)))
            # Линия к левому ребёнку
            canvas.create_line(loc2absX(p.lChild.value), loc2absY(p.level)-dy, loc2absX(p.value), loc2absY(p.level)-dy)
            # Линия к правому ребёнку
            canvas.create_line(loc2absX(p.rChild.value), loc2absY(p.level)-dy, loc2absX(p.value), loc2absY(p.level)-dy)
            # Если вершина не является корнем
            if p.parent:
                canvas.create_line(loc2absX(p.value), loc2absY(p.level)-dy, loc2absX(p.value), loc2absY(p.parent.level)-dy)
                q.put(p.parent)

        canvas.pack(fill=BOTH, expand=1)


    def convertTreeToNodes(self):
        # Спускается от корня к листам, чтобы получить данные для удобного рисования
        # точек (для соблюдения пропорций на прямой)
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
                self.points.append(v)
                return

        getNode(self.tree)



def show(tree, wSize=stdSize):
    root = Tk()

    TreeVisualizer(root, tree, size=wSize)
    
    root.geometry("%dx%d" % wSize)
    root.mainloop()


