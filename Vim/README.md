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

```python
import copy
import random

class OthelloAI:
    exe = 0
    def __init__(self, depth):
        self.depth = depth

    def evaluate_board(self, board, maximizing_player):
        player_piece = 'X' if maximizing_player else 'O'
        opponent_piece = 'O' if maximizing_player else 'X'

        player_score = 0
        opponent_score = 0

        # マスの評価値
        position_values = [
            [30, -12, 0, -1, -1, 0, -12, 30],
            [-12, -15, -3, -3, -3, -3, -15, -12],
            [0, -3, 0, -1, -1, 0, -3, 0],
            [-1, -3, -1, -1, -1, -1, -3, -1],
            [-1, -3, -1, -1, -1, -1, -3, -1],
            [0, -3, 0, -1, -1, 0, -3, 0],
            [-12, -15, -3, -3, -3, -3, -15, -12],
            [30, -12, 0, -1, -1, 0, -12, 30]
        ]

        for i in range(8):
            for j in range(8):
                if board[i][j] == player_piece:
                    player_score += position_values[i][j]
                elif board[i][j] == opponent_piece:
                    opponent_score += position_values[i][j]

        return player_score - opponent_score

    def nega_alpha(self, board, depth, alpha, beta, maximizing_player):
        self.exe += 1
        if depth == 0 or self.is_game_over(board):
            return self.evaluate_board(board, maximizing_player)

        legal_moves = self.get_legal_moves(board, maximizing_player)

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = self.make_move(copy.deepcopy(board), move, maximizing_player)
                eval = self.nega_alpha(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = self.make_move(copy.deepcopy(board), move, maximizing_player)
                eval = self.nega_alpha(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, board, player):
        legal_moves = self.get_legal_moves(board, player)
        best_moves = [legal_moves[0]]
        max_eval = float('-inf')

        for move in legal_moves:
            new_board = self.make_move(copy.deepcopy(board), move, player)
            eval = self.nega_alpha(new_board, self.depth - 1, float('-inf'), float('inf'), False)

            if eval > max_eval:
                max_eval = eval
                best_moves = [move]
            elif eval == max_eval:
                best_moves.append(move)

        return random.choice(best_moves)

    def is_game_over(self, board):
        return not any(' ' in row for row in board) or (not self.get_legal_moves(board, True) and not self.get_legal_moves(board, False))

    def get_legal_moves(self, board, player):
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(board, i, j, player):
                    legal_moves.append((i, j))
        return legal_moves

    def is_valid_move(self, board, row, col, player):
        if board[row][col] != ' ':
            return False

        opponent_piece = 'O' if player else 'X'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self.is_inside_board(r, c) and board[r][c] == opponent_piece:
                while self.is_inside_board(r, c) and board[r][c] == opponent_piece:
                    r += dr
                    c += dc
                if self.is_inside_board(r, c) and board[r][c] == ('X' if player else 'O'):
                    return True

        return False

    def is_inside_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def make_move(self, board, move, player):
        row, col = move
        player_piece = 'X' if player else 'O'
        opponent_piece = 'O' if player else 'X'

        if board[row][col] != ' ':
            raise ValueError("Invalid move. The cell is not empty.")

        board[row][col] = player_piece

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            flipped = False
            while self.is_inside_board(r, c) and board[r][c] == opponent_piece:
                flipped = True
                r += dr
                c += dc

            if self.is_inside_board(r, c) and board[r][c] == player_piece and flipped:
                r, c = row + dr, col + dc
                while board[r][c] == opponent_piece:
                    board[r][c] = player_piece
                    r += dr
                    c += dc

        return board


class OthelloGame:
    def __init__(self):
        self.board = self.initialize_board()

    def initialize_board(self):
        board = [[' ' for _ in range(8)] for _ in range(8)]
        board[3][3] = 'O'
        board[3][4] = 'X'
        board[4][3] = 'X'
        board[4][4] = 'O'
        return board

    def display_board(self):
        print("   0  1  2  3  4  5  6  7")
        print(" + -+ -+ -+ -+ -+ -+ -+ -")
        for i, row in enumerate(self.board):
            print(f"{i}|", end=" ")
            for cell in row:
                print(cell, end="| ")
            print("")
        print(" +-+-+-+-+-+-+-+-")
    
    def get_scores(self):
        player_score = sum(row.count('X') for row in self.board)
        opponent_score = sum(row.count('O') for row in self.board)
        return player_score, opponent_score

    def play_game(self):
        ai = OthelloAI(depth=7)
        player_turn = True

        while not self.is_game_over():
            self.display_board()

            if player_turn:
                self.ai_move(ai)
            else:
                self.ai_move(ai)

            player_turn = not player_turn

        self.display_board()
        player_score, opponent_score = self.get_scores()
        print(f"Player Score: {player_score}")
        print(f"AI Score: {opponent_score}")
        if player_score > opponent_score:
            print("Player wins!")
        elif player_score < opponent_score:
            print("AI wins!")
        else:
            print("It's a draw!")
        print("Game Over")

    def player_move(self):
        try:
            row = int(input("Enter the row (0-7): "))
            col = int(input("Enter the column (0-7): "))
            if self.is_valid_move(row, col, True):
                self.make_move(row, col, True)
            else:
                print("Invalid move. Try again.")
                self.player_move()
        except ValueError:
            print("Invalid input. Please enter a number.")
            self.player_move()

    def ai_move(self, ai):
        print("AI's move:")
        ai.exe = 0
        move = ai.get_best_move(self.board, False)
        self.make_move(move[0], move[1], False)
        print("execution",ai.exe)

    def is_valid_move(self, row, col, player):
        if self.board[row][col] != ' ':
            return False

        opponent_piece = 'O' if player else 'X'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self.is_inside_board(r, c) and self.board[r][c] == opponent_piece:
                while self.is_inside_board(r, c) and self.board[r][c] == opponent_piece:
                    r += dr
                    c += dc
                if self.is_inside_board(r, c) and self.board[r][c] == ('X' if player else 'O'):
                    return True

        return False

    def is_game_over(self):
        return not any(' ' in row for row in self.board) or (not self.get_legal_moves(True) and not self.get_legal_moves(False))

    def get_legal_moves(self, player):
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j, player):
                    legal_moves.append((i, j))
        return legal_moves

    def is_inside_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def make_move(self, row, col, player):
        player_piece = 'X' if player else 'O'
        opponent_piece = 'O' if player else 'X'

        if self.board[row][col] != ' ':
            raise ValueError("Invalid move. The cell is not empty.")

        self.board[row][col] = player_piece

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            flipped = False
            while self.is_inside_board(r, c) and self.board[r][c] == opponent_piece:
                flipped = True
                r += dr
                c += dc

            if self.is_inside_board(r, c) and self.board[r][c] == player_piece and flipped:
                r, c = row + dr, col + dc
                while self.board[r][c] == opponent_piece:
                    self.board[r][c] = player_piece
                    r += dr
                    c += dc


# 使用例
if __name__ == "__main__":
    game = OthelloGame()
    game.play_game()
```
