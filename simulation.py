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
        self.pressure = 0.2
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

    def random_start(self, p):
        for r in self.roads:
            r.random_start(p)

    # Focused car
        # Car starts at
        self.roads[20].cells[6] = Voiture()
        self.roads[20].cells[6].color = (255,0,0)
        self.roads[20].cells[6].chosen = True
        self.roads[20].cells[6].lifeExpectancy = 250

        # Car's destination
        self.roads[20].cells[6].destination = (5,3)

        self.roads[20].states[-1][6] = self.roads[20].cells[6]

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

        self.age += 1

    def show_graph_start(self):
        self.w.delete("all")

        data = numpy.zeros((self.size,self.size,3), dtype=numpy.uint8)

        # for each road
        for road in self.roads:
            x = road.x
            y = road.y
            for i in range(len(road)):
                if isinstance(road.cells[i],Voiture):
                    if road.cells[i].chosen:
                        data[y, x] = road.cells[i].color
                        dr, dc = road.cells[i].destination
                    else:
                        data[y, x] = (120,120,120)
                else:
                    data[y, x] = (120,120,120)

                x += road.dx
                y += road.dy

        # for each intersection
        for inter in self.intersections:
            if len(inter)==4:

                x = inter.x-1
                y = inter.y-1

                locations = [(-1,0), (0,1), (1,0), (0,-1)]
                for i in range(len(inter)):
                    a, b = locations[i]
                    data[y+b, x+a] = (120,120,120)

            if len(inter)==3:

                x = inter.x
                y = inter.y

                locations = [(0,0), (self.roads[inter.conf[0][1]].dx,self.roads[inter.conf[0][1]].dy),
                             (self.roads[inter.conf[2][1]].dx,self.roads[inter.conf[2][1]].dy)]
                for i in range(len(inter)):
                    a, b = locations[i]
                    data[y+b, x+a] = (120,120,120)

        x = self.roads[dr].x + self.roads[dr].dx * dc
        y = self.roads[dr].y + self.roads[dr].dy * dc
        data[y, x] = (0,255,0)

        img = Image.fromarray(data)
        img = img.resize((7*self.size, 7*self.size))
        photo = ImageTk.PhotoImage(img)
        self.w.create_image(photo.width()/2,photo.height()/2,image=photo)
        self.w.update()


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
                else:
                    data[y, x] = (120,120,120)
                x += road.dx
                y += road.dy

        # for each intersection
        for inter in self.intersections:
            if len(inter)==4:

                x = inter.x-1
                y = inter.y-1

                locations = [(-1,0), (0,1), (1,0), (0,-1)]
                for i in range(len(inter)):
                    a, b = locations[i]
                    if inter.cells[i]:
                        data[y+b, x+a] = inter.cells[i][0].color
                        #self.w.create_line(x, y, x+a, y+b, width=1)
                    else:
                        data[y+b, x+a] = (120,120,120)

            if len(inter)==3:

                x = inter.x
                y = inter.y

                locations = [(0,0), (self.roads[inter.conf[0][1]].dx,self.roads[inter.conf[0][1]].dy),
                             (self.roads[inter.conf[2][1]].dx,self.roads[inter.conf[2][1]].dy)]
                for i in range(len(inter)):
                    a, b = locations[i]
                    if inter.cells[i]:
                        data[y+b, x+a] = inter.cells[i][0].color
                        #self.w.create_line(x, y, x+a, y+b, width=1)
                    else:
                        data[y+b, x+a] = (120,120,120)

        img = Image.fromarray(data)
        img = img.resize((7*self.size, 7*self.size))
        photo = ImageTk.PhotoImage(img)
        self.w.create_image(photo.width()/2,photo.height()/2,image=photo)
        self.w.update()

    def print_all(self):
        for road in self.roads:
            print(road)
        for inter in self.intersections:
            print(inter)

class Voiture:
    def __init__(self):
        self.lifeExpectancy = int(random.expovariate(0.01))
        self.color = (255,255,255)
        self.destination = None
        self.chosen = False
        while self.lifeExpectancy<30 or self.lifeExpectancy>250:
            self.lifeExpectancy = random.expovariate(0.01)
        # Random color
        #while self.color[0]==self.color[1] and self.color[1]==self.color[2]:
        #    self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

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

        # All cells in the middle
        for i in range(1,len(self)-1):
            prev = self.states[-1][i-1]
            cur = self.states[-1][i]
            nex = self.states[-1][i+1]
            ruling = rules[(isinstance(prev,Voiture),isinstance(cur,Voiture),isinstance(nex,Voiture))]
            if ruling == 'next':
                self.cells[i] = prev
                if i == 1:
                    self.cells[0] = None
                # Manage life expectancy
                self.cells[i].lifeExpectancy -= 1
                if self.cells[i].lifeExpectancy == 0:
                    self.cells[i] = None
            elif ruling == 'empty':
                self.cells[i] = None
            if isinstance(self.cells[i], Voiture) and self.cells[i].chosen:
                dr, dc = self.cells[i].destination
                if dc == i and dr == self.simul.roads.index(self):
                    print("Goal !")


        # Last cell
        prev = cur
        cur = nex
        if isinstance(prev,Voiture) and not isinstance(cur,Voiture):
            self.cells[-1] = prev
            # Manage life expectancy
            self.cells[-1].lifeExpectancy -= 1
            if self.cells[-1].lifeExpectancy == 0:
                self.cells[-1] = None
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

# Type Of Cell
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
        self.field_I = 0
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
                    if self.simul.roads[self.conf[i][1]].cells[0] == None:
                        self.simul.roads[self.conf[i][1]].cells[0] = cur[0]
                        #Manage life expectancy
                        self.simul.roads[self.conf[i][1]].cells[0].lifeExpectancy -=1
                        if self.simul.roads[self.conf[i][1]].cells[0].lifeExpectancy == 0:
                            self.simul.roads[self.conf[i][1]].cells[0] = None
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
                    #Manage life expectancy
                    if self.cells[len(self)-i] != None:
                        self.cells[len(self)-i][0].lifeExpectancy -= 1
                        if self.cells[len(self)-i][0].lifeExpectancy == 0:
                            self.cells[len(self)-i] = None
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
                        self.cells[i][0].lifeExpectancy -= 1
                        if self.cells[i][0].lifeExpectancy == 0:
                            self.cells[i] = None
                    elif ruling == 'empty':
                        self.cells[i] = None

        #update the intensity of the field
        self.field_I = saturation*5


    def next_step(self):

        self.next_step_in()

        # Cars enter the intersection if they can
        for ind in self.entrances:
            # if the cell of entrance from this road is free and there is a car waiting, let the car in
            if self.cells[ind] == None and isinstance(self.simul.roads[self.conf[ind][1]].cells[-1], Voiture):
                # if the car is the interesting one it chooses it's direction with the potential field
                if self.simul.roads[self.conf[ind][1]].cells[-1].chosen:
                    potentials = []
                    dr, dc = self.simul.roads[self.conf[ind][1]].cells[-1].destination
                    for w in self.waysout:
                        x = self.x + self.simul.roads[self.conf[w][1]].dx
                        y = self.y + self.simul.roads[self.conf[w][1]].dy
                        P = 0
                        for i in self.simul.intersections:
                             d2 = (x-i.x)**2 + (y-i.y)**2
                             P += -i.field_I/d2

                        dx = self.simul.roads[dr].x + self.simul.roads[dr].dx * dc
                        dy = self.simul.roads[dr].y + self.simul.roads[dr].dy * dc
                        P += 100000/((x-dx)**2 + (y-dy)**2)
                        potentials.append((P,w))
                    potentials.sort(key=lambda l: -l[0])
                    self.cells[ind] = (self.simul.roads[self.conf[ind][1]].cells[-1], potentials[0][1])
                    self.simul.roads[self.conf[ind][1]].cells[-1] = None
                else:
                    wayout = random.randint(0,len(self.waysout)-1)
                    self.cells[ind] = (self.simul.roads[self.conf[ind][1]].cells[-1], self.waysout[wayout])
                    self.cells[ind][0].lifeExpectancy -= 1
                    if self.cells[ind][0].lifeExpectancy == 0:
                        self.cells[ind] = None
                    self.simul.roads[self.conf[ind][1]].cells[-1] = None

        # Copy to the state list
        self.states.append(self.cells[:])

def potential_at_mouse(event):
    x,y = event.x/7,event.y/7
    P = 0
    for i in simulation.intersections:
        d2 = (x-i.x)**2 + (y-i.y)**2
        P += -i.field_I/d2
    print(P)

master.bind('<Button>',potential_at_mouse)

# Choose a car change it's color to red and pick a destination
def choose_car(simulation):
    #randomly pick a car
    r = random.randint(0,len(simulation.roads)-1)
    c = random.randint(0,len(simulation.roads[r].cells)-1)
    while simulation.roads[r].cells[c] == None or r in simulation.exits:
        c = random.randint(0,len(simulation.roads[r].cells)-1)

    #randomly pick a destination
    dr = random.randint(0,len(simulation.roads)-1)
    dc = random.randint(0,len(simulation.roads[r].cells)-1)
    if dr in simulation.entrances:
        dr = random.randint(0,len(simulation.roads)-1)
        dc = random.randint(0,len(simulation.roads[r].cells)-1)
    # Give the car it's destination
    simulation.roads[r].cells[c].destination = (dr,dc)
    # Red car
    simulation.roads[r].cells[c].color = (255,0,0)
    simulation.roads[r].cells[c].chosen = True
    simulation.roads[r].cells[c].lifeExpectancy = 250

"""
simulation = Simulation(700, 700, 23)


# 4 way intersection

simulation.add_road(10,1,0, 0,11)
simulation.add_road(10,0,-1, 11, 22)
simulation.add_road(10,1,0, 13, 11)
simulation.add_road(10,0,-1, 11, 10)

branches = [(TOC.In,0), (TOC.In,1), (TOC.Out,2), (TOC.Out,3)]
simulation.add_intersection(branches, 12, 12)
"""

""" 
# 3 way intersection

simulation.add_road(10,1,0, 0,11)
simulation.add_road(10,0,-1, 11, 22)
simulation.add_road(10,0,-1, 11, 10)

branches = [(TOC.In,0), (TOC.In,1), (TOC.No,None), (TOC.Out,2)]
simulation.add_intersection(branches, 12, 12)

"""

city_map = { 'roads': [(10,1,0,0,11), (10,1,0,13,11), (10,1,0,26,11), (10,1,0,39,11), (10,1,0,52,11), (10,1,0,65,11), # 6
                     (10,1,0,26,24), # 1
                     (10,-1,0,9,37), (10,-1,0,22,37), (10,-1,0,35,37), (10,-1,0,48,37), (10,-1,0,61,37), (10,-1,0,74,37), # 6
                     (10,1,0,39,50), (10,1,0,52,50), # 2
                     (10,-1,0,9,63), (10,-1,0,22,63), (10,-1,0,35,63), # 3
                     (10,1,0,0,76), (10,1,0,13,76), (10,1,0,26,76), (10,1,0,39,76), (10,1,0,52,76), (10,1,0,65,76), # 6
                     # Vertical
                     (10,0,-1,11,9), (23,0,-1,11,35), (23,0,-1,11,61), (10,0,-1,11,74), (10,0,-1,11,87), # 5
                     (10,0,1,24,0), (10,0,1,24,13), (10,0,1,24,26), (23,0,1,24,39), (10,0,1,24,65), (10,0,1,24,78), # 6
                     (10,0,-1,37,10),(10,0,-1,37,22),(10,0,-1,37,35), (10,0,-1,37,48), (10,0,-1,37,61), (10,0,-1,37,74), (10,0,-1,37,87), # 7
                     (10,0,1,50,0), (23,0,1,50,13), (10,0,1,50,39), (23,0,1,50,52), # 4
                     (10,0,-1,63,10), (23,0,-1,63,35), (10,0,-1,63,48), (23,0,-1,63,74), (10,0,-1,63,87)], # 5

             'intersections': [([(TOC.In,0), (TOC.In,25), (TOC.Out,1), (TOC.Out,24)],(12,12)),
                             ([(TOC.In,1), (TOC.Out,30), (TOC.Out,2), (TOC.In,29)],(25,12)),
                             ([(TOC.In,2), (TOC.In,36), (TOC.Out,3), (TOC.Out,35)],(38,12)),
                             ([(TOC.In,3), (TOC.Out,43), (TOC.Out,4), (TOC.In,42)],(51,12)),
                             ([(TOC.In,4), (TOC.In,47), (TOC.Out,5), (TOC.Out,46)],(64,12)),
                             
                             ([(TOC.No,None), (TOC.Out,31), (TOC.Out,6), (TOC.In,30)],(25,25)),
                             ([(TOC.In,6), (TOC.In,37), (TOC.No,None), (TOC.Out,36)],(38,25)),
                             
                             ([(TOC.Out,7), (TOC.In,26), (TOC.In,8), (TOC.Out,25)],(12,38)),
                             ([(TOC.Out,8), (TOC.Out,32), (TOC.In,9), (TOC.In,31)],(25,38)),
                             ([(TOC.Out,9), (TOC.In,38), (TOC.In,10), (TOC.Out,37)],(38,38)),
                             ([(TOC.Out,10), (TOC.Out,44), (TOC.In,11), (TOC.In,43)],(51,38)),
                             ([(TOC.Out,11), (TOC.In,48), (TOC.In,12), (TOC.Out,47)],(64,38)),
                             
                             ([(TOC.No,None), (TOC.In,39), (TOC.Out,13), (TOC.Out,38)],(38,51)),
                             ([(TOC.In,13), (TOC.Out,45), (TOC.Out,14), (TOC.In,44)],(51,51)),
                             ([(TOC.In,14), (TOC.In,49), (TOC.No,None), (TOC.Out,48)],(64,51)),
                             
                             ([(TOC.Out,15), (TOC.In,27), (TOC.In,16), (TOC.Out,26)],(12,64)),
                             ([(TOC.Out,16), (TOC.Out,33), (TOC.In,17), (TOC.In,32)],(25,64)),
                             ([(TOC.Out,17), (TOC.In,40), (TOC.No,None), (TOC.Out,39)],(38,64)),
                             
                             ([(TOC.In,18), (TOC.In,28), (TOC.Out,19), (TOC.Out,27)],(12,77)),
                             ([(TOC.In,19), (TOC.Out,34), (TOC.Out,20), (TOC.In,33)],(25,77)),
                             ([(TOC.In,20), (TOC.In,41), (TOC.Out,21), (TOC.Out,40)],(38,77)),
                             ([(TOC.In,21), (TOC.No,None), (TOC.Out,22), (TOC.In,45)],(51,77)),
                             ([(TOC.In,22), (TOC.In,50), (TOC.Out,23), (TOC.Out,49)],(64,77))
                             ],
             'size': 90}

simulation = Simulation(700,700,city_map['size'])

for r in city_map['roads']:
    simulation.add_road(r[0],r[1],r[2],r[3],r[4])

for i in city_map['intersections']:
    simulation.add_intersection(i[0],i[1][0],i[1][1])

simulation.random_start(0.45)

# Choose a car randomly
choose_car(simulation)

# Show the chosen car in red and it's destination in green for 3 seconds
simulation.show_graph_start()
time.sleep(3)

for _ in range(200):
    simulation.next_step()
    simulation.show_graph()
    time.sleep(0.3)

