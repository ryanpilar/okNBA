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
        self.total_rank = 1000


        
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

    def returnColumnHeaders(self):
        return self.column_headers
    def returnPlayerData(self):
        return [
            self.player, self.position, self.team, self.games, self.minutes_game,
            self.field_goals, self.three_pointer, self.ft_percentage,
            self.assist, self.steals, self.blocks, self.turnovers, self.points,
            self.rebounds, self.doubles, self.total_rank
            ]

    def convertPoints(self):
        # need to implement ,self.team_wins, AND i addeded self.ft_percentage really late,
        # not sure if this is going to effect things?
        # i did NOT include self.turnovers in this equation!
        convertThese_Points = [
            self.field_goals, self.three_pointer, self.ft_percentage, self.assist,
            self.steals, self.blocks, self.points, self.rebounds,
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
        When a new Player is added, this function assembles simply assembles
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
