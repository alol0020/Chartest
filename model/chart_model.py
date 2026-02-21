from math import floor

from db.db import db_get_chart, db_get_refpoints


class ChartModel:
    def __init__(self):
        self.data = []
        self.refs = []

        self.currentSelection = []
        self.view = []

        self.center = None
        self.width = None
        self.height = None

        self.max_width = None
        self.max_height = None
        self.aspect = None

        self.frame_size = [None,None]


    def getX0(self):
        return max(self.center[0] - self.width // 2, 0)

    def getX1(self):
        return min(self.center[0] + self.width // 2, self.max_width)

    def getY0(self):
        return max(self.center[1] - self.height // 2, 0)

    def getY1(self):
        return min(self.center[1] + self.height // 2, self.max_height)

    def reset(self,w,h):
        self.center = [w//2,h//2]
        self.width = w
        self.height = h

        self.max_width = w
        self.max_height = h
        self.aspect = h/w

    def refresh(self):
        x0, x1 = self.getX0(), self.getX1()
        y0, y1 = self.getY0(), self.getY1()

        self.view = self.data[y0:y1, x0:x1].copy()

    def setHeight(self, h):
        self.height =min(max(h,0),self.max_height)
    def setWidht(self,w):
        self.width =min(max(w,0),self.max_width)

    def setCenter(self,c):
        x,y = c
        x=floor(x)
        y =floor(y)

        x = min(max(x,self.width//2),self.max_width-self.width//2)
        y = min(max(y,self.height//2),self.max_height-self.height//2)
        self.center=[x,y]





