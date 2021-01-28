import copy
import enum
import queue
from heapq import heappush, heappop, heapify 
import time

# Writ by JSkyes
# Created on 1/27/2020
# Program to create and run a modified 8 block puzzle game. 

def startGame():
    """Method to start the game rather than have the user have to manually go into my code and type to start the game"""
    userDifficulty = ""
    while True:
        # find and create the game based on the difficulty the user wants
        userDifficulty=str(input("Which difficulty would you like the game to be at?\nOptions are 'easy', 'medium', or 'hard': \n")).lower()
        if (userDifficulty == "easy"):
            difficulty = 1
        elif (userDifficulty == "medium"):
            difficulty = 2
        elif (userDifficulty == "hard"):
            difficulty = 3
        else:
            print("I'm sorry we don't have that difficulty or you spelled something wrong. Please try again!")
            return
        game = Game(difficulty, None)
        # find the algorithim the user desires, then use it on the created game above, printing the steps last
        userAlg=str(input("Which algorithim would you like the game to be solved by?\nOptions are 'bfs', 'dfs', 'uniform', 'greedy', 'a*h1', or 'a*man':\n")).lower()
        alg = Algorithms(game)
        if (userAlg == "bfs"):
            start=time.time()
            node = alg.breadthFirstSearch(game)
            alg.printPath(node, "Breadth First Search")
            end=time.time()
        elif (userAlg == "dfs"):
            start=time.time()
            node = alg.depthFirstSearch(game)
            alg.printPath(node, "Depth First Search")
            end=time.time()
        elif (userAlg == "uniform"):
            start=time.time()
            node = alg.uniformCostSearch(game)
            alg.printPath(node, "Uniform Cost Search")
            end=time.time()
        elif (userAlg == "greedy"):
            start=time.time()
            node = alg.greedyBestFirstSearch(game)
            alg.printPath(node, "Greedy Best First Search")
            end=time.time()
        elif (userAlg == "a*h1"):
            start=time.time()
            node = alg.aStarH1Search(game)
            alg.printPath(node, "A* H1 Search")
            end=time.time()
        elif (userAlg == "a*man"):
            start=time.time()
            node = alg.aStarManhattanSearch(game)
            alg.printPath(node, "A* H2 Manhattan Search")
            end=time.time()
        else:
            print("I'm sorry we don't have that algorithim or you spelled something wrong. Please try again!")
        print("The depth of the solution was: " + str(node.record.depth) + " layers.")
        print("The time it took for the algorithim to solve the puzzle at " + userDifficulty + " difficulty was: " + str((end-start)) + " second(s).")
        break

class Game:
    gameboard = []
    zeroIndex = 0
    hasEnded = True
    correctSolution = [1,2,3,8,0,4,7,6,5]

    def __init__(self, difficulty, board):
        """
        Method to intialize the game. Difficulty goes as follows:
        1 = Easy
        2 = Medium
        3 = Hard
        """
        if (difficulty == None):
            # we're creating a game board for the solution
            self.gameboard = board
            return
        
        if (difficulty == 1):
            self.gameboard = [1,3,4,8,6,2,7,0,5]
            self.zeroIndex = 7
            print("Let's begin! Easy mode start:")
            print(self.returnStringGameboard())
            self.hasEnded = False
        elif (difficulty == 2):
            self.gameboard = [2,8,1,0,4,3,7,6,5]
            self.zeroIndex = 3
            print("Let's begin! Medium mode start:")
            print(self.returnStringGameboard())
            self.hasEnded = False
        elif (difficulty == 3):
            self.gameboard = [5,6,7,4,0,8,3,2,1]
            self.zeroIndex = 4
            print("Let's begin! Hard mode start:")
            print(self.returnStringGameboard())
            self.hasEnded = False

    def checkIfWon(self):
        """
        Method that will run after each move to check if the player has reached the goal state
        """
        diff = False
        index = 0    
        corVal = 0
        curGameVal = 0
        
        while (not diff and index < 8):
            corVal = self.correctSolution[index]
            curGameVal = self.gameboard[index]
            if (corVal != curGameVal):
                diff = True
                return
            index = index + 1
        self.hasEnded = True
        print("You've found the correct solution!")
        print(self.returnStringGameboard())

    def reportMoveCostViaMoveType(self, action):
        """Helper function to report the move cost"""
        if (action == Action.Up):
            return self.gameboard[self.zeroIndex-3]
        elif(action == Action.Right):
            return self.gameboard[self.zeroIndex+1]
        elif(action == Action.Down):
            return self.gameboard[self.zeroIndex+3]
        elif(action == Action.Left):
            return self.gameboard[self.zeroIndex-1]

    def swap(self, zeroIndex, indexMovingTo):
        """Method to easily swap the values in the gameboard"""
        temp = self.gameboard[indexMovingTo]
        self.gameboard[indexMovingTo] = 0
        self.gameboard[zeroIndex] = temp
        self.zeroIndex = indexMovingTo
        
    def returnStringGameboard(self):
        """
        Method for UI viewing of the game.
        """
        strGameboard = ""
        for index in range(0,9):
            if (index%3 == 0 and index != 0):
                strGameboard = strGameboard +  "\n" + str(self.gameboard[index]) + " "
            else:
                strGameboard = strGameboard  + str(self.gameboard[index]) + " "
        return (strGameboard + "\n")

    def move(self, action):
        """
        Method to move the empty space in one of the four directions. The direction count follows the compass: 1 North/Up, 2 East/Right, 3 South/Down, and 4 West/Left.
        """
        if (not self.hasEnded):
            if (action == Action.Up and self.zeroIndex > 2):
                # that means it can move up!
                self.swap(self.zeroIndex, self.zeroIndex-3)
                
            elif (action == Action.Right and self.zeroIndex < 8):
                self.swap(self.zeroIndex, self.zeroIndex+1)

            elif (action == Action.Down and self.zeroIndex < 6):
                self.swap(self.zeroIndex, self.zeroIndex+3)

            elif (action == Action.Left and self.zeroIndex > 0):
                self.swap(self.zeroIndex, self.zeroIndex-1)

class Action(enum.Enum):
    """To make the actions easier to understand rather than simply numbers"""
    Up = 1
    Right = 2
    Down = 3
    Left = 4

class BookKeeping:
    """Class to manage all the statistics about the nodes outside of the nodes themselves"""
    pathcost = 0
    action = Action
    depth = 0
    expanded = False

    def __init__(self, pathcost, action, depth, expanded):
        self.pathcost = pathcost
        self.action = action
        self.depth = depth
        self.expanded = expanded

class Node:
    prev = None
    # next can be a list of nodes
    next = None
    record = None
    game = None

    def __init__(self, prev, next, record, game):
        self.prev = prev
        self.next = next
        self.record = record
        self.game = game

    def __lt__(self, otherNode):
        """A method that compares the node's records depth. Used for priority Queues"""
        return self.record.depth < otherNode.record.depth

    def __gt__(self, otherNode):
        """A method that compares the node's records depth. Used for priority Queues"""
        return self.record.depth > otherNode.record.depth

class Algorithms:
    intialState = []
    def __init__(self, game):
        self.intialState = game.gameboard

    def checkNextMoves(self, game, node):
        """A helper method to see if which of the actions are viable to the square and return all viable ones in a list"""
        nextMoves = []
        if (game.zeroIndex > 2):
            # a new record is made with the pathcost of the previous + the path cost of the current
            # actions is pretty easy, depth is prev node depth + 1
            newGame = copy.deepcopy(game)
            newGame.move(Action.Up)
            record = BookKeeping(node.record.pathcost + game.reportMoveCostViaMoveType(Action.Up), Action.Up, node.record.depth+1, False)
            newNode = Node(node, None, record, newGame)
            nextMoves.append(newNode)
            
        if (game.zeroIndex < 8):
            newGame = copy.deepcopy(game)
            newGame.move(Action.Right)
            record = BookKeeping(node.record.pathcost + game.reportMoveCostViaMoveType(Action.Right), Action.Right, node.record.depth+1, False)
            newNode = Node(node, None, record, newGame)
            nextMoves.append(newNode)
        
        if (game.zeroIndex < 6):
            newGame = copy.deepcopy(game)
            newGame.move(Action.Down)
            record = BookKeeping(node.record.pathcost + game.reportMoveCostViaMoveType(Action.Down), Action.Down, node.record.depth+1, False)
            newNode = Node(node, None, record, newGame)
            nextMoves.append(newNode)
        
        if (game.zeroIndex > 0):
            newGame = copy.deepcopy(game)
            newGame.move(Action.Left)
            record = BookKeeping(node.record.pathcost + game.reportMoveCostViaMoveType(Action.Left), Action.Left, node.record.depth+1, False)
            newNode = Node(node, None, record, newGame)
            nextMoves.append(newNode)
        return nextMoves

    def breadthFirstSearch(self, game):
        """BFS's implementation for solving the game"""
        # check if we start out in the win state
        game.checkIfWon()
        if (game.hasEnded == True):
            return
        record = BookKeeping(0, None, 0, False)
        node = Node(None, None, record, game)
        frontier = [node]
        explored = set()
        hasEnded = False
        maxSize = 0

        while(len(frontier) > 0 and not hasEnded):
            node = frontier.pop(0)
            node.game.checkIfWon()
            hasEnded=node.game.hasEnded

            # add all the possible next moves
            possibleMoves = self.checkNextMoves(node.game, node)
            for nodeMove in possibleMoves:
                if (str(nodeMove.game.gameboard) not in explored):
                    frontier.append(nodeMove)
                    explored.add(str(node.game.gameboard))
            # mark the node as expanded, move on the queue
            node.record.expanded = True
            node.next = possibleMoves
            if (len(frontier) > maxSize):
                maxSize = len(frontier)

        print("Max frontier/queue size is: " + str(maxSize) + ".")
        # if we got here we finally found the solution
        return node

    def depthFirstSearch(self, game):
        """DFS's implementation for solving the game"""
        # check if we start out in the win state
        game.checkIfWon()
        if (game.hasEnded == True):
            return
        record = BookKeeping(0, None, 0, False)
        node = Node(None, None, record, game)
        frontier = [node]
        explored = set()
        hasEnded = False
        maxSize = 0

        while(len(frontier) > 0 and not hasEnded):
            node = frontier.pop()
            node.game.checkIfWon()
            hasEnded=node.game.hasEnded

            # add all the possible next moves
            possibleMoves = self.checkNextMoves(node.game, node)
            for nodeMove in possibleMoves:
                if (str(nodeMove.game.gameboard) not in explored):
                    frontier.append(nodeMove)
                    explored.add(str(node.game.gameboard))
            # mark the node as expanded, move on the queue
            node.record.expanded = True
            node.next = possibleMoves
            if (len(frontier) > maxSize):
                maxSize = len(frontier)

        print("Max frontier/queue size is: " + str(maxSize) + ".")
        # if we got here we finally found the solution
        return node

    def uniformCostSearch(self, game):
        """Uniform's implementation for solving the game"""
        # check if we start out in the win state
        game.checkIfWon()
        if (game.hasEnded == True):
            return
        record = BookKeeping(0, None, 0, False)
        node = Node(None, None, record, game)
        frontier = queue.PriorityQueue(0)
        frontier.put(tuple((0, node)))
        explored = set()
        hasEnded = False
        maxSize = 0

        while(frontier.qsize() > 0 and not hasEnded):
            node = frontier.get()[1]
            node.game.checkIfWon()
            hasEnded=node.game.hasEnded

            # add all the possible next moves
            possibleMoves = self.checkNextMoves(node.game, node)
            for nodeMove in possibleMoves:
                if (str(nodeMove.game.gameboard) not in explored):
                    frontier.put(tuple((int(nodeMove.record.pathcost), nodeMove)))
                    explored.add(str(node.game.gameboard))
            # mark the node as expanded, move on the queue
            node.record.expanded = True
            node.next = possibleMoves
            if (frontier.qsize() > maxSize):
                maxSize = frontier.qsize()
        print("Max frontier/queue size is: " + str(maxSize) + ".")
        # if we got here we finally found the solution
        return node

    def h1Heuristic(self, game):
        """Is a heuristic that compares the current state to the correct answer and returns how many cubes are out of place"""
        # choses the option that is always the closest, so uniform cost search but with a different value being sorted 
        correctSolution = [1,2,3,8,0,4,7,6,5]
        difference = 0
        for index in range(len(correctSolution)):
            if (correctSolution[index] != game.gameboard[index]):
                difference = difference + 1
        return difference

    def findValue(self, value):
        """A helper function to find the index of a value in the correct solution"""
        correctSolution = [1,2,3,8,0,4,7,6,5]
        for index in range(len(correctSolution)):
            if (correctSolution[index] == value):
                return index

    def manhattanHeuristic(self, game):
        """A heuristic to calculate the moves and move cost it would take to get each square to the proper spot without concern of displacing the other squares"""
        # distance based on the number of moves it would need to make to get to the proper spot WITH the move costs!
        correctSolution = [1,2,3,8,0,4,7,6,5]
        totalDifference = 0
        
        for index in range(len(correctSolution)):
            if (correctSolution[index] != game.gameboard[index]):
                difference = abs(self.findValue(game.gameboard[index])-index)
                if difference >=3:
                    tempDiff = difference % 3
                    difference = int((difference-tempDiff)/3)
                    totalDifference = totalDifference + (tempDiff * game.gameboard[index]) + (difference * game.gameboard[index])
                else:
                    totalDifference = totalDifference + (difference * game.gameboard[index])
        return totalDifference

    def greedyBestFirstSearch(self,game):
        """Greedy's implementation for solving the game"""
        # check if we start out in the win state
        game.checkIfWon()
        if (game.hasEnded == True):
            return
        record = BookKeeping(0, None, 0, False)
        node = Node(None, None, record, game)
        frontier = queue.PriorityQueue(0)
        frontier.put(tuple((self.h1Heuristic(game), node)))
        explored = set()
        hasEnded = False
        maxSize = 0

        while(frontier.qsize() > 0 and not hasEnded):
            node = frontier.get()[1]
            node.game.checkIfWon()
            hasEnded=node.game.hasEnded

            # add all the possible next moves
            possibleMoves = self.checkNextMoves(node.game, node)
            for nodeMove in possibleMoves:
                if (str(nodeMove.game.gameboard) not in explored):
                    frontier.put(tuple((self.h1Heuristic(nodeMove.game), nodeMove)))
                    explored.add(str(node.game.gameboard))
            # mark the node as expanded, move on the queue
            node.record.expanded = True
            node.next = possibleMoves
            if (frontier.qsize() > maxSize):
                maxSize = frontier.qsize()
        print("Max frontier/queue size is: " + str(maxSize) + ".")
        # if we got here we finally found the solution
        return node

    def aStarH1Search(self, game):
        """A*'s implementation for solving the game"""
        # check if we start out in the win state
        game.checkIfWon()
        if (game.hasEnded == True):
            return
        record = BookKeeping(0, None, 0, False)
        node = Node(None, None, record, game)
        frontier = queue.PriorityQueue(0)
        frontier.put(tuple((self.h1Heuristic(game), node)))
        explored = set()
        hasEnded = False
        maxSize = 0

        while(frontier.qsize() > 0 and not hasEnded):
            node = frontier.get()[1]
            node.game.checkIfWon()
            hasEnded=node.game.hasEnded

            # add all the possible next moves
            possibleMoves = self.checkNextMoves(node.game, node)
            for nodeMove in possibleMoves:
                if (str(nodeMove.game.gameboard) not in explored):
                    frontier.put(tuple((self.h1Heuristic(nodeMove.game) + nodeMove.record.pathcost, nodeMove)))
                    explored.add(str(node.game.gameboard))
            # mark the node as expanded, move on the queue
            node.record.expanded = True
            node.next = possibleMoves
            if (frontier.qsize() > maxSize):
                maxSize = frontier.qsize()
        
        print("Max frontier/queue size is: " + str(maxSize) + ".")
        # if we got here we finally found the solution
        return node

    def aStarManhattanSearch(self, game):
        """A*Man's implementation for solving the game"""
        # check if we start out in the win state
        game.checkIfWon()
        if (game.hasEnded == True):
            return
        record = BookKeeping(0, None, 0, False)
        node = Node(None, None, record, game)
        frontier = queue.PriorityQueue(0)
        frontier.put(tuple((self.manhattanHeuristic(game), node)))
        explored = set()
        hasEnded = False
        maxSize = 0

        while(frontier.qsize() > 0 and not hasEnded):
            node = frontier.get()[1]
            node.game.checkIfWon()
            hasEnded=node.game.hasEnded

            # add all the possible next moves
            possibleMoves = self.checkNextMoves(node.game, node)
            for nodeMove in possibleMoves:
                if (str(nodeMove.game.gameboard) not in explored):
                    frontier.put(tuple((self.manhattanHeuristic(nodeMove.game) + nodeMove.record.pathcost, nodeMove)))
                    explored.add(str(node.game.gameboard))
            # mark the node as expanded, move on the queue
            node.record.expanded = True
            node.next = possibleMoves
            if (frontier.qsize() > maxSize):
                maxSize = frontier.qsize()

        print("Max frontier/queue size is: " + str(maxSize) + ".")
        # if we got here we finally found the solution
        return node

    def printPath(self, finalNode, type):
        """Method to print out the path from the final node back to the beginning node"""
        # lets build a string from bottom up
        ansString = ""
        node = finalNode
        while (node.prev != None):
            ansString = str(node.record.action) + "\n" + node.game.returnStringGameboard() + "\n" + ansString
            node = node.prev
        print("The path to get to the solution you discovered above is: \n" + ansString)
        print("It took " + type + " " + str(finalNode.record.pathcost) + " move cost.")

if __name__ == "__main__":
    startGame()

    

