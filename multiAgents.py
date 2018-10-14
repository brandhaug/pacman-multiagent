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
import math

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        score = 0.00

        for ghostState in newGhostStates:
            if ghostState.scaredTimer < 2:
                manhattan_distance = manhattanDistance(newPos, ghostState.getPosition())
                score = 0 if manhattan_distance == 0 else math.log2(manhattan_distance)

        print('Score after Manhattan Distance', score)

        if newFood[newPos[0] + 1][newPos[1]]:
            score += 5

        if newFood[newPos[0]][newPos[1] + 1]:
            score += 5

        if newFood[newPos[0] - 1][newPos[1]]:
            score += 5

        if newFood[newPos[0]][newPos[1] - 1]:
            score += 5

        print('Score after food', score)

        print('Total score', score)

        return score


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def minimizer(self, gameState, depth):
        print('Minimizing')

        agents_count = gameState.getNumAgents()
        minimum_score_sum = 0

        for ghost_index in range(1, agents_count):
            legalMoves = gameState.getLegalActions(ghost_index)

            minimum_score = math.inf

            for move_index, action in enumerate(legalMoves):
                print('MOVE_INDEX', move_index)
                successor_game_state = gameState.generateSuccessor(ghost_index, action)

                score = self.minimax(successor_game_state, depth - 1, True)

                print('Evaluation %.2f <= minEval %.2f' % (score, minimum_score))

                if score <= minimum_score:
                    minimum_score = score
                    print('Adding evalIndex to minIndex')

            minimum_score_sum += minimum_score

        return minimum_score_sum

    def maximizer(self, gameState, depth):
        print('Depth', depth)

        print('Maximizing')
        max_score = -math.inf

        legalMoves = gameState.getLegalActions()

        for move_index, action in enumerate(legalMoves):
            print('MOVE_INDEX', move_index)
            successor_game_state = gameState.generateSuccessor(0, action)

            score = self.minimax(successor_game_state, depth - 1, False)

            if score >= max_score:
                print('Evaluation %.2f >= maxEval %.2f' % (score, max_score))
                max_score = score

        print('Returning maxEval %.2f' % max_score)
        return max_score

    def minimax(self, gameState, depth, maximizingPlayer):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            print('Depth == 0', depth == 0)
            print('Is lose', gameState.isLose())
            print('Is win', gameState.isWin())
            score = gameState.getScore()
            print('Current score', score)
            return score

        if maximizingPlayer:
            return self.maximizer(gameState, depth)
        else:
            return self.minimizer(gameState, depth)

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
        """
        "*** YOUR CODE HERE ***"

        print('================ MINIMAX ================')
        legal_actions = gameState.getLegalActions()

        best_action = Directions.STOP
        score = -math.inf

        for action in legal_actions:
            print('================= START OF ACTION %s =================' % action)
            next_state = gameState.generateSuccessor(0, action)
            previous_score = score
            score = self.minimax(next_state, self.depth, False)
            print('============ SCORE ============')
            print(score)
            print('============ PREVIOUS SCORE ============')
            print(previous_score)

            if score > previous_score:
                print('SCORE IS HIGHER, SWITCHING ACTION')
                best_action = action

        print('================= END OF ACTION %s =================' % action)

        return best_action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
