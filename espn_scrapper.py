
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import statistics
import unicodedata


def scraper(webAddress):
    '''
    this function opens up a specified url from basketball-reference.com,
    and scrapes the data using BeautifulSoup
    
    returns: a panda dataframe
    '''
    
    year = 2021                                         # the NBA season we will be analyzing

    html = urlopen(webAddress.format(year))             # the webAddress we will be scraping 
    soup = BeautifulSoup(html)                          # returns a BeautifulSoup object
    soup.findAll('tr', limit=2)                         # use findALL() to get the column headers
                                                        # getText()to extract the text we need into a list

    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    headers = headers[1:]                               # exclude the first column, we don't need it
    rows = soup.findAll('tr')[1:]                       # exclude the first header row

    player_stats = [[td.getText() for td in rows[i].findAll('td')]
        for i in range(len(rows))]

    return pd.DataFrame(player_stats, columns = headers)

class Player(object):
    '''
    Player instance
    
    holds all data associated with that player, and some functions
    that perform operations on that specific player
    '''
    def __init__(self, player, pos, tm, g, mp, fg, three, ftp, ast, stl, blk, tov, trb, pts):
        self.player = player
        self.position = pos
        self.team = tm
        self.games = g
        self.minutes_game = mp
        self.field_goals = fg
        self.three_pointer = three
        self.ft_percentage = ftp
        self.assist = ast
        self.steals = stl
        self.blocks = blk
        self.turnovers = tov
        self.points = pts
        self.rebounds = trb
        self.doubles = 0
        self.team_wins = None
        self.rankings = []
        self.total_rank = None
        
    def getPlayer_object(self):
        return self
    def getPlayer(self):
        return self.player
    def getPosition(self):
        return self.position
    def getTeam(self):
        return self.team
    def getGames(self):
        return self.games
    def getField_goals(self):
        return self.field_goals
    def getThree_pointer(self):
        return self.three_pointer
    def getFreethrow_per(self):
        return self.ft_percentage
    def getAssist(self):
        return self.assist
    def getSteals(self):
        return self.steals
    def getBlocks(self):
        return self.blocks
    def getTurnovers(self):
        return self.turnovers
    def getRebounds(self):
        return self.rebounds
    def getPoints(self):
        return self.points
    def getDoubles(self):
        return self.doubles
    def getTeam_wins(self):
        return self.team_wins
    def getRankings(self):
        return self.rankings
    def getTotalRank(self):
        return self.total_rank

    def count_positions(self):
        return len(position)    
    def returnPoints(self):
        return [
            self.field_goals, self.three_pointer, self.ft_percentage, self.assist,
            self.steals, self.blocks, self.turnovers, self.points, self.rebounds,
            self.doubles, self.team_wins
            ]
    def convertPoints(self):
        # need to implement ,self.team_wins
        convertThese_Points = [
            self.field_goals, self.three_pointer, self.assist,
            self.steals, self.blocks, self.turnovers, self.points, self.rebounds,
            self.doubles
            ]

        for category in convertThese_Points:
           
            if not category == None:
                print(self.player, 'we be changing')
                print(category)
                games = self.getGames()
                print('      games', games)
                TotalPoints = category * games
                category = TotalPoints
                print('      Success!!! for category change or not?', category)
            else:
                # for the wierd case that a data entry's value is None:
                category = 0


    
    def updateRank(self, index, value):
        aList = self.getRankings()
        aList.insert(index, value)
        
    def meanElementRank(self):
        aList = []
        N = len(self.getRankings())
        
        for stat in self.getRankings():
            probability = stat / N
            aList.append(probability)
            
        self.total_rank = round(sum(aList), 4)
            

    def dataList(self, keyFunction_list):
        '''
        dataList is used in removeDuplicates(),
        and takes in a list of functions/getters.
        
        
        returns: a list of the data the getters obtained
        '''
        aList = []
        for function in keyFunction_list:
            data_point = function(self)
            aList.append(data_point)
        
        return aList
            
    def make_dict_entry(self):
        '''
        make_dict_entry() is used by addPlayer() in AllPlayersData.
        When a new Player is added, this function assembles simple assembles
        their data points into list form.
        '''
        
        return self, [
            self.position, self.team, self.games, self.minutes_game, self.field_goals,
            self.three_pointer, self.ft_percentage, self.assist, self.steals, self.blocks,
            self.turnovers, self.points, self.rebounds
            ]
    
    def __str__(self):
        a = ( self.player + ': ' + ' POS:' + str(self.position) + ' GAMES:' + str(self.games) + 
            ' FG:' + str(self.field_goals) + ' 3P:' + str(self.three_pointer) +
            ' FT%:' + str(self.ft_percentage) + ' ASS:' + str(self.assist) +
            ' STLs:' + str(self.steals) + ' BLKS:' + str(self.blocks) + 
            ' TOV:' + str(self.turnovers) + ' TRB: ' + str(self.rebounds) +
            ' PTS:' + str(self.points) + ' DBLS:' + str(self.doubles) +
            ' TW-> ' +  str(self.team_wins) + ' RANK-> ' +  str(self.total_rank)
        )  
        return a


class AllPlayersData():
    '''
    AllPlayerData is a dictionary. It holds every player in the NBA and their stats
    
    key: Player object, representing the
    value: a list, of data entries
    '''
    
    def __init__(self):
        self.playerDict = {}
    
    def getDict(self):
        return self.playerDict
    def getSelf(self):
        return self

    def getPlayer_object(self, aString):
        ''' use the player's string name to his Player object'''

        for key in self.playerDict.keys():
            
            if key.getPlayer() == aString:
                return key
            else:
#                 print('aStrin:', aString, 'is not in the dictionary')
                pass

    def searchPlayer(self, aString):
        '''
        searchPlayer searches the keys in the dictionary to see if the
        search name (aString) is present
        
        returns: true if aString is in the dictionary
        '''
        for key in self.getDict():
            get_string = key.getPlayer()
            if aString ==  get_string:
                return True
        return False

    def convertPoints(self):
        for key in self.getDict():
            print(key)
            key.convertPoints()
            print(key)
                  
    def countPlayers(self):
        ''' counts every player in the AllPlayersData base'''
        
        counter = 0 
        for key in self.playerDict:
            counter += 1
        return counter
    
    def addPlayer(self, player):
        ''' first, this will check to see if player already exists in
        the AllPlayer dictionary. If it doesn't already exist, add'''
        
        key, value = player.make_dict_entry()
        if key in self.getDict():
            print('\t', 'duplicate values coming from addPlayer()')
        else:
            self.playerDict[key] = value
            
    def removePlayer(self, player):
        del self.getDict()[player]

    def normalizeText(text):
        '''
        this scraping programs scrape from multiple sources. Each source formats their text
        differently. 'TJ' vs 'T.J.' for example. This code strips down or 'normalizes' the
        formatting of incoming text, so less problems rise when interacting with the main database '''

        try:
            text = unicode(text, 'utf-8')
        except NameError:
            pass

        text = str(unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8"))
        text = text.lower()
        text = text.replace('.', '')
        text = text.replace(' iii', '')

        # these are specific entries found to be problematic so far:
        text = text.replace('otto porter jr', 'otto porter')
        text = text.replace('marcus morris sr', 'marcus morris')
        text = text.replace('lonnie walker iv', 'lonnie walker')
        text = text.replace('danuel house jr', 'danuel house')
        text = text.replace('kevin knox ii', 'kevin knox')

        return str(text) 

    def removeDuplicates(self):
        '''
        often, duplicate player entries exist. this happens when players are traded. And
        multiple player-team entries exist. removeDuplicates(), seeks out these duplicates, 
        combines the data, calculates the new average and updates the dictionary
        
        returns: nothing, but updates the dictionary
        '''
        # remove duplicate names and combine their stats
        duplicate = []
        duplicate_objects = []
        duplicate_tracker = []
        aDict_main = {}
        
        ## re-create the dictionary, making sure there is only one athlete entry (the mid-season trade problem)
        for key, value in self.getDict().items():
            # catch any duplicat player entries
            if key.getPlayer() in duplicate:
                # save the dictionary key (Player object) to dupicate_objects
                duplicate_objects.append(key)
                if key.getPlayer() not in duplicate_tracker:
                    duplicate_tracker.append(key.getPlayer())
            else:
                # create/add to the dictionary - all duplicates should be caught already
                aDict_main[key] = value
                # add Player string-name to the duplicate list so you can catch future duplicates
                duplicate.append(key.getPlayer())
        
        ## a new Dictionary is now created with no duplicated entries. We now iterate over the duplicate entries
        ## and make sure to add this data to the Player
        for player_string in duplicate_tracker:
            
            # get player info/object that already exists in the dict
            player_object = self.getPlayer_object(player_string)
            
            # convert data into list form
            multiple_lists = []
            
            keyFunction_list = [
                Player.getField_goals, Player.getThree_pointer,
                Player.getFreethrow_per, Player.getAssist, Player.getSteals,
                Player.getBlocks, Player.getTurnovers, Player.getRebounds,
                Player.getPoints
                ]

            
            data_list = player_object.dataList(keyFunction_list)
            
            multiple_lists.append(data_list)
            
            # go through all the duplicate objects, we want to match/find player_string!
            for player_object_ in duplicate_objects:
                if player_string == player_object_.getPlayer():
                    
                    # convert this object into list form and add it to aList
                    temp_list = player_object_.dataList(keyFunction_list)
                    multiple_lists.append(temp_list)
                    
            # calcualte the averages of the duplicate values and add this value to the new dictionary
            result = [statistics.mean(k) for k in zip(*multiple_lists)]
            aDict_main[player_object] = result
        
        # update the objects dictionary
        self.playerDict = aDict_main

    def sortPlayers(self, keyFunction):
        player_objects = []
        
        # make a copy of the dictionary
        for key in self.getDict().keys():
            player_objects.append(key)
        
        sorted_copy = sorted(player_objects, key = keyFunction, reverse = True)
            
        return sorted_copy

    def printSortedPlayers(self, keyFunction):
        '''
        this function will sort all the players  in the league 
        according to the keyFunction you provide it
        
        returns: a list sorted in descending order'''
        sorted_list = self.sortPlayers(keyFunction)
        for i in sorted_list:
            print(i)
    
    def sort_all_categories(self):
        '''
        makes 9 sorted lists
        sorts according to the keyFunctions
        '''
        keyFunction_list = [
            Player.getField_goals, Player.getThree_pointer,
            Player.getFreethrow_per, Player.getAssist, Player.getSteals, 
            Player.getBlocks, Player.getTurnovers, Player.getRebounds,
            Player.getPoints
            ]
        master_list = []

        for keyFunction in keyFunction_list:
            sorted_list = self.sortPlayers(keyFunction)
            # -- > remove duplicates (havn't solved why their are duplicates yet
            aList = []
            temp = []
            for i in sorted_list:
                if i.player in aList:
                    pass
                else:
                    aList.append(i.player)
                    temp.append(i)

            if keyFunction == Player.getTurnovers:
                temp.reverse()
            master_list.append(temp)

            print('\n', keyFunction, '\n')
            for item in temp:
                print(item)
                
        return master_list
    
    def rank_every_player_category(self):
        '''
        makes 9 sorted lists
        sorts according to the keyFunctions
        '''

        ## i need to still include cp.Player.getTeam_wins!
        keyFunction_list = [
            Player.getField_goals, Player.getThree_pointer,
            Player.getFreethrow_per, Player.getAssist, Player.getSteals, 
            Player.getBlocks, Player.getTurnovers, Player.getRebounds,
            Player.getPoints, Player.getDoubles
            ]
        master_list = []
        
        for keyFunction in keyFunction_list:
            sorted_list = self.sortPlayers(keyFunction)
            # -- > remove duplicates (havn't solved why their are duplicates yet
            aList = []
            temp = []
            for i in sorted_list:
                if i.player in aList:
                    pass
                else:
                    aList.append(i.player)
                    temp.append(i)

            if keyFunction == Player.getTurnovers:
                temp.reverse()
            master_list.append(temp)
           
        return master_list
    
    def sortDoubles(self):
        '''update in the future: this function should evetually be included with the other sortFunctions'''
        keyFunction = Player.getDoubles
        sorted_list = self.sortPlayers(keyFunction)
        
        return sorted_list

    def doublesPerGame(self):
        '''this converts the double doule season total to a per game average'''
        for player in self.getDict():
            if player.doubles > 0:
                player.doubles = round((player.doubles / player.games), 4)
                
        
    def updateRankings(self):
        '''this is a wrapper like function, that deploys:

        - sort_all_categories() thus rank ordering every player stat relative to the league
        - sortDoubles(), and assigns a poor ranking to players that record zero double doubles
        '''
        
        master_list = self.sort_all_categories()
        
        # master_list includes everything BUT a sorted double double list
        for i in range(len(master_list)):
            
            # iterate over the sorted players and update rankings
            for player_rank in range(len(master_list[i])):
                
                # grab the player_object via ith elements
                player_object = master_list[i][player_rank]
                # change the ith value in self.rankings 
                player_object.updateRank(i, player_rank)
        
        # sort double doubles and add the values to self.rankings
        player_object_list = self.sortDoubles()

        for i in range(len(player_object_list)):
            if player_object_list[i].getDoubles() == 0:
                player_object_list[i].rankings.append(self.countPlayers())
            else:
                player_object_list[i].rankings.append(i)

    def openDoubleDouble(self, fileName):
        '''double double data was cut and pasted from a website and cleaned in xcel.
        it was then saved as a csv to be later used in this function

        this function opens said csv file, and returns a list containing player paird
        with their double double stat
        '''

        # Open fileName in a Try block to catch any errors  
        try:
            openFile = open(fileName, 'r')
        except:
            print('A File Related Error Occured')
        else:
            master_list = []
            for line in openFile:

                ## make a list, using split (',') to separate elements
                aList = line.split(',')
                ## get rid of trailling spaces and line breaks
                aList = [aList[0].strip(), aList[1].strip()]
                
                # the first index will be the player name. Normalize this string so we can search for things later!
                playerName_string = aList[0]
                normalize = AllPlayersData.normalizeText(playerName_string)
                aList.insert(0, normalize)  

                if self.getPlayer_object(aList[0]) not in self.getDict():
                    print('oh shit dog:', aList[0])
                
                master_list.append(aList)
            return master_list
                
        # Finally Statement, always close fileName          
        finally:
            openFile.close()
        
    def addDoubleDoubles(self, fileName):
        '''openDoubeDouble and only add double doule data to the player object
        if he achieves 1 or more double doubles'''
        
        master_list = self.openDoubleDouble(fileName)
        exceptions_handled = []
        for item in master_list:

            name = item[0]
            data = float(item[2])
            
            if data >= 1.0:
                # find player object in the dictoinary

                try:
                    player_object = self.getPlayer_object(name)
                    # update double double data
                    player_object.doubles = data
                except:
                    exceptions_handled.append(name)

        print('')
        print('##### DOUBLE DOUBLE EXCEPTIONS')
        print(exceptions_handled)

    def rankPlayers(self, print=False):
        
        # grab every player_object, and save it to a list so it can be easily sorted
        for player_object in self.getDict().keys():
            player_object.meanElementRank()
            
        # sort list according to keyFunction
        keyFunction = Player.getTotalRank
        sorted_list = self.sortPlayers(keyFunction)
        sorted_list.reverse()
        
        if print:
            for item in sorted_list:
                print(item)
                print('---------------------- rank list:', item.getRankings())

class run():
    def __init__(self):
        self.object_list = []
        
    def getSeasonList(self):
        return self.object_list
    
  
    def runMain(self, url, fileName):
        '''
        1 - runs the scraper which returns a panda containing the needed NBA data

        2 - iterate over that panda, and extract the needed data

        3 - creates a AllPlayerData object

        4 - add Player objects to the AllPlayerData object

        5 - manually add players that don't exist in the scraped database

        6 - check for object name duplicates (when players change teams), add the values to the original object

        7 - rank orders every players stat with respect to the population length

        takes in:
        - url: from basketball-reference.com, to be scraped
        - fileName: csv file containing double double data

        returns:
        - AllPlayersData object --> a clean dictionary
        containing Player Objects as keys and their data as values
        
        '''
        
        ## -- run the scraper -- ##
        stats = scraper(url)                                         # returns a panda dataframe
        handled_exceptions = []                                      # store exceptions that may happen
        
        a = AllPlayersData()                                         # create empty AllPlayersData object        
        for index, row in stats.iterrows():                          # iterate over the panda
            try:
                player_name = row["Player"]
                if not player_name == None:
                    normalizedName = AllPlayersData.normalizeText(player_name)
                    #print('     TEST - normalizedName -', normalizedName)
                
                    pos = row["Pos"]
                    tm = row["Tm"]
                    g = float(row["G"])
                    mp = float(row["MP"])
                    ftp = float(row["FT%"])

                    fg = round(float(row["FG"]) * g, 4)
                    three = round(float(row["3P"]) * g, 4)
                    ast = round(float(row["AST"]) * g, 4)
                    stl = round(float(row["STL"]) * g, 4)
                    blk = round(float(row["BLK"]) * g, 4)
                    tov = round(float(row["TOV"]) * g, 4)
                    trb = round(float(row["TRB"]) * g, 4)
                    pts = round(float(row["PTS"]) * g, 4)
                    
                    player_object = Player(normalizedName,
                                              pos, tm, g,
                                              mp, fg, three,
                                              ftp, ast, stl,
                                              blk, tov, trb,
                                              pts
                                              )
                
##                player_name = row["Player"]                          # build dict with normalized text
##                normalizedName = AllPlayersData.normalizeText(player_name)
##
##                player_object = Player(normalizedName, row["Pos"], row["Tm"], float(row["G"]), 
##                       float(row["MP"]), float(row["FG%"]), float(row["3P"]), float(row["AST"]), 
##                       float(row["STL"]), float(row["BLK"]), float(row["TOV"]), float(row["TRB"]), float(row["PTS"]))

                a.addPlayer(player_object)

            except Exception as error:
                handled_exceptions.append(player_name)
                
                print('     - Warning - addPlayer() did not work', player_name)
                print('     - Error', error)
                #print('     - is it in AllPlayersData?', a.searchPlayer(a.getPlayer_object(player_object)))
                #print('     - player_object not added -', row)

        a.removeDuplicates()                                         # remove duplicates that may happen
        print('**** removeDuplicates() complete')
        a.addDoubleDoubles(fileName)                                 # add double double data
        print('**** addDoubleDoubles() complete')                                 # add double double data

##        normalizedName = AllPlayersData.normalizeText('kevin durant')      # manually add kevin durant
##        player_object = Player(normalizedName, 'SF', "GSW", float("78"), 
##                       float("34.6"), float(".521"), float("1.8"), float("5.9"), 
##                       float("0.7"), float("1.1"), float("2.9"), float("6.4"), float("26.0"))
##        a.addPlayer(player_object)
##        player_object.doubles = 16
##        
##        
##        normalizedName = AllPlayersData.normalizeText('john wall')         # manually add John Wall
##
##        player_object2 = Player(normalizedName, 'PG', 'WAS', float('32'), 
##               float('34.5'), float('.444'), float('1.6'), float('8.7'), 
##               float('1.5'), float('0.9'), float('3.8'), float('3.6'), float('20.7'))
##        a.addPlayer(player_object2)
##        player_object2.doubles = 19
##
##        normalizedName = AllPlayersData.normalizeText('demarcus cousins')  # manually add demarcus cousins
##
##
##        player_object3 = Player(normalizedName, 'C', 'GSW', float('30'), 
##               float('25.7'), float('.480'), float('0.9'), float('3.6'), 
##               float('1.3'), float('1.5'), float('2.4'), float('8.2'), float('18'))
##        a.addPlayer(player_object3)
##        player_object3.doubles = 35
##
##        rookie_list = ['james wiseman', 'anthony edwards', 'obi toppin', 'lamelo ball']
##        for rookie in rookie_list:
##
##            normalizedName = AllPlayersData.normalizeText(rookie)    # manually add rookies
##            player_object = Player(normalizedName, 'SF', "GSW", float("65"), 
##                           float("22"), float(".46"), float("0.2"), float("3.9"), 
##                           float("0.5"), float(".3"), float("1.6"), float("4.5"), float("7.0"))
##            a.addPlayer(player_object)
##            player_object.doubles = 0

        #a.doublesPerGame()
        a.updateRankings()                                           # rank order every stat for every player
        a.rankPlayers()                                              # calcualte and store total rank for player
        

        # player, pos, tm, g, mp, fg, three, ast, stl, blk, tov, trb, pts
        
        print('Finished Loading AllPlayerData()')
        
        return a                                                     # return an AllPlayersData() object
    
    def runMulti(self):
        
        url1 = "https://www.basketball-reference.com/leagues/NBA_2020_per_game.html"
        url2 = "https://www.basketball-reference.com/leagues/NBA_2019_per_game.html"
        url3 = "https://www.basketball-reference.com/leagues/NBA_2018_per_game.html"

        fileName1 = 'NBA Double Doubles 2019 to 2020.csv'
        fileName2 = 'NBA Double Doubles 2018 to 2019.csv'
        fileName3 = 'NBA Double Doubles 2017 to 2018.csv'
            
        run2020 = self.runMain(url1, fileName1)
        run2019 = self.runMain(url2, fileName2)
        run2018 = self.runMain(url3, fileName3)
        
        self.object_list.append(run2020)
        self.object_list.append(run2019)
        self.object_list.append(run2018)

def loadData():

    url0 = "https://www.basketball-reference.com/leagues/NBA_2021_per_game.html"
    url1 = "https://www.basketball-reference.com/leagues/NBA_2020_per_game.html"
    url2 = "https://www.basketball-reference.com/leagues/NBA_2019_per_game.html"
    url3 = "https://www.basketball-reference.com/leagues/NBA_2018_per_game.html"

   
    fileName0 = 'NBA Double Doubles 2020 to 2021.csv'
    fileName1 = 'NBA Double Doubles 2019 to 2020.csv'
    fileName2 = 'NBA Double Doubles 2018 to 2019.csv'
    fileName3 = 'NBA Double Doubles 2017 to 2018.csv'
    
    Object = run()                                                  # create empty run object
    
    return Object.runMain(url0, fileName0)                          # returns an AllPlayersData() object
    
    
