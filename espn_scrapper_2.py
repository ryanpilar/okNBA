#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import espn_scrapper

import pytz
import espn_api
import random
import requests
from espn_api.basketball import League
from datetime import datetime, timezone, timedelta
from basketball_reference_web_scraper import client

class TeamSchedule():
    def __init__(self, name, initials, schedule):
        self.name = name
        self.initials = initials
        self.schedule = schedule
        
    def getTeamObject(self, initials):
        return self
    def getSchedule(self):
        return self.schedule


    def __str__(self):
        return self.initials

class FantasyTeam():
    def __init__(self, name):
        self.name = name                                        # espn.api Team object, not a string
        self.roster = []                                        
        
    def getName(self):
        espn_api_team_object = self.name
        return espn_api_team_object.team_name
    
    def getRoster(self):
        return self.roster

class Data_Center():
    
    def __init__(self):
        
        self.leagueId = 782572893
        self.url = 'https://fantasy.espn.com/basketball/league?leagueId=***YOUR-LEAGUE-IDEA-HERE***'
        self.cookie_1 = '{***YOUR-SWID-COOKIE-HERE***}'
        self.cookie_2 = '***YOUR-ESPN_S2-COOKIE-HERE***'
        self.TeamData = {}
        self.FantasyTeams = []
        self.calander = None
        
        # using the requests library, use the url and needed cookies
        r = requests.get(self.url, cookies = {"swid": self.cookie_1, "espn_s2": self.cookie_2})

        # from the espn_api.basketball, make a league object
        league = League(self.leagueId, year=2022, espn_s2 = self.cookie_2, swid = self.cookie_1)
        print(league)
        self.espn_api_object = league
        
        # create a AllPlayer Data Object / load all player stats 
        self.AllPlayerData = espn_scrapper.loadData()
        

    def getAllPlayerData(self):
        return self.AllPlayerData
    def getESPN_object(self):
        return self.espn_api_object
    def getTeamData(self):
        return self.TeamData
    def getFantasyTeams(self):
        return self.FantasyTeams
    def getCalander(self):
        return self.calander
    
    def saveMatchups(self, text):
        '''
        takes in text, and prints it to local file, espn_savematchups.txt

        returns: nothing
        '''
        # open the file
        file_var = open('espn_savematchups.txt', 'a')
        print(text, file = file_var)

        # close the file
        file_var.close()
        
    def updateTeamData_txt(self):
        '''
        this function, when MANUALLY called, will look up all matches 
        for the current week via espn_api and stores the data, including 
        player line-ups to a local .txt file
        
        .scorebored() defaults to current week but can be specified to
        display a specific week
        
        returns nothing, but updates self.TeamData
        '''
        matchups = self.getESPN_object().scoreboard()
        not_entered = []
        Team_Data = {}
        
        date = datetime.now().date()

        for match in matchups:
                        
            # unpack matchup object
            the_teams = [match.home_team, match.away_team]
            build_string = str(date) + '&&' + match.home_team.team_name + '**' + match.away_team.team_name 
            
            Team_Data[match.home_team] = [[],[]]
            Team_Data[match.away_team] = [[],[]]
            
            for team in the_teams:
                
                player_object_list = team.roster
                build_string_2 = '**'
                
                for player_object in player_object_list:
                    Team_Data[team][0].append(player_object)

                    # normamlize text
                    name = player_object.name
                    player_string = espn_scrapper.AllPlayersData.normalizeText(str(name))
                    build_string_2 += player_string + ','
                    
                    # varify player is in the data set 
                    if not self.AllPlayerData.searchPlayer(player_string):
                        Team_Data[team][1].append(player_string)
                        print('---not entered:', player_string)
                        not_entered.append(player_string)
                        

                    else:
                        Team_Data[team][1].append(self.AllPlayerData.getPlayer_object(player_string))
            
                build_string += build_string_2 
            self.saveMatchups(build_string)
            
        # update TeamData
        self.TeamData = Team_Data
    def correctTeam(self):
        ''' takes in a espn_api object that has the correct team information, it then looks up the player
in the AllPlayersData dictionary, and updates his position'''

        for key, value in self.getTeamData().items():

    
            # iterate over the espn_api players in every fantasy team
            for i in value[0]:
                name, team_initials = i.name, i.proTeam

                try:
                    # get AllPlayer Object
                    normalized = espn_scrapper.AllPlayersData.normalizeText(str(name))
                    AllPlayer_object = self.AllPlayerData.getPlayer_object(normalized)
                    # update correct initials
                    AllPlayer_object.team = team_initials
                except:
                    print('did not work correcTeam', name, team_initials)
                    pass
                
    def updateTeamData(self, week = 0):

        '''
        This function grabs the current weeks matchups via the espn_api. It then looks at each
        team's roster and converts the corresponding espn_api objects  into AllPlayerData objects.

        subsequently, self.TeamData is updated with this new information.
        '''
        print('updating TeamData...')
        
        matchups = self.getESPN_object().scoreboard(week)
        not_entered = []
        Team_Data = {}
        date = datetime.now().date()

        for match in matchups:
                                                                # unpack the espn_api matchup object
            the_teams = [match.home_team, match.away_team]
                                                                # [key] espn.api team objects
            Team_Data[match.home_team] = [[],[]]                # [0] roster of espn.api player objects
            Team_Data[match.away_team] = [[],[]]                # [1] roster of AllPlayerData.getPlayer_object's
            
            for team in the_teams:                          
                player_object_list = team.roster                # these are espn_api player objects
                
                for player_object in player_object_list:
                    
                    Team_Data[team][0].append(player_object)    

                    name = player_object.name                   # normamlize text
                    player_string = espn_scrapper.AllPlayersData.normalizeText(str(name))
                    
                                                                # before preoceeding. varify normalized text is in AllPlayerData 
                    if not self.AllPlayerData.searchPlayer(player_string):
                        Team_Data[team][1].append(player_string)
                        not_entered.append(player_string)
                        print('---not entered:', player_string)
                    else:                                       # use normalized text to getPlayer_object in AllPlayerData
                        Team_Data[team][1].append(self.AllPlayerData.getPlayer_object(player_string))
                                                                # !!ALSO!! correct player position in AllPlayerData !!HERE!!
                        all_player_object = self.AllPlayerData.getPlayer_object(player_string)
                        all_player_object.position = player_object.eligibleSlots

                        
                        

                        
        self.TeamData = Team_Data                               # update self.TeamData
        self.correctPositions()                                 # positions coming from espn_api is always dirty
        

    def correctPositions(self):
        ''' accepts a player object fetched from the espn_api. It gives up to date position information but its a list that also includes
some ambiguous . This function removes the ambiguous entries, and returns ONLY the player positions'''

        # go into self.TeamData and grab all the players espn_api objects (who will be assigned to teams)
        # use those espn_api objects to look up their positions
        # use those position values and update Player() data

        all_players = self.getAllPlayerData().getDict()
        to_be_removed = ['G', 'SG/SF', 'G/F', 'UT', 'BE',
                     'Rookie', 'PF/C', 'IR', 'F', 'F/C']


        for player in all_players:
            updated_position = []

            for position in player.position:
                if position in to_be_removed:
                    pass
                else:
                    updated_position.append(position)
            player.position = updated_position

    def normalizeTurnovers(self):
        aDict = self.getAllPlayerData().getDict()
        collect_turnovers = []

        for player in aDict:
            collect_turnovers.append(player.turnovers)
    
        penalized_mean = (sum(collect_turnovers)/len(collect_turnovers))*1.35   # this is the average turnover in the league

        # if a player is less than mean, and has less than 10 games, normalize their turnover data
        for player in aDict:
            turnovers = player.turnovers
            games = player.games

            try:
                if turnovers < penalized_mean and games < 15:
                    player.turnovers = penalized_mean
            except:                                                             # errors regarding player.games, default penalized_mean
                player.turnovers = penalized_mean
                
    def updatePositions(self, alist):

        for i in alist:

            update = []
            for pos in i.eligibleSlots:
                #if pos == 'G' or pos == 'SG/SF' or pos == 'G/F' or pos == 'UT' or pos == 'BE' or pos == 'Rookie' or pos == 'PF/C' or pos == 'IR' or pos == 'F' or pos == 'F/C':
                   # pass
                #else:
                update.append(pos)

            # look up Player object and update his position
            normal = espn_scrapper.AllPlayersData.normalizeText(str(i.name))
            player_object = self.getAllPlayerData().getPlayer_object(normal)

            player_object.position = update

                
    def updateFreeAgents(self, toPrint = False):
        '''this iterates over espn_free agents, and adds whatever players that were not already added to AllPlayerData'''
        
        
        yes = []
        no = []

        for position in ['PG', 'SG', 'SF', 'PF', 'C']:
            
            # Pull all the ESPN_api free agents for the given position
            for player in (self.getESPN_object().free_agents(1, 1000, position, None)):
                
                name = player.name
### espn_scrapper
                normal = espn_scrapper.AllPlayersData.normalizeText(str(name))

                # search to see if espn_object is in AllPlayer Data
                if self.getAllPlayerData().searchPlayer(normal):
                    if not player in yes:
                        # we don't need the data if its already in AllPlayer
                        yes.append(player)
                else:   # filter player data that is not in our dataset:
                    if not player in no:
                        no.append([position, player])
                        
        alist = []
        for i in no:
            
            
            try:
                stats = i[1].stats
                # get rid of players that have empty data
                if stats == {}:
                    continue
                # get player data from espn
                for value in stats.values():
                    data = value['avg']
                    
    ###espn_scrapper
                    name = espn_scrapper.AllPlayersData.normalizeText(str(i[1].name))
      
                    
                    # make a Player object, using espn-api data for input paramaters
                    addPlayer = espn_scrapper.Player(name, i[0], i[1].proTeam, [], data['MPG'], data['FGM'], \
                                       data['3PTM'], data['FT%'], data['AST'], data['STL'], data['BLK'], \
                                        data['TO'], data['REB'], data['PTS'])
                    self.getAllPlayerData().addPlayer(addPlayer)
                    yes.append(i[1])

            except:
                alist.append(i)
                pass

        if toPrint:

            print('Misc Free Agent Names That Did Not Convert Well:')
            for i in alist:
                print('\t', i)

        self.updatePositions(yes)

        for i in self.getAllPlayerData().getDict():
            if type(i.position) == list:
                pass
            else:
                i.position = [i.position]
                
        # manually update the positions for the following Players:
        player = [('keita bates-diop', ['SF']), ('alec burks', ['SG']), ('gary clark', ['PF']), ('robert covington', ['PF']), ('jae crowder', ['PF', 'SF']),
                  ('james ennis', ['SG', 'SF']), ('jeff green', ['PF']), ('maurice harkless', ['SF']), ('reggie jackson', ['PG']), ('james johnson', ['PF', 'SF']),
                  ('tyler johnson', ['PF', 'SG']), ('brandon knight', ['PG']), ('marcus morris', ['PF', 'SF']), ('caleb swanigan', ['PF'])]

        for i in player:
            
            player_object = self.getAllPlayerData().getPlayer_object(i[0])
            player_object.getPosition = i[1]
        

    def getLeaguePlayers(self):

        e = self.getTeamData()
        alist = []
        
        for key, value in e.items():
            
            players = value[1]
            for player in players:
                alist.append(player)

        return alist         

    def getFreeAgents(self):
        just_league_players = self.getLeaguePlayers()
        whole_league = self.getAllPlayerData().getDict()

        alist = []

        
        for player in whole_league:
            if not player in just_league_players:
                if not player.getTotalRank() == None:
                    alist.append(player)

        keyFunction = espn_scrapper.Player.getTotalRank
        sorted_copy = sorted(alist, key = keyFunction, reverse = False)

        for i in sorted_copy:
            print(i.position, i.getTotalRank(), i.getPlayer())

        return sorted_copy


        
    def createCalander(self):
        '''
        this function organizes the days of a Fantasy calander year by taking sets of datetime objects of len(7), and packaging
        the set with its corresponding week number. This 'week number' (an int) needs to line up with the 'week number' that defines
        what weekly matchup espn_api is pulling.

            - Week 1 starts on day zero.
            - Day zero, and Week 1 starts on December 21st 2020
            - Week 1 ends Dec 27th 2020, and Week 2 start Dec 28th

        returns: nothing, but creates a list of datetime objects and updates self.calander

        *** there is an obious problem. First half of the season is dec 22-mar 4th. this is currently all that
        the espn_api is fetching. Will this be automatically updated or will i have to utilize an ulternate param?
        '''
        print('create Calander...')
        
        first_day, last_day = datetime(2020, 12, 21), datetime(2021, 12, 21)

        #first_day = first_day.replace(tzinfo=pytz.UTC)  # make aware
        
                                                        # convert to UTC/ETC/Greenwich
        first_day = first_day.astimezone(pytz.timezone('UTC')) #'US/Mountain'

        #last_day = last_day.replace(tzinfo=pytz.UTC)    # make aware
        
        last_day = last_day.astimezone(pytz.timezone('UTC'))

        
        the_day = first_day
        calander_weeks = []
        week_number = 1
        
        while the_day < last_day:
            week = [[],[]]
            week[0] = week_number
            week_number += 1
            
            for day in range(7):                                # range(7) days in a week
                week[1].append(the_day)
                the_day += timedelta(days=1)

            calander_weeks.append(week)
        self.calander = calander_weeks

        print('\t'+'\t'+'complete')
        

    def createFantasyTeams(self, week):
        '''
        This will create a list of FantasyTeam objects. The weeks match ups are looked up,
        along with each team's corresponding player roster. This data is then organized into a
        more familiar form, called FantasyTeam.
        
        returns: nothing, but updates the list of self.FantasyTeams found in Data_Center  
        
        '''
        print('creating Fantasty Teams...')
        
        self.updateTeamData(week)                               # fetch the weeks matchups via espn_api and updateTeamData()
        
        FantasyTeams_list = []

        for key in self.getTeamData():                          # create a FantasyTeam with every key in TeamData (key = espn.api Team object)
            FantasyTeams_list.append(FantasyTeam(key))

        self.FantasyTeams = FantasyTeams_list

        print('\t'+'\t'+'complete')

    # complete --> update Team Data complete
    # complete --> convert that Team Data into a Fantasy Object
    # Make a week matchup that corresponds to datestamps and checks individual player schedule on every day
    # create a mock weekly schedule, with date stamps,  and does not throw errors with the limiting march data

    #def count_each_pos(self, alist):
        '''this will take in a list of players, counts every eligible position a player can play and
        returns a list of dictionaries, sorted by their values, increasing order '''
        
        aDict = {'PG':[], 'SG':[], 'SW':[], 'PF':[], 'C':[]}

        for player in alist:
            positions = player.position

            for pos in positions:
                if pos == 'PG':
                    aDict[pos].append(player)
                if pos == 'SG':
                    aDict[pos].append(player)
                if pos == 'SW':
                    aDict[pos].append(player)
                if pos == 'PF':
                    aDict[pos].append(player)
                if pos == 'C':
                    aDict[pos].append(player)

        for k,v in aDict.items():                       # remove the positions that ended up being empty lists
            if v == []:
                del aDict[k]
    
        #return [k, v for k, v in sorted(aDict.items(), key=lambda item: len(item[1]), reverse = False)]

    def decide_priority(self, pos_list, player_list):
        # least counted player position please
        aList = count_each_pos(player_list)

        for i in aList:
            if i[0] in pos_list:
                return i

            else:
                print('ERROR! none of the players play positions that can fill the pos_list')
                
    def calculatePoints(self, team, datetime_objects):
        
        team_roster = []
        fg, three, ast, stl, blk, tov, pts, trb, dbl = [], [], [], [], [], [], [], [], []
        weekly_line_up = []
        
        for team_object in self.TeamData:                       

            if team_object == team:                             # grab roster for paramter team

                roster = self.getTeamData()[team_object]
                team_roster = roster[1]

        for day in datetime_objects:

            day = self.changeTimeZone(day)

            #print('\t', 'the day start:', day, 'day end:', (day + timedelta(hours=23)))

            # find which players are playing on this day
            playing_today = []
            
            for player in team_roster:

                normalized = espn_scrapper.AllPlayersData.normalizeText(str(player.player))
                # look up player_object in all players data
                if not self.getAllPlayerData().searchPlayer(normalized):
                    print('strings from espn did not line up with my ALL Players Data')
                    return None
                
                player = self.getAllPlayerData().getPlayer_object(normalized)
                full_player_schedule = player.team.schedule
                for game in full_player_schedule:
                    game = self.changeTimeZone(game[0])             # player games that are within parameter datetime_objects
                    
                    if day < game and game < (day + timedelta(hours=23)):
                        playing_today.append(player)                # if True, store Player() for that day
                        break

                                                                    # all 5 positions need to be satisfied, to avoid a False
            aList = ['PG', 'SG', 'SW', 'PF', 'C']
            more_than_one = []
            
            if len(playing_today) <= 4:                             # 4 or less players playing, has no possitional constraints
                print('\t', '\t', 'line up is <= 4!')
                break

            # decide priority of the entire day of players, and randomly pick a player for every position
            # try finding a pick for that position, if no go after a bazillion tries, enter empty as a value for the position
            # leaving the most common position for last, or the utility positions
            
                                                                    # if set is >= len(8), enter this elif
            elif len(playing_today) >= 8:
                playing_today = random.sample(playing_today, 8)

                for player in playing_today:
                    if len(player.position) == 1:
                        try:
                            aList.remove(position)
                        except:
                            pass
                    else:
                        more_than_one.append(player)

                # -- what happens if more_than_one is an empty list and enters this while loop? -- #

                while_counter = 0
                while len(aList) > 0:

                    # grab the player with the position of least occurance amonst the other players, while also satisfying aList
                    position, the_players = decide_priority(aList, more_than_one)

                    for i in range(150):        # if remove() fails, another random pick can be done, range(150) to exhaust options
                        pick_random = random.choice(the_players)

                        try:                    # if an error is thrown, we have already used the player 
                            more_than_one.remove(pick_random)
                            aList.remove(position)
                            break
                        except:
                            pass

                    if len(aList) == 0:
                        break                   # evrything in aList has been satisfied, so playing_today is a valid line-up

                    while_counter += 1
                    if while_counter > 150:
                        return [False, weekly_line_up]
                        break

            elif len(playing_today) == 7:
                # atleast 4 positions need to be satisfied
                alist = ['PG', 'SG', 'SW', 'PF', 'C']

                for player in playing_today:
                    position = random.choice(player.position)

                    if position in alist:
                        alist.remove(position)

                if len(alist) > 1:
                    return [None, weekly_line_up]                                      # if strings are left, position is unsatisified!

            elif len(playing_today) == 6:
                # atleast 3 positions need to be satisfied
                alist = ['PG', 'SG', 'SW', 'PF', 'C']

                for player in playing_today:
                    position = random.choice(player.position)

                    if position in alist:
                        alist.remove(position)

                if len(alist) > 2:
                    return [None, weekly_line_up]                                      # position is unsatisified!

            elif len(playing_today) == 5:
                # atleast 3 positions need to be satisfied
                alist = ['PG', 'SG', 'SW', 'PF', 'C']

                for player in playing_today:
                    position = random.choice(player.position)

                    if position in alist:
                        alist.remove(position)

                if len(alist) > 3:
                    return [None, weekly_line_up]                                      # position is unsatisified!

            weekly_line_up.append(playing_today)

        return [True, weekly_line_up]

 

        # for every day in the datetime objects, check to see:
        #-1--- who is playing
        #-2--- who is injured
        #-3--- find that powerset of players left, it should be smaller
        #-4--- eliminate powersets that do not satisfy the position requirements
        #-5---------------> write a def that takes in a set (line-up) and checks if it satisfies position requirements
        #-6--- if True, return a dictionary, players as keys, and their returnPoints() as values
        #-7--- when all monday players are tallied, Monday is added to a dictionary, the datetime being the key,
                          # dictionary of players being the values
        #-8--- do this for every day of the week
        #-9--- Save the full weeks results in a global variable. If the total points of the new additions is more,
                          # than the old one is given the boot

        #-10-- run this simulation 100,000 of times, and see if we can pick out some optimal lineups
        
        



    def runMonteCarlo(self, numTrials, population):

        aDict = {}
        
        for trial in numTrials:
            sample = random.sample(population, 8)        
    
        
    def calculateMatchups(self, week):
                                                            # make sure the FantasyTeams are up to date
        #self.updateTeamData()
        
        get_matches = self.getESPN_object().scoreboard(week)# list of Match objects from espn.api

                                                            
        datetime_objects = ''
        for i in self.getCalander():                        # search for week in calander, and grab its datetime_objects
            if i[0] == week:
                datetime_objects = i[1]
                break

        monday = datetime_objects[0]
        friday = datetime_objects[-1]
        print('Monday:', self.changeTimeZone(monday), 'Friday:', self.changeTimeZone(friday))
        
        for match in get_matches:                           # get_matches = [[espn_api team obects],[],..]
            #pass
            print('The Match:')
            print('\t', match)
            
            home_team, away_team = match.home_team, match.away_team
            print('\t', 'home team:', home_team)            # calculate points for home_team        
            print('\t', 'away team:', away_team)            # calculate points for away_team


            def monte(numTrials, home_team, datetime_objects):

                count = 0
                for i in range(numTrials):

                    week_set = self.calculatePoints(home_team, datetime_objects)
                    if week_set[0] == True:
                        print('-------', 'Valid Line-up:')
                        week_line_up = week_set[1]
                        for i in range(len(week_line_up)):
                            print('day:', week_line_up[i])
                    else:
                        if count < len(week_set[1]):
                            count = len(week_set[1])
                            print('printing:', len(week_set[1]), week_set[1])

                print('final count:', count)
            

            monte(10000, home_team, datetime_objects)
            break
                        

  
            

    def getArchivedMatchups(self):
        '''
        This will read espn_savematchups.txt, convert its contents into list form,
        and apply a calculation to each matchup. The calculation is the optimization model
        i applied during the draft. This saves weekly rosters, so they can be referenced later
                
        [ [ timestamp, (team_winner, team_avg), won by: the difference] ]
        
        returns: a list of predicted winners
        '''

        try:
            file_var = open('espn_savematchups.txt', 'r')
        except:
            print('An Error occured while trying to open', file_var)
        else:
            
            prediction_list = []
            for item_line in file_var:

                new_line = item_line.strip('\n')
                new_line = new_line.replace('[', '')
                new_line = new_line.replace(']', '')
               
                # split at &&... datestamp will be element [0], and matchup data will be [1]
                datestamp, matchup_data = new_line.split('&&')
                matchup_data_splitted = matchup_data.split('**')
                
                # find players and calculate average
                team_one = matchup_data_splitted[0]
                team_two = matchup_data_splitted[1]
                team_one_data = matchup_data_splitted[2]
                team_two_data = matchup_data_splitted[3]
                
                splitted = team_one_data.split(',')
                splitted_two = team_two_data.split(',')
                
                player_ranks = []
                for player_string in splitted:
                    
                    if player_string == '':
                        pass
                    else:
                        a = self.getAllPlayerData().searchPlayer(player_string)
                        
                        player_object = self.getAllPlayerData().getPlayer_object(player_string)
                        total_rank = player_object.getTotalRank()
                        player_ranks.append(total_rank)
                
                player_ranks_two = []
                for player_string in splitted_two:
                    
                    if player_string == '':
                        pass
                    else:
                        a = self.getAllPlayerData().searchPlayer(player_string)
                        
                        player_object = self.getAllPlayerData().getPlayer_object(player_string)
                        total_rank = player_object.getTotalRank()
                        player_ranks_two.append(total_rank)
                
                # package everything together
                team_one_avg = [team_one, sum(player_ranks)/len(player_ranks)]
                team_two_avg = [team_two, sum(player_ranks_two)/len(player_ranks_two)]
                
                difference = abs(team_one_avg[1] - team_two_avg[1])
                
                if team_one_avg[1] < team_two_avg[1]:
                    winner = team_one_avg, difference
                else:
                    winner =  team_two_avg, difference
                
                prediction_list.append([datestamp, winner])
            return prediction_list
        
        finally:
            file_var.close()
            
    def changeTimeZone(self, utc_datetime_object):
        '''
        basketball_reference_web_scraper is used to get the NBA schedule
        and the api returns a datetime object in a utc timezone. This function
        adjusts the default utc timezone to eastern timezone
        
        takes in: a datetime object in the utc timezone
        returns: a datetime object in your local timezone'''

        #convert to aware
        #naive_to_aware = utc_datetime_object.replace(tzinfo=timezone.utc)

        
        #utc_datetime_object.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return utc_datetime_object.astimezone(pytz.timezone('US/Mountain'))
        
    def getSeasonSchedule(self):
        '''
        this function uses the basketball_reference_web_scraper api,
        the api is an easy way to grab datestamps of every matchup
        
        ** right now it only scrapes until end of March, make sure this updates
        as the season goes on
        
        returns: a dictionary, player teams as keys, datestamps as values
        '''
        season = client.season_schedule(season_end_year=2021)   # list of dicts, each dict representing a game
                                                                 
        SeasonSchedule = {}                                     # a dictionary, keys being the teams
        for game in season:

            datetime, away_team, home_team = '', '', ''

            for key, value in game.items():                     # key: 'a_string'
                if key == 'start_time':                         # value: 
                    datetime = game[key]
                    #datetime = datetime.astimezone(pytz.timezone('EST')) #'Etc/Greenwich'

                elif key == 'away_team':
                    away_team = (game[key]).value
                                                                # normalize the data
                    away_team = espn_scrapper.AllPlayersData.normalizeText(str(away_team))
                    
                                                                # add team: datestamp to SeasonSchedule
                    if not away_team in SeasonSchedule:
                        SeasonSchedule[away_team] = []
                    if not datetime in SeasonSchedule[away_team]:
                        SeasonSchedule[away_team].append([datetime, 'a'])
                
                elif key == 'home_team':
                    home_team = (game[key]).value
                                                                # normalize the data
                    home_team = espn_scrapper.AllPlayersData.normalizeText(str(home_team))
                    
                                                                # add team: datestamp to SeasonSchedule
                    if not home_team in SeasonSchedule:
                        SeasonSchedule[home_team] = []
                    if not datetime in SeasonSchedule[home_team]:
                        SeasonSchedule[home_team].append([datetime, 'h'])
                
        # a dictionary                    
        return SeasonSchedule 
    
    def getInitials(self):
        '''
        this function uses NBA_abreviations.csv to find its corresponding initials
        
        returns: a list containing the team name and its corresponding abreviation        
        '''
        try:
            openFile = open('NBA_abreviations.csv', 'r')
        except:
            print('A File Related Error Occured')
            
        else:
            team_list = []
            for line in openFile:
                line = line.strip()
                line = line.split(',')
                 
                team_name = espn_scrapper.AllPlayersData.normalizeText(str(line[0]))
                team_list.append([team_name, line[1]])
            return team_list
    
    def createSchedule(self):
        '''
        this functions uses self.getInitials() and self.getSeasonSchedule 
        to add a team object to every player in the league. The Team object
        holds the entire schedule for that team and thus can be referenced
        through every individual player object
        '''
        print('creating Shedule...')
              
        initials = self.getInitials()               # a list containing the team name and its corresponding abreviation
        schedule = self.getSeasonSchedule()         # a dictionary, player teams as keys, [datestamps,'a'] as values
        
        adict = {}
        
        # make Teams and store their datestamps in adict
        for name, datestamps in schedule.items():
            for item in initials:

                if item[0] == name:
                    initial = item[1]
            
                    add = TeamSchedule(name, initial, datestamps)
                    adict[initial] = add
                    
        for player_object in self.getAllPlayerData().getDict():
            team_abr = player_object.team
            
            # handle the one weird cases of abbreviations, like BRK, and change it to what we need
            if team_abr == 'BRK':
                team_abr = 'BKN'
            elif team_abr == 'TOT':
                team_abr = 'TOR'
            elif team_abr == 'PHO':
                team_abr = 'PHX'
            elif team_abr == 'CHO':
                team_abr = 'CHA'
            elif team_abr == 'PHL':
                team_abr = 'PHI'

            try:
                team_object = adict[team_abr]
                player_object.team = team_object
            except:
                print(team_abr)

        print('\t'+'\t'+'complete')

        
            
