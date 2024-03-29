# Vim
<img src="https://github.com/ntaku256/AI/blob/main/Source/VimKeySettings.png" width="100%">

```python
            import copy
            import random
            import pyodide
            from js import console, document
            from pyodide.ffi.wrappers import add_event_listener
            def do_flip(x, y, color):
                            js.document.getElementById('%d_%d' % (x, y)).color = color
                            img = js.document.getElementById('img%d_%d' % (x, y))
                            if color == 'O':
                                img.src = 'https://raw.githubusercontent.com/pukie/othello-game/master/images/white.png'
                                img.style.visibility = 'visible'
                            if color == 'X':
                                img.src = 'https://raw.githubusercontent.com/pukie/othello-game/master/images/black.png'
                                img.style.visibility = 'visible'
                            if color == ' ':
                                img.style.visibility = 'hidden'

            class OthelloAI:
                def __init__(self, depth):
                    self.depth = depth

                def evaluate_board(self, board, maximizing_player):
                    player_piece = 'X' if maximizing_player else 'O'
                    opponent_piece = 'O' if maximizing_player else 'X'
            
                    player_score = 0
                    opponent_score = 0

                    # マスの評価値
                    position_values = [
                        [60, -12, 0, -1, -1, 0, -12, 60],
                        [-12, -15, -3, -3, -3, -3, -15, -12],
                        [0, -3, 0, -1, -1, 0, -3, 0],
                        [-1, -3, -1, -1, -1, -1, -3, -1],
                        [-1, -3, -1, -1, -1, -1, -3, -1],
                        [0, -3, 0, -1, -1, 0, -3, 0],
                        [-12, -15, -3, -3, -3, -3, -15, -12],
                        [60, -12, 0, -1, -1, 0, -12, 60]
                    ]

                    for i in range(8):
                        for j in range(8):
                            if board[i][j] == player_piece:
                                player_score += position_values[i][j]
                            elif board[i][j] == opponent_piece:
                                opponent_score += position_values[i][j]

                    return - player_score + opponent_score

                def nega_alpha(self, board, depth, alpha, beta, maximizing_player):
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
                    best_move = [legal_moves[0]]
                    max_eval = float('-inf')

                    for move in legal_moves:
                        new_board = self.make_move(copy.deepcopy(board), move, player)
                        eval = self.nega_alpha(new_board, self.depth - 1, float('-inf'), float('inf'), False)
                                
                        if eval > max_eval:
                            max_eval = eval
                            best_moves = [move]
                        elif eval == max_eval:
                            best_moves.append(move)
                                
                    print(max_eval)
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
                player_turn = True
                boaard = None

                def __init__(self):
                    self.initialize_board()

                def initialize_board(self):
                    self.board = [[' ' for _ in range(8)] for _ in range(8)]
                    self.board[3][3] = 'O'
                    self.board[3][4] = 'X'
                    self.board[4][3] = 'X'
                    self.board[4][4] = 'O'

                def display_board(self):
                    print("  0 1 2 3 4 5 6 7")
                    print(" +-+-+-+-+-+-+-+-")
                    for i, row in enumerate(self.board):
                        print(f"{i}|", end=" ")
                        for cell in row:
                            print(cell, end=" ")
                        print("|")
                    print(" +-+-+-+-+-+-+-+-")
                    for i in range(8):
                        for j in range(8):
                            do_flip(i,j,self.board[i][j])
                        
                def get_scores(self):
                    player_score = sum(row.count('X') for row in self.board)
                    opponent_score = sum(row.count('O') for row in self.board)
                    return player_score, opponent_score

                def play_game(self):
                    ai = OthelloAI(depth=4)

                    while not self.is_game_over():
                        self.display_board()

                        if self.player_turn:
                            return
                        else:
                            self.ai_move(ai)

                        self.player_turn = not self.player_turn

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

                def player_move(self,row,col):
                    try:
                        # row = int(input("Enter the row (0-7): "))
                        # col = int(input("Enter the column (0-7): "))
                        if self.is_valid_move(row, col, True):
                            self.make_move(row, col, True)
                        else:
                            print("Invalid move. Try again.")
                            self.player_move()
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        self.player_move()
                    self.player_turn = not self.player_turn
                    self.play_game()

                def ai_move(self, ai):
                    print("AI's move:")
                    move = ai.get_best_move(self.board, False)
                    self.make_move(move[0], move[1], False)

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

            game = OthelloGame()

            def on_click(e):
                x, y = [int(i) for i in e.target.id.split('_')]
                print("[ "+str(x)+" , "+str(y)+" ]")
                game.player_move(x,y)

            board = js.document.getElementById('board')
            for i in range(8):
                tr = js.document.createElement('tr')
                for j in range(8):
                    td = js.document.createElement('td')
                    td.style.background = 'green'
                    td.style.border = '1px solid black'
                    td.width = td.height = 75
                    td.align = 'center'
                    td.id = '%d_%d' % (i, j)
                    td.color = 'empty'
                    
                    add_event_listener(td, "click", on_click)
                    img = js.document.createElement('img')
                    img.id = 'img%d_%d' % (i, j)
                    td.appendChild(img)
                    tr.appendChild(td)
                board.appendChild(tr)

            game.display_board()
            
            def Reset():    
                game.player_turn = True
                game.initialize_board()
                game.display_board()
                print("●の番です")

            def InstaReset():
                n_iters = 30

            def PSOReset():
                n_iters = 30
```
