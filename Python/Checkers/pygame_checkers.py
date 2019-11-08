import pygame
import sys

WHITE = (255,255,255)
RED = (200,0,0)
BLACK = (0,0,0)
RADIUS = 40

class board:
    def __init__(self):
        self.board = [['-',1,'-',1,'-',1,'-',1],
                 [1,'-',1,'-',1,'-',1,'-'],
                 ['-',1,'-',1,'-',1,'-',1],
                 [0,'-',0,'-',0,'-',0,'-'],
                 ['-',0,'-',0,'-',0,'-',0],
                 [2,'-',2,'-',2,'-',2,'-'],
                 ['-',2,'-',2,'-',2,'-',2],
                 [2,'-',2,'-',2,'-',2,'-']]
        self.turn = 1
        self.score =[0,0]

    def print_board(self):
        overline = u"\u203E" #opposite of underscore
        print("   1   2   3   4   5   6   7   8")
        for line in range(len(self.board)):
            print(" "+("|"+3*overline)*8+"|")
            if line%2 == 0:
                print(str(line+1)+"|   | "+str(self.board[line][1])+" |   | "+str(self.board[line][3])+" |   | "+str(self.board[line][5])+" |   | "+str(self.board[line][7])+" |")
            else:
                print(str(line+1)+"| "+str(self.board[line][0])+" |   | "+str(self.board[line][2])+" |   | "+str(self.board[line][4])+" |   | "+str(self.board[line][6])+" |   |")
            
        print('  '+(overline*3+' ')*8)
    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        print("Player"+str(self.turn)+"'s turn!")
    def move_piece(self,old,new): #tuple of old location and new location given..... old[row][col] new[row][col]
        self.board[new[0]][new[1]] = self.board[old[0]][old[1]]
        self.board[old[0]][old[1]] = 0
    def jump_available(self,piece):
        self.board[piece[0]][piece[1]]
        if self.turn==1:
            if piece[0]>5:
                return False
            if piece[1]<6:
                if self.board[piece[0]+1][piece[1]+1] == 2:
                    if self.board[piece[0]+2][piece[1]+2] == 0:
                        return True
            if piece[1]>2:
                if self.board[piece[0]+1][piece[1]-1] == 2:
                    if self.board[piece[0]+2][piece[1]-2] == 0:
                        return True
        else:
            if piece[0]<2:
                return False
            if piece[1]<6:
                if self.board[piece[0]-1][piece[1]+1] == 1:
                    if self.board[piece[0]-2][piece[1]+2] == 0:
                        return True
            if piece[1]>2:
                if self.board[piece[0]-1][piece[1]-1] == 1:
                    if self.board[piece[0]-2][piece[1]-2] == 0:
                        return True
        return False
        
    def jump(self,old,new): #already checked if it is a valid move
        if abs(old[0]-new[0]) == 2 and abs(old[1]-new[1]) == 2: #if they just jumped, remove a piece
            #self.score[self.board[new[0]][new[1]]-1]+=1
            self.score[self.turn-1]+=1
            self.board[old[0]+(new[0]-old[0])//2][old[1]+(new[1]-old[1])//2]=0
            return True
        else:
            return False

    def jump_again(self,new):
        if(self.jump_available(new)):
            double_jump = input("Jump again?(row,col)")
            new_new = double_jump.split(',')
            new_new[0] = int(new_new[0])-1
            new_new[1] = int(new_new[1])-1
            return(new,new_new,True)#old,new
        else:
            return new,new,False
            
    def check_king(self): #check if checker was moved somewhere where it would become a king
        pass
    def king(self): #make checker a king. check_king and validity where already done
        pass
    def is_valid_move(self,old,new):
        #trying to move to a spot too far away 
        #trying to move in wrong direction                         CHECK
        #trying to move wrong piece or to a spot that is not empty CHECK
        #check if it is a jump

        if self.turn != self.board[old[0]][old[1]]: #trying to move an opponent's piece
            return False
        if self.board[new[0]][new[1]] != 0: #trying to move to a spot that is not empty or not in play
            return False
        if self.turn == 1 and self.board[old[0]][old[1]] == 1: #if it is player 1's turn and they are moving a normal piece
            if new[0] - old[0] == 1 and abs(new[1] - old[1]) == 1: #regular move with regular piece
                return True
            if old[0] - new[0] == 1: #moving normal piece wrong direction
                return False
            if new[0] - old[0] == 2 and abs(new[1]-old[1]) == 2: #if moving for a jump
                if self.board[old[0]+1][old[1]+(new[1]-old[1])//2] == 2: #jump if there is a piece to jump
                    return True

        if self.turn == 2 and self.board[old[0]][old[1]] == 2: #if it is player 2's turn and they are moving a normal piece
            if old[0] - new[0] == 1 and abs(new[1]-old[1]) == 1: #regular move with regular piece
                return True
            if new[0] - old[0] == 1: #moving normal piece wrong direction
                return False
            if old[0] - new[0] == 2 and abs(new[1]-old[1]) == 2: #if moving for a jump
                if self.board[old[0]-1][old[1]+(new[1]-old[1])//2] == 1: #jump if there is a piece to jump
                    return True

    def draw_board(self,screen):
        pygame.draw.rect(screen,WHITE,(0,0,800,800))
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if ((row+1)%2==1 and (col+1)%2==0) or ((row+1)%2==0 and (col+1)%2==1):
                    pygame.draw.rect(screen,RED,(col*100,row*100,100,100))
                if self.board[row][col]==1:
                    pygame.draw.circle(screen,WHITE,(col*100+50,row*100+50),RADIUS)
                if self.board[row][col]==2:
                    pygame.draw.circle(screen,BLACK,(col*100+50,row*100+50),RADIUS)

        

def get_move():
    first_click = input('choose the one you want to move! (row,col):')
    old = first_click.split(',')
    old[0] = int(old[0])-1
    old[1] = int(old[1])-1
    first_click = input('choose where you want to move! (row,col):')
    new = first_click.split(',')
    new[0] = int(new[0])-1
    new[1] = int(new[1])-1
    return(old,new)



checkers = board()
#checkers.print_board()
#checkers.move_piece([3,4],[4,5])
#checkers.print_board()

SQUARESIZE = 100
width = SQUARESIZE*len(checkers.board)
height = SQUARESIZE*len(checkers.board[0])
size = (width,height)

pygame.init()

screen = pygame.display.set_mode(size)

while(True):
    #for event in pygame.event.get():
        #if event.type == pygame.QUIT:
            #sys.exit()
        #if event.type == pygame.MOUSEBUTTONDOWN:
    checkers.print_board()
    checkers.draw_board(screen)
    while(True):
        old,new = get_move()
        if(checkers.is_valid_move(old,new)):
            break
    checkers.move_piece(old,new)
    if(checkers.jump(old,new)):
        old,new,check = checkers.jump_again(new)
        if check:
            checkers.move_piece(old,new)
        checkers.jump(old,new)
    checkers.change_turn()