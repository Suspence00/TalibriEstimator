#!/usr/bin/env python

__author__ = "Suspence/Suspence0/Suspence00"

import random
import progressBar
import time

#Sets up the Talibri weighted die of destiny
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
    gearBonusProvided,timesLeveledUp, goodFortune = 0,0,0



    def __init__(self, masteryLevel, currentTicks):
        self.masteryLevel = masteryLevel
        self.currentTicks = currentTicks
        self.masteryPointsLeft = self.masteryNeeded[masteryLevel-1] - currentTicks
        self.numOfDice = self.possibleNumOfDice[masteryLevel-1]
        self.diceBonus = self.possibleDiceBonus[masteryLevel-1]
        self.currentGatheringDiffBonus = self.gatheringDiffBonus[masteryLevel-1]
        self.currentGatheringItemBonus = self.gatheringItemBonus[masteryLevel-1]
        self.currentCraftingItemBonus = self.craftingItemBonus[masteryLevel-1]
        self.currentCraftingDiffBonus = self.craftingDiffBonus[masteryLevel-1]

    def getDifficulty(self):
        return self.currentDifficulty

        #Checks if it's time for a level up 
    def masteryDingCheck(self):
        if self.masteryPointsLeft == 0:
            #Gratz!
            return True
        else:
            return False

        #Calculates Time (Ticks * 5 (1 tick per 5 seconds) /60 (Seconds) /60 (Minutes))
    def calcTime(self):
        self.masteryPointsLeft = self.masteryNeeded[self.masteryLevel-1] - self.currentTicks
        return round((self.masteryPointsLeft*5/60/60),2)

    #Simple function to get the amount of time it takes to do a whol'lotta ticks
    def calcTickTime(self, amountOfTicks):
        return round(amountOfTicks*5/60/60, 2)

    def checkGearBonus(self,gearBonus):
        if gearBonus < 100:
            if random.randint(1,100) <= gearBonus:
                return 1
            else:
                return 0
        else: 
            if random.randint(1,100) <= gearBonus%100:
                self.gearBonusProvided += int(gearBonus/100)+1
                self.goodFortune +=1
                return int(gearBonus/100)+1
            else:
                self.gearBonusProvided += int(gearBonus/100)
                return int(gearBonus/100)


class gatheringCalc(player):

    def setGatheringDifficulty(self, difficulty):
        self.currentDifficulty = difficulty - self.currentGatheringDiffBonus
    
    def gatherMatsTillNextMastery(self, gearBonus):

        #Initilizes variables
        #totalRoll = Combined value of dice rolled
        #totalTicks = total # of ticks done to achieve next mastery

        totalRoll,totalTicks,totalGathered = 0,0,0

        #while the # of ticks to next mastery is >1
        while self.masteryPointsLeft != 0:
            
            #For Everydice, roll a dice() and add it to totalRoll
            for i in range(1,self.numOfDice):
                totalRoll += dice.rollDice(self) 

            #Adds the bonus to dice
            totalRollWithBonus = totalRoll + self.diceBonus

            #if the totalRolls with bonus applied is less than the current difficulty with the gathering difficulty bonus applied, subtract from mastery ticksm add the loot + any gear bonus and mastery bonus and resets totalRoll
            #else, just get 1 tick closer to being a master
            if totalRollWithBonus >= self.currentDifficulty - self.currentGatheringDiffBonus:
                self.masteryPointsLeft -= 1
                totalGathered += 1 + self.currentGatheringItemBonus + self.checkGearBonus(gearBonus)
                totalRoll = 0
            else:
                self.masteryPointsLeft -= 1
                totalRoll = 0

        return totalGathered

    def gatherMatsTillEndOfTicks(self, amountOfTicks, gearBonus):

        #Initilizes variables
        #totalRoll = Combined value of dice rolled
        #totalTicks = total # of ticks done to achieve next mastery
        totalRoll,totalGathered = 0,0

        #while the # of ticks to next mastery is >1
        while amountOfTicks!= 0:
            for i in range(1,self.numOfDice):
                totalRoll += dice.rollDice(self) 
            
            # Adds dat bonus to the total roll and adds in any dice bonus provided by mastery
            totalRollWithBonus = totalRoll + self.diceBonus
            
            if totalRollWithBonus >= self.currentDifficulty - self.currentGatheringDiffBonus:
                
                self.masteryPointsLeft -= 1
                
                # Checks for a level up
                if (self.masteryDingCheck() == True):
                    self.masteryRankUp()

                amountOfTicks -= 1
                totalGathered += 1 + self.currentGatheringItemBonus + self.checkGearBonus(gearBonus)
                totalRoll = 0

            else:
                self.masteryPointsLeft -= 1
                
                if (self.masteryDingCheck() == True):
                    self.masteryRankUp()

                amountOfTicks -= 1
                totalRoll = 0

        return totalGathered
            
    #Levels up the Mastery and changes the Mastery needed to the next highest value
    def masteryRankUp(self):
        self.masteryLevel += 1
        self.masteryPointsLeft = self.masteryNeeded[self.masteryLevel-1]
        self.diceBonus = self.possibleDiceBonus[self.masteryLevel-1]
        self.timesLeveledUp += 1
        self.setGatheringDifficulty(self.getDifficulty())
        self.currentGatheringDiffBonus = self.gatheringDiffBonus[self.masteryLevel-1]
        self.currentGatheringItemBonus = self.gatheringItemBonus[self.masteryLevel-1]


class craftingCalc(player):

    def setCraftingDifficulty(self, difficulty):
        self.currentDifficulty = difficulty - self.currentCraftingDiffBonus

    def gatherMatsTillNextMastery(self, gearBonus):
            #Initilizes variables
        #totalRoll = Combined value of dice rolled
        #totalTicks = total # of ticks done to achieve next mastery

        totalRoll,totalTicks,totalCrafted = 0,0,0

        #while the # of ticks to next mastery is >1
        while self.masteryPointsLeft != 0:
            for i in range(1,self.numOfDice):
                totalRoll += dice.rollDice(self) 

            totalRollWithBonus = totalRoll + self.diceBonus
            if totalRollWithBonus >= self.currentDifficulty - self.currentCraftingDiffBonus:
                self.masteryPointsLeft -= 1
                totalCrafted += 1 + self.currentCraftingItemBonus + self.checkGearBonus(gearBonus)
                totalRoll = 0
            else:
                self.masteryPointsLeft -= 1
                totalRoll = 0

        return totalCrafted

    def gatherMatsTillEndOfTicks(self, amountOfTicks, gearBonus):

        #Initilizes variables
        #totalRoll = Combined value of dice rolled
        #totalTicks = total # of ticks done to achieve next mastery
        totalRoll,totalCrafted = 0,0

        #while the # of ticks to next mastery is >1
        while amountOfTicks!= 0:
            for i in range(1,self.numOfDice):
                totalRoll += dice.rollDice(self) 
            
            # Adds dat bonus to the total roll and adds in any dice bonus provided by mastery
            totalRollWithBonus = totalRoll + self.diceBonus
            
            if totalRollWithBonus >= self.currentDifficulty - self.currentCraftingDiffBonus:
                
                self.masteryPointsLeft -= 1
                
                # Checks for a level up
                if (self.masteryDingCheck() == True):
                    self.masteryRankUp()

                amountOfTicks -= 1
                totalCrafted += 1 + self.currentCraftingItemBonus + self.checkGearBonus(gearBonus)
                totalRoll = 0

            else:
                self.masteryPointsLeft -= 1
                
                if (self.masteryDingCheck() == True):
                    self.masteryRankUp()

                amountOfTicks -= 1
                totalRoll = 0

        return totalCrafted
            
    #Levels up the Mastery and changes the Mastery needed to the next highest value
    def masteryRankUp(self):
        self.masteryLevel += 1
        self.masteryPointsLeft = self.masteryNeeded[self.masteryLevel-1]
        self.diceBonus = self.possibleDiceBonus[self.masteryLevel-1]
        self.timesLeveledUp += 1
        self.setCraftingDifficulty(self.getDifficulty())
        self.currentCraftingDiffBonus = self.craftingDiffBonus[self.masteryLevel-1]
        self.currentCraftingItemBonus = self.craftingItemBonus[self.masteryLevel-1]



        
menu = {}
menu['1']="Gathering: Run Simulations till for specific tick amount" 
menu['2']="Gathering: Run Simulations till next mastery level."
menu['3']="Crafting: Run Simulations till for specific tick amount" 
menu['4']="Crafting: Run Simulations till next mastery level."
menu['5']="Exit"
loop = True
while loop: 
    print("\n Main Menu \n")
    simulationAttempts = list()
    totalSum = 0
    totalGathered = 0

    options=menu.keys()
    
    for i in options: 
        print(i,":", menu[i])
    
    selection = input("Please Select an Option: ")
    
    if selection =='1': 

        playerCurrentMastery = int(input("Input Current Mastery Level: "))
        while playerCurrentMastery < 1 or playerCurrentMastery > 20:
            print("\n"+"Please input a valid Mastery Level (1-20)")
            playerCurrentMastery = int(input("Input Current Mastery Level: "))
            
        gatheringDiff = int(input("What difficulty are you grinding out? (5,10,15,etc): "))
        while gatheringDiff%5 != 0:
            print("\n"+"Please input a proper difficulty (Divisable by 5)")
            gatheringDiff = int(input("What difficulty are you grinding out? (5,10,15,etc): "))

        playerCurrentNumOfTicks = int(input("How many ticks do you currently have? (Not combined, towards next mastery level): "))
        while playerCurrentNumOfTicks > player.masteryNeeded[playerCurrentMastery-1]:
            print("Hmm, that doesn't compute. Please make sure your current ticks is correct: ")
            playerCurrentNumOfTicks = int(input("How many ticks do you currently have? (Not combined, towards next mastery level): "))

        playerGearBonus = float(input("Got any Gathering Bonus? (Chance +1 Item while gathering bonus only, enter # with decimal. Eg: 154.3): "))
        while playerGearBonus < 0:
            print("You can't be less than naked. Input 0 if you have no gear.")
            playerGearBonus = float(input("Got any Gathering Bonus? (Chance +1 Item while gathering bonus only, enter # with decimal. Eg: 154.3): "))

        playerTicks = int(input("How many ticks would you like to simulate? "))
        while playerTicks < 1:
            print("Why would you try to run 0 ticks? Who are you? What are you doing with your life? Enter a positive number plz")
            playerTicks = int(input("How many ticks would you like to simulate?: "))
        
        simulationTimes = int(input("How many times would you like to run the simulation?: "))
        while simulationTimes < 1:
            print("Why would you try to run 0 simulations? Who are you? What are you doing with your life? Enter a positive number plz")
            simulationTimes = int(input("How many times would you like to run the simulation?: "))


        for i in range(0,simulationTimes):
            peon = gatheringCalc(playerCurrentMastery, playerCurrentNumOfTicks)
            peon.setGatheringDifficulty(gatheringDiff)
            print("\n"+"Simulation " + str(i+1)+": ")
            print("Starting Bonuses: ")
            print("\n"+"Starting Mastery: "+str(peon.masteryLevel))
            print("Gathering Count Bonus: " + str(peon.currentGatheringItemBonus))
            print("Gathering Difficulty Bonus: " +str(peon.currentGatheringDiffBonus))
            print("Dice Bonus: " +str(peon.diceBonus))
            simulationAttempts.append(peon.gatherMatsTillEndOfTicks(playerTicks, playerGearBonus))
            print("\n"+"Simulation " + str(i+1) + " Gathered: " + str(simulationAttempts[i]) + " Mats and leveled up " + str(peon.timesLeveledUp) + " time(s)!")
            print("Your gear provided an extra "+str(peon.gearBonusProvided)+" mats and you had "+str(peon.goodFortune)+" extra luck!")
            print("\n"+"Ending Bonuses: ")
            print("\n"+"Ending Mastery: "+str(peon.masteryLevel))
            print("Gathering Count Bonus: " + str(peon.currentGatheringItemBonus))
            print("Gathering Difficulty Bonus: " +str(peon.currentGatheringDiffBonus))
            print("Dice Bonus: " +str(peon.diceBonus))
    
        for i in range(len(simulationAttempts)):
             totalSum += simulationAttempts[i]
        print("\n"+"It will you " + str(player.calcTickTime(None,playerTicks))+ " hours to do this")
        print("During this time, you will gather an average of " +str(round(totalSum/len(simulationAttempts),2)) + " Mats!")

    elif selection == '2': 

        playerCurrentMastery = int(input("Input Current Mastery Level: "))
        while playerCurrentMastery < 1 or playerCurrentMastery > 20:
            print("\n"+"Please input a valid Mastery Level (1-20)")
            playerCurrentMastery = int(input("Input Current Mastery Level: "))
            
        gatheringDiff = int(input("What difficulty are you grinding out? (5,10,15,etc): "))
        while gatheringDiff%5 != 0:
            print("\n"+"Please input a proper difficulty (Divisable by 5)")
            gatheringDiff = int(input("What difficulty are you grinding out? (5,10,15,etc): "))

        playerCurrentNumOfTicks = int(input("How many ticks do you currently have? (Not combined, towards next mastery level): "))
        while playerCurrentNumOfTicks > player.masteryNeeded[playerCurrentMastery-1]:
            print("Hmm, that doesn't compute. Please make sure your current ticks is correct: ")
            playerCurrentNumOfTicks = int(input("How many ticks do you currently have? (Not combined, towards next mastery level): "))

        playerGearBonus = float(input("Got any Gathering Bonus? (Chance +1 Item while gathering bonus only, enter # with decimal. Eg: 154.3): "))
        while playerGearBonus < 0:
            print("You can't be less than naked. Input 0 if you have no gear.")
            playerGearBonus = float(input("Got any Gathering Bonus? (Chance +1 Item while gathering bonus only, enter # with decimal. Eg: 154.3): "))
        
        simulationTimes = int(input("How many times would you like to run the simulation?: "))
        while simulationTimes < 1:
            print("Why would you try to run 0 simulations? Who are you? What are you doing with your life? Enter a positive number plz")
            simulationTimes = int(input("How many times would you like to run the simulation?: "))

        for i in range(0,simulationTimes):
            peon = gatheringCalc(playerCurrentMastery, playerCurrentNumOfTicks)
            peon.setGatheringDifficulty(gatheringDiff)
            simulationAttempts.append(peon.gatherMatsTillNextMastery(playerGearBonus))
            print("Simulation " + str(i+1) + " Gathered: " + str(simulationAttempts[i]) + " Mats")
    
        for i in range(len(simulationAttempts)):
             totalSum += simulationAttempts[i]

        print("It will take you " + str(peon.calcTime()) + " hours to do this")
        print("During this time, you will gather an average of " +str(round(totalSum/len(simulationAttempts),2)) + " Mats!")
        

    elif selection == '3': 
        
        playerCurrentMastery = int(input("Input Current Mastery Level: "))
        while playerCurrentMastery < 1 or playerCurrentMastery > 20:
            print("\n"+"Please input a valid Mastery Level (1-20)")
            playerCurrentMastery = int(input("Input Current Mastery Level: "))
            
        craftingDiff = int(input("What difficulty are you grinding out? (5,10,15,etc): "))
        while craftingDiff%5 != 0:
            print("\n"+"Please input a proper difficulty (Divisable by 5)")
            craftingDiff = int(input("What difficulty are you grinding out? (5,10,15,etc): "))

        playerCurrentNumOfTicks = int(input("How many ticks do you currently have? (Not combined, towards next mastery level): "))
        while playerCurrentNumOfTicks > player.masteryNeeded[playerCurrentMastery-1]:
            print("Hmm, that doesn't compute. Please make sure your current ticks is correct: ")
            playerCurrentNumOfTicks = int(input("How many ticks do you currently have? (Not combined, towards next mastery level): "))

        playerGearBonus = float(input("Got any Gathering Bonus? (Chance +1 Item while gathering bonus only, enter # with decimal. Eg: 154.3): "))
        while playerGearBonus < 0:
            print("You can't be less than naked. Input 0 if you have no gear.")
            playerGearBonus = float(input("Got any Gathering Bonus? (Chance +1 Item while gathering bonus only, enter # with decimal. Eg: 154.3): "))

        playerTicks = int(input("How many ticks would you like to simulate? "))
        while playerTicks < 1:
            print("Why would you try to run 0 ticks? Who are you? What are you doing with your life? Enter a positive number plz")
            playerTicks = int(input("How many ticks would you like to simulate?: "))
        
        simulationTimes = int(input("How many times would you like to run the simulation?: "))
        while simulationTimes < 1:
            print("Why would you try to run 0 simulations? Who are you? What are you doing with your life? Enter a positive number plz")
            simulationTimes = int(input("How many times would you like to run the simulation?: "))


        for i in range(0,simulationTimes):
            peon = craftingCalc(playerCurrentMastery, playerCurrentNumOfTicks)
            peon.setCraftingDifficulty(craftingDiff)
            print("\n"+"Simulation " + str(i+1)+": ")
            print("Starting Bonuses: ")
            print("\n"+"Starting Mastery: "+str(peon.masteryLevel))
            print("Crafting Count Bonus: " + str(peon.currentCraftingItemBonus))
            print("Crafting Difficulty Bonus: " +str(peon.currentCraftingDiffBonus))
            print("Dice Bonus: " +str(peon.diceBonus))
            simulationAttempts.append(peon.gatherMatsTillEndOfTicks(playerTicks, playerGearBonus))
            print("\n"+"Simulation " + str(i+1) + " Gathered: " + str(simulationAttempts[i]) + " Mats and leveled up " + str(peon.timesLeveledUp) + " time(s)!")
            print("Your gear provided an extra "+str(peon.gearBonusProvided)+" mats and you had "+str(peon.goodFortune)+" extra luck!")
            print("\n"+"Ending Bonuses: ")
            print("\n"+"Ending Mastery: "+str(peon.masteryLevel))
            print("Crafting Count Bonus: " + str(peon.currentCraftingItemBonus))
            print("Crafting Difficulty Bonus: " +str(peon.currentCraftingDiffBonus))
            print("Dice Bonus: " +str(peon.diceBonus))
    
        for i in range(len(simulationAttempts)):
             totalSum += simulationAttempts[i]
        print("\n"+"It will you " + str(player.calcTickTime(None,playerTicks))+ " hours to do this")
        print("During this time, you will craft an average of " +str(round(totalSum/len(simulationAttempts),2)) + " items!")
         

    elif selection == '4': 

        playerCurrentMastery = int(input("Input Current Mastery Level: "))
        while playerCurrentMastery < 1 or playerCurrentMastery > 20:
            print("\n"+"Please input a valid Mastery Level (1-20)")
            playerCurrentMastery = int(input("Input Current Mastery Level: "))
            
        craftingDiff = int(input("What difficulty are you grinding out? : "))
        while craftingDiff < 1:
            print("\n"+"Please input a proper difficulty (>1)")
            craftingDiff = int(input("What difficulty are you grinding out?: "))

        playerCurrentNumOfTicks = int(input("How many ticks do you currently have? (Not combined, towards next mastery level): "))
        while playerCurrentNumOfTicks > player.masteryNeeded[playerCurrentMastery-1]:
            print("Hmm, that doesn't compute. Please make sure your current ticks is correct: ")
            playerCurrentNumOfTicks = int(input("How many ticks do you currently have? (Not combined, towards next mastery level): "))

        playerGearBonus = float(input("Got any Gathering Bonus? (Chance +1 Item while gathering bonus only, enter # with decimal. Eg: 154.3): "))
        while playerGearBonus < 0:
            print("You can't be less than naked. Input 0 if you have no gear.")
            playerGearBonus = float(input("Got any Gathering Bonus? (Chance +1 Item while gathering bonus only, enter # with decimal. Eg: 154.3): "))

        simulationTimes = int(input("How many times would you like to run the simulation?: "))
        while simulationTimes < 1:
            print("Why would you try to run 0 simulations? Who are you? What are you doing with your life? Enter a positive number plz")
            simulationTimes = int(input("How many times would you like to run the simulation?: "))

        for i in range(0,simulationTimes):
            peon = craftingCalc(playerCurrentMastery, playerCurrentNumOfTicks)
            peon.setCraftingDifficulty(craftingDiff)
            simulationAttempts.append(peon.gatherMatsTillNextMastery(playerGearBonus))
            print("Simulation " + str(i+1) + " Crafted: " + str(simulationAttempts[i]) + " Mats")
    
        for i in range(len(simulationAttempts)):
             totalSum += simulationAttempts[i]

        print("It will you " + str(peon.calcTime()) + " hours to do this")
        print("During this time, you will craft an average of " +str(round(totalSum/len(simulationAttempts),2)) + " items!")
    
    again = int(input("Run again? 1 = Yes: "))
        
    if (again != 1):
        loop=False

        



