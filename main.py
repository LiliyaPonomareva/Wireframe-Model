# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 18:52:07 2021

@author: lilyp_032u5e1
"""
from graphics import *
from math import *
import time

class point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class vertex:
    def __init__(self, x, y, z):
        self.worldcoord = point(x, y, z)
        self.pX = None
        self.pY = None
    
    def setscreencoord(self, view_p, c1, c2, dist):
        #углы в радианах
        temp = atan(1.0)/45.0
        th = view_p.y*temp
        ph = view_p.z*temp
        costh = cos(th); sinth = sin(th)
        cosph = cos(ph); sinph = sin(ph)
        #элементы марицы V
        v11 = -sinth; v12 = -cosph*costh; v13 = -sinph*costh
        v21 = costh; v22 = -cosph*sinth; v23= -sinph*sinth
        v32 = sinph; v33 = -cosph
        v43 = view_p.x   
        #видовые координаты
        xe = v11*self.worldcoord.x + v21*self.worldcoord.y
        ye = v12*self.worldcoord.x + v22*self.worldcoord.y + v32*self.worldcoord.z
        ze = v13*self.worldcoord.x + v23*self.worldcoord.y + v33*self.worldcoord.z + v43
        self.pX = dist*xe/ze + c1
        self.pY = dist*ye/ze + c2
        
        
class edge:
    def __init__(self, start, end):
        self.s_x = start.pX
        self.s_y = start.pY
        self.e_x = end.pX
        self.e_y = end.pY
        
    def drawedge(self, win):
        obj = Line(Point(self.s_x, self.s_y), Point(self.e_x, self.e_y))
        obj.setOutline("blue")
        obj.draw(win)

class surface:
    def __init__(self):
        self.vlist = []
        self.elist = []
        
    def load(self):
        #with open('description_cube.dat', 'r') as f:
        with open('myobject.dat', 'r') as f:
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
                
    def setviewpoint(self, ro, teta, fi):
        self.viewpoint = point(ro, teta, fi)
        
    def drawsurface(self, c1, c2, dist, win):
        for i in range(len(self.vlist)):
            self.vlist[i].setscreencoord(self.viewpoint, c1, c2, dist)
        for i in range(len(self.elist)):
            self.elist[i] 
            e = edge(self.vlist[self.elist[i][0]-1], self.vlist[self.elist[i][1]-1])
            e.drawedge(win)

def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()
 
win = GraphWin("Окно для графики", 500, 500) 
P1 = 0.3
P2 = 80
s1 = surface()
s1.load()
for i in range(10):
    s1.setviewpoint(100, P1, P2)
    s1.drawsurface(250, 250, 3000, win)
    P1 = P1 + 0.5
    P2 = P2 + 5
    time.sleep(2)
    clear(win)
win.getMouse()
win.close() 