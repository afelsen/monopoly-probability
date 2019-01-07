from graphics import *
import random
from random import shuffle
from colour import Color

def drawBoard(win):
    for r in range(0,550,50):
        line = Line(Point(r,0),Point(r,550))
        line.draw(win)
    for c in range(0,550,50):
        line = Line(Point(0,c),Point(550,c))
        line.draw(win)
    rectangle = Rectangle(Point(50,50), Point(500,500))
    rectangle.setFill('white')
    rectangle.draw(win)

    #Text
    namesListColumn1 = ["Free_Parking","New York_Avenue","Tennessee_Avenue","Community_Chest","St. James_Place","Pennsylvania_Railroad","Virginia_Avenue","States_Avenue","Electric_Company","St. Charles_Place","In_Jail"]
    for num in range(len(namesListColumn1)):
        name = namesListColumn1[num]
        pos = name.find("_")
        labelTop = Text(Point(25,10 + num * 50), name[:pos])
        labelBottom = Text(Point(25,20 + num * 50), name[pos+1:])
        labelTop.setSize(10)
        labelBottom.setSize(10)
        labelTop.draw(win)
        labelBottom.draw(win)

    namesListColumn2 = ["Go To_Jail","Pacific_Avenue","North Carolina_Avenue","Community_Chest","Pennsylvania_Avenue","Short_Line","Chance_","Park_Place","Luxury_Tax","Boardwalk_","GO_"]
    for num in range(len(namesListColumn2)):
        name = namesListColumn2[num]
        pos = name.find("_")
        labelTop = Text(Point(525,10 + num * 50), name[:pos])
        labelBottom = Text(Point(525,20 + num * 50), name[pos+1:])
        labelTop.setSize(10)
        labelBottom.setSize(10)
        labelTop.draw(win)
        labelBottom.draw(win)


    namesListRow1 = ["Kentucky_Avenue","Chance_","Indiana_Avenue","Illinois_Avenue","B. & O._Railroad","Atlantic_Avenue","Ventnor_Avenue","Water_Works","Marvin_Gardens"]
    for num in range(1,len(namesListRow1)+1):
        name = namesListRow1[num-1]
        pos = name.find("_")
        labelTop = Text(Point(25 + num * 50,10), name[:pos])
        labelBottom = Text(Point(25 + num * 50,20), name[pos+1:])
        labelTop.setSize(10)
        labelBottom.setSize(10)
        labelTop.draw(win)
        labelBottom.draw(win)

    namesListRow2 = ["Connecticut_Avenue","Vermont_Avenue","Chance_","Oriental_Avenue","Reading_Railroad","Income_Tax","Baltic_Avenue","Community_Chest","Mediterr..._Avenue"]
    for num in range(1,len(namesListRow2)+1):
        name = namesListRow2[num-1]
        pos = name.find("_")
        labelTop = Text(Point(25 + num * 50,510), name[:pos])
        labelBottom = Text(Point(25 + num * 50,520), name[pos+1:])
        labelTop.setSize(10)
        labelBottom.setSize(10)
        labelTop.draw(win)
        labelBottom.draw(win)


    #Big Monopoly
    monopolyTitle = Text(Point(275,275),"Monopoly")
    monopolyTitle.setSize(35)
    monopolyTitle.draw(win)

def getGradientListRGB(color1,color2,length):
    red = Color(color1)
    colors = list(red.range_to(Color(color2),length))
    for i in range(len(colors)):
        colors[i] = colors[i].rgb
        newcolor = []
        for c in range(3):
            newcolor.append(int(colors[i][c]*255))
        colors[i] = (newcolor[0],newcolor[1],newcolor[2])
    return colors

def playGame(win):

    #Coordinate values of each tile on the board
    coordinateValues = []
    for br in range(10,-1,-1):
        coordinateValues.append((25 + br * 50,540))
    for lc in range(9,0,-1):
        coordinateValues.append((25, 40  + lc * 50))
    for tr in range(11):
        coordinateValues.append((25 + tr * 50, 40))
    for rc in range(1,10):
        coordinateValues.append((525, 40  + rc * 50))


    #Sets the percent landed on each space to 0
    boxValues = [0]*40
    #This is the percent landed in each space after x number of games
    ultimateBoxValues = [0]*40

    chanceCards = [0,24,11,'U','R','R',"+50","Get out of jail","Back 3","-15",5,39,"giveeach50","+150","+100","Hotel/houses"]

    communityCards = ["+100","+100","+100","-150","+10","+45","geteach50","-50",0,"Get out of jail","-100","+200","Hotel/houses","+25","+20",10]

    #Property prices
    propertyPriceList = [None,60,None,60,None,200,100,None,100,120,None,140,150,140,160,200,180,None,180,200,None,220,None,220,240,200,260,260,150,280,None,300,300,None,320,200,None,350,None,400]

    propertyHouseCost = [None,50,None,50,None,"R",50,None,50,50,None,100,"U",100,100,"R",100,None,100,100,None,150,None,150,150,"R",150,150,"U",150,None,200,200,None,200,"R",None,200,None,200]

    monopolies = [(1,3),(6,8,9),(11,13,14),(16,18,19),(21,23,24),(26,27,29),(31,32,34),(37,39)]

    #Property rent
    propertyRentList = [None,2,None,4,None,"R",6,None,6,8,None,10,"U",10,12,"R",14,None,14,16,None,18,None,18,20,"R",22,22,"U",24,None,26,26,None,28,"R",None,35,None,40]
    oneHouseRent = [None,10,None,20,None,"R",30,None,30,40,None,50,"U",50,60,"R",70,None,70,80,None,90,None,90,100,"R",110,110,"U",120,None,130,130,None,150,"R",None,175,None,200]
    twoHousesRent = [None,30,None,60,None,"R",90,None,90,100,None,150,
    "U",150,180,"R",200,None,200,220,None,250,None,250,300,"R",330,330,"U",360,None,390,390,None,450,"R",None,500,None,600]
    threeHousesRent = [None,90,None,180,None,"R",270,None,270,300,None,450,"U",450,500,"R",550,None,550,600,None,700,None,700,750,"R",800,800,"U",850,None,900,900,None,1000,"R",None,1100,None,1400]
    fourHousesRent = [None,160,None,320,None,"R",400,None,400,450,None,625,"U",625,700,"R",750,None,750,800,None,875,None,875,925,"R",975,975,"U",1025,None,1100,1100,None,1200,"R",None,1300,None,1700]
    hotelRent = [None,250,None,450,None,"R",550,None,550,600,None,750,"U",750,900,"R",950,None,950,1000,None,1050,None,1050,1100,"R",1150,1150,"U",1200,None,1275,1275,None,1400,"R",None,1500,None,2000]


    numPlayers = 3
    wins = [0]*numPlayers
    losses = [0]*numPlayers
    ties = [0]*numPlayers

    winningProperties = [0]*40
    propertyLostOn = [0]*40


    #Game is played 10000 times
    for j in range(1000):

        #Determines if you want the game to run automatically or turn by turn
        turnByTurn = False
        turnsPlayed = 0
        turnSkip = 10

        #Number of players
        players = list(range(numPlayers))

        #initalizes players and text
        colors = ["blue", "orange","purple","black"]
        playerTextPos = [(100,100),(450,100),(100,450),(450,450)]
        playerTextList = []
        playerMoneyList = []
        playerCircleList = []
        propertiesOwnedList = [[],[],[],[]]

        for p in range(numPlayers):
            playerMoneyList.append(500+200+150+80+50+30+7)
            if turnByTurn:
                playerTextList.append(Text(Point(playerTextPos[p][0],playerTextPos[p][1]),"Player" + str(p+1) + ": " + str(playerMoneyList[p])))
                playerTextList[p].setTextColor(colors[p])
                playerTextList[p].draw(win)

                playerCircleList.append(Circle(Point(525,525), 7))
                playerCircleList[p].draw(win)
                playerCircleList[p].setFill(colors[p])


        #The position of the players
        posList = []
        for p in range(numPlayers):
            posList.append(0)

        masterPropertiesOwnedList = []
        masterHousesList = [0]*40
        masterMortgageList = []

        middlePot = 500


        ###########Change Starting Values###########
        # playerMoneyList = [1017,1017,1017,1017]
        # propertiesOwnedList = [[6,8,9],[],[],[]]
        # posList = [0,0,0,0]

        # masterHousesList[*] = *
        # masterHousesList[*] = ...
        #
        # masterMortgageList[*] = *
        # masterMortgageList[*] = ...
        #
        # middlePot = *

        ###Only necessary if changing starting properties, but doesn't hurt to leave uncommented
        for player in propertiesOwnedList:
            for property in player:
                masterPropertiesOwnedList.append(property)


        #Shuffle chance cards
        chance = [i for i in chanceCards]
        shuffle(chance)

        #Shuffle community cards
        community = [i for i in communityCards]
        shuffle(community)

        won = False


        while not won:
            #Roll for each player
            for p in players:
                done = False

                while not done:

                    #Unmortgaging properties
                    for property in propertiesOwnedList[p]:
                        #First try to mortgage a property without a house
                        if property in masterMortgageList and playerMoneyList[p] > (propertyPriceList[property]//2):
                            masterMortgageList.remove(property)
                            playerMoneyList[p] -= (propertyPriceList[property]//2)

                            #drawing
                            if turnByTurn:
                                mortgageCircle = Circle(Point(coordinateValues[property][0]+17,coordinateValues[property][1] - 11),5)
                                mortgageCircle.setFill("white")
                                mortgageCircle.setOutline("white")
                                mortgageCircle.draw(win)

                    #Buying houses
                    for m in monopolies:
                        haveMonopoly = True
                        for v in m:
                            if v not in propertiesOwnedList[p]:
                                haveMonopoly = False
                        if haveMonopoly == True:
                            while playerMoneyList[p] > 200 + propertyHouseCost[v]:
                                playerMoneyList[p] -= propertyHouseCost[v]
                                if len(m) == 3:
                                    if masterHousesList[m[0]] >= 5 or masterHousesList[m[1]] >= 5 or masterHousesList[m[2]] >= 5:
                                        break

                                    if masterHousesList[m[2]] <= masterHousesList[m[1]] and masterHousesList[m[1]] <= masterHousesList[m[0]]:
                                        masterHousesList[m[2]] += 1
                                    elif masterHousesList[m[1]] <= masterHousesList[m[0]]:
                                        masterHousesList[m[1]] += 1
                                    else:
                                        masterHousesList[m[0]] += 1

                                if len(m) == 2:
                                    if masterHousesList[m[0]] >= 5 or masterHousesList[m[1]] >= 5:
                                        break

                                    if masterHousesList[m[1]] <= masterHousesList[m[0]] and masterHousesList[m[1]] < 5:
                                        masterHousesList[m[1]] += 1
                                    elif masterHousesList[m[0]] < 5:
                                        masterHousesList[m[0]] += 1

                            if turnByTurn:
                                for i in range(len(m)):
                                    housesText = Circle(Point(coordinateValues[m[i]][0]-15,coordinateValues[m[i]][1] - 10),5)
                                    housesText.setFill("white")
                                    housesText.setOutline("white")
                                    housesText.draw(win)
                                for i in range(len(m)):
                                    housesText = Text(Point(coordinateValues[m[i]][0]-20,coordinateValues[m[i]][1] - 10), "h: " + str(masterHousesList[m[i]]))
                                    housesText.setTextColor("green")
                                    housesText.draw(win)

                    die1 = random.randrange(1,7)
                    die2 = random.randrange(1,7)

                    if die1 != die2:
                        done = True
                    posList[p] += die1 + die2

                    #If you get snake eyes
                    if die1 == 1 and die2 == 1:
                        playerMoneyList[p] += 100

                    #If you pass go
                    if posList[p] >= 40:
                        posList[p] -= 40
                        playerMoneyList[p] += 200

                    #If you land on "Go to jail", go to jail
                    if posList[p] == 30:
                        posList[p] = 10

                    #If you land on "Free Parking", get the pot
                    if posList[p] == 20:
                        playerMoneyList[p] += middlePot
                        middlePot = 500

                    #If you land on "chance"
                    if posList[p] == 7 or posList[p] == 22 or posList[p] == 36:
                        if len(chance) == 0:
                            chance = [i for i in chanceCards]
                            shuffle(chance)
                        if isinstance(chance[0],int):
                            posList[p] = chance[0]
                        elif chance[0] == 'U':
                            if posList[p] > 11:
                                posList[p] = 28
                            else:
                                posList[p] = 12
                        elif chance[0] == 'R':
                            if posList[p] < 5 or posList[p] >= 35:
                                posList[p] = 5
                            elif posList[p] < 15:
                                posList[p] = 15
                            elif posList[p] < 25:
                                posList[p] = 25
                            else:
                                posList[p] = 35
                        elif chance[0] == "Back 3":
                            posList[p] -= 3

                        #Money chance cards
                        elif chance[0][0] == "+":
                            playerMoneyList[p] += int(chance[0][1:])
                        elif chance[0][0] == "-":
                            playerMoneyList[p] -= int(chance[0][1:])
                            middlePot += int(chance[0][1:])

                        #Other cards
                        elif chance[0] == "giveeach50":
                            for player in players:
                                playerMoneyList[p] -= 50
                                playerMoneyList[player] += 50
                        elif chance[0] == "Get out of jail":
                            pass
                        elif chance[0] == "Hotel/houses":
                            pass

                        #Only run this if you want to simulate each turn at a time
                        if turnByTurn:
                            chanceText = Text(Point(275,400), "Chance: " + str(chance[0]))
                            chanceText.setSize(20)
                            chanceText.draw(win)
                            if turnsPlayed % turnSkip == 0:
                                win.getMouse()
                            chanceText.setTextColor("white")
                        chance.pop(0)


                    if posList[p] == 40:
                        playerMoneyList[p] += 200

                    if posList[p] == 2 or posList[p] == 17 or posList[p] == 33:
                        if len(community) == 0:
                            community = [i for i in communityCards]
                            shuffle(community)
                        if isinstance(community[0],int):
                            posList[p] = community[0]

                        #Money cards
                        elif community[0][0] == "+":
                            playerMoneyList[p] += int(community[0][1:])
                        elif community[0][0] == "-":
                            playerMoneyList[p] -= int(community[0][1:])
                            middlePot += int(community[0][1:])

                        #Other cards
                        elif community[0] == "geteach50":
                            for player in players:
                                playerMoneyList[p] += 50
                                playerMoneyList[player] -= 50
                        elif community[0] == "Get out of jail":
                            pass
                        elif community[0] == "Hotel/houses":
                            pass

                        #Only run this if you want to simulate each turn at a time
                        if turnByTurn:
                            communityText = Text(Point(275,400), "Community Chest: " + str(community[0]))
                            communityText.setSize(20)
                            communityText.draw(win)
                            if turnsPlayed % turnSkip == 0:
                                win.getMouse()
                            communityText.setTextColor("white")


                        community.pop(0)


                    #If the player lands on a owned property (not mortgaged) - RENT
                    if posList[p] in masterPropertiesOwnedList and posList[p] not in propertiesOwnedList[p] and posList[p] not in masterMortgageList:
                        for player in range(len(propertiesOwnedList)):
                            if posList[p] in propertiesOwnedList[player]:
                                if isinstance(propertyRentList[posList[p]],int):
                                    if masterHousesList[posList[p]] == 0:
                                        playerMoneyList[p] -= propertyRentList[posList[p]]
                                        playerMoneyList[player] += propertyRentList[posList[p]]
                                    elif masterHousesList[posList[p]] == 1:
                                        playerMoneyList[p] -= oneHouseRent[posList[p]]
                                        playerMoneyList[player] += oneHouseRent[posList[p]]
                                    elif masterHousesList[posList[p]] == 2:
                                        playerMoneyList[p] -= twoHousesRent[posList[p]]
                                        playerMoneyList[player] += twoHousesRent[posList[p]]

                                    elif masterHousesList[posList[p]] == 3:
                                        playerMoneyList[p] -= threeHousesRent[posList[p]]
                                        playerMoneyList[player] += threeHousesRent[posList[p]]

                                    elif masterHousesList[posList[p]] == 4:
                                        playerMoneyList[p] -= fourHousesRent[posList[p]]
                                        playerMoneyList[player] += fourHousesRent[posList[p]]

                                    elif masterHousesList[posList[p]] == 5:
                                        playerMoneyList[p] -= hotelRent[posList[p]]
                                        playerMoneyList[player] += hotelRent[posList[p]]

                                #If it's a railroad
                                elif propertyRentList[posList[p]] == "R":
                                    multiplier = .5
                                    if 5 in propertiesOwnedList[player]:
                                        multiplier *= 2
                                    if 15 in propertiesOwnedList[player]:
                                        multiplier *= 2
                                    if 25 in propertiesOwnedList[player]:
                                        multiplier *= 2
                                    if 35 in propertiesOwnedList[player]:
                                        multiplier *= 2
                                    multiplier = int(multiplier)
                                    playerMoneyList[p] -= 25*multiplier
                                    playerMoneyList[player] += 25*multiplier
                                #If it's a utility
                                elif propertyRentList[posList[p]] == "U":
                                    playerMoneyList[p] -= (die1+die2)*10
                                    playerMoneyList[player] += (die1+die2)*10


                    #Landing on squares that make you pay taxes
                    if posList[p] == 4:
                        if playerMoneyList[p] >= 2000:
                            playerMoneyList[p] -= 200
                            middlePot += 200
                        else:
                            playerMoneyList[p] -= (playerMoneyList[p]//10)
                            middlePot += (playerMoneyList[p]//10)
                    if posList[p] == 38:
                        playerMoneyList[p] -= 75
                        middlePot += 75

                    #If you have zero or negative money after paying rent/taxes
                    if playerMoneyList[p] <= 0:
                        for i in [True,False]: #On the first iteration only sell no houses, on the second iteration sell anything
                            for property in propertiesOwnedList[p]:
                                #First try to mortgage a property without a house
                                if property not in masterMortgageList and masterHousesList[property] == 0 and i:
                                    masterMortgageList.append(property)
                                    playerMoneyList[p] += (propertyPriceList[property]//2)
                                #Second, sell anything
                                elif property not in masterMortgageList and not i:
                                    masterMortgageList.append(property)
                                    playerMoneyList[p] += (propertyPriceList[property]//2)

                                #If nothing happened, break out of the loop
                                else:
                                    continue

                                #Printing it out
                                if turnByTurn:

                                    mortgageText = Text(Point(coordinateValues[property][0]+17,coordinateValues[property][1] - 10), "M")
                                    mortgageText.setTextColor("Red")
                                    mortgageText.draw(win)

                                #If the player has more than zero dollars, break out of the loop
                                if playerMoneyList[p] > 0:
                                    break
                            if playerMoneyList[p] > 0:
                                break

                    #if the player still has zero or less money even after mortgaging, the player loses
                    if playerMoneyList[p] <= 0:
                        #Remove properties from master lists
                        for property in propertiesOwnedList[p]:

                            #drawing

                            if turnByTurn:
                                #mortgage
                                if property in masterMortgageList:
                                    mortgageCircle = Circle(Point(coordinateValues[property][0]+17,coordinateValues[property][1] - 11),6)
                                    mortgageCircle.setFill("white")
                                    mortgageCircle.setOutline("white")
                                    mortgageCircle.draw(win)

                                #Properties Owned
                                propertyCircle = Circle(Point(coordinateValues[property][0],coordinateValues[property][1] - 10), 6)
                                propertyCircle.setFill("white")
                                propertyCircle.setOutline("white")
                                propertyCircle.draw(win)

                                #Houses
                                housesText = Circle(Point(coordinateValues[property][0]-15,coordinateValues[property][1] - 10),6)
                                housesText.setFill("white")
                                housesText.setOutline("white")
                                housesText.draw(win)
                        #erasing player
                        if turnByTurn:
                            #Player
                            playerCircleList[p].setOutline("white")
                            playerCircleList[p].setFill("white")


                        if property in masterMortgageList:
                            masterMortgageList.remove(property)
                        if property in masterPropertiesOwnedList:
                            masterPropertiesOwnedList.remove(property)
                        masterHousesList[property] = 0
                        losses[p] += 1
                        propertyLostOn[posList[p]] += 1
                        players.remove(p)
                        done = True

                    #If there is only one player left
                    if len(players) == 1:
                        won = True
                        done = True
                        for player in players:
                            wins[player] += 1
                            #Adding up properties owned
                            for property in propertiesOwnedList[player]:
                                winningProperties[property] += 1

                    elif turnsPlayed > 1000:
                        won = True
                        done = True
                        for player in players:
                            ties[player] += 1

                    #If the player lands on an unowned property
                    if isinstance(propertyPriceList[posList[p]],int) and (posList[p] not in masterPropertiesOwnedList):
                        #If the player can afford it
                        if propertyPriceList[posList[p]] < playerMoneyList[p]:
                            masterPropertiesOwnedList.append(posList[p])
                            propertiesOwnedList[p].append(posList[p])
                            playerMoneyList[p] -= propertyPriceList[posList[p]]

                            if turnByTurn:
                                propertyText = Text(Point(coordinateValues[posList[p]][0],coordinateValues[posList[p]][1] - 10), p+1)
                                propertyText.setTextColor(colors[p])
                                propertyText.draw(win)



                    #Only run this if you want to simulate each turn at a time
                    if turnByTurn:
                        playerCircleList[p].setOutline("white")
                        playerCircleList[p].setFill("white")
                        playerTextList[p].setTextColor("white")

                        playerCircleList[p] = Circle(Point(coordinateValues[posList[p]][0],coordinateValues[posList[p]][1]), 6)
                        playerCircleList[p].draw(win)
                        playerCircleList[p].setFill(colors[p])


                        playerTextList[p] = Text(Point(playerTextPos[p][0],playerTextPos[p][1]),"Player" + str(p+1) + ": " + str(playerMoneyList[p]))
                        playerTextList[p].setTextColor(colors[p])
                        playerTextList[p].draw(win)
                        print(str(p+1) + ": " + str(playerMoneyList[p]))


                        rollText = Text(Point(275,200), "Roll: " + str(die1) + " + " + str(die2) + " = " + str(die1+die2))

                        rollText.setSize(25)
                        rollText.draw(win)
                        if turnsPlayed % turnSkip == 0:
                            win.getMouse()
                        rollText.setTextColor("white")

                turnsPlayed += 1
                boxValues[posList[p]] += 1



        for v in range(len(boxValues)):
            boxValues[v] = (boxValues[v]/turnsPlayed)
            ultimateBoxValues[v] += boxValues[v]

        #Making sure it adds up to 100
        # accum = 0
        # for value in boxValues:
        #     accum += value
        # print(accum)

    nonProperties = [0,2,4,7,10,17,20,22,30,33,36,38]

###Percent landed on each square
    # for v in range(len(ultimateBoxValues)):
    #     ultimateBoxValues[v] = round(ultimateBoxValues[v]/(j+1)*100,3)
    # print(ultimateBoxValues)
    #
    #
    # #Sort the percentages in a list - used for color coding
    # sortedValues = ultimateBoxValues.copy()
    # for i in range(len(nonProperties)):
    #     sortedValues.pop(nonProperties[i]-i)
    # sortedValues.sort()
    # print(sortedValues)
    #
    # #Draw on the board color coded
    # gradient = getGradientListRGB("red","green",28)
    #
    # for i in range(len(ultimateBoxValues)):
    #     if i not in nonProperties:
    #         percent = Text(Point(coordinateValues[i][0],coordinateValues[i][1]), ultimateBoxValues[i])
    #         v = sortedValues.index(ultimateBoxValues[i])
    #         textcolor = color_rgb(gradient[v][0],gradient[v][1],gradient[v][2])
    #         percent.setTextColor(textcolor)
    #         percent.draw(win)

###Wins,Loss,Tie Ratio by player
    for i in range(len(wins)):
        wins[i] = wins[i]/(j+1)

    for i in range(len(losses)):
        losses[i] = losses[i]/(j+1)

    for i in range(len(ties)):
        ties[i] = ties[i]/(j+1)

    print(wins)
    print(losses)
    print(ties)


### Properties that the winners owned

    for p in range(len(winningProperties)):
        winningProperties[p] = winningProperties[p]/(j+1)


    #Sort the percentages in a list - used for color coding
    sortedValues = winningProperties.copy()
    sortedValues.sort()
    sortedValues = sortedValues[12:]

    #Draw on the board color coded
    gradient = getGradientListRGB("red","green",28)

    for i in range(len(winningProperties)):
        if i not in nonProperties:
            percent = Text(Point(coordinateValues[i][0],coordinateValues[i][1]-10), winningProperties[i])
            v = sortedValues.index(winningProperties[i])
            textcolor = color_rgb(gradient[v][0],gradient[v][1],gradient[v][2])
            percent.setTextColor(textcolor)
            percent.draw(win)
            print(winningProperties[i])

### Properties lost on
    for p in range(len(propertyLostOn)):
        propertyLostOn[p] = propertyLostOn[p]/(j+1)

    print (propertyLostOn)

    #Sort the percentages in a list - used for color coding
    sortedValues = propertyLostOn.copy()
    for i in range(len(nonProperties)):
        sortedValues.pop(nonProperties[i]-i)
    sortedValues.sort()

    #Draw on the board color coded
    gradient = getGradientListRGB("red","green",28)

    for i in range(len(propertyLostOn)):
        if i not in nonProperties:
            percent = Text(Point(coordinateValues[i][0],coordinateValues[i][1]), propertyLostOn[i])
            v = sortedValues.index(propertyLostOn[i])
            textcolor = color_rgb(gradient[v][0],gradient[v][1],gradient[v][2])
            percent.setTextColor(textcolor)
            percent.draw(win)
            print(propertyLostOn[i])


def main():
    win = GraphWin('Face', 550, 550) # give title and dimensions
    drawBoard(win)

    playGame(win)



    win.getMouse()
    win.close()

main()
