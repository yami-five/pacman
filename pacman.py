import curses
import os
from time import sleep
from getmap import GetMap
from random import randint
import _thread
import threading
import queue
import sys
lvlArray=GetMap()
Score=0
lives=3
playerPos=[20,12]
YesHeSDead=False
class Enemy:
    enemyPos=[11,12]
    def __init__(self,_colorNum):
        self.colorNum=_colorNum

def IsHeDead():
    global lives
    global playerPos
    global YesHeSDead
    global GameOver
    if lives>0:
        playerPos=[20,12]
    else:
        YesHeSDead=True
        sys.exit("Game over!")
        
def draw_level(lvlArray,enemies):
    global Score
    global lives
    global playerPos
    pad=curses.newpad(23,30)
    pad.addstr(0,25,"Score")
    pad.addstr(1,25,str(Score))
    pad.addstr(2,25,"Lives")
    pad.addstr(3,25,'# '*lives,curses.color_pair(8))
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_YELLOW,curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE,curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_YELLOW,curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA,curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_RED,curses.COLOR_BLACK)
    for x in range(0,23):
        for y in range(0,25):
            if lvlArray[x][y]==1:
                pad.addstr(x,y,'#',curses.color_pair(1))
            elif lvlArray[x][y]==2:
                pad.addstr(x,y,'#',curses.color_pair(3))
            elif lvlArray[x][y]==3:
                pad.addstr(x,y,'#',curses.color_pair(2))
    pad.addstr(playerPos[0],playerPos[1],'@')
    for x in range(0,4):
        pad.addstr(enemies[x].enemyPos[0],enemies[x].enemyPos[1],'M',curses.color_pair(enemies[x].colorNum))
    pad.refresh(0,0,0,0,22,29)

def change_pos(key,lvlArray):
    global Score
    global lives
    global playerPos
    #Up
    if key==259:
        playerPos[0]-=1
        if playerPos[0]<0:
            playerPos[0]=0
        elif lvlArray[playerPos[0]][playerPos[1]]==1 or lvlArray[playerPos[0]][playerPos[1]]==2:
            playerPos[0]+=1
        elif lvlArray[playerPos[0]][playerPos[1]]==3:
                Score+=1
                lvlArray[playerPos[0]][playerPos[1]]=0
    #Down
    if key==258:
        playerPos[0]+=1
        if playerPos[0]>23:
            playerPos[0]=23
        elif lvlArray[playerPos[0]][playerPos[1]]==1:
            playerPos[0]-=1
        elif lvlArray[playerPos[0]][playerPos[1]]==3:
                Score+=1
                lvlArray[playerPos[0]][playerPos[1]]=0
    #Left
    if key==260:
        playerPos[1]-=1
        if playerPos[1]<0:
            playerPos[1]=0
        elif lvlArray[playerPos[0]][playerPos[1]]==1:
            playerPos[1]+=1
        elif lvlArray[playerPos[0]][playerPos[1]]==3:
                Score+=1
                lvlArray[playerPos[0]][playerPos[1]]=0
    #Right
    if key==261:
        playerPos[1]+=1
        if playerPos[1]>25:
            playerPos[1]=25
        elif lvlArray[playerPos[0]][playerPos[1]]==1:
            playerPos[1]-=1
        elif lvlArray[playerPos[0]][playerPos[1]]==3:
                Score+=1
                lvlArray[playerPos[0]][playerPos[1]]=0
    return playerPos,Score

def change_enemy_pos(enemyPos,lvlArray):
    global lives
    global playerPos
    if (enemyPos[0]==11 or enemyPos[0]==12 or enemyPos[0]==13) and enemyPos[1]==12:
        return [enemyPos[0]+1,12]
    else:
        direction=randint(0,3)
        #Up
        if direction==0:
            enemyPos[0]-=1
            if enemyPos[0]<0:
                enemyPos[0]=0
            elif lvlArray[enemyPos[0]][enemyPos[1]]==1 or lvlArray[enemyPos[0]][enemyPos[1]]==2:
                enemyPos[0]+=1
        #Down
        if direction==1:
            enemyPos[0]+=1
            if enemyPos[0]>23:
                enemyPos[0]=23
            elif lvlArray[enemyPos[0]][enemyPos[1]]==1:
                    enemyPos[0]-=1
        #Left
        if direction==2:
            enemyPos[1]-=1
            if enemyPos[1]<0:
                enemyPos[1]=0
            elif lvlArray[enemyPos[0]][enemyPos[1]]==1:
                enemyPos[1]+=1
        #Right
        if direction==3:
            enemyPos[1]+=1
            if enemyPos[1]>25:
                enemyPos[1]=25
            elif lvlArray[enemyPos[0]][enemyPos[1]]==1:
                enemyPos[1]-=1
        return enemyPos
    
def enemyLoop(lvlArray,enemies,q):
    counter=1
    global Score
    global lives
    global playerPos
    while True:
        sleep(0.0005)
        for x in range(0,4):
            if enemies[x].enemyPos==playerPos:
                lives-=1
                IsHeDead()
        if counter==100:
            for x in range(0,4):
                enemies[x].enemyPos=change_enemy_pos(enemies[x].enemyPos,lvlArray)
            counter=0
            draw_level(lvlArray,enemies)
        else:
            counter+=1
            
def playerLoop(lvlArray,enemies,q):
    global Score
    global lives
    global playerPos
    global YesHeSDead
    while True:
        if YesHeSDead:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.endwin()
            sys.exit("Game over!")
        key=stdscr.getch()
        if key==27:
            break
        elif key in range(258,262):
            playerPos,Score=change_pos(key,lvlArray)
            draw_level(lvlArray,enemies)
        else:
            print(key)
        
        
def main():
    global YesHeSDead
    G1=Enemy(4)
    G2=Enemy(5)
    G3=Enemy(6)
    G4=Enemy(7)
    enemies=[]
    enemies.append(G1)
    enemies.append(G2)
    enemies.append(G3)
    enemies.append(G4)
    q=queue.Queue()
    draw_level(lvlArray,enemies)
    _thread.start_new_thread(playerLoop,(lvlArray,enemies,q))
    _thread.start_new_thread(enemyLoop,(lvlArray,enemies,q))
    while YesHeSDead==False:
        pass
    

if __name__=='__main__':
    #os.system("mode con cols=20 lines=21")
    stdscr=curses.initscr()
    curses.curs_set(0)
    curses.start_color()
    stdscr.refresh()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    main()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.endwin()
 
