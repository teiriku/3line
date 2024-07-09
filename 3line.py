import pyxel
import copy

class Board:
    def __init__(self):
        self.coord=[] #[y][x]でアクセス
        for i in range(12):
            self.coord.append([0,0,0,0,0,0])
        self.lines=[]


    def isCollide(self,piece):
        for cell in piece.place:
            if cell[0]>5 or cell[0]<0 or cell[1]>11 or cell[1]<0:
                return True
            if self.coord[cell[1]][cell[0]]!=0:
                return True
        return False


    def addPiece(self,piece):
        for cell in piece.place:
            self.coord[cell[1]][cell[0]]=cell[2]


    def score(self):
        lines=[]
        line=[]

        for y,row in enumerate(self.coord):
            line=[]
            for x,value in enumerate(row):
                if value==1 or value==2 or value==-2:
                    line.append([x,y,value])
                else:
                    if len(line)>2:
                        lines.append(line)
                    line=[]
            if len(line)>2:
                lines.append(line)

        coordT=[list(x) for x in zip(*self.coord)]

        for x,column in enumerate(coordT):
            line=[]
            for y,value in enumerate(column):
                if value==-1 or value==2 or value==-2:
                    line.append([x,y,value])
                else:
                    if len(line)>2:
                        lines.append(line)
                    line=[]
            if len(line)>2:
                lines.append(line)
        
        self.lines=lines


    def fall(self):
        for line in self.lines:
            for cell in line:
                self.coord[cell[1]][cell[0]]=0

        coordT=[list(x) for x in zip(*self.coord)]
        newCoordT=[]
        newColumn=[]

        for column in coordT:
            newColumn=[x for x in column if x!=0]
            while len(newColumn)<12:
                newColumn.insert(0,0)
            newCoordT.append(newColumn)

        self.coord=[list(x) for x in zip(*newCoordT)]



class Piece:
    def __init__(self):
        self.place=[[0,0,0],[0,0,0],[0,0,0]] # [x-coorc, y-coord, line orientation]
        self.kind=0 # 0:L 1:I
        self.orientation=0
        self.state=0  #self.states=[0,1] 落下中、落下済み


    def generate(self): #1:- -1:| 2or-2:+
        self.kind=pyxel.rndi(0,1)

        if self.kind: #I
            self.place[0][0]=1
            self.place[1][0]=2
            self.place[2][0]=3

        else: #L
            self.place[0][0]=2
            self.place[1][0]=2
            self.place[2][0]=3
            self.place[1][1]=1
            self.place[2][1]=1

        for place in self.place:
            p=5
            prob=pyxel.rndi(0,2*p)
            if prob<p:
                place[2]=1
            if prob>p:
                place[2]=-1
            if prob==p:
                place[2]=2


    def rotate(self,side): #1:right 0:left
        for cell in self.place:
            cell[2]*=-1

        if self.kind: #I
            if self.orientation==0: # 012
                if side: #right
                    self.place[0][0]+=1
                    self.place[0][1]-=1
                    self.place[2][0]-=1
                    self.place[2][1]+=1

                    self.orientation=1
                    return

                else: #left
                    self.place[0][0]+=1
                    self.place[0][1]+=1
                    self.place[2][0]-=1
                    self.place[2][1]-=1

                    self.orientation=3
                    return

            if self.orientation==1: #012^T
                if side: #right
                    self.place[0][0]+=1
                    self.place[0][1]+=1
                    self.place[2][0]-=1
                    self.place[2][1]-=1

                    self.orientation=2
                    return

                else: #left
                    self.place[0][0]-=1
                    self.place[0][1]+=1
                    self.place[2][0]+=1
                    self.place[2][1]-=1

                    self.orientation=0
                    return

            if self.orientation==2: #210
                if side: #right
                    self.place[0][0]-=1
                    self.place[0][1]+=1
                    self.place[2][0]+=1
                    self.place[2][1]-=1

                    self.orientation=3
                    return

                else: #left
                    self.place[0][0]-=1
                    self.place[0][1]-=1
                    self.place[2][0]+=1
                    self.place[2][1]+=1

                    self.orientation=1
                    return

            if self.orientation==3: #210^T
                if side: #right
                    self.place[0][0]-=1
                    self.place[0][1]-=1
                    self.place[2][0]+=1
                    self.place[2][1]+=1

                    self.orientation=0
                    return

                else: #left
                    self.place[0][0]+=1
                    self.place[0][1]-=1
                    self.place[2][0]-=1
                    self.place[2][1]+=1

                    self.orientation=2
                    return

        else: #L
            if self.orientation==0: # L
                if side: #right
                    self.place[0][0]+=1
                    self.place[1][1]-=1
                    self.place[2][0]-=1

                    self.orientation=1
                    return

                else: #left
                    self.place[0][1]+=1
                    self.place[1][0]+=1
                    self.place[2][1]-=1

                    self.orientation=3
                    return

            if self.orientation==1: #「
                if side: #right
                    self.place[0][1]+=1
                    self.place[1][0]+=1
                    self.place[2][1]-=1

                    self.orientation=2
                    return

                else: #left
                    self.place[0][0]-=1
                    self.place[1][1]+=1
                    self.place[2][0]+=1

                    self.orientation=0
                    return

            if self.orientation==2: # ￢
                if side: #right
                    self.place[0][0]-=1
                    self.place[1][1]+=1
                    self.place[2][0]+=1

                    self.orientation=3
                    return

                else: #left
                    self.place[0][1]-=1
                    self.place[1][0]-=1
                    self.place[2][1]+=1

                    self.orientation=1
                    return

            if self.orientation==3: # 」
                if side: #right
                    self.place[0][1]-=1
                    self.place[1][0]-=1
                    self.place[2][1]+=1

                    self.orientation=0
                    return

                else: #left
                    self.place[0][0]+=1
                    self.place[1][1]-=1
                    self.place[2][0]-=1

                    self.orientation=2
                    return


    def move(self,side): #1:right 0:left
        if side: #right
            for cell in self.place:
                cell[0]+=1
        else: #left
            for cell in self.place:
                cell[0]-=1


    def drop(self):
        for cell in self.place:
            cell[1]+=1


    def up(self):
        for cell in self.place:
            cell[1]-=1
            if cell[1]<0:
                cell[1]=12


    def isOutOfBounds(self):
        for cell in self.place:
            if cell[0]<0:
                return "left"
            if cell[0]>5:
                return "right"
            if cell[1]<0:
                return "up"
        return False


    def isDropped(self):
        for cell in self.place:
            if cell[1]>11:
                return True
        return False



class Score:
    def __init__(self,score):
        self.score=0
        self.level=1
        self.speed=30
        self.nowScore=0
        self.highScore=score


    def addScore(self,lines,combo):
        self.nowScore=0
        for l in lines:
            self.nowScore+=(len(l)-2)*30*combo
        self.score+=self.nowScore


    def calcLevel(self):
        self.level=self.score//200+1
        self.speed=max(30-(self.level-1)*2,6)
        if self.level>=20: self.speed=4
        if self.level>=30: self.speed=3
        if self.level>=40: self.speed=2
        if self.level>=50: self.speed=1
        


class Playing:
    def __init__(self,score):
        self.board=Board()
        self.nowPiece=Piece()
        self.nextPiece=Piece()
        self.checkPiece=Piece()
        self.score=Score(score)

        self.startMode=True
        self.playMode=False
        self.scoreMode=False
        self.overMode=False
        self.lastEx=False

        self.combo=0
        self.time=0
        self.scoreTime=0
        self.overTime=0


    def prep(self):
        self.nowPiece.generate()
        self.nextPiece.generate() #state:0


    def drop(self):
        self.checkPiece=copy.deepcopy(self.nowPiece)
        self.checkPiece.drop()

        if self.checkPiece.isDropped():
            self.nowPiece.state=1
            return
        if self.board.isCollide(self.checkPiece):
            self.nowPiece.state=1
            return

        self.nowPiece=self.checkPiece


    def control(self):
        self.checkPiece=copy.deepcopy(self.nowPiece)

        if pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.KEY_RIGHT): #move right
            self.checkPiece.move(1)
            if not self.checkPiece.isOutOfBounds() and not self.board.isCollide(self.checkPiece):
                self.nowPiece=self.checkPiece
                pyxel.play(0,0)

        if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.KEY_LEFT): #move left
            self.checkPiece.move(0)
            if not self.checkPiece.isOutOfBounds() and not self.board.isCollide(self.checkPiece):
                self.nowPiece=self.checkPiece
                pyxel.play(0,1)
        
        if pyxel.btnp(pyxel.KEY_S,10,5) or pyxel.btnp(pyxel.KEY_DOWN,10,5):
            self.drop()
            pyxel.play(0,2)

        if pyxel.btnp(pyxel.KEY_E): #rotate right
            self.checkPiece.rotate(1)

            if self.checkPiece.isOutOfBounds()=="right":
                self.checkPiece.move(0) #move left
                if not self.board.isCollide(self.checkPiece):
                    self.nowPiece=self.checkPiece
                    pyxel.play(0,3)
                    return

            if self.checkPiece.isOutOfBounds()=="left":
                self.checkPiece.move(1)
                if not self.board.isCollide(self.checkPiece):
                    self.nowPiece=self.checkPiece
                    pyxel.play(0,3)
                    return

            if self.checkPiece.isOutOfBounds()=="up":
                self.checkPiece.drop()
                if not self.board.isCollide(self.checkPiece):
                    self.nowPiece=self.checkPiece
                    pyxel.play(0,3)
                    return

            if self.board.isCollide(self.checkPiece):
                self.checkPiece.up()
                if not self.board.isCollide(self.checkPiece):
                    self.nowPiece=self.checkPiece
                    pyxel.play(0,3)
                return

            self.nowPiece=self.checkPiece
            pyxel.play(0,3)

        if pyxel.btnp(pyxel.KEY_Q): #rotate left
            self.checkPiece.rotate(0)

            if self.checkPiece.isOutOfBounds()=="right":
                self.checkPiece.move(0) #move left
                if not self.board.isCollide(self.checkPiece):
                    self.nowPiece=self.checkPiece                    
                    pyxel.play(0,4)
                    return

            if self.checkPiece.isOutOfBounds()=="left":
                self.checkPiece.move(1)
                if not self.board.isCollide(self.checkPiece):
                    self.nowPiece=self.checkPiece
                    pyxel.play(0,4) 
                    return

            if self.checkPiece.isOutOfBounds()=="up":
                self.checkPiece.drop()
                if not self.board.isCollide(self.checkPiece):
                    self.nowPiece=self.checkPiece
                    pyxel.play(0,4) 
                    return

            if self.board.isCollide(self.checkPiece):
                self.checkPiece.up()
                if not self.board.isCollide(self.checkPiece):
                    self.nowPiece=self.checkPiece
                    pyxel.play(0,4)
                return
                    
            self.nowPiece=self.checkPiece
            pyxel.play(0,4)


    def dropped(self):
        self.board.addPiece(self.nowPiece)

        self.playMode=False
        self.scoreMode=True
        self.board.fall()
        self.combo=1
        self.scoreTime=3

        pyxel.play(0,5)


    def isOver(self):
        coord=self.board.coord

        if self.nowPiece.kind: #I
            if coord[0][1] or coord[0][2] or coord[0][3]:
                return True
        else: #L
            if coord[0][2] or coord[1][2] or coord[1][3]:
                return True

        return False


    def drawSide(self):

        pyxel.blt(102,20,0,0,32,72,16)

        pyxel.text(110,55,f"level:{self.score.level}",7)
        pyxel.text(110,65,f"score:{self.score.score}",7)
        pyxel.text(106,75,f"Hscore:{self.score.highScore}",7)

        pyxel.text(110,100,"NEXT",7)

        pyxel.blt(105,110,0,0,48,60,48)
        
        pyxel.text(110,180,"@Jun M. 2023",7)


    def drawNext(self):

        for cell in self.nextPiece.place:
            x=cell[0]
            y=cell[1]
            value=cell[2]

            if self.nextPiece.kind==1: #I
                x+=5.8
                y+=7.79

            else:
                x+=5.3
                y+=7.3

            if value==1:
                pyxel.blt(x*16,y*16,0,0,96,16,16)
            if value==-1:
                pyxel.blt(x*16,y*16,0,16,96,16,16)
            if value==2 or value==-2:
                pyxel.blt(x*16,y*16,0,32,96,16,16)


    def playUpdate(self):
        self.control()

        if self.time%self.score.speed==0:
            self.drop()

        if self.nowPiece.state==1:
            self.dropped()

        self.time+=1


    def playDraw(self):
        for y,row in enumerate(self.board.coord):
            for x,value in enumerate(row):
                if value==1:
                    pyxel.blt(x*16,y*16,0,0,0,16,16)
                if value==-1:
                    pyxel.blt(x*16,y*16,0,16,0,16,16)
                if value==2 or value==-2:
                    pyxel.blt(x*16,y*16,0,32,0,16,16)
                if value==0:
                    pyxel.blt(x*16,y*16,0,48,0,16,16)

        for cell in self.nowPiece.place:
            x=cell[0]
            y=cell[1]
            value=cell[2]
            if value==1:
                pyxel.blt(x*16,y*16,0,0,0,16,16)
            if value==-1:
                pyxel.blt(x*16,y*16,0,16,0,16,16)
            if value==2 or value==-2:
                pyxel.blt(x*16,y*16,0,32,0,16,16)

        self.drawSide()
        self.drawNext()


    def scoreUpdate(self):

        if self.scoreTime%25==9:
            self.board.score()
            self.score.addScore(self.board.lines,self.combo)

            if self.score.nowScore==0:
                self.score.calcLevel()

                self.scoreMode=False
                self.playMode=True

                self.nowPiece=copy.deepcopy(self.nextPiece)

                if self.isOver():
                    self.playMode=False
                    self.overMode=True
                    return

                self.nextPiece.__init__()
                self.nextPiece.generate()

                return
            
        if self.scoreTime%25==10:
            sound=min(self.combo+5,11)
            pyxel.play(0,sound)

        if self.scoreTime%25==24:
            self.board.fall()
            self.combo+=1

        self.scoreTime+=1

    
    def scoreDraw(self):

        if self.scoreTime%25<10:
            self.droppedDraw()

        if 10<=self.scoreTime%25<20:
            self.clearDraw()

        if 20<=self.scoreTime%25:
            self.floatDraw()

        self.drawSide()
        self.drawNext()


    def droppedDraw(self):
        for y,row in enumerate(self.board.coord):
            for x,value in enumerate(row):
                if value==1:
                    pyxel.blt(x*16,y*16,0,0,0,16,16)
                if value==-1:
                    pyxel.blt(x*16,y*16,0,16,0,16,16)
                if value==2 or value==-2:
                    pyxel.blt(x*16,y*16,0,32,0,16,16)
                if value==0:
                    pyxel.blt(x*16,y*16,0,48,0,16,16)


    def clearDraw(self):
        for y,row in enumerate(self.board.coord):
            for x,value in enumerate(row):
                if value==1:
                    pyxel.blt(x*16,y*16,0,0,0,16,16)
                if value==-1:
                    pyxel.blt(x*16,y*16,0,16,0,16,16)
                if value==2 or value==-2:
                    pyxel.blt(x*16,y*16,0,32,0,16,16)
                if value==0:
                    pyxel.blt(x*16,y*16,0,48,0,16,16)

        for line in self.board.lines:
            for i,cell in enumerate(line):
                x=cell[0]
                y=cell[1]
                value=cell[2]

                if value==1:
                    pyxel.blt(x*16,y*16,0,0,16,16,16)
                if value==-1:
                    pyxel.blt(x*16,y*16,0,16,16,16,16)
                if value==2 or value==-2:
                    pyxel.blt(x*16,y*16,0,32,16,16,16)

        for line in self.board.lines:
            for i,cell in enumerate(line):
                x=cell[0]
                y=cell[1]
                value=cell[2]

                if i==0:
                    pyxel.text(x*16+2,y*16+5,f"+{(len(line)-2)*30+i*10}",0)

                if i==1 and self.combo>1:
                    pyxel.text(x*16+5,y*16+5,f"x{(self.combo)}",8)
                

    def floatDraw(self):
        for y,row in enumerate(self.board.coord):
            for x,value in enumerate(row):
                if value==1:
                    pyxel.blt(x*16,y*16,0,0,0,16,16)
                if value==-1:
                    pyxel.blt(x*16,y*16,0,16,0,16,16)
                if value==2 or value==-2:
                    pyxel.blt(x*16,y*16,0,32,0,16,16)
                if value==0:
                    pyxel.blt(x*16,y*16,0,48,0,16,16)

        for line in self.board.lines:
            for cell in line:
                x=cell[0]
                y=cell[1]
                pyxel.blt(x*16,y*16,0,48,0,16,16)


    def startUpdate(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.startMode=False
            self.playMode=True
            pyxel.play(0,20)


    def startDraw(self):
        for y in range(12):
            for x in range(6):
                pyxel.blt(x*16,y*16,0,48,0,16,16)

        pyxel.text(8,54,"Press SPACE to Start",7)

        pyxel.text(26,100,"How to play",7)

        pyxel.blt(26,110,0,0,112,44,32)
        pyxel.blt(26,140,0,0,144,44,32)

        self.drawSide()


    def overUpdate(self):

        if self.overTime==0:
            if self.nowPiece.kind==0 and not self.board.coord[0][1] and not self.board.coord[0][2]:
                self.nowPiece.up()
                self.lastEx=True

        if self.overTime==20:
            pyxel.play(0,21)

        if self.overTime>=50 and pyxel.btnp(pyxel.KEY_SPACE):
            self.__init__(max(self.score.score,self.score.highScore))

            self.prep()
            return

        self.overTime+=1


    def overDraw(self):

        if self.overTime<20:
            for y,row in enumerate(self.board.coord):
                for x,value in enumerate(row):
                    if value==1:
                        pyxel.blt(x*16,y*16,0,0,0,16,16)
                    if value==-1:
                        pyxel.blt(x*16,y*16,0,16,0,16,16)
                    if value==2 or value==-2:
                        pyxel.blt(x*16,y*16,0,32,0,16,16)
                    if value==0:
                        pyxel.blt(x*16,y*16,0,48,0,16,16)

            if self.lastEx:
                for cell in self.nowPiece.place:
                    x=cell[0]
                    y=cell[1]
                    value=cell[2]
                    if value==1:
                        pyxel.blt(x*16,y*16,0,0,0,16,16)
                    if value==-1:
                        pyxel.blt(x*16,y*16,0,16,0,16,16)
                    if value==2 or value==-2:
                        pyxel.blt(x*16,y*16,0,32,0,16,16)

        if 20<=self.overTime<50:
            for y,row in enumerate(self.board.coord):
                for x,value in enumerate(row):
                    if y<=self.overTime/2-10:
                        value=0
                    if value==1:
                        pyxel.blt(x*16,y*16,0,0,0,16,16)
                    if value==-1:
                        pyxel.blt(x*16,y*16,0,16,0,16,16)
                    if value==2 or value==-2:
                        pyxel.blt(x*16,y*16,0,32,0,16,16)
                    if value==0:
                        pyxel.blt(x*16,y*16,0,48,0,16,16)

        if 50<=self.overTime:
            pyxel.rect(0,0,96,192,1)
            pyxel.text(30,54,"GAME OVER",7)
            pyxel.text(30,77,f"score:{self.score.score}",7)
            pyxel.text(4,100,"Press SPACE to restart",7)

        self.drawSide()



class App:
    playing=Playing(0)

    def __init__(self):
        pyxel.init(170,192)
        pyxel.load("3line_resource.pyxres")
        self.playing.prep()

        pyxel.run(self.update,self.draw)


    def update(self):
        if self.playing.startMode:
            self.playing.startUpdate()
        if self.playing.playMode:
            self.playing.playUpdate()
        if self.playing.scoreMode:
            self.playing.scoreUpdate()
        if self.playing.overMode:
            self.playing.overUpdate()
        

    def draw(self):
        pyxel.cls(0)

        if self.playing.startMode:
            self.playing.startDraw()
        if self.playing.playMode:
            self.playing.playDraw()
        if self.playing.scoreMode:
            self.playing.scoreDraw()
        if self.playing.overMode:
            self.playing.overDraw()


App()