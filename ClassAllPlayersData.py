import statistics 
import unicodedata 
import ClassPlayer as cp

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
            print('\t', 'WARNING - duplicate values coming from addPlayer()')
        else:
            self.playerDict[key] = value
            
    def removePlayer(self, player):
        del self.getDict()[player]

    def normalizeText(text):
        '''
        this scraping programs scrape from multiple sources. Each source formats their text
        differently. 'TJ' vs 'T.J.' for example. This code strips down or 'normalizes' the
        formatting of incoming text, so less problems rise when interacting with the main database '''

        

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
        duplicate_objects = []    				# this is a list of Player objects
        duplicate_tracker = []    				# this is a list of strings
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
            
            # 1 - get player info/object that already exists in the dict
            player_object = self.getPlayer_object(player_string)
            
            # convert data into list form
            multiple_lists = []

            keyFunction_list = [
                cp.Player.getField_goals, cp.Player.getThree_pointer,
                cp.Player.getFreethrow_per, cp.Player.getAssist, cp.Player.getSteals,
                cp.Player.getBlocks, cp.Player.getTurnovers, cp.Player.getRebounds,
                cp.Player.getPoints
                ]
            
            
            data_list = player_object.dataList(keyFunction_list)
            
            multiple_lists.append(data_list)
            
            # 2 - go through all the duplicate objects, we want to match/find player_string!
            for player_object_ in duplicate_objects:
                if player_string == player_object_.getPlayer():
                    
                    # convert this object into list form and add it to aList

		
                    temp_list = player_object_.dataList(keyFunction_list)
                    multiple_lists.append(temp_list)
                    
            #print('yo! Multiple LISTS', player_string, multiple_lists)

            # calcualte the averages of the duplicate values and add this value to the new dictionary
            result = [statistics.mean(k) for k in zip(*multiple_lists)]

            #print('yo yo! These should be the results!', result)
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
            cp.Player.getField_goals, cp.Player.getThree_pointer,
            cp.Player.getFreethrow_per, cp.Player.getAssist, cp.Player.getSteals, 
            cp.Player.getBlocks, cp.Player.getTurnovers, cp.Player.getRebounds,
            cp.Player.getPoints
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

            if keyFunction == cp.Player.getTurnovers:
                temp.reverse()
            master_list.append(temp)

##            print('\n', keyFunction, '\n')
##            for item in temp:
##                print(item)
           
        return master_list
    
    def rank_every_player_category(self):
        '''
        makes sorted lists
        sorts according to the keyFunctions
        '''

        ## i need to still include cp.Player.getTeam_wins!
        keyFunction_list = [
            cp.Player.getField_goals, cp.Player.getThree_pointer,
            cp.Player.getFreethrow_per, cp.Player.getAssist, cp.Player.getSteals, 
            cp.Player.getBlocks, cp.Player.getTurnovers, cp.Player.getRebounds,
            cp.Player.getPoints, cp.Player.getDoubles
            ]
        master_list = []
        
        for keyFunction in keyFunction_list:
            sorted_list = self.sortPlayers(keyFunction)
            
### send all functions through cleanData() to help eliminate messy data in poor ranking players

            #print('BEFORE', sorted_list)
            sorted_list = self.cleanData(keyFunction, sorted_list)
            # -- > remove duplicates (havn't solved why their are duplicates yet

            print('')
            #print('AFTER', sorted_list)
            
            aList = []
            temp = []

            try:
                for i in sorted_list:
                    if i.player in aList:

    ### need to rectify duplicates!
                        #print('')
                        #print('duplicate entry in rank_every_player_category(), unexplained!')
                        pass
                    else:
                        aList.append(i.player)
                        temp.append(i)

                if keyFunction == cp.Player.getTurnovers:
                    temp.reverse()
                    
                master_list.append(temp)
            except Exception as error:
                print("ERROR MESSAGE", i, type(i))
                print(error)
            
            
        return master_list

    def cleanData(self, keyFunction, sorted_list):
        print('')
        print('cleanData entered sorted_list', sorted_list)
        # needs to be reverse sorted, because the lower the turnover the better. this should be a per game stat too.
        # b/c players that play less will inherently have less turnovers, which is a good stat!
        ### TOV zero turnover problem when ranking. also poor players seem to have a closed-box-entry ([]) in games. 24<
        if keyFunction == cp.Player.getTurnovers:
            for player in sorted_list:

                # some players have an empty list, [], recorded under games
                if type(player.games) == list:

                    # changing games to equal .1, ruins the players stat for this category
                    player.games = .1
                    

            
            return sorted_list.reverse()
        
        ### FT% players that achieve 1.0, which are generally poor players, need to be reclassified
        elif keyFunction == cp.Player.getFreethrow_per:
            return sorted_list

        ### DBLS maybe a better per game stat?
        elif keyFunction == cp.Player.getDoubles:
            return sorted_list

        return sorted_list
    
    def sortDoubles(self):
        '''update in the future: this function should evetually be included with the other sortFunctions'''
        keyFunction = cp.Player.getDoubles
        sorted_list = self.sortPlayers(keyFunction)
        
        return sorted_list

# check to see if this is being deployed. i think its set a totals right now
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
        
        ### master_list includes everything BUT a sorted double double list ###
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
                    print('@@@@@@ WARNING - Double Double list complication:', aList[0])
                
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
        keyFunction = cp.Player.getTotalRank
        sorted_list = self.sortPlayers(keyFunction)
        sorted_list.reverse()
        
        if print:
            for item in sorted_list:
                print(item)
                print('---------------------- rank list:', item.getRankings())
