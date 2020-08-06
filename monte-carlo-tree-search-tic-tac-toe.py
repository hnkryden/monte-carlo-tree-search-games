import numpy as np
from tictactoe.tictactoe import TicTacToeGameState
import random
from copy import deepcopy

res =[]
class MCTS:
    def __init__(self,_parent,_board_state,player):
        self.children=None
        self.wins = 0
        self.nsim = 0
        self.parent = _parent
        self.board_state = _board_state
        self.player = player 

    def select(self):
        if self.board_state.is_game_over():
            self.backpropagate(self.board_state.game_result)
        elif self.children:
            score =[c.getScore() 
                for c in self.children
            ]
            index = np.argmax(score)
            actions = self.board_state.get_legal_actions()
            self.children[index].board_state = self.board_state.move(actions[index])
            self.children[index].select()
        else:
            self.expand()
    def getScore(self):
        if self.nsim == 0:
            return 100
        s = self.wins/self.nsim + 1.41*np.sqrt(np.log(self.parent.nsim)/self.nsim) 
        return s

    def expand(self):
        actions = self.board_state.get_legal_actions()
        index = random.randrange(len(actions))
        # Next player is the opposite player
        self.board_state = self.board_state.move(actions[index])
        self.children = [MCTS(self,self.board_state,-1*self.player) for c in range(len(actions))] 
        self.children[index].simulate()

    def simulate(self):
        while not self.board_state.is_game_over():
            actions = self.board_state.get_legal_actions()
            
            self.board_state = self.board_state.move(random.choice(actions))
            #print(board_state.board)
           # print("simulating")
        self.backpropagate(self.board_state.game_result)
    def backpropagate(self,result):
        
        #print("backprop",self.wins,self.nsim)
        win = int(result==-self.player)
        loss = int(result==self.player)
        self.wins += win - loss
        self.nsim += 1
        if self.parent:
            self.parent.backpropagate(result)
        else: 
            res.append(result)
def findNextMove(board,player):
    boardCopy = deepcopy(board)
    rootNode = MCTS(None,boardCopy,player)
    for plays in range(3000):
        rootNode.board_state = deepcopy(board)
        rootNode.select()
    score =[c.getScore() 
        for c in rootNode.children
        ]
    index = np.argmax(score)
    actions = board_state.get_legal_actions()
    #for i in range(len(actions)):
        #print(actions[i].x_coordinate,actions[i].y_coordinate,np.round(score[i],3))
    return actions[index]
def playerNextMove(board):
    actions = board_state.get_legal_actions()
    for i in range(len(actions)):
        print(i,": ",actions[i].x_coordinate,actions[i].y_coordinate)
    action = input("Action: ")
    return actions[int(action)]

realPlayer=False
if __name__ == "__main__":
    
    for _ in range(100):
        state = np.zeros((3,3))
        player = 1
        board_state = TicTacToeGameState(state = state, next_to_move=player)
        for i in range(9):
            if realPlayer and (player==1):
                action = playerNextMove(board_state)
            else:
                action = findNextMove(board_state,player)
            board_state = board_state.move(action)
            player *= -1
            print(board_state.board)
            if board_state.is_game_over():
                print("Game over %d, player %d wins" % (i,board_state.game_result))
                break





