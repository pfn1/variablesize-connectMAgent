#ConnectM Game Group 5
import math
import sys
import random
import copy

#global variables for the board
HUMAN = "_X_"
COMPUTER = "_O_"
BLANK = "___"

#2d array creation representing board
def create_board(rows, cols):
   board = [[BLANK for col in range(cols)] for row in range(rows)]
   return board

#printing ascii representation of board
def print_board(board):
   for row in board:
      print("|"+ "|".join(row) + "|")    

#checks if column is available
def valid_column(board, inputCol):
   for row in range(len(board)-1, -1, -1):
      if board[row][inputCol] == BLANK:
         return True
   return False

#drops piece if column available
def column_select(board, inputCol, player):
   for row in range(len(board)-1, -1, -1):
      if board[row][inputCol] == BLANK:
         board[row][inputCol] = player
         return True
   return False

def get_next_open_row(board, col):
	for r in range(len(board)):
		if board[r][col] == BLANK:
			return r

#function for checking winning connections
def check_win_condition(board, player, connectWin):
   #horizontal check
   for row in range(len(board)):
      for col in range(len(board[0]) - connectWin + 1):
         if all (board[row][col + i] == player for i in range(connectWin)):
            return True
         
   #vertical check
   for col in range(len(board[0])):
      for row in range(len(board) - connectWin + 1):
         if all(board[row + i][col] == player for i in range(connectWin)):
            return True
         
   #negative slope diagonal check
   for col in range(len(board[0]) - connectWin + 1):
      for row in range(len(board) - connectWin + 1): 
         if all(board[row + i][col + i] == player for i in range(connectWin)):
            return True
   
   #positive slope diagonal check
   for col in range(len(board[0]) - connectWin + 1):
      for row in range((len(board) - connectWin + 1), len(board)): 
         if all(board[row - i][col + i] == player for i in range(connectWin)):
            return True
   return False


#assign scores for possible straight pieces positions passed as a list
def assign_score(possible_connect, player):
   score = 0
   opponent = '_X_'
   if player == '_X_':
      opponent = '_O_'
   
   if possible_connect.count(player) == 4:  #win potential
            score += 50
   elif possible_connect.count(player) == 3 and possible_connect.count(BLANK) == 1:
            score += 20
   elif possible_connect.count(player) == 2 and possible_connect.count(BLANK) == 2:
            score += 10
   #negative score for good opponent positions
   if possible_connect.count(opponent) == 3 and possible_connect.count(BLANK) == 1:
            score -= 20
   return score


# Evaluation function to evaluate remaining squares. 
# Projects dropping a piece into column and see if its a good position. By checking possible good connections
# This will call the scoring function
def evaluate_position(board, player, connectWin):
   score = 0
   #check horizontal / row pieces for possible high value positions
   for row in range(len(board)):
      for col in range(len(board[0]) - connectWin + 1):
         possible_col_connects = [board[row][col + i] for i in range(connectWin)]
         score += assign_score(possible_col_connects, player)

   #check vertical / column pieces for high value positions
   col_array = []
   for col in range(len(board[0])):
      col_array = []
      for i in range(len(board)):
         col_array.append(board[i][col])

      for row in range(len(board) - connectWin + 1):
         possible_col_connects = col_array[row : row + connectWin]
         score += assign_score(possible_col_connects, player)
   
   #check positive slope pieces for high value positions
   for col in range(len(board[0]) - connectWin + 1):
      for row in range((len(board) - connectWin + 1), len(board)):
         possible_col_connects = [board[row - i][col + i] for i in range(connectWin)]
         score += assign_score(possible_col_connects, player)

   #check negative slope pieces for high value positions
   for col in range(len(board[0]) - connectWin + 1):
      for row in range(len(board) - connectWin + 1): 
         possible_col_connects = [board[row + i][col + i] for i in range(connectWin)]
         score += assign_score(possible_col_connects, player)

   return score

#function to checks if column still has space
def get_valid_columns(board):
   valid_columns_arr = []
   for col in range(len(board)):
      if valid_column(board, col):
         valid_columns_arr.append(col)
   return valid_columns_arr


#checks if board is terminal and next move is a win or board will be full
#this will only be called during minmax process
def terminal_board(board, connectWin):
   return check_win_condition(board, HUMAN, connectWin) or check_win_condition(board, COMPUTER, connectWin) or len(get_valid_columns(board)) == 0

#minmax function
def minmax(board, depth, alpha, beta, maximizingPlayer, connectWin):
   valid_columns = get_valid_columns(board)
   is_terminal = terminal_board(board, connectWin)

   #base cases depth and terminal board
   #early return with highscore if board is terminal
   if is_terminal:
      if check_win_condition(board, COMPUTER, connectWin):
         return (None, 1000)
      elif check_win_condition(board, HUMAN, connectWin):
         return (None, -1000)
      else:
         return (None, 0)
   
   #return if depth is zero with highest evaluation
   if depth == 0:
      return (None, evaluate_position(board, COMPUTER, connectWin))
   
   #MAX
   if maximizingPlayer:
      value = -math.inf
      column = random.choice(valid_columns)
      for col in valid_columns:
         possible_board = copy.deepcopy(board)   #copies gameboard for use in scenario dropping of pieces
         column_select(possible_board, col, COMPUTER)  #scenario drop for each valid column
         new_score = minmax(possible_board, depth-1, alpha, beta, False, connectWin)[1] #recursion / assigns index 1(value) only
         if new_score > value:
            value = new_score
            column = col
         alpha = max(alpha, value) 
         if alpha >= beta: #pruning
             break
      return column, value
   
   else:
      value = math.inf
      column = random.choice(valid_columns)
      for col in valid_columns:
         possible_board = copy.deepcopy(board)
         column_select(possible_board, col, HUMAN)
         new_score = minmax(possible_board, depth-1, alpha, beta, True, connectWin)[1] #recursion / assigns index 1(value) only
         if new_score < value:
            value = new_score
            column = col
            
         beta = min(beta, value)
         if alpha >= beta: #pruning
             break
      return column, value
      
#main function
def main():
   #store all command line arguments
   args = sys.argv[1:]
   rows = int(args[0])
   cols = int(args[0])
   connectWin = int(args[1])
   turn = args[2]

   # CLI argument check
   if(cols < 3 or cols > 10):
      print('Grid must be at least 3 and not more than 10.')
      sys.exit()
   if(connectWin < 2 or connectWin > cols):
      print('Win connection must be at least 2 and not more than grid size.')
      sys.exit()

   #initial conditions and reate board
   totalTurns = 0
   depth = 4
   boardOne = create_board(rows, cols)
   
   #initial board printout
   print_board(boardOne)

   while True:
      #player's turn first set to default
      if turn == '1':
         try:
            colInput = int(input("Please enter column number to drop your piece: ")) - 1
            if colInput < 0 or colInput >= cols:
               print("Invalid column number. Please try again.")
               continue
            if not column_select(boardOne, colInput, HUMAN):
               print('Column is full.  Select another column.')
               continue
            turn = '0'
            print_board(boardOne)
            if(check_win_condition(boardOne, HUMAN, connectWin)):
               print('You Win!')
               break
         except ValueError:
            print("Oops!  That was no valid number.  Try again...")
      
      #computer's move execute min-max
      else:
         print('Computer moves!')
      
         # Call minmax function / returns score and column input
         # Depth set to 4  / lowest level min.  
         colInput, minmax_score = minmax(boardOne, depth, -math.inf, math.inf, True, connectWin)

         print('Column: ' + str(colInput+1))

         if colInput < 0 or colInput >= cols:
            print("Invalid column number. Please try again.")
            continue
         if not column_select(boardOne, colInput, COMPUTER):
            print('Column is full.  Select another column.')
            continue
         turn = '1'
         print_board(boardOne)
         if(check_win_condition(boardOne, COMPUTER, connectWin)):
            print('Computer Wins!')
            break

      #turn counter until total board size
      totalTurns += 1

      #draw condition
      if totalTurns == rows * cols:
         print("It's a draw!")
         break

if __name__ == '__main__':
   main()