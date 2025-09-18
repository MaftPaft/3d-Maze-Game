"""
maze game: find the target in a 3-dimensional maze (green wall as the target)
"""
from math import *
from random import randint,uniform,choice
import pygame as pg

def mazegenerator(width,height):
    # width and height must be an odd number to create a balanced maze
    if width%2==0 or height%2==0:
        raise ValueError("Width and Height must be an odd number")
    # map of 1s and 0s (currently filled with just 1s)
    m = [[1 for x in range(width)] for y in range(height)]
    # cell
    stack=[[1,1]]
    # Detect boundaries
    def notedge(x,y):
        return x>0 and x < len(m[0])-1 and y > 0 and y < len(m)-1
    # get the neigbour of the cell, two blocks next to the cell
    def get_neighbours(x,y):
        n=[]
        if notedge(x+2,y): n.append([x+2,y])
        if notedge(x-2,y): n.append([x-2,y])
        if notedge(x,y+2): n.append([x,y+2])
        if notedge(x,y-2): n.append([x,y-2])
        return n
    # place a 2
    k=True
    while stack:
        # current cell
        x,y=stack[-1]
        neighbours=get_neighbours(x,y)
        # if the neighbour cell is 1, then it is unvisited and added to the list
        unvisited=[n for n in neighbours if m[n[1]][n[0]]==1]

        if unvisited:
            # pick a random neighbour
            nx,ny=choice(unvisited)
            # get the midpoint of where the cell hopped to remove the wall
            m[(ny+y)//2][(nx+x)//2]=0
            # remove the wall the cell has hopped on
            m[ny][nx]=0
            # append to the stack
            stack.append([nx,ny])
        else:
            # places the 2 for the point the player must reach
            if k==True:
                m[y][x]=2
                k=False
            # pop to backtrack
            stack.pop()
    # returns the maze
    return m
mw,mh=33,33
MAP=mazegenerator(mw,mh)
TS=32
gx,gy=0,0
for y in range(len(MAP)):
    for x in range(len(MAP[y])):
        if MAP[y][x]==2:
            gx,gy=x*TS+TS/2,y*TS+TS/2
px,py=TS+TS/2,TS+TS/2
while [gx,gy]==[px,py]:
    MAP=mazegenerator(mw,mh)
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x]==2:
                gx,gy=x*TS+TS/2,y*TS+TS/2

pg.init()

w,h=800,600
win=pg.display.set_mode((w,h))

fov=60
rend=200
a=0
def get_wall(x,y,ts,m:list[list[int]]):
    x,y=int(x/ts),int(y/ts)
    if x >= 0 and x < len(m[-1]) and y >= 0 and y < len(m):
        return m[y][x]
ps=1
run=True
clock=pg.time.Clock()
while run:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run=False
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_SPACE:
                # places a marker to mark a spot you have already searched.
                fx,fy=TS*sin(a)+px,TS*cos(a)+py
                if get_wall(fx,fy,TS,MAP)==0:
                    MAP[int(fy/TS)][int(fx/TS)]=3
                elif get_wall(fx,fy,TS,MAP)==3:
                    MAP[int(fy/TS)][int(fx/TS)]=0
                    
    win.fill((0,0,0))

    u,d,l,r=pg.key.get_pressed()[pg.K_UP],pg.key.get_pressed()[pg.K_DOWN],pg.key.get_pressed()[pg.K_LEFT],pg.key.get_pressed()[pg.K_RIGHT]
    if u and get_wall(px+sin(a)*ps,py+cos(a)*ps,TS,MAP)!=1: # avoid clipping through walls by checking if the player's change in position will intercept the wall 
        px+=sin(a)*ps
        py+=cos(a)*ps
    elif get_wall(px,py,TS,MAP)==2:
        MAP=mazegenerator(mw,mh)
        gx,gy=0,0
        for y in range(len(MAP)):
            for x in range(len(MAP[y])):
                if MAP[y][x]==2:
                    gx,gy=x*TS+TS/2,y*TS+TS/2
        px,py=TS+TS/2,TS+TS/2
        while [gx,gy]==[px,py]:
            MAP=mazegenerator(mw,mh)
            for y in range(len(MAP)):
                for x in range(len(MAP[y])):
                    if MAP[y][x]==2:
                        gx,gy=x*TS+TS/2,y*TS+TS/2
        
    elif d and get_wall(px-sin(a)*ps,py-cos(a)*ps,TS,MAP)!=1:
        px-=sin(a)*ps
        py-=cos(a)*ps
    if l:
        a-=ps*.025
    elif r:
        a+=ps*.025
    
    for ray in range(fov):
        angle=a+radians(ray)-radians(fov/2)
        for d in range(rend):
            tx=sin(angle)*d+px
            ty=cos(angle)*d+py
            wall=get_wall(tx,ty,TS,MAP)
            if wall!=0:
                d*=cos(atan2(tx-px,ty-py)-a)
                wh=h*TS/(d+1)
                x1=(w/fov)*ray
                x2=(w/fov)+1
                y1=h/2-wh/2
                y2=wh
                color=lambda x: x-x*(d/rend)
                if wall==1:
                    pg.draw.rect(win,(color(255),color(155),color(155)),[x1,y1,x2,y2]) # maze walls
                elif wall==2:
                    pg.draw.rect(win,(color(155),color(255),color(155)),[x1,y1,x2,y2]) # target
                elif wall==3:
                    pg.draw.rect(win,(color(155),color(155),color(255)),[x1,y1,x2,y2]) # marked spots

                break

    


    pg.display.update()
    clock.tick(120)
