import random
import copy
import math

def randomPoint(state):
    candidates = []
    for i in range(N):
        for j in range(N):
            if state[i][j] == 0:
                candidates.append((i, j))
    if len(candidates) == 0:
        return None
    return random.choice(candidates)

def addRandomPoint(state):
    pt = randomPoint(state)
    if random.random() <= 0.1:
        state[pt[0]][pt[1]] = 4
    else:
        state[pt[0]][pt[1]] = 2
    return state

def randomInitState():
    state = [[0 for i in range(4)] for j in range(4)]
    state = addRandomPoint(state)
    state = addRandomPoint(state)
    return state

def endCondition(state):
    for row in state:
        if 2048 in row:
            return True
    return False

def printState(state):
    for row in state:
        print row
    print

def singleTransition(tmp):
    j = 0
    score = 0
    while j < len(tmp)-1:
        if tmp[j] == tmp[j+1]:
            del tmp[j]
            tmp[j] = tmp[j] * 2
            #score += tmp[j]
            score += math.log(tmp[j], 2)
            j += 1
        else:
            j += 1
    return tmp, score

def evaluateState(state):
    score = 0
    for row in state:
        score += row.count(0)
    return score

def boardMove(state, action):
    score = 0
    if action == 'up':
        for i in range(N):
            tmp = []
            for j in range(N):
                if state[j][i] != 0:
                    tmp.append(state[j][i])
                    state[j][i] = 0
            tmp, tmpScore = singleTransition(tmp)
            score += tmpScore
            for j in range(len(tmp)):
                state[j][i] = tmp[j]
    if action == 'down':
        for i in range(N):
            tmp = []
            for j in range(N-1, -1, -1):
                if state[j][i] != 0:
                    tmp.append(state[j][i])
                    state[j][i] = 0
            tmp, tmpScore = singleTransition(tmp)
            score += tmpScore
            for j in range(len(tmp)):
                state[N-1-j][i] = tmp[j]
    if action == 'left':
        for i in range(N):
            tmp = []
            for j in range(N):
                if state[i][j] != 0:
                    tmp.append(state[i][j])
                    state[i][j] = 0
            tmp, tmpScore = singleTransition(tmp)
            score += tmpScore
            for j in range(len(tmp)):
                state[i][j] = tmp[j]
    if action == 'right':
        for i in range(N):
            tmp = []
            for j in range(N-1, -1, -1):
                if state[i][j] != 0:
                    tmp.append(state[i][j])
                    state[i][j] = 0
            tmp, tmpScore = singleTransition(tmp)
            score += tmpScore
            for j in range(len(tmp)):
                state[i][N-1-j] = tmp[j]
    tmpScore = evaluateState(state)
    return state, tmpScore

def simulate(state, action):
    state, reward = boardMove(state, action)
    state = addRandomPoint(state)
    return state, reward

def validAction(state):
    actionList = ["up", "down", "left", "right"]
    resultMap = {}
    for action in actionList:
        tmpState = copy.deepcopy(state)
        tmpAfterState, rewards = boardMove(tmpState, action)
        if tmpAfterState != state:
            tmpAfterState = addRandomPoint(tmpAfterState)
            resultMap[action] = [tmpAfterState, rewards]
    return resultMap

def monteCarloTreeSearch(state, h):
    actionMap = validAction(state)
    if len(actionMap.keys()) == 0:
        return None, None, -100000
    if h == 0:
        return None, None, 0
    maxRewards = 0
    maxAction = None
    maxState = None
    for action in actionMap.keys():
        tmpState = actionMap[action][0]
        tmpRewards = actionMap[action][1] + monteCarloTreeSearch(tmpState, h-1)[2]
        if tmpRewards > maxRewards:
            maxRewards = tmpRewards
            maxAction = action
            maxState = copy.deepcopy(tmpState)
    return maxAction, maxState, maxRewards

def gameSimulate(state):
    while True:
        printState(state)
        if endCondition(state):
            break
        action, state, score = monteCarloTreeSearch(state, 4)
        if action == None:
            break
    
                    
                

N = 4
    
initState = randomInitState()
gameSimulate(initState)

