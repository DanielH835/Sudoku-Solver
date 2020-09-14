#!/usr/bin/env python
#coding:utf-8
import sys
import time
import statistics

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def check_board(board):
    #Code for check if all dict keys have value that is not zero
    for key in board:
        if board[key] == 0:
            return False
    
    return True

def unassigned_var(board):
    #MRV - Minimum Remaining Values
    #returns a variable from dict with the fewest legal values
    minVar = 11
    
    for var in board:
        if board[var] == 0:
            domain_length = len(get_domain(var, board))
            if domain_length < minVar:
                minVar = domain_length
                unassigned = var
    
    return unassigned

def check_neighbors(var, board):
    char = var[0]
    number = var[1]
    neighborsList = list()
    
    for i in COL:
        if char + i not in neighborsList:
            neighborsList.append(char + i)
        
    for i in ROW:
        if i + number not in neighborsList:
            neighborsList.append(i + number)
        
    if ord(char) < 68:
        if int(number) < 4:
            for i in range(ord('A'), ord('D')):
                for j in range(1, 4):
                    concat = chr(i) + str(j)
                    if concat not in neighborsList:
                        neighborsList.append(concat)
        elif 4 <= int(number) <= 6:        
            for i in range(ord('A'), ord('D')):
                for j in range(4, 7):
                    concat = chr(i) + str(j)
                    if concat not in neighborsList:
                        neighborsList.append(concat)
     
        elif int(number) > 7:
            for i in range(ord('A'), ord('D')):
                for j in range(7, 10):
                    concat = chr(i) + str(j)
                    if concat not in neighborsList:
                        neighborsList.append(concat)

    elif 68 <= ord(char) <= 70:
        if int(number) < 4:
            for i in range(ord('D'), ord('G')):
                for j in range(1, 4):
                    concat = chr(i) + str(j)
                    if concat not in neighborsList:
                        neighborsList.append(concat)
        elif 4 <= int(number) <= 6:        
            for i in range(ord('D'), ord('G')):
                for j in range(4, 7):
                    concat = chr(i) + str(j)
                    if concat not in neighborsList:
                        neighborsList.append(concat)
     
        elif int(number) > 7:
            for i in range(ord('D'), ord('G')):
                for j in range(7, 10):
                    concat = chr(i) + str(j)
                    if concat not in neighborsList:
                        neighborsList.append(concat)  
                        
    elif ord(char) > 70:
        if int(number) < 4:
            for i in range(ord('G'), ord('J')):
                for j in range(1, 4):
                    concat = chr(i) + str(j)
                    if concat not in neighborsList:
                        neighborsList.append(concat)
        elif 4 <= int(number) <= 6:        
            for i in range(ord('G'), ord('J')):
                for j in range(4, 7):
                    concat = chr(i) + str(j)
                    if concat not in neighborsList:
                        neighborsList.append(concat)
     
        elif int(number) > 7:
            for i in range(ord('G'), ord('J')):
                for j in range(7, 10):
                    concat = chr(i) + str(j)
                    if concat not in neighborsList:
                        neighborsList.append(concat)
    
    neighborsList.remove(var)
    return neighborsList
    
def get_domain(var, board):
    #returns the domain of var
    #checks row/column/square
    domain = list()
    for i in range(1, 10):
        domain.append(i)
    
    neighbors = check_neighbors(var, board)
    for neighbor in neighbors:
        if board[neighbor] > 0 and board[neighbor] in domain:
            domain.remove(board[neighbor])
    return domain

def forward_checking(value, variable, board):
    neighbors = check_neighbors(variable, board)
    
    for neighbor in neighbors:
        domain = get_domain(neighbor, board)
        if value in domain and len(domain) == 1:
            return False
    
    return True

def is_consistent(value, variable, board):
    neighbors = check_neighbors(variable, board)
    
    for neighbor in neighbors:
        if value == board[neighbor]:
            return False
    
    return True

def backtracking(board):
    """Takes a board and returns solved board."""
    
    if check_board(board) == True:
        return board

    variable = unassigned_var(board)
    domain = get_domain(variable, board)
    for value in domain:
        if is_consistent(value, variable, board) == True:
            board[variable] = value
            if forward_checking(value, variable, board) == True:
                result = backtracking(board)
                if not result == False:
                    return result
            board[variable] = 0
    
    return False

if __name__ == '__main__':

    if len(sys.argv) > 1:

        #  Read individual board from command line arg.
        sudoku = sys.argv[1]

        if len(sudoku) != 81:
            print("Error reading the sudoku string %s" % sys.argv[1])
        else:
            board = { ROW[r] + COL[c]: int(sudoku[9*r+c])
                      for r in range(9) for c in range(9)}
            
            print_board(board)

            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()
            
            print_board(solved_board)
            out_filename = 'output.txt'
            outfile = open(out_filename, "w")
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')


    else:

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        count = 0
        minTime = 1000
        maxTime = 0
        totalTime = 0
        sample = list()
        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                    for r in range(9) for c in range(9)}

            # Print starting board.
            print_board(board)

            # Solve with backtracking
            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()

            sample.append(end_time - start_time)
            totalTime += (end_time - start_time)
            # Print solved board. 
            if solved_board:
                print_board(solved_board)
                # Write board to file
                outfile.write(board_to_string(solved_board))
                outfile.write('\n')
                count += 1
                if minTime > (end_time - start_time):
                    minTime = (end_time - start_time)
                if maxTime < (end_time - start_time):
                    maxTime = (end_time - start_time)
                    
        readme_file = 'README.txt'
        readmeFile = open(readme_file, 'w')
        readmeFile.write("Number of solved boards: " + str(count) + '\n')
        readmeFile.write("Minimum Time: " + str(minTime) + '\n')
        readmeFile.write("Maximum Time: " + str(maxTime) + '\n')
        readmeFile.write("Mean Time: " + str(totalTime / count) + '\n')
        readmeFile.write("Standard Deviation: " + str(statistics.stdev(sample)) + '\n')
        
        print("Finishing all boards in file.")