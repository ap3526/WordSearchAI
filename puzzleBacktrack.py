import random
import copy

class Puzzle:

    def __init__(self, numRows, numColumns, words=[]):
        self.grid = self.createGrid(numRows, numColumns, words)
        self.words = words
        self.state = [self.grid, self.words]
        self.failCounter = 0
        self.backTrackCount = 0

    def createGrid(self, numRows, numColumns, words=[]):
        grid = []
        for row in range(numRows):
            grid.append([])
            for column in range(numColumns):
                grid[row].append('.')
        return grid

    def goal(self, state):
        if state[1] == []:
            return True

    def applyRule(self, rule, state):
        word = rule[0]
        startCol = rule[1]
        startRow = rule[2]
        changeY = rule[3]
        changeX = rule[4]
        dupGrid = []
        # dupGrid = copy.deepcopy(state[0])
        # print(type(dupGrid))
        for spot in state[0][:]:
            dupGrid.append(spot[:])
        
        for letter in word:
            dupGrid[startCol][startRow] = letter
            startCol += changeX
            startRow += changeY
        
        dupWords = state[1][:]
        dupWords.remove(word)
        return [dupGrid, dupWords]

    def preCondition(self, rule, state):
        height = len(self.grid)
        width = len(self.grid[0])
        word = rule[0]
        startCol = rule[1]
        startRow = rule[2]
        changeY = rule[3]
        changeX = rule[4]
        for letter in word:
            #check if each letter remains in the grid, if either coordinate exceeds the height or width or becomes negative, we know it doesn't fit
            if((startCol > width - 1) or (startRow > height - 1) or (startCol < 0 or startRow < 0)):
                return False
            startCol += changeX
            startRow += changeY


        startCol = rule[1]
        startRow = rule[2]

        #test if it overlaps with another word
        for letter in word:
            if((state[0][startCol][startRow] != ".") or (state[0][startCol][startRow] == letter)):
                return False
            startCol += changeX
            startRow += changeY

        return True

    def generateRules(self,state):
        rules = []

        height = len(self.grid)
        width = len(self.grid[0])
        # loop through each word
        for word in state[1]:
            # loop through each row
            for row in range(height):
                # check through each column in the row
                for column in range(width):
                    # row forward
                    if(column + (len(word) - 1) <= width - 1):
                        rule = (word, row, column, 1, 0)
                        if(self.preCondition(rule, state)):
                            rules.append(rule)
                    # row backward
                    if(column - (len(word) - 1) >= 0):
                        rule = (word, row, column, -1, 0)
                        if(self.preCondition(rule, state)):
                            rules.append(rule)
                    # column up
                    if(row - (len(word) -1 ) >= 0):
                        rule = (word, row, column, 0, -1)
                        if(self.preCondition(rule, state)):
                            rules.append(rule)
                    # column down
                    if(row + (len(word) - 1) <= height - 1):
                        rule = (word, row, column, 0, 1)
                        if(self.preCondition(rule, state)):
                            rules.append(rule)
                    # diagonal left and up
                    if((row - (len(word) -1 ) >= 0) and (column - (len(word) - 1) >= 0)):
                        rule = (word, row, column, -1, -1)
                        if(self.preCondition(rule, state)):
                            rules.append(rule)
                    #diagonal right and up
                    if((row - (len(word) - 1) >= 0) and (column + (len(word) - 1) <= width - 1)):
                        rule = (word, row, column, 1, -1)
                        if(self.preCondition(rule, state)):
                            rules.append(rule)
                    #diagonal left and down
                    if((row + (len(word) - 1) <= height - 1) and (column - (len(word) - 1) >= 0)):
                        rule = (word, row, column, -1, 1)
                        if(self.preCondition(rule, state)):
                            rules.append(rule)
                    #diagonal right and down
                    if((row + (len(word) - 1) <= height - 1) and (column + (len(word) - 1) <= width - 1)):
                        rule = (word, row, column, 1, 1)
                        if(self.preCondition(rule, state)):
                            rules.append(rule)
        return rules
    
    def describeState(self, state):
        parts = state[0]
        print("Current State:  \n")
        for row in parts:
            for column in row:
                print(column, end= '')
            print()
        print("\nRemaining Words: ", state[1])

    def describeRule(self, rule):
        print(rule)
        ruleExplanation = 'Rule: ' + str(rule) + '\nPlace the word '+ str(rule[0]) + ' in the grid starting at position (' + str(rule[1]) + ',' + str(rule[2]) + ') and proceeding in the direction [' + str(rule[3]) + ',' + str(rule[4]) + ']'
        print(ruleExplanation)

    def flailWildly(self,state):
        while self.goal(state) != True:
            allRules = self.generateRules(state)
            if(len(allRules) == 0):
                print(self.describeState(state))
                print("There are no rules that can be applied")
                break
            randomNumber = random.randrange(0, len(allRules) - 1)
            self.describeState(state)
            for rule in allRules:
                self.describeRule(rule)
            print("\nChosen Rule: ")
            self.describeRule(allRules[randomNumber])
            state = self.applyRule(allRules[randomNumber], state)
        #once there are no more words, print out the final state and notify there are no moves left
        if self.goal(state):
            print(self.describeState(state))
            print("No moves available")

    def backTrack(self, stateList):
        self.backTrackCount += 1
        depthBound = 100000
        state = stateList[0]
        if state in stateList[1:]:
            return 'FAILED'
        
        if self.goal(state):
            print("Goal State Reached")
            return None
        if len(self.generateRules(state)) == 0:
            return "FAILED"
        if len(stateList) > depthBound:
            return "FAILED"

        ruleSet = self.generateRules(state)
        if ruleSet == None:
            return "FAILED"

        for rule in ruleSet:
            newStateList = []
            newState = self.applyRule(rule, state)
            print("Rule Applied: ", rule)
            newStateList = copy.deepcopy(stateList)
            newStateList.insert(0, newState) 
            self.describeState(newState)
            path = self.backTrack(newStateList)
            if path != "FAILED":
                if path == None:
                    return [rule]
                path.append(rule)
                return path
            else:
                self.failCounter += 1
        
        return 'FAILED'

if __name__ == "__main__":
    # words = ["up", "down", "right", "left", "boy", "girl", "hi"]
    words = ["admissible", "agent", "backtrack", "cannibal", "deadend", "global", "graphsearch", "heuristic", "hill", "lisp", "local", "missionary", "optimum", "search", "symmetry"]
    initial = Puzzle(12, 12, words)
    newBackTrack = []
    newBackTrack = initial.backTrack([initial.state])

    # apply rules from backTrack to the state
    for rule in newBackTrack:
        initial.state = initial.applyRule(rule, initial.state)
    print("FINAL STATE: ")
    initial.describeState(initial.state)
    print("FAILS: ", initial.failCounter)
    print("BACKTRACK CALLS: ", initial.backTrackCount)

    # list returns last move made to first, we want first to last
    newBackTrack.reverse()
    print("PATH: ", newBackTrack)

