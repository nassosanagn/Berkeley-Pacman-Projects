# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        foodList = newFood.asList()
        foodDist = []
        ghostDist = []

        for x in foodList:
            foodDist.append(manhattanDistance(newPos,x))

        # If there are foods left find the closest and the furthest food
        if (foodList != []):
            closestFood = min(foodDist)
            furthestFood = max(foodDist)
        else:
            return successorGameState.getScore()

        # Find the closest ghost from the Pacman
        for ghost in newGhostStates:
            ghostDist.append(manhattanDistance(newPos,ghost.getPosition()))

        if (ghostDist != []):
           minGhostDist = min(ghostDist)

        # How many foods are left
        foodsLeft = len(foodList)

        # If there is only 1 food left then furthestFood == closestFood
        if foodsLeft == 1:
            score = minGhostDist - closestFood
        else:
            score = minGhostDist - (furthestFood + closestFood)

        return successorGameState.getScore() + score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def minimax(self, gameState, agent, depth):

        # If Pacman wins or loses or maximum depth is reached then stop recursion
        if (gameState.isLose() or gameState.isWin() or (depth == 0)):
            return [self.evaluationFunction(gameState)]

        if agent == 0:
            maxValue = -float("inf")
            pacmanActions = gameState.getLegalActions(agent)

            for action in pacmanActions:
                successorGameState = gameState.generateSuccessor(agent, action)
                newMax = self.minimax(successorGameState, agent + 1 , depth)[0]           # After pacman's turn, the first ghost moves

                # Update the maxValue
                if newMax > maxValue:
                    maxValue = newMax
                    bestAction = action

            return [maxValue, bestAction]

        # One of the ghosts turn (MIN)
        else:
            minValue = float("inf")
            numOfGhosts = gameState.getNumAgents() - 1      # number of ghosts Ghosts = all agents - pacman (1)

            if agent == numOfGhosts:       # If it's the final ghost
                depth -= 1
                nextAgent = 0                   # Go to pacman again agent == 0
            else:                               # If not go to the next ghost
                nextAgent = agent + 1

            ghostActions = gameState.getLegalActions(agent)

            for action in ghostActions:
                successorGameState = gameState.generateSuccessor(agent, action)
                # Index 0 is the previous minValue and index 1 is the previous best Action
                newMin = self.minimax(successorGameState, nextAgent, depth)[0]

                # Update the minValue
                if newMin < minValue:
                    minValue = newMin
                    bestAction = action

            return [minValue, bestAction]

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        bestAction = self.minimax(gameState, self.index, self.depth)[1]
        return bestAction
        util.raiseNotDefined()

# - - - - - - - - - - - - - End of minimax - - - - - - - - - - - - - - #

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def alphabeta(self, gameState, agent, depth, a , b):
        
        # If Pacman wins or loses or maximum depth is reached then stop recursion
        if (gameState.isLose() or gameState.isWin() or (depth == 0)):
            return [self.evaluationFunction(gameState)]

        if agent == 0:
            maxValue = -float("inf")
            pacmanActions = gameState.getLegalActions(agent)

            for action in pacmanActions:
                successorGameState = gameState.generateSuccessor(agent, action)
                newMax = self.alphabeta(successorGameState, agent + 1 , depth, a ,b)[0]             # after pacman's turn first ghost plays

                # Update the maxValue
                if newMax > maxValue:
                    maxValue = newMax
                    bestAction = action

                # If maxValue > b => Prune
                if maxValue > b:
                    return [maxValue]

                a = max(a,maxValue)
            return [maxValue, bestAction]

        else:
            minValue = float("inf")
            numOfGhosts = gameState.getNumAgents() - 1

            if agent == numOfGhosts:       # If it's the final ghost
                depth -= 1
                nextAgent = 0                   # Go to pacman again index = 0
            else:                                           # if not go to the next ghost
                nextAgent = agent + 1

            ghostActions = gameState.getLegalActions(agent)

            for action in ghostActions:
                successorGameState = gameState.generateSuccessor(agent, action)
                newMin = self.alphabeta(successorGameState, nextAgent, depth, a, b)[0]

                # Update the minValue
                if newMin < minValue:
                    minValue = newMin
                    bestAction = action

                # If minValue < a => Prune
                if minValue < a:
                    return [minValue]

                b = min(b,minValue)

            return [minValue, bestAction]

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a = -float("inf")
        b =  float("inf")
        bestAction = self.alphabeta(gameState, self.index, self.depth, a , b)[1]
        return bestAction
        util.raiseNotDefined()

# - - - - - - - - - - - - - End of AlphaBeta - - - - - - - - - - - - - - #

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expectimax(self, gameState, agent, depth):

        # If Pacman wins or loses or maximum depth is reached then stop recursion
        if (gameState.isLose() or gameState.isWin() or (depth == 0)):
            return [self.evaluationFunction(gameState)]

        if agent == 0:
           maxValue = -float("inf")
           pacmanActions = gameState.getLegalActions(agent)

           for action in pacmanActions:
               successorGameState = gameState.generateSuccessor(agent, action)
               newMax = self.expectimax(successorGameState, agent + 1 , depth)[0]             # after pacman's turn first ghost plays

               # Update the maxValue
               if newMax > maxValue:
                   maxValue = newMax
                   bestAction = action

           return [maxValue, bestAction]

        # One of the ghosts turn (MIN)
        else:
            minValue = 0                    # Initialize minValue with 0
            numOfGhosts = gameState.getNumAgents() - 1

            if agent == numOfGhosts:       # If it's the final ghost
                depth -= 1
                nextAgent = 0                   # go to pacman again index = 0
            else:                                           # if not go to the next ghost
                nextAgent = agent + 1

            ghostActions = gameState.getLegalActions(agent)

            for action in ghostActions:
                successorGameState = gameState.generateSuccessor(agent, action)
                minValue += self.expectimax(successorGameState, nextAgent, depth)[0]
                bestAction = action

            minValue = minValue / len(ghostActions)
            return [minValue, action]

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestAction = self.expectimax(gameState, self.index, self.depth)[1]
        return bestAction
        util.raiseNotDefined()

# - - - - - - - - - - - - - End of Expectimax - - - - - - - - - - - - - - #

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    # Same evaluation function as q1 but if ghost is scared pacman runs to the ghost
    newFood = currentGameState.getFood()
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodList = newFood.asList()
    foodDist = []

    # Find the closest and the furthest food
    for x in foodList:
        foodDist.append(manhattanDistance(newPos,x))

    if (foodList != []):
        closestFood = min(foodDist)
        furthestFood = max(foodDist)
    else:
        return currentGameState.getScore()

    # Find the closest ghost from the Pacman
    ghostDist = []

    for ghost in newGhostStates:
        ghostDist.append(manhattanDistance(newPos,ghost.getPosition()))

    if (ghostDist != []):
        minGhostDist = min(ghostDist)

    # How many foods are left
    foodsLeft = len(foodList)

    timeScared = sum(newScaredTimes)

    # If Ghost is Scared, pacman runs to the ghost
    if (timeScared > 0):
        score = -minGhostDist - closestFood

    # If there is only 1 food left then furthestFood == closestFood
    elif (foodsLeft == 1):
        score = minGhostDist - furthestFood

    else:
        score = minGhostDist - (furthestFood + closestFood)

    return currentGameState.getScore() + score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
