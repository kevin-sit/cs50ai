"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_x = 0
    num_o = 0
    for row in board:
        for cell in row:
            if (cell == X):
                num_x += 1
            elif (cell == O):
                num_o += 1
    if num_x == num_o:
        return X
    else:
        return O            
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set=set()
    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):
                action_set.add((i, j))
    return action_set         


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result = copy.deepcopy(board)
    (i, j) = action
    c_player = player(board)
    result[i][j] = c_player
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O
    
    tboard = 3*[3*[0]]
    for i in range(3):
        for j in range(3):
            tboard[i][j]= board[j][i]
    for j in range(3):
        if tboard[j].count(X) == 3:
            return X
        elif tboard[j].count(O) == 3:
            return O
    
    dia1 = []
    dia2 = []
    for i in range(3):
        dia1.append(board[i][i])
        dia2.append(board[i][2-i])
    if dia1.count(X) == 3 or dia2.count(X) == 3:
        return X
    elif dia2.count(O) == 3 or dia2.count(O) == 3:
        return O
    
    return None

            


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if any(row.count(EMPTY) != 0 for row in board):
        if winner(board) == X or winner(board) == O:
            return True
        else: 
            return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """            
    if terminal(board):
        return None
    else:
        if player(board) == X:
            ou = 9
        else:
            ou = -9
        (null, action) = cu(board,ou)
        return action
        
 
def cu(board, lu):
    if player(board) == X:
        ou = -9
    else:
        ou = 9
    oaction = (0,0)
    for action in actions(board):
        new_board = result(board,action)

        if terminal(new_board):
            u = utility(new_board)
        else:
            (u, null) = cu(new_board, ou)

        if player(board) == X and u > ou:
            ou = u
            oaction = action
        elif player(board) == O and u < ou:
            ou = u
            oaction = action
        if (player(board) == X and u > lu) or (player(board) == O and u < lu):
            break
    return ou, oaction
"""
        if player(board) == X and u > lu:
            continue
        elif player(board) == O and u < lu:
            continue
"""

            
   
'''
                if u < ou:
                    return ou, oaction
                else:
                    lou = u
            else:
                if u > ou:
                    return ou
                else:
                    ou = u'''
        
                