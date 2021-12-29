from graphics import *
from math import *
import time

#Класс задания точки
class point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

#Класс вершины
class vertex:
    def __init__(self, x, y, z):
        self.worldcoord = point(x, y, z)
        #Будущие экранные координаты
        self.pX = None
        self.pY = None
    
    def setscreencoord(self, view_p, c1, c2, dist):
        #Углы в радианах
        temp = atan(1.0)/45.0
        th = view_p.y*temp
        ph = view_p.z*temp
        costh = cos(th); sinth = sin(th)
        cosph = cos(ph); sinph = sin(ph)
        #Элементы марицы V
        v11 = -sinth; v12 = -cosph*costh; v13 = -sinph*costh
        v21 = costh; v22 = -cosph*sinth; v23= -sinph*sinth
        v32 = sinph; v33 = -cosph
        v43 = view_p.x   
        #Видовые координаты
        xe = v11*self.worldcoord.x + v21*self.worldcoord.y
        ye = v12*self.worldcoord.x + v22*self.worldcoord.y + v32*self.worldcoord.z
        ze = v13*self.worldcoord.x + v23*self.worldcoord.y + v33*self.worldcoord.z + v43
        #Экранные координаты
        self.pX = dist*xe/ze + c1
        self.pY = dist*ye/ze + c2
        
#Ребра
class edge:
    def __init__(self, start, end):
        #Экранные координаты начальной и конечной точки ребра
        self.s_x = start.pX
        self.s_y = start.pY
        self.e_x = end.pX
        self.e_y = end.pY
        
    #Отрисовка ребра
    def drawedge(self, win):
        obj = Line(Point(self.s_x, self.s_y), Point(self.e_x, self.e_y))
        obj.setOutline("blue")
        obj.draw(win)

class surface:
    def __init__(self):
        #Список верштн
        self.vlist = []
        #Список ребер
        self.elist = []
        
    def load(self, file_name):
        with open(file_name, 'r') as f:
            v_n = int(f.readline())
            for i in range(v_n):
                line = f.readline().split()
                x = float(line[0])
                y = float(line[1])
                z = float(line[2])
                self.vlist.append(vertex(x, y, z))
            e_n = int(f.readline())
            for i in range(e_n):
                line = f.readline().split()
                e1 = int(line[0])
                e2 = int(line[1])
                self.elist.append([e1, e2])
    #Задание точки наблюдения          
    def setviewpoint(self, ro, teta, fi):
        self.viewpoint = point(ro, teta, fi)
    
    #Прорисовка тела
    def drawsurface(self, c1, c2, dist, win):
        #Высчитываем экранные координаты
        for i in range(len(self.vlist)):
            self.vlist[i].setscreencoord(self.viewpoint, c1, c2, dist)
        #Соотносим ребра с их координатами
        for i in range(len(self.elist)):
            self.elist[i] 
            e = edge(self.vlist[self.elist[i][0]-1], self.vlist[self.elist[i][1]-1])
            e.drawedge(win)

def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()
 
win = GraphWin("Каркасные модели", 500, 500) 
P1 = 0.3
P2 = 80
s1 = surface()
s1.load('myobject.dat')
s2 = surface()
s2.load('description_cube.dat')
for i in range(10):
    s1.setviewpoint(100, P1, P2)
    s2.setviewpoint(100, P1, P2)
    s1.drawsurface(150, 150, 3000, win)
    s2.drawsurface(350, 350, 3000, win)
    P1 = P1 + 0.5
    P2 = P2 + 5
    time.sleep(1)
    clear(win)
win.getMouse()
win.close() 
