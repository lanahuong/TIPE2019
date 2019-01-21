from tkinter import *
#from tkinter.ttk import *
import random, time
from enum import Enum
import numpy
from PIL import Image, ImageTk

master = Tk()

class Simulation:
    def __init__(self, width, height, size):
        self.roads = []
        self.intersections = []
        self.entrances = []
        self.exits = []
        self.pressure = 0.8
        self.size = size
        self.w = Canvas(master, width=width, height=height)
        self.w.pack()

    def __repr__(self):
        string = "Roads : "+str(self.roads)+"\n"
        string += "Intersections : "+str(self.intersections)+"\n"
        string += "Entrances : "+str(self.entrances)+"\n"
        string += "Exits : "+str(self.exits)+"\n"
        return string

    def add_road(self,length,dx,dy, x, y):
        self.roads.append(Road(self, length,dx,dy,x,y))
        self.entrances.append(len(self.roads)-1)
        self.exits.append(len(self.roads)-1)

    def add_intersection(self, branches, x, y):
        self.intersections.append(Intersection(self, branches, x, y))
        for b in branches:
            if b[0] == TOC.In:
                self.exits.remove(b[1])
            elif b[0] == TOC.Out:
                self.entrances.remove(b[1])

    def next_step(self):
        # move cars in intersections
        for inter in self.intersections:
            inter.next_step()
        # then move cars in streets
        for road in self.roads:
            road.next_step()
        # then populate entrances of the city
        for e in self.entrances:
            if self.roads[e].cells[0] is None:
                self.roads[e].cells[0] = random_car(self.pressure)
                self.roads[e].states[-1][0] = self.roads[e].cells[0]
        # then empty exits of roads
        for e in self.exits:
            if self.roads[e]:
                self.roads[e].cells[-1] = None

    def make_city(self, city):
        return


    def show_graph(self):
        self.w.delete("all")
        data = numpy.zeros((self.size,self.size,3), dtype=numpy.uint8)
        img = Image.fromarray(data)
        img = img.resize((10*self.size, 10*self.size))
        #img.show()
        # for each road
        for road in self.roads:
            x = road.x
            y = road.y
            for i in range(len(road)):
                if isinstance(road.cells[i],Voiture):
                    data[y, x] = road.cells[i].color
                    #self.w.create_line(x, y, x+road.dx, y+road.dy, width=1)
                x += road.dx
                y += road.dy

        # for each intersection
        for inter in self.intersections:
            if len(inter)==4:

                x = inter.x-1
                y = inter.y-1

                locations = [(-1,0), (0,1), (1,0), (0,-1)]
                for i in range(len(inter)):
                    if inter.cells[i]:
                        a, b = locations[i]
                        data[y+b, x+a] = inter.cells[i][0].color
                        #self.w.create_line(x, y, x+a, y+b, width=1)

            if len(inter)==3:

                x = inter.x
                y = inter.y

                locations = [(0,0), (self.roads[inter.conf[0][1]].dx,self.roads[inter.conf[0][1]].dy),
                             (self.roads[inter.conf[2][1]].dx,self.roads[inter.conf[2][1]].dy)]
                for i in range(len(inter)):
                    if inter.cells[i]:
                        a, b = locations[i]
                        data[y+b, x+a] = inter.cells[i][0].color
                        #self.w.create_line(x, y, x+a, y+b, width=1)

        img = Image.fromarray(data)
        img = img.resize((10*self.size, 10*self.size))
        photo = ImageTk.PhotoImage(img)
        self.w.create_image(photo.width()/2,photo.height()/2,image=photo)
        self.w.update()
        time.sleep(0.5)

    def print_all(self):
        for road in self.roads:
            print(road)
        for inter in self.intersections:
            print(inter)

class Voiture:
    def __init__(self):
        self.speed = 1
        self.color = (0,0,0)
        while self.color[0]==self.color[1] and self.color[1]==self.color[2]:
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def __repr__(self):
        return str(1)

def random_car(p):
    output = random.random()
    if output<p:
        return Voiture()
    return None

rules = {(True,True,True):'stay',
            (True,True,False):'empty',
            (True,False,True):'next',
            (True,False,False):'next',
            (False,True,True):'stay',
            (False,True,False):'empty',
            (False,False,True):'empty',
            (False,False,False):'empty'}

class Road:
    def __init__(self, simul, length, dx, dy, x, y):
        self.simul = simul
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.cells = [None for _ in range(length)]
        self.states = [self.cells[:]]

    def random_start(self, p):
        self.cells = [random_car(p) for _ in range(len(self))]
        self.states = [self.cells[:]]

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        string = str(self.cells)
        return string

    def age(self):
        return len(self.states)

    def next_step(self):
        # 1st cell
        #if not isinstance(self.cells[0], Voiture):
        #    self.cells[0] = random_car(0.8)
        #elif not isinstance(self.cells[1], Voiture):
        #    self.cells[0] = None

        # All all cells in the middle
        for i in range(1,len(self)-1):
            prev = self.states[-1][i-1]
            cur = self.states[-1][i]
            nex = self.states[-1][i+1]
            ruling = rules[(isinstance(prev,Voiture),isinstance(cur,Voiture),isinstance(nex,Voiture))]
            if ruling == 'next':
                self.cells[i] = prev
                if i == 1:
                    self.cells[0] = None
            elif ruling == 'empty':
                self.cells[i] = None


        # Last cell
        prev = cur
        cur = nex
        if isinstance(prev,Voiture) and not isinstance(cur,Voiture):
            self.cells[-1] = prev
        #elif isinstance(nex,Voiture):
        #    self.cells[-1] = None

        # Copy to the state list
        self.states.append(self.cells[:])

    def time_graph(self, w):
        size = 3
        x = 5
        y = 5
        for i in range(self.age()):
            for j in range(len(self)):
                if isinstance(self.states[i][j],Voiture):
                    w.create_line(x, y, x+size, y, width=size)
                x += size
            y += size
            x = 5

    def animate(self, w):
        size = 5
        x = 5
        y = 5
        for i in range(self.age()):
            w.delete('all')
            for j in range(len(self)):
                if isinstance(self.states[i][j],Voiture):
                    w.create_line(x, y, x+size, y, width=size)
                x += size
            x = 5
            w.update()
            time.sleep(0.03)

class TOC(Enum):
    No = 0
    In = 1
    Out = 2

# branches [(type_of_cell, index_in_road_list) ...]
# cells = [(Voiture, Out) or None]

class Intersection:
    def __init__(self, simul, branches, x, y):
        self.simul = simul
        self.conf = branches
        self.cells = [None for _ in range(len(branches))]
        self.states = [list(self.cells)]
        self.x = x
        self.y = y
        self.cars_stopped = []
        self.entrances = []
        self.waysout = []
        for i in range(len(branches)):
            if branches[i][0] == TOC.In:
                self.entrances.append(i)
            elif branches[i][0] == TOC.Out:
                self.waysout.append(i)

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        string = str(self.cells)
        return string

    def age(self):
        return len(self.states)

    def next_step_in(self):
        saturation = 0
        # Cars who want to and can leave do so else they stop and calculate saturation
        for i in range(len(self)):
            prev = self.states[-1][i-1]
            cur = self.states[-1][i]
            nex = self.states[-1][(i+1)%len(self)]
            if cur != None:
                saturation += 1
                if cur[1] == i:
                # if the road's entrance is free, speak friend and enter
                    self.simul.roads[self.conf[i][1]].cells[0] = cur[0]
                    self.cells[i] = None
                    saturation -= 1
                # else don't move
        # adjust the saturation to avoid issues in 3 way intersections
        # ie : cars from one road are completely blocked
        saturation += sum([int(w[0]==TOC.No) for w in self.conf])
        copy_current_state = list(self.cells)
        # if the intersection is saturated and no car is stopped -> carroussel style
        if saturation == len(self):
            if self.cars_stopped == []:
                last = self.cells[-1]
                for i in range(1,len(self)):
                    self.cells[len(self)-i] = self.cells[len(self)-1-i]
                self.cells[0] = last

        # if the intersection is not saturated, move normally
        else:
            for i in range(len(self)):
                prev = copy_current_state[i-1]
                cur = copy_current_state[i]
                nex = copy_current_state[(i+1)%len(self)]
                # if the car is not stopped move normally else don't do anything
                if not (cur in self.cars_stopped) :
                    ruling = rules[((prev != None),(cur != None),(nex != None))]
                    if ruling == 'next':
                        self.cells[i] = prev
                    elif ruling == 'empty':
                        self.cells[i] = None


    def next_step(self):

        self.next_step_in()

        # Cars enter the intersection if they can
        for ind in self.entrances:
            # if the cell of entrance from this road is free and there is a car waiting, let the car in
            if self.cells[ind] == None and isinstance(self.simul.roads[self.conf[ind][1]].cells[-1], Voiture):
                wayout = random.randint(0,len(self.waysout)-1)
                self.cells[ind] = (self.simul.roads[self.conf[ind][1]].cells[-1], self.waysout[wayout])
                self.simul.roads[self.conf[ind][1]].cells[-1] = None

        # Copy to the state list
        self.states.append(self.cells[:])

simulation = Simulation(700, 700, 23)

simulation.add_road(10,1,0, 0,11)
simulation.add_road(10,0,-1, 11, 22)
#simulation.add_road(10,1,0, 13, 11)
simulation.add_road(10,0,-1, 11, 10)
"""
city_map = { roads: [(10,1,0), (10,1,0), (10,1,0), (11,1,0), (10,1,0), (10,1,0), # 6
                     (10,1,0), # 1
                     (10,-1,0), (10,-1,0), (10,-1,0), (10,-1,0), (10,-1,0), (10,-1,0), # 6
                     (10,1,0), (10,1,0), # 2
                     (10,-1,0), (10,-1,0), (10,-1,0), # 3
                     (10,1,0), (10,1,0), (10,1,0), (11,1,0), (10,1,0), (10,1,0), # 6
                     # Vertical
                     (10,0,-1), (24,0,-1), (24,0,-1), (10,0,-1), (10,0,-1), # 5
                     (10,0,1), (11,0,1), (10,0,1), (24,0,1), (10,0,1), (10,0,1), # 6
                     (10,0,-1),(11,0,-1),(10,0,-1), (11,0,-1), (10,0,-1), (10,0,-1), # 6
                     (10,0,1), (24,0,1), (10,0,1), (24,0,1), # 4
                     (10,0,-1), (24,0,-1), (10,0,-1), (24,0,-1), (10,0,-1)], # 5

             intersections: [[(TOC.In,0), (TOC.In,20), (TOC.Out,1), (TOC.Out,19)],
                             [(TOC.In,1), (TOC.Out,25), (TOC.Out,2), (TOC.In,24)]],
             size: 75}"""

# Size of the city : 6*10 + 3*5 = 75

branches = [(TOC.In,0), (TOC.In,1), (TOC.No,None), (TOC.Out,2)]
simulation.add_intersection(branches, 12, 12)

print(simulation)

for _ in range(50):
    simulation.next_step()
    simulation.show_graph()

