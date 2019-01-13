from graphics import *
import random
from random import shuffle
from colour import Color

def getGradientListRGB(color1,color2,length):
    '''
        Creates a color gradient between two colors and returns the color values in a list
        args:
            color1 (str) - The beginning color
            color2 (str) - The ending color
            length (int) - The length of the gradient list
        returns:
            colors: The gradient list between the two colors
    '''
    red = Color(color1)
    colors = list(red.range_to(Color(color2),length))
    for i in range(len(colors)):
        colors[i] = colors[i].rgb
        newcolor = []
        for c in range(3):
            newcolor.append(int(colors[i][c]*255))
        colors[i] = (newcolor[0],newcolor[1],newcolor[2])
    return colors

class Game:
    def __init__(self,win,numPlayersO,turnByTurnO,turnSkipO,playerMoneyListO,propertiesOwnedListO,posListO,masterHousesListO,masterMortgageListO,middlePotO,masterPropertiesOwnedListO):
        self.j = 0

        self.win = win
        self.numPlayersO = numPlayersO
        self.turnByTurnO = turnByTurnO
        self.turnSkipO = turnSkipO
        self.playerMoneyListO = playerMoneyListO
        self.propertiesOwnedListO = propertiesOwnedListO
        self.posListO = posListO
        self.masterHousesListO = masterHousesListO
        self.masterMortgageListO = masterMortgageListO
        self.middlePotO = middlePotO
        self.masterPropertiesOwnedListO = masterPropertiesOwnedListO

        #Coordinate values of each tile on the board
        self.coordinateValues = []
        for br in range(10,-1,-1):
            self.coordinateValues.append((25 + br * 50,540))
        for lc in range(9,0,-1):
            self.coordinateValues.append((25, 40  + lc * 50))
        for tr in range(11):
            self.coordinateValues.append((25 + tr * 50, 40))
        for rc in range(1,10):
            self.coordinateValues.append((525, 40  + rc * 50))


        #Sets the percent landed on each space to 0
        self.boxValues = [0]*40
        #This is the percent landed in each space after x number of games
        self.ultimateBoxValues = [0]*40

        self.chanceCards = [0,24,11,'U','R','R',"+50","Get out of jail","Back 3","-15",5,39,"giveeach50","+150","+100","Hotel/houses"]

        self.communityCards = ["+100","+100","+100","-150","+10","+45","geteach50","-50",0,"Get out of jail","-100","+200","Hotel/houses","+25","+20","J"]

        #Property prices
        self.propertyPriceList = [None,60,None,60,None,200,100,None,100,120,None,140,150,140,160,200,180,None,180,200,None,220,None,220,240,200,260,260,150,280,None,300,300,None,320,200,None,350,None,400]

        self.propertyHouseCost = [None,50,None,50,None,"R",50,None,50,50,None,100,"U",100,100,"R",100,None,100,100,None,150,None,150,150,"R",150,150,"U",150,None,200,200,None,200,"R",None,200,None,200]

        self.monopolies = [(1,3),(6,8,9),(11,13,14),(16,18,19),(21,23,24),(26,27,29),(31,32,34),(37,39)]

        #Property rent
        self.propertyRentList = [None,2,None,4,None,"R",6,None,6,8,None,10,"U",10,12,"R",14,None,14,16,None,18,None,18,20,"R",22,22,"U",24,None,26,26,None,28,"R",None,35,None,40]
        self.oneHouseRent = [None,10,None,20,None,"R",30,None,30,40,None,50,"U",50,60,"R",70,None,70,80,None,90,None,90,100,"R",110,110,"U",120,None,130,130,None,150,"R",None,175,None,200]
        self.twoHousesRent = [None,30,None,60,None,"R",90,None,90,100,None,150,
        "U",150,180,"R",200,None,200,220,None,250,None,250,300,"R",330,330,"U",360,None,390,390,None,450,"R",None,500,None,600]
        self.threeHousesRent = [None,90,None,180,None,"R",270,None,270,300,None,450,"U",450,500,"R",550,None,550,600,None,700,None,700,750,"R",800,800,"U",850,None,900,900,None,1000,"R",None,1100,None,1400]
        self.fourHousesRent = [None,160,None,320,None,"R",400,None,400,450,None,625,"U",625,700,"R",750,None,750,800,None,875,None,875,925,"R",975,975,"U",1025,None,1100,1100,None,1200,"R",None,1300,None,1700]
        self.hotelRent = [None,250,None,450,None,"R",550,None,550,600,None,750,"U",750,900,"R",950,None,950,1000,None,1050,None,1050,1100,"R",1150,1150,"U",1200,None,1275,1275,None,1400,"R",None,1500,None,2000]

        self.numPlayers = self.numPlayersO
        self.turnByTurn = self.turnByTurnO
        self.turnSkip = self.turnSkipO

        self.wins = [0]*self.numPlayers
        self.losses = [0]*self.numPlayers
        self.ties = [0]*self.numPlayers

        self.winningProperties = [0]*40
        self.losingProperties = [0]*40
        self.propertyLostOn = [0]*40

        self.averageTurns = 0
        self.maxTurns = 0

        self.gameState = []
        self.gamesWon = [[],[],[],[],[],[],[],[],[],[]]

        self.nonProperties = [0,2,4,7,10,17,20,22,30,33,36,38]

        #Strategy variables
        self.moneyToBuyHouse = 200
        self.minValueToBuyProperty = 0

    def drawBoard(self):
        '''
            Draws the game board
        '''

        #Drawing grid
        for r in range(0,550,50):
            line = Line(Point(r,0),Point(r,550))
            line.draw(self.win)
        for c in range(0,550,50):
            line = Line(Point(0,c),Point(550,c))
            line.draw(self.win)
        rectangle = Rectangle(Point(50,50), Point(500,500))
        rectangle.setFill('white')
        rectangle.draw(self.win)

        #Text
        coordinateValues = []
        for br in range(10,-1,-1):
            coordinateValues.append((25 + br * 50,500))
        for lc in range(9,0,-1):
            coordinateValues.append((25, lc * 50))
        for tr in range(11):
            coordinateValues.append((25 + tr * 50, 0))
        for rc in range(1,10):
            coordinateValues.append((525, rc * 50))

        names = ['GO_','Mediterr..._Avenue', 'Community_Chest', 'Baltic_Avenue', 'Income_Tax', 'Reading_Railroad', 'Oriental_Avenue', 'Chance_', 'Vermont_Avenue', 'Connecticut_Avenue', 'In_Jail', 'St. Charles_Place', 'Electric_Company', 'States_Avenue', 'Virginia_Avenue', 'Pennsylvania_Railroad', 'St. James_Place', 'Community_Chest', 'Tennessee_Avenue', 'New York_Avenue', 'Free_Parking', 'Kentucky_Avenue', 'Chance_', 'Indiana_Avenue', 'Illinois_Avenue', 'B. & O._Railroad', 'Atlantic_Avenue', 'Ventnor_Avenue', 'Water_Works', 'Marvin_Gardens', 'Go To_Jail', 'Pacific_Avenue', 'North Carolina_Avenue', 'Community_Chest', 'Pennsylvania_Avenue', 'Short_Line', 'Chance_', 'Park_Place', 'Luxury_Tax', 'Boardwalk_']

        for n in range(len(names)):
            name = names[n]
            br = name.find("_")
            labelTop = Text(Point(coordinateValues[n][0],10+coordinateValues[n][1]), name[:br])
            labelBottom = Text(Point(coordinateValues[n][0],20+coordinateValues[n][1]), name[br+1:])
            labelTop.setSize(10)
            labelBottom.setSize(10)
            labelTop.draw(self.win)
            labelBottom.draw(self.win)

        #Big Monopoly Text
        monopolyTitle = Text(Point(275,275),"Monopoly")
        monopolyTitle.setSize(35)
        monopolyTitle.draw(self.win)

    def simulate(self):
        '''
            Simulates a full game of monopoly
        '''

        self.playerMoneyList = self.playerMoneyListO.copy()
        self.propertiesOwnedList = [[],[],[],[],[],[],[],[],[],[],[]]
        for n in range(len(self.propertiesOwnedListO)):
            self.propertiesOwnedList[n] = self.propertiesOwnedListO[n].copy()
        self.posList = self.posListO.copy()
        self.masterHousesList = self.masterHousesListO.copy()
        self.masterMortgageList = self.masterMortgageListO.copy()
        self.middlePot = self.middlePotO
        self.masterPropertiesOwnedList = self.masterPropertiesOwnedListO.copy()

        self.turnsPlayed = 0

        #Number of players
        self.players = list(range(self.numPlayers))

        #initalizes players and text
        self.colors = ["blue", "orange","purple","black","cyan","magenta","lime","gold","dark green","maroon"]
        self.playerTextPos = []
        self.CommunityFreePos = []
        self.ChanceFreePos = []

        if self.numPlayers > 2:
            self.playerTextStep = 350//((self.numPlayers-1)//2)
        else:
            self.playerTextStep = 0
        for n in range(self.numPlayers):
            if n%2 == 0:
                self.playerTextPos.append((100,100+((n+1)//2)*self.playerTextStep))
                self.CommunityFreePos.append((80,120+((n+1)//2)*self.playerTextStep))
                self.ChanceFreePos.append((120,120+((n+1)//2)*self.playerTextStep))
            else:
                self.playerTextPos.append((450,100+(n//2)*self.playerTextStep))
                self.CommunityFreePos.append((430,120+((n+1)//2)*self.playerTextStep))
                self.ChanceFreePos.append((470,120+((n+1)//2)*self.playerTextStep))


        self.CommunityFreeTextList = []
        self.ChanceFreeTextList = []

        self.playerTextList = []
        self.playerCircleList = []

        #Jail
        self.getOutofJailCard = [0]*self.numPlayers
        self.inJail = [False]*self.numPlayers

        #Count how many doubles have been thrown (or how many times has been rolled to escape jail)
        self.rollCounter = 0
        #How long a player has been in jail
        self.inJailCounter = 0

        #Creating most of the player-related middle text
        for p in range(self.numPlayers):
            if self.turnByTurn:
                self.playerTextList.append(Text(Point(self.playerTextPos[p][0],self.playerTextPos[p][1]),"Player" + str(p+1) + ": " + str(self.playerMoneyList[p])))
                self.playerTextList[p].setTextColor(self.colors[p])
                self.playerTextList[p].draw(self.win)

                self.playerCircleList.append(Circle(Point(525,525), 7))
                self.playerCircleList[p].draw(self.win)
                self.playerCircleList[p].setFill(self.colors[p])

                #Get out of Jail Free icon
                self.CommunityFreeTextList.append(Text(Point(self.CommunityFreePos[p][0],self.CommunityFreePos[p][1]),"Free"))
                self.CommunityFreeTextList[p].setTextColor("white")
                self.CommunityFreeTextList[p].draw(self.win)

                self.ChanceFreeTextList.append(Text(Point(self.ChanceFreePos[p][0],self.ChanceFreePos[p][1]),"Free"))
                self.ChanceFreeTextList[p].setTextColor("white")
                self.ChanceFreeTextList[p].draw(self.win)

        #Shuffle chance cards
        self.chance = [i for i in self.chanceCards]
        shuffle(self.chance)

        #Shuffle community cards
        self.community = [i for i in self.communityCards]
        shuffle(self.community)

        won = False

        while not won:
            #Roll for each player
            for p in self.players:
                done = False
                rollCounter = 0

                while not done:
                    if self.turnByTurn:
                        print()
                        print("Player " + str(p+1))
                        print("Pos: " + str(self.posList[p]))

                    #Unmortgaging properties
                    for property in self.propertiesOwnedList[p]:
                        #First try to mortgage a property without a house
                        if property in self.masterMortgageList and self.playerMoneyList[p] > (self.propertyPriceList[property]//2):
                            self.masterMortgageList.remove(property)
                            self.playerMoneyList[p] -= (self.propertyPriceList[property]//2)

                            #drawing
                            if self.turnByTurn:
                                mortgageCircle = Circle(Point(self.coordinateValues[property][0]+17,self.coordinateValues[property][1] - 11),5)
                                mortgageCircle.setFill("white")
                                mortgageCircle.setOutline("white")
                                mortgageCircle.draw(win)

                    #Buying houses
                    for m in self.monopolies:
                        haveMonopoly = True
                        for v in m:
                            if v not in self.propertiesOwnedList[p]:
                                haveMonopoly = False
                        if haveMonopoly == True:
                            while self.playerMoneyList[p] > self.propertyHouseCost[v] and (p != 0 or self.playerMoneyList[p] - self.propertyHouseCost[v] > self.moneyToBuyHouse):
                                self.playerMoneyList[p] -= self.propertyHouseCost[v]
                                if len(m) == 3:
                                    if self.masterHousesList[m[0]] >= 5 and self.masterHousesList[m[1]] >= 5 and self.masterHousesList[m[2]] >= 5:
                                        break

                                    if self.masterHousesList[m[2]] <= self.masterHousesList[m[1]] and self.masterHousesList[m[1]] <= self.masterHousesList[m[0]]:
                                        self.masterHousesList[m[2]] += 1
                                    elif self.masterHousesList[m[1]] <= self.masterHousesList[m[0]]:
                                        self.masterHousesList[m[1]] += 1
                                    else:
                                        self.masterHousesList[m[0]] += 1

                                if len(m) == 2:
                                    if self.masterHousesList[m[0]] >= 5 and self.masterHousesList[m[1]] >= 5:
                                        break

                                    if self.masterHousesList[m[1]] <= self.masterHousesList[m[0]] and self.masterHousesList[m[1]] < 5:
                                        self.masterHousesList[m[1]] += 1
                                    elif self.masterHousesList[m[0]] < 5:
                                        self.masterHousesList[m[0]] += 1

                            if self.turnByTurn:
                                for i in range(len(m)):
                                    housesText = Circle(Point(self.coordinateValues[m[i]][0]-15,self.coordinateValues[m[i]][1] - 10),5)
                                    housesText.setFill("white")
                                    housesText.setOutline("white")
                                    housesText.draw(win)
                                for i in range(len(m)):
                                    housesText = Text(Point(self.coordinateValues[m[i]][0]-20,self.coordinateValues[m[i]][1] - 10), "h: " + str(self.masterHousesList[m[i]]))
                                    housesText.setTextColor("green")
                                    housesText.draw(win)

                    self.die1 = random.randrange(1,7)
                    self.die2 = random.randrange(1,7)

                    if self.die1 != self.die2:
                        done = True
                    else:
                        self.rollCounter += 1

                    #Jail functionality
                    if self.inJail[p] == True:
                        if self.getOutofJailCard[p] > 0:
                            self.getOutofJailCard[p] -= 1
                            self.inJail[p] = False
                            self.inJailCounter = 0
                            if self.turnByTurn:
                                if self.getOutofJailCard[p] == 1:
                                    self.ChanceFreeTextList[p].setTextColor("white")
                                else:
                                    self.CommunityFreeTextList[p].setTextColor("white")
                                    self.ChanceFreeTextList[p].setTextColor("white")
                        elif self.playerMoneyList[p] > 50:
                            self.playerMoneyList[p] -= 50
                            self.middlePot += 50
                            self.inJail[p] = False
                            self.inJailCounter = 0
                        elif self.rollCounter > 0:
                            self.inJail[p] = False
                            #You don't move on the double, you roll again
                            self.die1 = 0
                            self.die2 = 0
                            self.inJailCounter = 0
                        elif self.inJailCounter >=3:
                            #After three rolls, move out of jail but don't roll
                            self.done = True
                            self.inJail[p] = False
                            self.inJailCounter = 0
                        else:
                            self.die1 = 0
                            self.die2 = 0
                            self.inJailCounter += 1


                    #If you've rolled doubles three times
                    if self.rollCounter >= 3:
                        self.inJail[p] = True
                        self.posList[p] = 10
                        self.rollCounter = 0
                        self.die1 = 0
                        self.die2 = 0

                    self.posList[p] += self.die1 + self.die2

                    #If you roll snake eyes
                    if self.die1 == 1 and self.die2 == 1:
                        self.playerMoneyList[p] += 100

                    #Landing on go = extra $200
                    if self.posList[p] == 40:
                        self.playerMoneyList[p] += 200

                    #If you pass go
                    if self.posList[p] >= 40:
                        self.posList[p] -= 40
                        self.playerMoneyList[p] += 200

                    #If you land on "Go to jail", go to jail
                    if self.posList[p] == 30:
                        self.posList[p] = 10
                        self.inJail[p] = True

                    #If you land on "Free Parking", get the pot
                    if self.posList[p] == 20:
                        self.playerMoneyList[p] += self.middlePot
                        self.middlePot = 500

                    #If you land on "chance"
                    if self.posList[p] == 7 or self.posList[p] == 22 or self.posList[p] == 36:
                        if len(self.chance) == 0:
                            self.chance = [i for i in self.chanceCards]
                            shuffle(self.chance)
                        if isinstance(self.chance[0],int):
                            self.posList[p] = self.chance[0]
                        elif self.chance[0] == 'U':
                            if self.posList[p] > 11:
                                self.posList[p] = 28
                            else:
                                self.posList[p] = 12
                        elif self.chance[0] == 'R':
                            if self.posList[p] < 5 or self.posList[p] >= 35:
                                self.posList[p] = 5
                            elif self.posList[p] < 15:
                                self.posList[p] = 15
                            elif self.posList[p] < 25:
                                self.posList[p] = 25
                            else:
                                self.posList[p] = 35
                        elif self.chance[0] == "Back 3":
                            self.posList[p] -= 3

                        #Money chance cards
                        elif self.chance[0][0] == "+":
                            self.playerMoneyList[p] += int(self.chance[0][1:])
                        elif self.chance[0][0] == "-":
                            self.playerMoneyList[p] -= int(self.chance[0][1:])
                            self.middlePot += int(self.chance[0][1:])

                        #Other cards
                        elif self.chance[0] == "giveeach50":
                            for player in self.players:
                                self.playerMoneyList[p] -= 50
                                self.playerMoneyList[player] += 50
                        elif self.chance[0] == "Get out of jail":
                            self.getOutofJailCard[p] += 1
                            if self.turnByTurn:
                                self.ChanceFreeTextList[p].setTextColor("green")
                        elif self.chance[0] == "Hotel/houses":
                            pass

                        #Only run this if you want to simulate each turn at a time
                        if self.turnByTurn:
                            chanceText = Text(Point(275,400), "Chance: " + str(self.chance[0]))
                            chanceText.setSize(20)
                            chanceText.draw(self.win)
                            if self.turnsPlayed % self.turnSkip == 0:
                                self.win.getMouse()
                            chanceText.setTextColor("white")

                            print("Chance: " + str(self.chance[0]))
                        self.chance.pop(0)

                    #Community Chest
                    if self.posList[p] == 2 or self.posList[p] == 17 or self.posList[p] == 33:
                        if len(self.community) == 0:
                            self.community = [i for i in self.communityCards]
                            shuffle(self.community)
                        if isinstance(self.community[0],int):
                            self.posList[p] = self.community[0]

                        #Money cards
                        elif self.community[0][0] == "+":
                            self.playerMoneyList[p] += int(self.community[0][1:])
                        elif self.community[0][0] == "-":
                            self.playerMoneyList[p] -= int(self.community[0][1:])
                            self.middlePot += int(self.community[0][1:])

                        #Other cards
                        elif self.community[0] == "geteach50":
                            for player in self.players:
                                self.playerMoneyList[p] += 50
                                self.playerMoneyList[player] -= 50
                        elif self.community[0] == "Get out of jail":
                            self.getOutofJailCard[p] += 1
                            if self.turnByTurn:
                                self.CommunityFreeTextList[p].setTextColor("green")
                        elif self.community[0] == "J":
                            self.inJail[p] = True
                            self.posList[p] = 10
                        elif self.community[0] == "Hotel/houses":
                            pass

                        #Only run this if you want to simulate each turn at a time
                        if self.turnByTurn:
                            communityText = Text(Point(275,400), "Community Chest: " + str(self.community[0]))
                            communityText.setSize(20)
                            communityText.draw(self.win)
                            if self.turnsPlayed % self.turnSkip == 0:
                                self.win.getMouse()
                            communityText.setTextColor("white")

                            print("Community Chest: " + str(self.community[0]))


                        self.community.pop(0)


                    #If the player lands on an unowned property
                    if isinstance(self.propertyPriceList[self.posList[p]],int) and (self.posList[p] not in self.masterPropertiesOwnedList):
                        #If the player can afford it
                        if self.propertyPriceList[self.posList[p]] < self.playerMoneyList[p]  and (p != 0 or self.playerMoneyList[p]-self.propertyPriceList[self.posList[p]] > self.minValueToBuyProperty):
                            self.masterPropertiesOwnedList.append(self.posList[p])
                            self.propertiesOwnedList[p].append(self.posList[p])
                            self.playerMoneyList[p] -= self.propertyPriceList[self.posList[p]]

                            if self.turnByTurn:
                                propertyText = Text(Point(self.coordinateValues[self.posList[p]][0],self.coordinateValues[self.posList[p]][1] - 10), p+1)
                                propertyText.setTextColor(self.colors[p])
                                propertyText.draw(self.win)

                    #If the player lands on a owned property (not mortgaged) - RENT
                    if self.posList[p] in self.masterPropertiesOwnedList and self.posList[p] not in self.propertiesOwnedList[p] and self.posList[p] not in self.masterMortgageList:
                        for player in range(len(self.propertiesOwnedList)):
                            if self.posList[p] in self.propertiesOwnedList[player]:
                                if isinstance(self.propertyRentList[self.posList[p]],int):
                                    if self.masterHousesList[self.posList[p]] == 0:
                                        self.playerMoneyList[p] -= self.propertyRentList[self.posList[p]]
                                        self.playerMoneyList[player] += self.propertyRentList[self.posList[p]]
                                    elif self.masterHousesList[self.posList[p]] == 1:
                                        self.playerMoneyList[p] -= self.oneHouseRent[self.posList[p]]
                                        self.playerMoneyList[player] += self.oneHouseRent[self.posList[p]]
                                    elif self.masterHousesList[self.posList[p]] == 2:
                                        self.playerMoneyList[p] -= self.twoHousesRent[self.posList[p]]
                                        self.playerMoneyList[player] += self.twoHousesRent[self.posList[p]]

                                    elif self.masterHousesList[self.posList[p]] == 3:
                                        self.playerMoneyList[p] -= self.threeHousesRent[self.posList[p]]
                                        self.playerMoneyList[player] += self.threeHousesRent[self.posList[p]]

                                    elif self.masterHousesList[self.posList[p]] == 4:
                                        self.playerMoneyList[p] -= self.fourHousesRent[self.posList[p]]
                                        self.playerMoneyList[player] += self.fourHousesRent[self.posList[p]]

                                    elif self.masterHousesList[self.posList[p]] == 5:
                                        self.playerMoneyList[p] -= self.hotelRent[self.posList[p]]
                                        self.playerMoneyList[player] += self.hotelRent[self.posList[p]]

                                #If it's a railroad
                                elif self.propertyRentList[self.posList[p]] == "R":
                                    multiplier = .5
                                    if 5 in self.propertiesOwnedList[player]:
                                        multiplier *= 2
                                    if 15 in self.propertiesOwnedList[player]:
                                        multiplier *= 2
                                    if 25 in self.propertiesOwnedList[player]:
                                        multiplier *= 2
                                    if 35 in self.propertiesOwnedList[player]:
                                        multiplier *= 2
                                    multiplier = int(multiplier)
                                    self.playerMoneyList[p] -= 25*multiplier
                                    self.playerMoneyList[player] += 25*multiplier
                                #If it's a utility
                                elif self.propertyRentList[self.posList[p]] == "U":
                                    self.playerMoneyList[p] -= (self.die1+self.die2)*10
                                    self.playerMoneyList[player] += (self.die1+self.die2)*10


                    #Landing on squares that make you pay taxes
                    if self.posList[p] == 4:
                        if self.playerMoneyList[p] >= 2000:
                            self.playerMoneyList[p] -= 200
                            self.middlePot += 200
                        else:
                            self.playerMoneyList[p] -= (self.playerMoneyList[p]//10)
                            self.middlePot += (self.playerMoneyList[p]//10)
                    if self.posList[p] == 38:
                        self.playerMoneyList[p] -= 75
                        self.middlePot += 75

                    #If you have zero or negative money after paying rent/taxes
                    if self.playerMoneyList[p] <= 0:
                        for i in [True,False]: #On the first iteration only sell no houses, on the second iteration sell anything
                            for property in self.propertiesOwnedList[p]:
                                #First try to mortgage a property without a house
                                if property not in self.masterMortgageList and self.masterHousesList[property] == 0 and i:
                                    self.masterMortgageList.append(property)
                                    self.playerMoneyList[p] += (self.propertyPriceList[property]//2)
                                #Second, sell anything
                                elif property not in self.masterMortgageList and not i:
                                    self.masterMortgageList.append(property)
                                    self.playerMoneyList[p] += (self.propertyPriceList[property]//2)

                                #If nothing happened, break out of the loop
                                else:
                                    continue

                                #Printing it out
                                if self.turnByTurn:

                                    mortgageText = Text(Point(self.coordinateValues[property][0]+17,self.coordinateValues[property][1] - 10), "M")
                                    mortgageText.setTextColor("Red")
                                    mortgageText.draw(win)

                                #If the player has more than zero dollars, break out of the loop
                                if self.playerMoneyList[p] > 0:
                                    break
                            if self.playerMoneyList[p] > 0:
                                break

                    #if the player still has zero or less money even after mortgaging, the player loses
                    if self.playerMoneyList[p] <= 0:

                        #erasing player
                        if self.turnByTurn:
                            #Player
                            self.playerCircleList[p].setOutline("white")
                            self.playerCircleList[p].setFill("white")

                        for property in self.propertiesOwnedList[p]:

                            #drawing

                            if self.turnByTurn:
                                #mortgage
                                if property in self.masterMortgageList:
                                    mortgageCircle = Circle(Point(self.coordinateValues[property][0]+17,self.coordinateValues[property][1] - 11),6)
                                    mortgageCircle.setFill("white")
                                    mortgageCircle.setOutline("white")
                                    mortgageCircle.draw(win)

                                #Properties Owned
                                propertyCircle = Circle(Point(self.coordinateValues[property][0],self.coordinateValues[property][1] - 10), 6)
                                propertyCircle.setFill("white")
                                propertyCircle.setOutline("white")
                                propertyCircle.draw(win)

                                #Houses
                                housesText = Circle(Point(self.coordinateValues[property][0]-15,self.coordinateValues[property][1] - 10),6)
                                housesText.setFill("white")
                                housesText.setOutline("white")
                                housesText.draw(win)

                            #Remove properties from master lists
                            if len(self.players) > 2: #This just helps with displaying 2nd place statistics
                                if property in self.masterMortgageList:
                                    self.masterMortgageList.remove(property)
                                if property in self.masterPropertiesOwnedList:
                                    self.masterPropertiesOwnedList.remove(property)
                                self.masterHousesList[property] = 0

                        #If there are still players left, clear propertiesOwnedList - This is useful to show the statistics of 2nd place
                        if len(self.players) > 2:
                            self.propertiesOwnedList[p].clear()

                        self.losses[p] += 1
                        self.propertyLostOn[self.posList[p]] += 1
                        for property in self.propertiesOwnedList[p]:
                            self.losingProperties[property] += 1
                        try:
                            self.players.remove(p)
                        except ValueError:
                            print(self.j)
                        done = True

                    #If there is only one player left
                    if len(self.players) == 1:
                        won = True
                        done = True
                        for player in self.players:
                            self.wins[player] += 1
                            self.gamesWon[player].append(self.j+1)
                            #Adding up properties owned
                            for property in self.propertiesOwnedList[player]:
                                self.winningProperties[property] += 1

                        if self.turnByTurn:
                            rect = Rectangle(Point(0, 0), Point(550,550))
                            rect.setFill("white")
                            rect.draw(self.win)
                            self.drawBoard()
                        self.averageTurns += self.turnsPlayed
                        if self.turnsPlayed > self.maxTurns:
                            self.maxTurns = self.turnsPlayed

                    elif self.turnsPlayed >= 1000:
                        won = True
                        done = True
                        for player in self.players:
                            self.ties[player] += 1
                        self.players = [] #This is important to stop continuing the for loop. It can cause the value of ties to be much higher than it actually is


                    #Only run this if you want to simulate each turn at a time
                    if self.turnByTurn:
                        self.playerCircleList[p].setOutline("white")
                        self.playerCircleList[p].setFill("white")
                        self.playerTextList[p].setTextColor("white")

                        self.playerCircleList[p] = Circle(Point(self.coordinateValues[self.posList[p]][0],self.coordinateValues[self.posList[p]][1]), 6)
                        self.playerCircleList[p].draw(self.win)
                        self.playerCircleList[p].setFill(self.colors[p])


                        self.playerTextList[p] = Text(Point(self.playerTextPos[p][0],self.playerTextPos[p][1]),"Player" + str(p+1) + ": " + str(self.playerMoneyList[p]))
                        self.playerTextList[p].setTextColor(self.colors[p])
                        self.playerTextList[p].draw(self.win)

                        #Jail text
                        jailIcon = Text(Point(self.coordinateValues[10][0],self.coordinateValues[10][1]-10), "J")
                        jailIcon.setTextColor("white")
                        jailIcon.draw(self.win)

                        for player in self.players:
                            if self.inJail[player] == True:
                                jailIcon.setTextColor("red")

                        rollText = Text(Point(275,200), "Roll: " + str(self.die1) + " + " + str(self.die2) + " = " + str(self.die1+self.die2))
                        rollText.setSize(25)
                        rollText.draw(self.win)

                        middlePotText = Text(Point(275,310), "Middle Pot: " + str(self.middlePot))
                        middlePotText.setSize(15)
                        middlePotText.draw(self.win)

                        turnsPlayedText = Text(Point(275,480), "Turns Played: " + str(self.turnsPlayed))
                        turnsPlayedText.setSize(15)
                        turnsPlayedText.draw(self.win)

                        #Printing to terminal
                        print("Roll: " + str(self.die1) + " + " + str(self.die2) + " = " + str(self.die1+self.die2))
                        print("Money" + ": " + str(self.playerMoneyList[p]))

                        if self.turnsPlayed % self.turnSkip == 0:
                            self.win.getMouse()


                        rollText.setTextColor("white")
                        middlePotText.setTextColor("white")
                        turnsPlayedText.setTextColor("white")



                self.turnsPlayed += 1
                self.boxValues[self.posList[p]] += 1



        for v in range(len(self.boxValues)):
            self.boxValues[v] = (self.boxValues[v]/self.turnsPlayed)
            self.ultimateBoxValues[v] += self.boxValues[v]


        #Saving end game state
        self.gameState.append(self.__dict__.copy())
        # gameInfoDict[j] = [playerMoneyList.copy(),[l.copy() for l in propertiesOwnedList],posList.copy(),masterHousesList.copy(),masterMortgageList.copy(),middlePot,masterPropertiesOwnedList.copy(), turnsPlayed ,inJail]


    def simulateMany(self,num):
        '''
            Simulates a specific number of games
            args: num (int) - The number of games to simulate
        '''
        for self.j in range(num):
            self.simulate()

    def findStrategy(self):
        '''
            Changes vairables to find the ideal strategy
        '''
        self.maxWins = 0
        self.minWins = 100
        strategyList = []
        for i in range(40):
            self.minValueToBuyProperty = random.choice([0,65])
            self.moneyToBuyHouse = 50*i
            self.wins[0] = 0
            for self.j in range(100):
                self.simulate()
            if  self.wins[0] > self.maxWins:
                strategyList.clear()
                strategyList.append((self.j+1)*(i+1))
                strategyList.append("minValueToBuyProperty: " + str(self.minValueToBuyProperty))
                strategyList.append("moneyToBuyHouse: " + str(self.moneyToBuyHouse))
                self.maxWins = self.wins[0]
            # print(self.wins[0])
            # print(((self.j+1)*(i+1)))
            # print("minValueToBuyProperty: " + str(self.minValueToBuyProperty))
            # print(("moneyToBuyHouse: " + str(self.moneyToBuyHouse)))
            # print()
        print(self.maxWins)
        print(strategyList)

    def displayWinLossTieRatio(self):
        '''
            Displays each player's win, loss and tie ratio
        '''

        self.numWins = 0
        self.numLosses = 0
        self.numTies = 0

        for i in range(len(self.wins)):
            self.numWins += self.wins[i]
            self.wins[i] = self.wins[i]/(self.j+1)

        for i in range(len(self.losses)):
            self.numLosses += self.losses[i]
            self.losses[i] = self.losses[i]/(self.j+1)

        for i in range(len(self.ties)):
            self.numTies += self.ties[i]
            self.ties[i] = self.ties[i]/(self.j+1)

        print(self.wins)
        print(self.losses)
        print(self.ties)

        wlt = Text(Point(275,420), "Wins | " + str(self.wins))
        wlt.setTextColor('green')
        wlt.draw(self.win)
        wlt = Text(Point(275,440), "Losses | " + str(self.losses))
        wlt.setTextColor('red')
        wlt.draw(self.win)
        wlt = Text(Point(275,460), "Ties | " + str(self.ties))
        wlt.setTextColor('orange')
        wlt.draw(self.win)

    def displayPercentLandedOn(self):
        '''
            Percent of the time players landed on each square
        '''
        for v in range(len(self.ultimateBoxValues)):
            self.ultimateBoxValues[v] = round(self.ultimateBoxValues[v]/(self.j+1)*100,3)
        print(self.ultimateBoxValues)


        #Sort the percentages in a list - used for color coding
        sortedValues = self.ultimateBoxValues.copy()
        for i in range(len(self.nonProperties)):
            sortedValues.pop(self.nonProperties[i]-i)
        sortedValues.sort()
        print(sortedValues)

        #Draw on the board color coded
        gradient = getGradientListRGB("red","green",28)

        for i in range(len(self.ultimateBoxValues)):
            if i not in self.nonProperties:
                percent = Text(Point(self.coordinateValues[i][0],self.coordinateValues[i][1]), self.ultimateBoxValues[i])
                v = sortedValues.index(self.ultimateBoxValues[i])
                textcolor = color_rgb(gradient[v][0],gradient[v][1],gradient[v][2])
                percent.setTextColor(textcolor)
                percent.draw(self.win)

        print("Average Turns:" + str(self.averageTurns/(self.j+1)))
        print("Max Turns:" + str(self.maxTurns))

    def displayWinningProperties(self):
        accum = 0
        for p in range(len(self.winningProperties)):
            accum += self.winningProperties[p]
            self.winningProperties[p] = round(self.winningProperties[p]/self.numWins,3)

        accum = Text(Point(150,100), "Winner property percent: " + str(round(accum/self.numWins/28*100,2)))
        accum.setTextColor('green')
        accum.draw(self.win)




        #Sort the percentages in a list - used for color coding
        sortedValues = self.winningProperties.copy()
        sortedValues.sort()
        sortedValues = sortedValues[12:]

        #Draw on the board color coded
        gradient = getGradientListRGB("red","green",28)

        for i in range(len(self.winningProperties)):
            if i not in self.nonProperties:
                percent = Text(Point(self.coordinateValues[i][0],self.coordinateValues[i][1]-10), self.winningProperties[i])
                v = sortedValues.index(self.winningProperties[i])
                textcolor = color_rgb(gradient[v][0],gradient[v][1],gradient[v][2])
                percent.setTextColor(textcolor)
                percent.draw(self.win)

    def displayLosingProperties(self):
        accum = 0
        for p in range(len(self.losingProperties)):
            accum += self.losingProperties[p]
            self.losingProperties[p] = round(self.losingProperties[p]/self.numLosses,3)

        accum = Text(Point(400,100), "Loser property percent: " + str(round(accum/self.numLosses/28*100,2)))
        accum.setTextColor('red')
        accum.draw(self.win)



        #Sort the percentages in a list - used for color coding
        sortedValues = self.losingProperties.copy()
        sortedValues.sort()
        sortedValues = sortedValues[12:]

        #Draw on the board color coded
        gradient = getGradientListRGB("red","green",28)

        for i in range(len(self.losingProperties)):
            if i not in self.nonProperties:
                percent = Text(Point(self.coordinateValues[i][0],self.coordinateValues[i][1]), self.losingProperties[i])
                v = sortedValues.index(self.losingProperties[i])
                textcolor = color_rgb(gradient[v][0],gradient[v][1],gradient[v][2])
                percent.setTextColor(textcolor)
                percent.draw(self.win)

    def displayLostOnProperties(self):
        for p in range(len(self.propertyLostOn)):
            self.propertyLostOn[p] = round(self.propertyLostOn[p]/self.numLosses,3)

        #Sort the percentages in a list - used for color coding
        sortedValues = self.propertyLostOn.copy()
        for i in range(len(self.nonProperties)):
            sortedValues.pop(self.nonProperties[i]-i)
        sortedValues.sort()

        #Draw on the board color coded
        gradient = getGradientListRGB("red","green",28)

        for i in range(len(self.propertyLostOn)):
            if i not in self.nonProperties:
                percent = Text(Point(self.coordinateValues[i][0],self.coordinateValues[i][1]), self.propertyLostOn[i])
                v = sortedValues.index(self.propertyLostOn[i])
                textcolor = color_rgb(gradient[v][0],gradient[v][1],gradient[v][2])
                percent.setTextColor(textcolor)
                percent.draw(self.win)

    def displaySpecificGame(self):
        self.win.getMouse()
        gameNum = None
        players = list(range(self.numPlayers))

        for p in players:
            print("Games Won P" + str(p+1) + ": " + str(self.gamesWon[p]))

        while gameNum != -1:
            #Resetting board
            rect = Rectangle(Point(0, 0), Point(550,550))
            rect.setFill("white")
            rect.draw(self.win)
            self.drawBoard()

            gameNum = int(input("Input game number to display (0 to quit): ")) - 1
            self.__dict__ = self.gameState[gameNum]

            # playerMoneyList = gameList[0]
            # propertiesOwnedList = gameList[1]
            # posList = gameList[2]
            # masterHousesList = gameList[3]
            # masterMortgageList = gameList[4]
            # middlePot = gameList[5]
            # masterPropertiesOwnedList = gameList[6]
            # turnsPlayed = gameList[7]
            # inJail = gameList[8]

            playerTextList = []
            playerCircleList = []
            for p in range(self.numPlayers):
                playerTextList.append(Text(Point(self.playerTextPos[p][0],self.playerTextPos[p][1]),"Player" + str(p+1) + ": " + str(self.playerMoneyList[p])))
                playerTextList[p].setTextColor(self.colors[p])
                playerTextList[p].draw(self.win)

                playerCircleList.append(Circle(Point(525,525), 7))
                playerCircleList[p].draw(self.win)
                playerCircleList[p].setFill(self.colors[p])

            for p in players:

                playerCircleList[p].setOutline("white")
                playerCircleList[p].setFill("white")
                playerTextList[p].setTextColor("white")

                playerCircleList[p] = Circle(Point(self.coordinateValues[self.posList[p]][0]+2*p,self.coordinateValues[self.posList[p]][1]), 6)
                playerCircleList[p].draw(self.win)
                playerCircleList[p].setFill(self.colors[p])

                playerTextList[p] = Text(Point(self.playerTextPos[p][0],self.playerTextPos[p][1]),"Player" + str(p+1) + ": " + str(self.playerMoneyList[p]))
                playerTextList[p].setTextColor(self.colors[p])
                playerTextList[p].draw(self.win)

            #Jail text
            jailIcon = Text(Point(self.coordinateValues[10][0],self.coordinateValues[10][1]-10), "J")
            jailIcon.setTextColor("white")
            jailIcon.draw(self.win)

            for player in self.players:
                if self.inJail[player] == True:
                    jailIcon.setTextColor("red")

            middlePotText = Text(Point(275,310), "Middle Pot: " + str(self.middlePot))
            middlePotText.setSize(15)
            middlePotText.draw(self.win)

            turnsPlayedText = Text(Point(275,480), "Turns Played: " + str(self.turnsPlayed))
            turnsPlayedText.setSize(15)
            turnsPlayedText.draw(self.win)

            for p in range(len(self.propertiesOwnedList)):
                for property in self.propertiesOwnedList[p]:
                    propertyText = Text(Point(self.coordinateValues[property][0],self.coordinateValues[property][1] - 10), p+1)
                    propertyText.setTextColor(self.colors[p])
                    propertyText.draw(self.win)

            for h in range(len(self.masterHousesList)):
                if self.masterHousesList[h] > 0:
                    housesText = Text(Point(self.coordinateValues[h][0]-20,self.coordinateValues[h][1] - 10), "h: " + str(self.masterHousesList[h]))
                    housesText.setTextColor("green")
                    housesText.draw(self.win)
            for property in self.masterMortgageList:
                mortgageText = Text(Point(self.coordinateValues[property][0]+17,self.coordinateValues[property][1] - 10), "M")
                mortgageText.setTextColor("Red")
                mortgageText.draw(self.win)


            self.win.getMouse()
            middlePotText.setTextColor("white")
            turnsPlayedText.setTextColor("white")


def main():

    ################## Edit Starting Values ####################
    numPlayers = 10 #Number of players
    turnByTurn = False #True for one game at a time, False for 10,000 game simulation
    turnSkip = 1 #Number of turns played after click

    playerMoneyList = [1017,1017,1017,1017,1017,1017,1017,1017,1017,1017] #Starting money
    propertiesOwnedList = [[],[],[],[],[],[],[],[],[],[]] #Starting properties (0-39)
    posList = [0,0,0,0,0,0,0,0,0,0] #Starting position (0-39)

    masterHousesList = [
    0,
    0, #Mediterranean
    0,
    0, #Baltic
    0,
    0,
    0, #Oriental
    0,
    0, #Vermont
    0, #Connecticut
    0,
    0, #St. Charles
    0,
    0, #States
    0, #Virginia
    0,
    0, #St. James
    0,
    0, #Tennessee
    0, #New York
    0,
    0, #Kentucky
    0,
    0, #Indiana
    0, #Illinois
    0,
    0, #Atlantic
    0, #Ventnor
    0,
    0, #Marvin Gardens
    0,
    0, #Pacific
    0, #North Carolina
    0,
    0, #Pennsylvania
    0,
    0,
    0, #Park Place
    0,
    0 #Boardwalk
    ]

    masterMortgageList = []

    middlePot = 500

    masterPropertiesOwnedList = []
    #Only necessary if changing starting properties, but doesn't hurt to leave uncommented
    for player in propertiesOwnedList:
            for property in player:
                masterPropertiesOwnedList.append(property)
    #######################################################


    win = GraphWin('Monopoly Simulator', 550, 550) # give title and dimensions


    # for numPlayers in range(2,11):
    #     game = Game(win,numPlayers,turnByTurn,turnSkip,playerMoneyList,propertiesOwnedList,posList,masterHousesList,masterMortgageList,middlePot,masterPropertiesOwnedList)
    #     print("numPlayers: " + str(numPlayers))
    #     game.findStrategy()
    #     print()





    game1 = Game(win,numPlayers,turnByTurn,turnSkip,playerMoneyList,propertiesOwnedList,posList,masterHousesList,masterMortgageList,middlePot,masterPropertiesOwnedList)
    game1.drawBoard()
    game1.simulateMany(1000)
    # game1.findStrategy()
    game1.displayWinLossTieRatio()

    #Displayed top row on properties
    game1.displayWinningProperties()

    #Displayed bottom row on properties - choose 1
    # game1.displayPercentLandedOn()
    # game1.displayLosingProperties()
    game1.displayLostOnProperties()


    game1.displaySpecificGame()

    win.getMouse()
    win.close()

main()

#To do:

# Don't pay rent if owner is in jail
# Fix occasional bug: File "main.py", line 625, in simulate
#     self.players.remove(p)
#     ValueError: list.remove(x): x not in list
