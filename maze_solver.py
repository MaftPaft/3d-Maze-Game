from random import choice
import pygame as pg
from math import *
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

def mazefinder(MAZE,start=[1,1],target=2):
    maze=[[MAZE[y][x] for x in range(len(MAZE[y]))] for y in range(len(MAZE))]
    stack=[start]
    def notedge(x,y):
        return x > 0 and x < len(maze[0])-1 and y > 0 and y < len(maze)-1
    def getneighbours(x,y):
        n=[]
        if notedge(x+1,y): n.append([x+1,y])
        if notedge(x-1,y): n.append([x-1,y])
        if notedge(x,y+1): n.append([x,y+1])
        if notedge(x,y-1): n.append([x,y-1])
        return n
    run=True
    
    while run and stack:
        x,y=stack[-1]
        neighbours=getneighbours(x,y)
        unvisited=[n for n in neighbours if maze[n[1]][n[0]]==0 or maze[n[1]][n[0]]==2]
        if unvisited:
            nx,ny=choice(unvisited)
            if maze[y][x]==target:
                break
            maze[y][x]=3
            if maze[ny][nx]==target:
                break
            maze[ny][nx]=3
            stack.append([nx,ny])
        else:
            stack.pop()
    while stack:
        x,y=stack[-1]
        maze[y][x]=4

        stack.pop()
    return maze


pg.init()

w,h=799,599
win=pg.display.set_mode((w,h))
mw,mh=w,h
TS=1
MAP=mazegenerator(mw,mh)
path=mazefinder(MAP,[mw-2,mh-2],2)
fps=60
fin=[]
run=True
clock=pg.time.Clock()
while run:
    mp=pg.mouse.get_pressed()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run=False
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_r:
                MAP=mazegenerator(mw,mh)
                path=mazefinder(MAP,[mw-2,mh-2],2)
    win.fill((0,0,0))

    
    for y in range(len(path)):
        for x in range(len(path[y])):
            rect=[TS*x,TS*y,TS,TS]
            if path[y][x]==1:
                pg.draw.rect(win,(0,0,155),rect)
            elif path[y][x]==2:
                pg.draw.rect(win,(255,0,0),rect)
                fin=[x*TS+TS/2,y*TS+TS/2]
            elif path[y][x]==4:
                pg.draw.rect(win,(255,255,0),rect)
            elif path[y][x]==3:
                pg.draw.rect(win,(0,255,0),rect)
            elif path[y][x]==0:
                pg.draw.rect(win,(0,0,155),rect)
    if mp[0] and fin:
        pg.draw.circle(win,(255,0,0),fin,7)
    pg.display.update()
    clock.tick(fps)
