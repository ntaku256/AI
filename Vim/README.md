# Vim
<img src="https://github.com/ntaku256/AI/blob/main/Source/VimKeySettings.png" width="100%">

```python
import numpy as np
import copy

class Osero:
    Width = 8
    Height = 8

    #white:0, black:1, empty:-1
    Field = None

    PlayerColor = None
    Execution = None
    PutPosition = []
    NextMove = 4
    GetValue = []

    def __init__(self):
        self.Field = [[-1 for i in range(self.Width)] for i in range(self.Height)]
        self.Field[3][3] = 0
        self.Field[3][4] = 1
        self.Field[4][3] = 1
        self.Field[4][4] = 0

        self.Execution = [0 for i in range(self.NextMove)]

    def Disp(self,field):
        s = "  "
        for i in range(self.Width):
            s += "|"+str(i)+" "
        s += "\n  "
        for i in range(self.Width):
            s += "|--"
        s += "\n"
        for i in range(self.Height):
            s += str(i) + " "
            for j in range(self.Width):
                if field[i][j] == 0:
                    s += "|● "
                if field[i][j] == 1:
                    s += "|○ "
                if field[i][j] == -1:
                    s += "|  "
            s += "|\n"
        s+= "  "
        for i in range(self.Width):
            s += "|--"
        s += "\n"
        print(s)

    def Put(self,y,x,color,field):
        dxArr = [0,1,1,1,0,-1,-1,-1]
        dyArr = [1,1,0,-1,-1,-1,0,1]
        for dx,dy in zip(dxArr,dyArr):
            if(l := self.CheckDepth(color,y,x,dy,dx,field),l!=-1):
                xx = x
                yy = y
                for i in range(l+1):
                    field[yy][xx] = color
                    xx += dx
                    yy += dy
        return field

    def CheckDepth(self,color,y,x,dy,dx,field):
        depth = 0
        while(True):
            y += dy
            x += dx
            if(self.IsInside(y,x)==False or field[y][x] == -1):
                return -1
            if(field[y][x] == color):
                return depth
            depth += 1

    def IsInside(self,y,x):
        return x >= 0 and x < self.Width and y >= 0 and y < self.Height

    def CanPut(self,y,x,color,field):
        if not self.IsInside(y, x) or field[y][x] != -1:
            return False
        flag = False
        dxArr = [0,1,1,1,0,-1,-1,-1]
        dyArr = [1,1,0,-1,-1,-1,0,1]
        for dx,dy in zip(dxArr,dyArr):
            if(self.CheckDepth(color,y,x,dy,dx,field) > 0):
                return True
    
    def CalcStoneValue(self,y,x,color,field,stoneMap):
        plusmass = []
        dxArr = [0,1,1,1,0,-1,-1,-1]
        dyArr = [1,1,0,-1,-1,-1,0,1]
        value = stoneMap[y][x]
        plusmass.append(stoneMap[y][x])
        for dx,dy in zip(dxArr,dyArr):
            if(l := self.CheckDepth(color,y,x,dy,dx,field),l!=-1):
                xx = x+dx
                yy = y+dy
                for _ in range(l):
                    if field[yy][xx] != color:
                        plusmass.append(stoneMap[yy][xx])
                        value += stoneMap[yy][xx]
                    xx += dx
                    yy += dy

        # print("GetPos = ",plusmass)
        if self.PlayerColor == color:
            return -value
        else:
            return value
    
    def GetPossiblePutPositionAndValue(self,color,stoneMap):
        positions = []
        values = []
        for y in range(self.Height):
            for x in range(self.Width):
                if self.CanPut(y,x,color,self.Field):
                    positions.append([y,x])
                    values.append(self.CalcStoneValue(y,x,color,self.Field,stoneMap))
        return positions,values

    def CalcValue(self,field,stoneMap):
        value = 0
        for y in range(self.Height):
                for x in range(self.Width):
                    if field[y][x] == self.PlayerColor:
                        value -=stoneMap[y][x]
                    elif field[y][x] == (self.PlayerColor + 1)%2:
                        value +=stoneMap[y][x]
        return value




    def GetPossiblePutPosition(self,color,field,n,stoneMap,value = 0):
        positions = []
        values = []
        PossiblePositon = False 
        if n<self.NextMove:
            for y in range(self.Height):
                for x in range(self.Width):
                    if self.CanPut(y,x,color,field):
                        subValue = np.copy(value)
                        PossiblePositon = True
                        putField = self.Put(y,x,color,np.copy(field))
                        self.Execution[n] = self.Execution[n] + 1
                        subValue += self.CalcStoneValue(y,x,color,field,stoneMap)
                        # print("Execution = ",self.Execution,"\tclass = ",n,"\tPut = ",[y,x],"\tvalue = ",subValue)
                        # self.Disp(putField)
                        positions.append([y,x])
                        values.append(self.GetPossiblePutPosition((color + 1)%2,putField,n + 1,stoneMap,np.copy(subValue)))
            if PossiblePositon is False:
                values.append(self.GetPossiblePutPosition((color + 1)%2,field,n + 1,stoneMap,np.copy(value)))
        # if values != []:
        #     print("class = ",n,"\tvalues = ",values)

        if n == 0:
            if values !=[]:
                print("PossiblePositons = ",positions,"\tvalue = ",np.argmax(values))
                return positions[np.argmax(values)]
        elif n == self.NextMove:
            # return self.CalcValue(field,stoneMap)
            return value
        else:
            if values !=[]:
                if self.PlayerColor == color:
                    return max(values)
                else:
                    return min(values)
            return 0
    
    def Result(self):
        n_white = 0
        n_black = 0
        n_sum = 0
        for y in range(self.Height):
            for x in range(self.Width):
                if self.Field[y][x] == -1:
                    continue
                n_sum += 1
                if self.Field[y][x] == 0:
                    n_white += 1
                if self.Field[y][x] == 1:
                    n_black += 1
        return n_white,n_black,n_sum
    
if __name__ == "__main__":
    o = Osero()
    color = 0
    o.PlayerColor = color
    stoneMap = [
            [ 30, -12,  0, -1, -1,   0, -12,  30],
            [-12, -15, -3, -3, -3, -15, -15, -12],
            [  0,  -3,  0, -1, -1,   0,  -3,   0],
            [ -1,  -3, -1, -1, -1,  -1,  -3,  -1],
            [ -1,  -3, -1, -1, -1,  -1,  -3,  -1],
            [  0,  -3,  0, -1, -1,   0,  -3,   0],
            [-12, -15, -3, -3, -3, -15, -15, -12],
            [ 30, -12,  0, -1, -1,   0, -12,  30],
            ]
    
    while(True):
        if color == 0:
            print("●の番です")
        else:
            print("○の番です")
        o.Disp(o.Field)
        arr,values = o.GetPossiblePutPositionAndValue(color,stoneMap)
        ## 二連続でどっちも置く場所がなければ終わり
        if len(arr) == 0:
            if flag:
                break
            color = (color + 1)%2
            flag = True
            continue
        else:
            flag = False
        if color == o.PlayerColor:
            print("おける場所")
            for (yy,xx) in arr:
                print("yy:",yy,"xx:",xx,"value:",o.CalcStoneValue(yy,xx,color,o.Field,stoneMap))
            y = int(input("y:"))
            x = int(input("x:"))
            if not o.CanPut(y, x, color,o.Field):
                print("置やんぞ!!")
            else:
                o.Put(y,x,color,o.Field)
                color = (color + 1)%2
        else:
            o.Execution = [0 for i in range(o.NextMove)]
            bestPosition = []
            bestPosition = o.GetPossiblePutPosition(np.copy(color),np.copy(o.Field),0,stoneMap)
            if bestPosition != []:
                print("Execution = ",o.Execution)
                print("BestPosition = ",bestPosition)
                o.Put(bestPosition[0],bestPosition[1],color,o.Field)
            else:
                print("BestPosition = None")
            color = (color + 1)%2

    n_white,n_black,n_sum = o.Result()
    print("white:",n_white,"black:",n_black,"total:",n_sum)
```

```python
import numpy as np
import copy

class Osero:
    Width = 8
    Height = 8

    #white:0, black:1, empty:-1
    Field = None

    PlayerColor = None
    Execution = None
    PutPosition = []
    NextMove = 4
    BestValue = None

    def __init__(self):
        self.Field = [[-1 for i in range(self.Width)] for i in range(self.Height)]
        self.Field[3][3] = 0
        self.Field[3][4] = 1
        self.Field[4][3] = 1
        self.Field[4][4] = 0

        self.Execution = [0 for i in range(self.NextMove)]

    def Disp(self,field):
        s = "  "
        for i in range(self.Width):
            s += "|"+str(i)+" "
        s += "\n  "
        for i in range(self.Width):
            s += "|--"
        s += "\n"
        for i in range(self.Height):
            s += str(i) + " "
            for j in range(self.Width):
                if field[i][j] == 0:
                    s += "|● "
                if field[i][j] == 1:
                    s += "|○ "
                if field[i][j] == -1:
                    s += "|  "
            s += "|\n"
        s+= "  "
        for i in range(self.Width):
            s += "|--"
        s += "\n"
        print(s)

    def Put(self,y,x,color,field):
        dxArr = [0,1,1,1,0,-1,-1,-1]
        dyArr = [1,1,0,-1,-1,-1,0,1]
        for dx,dy in zip(dxArr,dyArr):
            if(l := self.CheckDepth(color,y,x,dy,dx,field),l!=-1):
                xx = x
                yy = y
                for i in range(l+1):
                    field[yy][xx] = color
                    xx += dx
                    yy += dy
        return field

    def CheckDepth(self,color,y,x,dy,dx,field):
        depth = 0
        while(True):
            y += dy
            x += dx
            if(self.IsInside(y,x)==False or field[y][x] == -1):
                return -1
            if(field[y][x] == color):
                return depth
            depth += 1

    def IsInside(self,y,x):
        return x >= 0 and x < self.Width and y >= 0 and y < self.Height

    def CanPut(self,y,x,color,field):
        if not self.IsInside(y, x) or field[y][x] != -1:
            return False
        flag = False
        dxArr = [0,1,1,1,0,-1,-1,-1]
        dyArr = [1,1,0,-1,-1,-1,0,1]
        for dx,dy in zip(dxArr,dyArr):
            if(self.CheckDepth(color,y,x,dy,dx,field) > 0):
                return True
    
    def CalcStoneValue(self,y,x,color,field,stoneMap):
        dxArr = [0,1,1,1,0,-1,-1,-1]
        dyArr = [1,1,0,-1,-1,-1,0,1]
        value = stoneMap[y][x]
        for dx,dy in zip(dxArr,dyArr):
            if(l := self.CheckDepth(color,y,x,dy,dx,field),l!=-1):
                xx = x+dx
                yy = y+dy
                for _ in range(l):
                    if field[yy][xx] != color:
                        value += stoneMap[yy][xx]
                    xx += dx
                    yy += dy
        if self.PlayerColor == color:
            return -value
        else:
            return value
    
    def CalcValue(self,field,stoneMap):
        value = 0
        for y in range(self.Height):
                for x in range(self.Width):
                    if field[y][x] == self.PlayerColor:
                        value -=stoneMap[y][x]
                    elif field[y][x] == (self.PlayerColor + 1)%2:
                        value +=stoneMap[y][x]
        return value
    
    def GetPossiblePutPositionAndValue(self,color,stoneMap):
        positions = []
        values = []
        for y in range(self.Height):
            for x in range(self.Width):
                if self.CanPut(y,x,color,self.Field):
                    positions.append([y,x])
                    values.append(self.CalcStoneValue(y,x,color,self.Field,stoneMap))
        return positions,values

    def GetPossiblePutPosition(self,color,field,n,stoneMap,value = 0):
        positions = []
        values = []
        PossiblePositon = False 
        if n<self.NextMove:
            for y in range(self.Height):
                for x in range(self.Width):
                    if self.CanPut(y,x,color,field):
                        PossiblePositon = True
                        putField = self.Put(y,x,color,np.copy(field))
                        self.Execution[n] = self.Execution[n] + 1
                        subValue = self.CalcStoneValue(y,x,color,field,stoneMap) + np.copy(value)
                        # print("Execution = ",self.Execution,"\tclass = ",n,"\tPut = ",[y,x],"\tvalue = ",subValue)
                        self.Disp(putField)
                        if n == 0:
                            positions.append([y,x])
                        values.append(-self.GetPossiblePutPosition((color + 1)%2,putField,n + 1,stoneMap,np.copy(subValue)))
            if PossiblePositon is False:
                self.GetPossiblePutPosition((color + 1)%2,field,n + 1,stoneMap,np.copy(value))
            else:
                if values != []:
                    print("class = ",n,"\tvalues = ",values)
                if n == 0:
                    print("PossiblePositons = ",positions,"\tvalue = ",max(values))
                    return positions[np.argmax(values)]
                else:
                    return min(values)
                    # if self.PlayerColor == color:
                    #     return max(values)
                    # else:
                    #     return min(values)
        elif n == self.NextMove:
            # return self.CalcValue(field,stoneMap)
            if self.NextMove%2 == self.PlayerColor:
                return value
            else:
                return -value
            return value
        return 0
    
    def Result(self):
        n_white = 0
        n_black = 0
        n_sum = 0
        for y in range(self.Height):
            for x in range(self.Width):
                if self.Field[y][x] == -1:
                    continue
                n_sum += 1
                if self.Field[y][x] == 0:
                    n_white += 1
                if self.Field[y][x] == 1:
                    n_black += 1
        return n_white,n_black,n_sum
    
if __name__ == "__main__":
    o = Osero()
    color = 0
    o.PlayerColor = color
    stoneMap = [
            [ 30, -12,  0, -1, -1,   0, -12,  30],
            [-12, -15, -3, -3, -3, -15, -15, -12],
            [  0,  -3,  0, -1, -1,   0,  -3,   0],
            [ -1,  -3, -1, -1, -1,  -1,  -3,  -1],
            [ -1,  -3, -1, -1, -1,  -1,  -3,  -1],
            [  0,  -3,  0, -1, -1,   0,  -3,   0],
            [-12, -15, -3, -3, -3, -15, -15, -12],
            [ 30, -12,  0, -1, -1,   0, -12,  30],
            ]
    
    while(True):
        if color == 0:
            print("●の番です")
        else:
            print("○の番です")
        o.Disp(o.Field)
        arr,values = o.GetPossiblePutPositionAndValue(color,stoneMap)
        ## 二連続でどっちも置く場所がなければ終わり
        if len(arr) == 0:
            if flag:
                break
            color = (color + 1)%2
            flag = True
            continue
        else:
            flag = False
        if color == o.PlayerColor:
            print("おける場所")
            for (yy,xx) in arr:
                print("yy:",yy,"xx:",xx,"value:",o.CalcStoneValue(yy,xx,color,o.Field,stoneMap))
            y = int(input("y:"))
            x = int(input("x:"))
            if not o.CanPut(y, x, color,o.Field):
                print("置やんぞ!!")
            else:
                o.Put(y,x,color,o.Field)
                color = (color + 1)%2
        else:
            o.Execution = [0 for i in range(o.NextMove)]
            bestPosition = []
            bestPosition = o.GetPossiblePutPosition(np.copy(color),np.copy(o.Field),0,stoneMap)
            if bestPosition != []:
                print("Execution = ",o.Execution)
                print("BestPosition = ",bestPosition)
                o.Put(bestPosition[0],bestPosition[1],color,o.Field)
            else:
                print("BestPosition = None")
            color = (color + 1)%2

    n_white,n_black,n_sum = o.Result()
    print("white:",n_white,"black:",n_black,"total:",n_sum)
```
