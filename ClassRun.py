
import basketballReference
import ClassPlayer as cp
import ClassAllPlayersData as capd


class run():
    def __init__(self):
        self.object_list = []
        
    def getSeasonList(self):
        return self.object_list
    
  
    def runMain(self, url, fileName):
        '''
        1 - runs the scraper which returns a panda containing the needed NBA data

        2 - iterate over that panda, and extract the needed data

        3 - create an AllPlayerData object, which is an empty dictionary

        4 - add Player objects as keys to the AllPlayerData object

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
        stats = basketballReference.scraper(url)                     # returns a panda dataframe
        handled_exceptions = []                                      # store exceptions that may happen
        

# 1 - make so it passes a list of strings. self.modularize
# 2 - go into allplays data and make sure its there
# 3 - modularize code below

        a = capd.AllPlayersData()                                    # create empty AllPlayersData object        
        # a = capd.AllPlayersData(categories)
        for index, row in stats.iterrows():                          # iterate over the panda
            try:
                #print('TRy')
                player_name = row["Player"]                          # build dict with normalized text
                #print('-----', player_name)
                #print('     ----- ROW:', row)
                if not player_name == None:
                    normalizedName = capd.AllPlayersData.normalizeText(player_name)
                    
                    #print('TEST - normalizedName -', normalizedName)
                    #print('row', row)

                    aDict = {}

                    aDict['pos'] = row["Pos"]
                    aDict['tm'] = row["Tm"]
                    aDict['g'] = row["G"]
                    aDict['mp'] = row["MP"]
                    aDict['fg'] = row["FG"]
                    aDict['three'] = row["3P"]
                    aDict['ftp'] = row["FT%"]
                    aDict['ast'] = row["AST"]
                    aDict['stl'] = row["STL"]
                    aDict['blk'] = row["BLK"]
                    aDict['tov'] = row["TOV"]
                    aDict['trb'] = row["TRB"]
                    aDict['pts'] = row["PTS"]

                    for entry in ['g', 'mp', 'fg', 'three', 'ftp', 'ast', 'stl', 'blk', 'tov', 'trb', 'pts']:
                        if entry in aDict:
                            try:
                                floatValue = float(aDict[entry])
                                aDict[entry] = floatValue

                            except Exception as error:
                                aDict[entry] = 0.0
                                #print('     Dictionary Entry', entry, aDict[entry], type(aDict[entry]))

                    #pts = round((row["PTS"]) * g, 4)

                    player_object = cp.Player(normalizedName,
                                              aDict['pos'], aDict['tm'], aDict['g'],
                                              aDict['mp'], aDict['fg'], aDict['three'],
                                              aDict['ftp'], aDict['ast'], aDict['stl'],
                                              aDict['blk'], aDict['tov'], aDict['trb'],
                                              aDict['pts']
                                              )

                    #print('     player_object about to add', player_object)
                    a.addPlayer(player_object)
                    #print('     - Test - addPlayer(player_object) -', normalizedName)
                    
                
            except Exception as error:
                handled_exceptions.append(player_object)
                
                print('     - Warning - addPlayer() did not work', player_name)
                print('     - Error', error)

                print('     - is it in AllPlayersData?', a.searchPlayer(a.getPlayer_object(player_object)))

                                                                     # Manually Add Player Entries
        self.manualPlayerEntry(a)    
# get rid of all entries that have g == []
        a.removeDuplicates()                                         # remove duplicates that may happen
        print('**** removeDuplicates() complete')
        a.addDoubleDoubles(fileName)                                 # add double double data
        print('**** addDoubleDoubles() complete')


        #a.doublesPerGame()
        #print('\n', '**** convert to doublePerGame() complete')

### a.updateRankings(), a.rankPlayers() maybe should be delayed after updateTeam?
        a.updateRankings()                                           # rank order every stat for every player
        a.rankPlayers()                                              # calcualte and store total rank for player
        

        # player, pos, tm, g, mp, fg, three, ast, stl, blk, tov, trb, pts
##        print('There was a problem adding these entries -', handled_exceptions)
##        print('')
##        for item in handled_exceptions:
##            print(item)
##            print(item.getPosition(), type(item.getPosition()))
##            print(item.getTeam(), type(item.getTeam()))
##            print(item.getField_goals(), type(item.getField_goals()))
##            print(item.getThree_pointer(), type(item.getThree_pointer()))
##            print(item.getFreethrow_per(), type(item.getFreethrow_per()))
##            print(item.getAssist(), type(item.getAssist()))
##            print(item.getSteals(), type(item.getSteals()))
##            print(item.getBlocks(), type(item.getBlocks()))
##            print(item.getTurnovers(), type(item.getTurnovers()))
##            print(item.getRebounds(), type(item.getRebounds()))
##            print(item.getPoints(), type(item.getPoints()))
##            print(item.getDoubles(), type(item.getDoubles()))
##            print(item.getTeam_wins(), type(item.getTeam_wins()))
##            print(item.getRankings(), type(item.getRankings()))
##            print(item.getTotalRank(), type(item.getTotalRank()))
            
        print('Finished Loading AllPlayerData()')
        
        
        return a                                                     # return an AllPlayersData() object

    def manualPlayerEntry(self, AllPlayersData_object):

        normalizedName = capd.AllPlayersData.normalizeText('jalen suggs')
        player_object = cp.Player(normalizedName, 'PG', 'ORL', 9, 29.2, 4.0, 1.3, 0.833, 3.4, 1.0, 0.3, 3.3, 3.6, 12.7)
        AllPlayersData_object.addPlayer(player_object)

        normalizedName = capd.AllPlayersData.normalizeText('klay thompson')
        player_object = cp.Player(normalizedName, 'SG', 'GSW', 78, 34.0, 8.4, 3.1, .816, 2.4, 1.1, 0.6, 1.5, 3.8, 21.5)
        AllPlayersData_object.addPlayer(player_object)

        normalizedName = capd.AllPlayersData.normalizeText('chris duarte')
        player_object = cp.Player(normalizedName, 'SG', 'IND', 9, 34.8, 6.4, 2.7, 0.923, 2.2, 1.0, 0.1, 1.9, 4.6, 16.9)
        AllPlayersData_object.addPlayer(player_object)

        normalizedName = capd.AllPlayersData.normalizeText('jonathan isaac')
        player_object = cp.Player(normalizedName, 'PF', 'ORL', 34, 28.8, 4.6, 0.9, 0.779, 1.4, 1.6, 2.3, 1.4, 6.8, 11.9)
        AllPlayersData_object.addPlayer(player_object)

        normalizedName = capd.AllPlayersData.normalizeText('cade cunningham')
        player_object = cp.Player(normalizedName, 'PG', 'DET', 2, 24, 1.5, 0.0, 0.500, 2.5, 0.0, 0.5, 2.0, 4.5, 4.0)
        AllPlayersData_object.addPlayer(player_object)

        normalizedName = capd.AllPlayersData.normalizeText('jalen green')
        player_object = cp.Player(normalizedName, 'SG', 'HOU', 7, 32.7, 5.3, 2.4, 0.647, 3.3, 0.9, 0.6, 2.9, 3.7, 14.6)
        AllPlayersData_object.addPlayer(player_object)

        normalizedName = capd.AllPlayersData.normalizeText('scottie barnes')
        player_object = cp.Player(normalizedName, 'PF', 'TOR', 7, 34.9, 7.7, 0.3, 0.708, 2.0, 0.7, 0.6, 2.4, 8.9, 18.1)
        AllPlayersData_object.addPlayer(player_object)

        normalizedName = capd.AllPlayersData.normalizeText('evan mobley')
        player_object = cp.Player(normalizedName, 'PF', 'CLE', 9, 33.8, 5.3, 0.2, 0.759, 2.3, 1.1, 1.3, 1.8, 8.2, 13.3)
        AllPlayersData_object.addPlayer(player_object)

        normalizedName = capd.AllPlayersData.normalizeText('alperen sengun')
        player_object = cp.Player(normalizedName, 'C', 'HOU', 7, 20, 2.7, 0.3, 0.769, 2.1, 2.3, 0.4, 3.0, 4.4, 8.6)
        AllPlayersData_object.addPlayer(player_object)

        normalizedName = capd.AllPlayersData.normalizeText('franz wagner')
        player_object = cp.Player(normalizedName, 'SF', 'ORL', 9, 32.0, 5.9, 2.2, 0.667, 1.7, 1.1, 0.6, 0.9, 3.6, 14.9)
        AllPlayersData_object.addPlayer(player_object)

        normalizedName = capd.AllPlayersData.normalizeText('xavier tillman')
        player_object = cp.Player(normalizedName, 'PF', 'MEM', 59, 18.4, 2.8, 0.4, 0.642, 1.3, 0.7, 0.6, 0.8, 4.3, 6.6)
        AllPlayersData_object.addPlayer(player_object)

    def runMulti(self):
        
        url1 = "https://www.basketball-reference.com/leagues/NBA_2021_per_game.html"
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
    
   
