
"""
Information:

Level	Dice	Min Roll	Max Roll	Average Roll	Gathering Effect	Crafting Effect
1	    2d6 +0	2	        12	            6.56	        None	        None
2	    2d6 +1	3	        13	            7.56	        None	        None
3	    3d6 +1	4	        19	            10.84	        None	        None
4	    3d6 +2	5	        20	            11.84	        None	        +1 item when refining
5	    3d6 +2	5	        20	            11.84	        -1 dif	        Reduce difficulty by 1 when refining
6	    4d6 +3	7	        27	            16.12	        None	        None
7	    4d6 +3	7	        27	            16.12	        +1 item     	None
8	    4d6 +4	8	        28	            17.12	        None	        +1 item when refining
9	    5d6 +4	9	        34	            20.4	        None	        None
10	    5d6 +5	10	        35	            21.4	        None	        none
11	    5d6 +5	10	        35	            21.4	        +1 item     	none
12	    6d6 +6	12	        42	            25.68	        None	        +1 item when refining
13	    6d6 +6	12	        42	            25.68	        -1 dif      	reduce difficulty by 1 when refining
14	    6d6 +7	13	        43	            26.68	        None	        none
15	    7d6 +7	14	        49	            29.96	        None	        none
16	    7d6 +8	15	        50	            30.96	        None	        +1 item when refining
17	    7d6 +8	15	        50	            30.96	        +1 item     	none
18	    8d6 +9	17	        57	            35.24	        None	        none
19	    8d6 +9	17	        57	            35.24	        -1 dif      	reduce difficulty by 1 when refining
20	    8d6 +10	18	        58	            36.24	        None	        +1 item when refining
gatheringItemBonus = [0,0,0,0,0,0,1,1,1,1,2,2,2,2,2,2,3,3,3,3]
gatheringDiffBonus = [0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3]
craftingItemBonus = [0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5]
craftingDiffBonus = [0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3]
                    [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0]
1	Normal	5	+0%
2	Elder	10	+5%
3	Rare	15	+10%
4	Ancient	20	+15%
5	Imbued	25	+20%
6	Legendary	30	+25%
7	Infernal	35	+30%
8	Celestial	40	+35%
9	Ascendant	45	+40%

Level	Mastery Required	Total Mastery Required
1	0	0
2	720	720
3	2200	2920
4	7800	10720
5	28800	39520
6	43200	82720
7	57600	140320
8	86400	226720
9	108000	334720
10	144000	478720
11	180000	658720
12	216000	874720
13	252000	1126720
14	288000	1414720
15	324000	1738720
16	360000	2098720
17	432000	2530720
18	504000	3034720
19	576000	3610720
20	720000	4330720
"""

import random

class dice:
    def rollDice(self):
        roll = random.randint(1,100)
        if roll <= 18:
           roll = 1
        elif roll > 18 and roll <= 36:
           roll = 2
        elif roll > 36 and roll <= 55:
           roll = 3
        elif roll > 55 and roll <= 73:
            roll = 4
        elif roll > 73 and roll <= 90:
            roll = 5
        elif roll > 90 and roll <= 100: 
            roll = 6
        
        return roll
    
#Player Class

class player:
    masteryNeeded = [720,2200,7800,28800,43200,57600,86400,108000,144000,180000,216000,252000,288000,324000,360000,432000,504000,576000,720000]
    possibleNumOfDice = [2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8]
    possibleDiceBonus = [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10]
    gatheringItemBonus = [0,0,0,0,0,0,1,1,1,1,2,2,2,2,2,2,3,3,3,3]
    gatheringDiffBonus = [0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3]
    craftingItemBonus = [0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5]
    craftingDiffBonus = [0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3]



    def __init__(self, masteryLevel, currentTicks):
        self.masteryLevel = masteryLevel
        self.currentTicks = currentTicks
        self.masteryLeft = self.masteryNeeded[masteryLevel-1] - self.currentTicks
        self.numOfDice = self.possibleNumOfDice[masteryLevel-1]
        self.diceBonus = self.possibleDiceBonus[masteryLevel-1]
        self.gatheringDiffBonus = self.gatheringDiffBonus[masteryLevel-1]
        self.gatheringItemBonus = self.gatheringItemBonus[masteryLevel-1]
        self.craftingItemBonus = self.craftingDiffBonus[masteryLevel-1]
        self.craftingDiffBonus = self.craftingDiffBonus[masteryLevel-1]

    def gatherMats(self, difficulty):

        #Initilizes variables
        #totalRoll = Combined value of dice rolled
        #totalTicks = total # of ticks done to achieve next mastery

        totalRoll,totalTicks,totalGathered = 0,0,0

        #while the # of ticks to next mastery is >1
        while self.masteryLeft != 0:
            for i in range(1,self.numOfDice):
                totalRoll += dice.rollDice(self) 

            totalRollWithBonus = totalRoll + self.diceBonus
            if totalRollWithBonus >= difficulty - self.gatheringDiffBonus:
                self.masteryLeft -= 1
                totalGathered += 1 + self.gatheringItemBonus
                totalRoll = 0
            else:
                self.masteryLeft -= 1
                totalRoll = 0

        return totalGathered


    #Calculates Time (Ticks * 5 (1 tick per 5 seconds) /60 (Seconds) /60 (Minutes))
    def calcTime(self, currentMastery):
        self.masteryLeft = self.masteryNeeded[self.masteryLevel-1] - self.currentTicks
        return round(float((self.masteryLeft*5/60/60)),2)


playerCurrentMastery = int(input("Input Current Mastery Level: "))
playerCurrentNumOfTicks = int(input("How many ticks do you currently have? (Not combined, towards next mastery level) "))
gatheringDiff = int(input("What difficulty are you grinding out? (5,10,15, etc) "))
simulationTimes = int(input("How many times would you like to run the simulation? "))
simulationAttempts = list()
totalSum = 0
totalGathered = 0
peon = player(playerCurrentMastery, playerCurrentNumOfTicks)

for i in range(0,simulationTimes):
    peon = player(playerCurrentMastery, playerCurrentNumOfTicks)
    simulationAttempts.append(peon.gatherMats(gatheringDiff))
    print("Simulation " + str(i+1) + " Gathered: " + str(simulationAttempts[i]) + " Mats")
    
for i in range(len(simulationAttempts)):
     totalSum += simulationAttempts[i]

print("It will take around " + str(peon.calcTime(playerCurrentMastery))+ " hours to do this")
print("During this time, you will gather an average of " +str(totalSum/len(simulationAttempts)) + " Mats!")


