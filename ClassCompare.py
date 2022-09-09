import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

import ClassAllPlayersData as capd

'''
two calls exist at the bottom of this cell:

    - getFantasyTeams()                              
    - compareTwo(player_A, player_B) 
    
    getFantasyTeams() will calculate the average rank average fro every category 
    for every Fantasy Team

    compareTwo(player_A, player_B) will plot two players rank averages side by side

'''
    
class Compare():
      def __init__(self, dcObject):
            self.Data_Center = dcObject
            self.matPlotFigure = None
            self.fig = None
            self.ax = None
      def getData_Center(self):
            return self.Data_Center
 

      def calculateTeamAvg(self, aList):
            return [round(float(sum(col))/len(col)) for col in zip(*aList)]


      def getFantasyTeams(self):
          
            TeamData_dict = self.getData_Center().getTeamData()

            
          
            for team, v in TeamData_dict.items():
                  roster = v[1]
                  full_team = []
              
                  # this iterates over every player found in each Fantasy team
                  for player in roster:
                        try:
                              aList = self.rankPlayerCategories(player)
                              full_team.append(aList)
                        except Exception as error:
                              print('')
                              print('ERROR', error)
                              print('')
                              pass


              
                  TeamAvg = self.calculateTeamAvg(full_team)
                  print(team)
                  print('\t', 'TeamAvg:', TeamAvg)
                  
              
        
      def rankPlayerCategories(self, player):
            
            # these lists are sorted from best to worst:           
            sorted_categories = self.getData_Center().getAllPlayerData().rank_every_player_category()
            print('')
            print('SORTED_CATEGORIES', sorted_categories)
            
            sorted_rank_categories = []
                
            for category in sorted_categories:

                                                                        # remember we are searching for 'player' in every 'category'
                                                                        # [i]'th position will be the player's rank in that category
                  for i in range(len(category)):
                        #print(category[i], type(category[i]))
                        try:
                              #print('     ', category[i].player, player.player)
                              if category[i].player == player.player:
                                    sorted_rank_categories.append(i)
                              else:
                                    pass
                        except Exception as error:
                              print('')
                              print('EXCEPTION at rankPlayerCategories', error)
                              print('     ', category[i].player)
                              print('     ', type(category[i].player), type(player.player))
                              print('')

                              pass
                        
            ## for the testing of category enties
            headers = ['Name', 'Pos', 'Tm', 'Gm', 'MP',
                       'FG', '3s', 'FT%', 'Ast', 'Stl',
                       'Blk', 'TOV', 'TRB', 'Pts', 'Dbl',
                       'Avg Rank']

            df2 = pd.DataFrame(columns = headers)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            pd.set_option('display.colheader_justify', 'center')
            pd.set_option('display.precision', 3)
          
            toTest = True
            while toTest:
                  temp = sorted_categories[6]            
                  
                  for i in range(len(temp)):
                       
                        player_data = temp[i].returnPlayerData()
                        df2.loc[len(df2)] = player_data
                        
                        #df2.append(pd.DataFrame([player_data])
                        #print('\t', '\t', i, temp[i].player, temp[i].turnovers, temp[i].games)
                        
                  #display(df2)
                  #raise SystemExit('Manual exception Rasied!')
                  break
                   
          
            try: 
                  sorted_rank_categories.append(round(player.getTotalRank(), 2))
            except:
                  print('except thrown right after round(player.getTotalRank(), 2)')
                  pass

            return sorted_rank_categories
          
      def compareTwo(self, player_A, player_B):
            player_A = self.getData_Center().getAllPlayerData().getPlayer_object(capd.AllPlayersData.normalizeText(str(player_A)))
            player_B = self.getData_Center().getAllPlayerData().getPlayer_object(capd.AllPlayersData.normalizeText(str(player_B)))


            column_headers = self.getData_Center().getColumnHeaders() 

            

            
            player_A_ranks = self.rankPlayerCategories(player_A)
            player_B_ranks = self.rankPlayerCategories(player_B)

            player_data_A = player_A.returnPlayerData()
            player_data_B = player_B.returnPlayerData()

            df = pd.DataFrame([player_data_A, player_data_B], columns = column_headers)


            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            pd.set_option('display.colheader_justify', 'center')
            pd.set_option('display.precision', 3)

            display(df)
            

            labels = ['FG', '3s', 'FT%',
                      'Ast', 'Stl', 'Blk',
                      'TOV', 'TRB', 'Pts',
                      'Dbl', 'Avg Rank']
            
            x = np.arange(len(labels))                                   # the labels
            width = 0.25                                                 # the width of the bars

            self.matPlotFigure = plt.subplots()

            fig, ax = self.matPlotFigure

            rects1 = ax.bar(x - width/2, player_A_ranks, width, label = player_A.player)
            rects2 = ax.bar(x + width/2, player_B_ranks, width, label = player_B.player)
            
            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_ylabel('Relative Positition in the League')
            ax.set_title(player_A.player + ' vs. ' + player_B.player)
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.legend()
          


            self.autolabel(rects1, ax)
            self.autolabel(rects2, ax)

            fig.tight_layout()
            plt.show()

      def autolabel(self, rects, ax):
            """Attach a text label above each bar in *rects*, thus displaying its height."""
          
            for rect in rects:
                  height = rect.get_height()
                  ax.annotate('{}'.format(height),
                              xy=(rect.get_x() + rect.get_width() / 2, height),
                              xytext=(0, 3),  # 3 points vertical offset
                              textcoords="offset points",
                              ha='center',
                              va='bottom')

      def printTeamRosters(self, Data_Center):



            # print off every teams roster, and their players rank
            b = Data_Center.getTeamData()
            d = Data_Center.getAllPlayerData().getDict()

            # this calculates the mean total of the league:
            total_ranks = []
            for player in d:
                  if player.total_rank == None:
                        pass
                  else:
                        total_ranks.append(player.total_rank)
                
            mean = sum(total_ranks) / len(total_ranks)

            # this iterates over every Fantasy team:
            for team, v in b.items():
                  #print(team)
                  #print(v)
                  roster = v[1]
                  to_print = []
                  tally = []

                  # this iterates over every player found in each Fantasy team
                  for player in roster:
                        try:
                              tally.append(player.total_rank)
                        except:
                              pass

                  try:
                        avg_rank = sum(tally) / len(tally)
                        print(team, round(avg_rank, 2))
                    
                  except:
                        av_rank = 'Average Ranke NOT tallied yet'
                        print(av_rank)

                  toPrint = True

                  if (toPrint):
                        for player in roster:
                              try:
                                    print('\t', player.player, '-', player.total_rank, '-', player.position)
                              except:
                                    pass


                
                
