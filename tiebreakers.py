
import numpy as np
import pandas as pd
import random
from collections import Counter
import json
from supabase import create_client, Client
import os


#supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))
supabase = create_client("https://gypbjlbuznipjrvbhlbg.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5cGJqbGJ1em5pcGpydmJobGJnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjY1NzUzNywiZXhwIjoyMDcyMjMzNTM3fQ.eIAQmlvcQQm9oP8E54XE2-Ez3WduDINtD_U3s51_YK8")

# Load team map
# Fetch team map from Supabase
team_map_data = supabase.table('Teams').select('teamId, displayName').execute()
teamMap = pd.DataFrame(team_map_data.data)
teamMap.columns = ['teamId', 'teamName']  # Match existing column names


class Team:
    def __init__(self, name, conference, division, g1, g1result, g2, g2result, g3, g3result,
                 g4, g4result, g5, g5result, g6, g6result, g7, g7result, g8, g8result, g9, g9result, g10, g10result,
                 g11, g11result, g12, g12result, g13, g13result, g14, g14result, g15, g15result, g16, g16result,
                 g17, g17result):
        self.name = name
        self.conference = conference
        self.division = division
        self.g1 = g1
        self.g2 = g2
        self.g3 = g3
        self.g4 = g4
        self.g5 = g5
        self.g6 = g6
        self.g7 = g7
        self.g8 = g8
        self.g9 = g9
        self.g10 = g10
        self.g11 = g11
        self.g12 = g12
        self.g13 = g13
        self.g14 = g14
        self.g15 = g15
        self.g16 = g16
        self.g17 = g17
        self.g1result = g1result
        self.g2result = g2result
        self.g3result = g3result
        self.g4result = g4result
        self.g5result = g5result
        self.g6result = g6result
        self.g7result = g7result
        self.g8result = g8result
        self.g9result = g9result
        self.g10result = g10result
        self.g11result = g11result
        self.g12result = g12result
        self.g13result = g13result
        self.g14result = g14result
        self.g15result = g15result
        self.g16result = g16result
        self.g17result = g17result

        self.matchups = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17]
        self.results = [g1result, g2result, g3result, g4result, g5result, g6result, g7result, g8result, g9result,
                        g10result, g11result, g12result, g13result, g14result, g15result, g16result, g17result]

    def getName(self):
        return self.name

    def getConference(self):
        return self.conference

    def getDivision(self):
        return self.division

    def getWins(self):
        return (self.results.count('W'))

    def getLosses(self):
        return (self.results.count('L'))

    def getWinPercentage(self):
        winPercentage = float(self.results.count('W')) / (self.results.count('W') + self.results.count('L'))
        return (winPercentage)



# Fetch games from Supabase
games_data = supabase.table('Games').select('homeTeamId, awayTeamId, homeScore, awayScore', 'scheduleId').filter('stageIndex', 'neq', 0).filter('weekIndex', 'lte', 17).execute()
games_df = pd.DataFrame(games_data.data)

# Map IDs to names using teamMap
games_df['homeTeam'] = games_df['homeTeamId'].map(dict(zip(teamMap['teamId'], teamMap['teamName'])))
games_df['awayTeam'] = games_df['awayTeamId'].map(dict(zip(teamMap['teamId'], teamMap['teamName'])))
games_df = games_df.drop(['homeTeamId', 'awayTeamId'], axis=1)  # Drop ID columns

df = games_df  # Now df has name-based columns like original CSV


count = 0


def fillSchedules(df):
    global Bills, Dolphins, Jets, Patriots, Bengals, Browns, Ravens, Steelers, Colts, Jaguars, Titans, Texans, Broncos, Chiefs, Chargers, Raiders, Commanders, Cowboys, Giants, Eagles, Bears, Lions, Packers, Vikings, Buccaneers, Falcons, Saints, Panthers, Niners, Cardinals, Rams, Seahawks
    #print object id of Bills
    global count
    if (count == 0): 

        bills_data = df[(df['homeTeam'] == 'Bills') | (df['awayTeam'] == 'Bills')]

        bills_schedule = []
        for index, row in bills_data.iterrows():
            if (row['homeTeam'] == 'Bills'):
                bills_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Bills'):
                bills_schedule.append(row['homeTeam'])

        bills_schedule_results = []
        for index, row in bills_data.iterrows():
            if (row['homeTeam'] == 'Bills' and row['homeScore'] > row['awayScore']):
                bills_schedule_results.append('W')
            elif (row['awayTeam'] == 'Bills' and row['awayScore'] > row['homeScore']):
                bills_schedule_results.append('W')
            elif (row['homeTeam'] == 'Bills' and row['homeScore'] < row['awayScore']):
                bills_schedule_results.append('L')
            elif (row['awayTeam'] == 'Bills' and row['awayScore'] < row['homeScore']):
                bills_schedule_results.append('L')
            elif (row['awayTeam'] == 'Bills' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                bills_schedule_results.append('T')
            elif (row['homeTeam'] == 'Bills' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                bills_schedule_results.append('T')
            else:
                bills_schedule_results.append('NA')


        Bills = Team('Bills', 'AFC', 'AFCE', bills_schedule[0], bills_schedule_results[0], bills_schedule[1],
                    bills_schedule_results[1], bills_schedule[2], bills_schedule_results[2], bills_schedule[3],
                    bills_schedule_results[3],
                    bills_schedule[4], bills_schedule_results[4], bills_schedule[5], bills_schedule_results[5],
                    bills_schedule[6],
                    bills_schedule_results[6], bills_schedule[7], bills_schedule_results[7], bills_schedule[8],
                    bills_schedule_results[8],
                    bills_schedule[9], bills_schedule_results[9], bills_schedule[10], bills_schedule_results[10],
                    bills_schedule[11],
                    bills_schedule_results[11], bills_schedule[12], bills_schedule_results[12], bills_schedule[13],
                    bills_schedule_results[13],
                    bills_schedule[14], bills_schedule_results[14], bills_schedule[15], bills_schedule_results[15],
                    bills_schedule[16],
                    bills_schedule_results[16])
        print(id(Bills))

        dolphins_data = df[(df['homeTeam'] == 'Dolphins') | (df['awayTeam'] == 'Dolphins')]

        dolphins_schedule = []
        for index, row in dolphins_data.iterrows():
            if (row['homeTeam'] == 'Dolphins'):
                dolphins_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Dolphins'):
                dolphins_schedule.append(row['homeTeam'])

        dolphins_schedule_results = []
        for index, row in dolphins_data.iterrows():
            if (row['homeTeam'] == 'Dolphins' and row['homeScore'] > row['awayScore']):
                dolphins_schedule_results.append('W')
            elif (row['awayTeam'] == 'Dolphins' and row['awayScore'] > row['homeScore']):
                dolphins_schedule_results.append('W')
            elif (row['homeTeam'] == 'Dolphins' and row['homeScore'] < row['awayScore']):
                dolphins_schedule_results.append('L')
            elif (row['awayTeam'] == 'Dolphins' and row['awayScore'] < row['homeScore']):
                dolphins_schedule_results.append('L')
            elif (row['awayTeam'] == 'Dolphins' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                dolphins_schedule_results.append('T')
            elif (row['homeTeam'] == 'Dolphins' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                dolphins_schedule_results.append('T')
            else:
                dolphins_schedule_results.append('NA')

        Dolphins = Team('Dolphins', 'AFC', 'AFCE', dolphins_schedule[0], dolphins_schedule_results[0], dolphins_schedule[1],
                        dolphins_schedule_results[1], dolphins_schedule[2], dolphins_schedule_results[2], dolphins_schedule[3],
                        dolphins_schedule_results[3],
                        dolphins_schedule[4], dolphins_schedule_results[4], dolphins_schedule[5], dolphins_schedule_results[5],
                        dolphins_schedule[6],
                        dolphins_schedule_results[6], dolphins_schedule[7], dolphins_schedule_results[7], dolphins_schedule[8],
                        dolphins_schedule_results[8],
                        dolphins_schedule[9], dolphins_schedule_results[9], dolphins_schedule[10],
                        dolphins_schedule_results[10], dolphins_schedule[11],
                        dolphins_schedule_results[11], dolphins_schedule[12], dolphins_schedule_results[12],
                        dolphins_schedule[13], dolphins_schedule_results[13],
                        dolphins_schedule[14], dolphins_schedule_results[14], dolphins_schedule[15],
                        dolphins_schedule_results[15], dolphins_schedule[16],
                        dolphins_schedule_results[16])

        jets_data = df[(df['homeTeam'] == 'Jets') | (df['awayTeam'] == 'Jets')]

        jets_schedule = []
        for index, row in jets_data.iterrows():
            if (row['homeTeam'] == 'Jets'):
                jets_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Jets'):
                jets_schedule.append(row['homeTeam'])

        jets_schedule_results = []
        for index, row in jets_data.iterrows():
            if (row['homeTeam'] == 'Jets' and row['homeScore'] > row['awayScore']):
                jets_schedule_results.append('W')
            elif (row['awayTeam'] == 'Jets' and row['awayScore'] > row['homeScore']):
                jets_schedule_results.append('W')
            elif (row['homeTeam'] == 'Jets' and row['homeScore'] < row['awayScore']):
                jets_schedule_results.append('L')
            elif (row['awayTeam'] == 'Jets' and row['awayScore'] < row['homeScore']):
                jets_schedule_results.append('L')
            elif (row['awayTeam'] == 'Jets' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                jets_schedule_results.append('T')
            elif (row['homeTeam'] == 'Jets' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                jets_schedule_results.append('T')
            else:
                jets_schedule_results.append('NA')

        Jets = Team('Jets', 'AFC', 'AFCE', jets_schedule[0], jets_schedule_results[0], jets_schedule[1],
                    jets_schedule_results[1], jets_schedule[2], jets_schedule_results[2], jets_schedule[3],
                    jets_schedule_results[3],
                    jets_schedule[4], jets_schedule_results[4], jets_schedule[5], jets_schedule_results[5], jets_schedule[6],
                    jets_schedule_results[6], jets_schedule[7], jets_schedule_results[7], jets_schedule[8],
                    jets_schedule_results[8],
                    jets_schedule[9], jets_schedule_results[9], jets_schedule[10], jets_schedule_results[10], jets_schedule[11],
                    jets_schedule_results[11], jets_schedule[12], jets_schedule_results[12], jets_schedule[13],
                    jets_schedule_results[13],
                    jets_schedule[14], jets_schedule_results[14], jets_schedule[15], jets_schedule_results[15],
                    jets_schedule[16],
                    jets_schedule_results[16])

        patriots_data = df[(df['homeTeam'] == 'Patriots') | (df['awayTeam'] == 'Patriots')]

        patriots_schedule = []
        for index, row in patriots_data.iterrows():
            if (row['homeTeam'] == 'Patriots'):
                patriots_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Patriots'):
                patriots_schedule.append(row['homeTeam'])

        patriots_schedule_results = []
        for index, row in patriots_data.iterrows():
            if (row['homeTeam'] == 'Patriots' and row['homeScore'] > row['awayScore']):
                patriots_schedule_results.append('W')
            elif (row['awayTeam'] == 'Patriots' and row['awayScore'] > row['homeScore']):
                patriots_schedule_results.append('W')
            elif (row['homeTeam'] == 'Patriots' and row['homeScore'] < row['awayScore']):
                patriots_schedule_results.append('L')
            elif (row['awayTeam'] == 'Patriots' and row['awayScore'] < row['homeScore']):
                patriots_schedule_results.append('L')
            elif (row['awayTeam'] == 'Patriots' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                patriots_schedule_results.append('T')
            elif (row['homeTeam'] == 'Patriots' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                patriots_schedule_results.append('T')
            else:
                patriots_schedule_results.append('NA')

        Patriots = Team('Patriots', 'AFC', 'AFCE', patriots_schedule[0], patriots_schedule_results[0], patriots_schedule[1],
                        patriots_schedule_results[1], patriots_schedule[2], patriots_schedule_results[2], patriots_schedule[3],
                        patriots_schedule_results[3],
                        patriots_schedule[4], patriots_schedule_results[4], patriots_schedule[5], patriots_schedule_results[5],
                        patriots_schedule[6],
                        patriots_schedule_results[6], patriots_schedule[7], patriots_schedule_results[7], patriots_schedule[8],
                        patriots_schedule_results[8],
                        patriots_schedule[9], patriots_schedule_results[9], patriots_schedule[10],
                        patriots_schedule_results[10], patriots_schedule[11],
                        patriots_schedule_results[11], patriots_schedule[12], patriots_schedule_results[12],
                        patriots_schedule[13], patriots_schedule_results[13],
                        patriots_schedule[14], patriots_schedule_results[14], patriots_schedule[15],
                        patriots_schedule_results[15], patriots_schedule[16],
                        patriots_schedule_results[16])

        bengals_data = df[(df['homeTeam'] == 'Bengals') | (df['awayTeam'] == 'Bengals')]

        bengals_schedule = []
        for index, row in bengals_data.iterrows():
            if (row['homeTeam'] == 'Bengals'):
                bengals_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Bengals'):
                bengals_schedule.append(row['homeTeam'])

        bengals_schedule_results = []
        for index, row in bengals_data.iterrows():
            if (row['homeTeam'] == 'Bengals' and row['homeScore'] > row['awayScore']):
                bengals_schedule_results.append('W')
            elif (row['awayTeam'] == 'Bengals' and row['awayScore'] > row['homeScore']):
                bengals_schedule_results.append('W')
            elif (row['homeTeam'] == 'Bengals' and row['homeScore'] < row['awayScore']):
                bengals_schedule_results.append('L')
            elif (row['awayTeam'] == 'Bengals' and row['awayScore'] < row['homeScore']):
                bengals_schedule_results.append('L')
            elif (row['awayTeam'] == 'Bengals' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                bengals_schedule_results.append('T')
            elif (row['homeTeam'] == 'Bengals' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                bengals_schedule_results.append('T')
            else:
                bengals_schedule_results.append('NA')

        Bengals = Team('Bengals', 'AFC', 'AFCN', bengals_schedule[0], bengals_schedule_results[0], bengals_schedule[1],
                    bengals_schedule_results[1], bengals_schedule[2], bengals_schedule_results[2], bengals_schedule[3],
                    bengals_schedule_results[3],
                    bengals_schedule[4], bengals_schedule_results[4], bengals_schedule[5], bengals_schedule_results[5],
                    bengals_schedule[6],
                    bengals_schedule_results[6], bengals_schedule[7], bengals_schedule_results[7], bengals_schedule[8],
                    bengals_schedule_results[8],
                    bengals_schedule[9], bengals_schedule_results[9], bengals_schedule[10], bengals_schedule_results[10],
                    bengals_schedule[11],
                    bengals_schedule_results[11], bengals_schedule[12], bengals_schedule_results[12], bengals_schedule[13],
                    bengals_schedule_results[13],
                    bengals_schedule[14], bengals_schedule_results[14], bengals_schedule[15], bengals_schedule_results[15],
                    bengals_schedule[16],
                    bengals_schedule_results[16])

        browns_data = df[(df['homeTeam'] == 'Browns') | (df['awayTeam'] == 'Browns')]

        browns_schedule = []
        for index, row in browns_data.iterrows():
            if (row['homeTeam'] == 'Browns'):
                browns_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Browns'):
                browns_schedule.append(row['homeTeam'])

        browns_schedule_results = []
        for index, row in browns_data.iterrows():
            if (row['homeTeam'] == 'Browns' and row['homeScore'] > row['awayScore']):
                browns_schedule_results.append('W')
            elif (row['awayTeam'] == 'Browns' and row['awayScore'] > row['homeScore']):
                browns_schedule_results.append('W')
            elif (row['homeTeam'] == 'Browns' and row['homeScore'] < row['awayScore']):
                browns_schedule_results.append('L')
            elif (row['awayTeam'] == 'Browns' and row['awayScore'] < row['homeScore']):
                browns_schedule_results.append('L')
            elif (row['awayTeam'] == 'Browns' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                browns_schedule_results.append('T')
            elif (row['homeTeam'] == 'Browns' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                browns_schedule_results.append('T')
            else:
                browns_schedule_results.append('NA')

        Browns = Team('Browns', 'AFC', 'AFCN', browns_schedule[0], browns_schedule_results[0], browns_schedule[1],
                    browns_schedule_results[1], browns_schedule[2], browns_schedule_results[2], browns_schedule[3],
                    browns_schedule_results[3],
                    browns_schedule[4], browns_schedule_results[4], browns_schedule[5], browns_schedule_results[5],
                    browns_schedule[6],
                    browns_schedule_results[6], browns_schedule[7], browns_schedule_results[7], browns_schedule[8],
                    browns_schedule_results[8],
                    browns_schedule[9], browns_schedule_results[9], browns_schedule[10], browns_schedule_results[10],
                    browns_schedule[11],
                    browns_schedule_results[11], browns_schedule[12], browns_schedule_results[12], browns_schedule[13],
                    browns_schedule_results[13],
                    browns_schedule[14], browns_schedule_results[14], browns_schedule[15], browns_schedule_results[15],
                    browns_schedule[16],
                    browns_schedule_results[16])

        ravens_data = df[(df['homeTeam'] == 'Ravens') | (df['awayTeam'] == 'Ravens')]

        ravens_schedule = []
        for index, row in ravens_data.iterrows():
            if (row['homeTeam'] == 'Ravens'):
                ravens_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Ravens'):
                ravens_schedule.append(row['homeTeam'])

        ravens_schedule_results = []
        for index, row in ravens_data.iterrows():
            if (row['homeTeam'] == 'Ravens' and row['homeScore'] > row['awayScore']):
                ravens_schedule_results.append('W')
            elif (row['awayTeam'] == 'Ravens' and row['awayScore'] > row['homeScore']):
                ravens_schedule_results.append('W')
            elif (row['homeTeam'] == 'Ravens' and row['homeScore'] < row['awayScore']):
                ravens_schedule_results.append('L')
            elif (row['awayTeam'] == 'Ravens' and row['awayScore'] < row['homeScore']):
                ravens_schedule_results.append('L')
            elif (row['awayTeam'] == 'Ravens' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                ravens_schedule_results.append('T')
            elif (row['homeTeam'] == 'Ravens' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                ravens_schedule_results.append('T')
            else:
                ravens_schedule_results.append('NA')

        Ravens = Team('Ravens', 'AFC', 'AFCN', ravens_schedule[0], ravens_schedule_results[0], ravens_schedule[1],
                    ravens_schedule_results[1], ravens_schedule[2], ravens_schedule_results[2], ravens_schedule[3],
                    ravens_schedule_results[3],
                    ravens_schedule[4], ravens_schedule_results[4], ravens_schedule[5], ravens_schedule_results[5],
                    ravens_schedule[6],
                    ravens_schedule_results[6], ravens_schedule[7], ravens_schedule_results[7], ravens_schedule[8],
                    ravens_schedule_results[8],
                    ravens_schedule[9], ravens_schedule_results[9], ravens_schedule[10], ravens_schedule_results[10],
                    ravens_schedule[11],
                    ravens_schedule_results[11], ravens_schedule[12], ravens_schedule_results[12], ravens_schedule[13],
                    ravens_schedule_results[13],
                    ravens_schedule[14], ravens_schedule_results[14], ravens_schedule[15], ravens_schedule_results[15],
                    ravens_schedule[16],
                    ravens_schedule_results[16])

        steelers_data = df[(df['homeTeam'] == 'Steelers') | (df['awayTeam'] == 'Steelers')]

        steelers_schedule = []
        for index, row in steelers_data.iterrows():
            if (row['homeTeam'] == 'Steelers'):
                steelers_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Steelers'):
                steelers_schedule.append(row['homeTeam'])

        steelers_schedule_results = []
        for index, row in steelers_data.iterrows():
            if (row['homeTeam'] == 'Steelers' and row['homeScore'] > row['awayScore']):
                steelers_schedule_results.append('W')
            elif (row['awayTeam'] == 'Steelers' and row['awayScore'] > row['homeScore']):
                steelers_schedule_results.append('W')
            elif (row['homeTeam'] == 'Steelers' and row['homeScore'] < row['awayScore']):
                steelers_schedule_results.append('L')
            elif (row['awayTeam'] == 'Steelers' and row['awayScore'] < row['homeScore']):
                steelers_schedule_results.append('L')
            elif (row['awayTeam'] == 'Steelers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                steelers_schedule_results.append('T')
            elif (row['homeTeam'] == 'Steelers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                steelers_schedule_results.append('T')
            else:
                steelers_schedule_results.append('NA')

        Steelers = Team('Steelers', 'AFC', 'AFCN', steelers_schedule[0], steelers_schedule_results[0], steelers_schedule[1],
                        steelers_schedule_results[1], steelers_schedule[2], steelers_schedule_results[2], steelers_schedule[3],
                        steelers_schedule_results[3],
                        steelers_schedule[4], steelers_schedule_results[4], steelers_schedule[5], steelers_schedule_results[5],
                        steelers_schedule[6],
                        steelers_schedule_results[6], steelers_schedule[7], steelers_schedule_results[7], steelers_schedule[8],
                        steelers_schedule_results[8],
                        steelers_schedule[9], steelers_schedule_results[9], steelers_schedule[10],
                        steelers_schedule_results[10], steelers_schedule[11],
                        steelers_schedule_results[11], steelers_schedule[12], steelers_schedule_results[12],
                        steelers_schedule[13], steelers_schedule_results[13],
                        steelers_schedule[14], steelers_schedule_results[14], steelers_schedule[15],
                        steelers_schedule_results[15], steelers_schedule[16],
                        steelers_schedule_results[16])

        colts_data = df[(df['homeTeam'] == 'Colts') | (df['awayTeam'] == 'Colts')]

        colts_schedule = []
        for index, row in colts_data.iterrows():
            if (row['homeTeam'] == 'Colts'):
                colts_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Colts'):
                colts_schedule.append(row['homeTeam'])

        colts_schedule_results = []
        for index, row in colts_data.iterrows():
            if (row['homeTeam'] == 'Colts' and row['homeScore'] > row['awayScore']):
                colts_schedule_results.append('W')
            elif (row['awayTeam'] == 'Colts' and row['awayScore'] > row['homeScore']):
                colts_schedule_results.append('W')
            elif (row['homeTeam'] == 'Colts' and row['homeScore'] < row['awayScore']):
                colts_schedule_results.append('L')
            elif (row['awayTeam'] == 'Colts' and row['awayScore'] < row['homeScore']):
                colts_schedule_results.append('L')
            elif (row['awayTeam'] == 'Colts' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                colts_schedule_results.append('T')
            elif (row['homeTeam'] == 'Colts' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                colts_schedule_results.append('T')
            else:
                colts_schedule_results.append('NA')

        Colts = Team('Colts', 'AFC', 'AFCS', colts_schedule[0], colts_schedule_results[0], colts_schedule[1],
                    colts_schedule_results[1], colts_schedule[2], colts_schedule_results[2], colts_schedule[3],
                    colts_schedule_results[3],
                    colts_schedule[4], colts_schedule_results[4], colts_schedule[5], colts_schedule_results[5],
                    colts_schedule[6],
                    colts_schedule_results[6], colts_schedule[7], colts_schedule_results[7], colts_schedule[8],
                    colts_schedule_results[8],
                    colts_schedule[9], colts_schedule_results[9], colts_schedule[10], colts_schedule_results[10],
                    colts_schedule[11],
                    colts_schedule_results[11], colts_schedule[12], colts_schedule_results[12], colts_schedule[13],
                    colts_schedule_results[13],
                    colts_schedule[14], colts_schedule_results[14], colts_schedule[15], colts_schedule_results[15],
                    colts_schedule[16],
                    colts_schedule_results[16])

        jaguars_data = df[(df['homeTeam'] == 'Jaguars') | (df['awayTeam'] == 'Jaguars')]

        jaguars_schedule = []
        for index, row in jaguars_data.iterrows():
            if (row['homeTeam'] == 'Jaguars'):
                jaguars_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Jaguars'):
                jaguars_schedule.append(row['homeTeam'])

        jaguars_schedule_results = []
        for index, row in jaguars_data.iterrows():
            if (row['homeTeam'] == 'Jaguars' and row['homeScore'] > row['awayScore']):
                jaguars_schedule_results.append('W')
            elif (row['awayTeam'] == 'Jaguars' and row['awayScore'] > row['homeScore']):
                jaguars_schedule_results.append('W')
            elif (row['homeTeam'] == 'Jaguars' and row['homeScore'] < row['awayScore']):
                jaguars_schedule_results.append('L')
            elif (row['awayTeam'] == 'Jaguars' and row['awayScore'] < row['homeScore']):
                jaguars_schedule_results.append('L')
            elif (row['awayTeam'] == 'Jaguars' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                jaguars_schedule_results.append('T')
            elif (row['homeTeam'] == 'Jaguars' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                jaguars_schedule_results.append('T')
            else:
                jaguars_schedule_results.append('NA')

        Jaguars = Team('Jaguars', 'AFC', 'AFCS', jaguars_schedule[0], jaguars_schedule_results[0], jaguars_schedule[1],
                    jaguars_schedule_results[1], jaguars_schedule[2], jaguars_schedule_results[2], jaguars_schedule[3],
                    jaguars_schedule_results[3],
                    jaguars_schedule[4], jaguars_schedule_results[4], jaguars_schedule[5], jaguars_schedule_results[5],
                    jaguars_schedule[6],
                    jaguars_schedule_results[6], jaguars_schedule[7], jaguars_schedule_results[7], jaguars_schedule[8],
                    jaguars_schedule_results[8],
                    jaguars_schedule[9], jaguars_schedule_results[9], jaguars_schedule[10], jaguars_schedule_results[10],
                    jaguars_schedule[11],
                    jaguars_schedule_results[11], jaguars_schedule[12], jaguars_schedule_results[12], jaguars_schedule[13],
                    jaguars_schedule_results[13],
                    jaguars_schedule[14], jaguars_schedule_results[14], jaguars_schedule[15], jaguars_schedule_results[15],
                    jaguars_schedule[16],
                    jaguars_schedule_results[16])

        titans_data = df[(df['homeTeam'] == 'Titans') | (df['awayTeam'] == 'Titans')]

        titans_schedule = []
        for index, row in titans_data.iterrows():
            if (row['homeTeam'] == 'Titans'):
                titans_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Titans'):
                titans_schedule.append(row['homeTeam'])

        titans_schedule_results = []
        for index, row in titans_data.iterrows():
            if (row['homeTeam'] == 'Titans' and row['homeScore'] > row['awayScore']):
                titans_schedule_results.append('W')
            elif (row['awayTeam'] == 'Titans' and row['awayScore'] > row['homeScore']):
                titans_schedule_results.append('W')
            elif (row['homeTeam'] == 'Titans' and row['homeScore'] < row['awayScore']):
                titans_schedule_results.append('L')
            elif (row['awayTeam'] == 'Titans' and row['awayScore'] < row['homeScore']):
                titans_schedule_results.append('L')
            elif (row['awayTeam'] == 'Titans' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                titans_schedule_results.append('T')
            elif (row['homeTeam'] == 'Titans' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                titans_schedule_results.append('T')
            else:
                titans_schedule_results.append('NA')

        Titans = Team('Titans', 'AFC', 'AFCS', titans_schedule[0], titans_schedule_results[0], titans_schedule[1],
                    titans_schedule_results[1], titans_schedule[2], titans_schedule_results[2], titans_schedule[3],
                    titans_schedule_results[3],
                    titans_schedule[4], titans_schedule_results[4], titans_schedule[5], titans_schedule_results[5],
                    titans_schedule[6],
                    titans_schedule_results[6], titans_schedule[7], titans_schedule_results[7], titans_schedule[8],
                    titans_schedule_results[8],
                    titans_schedule[9], titans_schedule_results[9], titans_schedule[10], titans_schedule_results[10],
                    titans_schedule[11],
                    titans_schedule_results[11], titans_schedule[12], titans_schedule_results[12], titans_schedule[13],
                    titans_schedule_results[13],
                    titans_schedule[14], titans_schedule_results[14], titans_schedule[15], titans_schedule_results[15],
                    titans_schedule[16],
                    titans_schedule_results[16])

        texans_data = df[(df['homeTeam'] == 'Texans') | (df['awayTeam'] == 'Texans')]

        texans_schedule = []
        for index, row in texans_data.iterrows():
            if (row['homeTeam'] == 'Texans'):
                texans_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Texans'):
                texans_schedule.append(row['homeTeam'])

        texans_schedule_results = []
        for index, row in texans_data.iterrows():
            if (row['homeTeam'] == 'Texans' and row['homeScore'] > row['awayScore']):
                texans_schedule_results.append('W')
            elif (row['awayTeam'] == 'Texans' and row['awayScore'] > row['homeScore']):
                texans_schedule_results.append('W')
            elif (row['homeTeam'] == 'Texans' and row['homeScore'] < row['awayScore']):
                texans_schedule_results.append('L')
            elif (row['awayTeam'] == 'Texans' and row['awayScore'] < row['homeScore']):
                texans_schedule_results.append('L')
            elif (row['awayTeam'] == 'Texans' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                texans_schedule_results.append('T')
            elif (row['homeTeam'] == 'Texans' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                texans_schedule_results.append('T')
            else:
                texans_schedule_results.append('NA')

        Texans = Team('Texans', 'AFC', 'AFCS', texans_schedule[0], texans_schedule_results[0], texans_schedule[1],
                    texans_schedule_results[1], texans_schedule[2], texans_schedule_results[2], texans_schedule[3],
                    texans_schedule_results[3],
                    texans_schedule[4], texans_schedule_results[4], texans_schedule[5], texans_schedule_results[5],
                    texans_schedule[6],
                    texans_schedule_results[6], texans_schedule[7], texans_schedule_results[7], texans_schedule[8],
                    texans_schedule_results[8],
                    texans_schedule[9], texans_schedule_results[9], texans_schedule[10], texans_schedule_results[10],
                    texans_schedule[11],
                    texans_schedule_results[11], texans_schedule[12], texans_schedule_results[12], texans_schedule[13],
                    texans_schedule_results[13],
                    texans_schedule[14], texans_schedule_results[14], texans_schedule[15], texans_schedule_results[15],
                    texans_schedule[16],
                    texans_schedule_results[16])

        broncos_data = df[(df['homeTeam'] == 'Broncos') | (df['awayTeam'] == 'Broncos')]

        broncos_schedule = []
        for index, row in broncos_data.iterrows():
            if (row['homeTeam'] == 'Broncos'):
                broncos_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Broncos'):
                broncos_schedule.append(row['homeTeam'])

        broncos_schedule_results = []
        for index, row in broncos_data.iterrows():
            if (row['homeTeam'] == 'Broncos' and row['homeScore'] > row['awayScore']):
                broncos_schedule_results.append('W')
            elif (row['awayTeam'] == 'Broncos' and row['awayScore'] > row['homeScore']):
                broncos_schedule_results.append('W')
            elif (row['homeTeam'] == 'Broncos' and row['homeScore'] < row['awayScore']):
                broncos_schedule_results.append('L')
            elif (row['awayTeam'] == 'Broncos' and row['awayScore'] < row['homeScore']):
                broncos_schedule_results.append('L')
            elif (row['awayTeam'] == 'Broncos' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                broncos_schedule_results.append('T')
            elif (row['homeTeam'] == 'Broncos' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                broncos_schedule_results.append('T')
            else:
                broncos_schedule_results.append('NA')

        Broncos = Team('Broncos', 'AFC', 'AFCW', broncos_schedule[0], broncos_schedule_results[0], broncos_schedule[1],
                    broncos_schedule_results[1], broncos_schedule[2], broncos_schedule_results[2], broncos_schedule[3],
                    broncos_schedule_results[3],
                    broncos_schedule[4], broncos_schedule_results[4], broncos_schedule[5], broncos_schedule_results[5],
                    broncos_schedule[6],
                    broncos_schedule_results[6], broncos_schedule[7], broncos_schedule_results[7], broncos_schedule[8],
                    broncos_schedule_results[8],
                    broncos_schedule[9], broncos_schedule_results[9], broncos_schedule[10], broncos_schedule_results[10],
                    broncos_schedule[11],
                    broncos_schedule_results[11], broncos_schedule[12], broncos_schedule_results[12], broncos_schedule[13],
                    broncos_schedule_results[13],
                    broncos_schedule[14], broncos_schedule_results[14], broncos_schedule[15], broncos_schedule_results[15],
                    broncos_schedule[16],
                    broncos_schedule_results[16])

        chiefs_data = df[(df['homeTeam'] == 'Chiefs') | (df['awayTeam'] == 'Chiefs')]

        chiefs_schedule = []
        for index, row in chiefs_data.iterrows():
            if (row['homeTeam'] == 'Chiefs'):
                chiefs_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Chiefs'):
                chiefs_schedule.append(row['homeTeam'])

        chiefs_schedule_results = []
        for index, row in chiefs_data.iterrows():
            if (row['homeTeam'] == 'Chiefs' and row['homeScore'] > row['awayScore']):
                chiefs_schedule_results.append('W')
            elif (row['awayTeam'] == 'Chiefs' and row['awayScore'] > row['homeScore']):
                chiefs_schedule_results.append('W')
            elif (row['homeTeam'] == 'Chiefs' and row['homeScore'] < row['awayScore']):
                chiefs_schedule_results.append('L')
            elif (row['awayTeam'] == 'Chiefs' and row['awayScore'] < row['homeScore']):
                chiefs_schedule_results.append('L')
            elif (row['awayTeam'] == 'Chiefs' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                chiefs_schedule_results.append('T')
            elif (row['homeTeam'] == 'Chiefs' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                chiefs_schedule_results.append('T')
            else:
                chiefs_schedule_results.append('NA')

        Chiefs = Team('Chiefs', 'AFC', 'AFCW', chiefs_schedule[0], chiefs_schedule_results[0], chiefs_schedule[1],
                    chiefs_schedule_results[1], chiefs_schedule[2], chiefs_schedule_results[2], chiefs_schedule[3],
                    chiefs_schedule_results[3],
                    chiefs_schedule[4], chiefs_schedule_results[4], chiefs_schedule[5], chiefs_schedule_results[5],
                    chiefs_schedule[6],
                    chiefs_schedule_results[6], chiefs_schedule[7], chiefs_schedule_results[7], chiefs_schedule[8],
                    chiefs_schedule_results[8],
                    chiefs_schedule[9], chiefs_schedule_results[9], chiefs_schedule[10], chiefs_schedule_results[10],
                    chiefs_schedule[11],
                    chiefs_schedule_results[11], chiefs_schedule[12], chiefs_schedule_results[12], chiefs_schedule[13],
                    chiefs_schedule_results[13],
                    chiefs_schedule[14], chiefs_schedule_results[14], chiefs_schedule[15], chiefs_schedule_results[15],
                    chiefs_schedule[16],
                    chiefs_schedule_results[16])

        chargers_data = df[(df['homeTeam'] == 'Chargers') | (df['awayTeam'] == 'Chargers')]

        chargers_schedule = []
        for index, row in chargers_data.iterrows():
            if (row['homeTeam'] == 'Chargers'):
                chargers_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Chargers'):
                chargers_schedule.append(row['homeTeam'])

        chargers_schedule_results = []
        for index, row in chargers_data.iterrows():
            if (row['homeTeam'] == 'Chargers' and row['homeScore'] > row['awayScore']):
                chargers_schedule_results.append('W')
            elif (row['awayTeam'] == 'Chargers' and row['awayScore'] > row['homeScore']):
                chargers_schedule_results.append('W')
            elif (row['homeTeam'] == 'Chargers' and row['homeScore'] < row['awayScore']):
                chargers_schedule_results.append('L')
            elif (row['awayTeam'] == 'Chargers' and row['awayScore'] < row['homeScore']):
                chargers_schedule_results.append('L')
            elif (row['awayTeam'] == 'Chargers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                chargers_schedule_results.append('T')
            elif (row['homeTeam'] == 'Chargers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                chargers_schedule_results.append('T')
            else:
                chargers_schedule_results.append('NA')

        Chargers = Team('Chargers', 'AFC', 'AFCW', chargers_schedule[0], chargers_schedule_results[0], chargers_schedule[1],
                        chargers_schedule_results[1], chargers_schedule[2], chargers_schedule_results[2], chargers_schedule[3],
                        chargers_schedule_results[3],
                        chargers_schedule[4], chargers_schedule_results[4], chargers_schedule[5], chargers_schedule_results[5],
                        chargers_schedule[6],
                        chargers_schedule_results[6], chargers_schedule[7], chargers_schedule_results[7], chargers_schedule[8],
                        chargers_schedule_results[8],
                        chargers_schedule[9], chargers_schedule_results[9], chargers_schedule[10],
                        chargers_schedule_results[10], chargers_schedule[11],
                        chargers_schedule_results[11], chargers_schedule[12], chargers_schedule_results[12],
                        chargers_schedule[13], chargers_schedule_results[13],
                        chargers_schedule[14], chargers_schedule_results[14], chargers_schedule[15],
                        chargers_schedule_results[15], chargers_schedule[16],
                        chargers_schedule_results[16])

        raiders_data = df[(df['homeTeam'] == 'Raiders') | (df['awayTeam'] == 'Raiders')]

        raiders_schedule = []
        for index, row in raiders_data.iterrows():
            if (row['homeTeam'] == 'Raiders'):
                raiders_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Raiders'):
                raiders_schedule.append(row['homeTeam'])

        raiders_schedule_results = []
        for index, row in raiders_data.iterrows():
            if (row['homeTeam'] == 'Raiders' and row['homeScore'] > row['awayScore']):
                raiders_schedule_results.append('W')
            elif (row['awayTeam'] == 'Raiders' and row['awayScore'] > row['homeScore']):
                raiders_schedule_results.append('W')
            elif (row['homeTeam'] == 'Raiders' and row['homeScore'] < row['awayScore']):
                raiders_schedule_results.append('L')
            elif (row['awayTeam'] == 'Raiders' and row['awayScore'] < row['homeScore']):
                raiders_schedule_results.append('L')
            elif (row['awayTeam'] == 'Raiders' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                raiders_schedule_results.append('T')
            elif (row['homeTeam'] == 'Raiders' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                raiders_schedule_results.append('T')
            else:
                raiders_schedule_results.append('NA')

        Raiders = Team('Raiders', 'AFC', 'AFCW', raiders_schedule[0], raiders_schedule_results[0], raiders_schedule[1],
                    raiders_schedule_results[1], raiders_schedule[2], raiders_schedule_results[2], raiders_schedule[3],
                    raiders_schedule_results[3],
                    raiders_schedule[4], raiders_schedule_results[4], raiders_schedule[5], raiders_schedule_results[5],
                    raiders_schedule[6],
                    raiders_schedule_results[6], raiders_schedule[7], raiders_schedule_results[7], raiders_schedule[8],
                    raiders_schedule_results[8],
                    raiders_schedule[9], raiders_schedule_results[9], raiders_schedule[10], raiders_schedule_results[10],
                    raiders_schedule[11],
                    raiders_schedule_results[11], raiders_schedule[12], raiders_schedule_results[12], raiders_schedule[13],
                    raiders_schedule_results[13],
                    raiders_schedule[14], raiders_schedule_results[14], raiders_schedule[15], raiders_schedule_results[15],
                    raiders_schedule[16],
                    raiders_schedule_results[16])

        commanders_data = df[(df['homeTeam'] == 'Commanders') | (df['awayTeam'] == 'Commanders')]

        commanders_schedule = []
        for index, row in commanders_data.iterrows():
            if (row['homeTeam'] == 'Commanders'):
                commanders_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Commanders'):
                commanders_schedule.append(row['homeTeam'])

        commanders_schedule_results = []
        for index, row in commanders_data.iterrows():
            if (row['homeTeam'] == 'Commanders' and row['homeScore'] > row['awayScore']):
                commanders_schedule_results.append('W')
            elif (row['awayTeam'] == 'Commanders' and row['awayScore'] > row['homeScore']):
                commanders_schedule_results.append('W')
            elif (row['homeTeam'] == 'Commanders' and row['homeScore'] < row['awayScore']):
                commanders_schedule_results.append('L')
            elif (row['awayTeam'] == 'Commanders' and row['awayScore'] < row['homeScore']):
                commanders_schedule_results.append('L')
            elif (row['awayTeam'] == 'Commanders' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                commanders_schedule_results.append('T')
            elif (row['homeTeam'] == 'Commanders' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                commanders_schedule_results.append('T')
            else:
                commanders_schedule_results.append('NA')

        Commanders = Team('Commanders', 'NFC', 'NFCE', commanders_schedule[0], commanders_schedule_results[0],
                        commanders_schedule[1],
                        commanders_schedule_results[1], commanders_schedule[2], commanders_schedule_results[2],
                        commanders_schedule[3], commanders_schedule_results[3],
                        commanders_schedule[4], commanders_schedule_results[4], commanders_schedule[5],
                        commanders_schedule_results[5], commanders_schedule[6],
                        commanders_schedule_results[6], commanders_schedule[7], commanders_schedule_results[7],
                        commanders_schedule[8], commanders_schedule_results[8],
                        commanders_schedule[9], commanders_schedule_results[9], commanders_schedule[10],
                        commanders_schedule_results[10], commanders_schedule[11],
                        commanders_schedule_results[11], commanders_schedule[12], commanders_schedule_results[12],
                        commanders_schedule[13], commanders_schedule_results[13],
                        commanders_schedule[14], commanders_schedule_results[14], commanders_schedule[15],
                        commanders_schedule_results[15], commanders_schedule[16],
                        commanders_schedule_results[16])

        cowboys_data = df[(df['homeTeam'] == 'Cowboys') | (df['awayTeam'] == 'Cowboys')]

        cowboys_schedule = []
        for index, row in cowboys_data.iterrows():
            if (row['homeTeam'] == 'Cowboys'):
                cowboys_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Cowboys'):
                cowboys_schedule.append(row['homeTeam'])

        cowboys_schedule_results = []
        for index, row in cowboys_data.iterrows():
            if (row['homeTeam'] == 'Cowboys' and row['homeScore'] > row['awayScore']):
                cowboys_schedule_results.append('W')
            elif (row['awayTeam'] == 'Cowboys' and row['awayScore'] > row['homeScore']):
                cowboys_schedule_results.append('W')
            elif (row['homeTeam'] == 'Cowboys' and row['homeScore'] < row['awayScore']):
                cowboys_schedule_results.append('L')
            elif (row['awayTeam'] == 'Cowboys' and row['awayScore'] < row['homeScore']):
                cowboys_schedule_results.append('L')
            elif (row['awayTeam'] == 'Cowboys' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                cowboys_schedule_results.append('T')
            elif (row['homeTeam'] == 'Cowboys' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                cowboys_schedule_results.append('T')
            else:
                cowboys_schedule_results.append('NA')

        Cowboys = Team('Cowboys', 'NFC', 'NFCE', cowboys_schedule[0], cowboys_schedule_results[0], cowboys_schedule[1],
                    cowboys_schedule_results[1], cowboys_schedule[2], cowboys_schedule_results[2], cowboys_schedule[3],
                    cowboys_schedule_results[3],
                    cowboys_schedule[4], cowboys_schedule_results[4], cowboys_schedule[5], cowboys_schedule_results[5],
                    cowboys_schedule[6],
                    cowboys_schedule_results[6], cowboys_schedule[7], cowboys_schedule_results[7], cowboys_schedule[8],
                    cowboys_schedule_results[8],
                    cowboys_schedule[9], cowboys_schedule_results[9], cowboys_schedule[10], cowboys_schedule_results[10],
                    cowboys_schedule[11],
                    cowboys_schedule_results[11], cowboys_schedule[12], cowboys_schedule_results[12], cowboys_schedule[13],
                    cowboys_schedule_results[13],
                    cowboys_schedule[14], cowboys_schedule_results[14], cowboys_schedule[15], cowboys_schedule_results[15],
                    cowboys_schedule[16],
                    cowboys_schedule_results[16])

        giants_data = df[(df['homeTeam'] == 'Giants') | (df['awayTeam'] == 'Giants')]

        giants_schedule = []
        for index, row in giants_data.iterrows():
            if (row['homeTeam'] == 'Giants'):
                giants_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Giants'):
                giants_schedule.append(row['homeTeam'])

        giants_schedule_results = []
        for index, row in giants_data.iterrows():
            if (row['homeTeam'] == 'Giants' and row['homeScore'] > row['awayScore']):
                giants_schedule_results.append('W')
            elif (row['awayTeam'] == 'Giants' and row['awayScore'] > row['homeScore']):
                giants_schedule_results.append('W')
            elif (row['homeTeam'] == 'Giants' and row['homeScore'] < row['awayScore']):
                giants_schedule_results.append('L')
            elif (row['awayTeam'] == 'Giants' and row['awayScore'] < row['homeScore']):
                giants_schedule_results.append('L')
            elif (row['awayTeam'] == 'Giants' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                giants_schedule_results.append('T')
            elif (row['homeTeam'] == 'Giants' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                giants_schedule_results.append('T')
            else:
                giants_schedule_results.append('NA')

        Giants = Team('Giants', 'NFC', 'NFCE', giants_schedule[0], giants_schedule_results[0], giants_schedule[1],
                    giants_schedule_results[1], giants_schedule[2], giants_schedule_results[2], giants_schedule[3],
                    giants_schedule_results[3],
                    giants_schedule[4], giants_schedule_results[4], giants_schedule[5], giants_schedule_results[5],
                    giants_schedule[6],
                    giants_schedule_results[6], giants_schedule[7], giants_schedule_results[7], giants_schedule[8],
                    giants_schedule_results[8],
                    giants_schedule[9], giants_schedule_results[9], giants_schedule[10], giants_schedule_results[10],
                    giants_schedule[11],
                    giants_schedule_results[11], giants_schedule[12], giants_schedule_results[12], giants_schedule[13],
                    giants_schedule_results[13],
                    giants_schedule[14], giants_schedule_results[14], giants_schedule[15], giants_schedule_results[15],
                    giants_schedule[16],
                    giants_schedule_results[16])

        eagles_data = df[(df['homeTeam'] == 'Eagles') | (df['awayTeam'] == 'Eagles')]

        eagles_schedule = []
        for index, row in eagles_data.iterrows():
            if (row['homeTeam'] == 'Eagles'):
                eagles_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Eagles'):
                eagles_schedule.append(row['homeTeam'])

        eagles_schedule_results = []
        for index, row in eagles_data.iterrows():
            if (row['homeTeam'] == 'Eagles' and row['homeScore'] > row['awayScore']):
                eagles_schedule_results.append('W')
            elif (row['awayTeam'] == 'Eagles' and row['awayScore'] > row['homeScore']):
                eagles_schedule_results.append('W')
            elif (row['homeTeam'] == 'Eagles' and row['homeScore'] < row['awayScore']):
                eagles_schedule_results.append('L')
            elif (row['awayTeam'] == 'Eagles' and row['awayScore'] < row['homeScore']):
                eagles_schedule_results.append('L')
            elif (row['awayTeam'] == 'Eagles' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                eagles_schedule_results.append('T')
            elif (row['homeTeam'] == 'Eagles' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                eagles_schedule_results.append('T')
            else:
                eagles_schedule_results.append('NA')

        Eagles = Team('Eagles', 'NFC', 'NFCE', eagles_schedule[0], eagles_schedule_results[0], eagles_schedule[1],
                    eagles_schedule_results[1], eagles_schedule[2], eagles_schedule_results[2], eagles_schedule[3],
                    eagles_schedule_results[3],
                    eagles_schedule[4], eagles_schedule_results[4], eagles_schedule[5], eagles_schedule_results[5],
                    eagles_schedule[6],
                    eagles_schedule_results[6], eagles_schedule[7], eagles_schedule_results[7], eagles_schedule[8],
                    eagles_schedule_results[8],
                    eagles_schedule[9], eagles_schedule_results[9], eagles_schedule[10], eagles_schedule_results[10],
                    eagles_schedule[11],
                    eagles_schedule_results[11], eagles_schedule[12], eagles_schedule_results[12], eagles_schedule[13],
                    eagles_schedule_results[13],
                    eagles_schedule[14], eagles_schedule_results[14], eagles_schedule[15], eagles_schedule_results[15],
                    eagles_schedule[16],
                    eagles_schedule_results[16])

        bears_data = df[(df['homeTeam'] == 'Bears') | (df['awayTeam'] == 'Bears')]

        bears_schedule = []
        for index, row in bears_data.iterrows():
            if (row['homeTeam'] == 'Bears'):
                bears_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Bears'):
                bears_schedule.append(row['homeTeam'])

        bears_schedule_results = []
        for index, row in bears_data.iterrows():
            if (row['homeTeam'] == 'Bears' and row['homeScore'] > row['awayScore']):
                bears_schedule_results.append('W')
            elif (row['awayTeam'] == 'Bears' and row['awayScore'] > row['homeScore']):
                bears_schedule_results.append('W')
            elif (row['homeTeam'] == 'Bears' and row['homeScore'] < row['awayScore']):
                bears_schedule_results.append('L')
            elif (row['awayTeam'] == 'Bears' and row['awayScore'] < row['homeScore']):
                bears_schedule_results.append('L')
            elif (row['awayTeam'] == 'Bears' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                bears_schedule_results.append('T')
            elif (row['homeTeam'] == 'Bears' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                bears_schedule_results.append('T')
            else:
                bears_schedule_results.append('NA')

        Bears = Team('Bears', 'NFC', 'NFCN', bears_schedule[0], bears_schedule_results[0], bears_schedule[1],
                    bears_schedule_results[1], bears_schedule[2], bears_schedule_results[2], bears_schedule[3],
                    bears_schedule_results[3],
                    bears_schedule[4], bears_schedule_results[4], bears_schedule[5], bears_schedule_results[5],
                    bears_schedule[6],
                    bears_schedule_results[6], bears_schedule[7], bears_schedule_results[7], bears_schedule[8],
                    bears_schedule_results[8],
                    bears_schedule[9], bears_schedule_results[9], bears_schedule[10], bears_schedule_results[10],
                    bears_schedule[11],
                    bears_schedule_results[11], bears_schedule[12], bears_schedule_results[12], bears_schedule[13],
                    bears_schedule_results[13],
                    bears_schedule[14], bears_schedule_results[14], bears_schedule[15], bears_schedule_results[15],
                    bears_schedule[16],
                    bears_schedule_results[16])

        lions_data = df[(df['homeTeam'] == 'Lions') | (df['awayTeam'] == 'Lions')]

        lions_schedule = []
        for index, row in lions_data.iterrows():
            if (row['homeTeam'] == 'Lions'):
                lions_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Lions'):
                lions_schedule.append(row['homeTeam'])

        lions_schedule_results = []
        for index, row in lions_data.iterrows():
            if (row['homeTeam'] == 'Lions' and row['homeScore'] > row['awayScore']):
                lions_schedule_results.append('W')
            elif (row['awayTeam'] == 'Lions' and row['awayScore'] > row['homeScore']):
                lions_schedule_results.append('W')
            elif (row['homeTeam'] == 'Lions' and row['homeScore'] < row['awayScore']):
                lions_schedule_results.append('L')
            elif (row['awayTeam'] == 'Lions' and row['awayScore'] < row['homeScore']):
                lions_schedule_results.append('L')
            elif (row['awayTeam'] == 'Lions' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                lions_schedule_results.append('T')
            elif (row['homeTeam'] == 'Lions' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                lions_schedule_results.append('T')
            else:
                lions_schedule_results.append('NA')

        Lions = Team('Lions', 'NFC', 'NFCN', lions_schedule[0], lions_schedule_results[0], lions_schedule[1],
                    lions_schedule_results[1], lions_schedule[2], lions_schedule_results[2], lions_schedule[3],
                    lions_schedule_results[3],
                    lions_schedule[4], lions_schedule_results[4], lions_schedule[5], lions_schedule_results[5],
                    lions_schedule[6],
                    lions_schedule_results[6], lions_schedule[7], lions_schedule_results[7], lions_schedule[8],
                    lions_schedule_results[8],
                    lions_schedule[9], lions_schedule_results[9], lions_schedule[10], lions_schedule_results[10],
                    lions_schedule[11],
                    lions_schedule_results[11], lions_schedule[12], lions_schedule_results[12], lions_schedule[13],
                    lions_schedule_results[13],
                    lions_schedule[14], lions_schedule_results[14], lions_schedule[15], lions_schedule_results[15],
                    lions_schedule[16],
                    lions_schedule_results[16])

        packers_data = df[(df['homeTeam'] == 'Packers') | (df['awayTeam'] == 'Packers')]

        packers_schedule = []
        for index, row in packers_data.iterrows():
            if (row['homeTeam'] == 'Packers'):
                packers_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Packers'):
                packers_schedule.append(row['homeTeam'])

        packers_schedule_results = []
        for index, row in packers_data.iterrows():
            if (row['homeTeam'] == 'Packers' and row['homeScore'] > row['awayScore']):
                packers_schedule_results.append('W')
            elif (row['awayTeam'] == 'Packers' and row['awayScore'] > row['homeScore']):
                packers_schedule_results.append('W')
            elif (row['homeTeam'] == 'Packers' and row['homeScore'] < row['awayScore']):
                packers_schedule_results.append('L')
            elif (row['awayTeam'] == 'Packers' and row['awayScore'] < row['homeScore']):
                packers_schedule_results.append('L')
            elif (row['awayTeam'] == 'Packers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                packers_schedule_results.append('T')
            elif (row['homeTeam'] == 'Packers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                packers_schedule_results.append('T')
            else:
                packers_schedule_results.append('NA')

        Packers = Team('Packers', 'NFC', 'NFCN', packers_schedule[0], packers_schedule_results[0], packers_schedule[1],
                    packers_schedule_results[1], packers_schedule[2], packers_schedule_results[2], packers_schedule[3],
                    packers_schedule_results[3],
                    packers_schedule[4], packers_schedule_results[4], packers_schedule[5], packers_schedule_results[5],
                    packers_schedule[6],
                    packers_schedule_results[6], packers_schedule[7], packers_schedule_results[7], packers_schedule[8],
                    packers_schedule_results[8],
                    packers_schedule[9], packers_schedule_results[9], packers_schedule[10], packers_schedule_results[10],
                    packers_schedule[11],
                    packers_schedule_results[11], packers_schedule[12], packers_schedule_results[12], packers_schedule[13],
                    packers_schedule_results[13],
                    packers_schedule[14], packers_schedule_results[14], packers_schedule[15], packers_schedule_results[15],
                    packers_schedule[16],
                    packers_schedule_results[16])

        vikings_data = df[(df['homeTeam'] == 'Vikings') | (df['awayTeam'] == 'Vikings')]

        vikings_schedule = []
        for index, row in vikings_data.iterrows():
            if (row['homeTeam'] == 'Vikings'):
                vikings_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Vikings'):
                vikings_schedule.append(row['homeTeam'])

        vikings_schedule_results = []
        for index, row in vikings_data.iterrows():
            if (row['homeTeam'] == 'Vikings' and row['homeScore'] > row['awayScore']):
                vikings_schedule_results.append('W')
            elif (row['awayTeam'] == 'Vikings' and row['awayScore'] > row['homeScore']):
                vikings_schedule_results.append('W')
            elif (row['homeTeam'] == 'Vikings' and row['homeScore'] < row['awayScore']):
                vikings_schedule_results.append('L')
            elif (row['awayTeam'] == 'Vikings' and row['awayScore'] < row['homeScore']):
                vikings_schedule_results.append('L')
            elif (row['awayTeam'] == 'Vikings' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                vikings_schedule_results.append('T')
            elif (row['homeTeam'] == 'Vikings' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                vikings_schedule_results.append('T')
            else:
                vikings_schedule_results.append('NA')

        Vikings = Team('Vikings', 'NFC', 'NFCN', vikings_schedule[0], vikings_schedule_results[0], vikings_schedule[1],
                    vikings_schedule_results[1], vikings_schedule[2], vikings_schedule_results[2], vikings_schedule[3],
                    vikings_schedule_results[3],
                    vikings_schedule[4], vikings_schedule_results[4], vikings_schedule[5], vikings_schedule_results[5],
                    vikings_schedule[6],
                    vikings_schedule_results[6], vikings_schedule[7], vikings_schedule_results[7], vikings_schedule[8],
                    vikings_schedule_results[8],
                    vikings_schedule[9], vikings_schedule_results[9], vikings_schedule[10], vikings_schedule_results[10],
                    vikings_schedule[11],
                    vikings_schedule_results[11], vikings_schedule[12], vikings_schedule_results[12], vikings_schedule[13],
                    vikings_schedule_results[13],
                    vikings_schedule[14], vikings_schedule_results[14], vikings_schedule[15], vikings_schedule_results[15],
                    vikings_schedule[16],
                    vikings_schedule_results[16])

        buccaneers_data = df[(df['homeTeam'] == 'Buccaneers') | (df['awayTeam'] == 'Buccaneers')]

        buccaneers_schedule = []
        for index, row in buccaneers_data.iterrows():
            if (row['homeTeam'] == 'Buccaneers'):
                buccaneers_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Buccaneers'):
                buccaneers_schedule.append(row['homeTeam'])

        buccaneers_schedule_results = []
        for index, row in buccaneers_data.iterrows():
            if (row['homeTeam'] == 'Buccaneers' and row['homeScore'] > row['awayScore']):
                buccaneers_schedule_results.append('W')
            elif (row['awayTeam'] == 'Buccaneers' and row['awayScore'] > row['homeScore']):
                buccaneers_schedule_results.append('W')
            elif (row['homeTeam'] == 'Buccaneers' and row['homeScore'] < row['awayScore']):
                buccaneers_schedule_results.append('L')
            elif (row['awayTeam'] == 'Buccaneers' and row['awayScore'] < row['homeScore']):
                buccaneers_schedule_results.append('L')
            elif (row['awayTeam'] == 'Buccaneers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                buccaneers_schedule_results.append('T')
            elif (row['homeTeam'] == 'Buccaneers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                buccaneers_schedule_results.append('T')
            else:
                buccaneers_schedule_results.append('NA')

        Buccaneers = Team('Buccaneers', 'NFC', 'NFCS', buccaneers_schedule[0], buccaneers_schedule_results[0],
                        buccaneers_schedule[1],
                        buccaneers_schedule_results[1], buccaneers_schedule[2], buccaneers_schedule_results[2],
                        buccaneers_schedule[3], buccaneers_schedule_results[3],
                        buccaneers_schedule[4], buccaneers_schedule_results[4], buccaneers_schedule[5],
                        buccaneers_schedule_results[5], buccaneers_schedule[6],
                        buccaneers_schedule_results[6], buccaneers_schedule[7], buccaneers_schedule_results[7],
                        buccaneers_schedule[8], buccaneers_schedule_results[8],
                        buccaneers_schedule[9], buccaneers_schedule_results[9], buccaneers_schedule[10],
                        buccaneers_schedule_results[10], buccaneers_schedule[11],
                        buccaneers_schedule_results[11], buccaneers_schedule[12], buccaneers_schedule_results[12],
                        buccaneers_schedule[13], buccaneers_schedule_results[13],
                        buccaneers_schedule[14], buccaneers_schedule_results[14], buccaneers_schedule[15],
                        buccaneers_schedule_results[15], buccaneers_schedule[16],
                        buccaneers_schedule_results[16])

        falcons_data = df[(df['homeTeam'] == 'Falcons') | (df['awayTeam'] == 'Falcons')]

        falcons_schedule = []
        for index, row in falcons_data.iterrows():
            if (row['homeTeam'] == 'Falcons'):
                falcons_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Falcons'):
                falcons_schedule.append(row['homeTeam'])

        falcons_schedule_results = []
        for index, row in falcons_data.iterrows():
            if (row['homeTeam'] == 'Falcons' and row['homeScore'] > row['awayScore']):
                falcons_schedule_results.append('W')
            elif (row['awayTeam'] == 'Falcons' and row['awayScore'] > row['homeScore']):
                falcons_schedule_results.append('W')
            elif (row['homeTeam'] == 'Falcons' and row['homeScore'] < row['awayScore']):
                falcons_schedule_results.append('L')
            elif (row['awayTeam'] == 'Falcons' and row['awayScore'] < row['homeScore']):
                falcons_schedule_results.append('L')
            elif (row['awayTeam'] == 'Falcons' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                falcons_schedule_results.append('T')
            elif (row['homeTeam'] == 'Falcons' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                falcons_schedule_results.append('T')
            else:
                falcons_schedule_results.append('NA')

        Falcons = Team('Falcons', 'NFC', 'NFCS', falcons_schedule[0], falcons_schedule_results[0], falcons_schedule[1],
                    falcons_schedule_results[1], falcons_schedule[2], falcons_schedule_results[2], falcons_schedule[3],
                    falcons_schedule_results[3],
                    falcons_schedule[4], falcons_schedule_results[4], falcons_schedule[5], falcons_schedule_results[5],
                    falcons_schedule[6],
                    falcons_schedule_results[6], falcons_schedule[7], falcons_schedule_results[7], falcons_schedule[8],
                    falcons_schedule_results[8],
                    falcons_schedule[9], falcons_schedule_results[9], falcons_schedule[10], falcons_schedule_results[10],
                    falcons_schedule[11],
                    falcons_schedule_results[11], falcons_schedule[12], falcons_schedule_results[12], falcons_schedule[13],
                    falcons_schedule_results[13],
                    falcons_schedule[14], falcons_schedule_results[14], falcons_schedule[15], falcons_schedule_results[15],
                    falcons_schedule[16],
                    falcons_schedule_results[16])

        saints_data = df[(df['homeTeam'] == 'Saints') | (df['awayTeam'] == 'Saints')]

        saints_schedule = []
        for index, row in saints_data.iterrows():
            if (row['homeTeam'] == 'Saints'):
                saints_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Saints'):
                saints_schedule.append(row['homeTeam'])

        saints_schedule_results = []
        for index, row in saints_data.iterrows():
            if (row['homeTeam'] == 'Saints' and row['homeScore'] > row['awayScore']):
                saints_schedule_results.append('W')
            elif (row['awayTeam'] == 'Saints' and row['awayScore'] > row['homeScore']):
                saints_schedule_results.append('W')
            elif (row['homeTeam'] == 'Saints' and row['homeScore'] < row['awayScore']):
                saints_schedule_results.append('L')
            elif (row['awayTeam'] == 'Saints' and row['awayScore'] < row['homeScore']):
                saints_schedule_results.append('L')
            elif (row['awayTeam'] == 'Saints' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                saints_schedule_results.append('T')
            elif (row['homeTeam'] == 'Saints' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                saints_schedule_results.append('T')
            else:
                saints_schedule_results.append('NA')

        Saints = Team('Saints', 'NFC', 'NFCS', saints_schedule[0], saints_schedule_results[0], saints_schedule[1],
                    saints_schedule_results[1], saints_schedule[2], saints_schedule_results[2], saints_schedule[3],
                    saints_schedule_results[3],
                    saints_schedule[4], saints_schedule_results[4], saints_schedule[5], saints_schedule_results[5],
                    saints_schedule[6],
                    saints_schedule_results[6], saints_schedule[7], saints_schedule_results[7], saints_schedule[8],
                    saints_schedule_results[8],
                    saints_schedule[9], saints_schedule_results[9], saints_schedule[10], saints_schedule_results[10],
                    saints_schedule[11],
                    saints_schedule_results[11], saints_schedule[12], saints_schedule_results[12], saints_schedule[13],
                    saints_schedule_results[13],
                    saints_schedule[14], saints_schedule_results[14], saints_schedule[15], saints_schedule_results[15],
                    saints_schedule[16],
                    saints_schedule_results[16])

        panthers_data = df[(df['homeTeam'] == 'Panthers') | (df['awayTeam'] == 'Panthers')]

        panthers_schedule = []
        for index, row in panthers_data.iterrows():
            if (row['homeTeam'] == 'Panthers'):
                panthers_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Panthers'):
                panthers_schedule.append(row['homeTeam'])

        panthers_schedule_results = []
        for index, row in panthers_data.iterrows():
            if (row['homeTeam'] == 'Panthers' and row['homeScore'] > row['awayScore']):
                panthers_schedule_results.append('W')
            elif (row['awayTeam'] == 'Panthers' and row['awayScore'] > row['homeScore']):
                panthers_schedule_results.append('W')
            elif (row['homeTeam'] == 'Panthers' and row['homeScore'] < row['awayScore']):
                panthers_schedule_results.append('L')
            elif (row['awayTeam'] == 'Panthers' and row['awayScore'] < row['homeScore']):
                panthers_schedule_results.append('L')
            elif (row['awayTeam'] == 'Panthers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                panthers_schedule_results.append('T')
            elif (row['homeTeam'] == 'Panthers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                panthers_schedule_results.append('T')
            else:
                panthers_schedule_results.append('NA')

        Panthers = Team('Panthers', 'NFC', 'NFCS', panthers_schedule[0], panthers_schedule_results[0], panthers_schedule[1],
                        panthers_schedule_results[1], panthers_schedule[2], panthers_schedule_results[2], panthers_schedule[3],
                        panthers_schedule_results[3],
                        panthers_schedule[4], panthers_schedule_results[4], panthers_schedule[5], panthers_schedule_results[5],
                        panthers_schedule[6],
                        panthers_schedule_results[6], panthers_schedule[7], panthers_schedule_results[7], panthers_schedule[8],
                        panthers_schedule_results[8],
                        panthers_schedule[9], panthers_schedule_results[9], panthers_schedule[10],
                        panthers_schedule_results[10], panthers_schedule[11],
                        panthers_schedule_results[11], panthers_schedule[12], panthers_schedule_results[12],
                        panthers_schedule[13], panthers_schedule_results[13],
                        panthers_schedule[14], panthers_schedule_results[14], panthers_schedule[15],
                        panthers_schedule_results[15], panthers_schedule[16],
                        panthers_schedule_results[16])

        niners_data = df[(df['homeTeam'] == '49ers') | (df['awayTeam'] == '49ers')]

        niners_schedule = []
        for index, row in niners_data.iterrows():
            if (row['homeTeam'] == '49ers'):
                niners_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == '49ers'):
                niners_schedule.append(row['homeTeam'])

        niners_schedule_results = []
        for index, row in niners_data.iterrows():
            if (row['homeTeam'] == '49ers' and row['homeScore'] > row['awayScore']):
                niners_schedule_results.append('W')
            elif (row['awayTeam'] == '49ers' and row['awayScore'] > row['homeScore']):
                niners_schedule_results.append('W')
            elif (row['homeTeam'] == '49ers' and row['homeScore'] < row['awayScore']):
                niners_schedule_results.append('L')
            elif (row['awayTeam'] == '49ers' and row['awayScore'] < row['homeScore']):
                niners_schedule_results.append('L')
            elif (row['awayTeam'] == '49ers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                niners_schedule_results.append('T')
            elif (row['homeTeam'] == '49ers' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                niners_schedule_results.append('T')
            else:
                niners_schedule_results.append('NA')

        Niners = Team('49ers', 'NFC', 'NFCW', niners_schedule[0], niners_schedule_results[0], niners_schedule[1],
                    niners_schedule_results[1], niners_schedule[2], niners_schedule_results[2], niners_schedule[3],
                    niners_schedule_results[3],
                    niners_schedule[4], niners_schedule_results[4], niners_schedule[5], niners_schedule_results[5],
                    niners_schedule[6],
                    niners_schedule_results[6], niners_schedule[7], niners_schedule_results[7], niners_schedule[8],
                    niners_schedule_results[8],
                    niners_schedule[9], niners_schedule_results[9], niners_schedule[10], niners_schedule_results[10],
                    niners_schedule[11],
                    niners_schedule_results[11], niners_schedule[12], niners_schedule_results[12], niners_schedule[13],
                    niners_schedule_results[13],
                    niners_schedule[14], niners_schedule_results[14], niners_schedule[15], niners_schedule_results[15],
                    niners_schedule[16],
                    niners_schedule_results[16])

        cardinals_data = df[(df['homeTeam'] == 'Cardinals') | (df['awayTeam'] == 'Cardinals')]

        cardinals_schedule = []
        for index, row in cardinals_data.iterrows():
            if (row['homeTeam'] == 'Cardinals'):
                cardinals_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Cardinals'):
                cardinals_schedule.append(row['homeTeam'])

        cardinals_schedule_results = []
        for index, row in cardinals_data.iterrows():
            if (row['homeTeam'] == 'Cardinals' and row['homeScore'] > row['awayScore']):
                cardinals_schedule_results.append('W')
            elif (row['awayTeam'] == 'Cardinals' and row['awayScore'] > row['homeScore']):
                cardinals_schedule_results.append('W')
            elif (row['homeTeam'] == 'Cardinals' and row['homeScore'] < row['awayScore']):
                cardinals_schedule_results.append('L')
            elif (row['awayTeam'] == 'Cardinals' and row['awayScore'] < row['homeScore']):
                cardinals_schedule_results.append('L')
            elif (row['awayTeam'] == 'Cardinals' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                cardinals_schedule_results.append('T')
            elif (row['homeTeam'] == 'Cardinals' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                cardinals_schedule_results.append('T')
            else:
                cardinals_schedule_results.append('NA')

        Cardinals = Team('Cardinals', 'NFC', 'NFCW', cardinals_schedule[0], cardinals_schedule_results[0],
                        cardinals_schedule[1],
                        cardinals_schedule_results[1], cardinals_schedule[2], cardinals_schedule_results[2],
                        cardinals_schedule[3], cardinals_schedule_results[3],
                        cardinals_schedule[4], cardinals_schedule_results[4], cardinals_schedule[5],
                        cardinals_schedule_results[5], cardinals_schedule[6],
                        cardinals_schedule_results[6], cardinals_schedule[7], cardinals_schedule_results[7],
                        cardinals_schedule[8], cardinals_schedule_results[8],
                        cardinals_schedule[9], cardinals_schedule_results[9], cardinals_schedule[10],
                        cardinals_schedule_results[10], cardinals_schedule[11],
                        cardinals_schedule_results[11], cardinals_schedule[12], cardinals_schedule_results[12],
                        cardinals_schedule[13], cardinals_schedule_results[13],
                        cardinals_schedule[14], cardinals_schedule_results[14], cardinals_schedule[15],
                        cardinals_schedule_results[15], cardinals_schedule[16],
                        cardinals_schedule_results[16])

        rams_data = df[(df['homeTeam'] == 'Rams') | (df['awayTeam'] == 'Rams')]

        rams_schedule = []
        for index, row in rams_data.iterrows():
            if (row['homeTeam'] == 'Rams'):
                rams_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Rams'):
                rams_schedule.append(row['homeTeam'])

        rams_schedule_results = []
        for index, row in rams_data.iterrows():
            if (row['homeTeam'] == 'Rams' and row['homeScore'] > row['awayScore']):
                rams_schedule_results.append('W')
            elif (row['awayTeam'] == 'Rams' and row['awayScore'] > row['homeScore']):
                rams_schedule_results.append('W')
            elif (row['homeTeam'] == 'Rams' and row['homeScore'] < row['awayScore']):
                rams_schedule_results.append('L')
            elif (row['awayTeam'] == 'Rams' and row['awayScore'] < row['homeScore']):
                rams_schedule_results.append('L')
            elif (row['awayTeam'] == 'Rams' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                rams_schedule_results.append('T')
            elif (row['homeTeam'] == 'Rams' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                rams_schedule_results.append('T')
            else:
                rams_schedule_results.append('NA')

        Rams = Team('Rams', 'NFC', 'NFCW', rams_schedule[0], rams_schedule_results[0], rams_schedule[1],
                    rams_schedule_results[1], rams_schedule[2], rams_schedule_results[2], rams_schedule[3],
                    rams_schedule_results[3],
                    rams_schedule[4], rams_schedule_results[4], rams_schedule[5], rams_schedule_results[5], rams_schedule[6],
                    rams_schedule_results[6], rams_schedule[7], rams_schedule_results[7], rams_schedule[8],
                    rams_schedule_results[8],
                    rams_schedule[9], rams_schedule_results[9], rams_schedule[10], rams_schedule_results[10], rams_schedule[11],
                    rams_schedule_results[11], rams_schedule[12], rams_schedule_results[12], rams_schedule[13],
                    rams_schedule_results[13],
                    rams_schedule[14], rams_schedule_results[14], rams_schedule[15], rams_schedule_results[15],
                    rams_schedule[16],
                    rams_schedule_results[16])

        seahawks_data = df[(df['homeTeam'] == 'Seahawks') | (df['awayTeam'] == 'Seahawks')]

        seahawks_schedule = []
        for index, row in seahawks_data.iterrows():
            if (row['homeTeam'] == 'Seahawks'):
                seahawks_schedule.append(row['awayTeam'])
            elif (row['awayTeam'] == 'Seahawks'):
                seahawks_schedule.append(row['homeTeam'])

        seahawks_schedule_results = []
        for index, row in seahawks_data.iterrows():
            if (row['homeTeam'] == 'Seahawks' and row['homeScore'] > row['awayScore']):
                seahawks_schedule_results.append('W')
            elif (row['awayTeam'] == 'Seahawks' and row['awayScore'] > row['homeScore']):
                seahawks_schedule_results.append('W')
            elif (row['homeTeam'] == 'Seahawks' and row['homeScore'] < row['awayScore']):
                seahawks_schedule_results.append('L')
            elif (row['awayTeam'] == 'Seahawks' and row['awayScore'] < row['homeScore']):
                seahawks_schedule_results.append('L')
            elif (row['awayTeam'] == 'Seahawks' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                seahawks_schedule_results.append('T')
            elif (row['homeTeam'] == 'Seahawks' and row['awayScore'] == row['homeScore'] and not row['awayScore'] == 0):
                seahawks_schedule_results.append('T')
            else:
                seahawks_schedule_results.append('NA')

        Seahawks = Team('Seahawks', 'NFC', 'NFCW', seahawks_schedule[0], seahawks_schedule_results[0], seahawks_schedule[1],
                        seahawks_schedule_results[1], seahawks_schedule[2], seahawks_schedule_results[2], seahawks_schedule[3],
                        seahawks_schedule_results[3],
                        seahawks_schedule[4], seahawks_schedule_results[4], seahawks_schedule[5], seahawks_schedule_results[5],
                        seahawks_schedule[6],
                        seahawks_schedule_results[6], seahawks_schedule[7], seahawks_schedule_results[7], seahawks_schedule[8],
                        seahawks_schedule_results[8],
                        seahawks_schedule[9], seahawks_schedule_results[9], seahawks_schedule[10],
                        seahawks_schedule_results[10], seahawks_schedule[11],
                        seahawks_schedule_results[11], seahawks_schedule[12], seahawks_schedule_results[12],
                        seahawks_schedule[13], seahawks_schedule_results[13],
                        seahawks_schedule[14], seahawks_schedule_results[14], seahawks_schedule[15],
                        seahawks_schedule_results[15], seahawks_schedule[16],
                        seahawks_schedule_results[16])
    else:
        for team_name, team_obj in [
            ('Bills', Bills), ('Dolphins', Dolphins), ('Jets', Jets), ('Patriots', Patriots),
            ('Bengals', Bengals), ('Browns', Browns), ('Ravens', Ravens), ('Steelers', Steelers),
            ('Colts', Colts), ('Jaguars', Jaguars), ('Titans', Titans), ('Texans', Texans),
            ('Broncos', Broncos), ('Chiefs', Chiefs), ('Chargers', Chargers), ('Raiders', Raiders),
            ('Commanders', Commanders), ('Cowboys', Cowboys), ('Giants', Giants), ('Eagles', Eagles),
            ('Bears', Bears), ('Lions', Lions), ('Packers', Packers), ('Vikings', Vikings),
            ('Buccaneers', Buccaneers), ('Falcons', Falcons), ('Saints', Saints), ('Panthers', Panthers),
            ('49ers', Niners), ('Cardinals', Cardinals), ('Rams', Rams), ('Seahawks', Seahawks)
        ]:
            # Get team data from DataFrame
            team_data = df[(df['homeTeam'] == team_name) | (df['awayTeam'] == team_name)]

            # Build schedule
            schedule = []
            for index, row in team_data.iterrows():
                if row['homeTeam'] == team_name:
                    schedule.append(row['awayTeam'])
                elif row['awayTeam'] == team_name:
                    schedule.append(row['homeTeam'])

            # Build results
            schedule_results = []
            for index, row in team_data.iterrows():
                if row['homeTeam'] == team_name and row['homeScore'] > row['awayScore']:
                    schedule_results.append('W')
                elif row['awayTeam'] == team_name and row['awayScore'] > row['homeScore']:
                    schedule_results.append('W')
                elif row['homeTeam'] == team_name and row['homeScore'] < row['awayScore']:
                    schedule_results.append('L')
                elif row['awayTeam'] == team_name and row['awayScore'] < row['homeScore']:
                    schedule_results.append('L')
                elif row['awayScore'] == row['homeScore'] and row['awayScore'] != 0:
                    schedule_results.append('T')
                else:
                    schedule_results.append('NA')

            # Update team object attributes
            team_obj.matchups = schedule
            team_obj.results = schedule_results

            # Update individual game and result attributes (g1, g1result, ..., g17, g17result)
            for i in range(17):
                setattr(team_obj, f'g{i+1}', schedule[i] if i < len(schedule) else '')
                setattr(team_obj, f'g{i+1}result', schedule_results[i] if i < len(schedule_results) else 'NA')


    count += 1


fillSchedules(df)

teamList = [Bills, Dolphins, Jets, Patriots, Bengals, Browns, Ravens, Steelers, Colts, Jaguars, Titans, Texans,
            Broncos, Chiefs, Chargers, Raiders, Commanders, Cowboys, Giants, Eagles, Bears, Lions, Packers, Vikings,
            Buccaneers,
            Falcons, Saints, Panthers, Niners, Cardinals, Rams, Seahawks]

#print("In teamList: " + str(id(teamList[0])))

AFC = [Bills, Dolphins, Jets, Patriots, Bengals, Browns, Ravens, Steelers, Colts, Jaguars, Titans, Texans,
       Broncos, Chiefs, Chargers, Raiders]
NFC = [Commanders, Cowboys, Giants, Eagles, Bears, Lions, Packers, Vikings, Buccaneers,
       Falcons, Saints, Panthers, Niners, Cardinals, Rams, Seahawks]

AFCE = [Bills, Dolphins, Jets, Patriots]
AFCN = [Bengals, Browns, Ravens, Steelers]
AFCS = [Colts, Jaguars, Titans, Texans]
AFCW = [Broncos, Chiefs, Chargers, Raiders]
NFCE = [Commanders, Cowboys, Giants, Eagles]
NFCN = [Bears, Lions, Packers, Vikings]
NFCS = [Buccaneers, Falcons, Saints, Panthers]
NFCW = [Niners, Cardinals, Rams, Seahawks]

for i in teamList:
    if (i.getDivision() == 'AFCE'):
        AFCE.append(i)
    elif (i.getDivision() == 'AFCN'):
        AFCN.append(i)
    elif (i.getDivision() == 'AFCS'):
        AFCS.append(i)
    elif (i.getDivision() == 'AFCW'):
        AFCW.append(i)
    elif (i.getDivision() == 'NFCE'):
        NFCE.append(i)
    elif (i.getDivision() == 'NFCN'):
        NFCN.append(i)
    elif (i.getDivision() == 'NFCS'):
        NFCS.append(i)
    elif (i.getDivision() == 'NFCW'):
        NFCW.append(i)


def tiebreak2(Team1, Team2):
    pass


def tiebreak3(Team1, Team2, Team3):
    pass


def tiebreak4(Team1, Team2, Team3, Team4):
    pass

def tiebreak5(Team1, Team2, Team3, Team4, Team5):
    pass

def tiebreak6(Team1, Team2, Team3, Team4, Team5, Team6):
    pass

def tiebreak7(Team1, Team2, Team3, Team4, Team5, Team6, Team7):
    pass

def tiebreak8(Team1, Team2, Team3, Team4, Team5, Team6, Team7, Team8):
    pass

def findTeam(name):
    for team in teamList:
        if team.getName() == name:
            return team


divh2h2Matchups1 = []
divh2h2Matchups2 = []


def isDivH2H2(Team1, Team2):
    global divh2hMatchups1, divh2hMatchups2
    divh2h2Matchups1 = []
    divh2h2Matchups2 = []
    for i in range(17):
        if (Team1.matchups[i] == Team2.getName()):
            divh2h2Matchups1.append(Team1.results[i])
        if (Team2.matchups[i] == Team1.getName()):
            divh2h2Matchups2.append(Team2.results[i])
    if (divh2h2Matchups1.count('W') == 2 or divh2h2Matchups1.count('L') == 2):
        return ([True, divh2h2Matchups1.count('W'), divh2h2Matchups2.count('W')])
    else:
        return ([False, divh2h2Matchups1.count('W'), divh2h2Matchups2.count('W')])
    # currently only works if all games are played between them


def divH2H2(Team1, Team2):
    global divh2h2Matchups1, divh2h2Matchups2
    #print (divh2h2Matchups1)
    #print (divh2h2Matchups2)
    if (divh2h2Matchups1.count('W') > divh2h2Matchups2.count('W')):
        #print (Team1.getName() + " wins via div h2h over " + Team2.getName())
        return (Team1)
    else:
        #print (Team2.getName() + " wins via div h2h over " + Team1.getName())
        return (Team2)


divh2h3Matchups1 = []
divh2h3Matchups2 = []
divh2h3Matchups3 = []


def isDivH2H3(Team1, Team2, Team3):
    global divh2h3Matchups1, divh2h3Matchups2, divh2h3Matchups3
    divh2h3Matchups1 = []
    divh2h3Matchups2 = []
    divh2h3Matchups3 = []
    for i in range(17):
        if (Team1.matchups[i] == Team2.getName()):
            divh2h3Matchups1.append(Team1.results[i])
        if (Team1.matchups[i] == Team3.getName()):
            divh2h3Matchups1.append(Team1.results[i])
        if (Team2.matchups[i] == Team1.getName()):
            divh2h3Matchups2.append(Team2.results[i])
        if (Team2.matchups[i] == Team3.getName()):
            divh2h3Matchups2.append(Team2.results[i])
        if (Team3.matchups[i] == Team1.getName()):
            divh2h3Matchups3.append(Team3.results[i])
        if (Team3.matchups[i] == Team2.getName()):
            divh2h3Matchups3.append(Team3.results[i])

    if (divh2h3Matchups1.count('W') > divh2h3Matchups2.count('W') or divh2h3Matchups1.count('W') >
            divh2h3Matchups3.count('W') or divh2h3Matchups2.count('W') > divh2h3Matchups3.count('W')):
        return (True)
    else:
        return (False)


def divH2H3(Team1, Team2, Team3):
    order = []
    wins1 = divh2h3Matchups1.count('W')
    wins2 = divh2h3Matchups2.count('W')
    wins3 = divh2h3Matchups3.count('W')

    if (wins1 > wins2 and wins3 > wins1):
        order = [Team3, Team1, Team2]

    elif (wins2 > wins1 and wins3 > wins2):
        order = [Team3, Team2, Team1]

    elif (wins2 > wins3 and wins1 > wins2):
        order = [Team1, Team2, Team3]

    elif (wins3 > wins2 and wins1 > wins3):
        order = [Team1, Team3, Team2]

    elif (wins3 > wins1 and wins2 > wins3):
        order = [Team2, Team3, Team1]

    elif (wins1 > wins3 and wins2 > wins1):
        order = [Team2, Team1, Team3]

    elif (wins1 == wins2 and wins1 > wins3):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3]

    elif (wins1 == wins3 and wins1 > wins2):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2]

    elif (wins3 == wins2 and wins3 > wins1):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1]

    elif (wins1 == wins2 and wins1 < wins3):
        result = tiebreak2(Team1, Team2)
        order = [Team3, result[0], result[1]]

    elif (wins1 == wins3 and wins1 < wins2):
        result = tiebreak2(Team1, Team3)
        order = [Team2, result[0], result[1]]

    elif (wins3 == wins2 and wins3 < wins1):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1]]

    else:
        print("div h2h3 not working")
        order = [Team1, Team2, Team3]
    #print ("Div H2H3 order: " + order[0].getName() + ", " + order[1].getName() + ", " + order[2].getName())
    
    return (order)


h2h2Matchups1 = []
h2h2Matchups2 = []


def isH2H2(Team1, Team2):
    global h2h2Matchups1, h2h2Matchups2
    h2h2Matchups1 = []
    h2h2Matchups2 = []
    for i in range(17):
        if (Team1.matchups[i] == Team2.getName()):
            h2h2Matchups1.append(Team1.results[i])
        if (Team2.matchups[i] == Team1.getName()):
            h2h2Matchups2.append(Team2.results[i])
    if (h2h2Matchups1.count('W') == 1 or h2h2Matchups2.count('W') == 1):
        return (True)
    else:
        return (False)


def h2h2(Team1, Team2):
    #print (h2h2Matchups1)
    #print (h2h2Matchups2)
    if (h2h2Matchups1.count('W') > h2h2Matchups2.count('W')):
        #print (Team1.getName() + " wins h2h tiebreaker over " + Team2.getName())
        return (Team1)
    else:
        #print (Team2.getName() + " wins h2h tiebreaker over " + Team1.getName())
        return (Team2)


h2h3Matchups1 = []
h2h3Matchups2 = []
h2h3Matchups3 = []


def isH2H3(Team1, Team2, Team3):
    global h2h3Matchups1, h2h3Matchups2, h2h3Matchups3
    h2h3Matchups1 = []
    h2h3Matchups2 = []
    h2h3Matchups3 = []
    for i in range(17):
        if (Team1.matchups[i] == Team2.getName()):
            h2h3Matchups1.append(Team1.results[i])
        if (Team1.matchups[i] == Team3.getName()):
            h2h3Matchups1.append(Team1.results[i])
        if (Team2.matchups[i] == Team1.getName()):
            h2h3Matchups2.append(Team2.results[i])
        if (Team2.matchups[i] == Team3.getName()):
            h2h3Matchups2.append(Team2.results[i])
        if (Team3.matchups[i] == Team1.getName()):
            h2h3Matchups3.append(Team3.results[i])
        if (Team3.matchups[i] == Team2.getName()):
            h2h3Matchups3.append(Team3.results[i])
    if (h2h3Matchups1.count('W') == 2 or h2h3Matchups2.count('W') == 2 or h2h3Matchups3.count('W') == 2 or
            h2h3Matchups3.count('L') == 2 or h2h3Matchups2.count('L') == 2 or h2h3Matchups3.count('L') == 2):
        return (True)
    else:
        return (False)


def h2h3(Team1, Team2, Team3):
    order = []
    wins1 = h2h3Matchups1.count('W')
    wins2 = h2h3Matchups2.count('W')
    wins3 = h2h3Matchups3.count('W')

    if (wins1 == wins2 and wins1 > wins3):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3]

    elif (wins1 == wins3 and wins1 > wins2):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2]

    elif (wins3 == wins2 and wins3 > wins1):
        result = tiebreak2(Team3, Team2)
        order = [result[0], result[1], Team1]

    elif (wins1 == wins2 and wins1 < wins3):
        result = tiebreak2(Team1, Team2)
        order = [Team3, result[0], result[1]]

    elif (wins1 == wins3 and wins1 < wins2):
        result = tiebreak2(Team1, Team3)
        order = [Team2, result[0], result[1]]

    elif (wins3 == wins2 and wins3 < wins1):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1]]

    elif (wins1 > wins2 and wins2 > wins3):
        order = [Team1, Team2, Team3]

    elif (wins2 > wins1 and wins1 > wins3):
        order = [Team2, Team1, Team3]

    elif (wins3 > wins2 and wins2 > wins1):
        order = [Team3, Team2, Team1]

    elif (wins1 > wins3 and wins3 > wins2):
        order = [Team1, Team3, Team2]

    elif (wins2 > wins3 and wins3 > wins1):
        order = [Team2, Team3, Team1]

    elif (wins3 > wins1 and wins1 > wins2):
        order = [Team3, Team1, Team2]

    #print ("Order of h2h3 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + order[2].getName())
    return (order)


h2h4Matchups1 = []
h2h4Matchups2 = []
h2h4Matchups3 = []
h2h4Matchups4 = []


def isH2H4(Team1, Team2, Team3, Team4):
    global h2h4Matchups1, h2h4Matchups2, h2h4Matchups3, h2h4Matchups4
    h2h4Matchups1 = []
    h2h4Matchups2 = []
    h2h4Matchups3 = []
    h2h4Matchups4 = []
    for i in range(17):
        if (Team1.matchups[i] == Team2.getName()):
            h2h4Matchups1.append(Team1.results[i])
        if (Team1.matchups[i] == Team3.getName()):
            h2h4Matchups1.append(Team1.results[i])
        if (Team1.matchups[i] == Team4.getName()):
            h2h4Matchups1.append(Team1.results[i])
        if (Team2.matchups[i] == Team1.getName()):
            h2h4Matchups2.append(Team2.results[i])
        if (Team2.matchups[i] == Team3.getName()):
            h2h4Matchups2.append(Team2.results[i])
        if (Team2.matchups[i] == Team4.getName()):
            h2h4Matchups2.append(Team2.results[i])
        if (Team3.matchups[i] == Team1.getName()):
            h2h4Matchups3.append(Team3.results[i])
        if (Team3.matchups[i] == Team2.getName()):
            h2h4Matchups3.append(Team3.results[i])
        if (Team3.matchups[i] == Team4.getName()):
            h2h4Matchups3.append(Team3.results[i])
        if (Team4.matchups[i] == Team1.getName()):
            h2h4Matchups4.append(Team4.results[i])
        if (Team4.matchups[i] == Team2.getName()):
            h2h4Matchups4.append(Team4.results[i])
        if (Team4.matchups[i] == Team3.getName()):
            h2h4Matchups4.append(Team4.results[i])
    if (h2h4Matchups1.count('W') == 3 or h2h4Matchups2.count('W') == 3 or h2h4Matchups3.count('W') == 3 or
            h2h4Matchups3.count('L') == 3 or h2h4Matchups2.count('L') == 3 or h2h4Matchups3.count('L') == 3 or
            h2h4Matchups4.count('W') == 3 or h2h4Matchups4.count('L') == 3):
        return (True)
    else:
        return (False)


def h2h4(Team1, Team2, Team3, Team4):
    order = []
    wins1 = h2h4Matchups1.count('W')
    wins2 = h2h4Matchups2.count('W')
    wins3 = h2h4Matchups3.count('W')
    wins4 = h2h4Matchups4.count('W')
    losses1 = h2h4Matchups1.count('L')
    losses2 = h2h4Matchups2.count('L')
    losses3 = h2h4Matchups3.count('L')
    losses4 = h2h4Matchups4.count('L')

    if (wins1 == 3 and losses4 == 3):
        result = tiebreak2(Team2, Team3)
        order = [Team1, result[0], result[1], Team4]

    elif (wins1 == 3 and losses3 == 3):
        result = tiebreak2(Team2, Team4)
        order = [Team1, result[0], result[1], Team3]

    elif (wins1 == 3 and losses2 == 3):
        result = tiebreak2(Team3, Team4)
        order = [Team1, result[0], result[1], Team2]

    elif (wins2 == 3 and losses1 == 3):
        result = tiebreak2(Team3, Team4)
        order = [Team2, result[0], result[1], Team1]

    elif (wins2 == 3 and losses3 == 3):
        result = tiebreak2(Team1, Team4)
        order = [Team2, result[0], result[1], Team3]

    elif (wins2 == 3 and losses4 == 3):
        result = tiebreak2(Team3, Team1)
        order = [Team2, result[0], result[1], Team4]

    elif (wins3 == 3 and losses1 == 3):
        result = tiebreak2(Team2, Team4)
        order = [Team3, result[0], result[1], Team1]

    elif (wins3 == 3 and losses2 == 3):
        result = tiebreak2(Team1, Team4)
        order = [Team3, result[0], result[1], Team2]

    elif (wins3 == 3 and losses4 == 3):
        result = tiebreak2(Team2, Team1)
        order = [Team3, result[0], result[1], Team4]

    elif (wins4 == 3 and losses1 == 3):
        result = tiebreak2(Team2, Team3)
        order = [Team4, result[0], result[1], Team1]

    elif (wins4 == 3 and losses2 == 3):
        result = tiebreak2(Team1, Team3)
        order = [Team4, result[0], result[1], Team2]

    elif (wins4 == 3 and losses3 == 3):
        result = tiebreak2(Team2, Team1)
        order = [Team4, result[0], result[1], Team3]

    elif (wins1 == 3):
        result = tiebreak3(Team2, Team3, Team4)
        order = [Team1, result[0], result[1], result[2]]

    elif (wins2 == 3):
        result = tiebreak3(Team1, Team3, Team4)
        order = [Team2, result[0], result[1], result[2]]

    elif (wins3 == 3):
        result = tiebreak3(Team2, Team1, Team4)
        order = [Team3, result[0], result[1], result[2]]

    elif (wins4 == 3):
        result = tiebreak3(Team2, Team3, Team1)
        order = [Team4, result[0], result[1], result[2]]

    elif (losses1 == 3):
        result = tiebreak3(Team2, Team3, Team4)
        order = [result[0], result[1], result[2], Team1]

    elif (losses2 == 3):
        result = tiebreak3(Team1, Team3, Team4)
        order = [result[0], result[1], result[2], Team2]

    elif (losses3 == 3):
        result = tiebreak3(Team2, Team1, Team4)
        order = [result[0], result[1], result[2], Team3]

    elif (losses4 == 3):
        result = tiebreak3(Team2, Team3, Team1)
        order = [result[0], result[1], result[2], Team4]

    #print ("Order of h2h4 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName() + ", " + order[3].getName())
    return (order)


divMatchups2_1 = []
divMatchups2_2 = []


def isDivRecord2(Team1, Team2):
    global divMatchups2_1, divMatchups2_2
    divMatchups2_1 = []
    divMatchups2_2 = []
    for i in range(17):
        if (Team1.getDivision() == 'AFCE'):
            if (Team1.matchups[i] == 'Bills' or Team1.matchups[i] == 'Jets' or Team1.matchups[i] == 'Dolphins' or
                    Team1.matchups[i] == 'Patriots'):
                divMatchups2_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'AFCN'):
            if (Team1.matchups[i] == 'Bengals' or Team1.matchups[i] == 'Bills' or Team1.matchups[i] == 'Ravens' or
                    Team1.matchups[i] == 'Steelers'):
                divMatchups2_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'AFCS'):
            if (Team1.matchups[i] == 'Colts' or Team1.matchups[i] == 'Jaguars' or Team1.matchups[i] == 'Titans' or
                    Team1.matchups[i] == 'Texans'):
                divMatchups2_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'AFCW'):
            if (Team1.matchups[i] == 'Broncos' or Team1.matchups[i] == 'Chiefs' or Team1.matchups[i] == 'Chargers' or
                    Team1.matchups[i] == 'Raiders'):
                divMatchups2_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCE'):
            if (Team1.matchups[i] == 'Cowboys' or Team1.matchups[i] == 'Commanders' or Team1.matchups[i] == 'Eagles' or
                    Team1.matchups[i] == 'Giants'):
                divMatchups2_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCN'):
            if (Team1.matchups[i] == 'Bears' or Team1.matchups[i] == 'Lions' or Team1.matchups[i] == 'Packers' or
                    Team1.matchups[i] == 'Vikings'):
                divMatchups2_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCS'):
            if (Team1.matchups[i] == 'Buccaneers' or Team1.matchups[i] == 'Falcons' or Team1.matchups[i] == 'Saints' or
                    Team1.matchups[i] == 'Panthers'):
                divMatchups2_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCW'):
            if (Team1.matchups[i] == '49ers' or Team1.matchups[i] == 'Cardinals' or Team1.matchups[i] == 'Rams' or
                    Team1.matchups[i] == 'Seahawks'):
                divMatchups2_1.append(Team1.results[i])

    for i in range(17):
        if (Team2.getDivision() == 'AFCE'):
            if (Team2.matchups[i] == 'Bills' or Team2.matchups[i] == 'Jets' or Team2.matchups[i] == 'Dolphins' or
                    Team2.matchups[i] == 'Patriots'):
                divMatchups2_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'AFCN'):
            if (Team2.matchups[i] == 'Bengals' or Team2.matchups[i] == 'Bills' or Team2.matchups[i] == 'Ravens' or
                    Team2.matchups[i] == 'Steelers'):
                divMatchups2_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'AFCS'):
            if (Team2.matchups[i] == 'Colts' or Team2.matchups[i] == 'Jaguars' or Team2.matchups[i] == 'Titans' or
                    Team2.matchups[i] == 'Texans'):
                divMatchups2_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'AFCW'):
            if (Team2.matchups[i] == 'Broncos' or Team2.matchups[i] == 'Chiefs' or Team2.matchups[i] == 'Chargers' or
                    Team2.matchups[i] == 'Raiders'):
                divMatchups2_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCE'):
            if (Team2.matchups[i] == 'Cowboys' or Team2.matchups[i] == 'Commanders' or Team2.matchups[i] == 'Eagles' or
                    Team2.matchups[i] == 'Giants'):
                divMatchups2_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCN'):
            if (Team2.matchups[i] == 'Bears' or Team2.matchups[i] == 'Lions' or Team2.matchups[i] == 'Packers' or
                    Team2.matchups[i] == 'Vikings'):
                divMatchups2_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCS'):
            if (Team2.matchups[i] == 'Buccaneers' or Team2.matchups[i] == 'Falcons' or Team2.matchups[i] == 'Saints' or
                    Team2.matchups[i] == 'Panthers'):
                divMatchups2_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCW'):
            if (Team2.matchups[i] == '49ers' or Team2.matchups[i] == 'Cardinals' or Team2.matchups[i] == 'Rams' or
                    Team2.matchups[i] == 'Seahawks'):
                divMatchups2_2.append(Team2.results[i])

    if (divMatchups2_1.count('W') > divMatchups2_2.count('W')):
        return (True)
    elif (divMatchups2_1.count('W') < divMatchups2_2.count('W')):
        return (True)
    else:
        return (False)


def divRecord2(Team1, Team2):
    if (divMatchups2_1.count('W') > divMatchups2_2.count('W')):
        #print (Team1.getName() + " wins div record tiebreaker over " + Team2.getName())
        return (Team1)
    else:
        #print (Team2.getName() + " wins div record tiebreaker over " + Team1.getName())
        return (Team2)


divMatchups3_1 = []
divMatchups3_2 = []
divMatchups3_3 = []


def isDivRecord3(Team1, Team2, Team3):
    global divMatchups3_1, divMatchups3_2, divMatchups3_3
    divMatchups3_1 = []
    divMatchups3_2 = []
    divMatchups3_3 = []
    for i in range(17):
        if (Team1.getDivision() == 'AFCE'):
            if (Team1.matchups[i] == 'Bills' or Team1.matchups[i] == 'Jets' or Team1.matchups[i] == 'Dolphins' or
                    Team1.matchups[i] == 'Patriots'):
                divMatchups3_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'AFCN'):
            if (Team1.matchups[i] == 'Bengals' or Team1.matchups[i] == 'Bills' or Team1.matchups[i] == 'Ravens' or
                    Team1.matchups[i] == 'Steelers'):
                divMatchups3_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'AFCS'):
            if (Team1.matchups[i] == 'Colts' or Team1.matchups[i] == 'Jaguars' or Team1.matchups[i] == 'Titans' or
                    Team1.matchups[i] == 'Texans'):
                divMatchups3_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'AFCW'):
            if (Team1.matchups[i] == 'Broncos' or Team1.matchups[i] == 'Chiefs' or Team1.matchups[i] == 'Chargers' or
                    Team1.matchups[i] == 'Raiders'):
                divMatchups3_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCE'):
            if (Team1.matchups[i] == 'Cowboys' or Team1.matchups[i] == 'Commanders' or Team1.matchups[i] == 'Eagles' or
                    Team1.matchups[i] == 'Giants'):
                divMatchups3_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCN'):
            if (Team1.matchups[i] == 'Bears' or Team1.matchups[i] == 'Lions' or Team1.matchups[i] == 'Packers' or
                    Team1.matchups[i] == 'Vikings'):
                divMatchups3_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCS'):
            if (Team1.matchups[i] == 'Buccaneers' or Team1.matchups[i] == 'Falcons' or Team1.matchups[i] == 'Saints' or
                    Team1.matchups[i] == 'Panthers'):
                divMatchups3_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCW'):
            if (Team1.matchups[i] == '49ers' or Team1.matchups[i] == 'Cardinals' or Team1.matchups[i] == 'Rams' or
                    Team1.matchups[i] == 'Seahawks'):
                divMatchups3_1.append(Team1.results[i])


    for i in range(17):
        if (Team2.getDivision() == 'AFCE'):
            if (Team2.matchups[i] == 'Bills' or Team2.matchups[i] == 'Jets' or Team2.matchups[i] == 'Dolphins' or
                    Team2.matchups[i] == 'Patriots'):
                divMatchups3_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'AFCN'):
            if (Team2.matchups[i] == 'Bengals' or Team2.matchups[i] == 'Bills' or Team2.matchups[i] == 'Ravens' or
                    Team2.matchups[i] == 'Steelers'):
                divMatchups3_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'AFCS'):
            if (Team2.matchups[i] == 'Colts' or Team2.matchups[i] == 'Jaguars' or Team2.matchups[i] == 'Titans' or
                    Team2.matchups[i] == 'Texans'):
                divMatchups3_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'AFCW'):
            if (Team2.matchups[i] == 'Broncos' or Team2.matchups[i] == 'Chiefs' or Team2.matchups[i] == 'Chargers' or
                    Team2.matchups[i] == 'Raiders'):
                divMatchups3_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCE'):
            if (Team2.matchups[i] == 'Cowboys' or Team2.matchups[i] == 'Commanders' or Team2.matchups[i] == 'Eagles' or
                    Team2.matchups[i] == 'Giants'):
                divMatchups3_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCN'):
            if (Team2.matchups[i] == 'Bears' or Team2.matchups[i] == 'Lions' or Team2.matchups[i] == 'Packers' or
                    Team2.matchups[i] == 'Vikings'):
                divMatchups3_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCS'):
            if (Team2.matchups[i] == 'Buccaneers' or Team2.matchups[i] == 'Falcons' or Team2.matchups[i] == 'Saints' or
                    Team2.matchups[i] == 'Panthers'):
                divMatchups3_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCW'):
            if (Team2.matchups[i] == '49ers' or Team2.matchups[i] == 'Cardinals' or Team2.matchups[i] == 'Rams' or
                    Team2.matchups[i] == 'Seahawks'):
                divMatchups3_2.append(Team2.results[i])


    for i in range(17):
        if (Team3.getDivision() == 'AFCE'):
            if (Team3.matchups[i] == 'Bills' or Team3.matchups[i] == 'Jets' or Team3.matchups[i] == 'Dolphins' or
                    Team3.matchups[i] == 'Patriots'):
                divMatchups3_3.append(Team3.results[i])
        elif (Team3.getDivision() == 'AFCN'):
            if (Team3.matchups[i] == 'Bengals' or Team3.matchups[i] == 'Bills' or Team3.matchups[i] == 'Ravens' or
                    Team3.matchups[i] == 'Steelers'):
                divMatchups3_2.append(Team3.results[i])
        elif (Team3.getDivision() == 'AFCS'):
            if (Team3.matchups[i] == 'Colts' or Team3.matchups[i] == 'Jaguars' or Team3.matchups[i] == 'Titans' or
                    Team3.matchups[i] == 'Texans'):
                divMatchups3_2.append(Team3.results[i])
        elif (Team3.getDivision() == 'AFCW'):
            if (Team3.matchups[i] == 'Broncos' or Team3.matchups[i] == 'Chiefs' or Team3.matchups[i] == 'Chargers' or
                    Team3.matchups[i] == 'Raiders'):
                divMatchups3_2.append(Team3.results[i])
        elif (Team3.getDivision() == 'NFCE'):
            if (Team3.matchups[i] == 'Cowboys' or Team3.matchups[i] == 'Commanders' or Team3.matchups[i] == 'Eagles' or
                    Team3.matchups[i] == 'Giants'):
                divMatchups3_2.append(Team3.results[i])
        elif (Team3.getDivision() == 'NFCN'):
            if (Team3.matchups[i] == 'Bears' or Team3.matchups[i] == 'Lions' or Team3.matchups[i] == 'Packers' or
                    Team3.matchups[i] == 'Vikings'):
                divMatchups3_2.append(Team3.results[i])
        elif (Team3.getDivision() == 'NFCS'):
            if (Team3.matchups[i] == 'Buccaneers' or Team3.matchups[i] == 'Falcons' or Team3.matchups[i] == 'Saints' or
                    Team3.matchups[i] == 'Panthers'):
                divMatchups3_2.append(Team3.results[i])
        elif (Team3.getDivision() == 'NFCW'):
            if (Team3.matchups[i] == '49ers' or Team3.matchups[i] == 'Cardinals' or Team3.matchups[i] == 'Rams' or
                    Team3.matchups[i] == 'Seahawks'):
                divMatchups3_2.append(Team3.results[i])

    if (divMatchups3_1.count('W') == divMatchups3_2.count('W') and divMatchups3_1.count('W') == divMatchups3_3.count(
            'W')):
        return (False)
    else:
        return (True)


def divRecord3(Team1, Team2, Team3):
    order = []
    wins1 = divMatchups3_1.count('W')
    wins2 = divMatchups3_2.count('W')
    wins3 = divMatchups3_3.count('W')
    if (wins1 > wins2 and wins3 > wins1):
        order = [Team3, Team1, Team2]

    elif (wins2 > wins1 and wins3 > wins2):
        order = [Team3, Team2, Team1]

    elif (wins2 > wins3 and wins1 > wins2):
        order = [Team1, Team2, Team3]

    elif (wins3 > wins2 and wins1 > wins3):
        order = [Team1, Team3, Team2]

    elif (wins3 > wins1 and wins2 > wins3):
        order = [Team2, Team3, Team1]

    elif (wins1 > wins3 and wins2 > wins1):
        order = [Team2, Team1, Team3]

    elif (wins1 == wins2 and wins1 > wins3):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3]

    elif (wins1 == wins3 and wins1 > wins2):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2]

    elif (wins3 == wins2 and wins3 > wins1):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1]

    elif (wins1 == wins2 and wins1 < wins3):
        result = tiebreak2(Team1, Team2)
        order = [Team3, result[0], result[1]]

    elif (wins1 == wins3 and wins1 < wins2):
        result = tiebreak2(Team1, Team3)
        order = [Team2, result[0], result[1]]

    elif (wins3 == wins2 and wins3 < wins1):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1]]
    
    #print ("Order of div record 3 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName())
    return (order)


divMatchups4_1 = []
divMatchups4_2 = []
divMatchups4_3 = []
divMatchups4_4 = []


def isDivRecord4(Team1, Team2, Team3, Team4):
    global divMatchups4_1, divMatchups4_2, divMatchups4_3, divMatchups4_4
    divMatchups4_1 = []
    divMatchups4_2 = []
    divMatchups4_3 = []
    divMatchups4_4 = []
    for i in range(17):
        if (Team1.getDivision() == 'AFCE'):
            if (Team1.matchups[i] == 'Bills' or Team1.matchups[i] == 'Jets' or Team1.matchups[i] == 'Dolphins' or
                    Team1.matchups[i] == 'Patriots'):
                divMatchups4_1.append(Team1.results[i])
        elif (Team1.getDivision == 'AFCN'):
            if (Team1.matchups[i] == 'Bengals' or Team1.matchups[i] == 'Bills' or Team1.matchups[i] == 'Ravens' or
                    Team1.matchups[i] == 'Steelers'):
                divMatchups4_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'AFCS'):
            if (Team1.matchups[i] == 'Colts' or Team1.matchups[i] == 'Jaguars' or Team1.matchups[i] == 'Titans' or
                    Team1.matchups[i] == 'Texans'):
                divMatchups4_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'AFCW'):
            if (Team1.matchups[i] == 'Broncos' or Team1.matchups[i] == 'Chiefs' or Team1.matchups[i] == 'Chargers' or
                    Team1.matchups[i] == 'Raiders'):
                divMatchups4_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCE'):
            if (Team1.matchups[i] == 'Cowboys' or Team1.matchups[i] == 'Commanders' or Team1.matchups[i] == 'Eagles' or
                    Team1.matchups[i] == 'Giants'):
                divMatchups4_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCN'):
            if (Team1.matchups[i] == 'Bears' or Team1.matchups[i] == 'Lions' or Team1.matchups[i] == 'Packers' or
                    Team1.matchups[i] == 'Vikings'):
                divMatchups4_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCS'):
            if (Team1.matchups[i] == 'Buccaneers' or Team1.matchups[i] == 'Falcons' or Team1.matchups[i] == 'Saints' or
                    Team1.matchups[i] == 'Panthers'):
                divMatchups4_1.append(Team1.results[i])
        elif (Team1.getDivision() == 'NFCW'):
            if (Team1.matchups[i] == '49ers' or Team1.matchups[i] == 'Cardinals' or Team1.matchups[i] == 'Rams' or
                    Team1.matchups[i] == 'Seahawks'):
                divMatchups4_1.append(Team1.results[i])
                # Need to copy over every division

    for i in range(17):
        if (Team2.getDivision() == 'AFCE'):
            if (Team2.matchups[i] == 'Bills' or Team2.matchups[i] == 'Jets' or Team2.matchups[i] == 'Dolphins' or
                    Team2.matchups[i] == 'Patriots'):
                divMatchups4_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'AFCN'):
            if (Team2.matchups[i] == 'Bengals' or Team2.matchups[i] == 'Bills' or Team2.matchups[i] == 'Ravens' or
                    Team2.matchups[i] == 'Steelers'):
                divMatchups4_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'AFCS'):
            if (Team2.matchups[i] == 'Colts' or Team2.matchups[i] == 'Jaguars' or Team2.matchups[i] == 'Titans' or
                    Team2.matchups[i] == 'Texans'):
                divMatchups4_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'AFCW'):
            if (Team2.matchups[i] == 'Broncos' or Team2.matchups[i] == 'Chiefs' or Team2.matchups[i] == 'Chargers' or
                    Team2.matchups[i] == 'Raiders'):
                divMatchups4_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCE'):
            if (Team2.matchups[i] == 'Cowboys' or Team2.matchups[i] == 'Commanders' or Team2.matchups[i] == 'Eagles' or
                    Team2.matchups[i] == 'Giants'):
                divMatchups4_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCN'):
            if (Team2.matchups[i] == 'Bears' or Team2.matchups[i] == 'Lions' or Team2.matchups[i] == 'Packers' or
                    Team2.matchups[i] == 'Vikings'):
                divMatchups4_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCS'):
            if (Team2.matchups[i] == 'Buccaneers' or Team2.matchups[i] == 'Falcons' or Team2.matchups[i] == 'Saints' or
                    Team2.matchups[i] == 'Panthers'):
                divMatchups4_2.append(Team2.results[i])
        elif (Team2.getDivision() == 'NFCW'):
            if (Team2.matchups[i] == '49ers' or Team2.matchups[i] == 'Cardinals' or Team2.matchups[i] == 'Rams' or
                    Team2.matchups[i] == 'Seahawks'):
                divMatchups4_2.append(Team2.results[i])

    for i in range(17):
        if (Team3.getDivision() == 'AFCE'):
            if (Team3.matchups[i] == 'Bills' or Team3.matchups[i] == 'Jets' or Team3.matchups[i] == 'Dolphins' or
                    Team3.matchups[i] == 'Patriots'):
                divMatchups4_3.append(Team3.results[i])
        elif (Team3.getDivision() == 'AFCN'):
            if (Team3.matchups[i] == 'Bengals' or Team3.matchups[i] == 'Bills' or Team3.matchups[i] == 'Ravens' or
                    Team3.matchups[i] == 'Steelers'):
                divMatchups4_3.append(Team3.results[i])
        elif (Team3.getDivision() == 'AFCS'):
            if (Team3.matchups[i] == 'Colts' or Team3.matchups[i] == 'Jaguars' or Team3.matchups[i] == 'Titans' or
                    Team3.matchups[i] == 'Texans'):
                divMatchups4_3.append(Team3.results[i])
        elif (Team3.getDivision() == 'AFCW'):
            if (Team3.matchups[i] == 'Broncos' or Team3.matchups[i] == 'Chiefs' or Team3.matchups[i] == 'Chargers' or
                    Team3.matchups[i] == 'Raiders'):
                divMatchups4_3.append(Team3.results[i])
        elif (Team3.getDivision() == 'NFCE'):
            if (Team3.matchups[i] == 'Cowboys' or Team3.matchups[i] == 'Commanders' or Team3.matchups[i] == 'Eagles' or
                    Team3.matchups[i] == 'Giants'):
                divMatchups4_3.append(Team3.results[i])
        elif (Team3.getDivision() == 'NFCN'):
            if (Team3.matchups[i] == 'Bears' or Team3.matchups[i] == 'Lions' or Team3.matchups[i] == 'Packers' or
                    Team3.matchups[i] == 'Vikings'):
                divMatchups4_3.append(Team3.results[i])
        elif (Team3.getDivision() == 'NFCS'):
            if (Team3.matchups[i] == 'Buccaneers' or Team3.matchups[i] == 'Falcons' or Team3.matchups[i] == 'Saints' or
                    Team3.matchups[i] == 'Panthers'):
                divMatchups4_3.append(Team3.results[i])
        elif (Team3.getDivision() == 'NFCW'):
            if (Team3.matchups[i] == '49ers' or Team3.matchups[i] == 'Cardinals' or Team3.matchups[i] == 'Rams' or
                    Team3.matchups[i] == 'Seahawks'):
                divMatchups4_3.append(Team3.results[i])


    for i in range(17):
        if (Team4.getDivision() == 'AFCE'):
            if (Team4.matchups[i] == 'Bills' or Team4.matchups[i] == 'Jets' or Team4.matchups[i] == 'Dolphins' or
                    Team4.matchups[i] == 'Patriots'):
                divMatchups4_4.append(Team4.results[i])
        elif (Team4.getDivision() == 'AFCN'):
            if (Team4.matchups[i] == 'Bengals' or Team4.matchups[i] == 'Bills' or Team4.matchups[i] == 'Ravens' or
                    Team4.matchups[i] == 'Steelers'):
                divMatchups4_4.append(Team4.results[i])
        elif (Team4.getDivision() == 'AFCS'):
            if (Team4.matchups[i] == 'Colts' or Team4.matchups[i] == 'Jaguars' or Team4.matchups[i] == 'Titans' or
                    Team4.matchups[i] == 'Texans'):
                divMatchups4_4.append(Team4.results[i])
        elif (Team4.getDivision() == 'AFCW'):
            if (Team4.matchups[i] == 'Broncos' or Team4.matchups[i] == 'Chiefs' or Team4.matchups[i] == 'Chargers' or
                    Team4.matchups[i] == 'Raiders'):
                divMatchups4_4.append(Team4.results[i])
        elif (Team4.getDivision() == 'NFCE'):
            if (Team4.matchups[i] == 'Cowboys' or Team4.matchups[i] == 'Commanders' or Team4.matchups[i] == 'Eagles' or
                    Team4.matchups[i] == 'Giants'):
                divMatchups4_4.append(Team4.results[i])
        elif (Team4.getDivision() == 'NFCN'):
            if (Team4.matchups[i] == 'Bears' or Team4.matchups[i] == 'Lions' or Team4.matchups[i] == 'Packers' or
                    Team4.matchups[i] == 'Vikings'):
                divMatchups4_4.append(Team4.results[i])
        elif (Team4.getDivision() == 'NFCS'):
            if (Team4.matchups[i] == 'Buccaneers' or Team4.matchups[i] == 'Falcons' or Team4.matchups[i] == 'Saints' or
                    Team4.matchups[i] == 'Panthers'):
                divMatchups4_4.append(Team4.results[i])
        elif (Team4.getDivision() == 'NFCW'):
            if (Team4.matchups[i] == '49ers' or Team4.matchups[i] == 'Cardinals' or Team4.matchups[i] == 'Rams' or
                    Team4.matchups[i] == 'Seahawks'):
                divMatchups4_4.append(Team4.results[i])

    if (divMatchups4_1.count('W') == divMatchups4_2.count('W') and divMatchups4_1.count('W') == divMatchups4_3.count(
            'W') and
            divMatchups4_1.count('W') == divMatchups4_4.count('W')):
        return (False)
    else:
        return (True)


def divRecord4(Team1, Team2, Team3, Team4):
    order = []
    wins1 = divMatchups4_1.count('W')
    wins2 = divMatchups4_2.count('W')
    wins3 = divMatchups4_3.count('W')
    wins4 = divMatchups4_4.count('W')

    if (wins1 > wins2 and wins2 > wins3 and wins3 > wins4):
        order = [Team1, Team2, Team3, Team4]

    elif (wins1 > wins2 and wins2 > wins4 and wins4 > wins3):
        order = [Team1, Team2, Team4, Team3]

    elif (wins1 > wins3 and wins3 > wins2 and wins2 > wins4):
        order = [Team1, Team3, Team2, Team4]

    elif (wins1 > wins3 and wins3 > wins4 and wins4 > wins2):
        order = [Team1, Team3, Team4, Team2]

    elif (wins1 > wins4 and wins4 > wins3 and wins3 > wins2):
        order = [Team1, Team4, Team3, Team2]

    elif (wins1 > wins4 and wins4 > wins2 and wins2 > wins3):
        order = [Team1, Team4, Team2, Team3]

    elif (wins2 > wins1 and wins1 > wins4 and wins4 > wins3):
        order = [Team2, Team1, Team4, Team3]

    elif (wins2 > wins1 and wins1 > wins3 and wins3 > wins4):
        order = [Team2, Team1, Team3, Team4]

    elif (wins2 > wins3 and wins3 > wins1 and wins1 > wins4):
        order = [Team2, Team3, Team1, Team4]

    elif (wins2 > wins3 and wins3 > wins4 and wins4 > wins1):
        order = [Team2, Team3, Team4, Team1]

    elif (wins2 > wins4 and wins4 > wins1 and wins1 > wins3):
        order = [Team2, Team4, Team1, Team3]

    elif (wins2 > wins4 and wins4 > wins3 and wins3 > wins1):
        order = [Team2, Team4, Team3, Team1]

    elif (wins3 > wins1 and wins1 > wins2 and wins2 > wins4):
        order = [Team3, Team1, Team2, Team4]

    elif (wins3 > wins1 and wins1 > wins4 and wins4 > wins2):
        order = [Team3, Team1, Team4, Team2]

    elif (wins3 > wins2 and wins2 > wins1 and wins1 > wins4):
        order = [Team3, Team2, Team1, Team4]

    elif (wins3 > wins2 and wins2 > wins4 and wins4 > wins1):
        order = [Team3, Team2, Team4, Team1]

    elif (wins3 > wins4 and wins4 > wins1 and wins1 > wins2):
        order = [Team3, Team4, Team1, Team2]

    elif (wins3 > wins4 and wins4 > wins2 and wins2 > wins1):
        order = [Team3, Team4, Team2, Team1]

    elif (wins4 > wins1 and wins1 > wins3 and wins3 > wins2):
        order = [Team4, Team1, Team3, Team2]

    elif (wins4 > wins1 and wins1 > wins2 and wins2 > wins3):
        order = [Team4, Team1, Team2, Team3]

    elif (wins4 > wins3 and wins3 > wins1 and wins1 > wins2):
        order = [Team4, Team3, Team1, Team2]

    elif (wins4 > wins3 and wins3 > wins2 and wins2 > wins1):
        order = [Team4, Team3, Team2, Team1]

    elif (wins4 > wins2 and wins2 > wins3 and wins3 > wins1):
        order = [Team4, Team2, Team3, Team1]

    elif (wins4 > wins2 and wins2 > wins1 and wins1 > wins3):
        order = [Team4, Team2, Team1, Team3]

    elif (wins1 > wins2 and wins2 > wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team1, Team2, result[0], result[1]]

    elif (wins2 > wins1 and wins2 > wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team2, Team1, result[0], result[1]]

    elif (wins1 > wins3 and wins3 > wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team1, Team3, result[0], result[1]]

    elif (wins3 > wins1 and wins1 > wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team3, Team1, result[0], result[1]]

    elif (wins1 > wins4 and wins4 > wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [Team1, Team4, result[0], result[1]]

    elif (wins4 > wins1 and wins1 > wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [Team4, Team1, result[0], result[1]]

    elif (wins2 > wins3 and wins3 > wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [Team2, Team3, result[0], result[1]]

    elif (wins3 > wins2 and wins2 > wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [Team3, Team2, result[0], result[1]]

    elif (wins2 > wins4 and wins4 > wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [Team2, Team4, result[0], result[1]]

    elif (wins4 > wins2 and wins2 > wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [Team4, Team2, result[0], result[1]]

    elif (wins3 > wins4 and wins4 > wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [Team2, Team4, result[0], result[1]]

    elif (wins4 > wins3 and wins3 > wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [Team4, Team3, result[0], result[1]]

    elif (wins1 < wins2 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [result[0], result[1], Team2, Team1]

    elif (wins2 < wins1 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [result[0], result[1], Team1, Team2]

    elif (wins1 < wins3 and wins3 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [result[0], result[1], Team3, Team1]

    elif (wins3 < wins1 and wins1 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [result[0], result[1], Team1, Team3]

    elif (wins1 < wins4 and wins4 < wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team4, Team1]

    elif (wins4 < wins1 and wins1 < wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1, Team4]

    elif (wins2 < wins3 and wins3 < wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [result[0], result[1], Team3, Team2]

    elif (wins3 < wins2 and wins2 < wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [result[0], result[1], Team2, Team3]

    elif (wins2 < wins4 and wins4 < wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team4, Team2]

    elif (wins4 < wins2 and wins2 < wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2, Team4]

    elif (wins3 < wins4 and wins4 < wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team4, Team3]

    elif (wins4 < wins3 and wins3 < wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3, Team4]

    elif (wins1 > wins2 and wins2 == wins3 and wins2 == wins4):
        result = tiebreak3(Team2, Team3, Team4)
        order = [Team1, result[0], result[1], result[2]]

    elif (wins2 > wins1 and wins1 == wins3 and wins1 == wins4):
        result = tiebreak3(Team1, Team3, Team4)
        order = [Team2, result[0], result[1], result[2]]

    elif (wins3 > wins2 and wins2 == wins1 and wins2 == wins4):
        result = tiebreak3(Team2, Team1, Team4)
        order = [Team3, result[0], result[1], result[2]]

    elif (wins4 > wins2 and wins2 == wins3 and wins2 == wins1):
        result = tiebreak3(Team2, Team3, Team1)
        order = [Team4, result[0], result[1], result[2]]

    elif (wins1 < wins2 and wins2 == wins3 and wins2 == wins4):
        result = tiebreak3(Team2, Team3, Team4)
        order = [result[0], result[1], result[2], Team1]

    elif (wins2 < wins1 and wins1 == wins3 and wins1 == wins4):
        result = tiebreak3(Team1, Team3, Team4)
        order = [result[0], result[1], result[2], Team2]

    elif (wins3 < wins2 and wins2 == wins1 and wins2 == wins4):
        result = tiebreak3(Team2, Team1, Team4)
        order = [result[0], result[1], result[2], Team3]

    elif (wins4 < wins2 and wins2 == wins3 and wins2 == wins1):
        result = tiebreak3(Team2, Team3, Team1)
        order = [result[0], result[1], result[2], Team4]

    elif (wins1 > wins3 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team1, result[0], result[1], Team2]

    elif (wins2 > wins3 and wins1 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team2, result[0], result[1], Team1]

    elif (wins1 > wins2 and wins3 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team1, result[0], result[1], Team3]

    elif (wins3 > wins2 and wins1 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team3, result[0], result[1], Team1]

    elif (wins1 > wins3 and wins4 < wins3 and wins3 == wins2):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1], Team4]

    elif (wins4 > wins3 and wins1 < wins3 and wins3 == wins2):
        result = tiebreak2(Team3, Team2)
        order = [Team4, result[0], result[1], Team1]

    elif (wins2 > wins4 and wins3 < wins4 and wins4 == wins1):
        result = tiebreak2(Team4, Team1)
        order = [Team2, result[0], result[1], Team3]

    elif (wins3 > wins4 and wins2 < wins4 and wins4 == wins1):
        result = tiebreak2(Team4, Team1)
        order = [Team3, result[0], result[1], Team2]

    elif (wins2 > wins3 and wins4 < wins3 and wins3 == wins1):
        result = tiebreak2(Team3, Team1)
        order = [Team2, result[0], result[1], Team4]

    elif (wins4 > wins3 and wins2 < wins3 and wins3 == wins1):
        result = tiebreak2(Team3, Team1)
        order = [Team4, result[0], result[1], Team2]

    elif (wins3 > wins2 and wins4 < wins2 and wins2 == wins1):
        result = tiebreak2(Team2, Team1)
        order = [Team3, result[0], result[1], Team4]

    elif (wins4 > wins2 and wins3 < wins2 and wins2 == wins1):
        result = tiebreak2(Team2, Team1)
        order = [Team4, result[0], result[1], Team3]

    elif (wins1 == wins2 and wins3 == wins4 and wins1 > wins3):
        result1 = tiebreak2(Team1, Team2)
        result2 = tiebreak2(Team3, Team4)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins2 and wins3 == wins4 and wins1 < wins3):
        result1 = tiebreak2(Team1, Team2)
        result2 = tiebreak2(Team3, Team4)
        order = [result2[0], result2[1], result1[0], result1[1]]

    elif (wins1 == wins3 and wins2 == wins4 and wins1 > wins2):
        result1 = tiebreak2(Team1, Team3)
        result2 = tiebreak2(Team2, Team4)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins3 and wins2 == wins4 and wins1 < wins2):
        result1 = tiebreak2(Team1, Team3)
        result2 = tiebreak2(Team2, Team4)
        order = [result2[0], result2[1], result1[0], result1[1]]

    elif (wins1 == wins4 and wins2 == wins3 and wins1 > wins2):
        result1 = tiebreak2(Team1, Team4)
        result2 = tiebreak2(Team2, Team3)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins4 and wins2 == wins3 and wins1 < wins2):
        result1 = tiebreak2(Team1, Team4)
        result2 = tiebreak2(Team2, Team3)
        order = [result2[0], result2[1], result1[0], result1[1]]
    else: 
        print ("div record didn't work")
        order = [Team1, Team2, Team3, Team4]
    
    #print ("Order of div record 4 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName() + ", " + order[3].getName())
    return (order)


common2_1 = []
common2_2 = []


def isCommonRecord2(Team1, Team2):
    global common2_1, common2_2
    common2_1 = []
    common2_2 = []
    unqMatchups1 = list(set(Team1.matchups))
    unqMatchups2 = list(set(Team2.matchups))
    for i in range(14):
        if (Team2.matchups.count(unqMatchups1[i]) > 0):
            opponent = unqMatchups1[i]
            for j in range(17):
                if (Team2.matchups[j] == opponent):
                    common2_2.append(Team2.results[j])
    for i in range(14):
        if (Team1.matchups.count(unqMatchups2[i]) > 0):
            opponent = unqMatchups2[i]
            for j in range(17):
                if (Team1.matchups[j] == opponent):
                    common2_1.append(Team1.results[j])

    if (common2_1.count('W') == common2_2.count('W') or len(common2_1) < 4):
        return (False)
    else:
        return (True)


def commonRecord2(Team1, Team2):
    if (common2_1.count('W') > common2_2.count('W')):
        #print (Team1.getName() + " wins on common record over " + Team2.getName())
        return (Team1)
    else:
        #print (Team2.getName() + " wins on common record over " + Team1.getName())
        return (Team2)


common3_1 = []
common3_2 = []
common3_3 = []


def isCommonRecord3(Team1, Team2, Team3):
    global common3_1, common3_2, common3_3
    common3_1 = []
    common3_2 = []
    common3_3 = []
    unqMatchups1 = list(set(Team1.matchups))
    #unqMatchups2 = list(set(Team2.matchups))
    #unqMatchups3 = list(set(Team3.matchups))
    for i in range(14):
        if (Team2.matchups.count(unqMatchups1[i]) > 0 and Team3.matchups.count(unqMatchups1[i]) > 0):
            opponent = unqMatchups1[i]
            for j in range(17):
                if (Team1.matchups[j] == opponent):
                    common3_1.append(Team1.results[j])
                if (Team2.matchups[j] == opponent):
                    common3_2.append(Team2.results[j])
                if (Team3.matchups[j] == opponent):
                    common3_3.append(Team3.results[j])
                    
    #print (common3_1)
    #print (common3_2)
    #print (common3_3)

    if (common3_1.count('W') == common3_2.count('W') and common3_1.count('W') == common3_3.count('W') or len(
            common3_1) < 4):
        return (False)
    else:
        return (True)


def commonRecord3(Team1, Team2, Team3):
    order = []
    wins1 = common3_1.count('W')
    wins2 = common3_2.count('W')
    wins3 = common3_3.count('W')
    if (wins1 > wins2 and wins3 > wins1):
        order = [Team3, Team1, Team2]

    elif (wins2 > wins1 and wins3 > wins2):
        order = [Team3, Team2, Team1]

    elif (wins2 > wins3 and wins1 > wins2):
        order = [Team1, Team2, Team3]

    elif (wins3 > wins2 and wins1 > wins3):
        order = [Team1, Team3, Team2]

    elif (wins3 > wins1 and wins2 > wins3):
        order = [Team2, Team3, Team1]

    elif (wins1 > wins3 and wins2 > wins1):
        order = [Team2, Team1, Team3]

    elif (wins1 == wins2 and wins1 > wins3):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3]

    elif (wins1 == wins3 and wins1 > wins2):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2]

    elif (wins3 == wins2 and wins3 > wins1):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1]

    elif (wins1 == wins2 and wins1 < wins3):
        result = tiebreak2(Team1, Team2)
        order = [Team3, result[0], result[1]]

    elif (wins1 == wins3 and wins1 < wins2):
        result = tiebreak2(Team1, Team3)
        order = [Team2, result[0], result[1]]

    elif (wins3 == wins2 and wins3 < wins1):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1]]
    else: 
        order = [Team1, Team2, Team3]
        print ("common opponents 3 isn't working")
        
    #print ("Order of common record 3 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName())
    return (order)


common4_1 = []
common4_2 = []
common4_3 = []
common4_4 = []


def isCommonRecord4(Team1, Team2, Team3, Team4):
    global common4_1, common4_2, common4_3, common4_4
    common4_1 = []
    common4_2 = []
    common4_3 = []
    common4_4 = []
    unqMatchups1 = list(set(Team1.matchups))
    #unqMatchups2 = list(set(Team2.matchups))
    #unqMatchups3 = list(set(Team3.matchups))
    for i in range(14):
        if (Team2.matchups.count(unqMatchups1[i]) > 0 and Team3.matchups.count(unqMatchups1[i]) > 0 and 
            Team4.matchups.count(unqMatchups1[i]) > 0):
            opponent = unqMatchups1[i]
            for j in range(17):
                if (Team1.matchups[j] == opponent):
                    common4_1.append(Team1.results[j])
                if (Team2.matchups[j] == opponent):
                    common4_2.append(Team2.results[j])
                if (Team3.matchups[j] == opponent):
                    common4_3.append(Team3.results[j])
                if (Team4.matchups[j] == opponent):
                    common4_4.append(Team4.results[j])
                    
    #print (common4_1)
    #print (common4_2)
    #print (common4_3)
    #print (common4_4)

    if (common4_1.count('W') == common4_2.count('W') and common4_1.count('W') == common4_3.count('W') and
            common4_1.count('W') == common4_4.count('W') or len(common4_1) < 4):
        return (False)
    else:
        return (True)


def commonRecord4(Team1, Team2, Team3, Team4):
    order = []
    wins1 = common4_1.count('W')
    wins2 = common4_2.count('W')
    wins3 = common4_3.count('W')
    wins4 = common4_4.count('W')

    if (wins1 > wins2 and wins2 > wins3 and wins3 > wins4):
        order = [Team1, Team2, Team3, Team4]

    elif (wins1 > wins2 and wins2 > wins4 and wins4 > wins3):
        order = [Team1, Team2, Team4, Team3]

    elif (wins1 > wins3 and wins3 > wins2 and wins2 > wins4):
        order = [Team1, Team3, Team2, Team4]

    elif (wins1 > wins3 and wins3 > wins4 and wins4 > wins2):
        order = [Team1, Team3, Team4, Team2]

    elif (wins1 > wins4 and wins4 > wins3 and wins3 > wins2):
        order = [Team1, Team4, Team3, Team2]

    elif (wins1 > wins4 and wins4 > wins2 and wins2 > wins3):
        order = [Team1, Team4, Team2, Team3]

    elif (wins2 > wins1 and wins1 > wins4 and wins4 > wins3):
        order = [Team2, Team1, Team4, Team3]

    elif (wins2 > wins1 and wins1 > wins3 and wins3 > wins4):
        order = [Team2, Team1, Team3, Team4]

    elif (wins2 > wins3 and wins3 > wins1 and wins1 > wins4):
        order = [Team2, Team3, Team1, Team4]

    elif (wins2 > wins3 and wins3 > wins4 and wins4 > wins1):
        order = [Team2, Team3, Team4, Team1]

    elif (wins2 > wins4 and wins4 > wins1 and wins1 > wins3):
        order = [Team2, Team4, Team1, Team3]

    elif (wins2 > wins4 and wins4 > wins3 and wins3 > wins1):
        order = [Team2, Team4, Team3, Team1]

    elif (wins3 > wins1 and wins1 > wins2 and wins2 > wins4):
        order = [Team3, Team1, Team2, Team4]

    elif (wins3 > wins1 and wins1 > wins4 and wins4 > wins2):
        order = [Team3, Team1, Team4, Team2]

    elif (wins3 > wins2 and wins2 > wins1 and wins1 > wins4):
        order = [Team3, Team2, Team1, Team4]

    elif (wins3 > wins2 and wins2 > wins4 and wins4 > wins1):
        order = [Team3, Team2, Team4, Team1]

    elif (wins3 > wins4 and wins4 > wins1 and wins1 > wins2):
        order = [Team3, Team4, Team1, Team2]

    elif (wins3 > wins4 and wins4 > wins2 and wins2 > wins1):
        order = [Team3, Team4, Team2, Team1]

    elif (wins4 > wins1 and wins1 > wins3 and wins3 > wins2):
        order = [Team4, Team1, Team3, Team2]

    elif (wins4 > wins1 and wins1 > wins2 and wins2 > wins3):
        order = [Team4, Team1, Team2, Team3]

    elif (wins4 > wins3 and wins3 > wins1 and wins1 > wins2):
        order = [Team4, Team3, Team1, Team2]

    elif (wins4 > wins3 and wins3 > wins2 and wins2 > wins1):
        order = [Team4, Team3, Team2, Team1]

    elif (wins4 > wins2 and wins2 > wins3 and wins3 > wins1):
        order = [Team4, Team2, Team3, Team1]

    elif (wins4 > wins2 and wins2 > wins1 and wins1 > wins3):
        order = [Team4, Team2, Team1, Team3]

    elif (wins1 > wins2 and wins2 > wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team1, Team2, result[0], result[1]]

    elif (wins2 > wins1 and wins2 > wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team2, Team1, result[0], result[1]]

    elif (wins1 > wins3 and wins3 > wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team1, Team3, result[0], result[1]]

    elif (wins3 > wins1 and wins1 > wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team3, Team1, result[0], result[1]]

    elif (wins1 > wins4 and wins4 > wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [Team1, Team4, result[0], result[1]]

    elif (wins4 > wins1 and wins1 > wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [Team4, Team1, result[0], result[1]]

    elif (wins2 > wins3 and wins3 > wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [Team2, Team3, result[0], result[1]]

    elif (wins3 > wins2 and wins2 > wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [Team3, Team2, result[0], result[1]]

    elif (wins2 > wins4 and wins4 > wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [Team2, Team4, result[0], result[1]]

    elif (wins4 > wins2 and wins2 > wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [Team4, Team2, result[0], result[1]]

    elif (wins3 > wins4 and wins4 > wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [Team2, Team4, result[0], result[1]]

    elif (wins4 > wins3 and wins3 > wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [Team4, Team3, result[0], result[1]]

    elif (wins1 < wins2 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [result[0], result[1], Team2, Team1]

    elif (wins2 < wins1 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [result[0], result[1], Team1, Team2]

    elif (wins1 < wins3 and wins3 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [result[0], result[1], Team3, Team1]

    elif (wins3 < wins1 and wins1 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [result[0], result[1], Team1, Team3]

    elif (wins1 < wins4 and wins4 < wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team4, Team1]

    elif (wins4 < wins1 and wins1 < wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1, Team4]

    elif (wins2 < wins3 and wins3 < wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [result[0], result[1], Team3, Team2]

    elif (wins3 < wins2 and wins2 < wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [result[0], result[1], Team2, Team3]

    elif (wins2 < wins4 and wins4 < wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team4, Team2]

    elif (wins4 < wins2 and wins2 < wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2, Team4]

    elif (wins3 < wins4 and wins4 < wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team4, Team3]

    elif (wins4 < wins3 and wins3 < wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3, Team4]

    elif (wins1 > wins2 and wins2 == wins3 and wins2 == wins4):
        result = tiebreak3(Team2, Team3, Team4)
        order = [Team1, result[0], result[1], result[2]]

    elif (wins2 > wins1 and wins1 == wins3 and wins1 == wins4):
        result = tiebreak3(Team1, Team3, Team4)
        order = [Team2, result[0], result[1], result[2]]

    elif (wins3 > wins2 and wins2 == wins1 and wins2 == wins4):
        result = tiebreak3(Team2, Team1, Team4)
        order = [Team3, result[0], result[1], result[2]]

    elif (wins4 > wins2 and wins2 == wins3 and wins2 == wins1):
        result = tiebreak3(Team2, Team3, Team1)
        order = [Team4, result[0], result[1], result[2]]

    elif (wins1 < wins2 and wins2 == wins3 and wins2 == wins4):
        result = tiebreak3(Team2, Team3, Team4)
        order = [result[0], result[1], result[2], Team1]

    elif (wins2 < wins1 and wins1 == wins3 and wins1 == wins4):
        result = tiebreak3(Team1, Team3, Team4)
        order = [result[0], result[1], result[2], Team2]

    elif (wins3 < wins2 and wins2 == wins1 and wins2 == wins4):
        result = tiebreak3(Team2, Team1, Team4)
        order = [result[0], result[1], result[2], Team3]

    elif (wins4 < wins2 and wins2 == wins3 and wins2 == wins1):
        result = tiebreak3(Team2, Team3, Team1)
        order = [result[0], result[1], result[2], Team4]

    elif (wins1 > wins3 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team1, result[0], result[1], Team2]

    elif (wins2 > wins3 and wins1 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team2, result[0], result[1], Team1]

    elif (wins1 > wins2 and wins3 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team1, result[0], result[1], Team3]

    elif (wins3 > wins2 and wins1 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team3, result[0], result[1], Team1]

    elif (wins1 > wins3 and wins4 < wins3 and wins3 == wins2):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1], Team4]

    elif (wins4 > wins3 and wins1 < wins3 and wins3 == wins2):
        result = tiebreak2(Team3, Team2)
        order = [Team4, result[0], result[1], Team1]

    elif (wins2 > wins4 and wins3 < wins4 and wins4 == wins1):
        result = tiebreak2(Team4, Team1)
        order = [Team2, result[0], result[1], Team3]

    elif (wins3 > wins4 and wins2 < wins4 and wins4 == wins1):
        result = tiebreak2(Team4, Team1)
        order = [Team3, result[0], result[1], Team2]

    elif (wins2 > wins3 and wins4 < wins3 and wins3 == wins1):
        result = tiebreak2(Team3, Team1)
        order = [Team2, result[0], result[1], Team4]

    elif (wins4 > wins3 and wins2 < wins3 and wins3 == wins1):
        result = tiebreak2(Team3, Team1)
        order = [Team4, result[0], result[1], Team2]

    elif (wins3 > wins2 and wins4 < wins2 and wins2 == wins1):
        result = tiebreak2(Team2, Team1)
        order = [Team3, result[0], result[1], Team4]

    elif (wins4 > wins2 and wins3 < wins2 and wins2 == wins1):
        result = tiebreak2(Team2, Team1)
        order = [Team4, result[0], result[1], Team3]

    elif (wins1 == wins2 and wins3 == wins4 and wins1 > wins3):
        result1 = tiebreak2(Team1, Team2)
        result2 = tiebreak2(Team3, Team4)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins2 and wins3 == wins4 and wins1 < wins3):
        result1 = tiebreak2(Team1, Team2)
        result2 = tiebreak2(Team3, Team4)
        order = [result2[0], result2[1], result1[0], result1[1]]

    elif (wins1 == wins3 and wins2 == wins4 and wins1 > wins2):
        result1 = tiebreak2(Team1, Team3)
        result2 = tiebreak2(Team2, Team4)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins3 and wins2 == wins4 and wins1 < wins2):
        result1 = tiebreak2(Team1, Team3)
        result2 = tiebreak2(Team2, Team4)
        order = [result2[0], result2[1], result1[0], result1[1]]

    elif (wins1 == wins4 and wins2 == wins3 and wins1 > wins2):
        result1 = tiebreak2(Team1, Team4)
        result2 = tiebreak2(Team2, Team3)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins4 and wins2 == wins3 and wins1 < wins2):
        result1 = tiebreak2(Team1, Team4)
        result2 = tiebreak2(Team2, Team3)
        order = [result2[0], result2[1], result1[0], result1[1]]
    else:
        print ("common record 4 failed")
        order = [Team1, Team2, Team3, Team4]
    
    #print ("Order of common record 4 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName() + ", " + order[3].getName())
    return (order)


confMatchups2_1 = []
confMatchups2_2 = []


def isConfRecord2(Team1, Team2):
    global confMatchups2_1, confMatchups2_2
    confMatchups2_1 = []
    confMatchups2_2 = []
    for i in range(17):
        if (Team1.getConference() == 'AFC'):
            if (Team1.matchups[i] == 'Bills' or Team1.matchups[i] == 'Dolphins' or Team1.matchups[i] == 'Jets' or
                    Team1.matchups[i] == 'Browns' or Team1.matchups[i] == 'Bengals' or Team1.matchups[
                        i] == 'Steelers' or
                    Team1.matchups[i] == 'Ravens' or Team1.matchups[i] == 'Colts' or Team1.matchups[i] == 'Jaguars' or
                    Team1.matchups[i] == 'Titans' or Team1.matchups[i] == 'Texans' or Team1.matchups[i] == 'Broncos' or
                    Team1.matchups[i] == 'Chiefs' or Team1.matchups[i] == 'Chargers' or Team1.matchups[
                        i] == 'Raiders' or
                    Team1.matchups[i] == 'Patriots'):
                confMatchups2_1.append(Team1.results[i])
        elif (Team1.getConference() == 'NFC'):
            if (Team1.matchups[i] == 'Commanders' or Team1.matchups[i] == 'Cowboys' or Team1.matchups[i] == 'Giants' or
                    Team1.matchups[i] == 'Eagles' or Team1.matchups[i] == 'Bears' or Team1.matchups[i] == 'Lions' or
                    Team1.matchups[i] == 'Packers' or Team1.matchups[i] == 'Vikings' or Team1.matchups[
                        i] == 'Buccaneers' or
                    Team1.matchups[i] == 'Saints' or Team1.matchups[i] == 'Falcons' or Team1.matchups[
                        i] == 'Panthers' or
                    Team1.matchups[i] == '49ers' or Team1.matchups[i] == 'Cardinals' or Team1.matchups[
                        i] == 'Seahawks' or
                    Team1.matchups[i] == 'Rams'):
                confMatchups2_1.append(Team1.results[i])

    for i in range(17):
        if (Team2.getConference() == 'AFC'):
            if (Team2.matchups[i] == 'Bills' or Team2.matchups[i] == 'Dolphins' or Team2.matchups[i] == 'Jets' or
                    Team2.matchups[i] == 'Browns' or Team2.matchups[i] == 'Bengals' or Team2.matchups[
                        i] == 'Steelers' or
                    Team2.matchups[i] == 'Ravens' or Team2.matchups[i] == 'Colts' or Team2.matchups[i] == 'Jaguars' or
                    Team2.matchups[i] == 'Titans' or Team2.matchups[i] == 'Texans' or Team2.matchups[i] == 'Broncos' or
                    Team2.matchups[i] == 'Chiefs' or Team2.matchups[i] == 'Chargers' or Team2.matchups[
                        i] == 'Raiders' or
                    Team2.matchups[i] == 'Patriots'):
                confMatchups2_2.append(Team2.results[i])
        elif (Team2.getConference() == 'NFC'):
            if (Team2.matchups[i] == 'Commanders' or Team2.matchups[i] == 'Cowboys' or Team2.matchups[i] == 'Giants' or
                    Team2.matchups[i] == 'Eagles' or Team2.matchups[i] == 'Bears' or Team2.matchups[i] == 'Lions' or
                    Team2.matchups[i] == 'Packers' or Team2.matchups[i] == 'Vikings' or Team2.matchups[
                        i] == 'Buccaneers' or
                    Team2.matchups[i] == 'Saints' or Team2.matchups[i] == 'Falcons' or Team2.matchups[
                        i] == 'Panthers' or
                    Team2.matchups[i] == '49ers' or Team2.matchups[i] == 'Cardinals' or Team2.matchups[
                        i] == 'Seahawks' or
                    Team2.matchups[i] == 'Rams'):
                confMatchups2_2.append(Team2.results[i])

    if (confMatchups2_1.count('W') == confMatchups2_2.count('W')):
        return (False)
    else:
        return (True)


def confRecord2(Team1, Team2):
    if (confMatchups2_1.count('W') > confMatchups2_2.count('W')):
        #print (Team1.getName() + " wins on conf record over " + Team2.getName())
        return (Team1)
    else:
        #print (Team2.getName() + " wins on conf record over " + Team1.getName())
        return (Team2)


confMatchups3_1 = []
confMatchups3_2 = []
confMatchups3_3 = []


def isConfRecord3(Team1, Team2, Team3):
    global confMatchups3_1, confMatchups3_2, confMatchups3_3
    confMatchups3_1 = []
    confMatchups3_2 = []
    confMatchups3_3 = []
    for i in range(17):
        if (Team1.getConference() == 'AFC'):
            if (Team1.matchups[i] == 'Bills' or Team1.matchups[i] == 'Dolphins' or Team1.matchups[i] == 'Jets' or
                    Team1.matchups[i] == 'Browns' or Team1.matchups[i] == 'Bengals' or Team1.matchups[
                        i] == 'Steelers' or
                    Team1.matchups[i] == 'Ravens' or Team1.matchups[i] == 'Colts' or Team1.matchups[i] == 'Jaguars' or
                    Team1.matchups[i] == 'Titans' or Team1.matchups[i] == 'Texans' or Team1.matchups[i] == 'Broncos' or
                    Team1.matchups[i] == 'Chiefs' or Team1.matchups[i] == 'Chargers' or Team1.matchups[
                        i] == 'Raiders' or
                    Team1.matchups[i] == 'Patriots'):
                confMatchups3_1.append(Team1.results[i])
        elif (Team1.getConference() == 'NFC'):
            if (Team1.matchups[i] == 'Commanders' or Team1.matchups[i] == 'Cowboys' or Team1.matchups[i] == 'Giants' or
                    Team1.matchups[i] == 'Eagles' or Team1.matchups[i] == 'Bears' or Team1.matchups[i] == 'Lions' or
                    Team1.matchups[i] == 'Packers' or Team1.matchups[i] == 'Vikings' or Team1.matchups[
                        i] == 'Buccaneers' or
                    Team1.matchups[i] == 'Saints' or Team1.matchups[i] == 'Falcons' or Team1.matchups[
                        i] == 'Panthers' or
                    Team1.matchups[i] == '49ers' or Team1.matchups[i] == 'Cardinals' or Team1.matchups[
                        i] == 'Seahawks' or
                    Team1.matchups[i] == 'Rams'):
                confMatchups3_1.append(Team1.results[i])

    for i in range(17):
        if (Team2.getConference() == 'AFC'):
            if (Team2.matchups[i] == 'Bills' or Team2.matchups[i] == 'Dolphins' or Team2.matchups[i] == 'Jets' or
                    Team2.matchups[i] == 'Browns' or Team2.matchups[i] == 'Bengals' or Team2.matchups[
                        i] == 'Steelers' or
                    Team2.matchups[i] == 'Ravens' or Team2.matchups[i] == 'Colts' or Team2.matchups[i] == 'Jaguars' or
                    Team2.matchups[i] == 'Titans' or Team2.matchups[i] == 'Texans' or Team2.matchups[i] == 'Broncos' or
                    Team2.matchups[i] == 'Chiefs' or Team2.matchups[i] == 'Chargers' or Team2.matchups[
                        i] == 'Raiders' or
                    Team2.matchups[i] == 'Patriots'):
                confMatchups3_2.append(Team2.results[i])
        elif (Team2.getConference() == 'NFC'):
            if (Team2.matchups[i] == 'Commanders' or Team2.matchups[i] == 'Cowboys' or Team2.matchups[i] == 'Giants' or
                    Team2.matchups[i] == 'Eagles' or Team2.matchups[i] == 'Bears' or Team2.matchups[i] == 'Lions' or
                    Team2.matchups[i] == 'Packers' or Team2.matchups[i] == 'Vikings' or Team2.matchups[
                        i] == 'Buccaneers' or
                    Team2.matchups[i] == 'Saints' or Team2.matchups[i] == 'Falcons' or Team2.matchups[
                        i] == 'Panthers' or
                    Team2.matchups[i] == '49ers' or Team2.matchups[i] == 'Cardinals' or Team2.matchups[
                        i] == 'Seahawks' or
                    Team2.matchups[i] == 'Rams'):
                confMatchups3_2.append(Team2.results[i])

        if (Team3.getConference() == 'AFC'):
            if (Team3.matchups[i] == 'Bills' or Team3.matchups[i] == 'Dolphins' or Team3.matchups[i] == 'Jets' or
                    Team3.matchups[i] == 'Browns' or Team3.matchups[i] == 'Bengals' or Team3.matchups[
                        i] == 'Steelers' or
                    Team3.matchups[i] == 'Ravens' or Team3.matchups[i] == 'Colts' or Team3.matchups[i] == 'Jaguars' or
                    Team3.matchups[i] == 'Titans' or Team3.matchups[i] == 'Texans' or Team3.matchups[i] == 'Broncos' or
                    Team3.matchups[i] == 'Chiefs' or Team3.matchups[i] == 'Chargers' or Team3.matchups[
                        i] == 'Raiders' or
                    Team3.matchups[i] == 'Patriots'):
                confMatchups3_3.append(Team3.results[i])
        elif (Team3.getConference() == 'NFC'):
            if (Team3.matchups[i] == 'Commanders' or Team3.matchups[i] == 'Cowboys' or Team3.matchups[i] == 'Giants' or
                    Team3.matchups[i] == 'Eagles' or Team3.matchups[i] == 'Bears' or Team3.matchups[i] == 'Lions' or
                    Team3.matchups[i] == 'Packers' or Team3.matchups[i] == 'Vikings' or Team3.matchups[
                        i] == 'Buccaneers' or
                    Team3.matchups[i] == 'Saints' or Team3.matchups[i] == 'Falcons' or Team3.matchups[
                        i] == 'Panthers' or
                    Team3.matchups[i] == '49ers' or Team3.matchups[i] == 'Cardinals' or Team3.matchups[
                        i] == 'Seahawks' or
                    Team3.matchups[i] == 'Rams'):
                confMatchups3_3.append(Team3.results[i])

    #print (confMatchups3_1)
    #print (confMatchups3_2)
    #print (confMatchups3_3)
    if (confMatchups3_1.count('W') == confMatchups3_2.count('W') and confMatchups3_1.count(
            'W') == confMatchups3_3.count('W')):
        #print ("False")
        return (False)
    else:
        #print ("True")
        return (True)


def confRecord3(Team1, Team2, Team3):
    order = []
    wins1 = confMatchups3_1.count('W')
    wins2 = confMatchups3_2.count('W')
    wins3 = confMatchups3_3.count('W')
    #print (str(wins1) + str(wins2) + str(wins3))
    if (wins1 > wins2 and wins3 > wins1):
        order = [Team3, Team1, Team2]

    elif (wins2 > wins1 and wins3 > wins2):
        order = [Team3, Team2, Team1]

    elif (wins2 > wins3 and wins1 > wins2):
        order = [Team1, Team2, Team3]

    elif (wins3 > wins2 and wins1 > wins3):
        order = [Team1, Team3, Team2]

    elif (wins3 > wins1 and wins2 > wins3):
        order = [Team2, Team3, Team1]

    elif (wins1 > wins3 and wins2 > wins1):
        order = [Team2, Team1, Team3]

    elif (wins1 == wins2 and wins1 > wins3):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3]

    elif (wins1 == wins3 and wins1 > wins2):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2]

    elif (wins3 == wins2 and wins3 > wins1):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1]

    elif (wins1 == wins2 and wins1 < wins3):
        result = tiebreak2(Team1, Team2)
        order = [Team3, result[0], result[1]]

    elif (wins1 == wins3 and wins1 < wins2):
        result = tiebreak2(Team1, Team3)
        order = [Team2, result[0], result[1]]

    elif (wins3 == wins2 and wins3 < wins1):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1]]
    
    else: 
        print ("conf record not working")
        order = [Team1, Team2, Team3]

    #print ("Order of conf record 3 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName())
    return (order)


confMatchups4_1 = []
confMatchups4_2 = []
confMatchups4_3 = []
confMatchups4_4 = []


def isConfRecord4(Team1, Team2, Team3, Team4):
    global confMatchups4_1, confMatchups4_2, confMatchups4_3, confMatchups4_4
    confMatchups4_1 = []
    confMatchups4_2 = []
    confMatchups4_3 = []
    confMatchups4_4 = []
    for i in range(17):
        if (Team1.getConference() == 'AFC'):
            if (Team1.matchups[i] == 'Bills' or Team1.matchups[i] == 'Dolphins' or Team1.matchups[i] == 'Jets' or
                    Team1.matchups[i] == 'Browns' or Team1.matchups[i] == 'Bengals' or Team1.matchups[
                        i] == 'Steelers' or
                    Team1.matchups[i] == 'Ravens' or Team1.matchups[i] == 'Colts' or Team1.matchups[i] == 'Jaguars' or
                    Team1.matchups[i] == 'Titans' or Team1.matchups[i] == 'Texans' or Team1.matchups[i] == 'Broncos' or
                    Team1.matchups[i] == 'Chiefs' or Team1.matchups[i] == 'Chargers' or Team1.matchups[
                        i] == 'Raiders' or
                    Team1.matchups[i] == 'Patriots'):
                confMatchups4_1.append(Team1.results[i])
        elif (Team1.getConference() == 'NFC'):
            if (Team1.matchups[i] == 'Commanders' or Team1.matchups[i] == 'Cowboys' or Team1.matchups[i] == 'Giants' or
                    Team1.matchups[i] == 'Eagles' or Team1.matchups[i] == 'Bears' or Team1.matchups[i] == 'Lions' or
                    Team1.matchups[i] == 'Packers' or Team1.matchups[i] == 'Vikings' or Team1.matchups[
                        i] == 'Buccaneers' or
                    Team1.matchups[i] == 'Saints' or Team1.matchups[i] == 'Falcons' or Team1.matchups[
                        i] == 'Panthers' or
                    Team1.matchups[i] == '49ers' or Team1.matchups[i] == 'Cardinals' or Team1.matchups[
                        i] == 'Seahawks' or
                    Team1.matchups[i] == 'Rams'):
                confMatchups4_1.append(Team1.results[i])

    for i in range(17):
        if (Team2.getConference() == 'AFC'):
            if (Team2.matchups[i] == 'Bills' or Team2.matchups[i] == 'Dolphins' or Team2.matchups[i] == 'Jets' or
                    Team2.matchups[i] == 'Browns' or Team2.matchups[i] == 'Bengals' or Team2.matchups[
                        i] == 'Steelers' or
                    Team2.matchups[i] == 'Ravens' or Team2.matchups[i] == 'Colts' or Team2.matchups[i] == 'Jaguars' or
                    Team2.matchups[i] == 'Titans' or Team2.matchups[i] == 'Texans' or Team2.matchups[i] == 'Broncos' or
                    Team2.matchups[i] == 'Chiefs' or Team2.matchups[i] == 'Chargers' or Team2.matchups[
                        i] == 'Raiders' or
                    Team2.matchups[i] == 'Patriots'):
                confMatchups4_2.append(Team2.results[i])
        elif (Team2.getConference() == 'NFC'):
            if (Team2.matchups[i] == 'Commanders' or Team2.matchups[i] == 'Cowboys' or Team2.matchups[i] == 'Giants' or
                    Team2.matchups[i] == 'Eagles' or Team2.matchups[i] == 'Bears' or Team2.matchups[i] == 'Lions' or
                    Team2.matchups[i] == 'Packers' or Team2.matchups[i] == 'Vikings' or Team2.matchups[
                        i] == 'Buccaneers' or
                    Team2.matchups[i] == 'Saints' or Team2.matchups[i] == 'Falcons' or Team2.matchups[
                        i] == 'Panthers' or
                    Team2.matchups[i] == '49ers' or Team2.matchups[i] == 'Cardinals' or Team2.matchups[
                        i] == 'Seahawks' or
                    Team2.matchups[i] == 'Rams'):
                confMatchups4_2.append(Team2.results[i])

    for i in range(17):
        if (Team3.getConference() == 'AFC'):
            if (Team3.matchups[i] == 'Bills' or Team3.matchups[i] == 'Dolphins' or Team3.matchups[i] == 'Jets' or
                    Team3.matchups[i] == 'Browns' or Team3.matchups[i] == 'Bengals' or Team3.matchups[
                        i] == 'Steelers' or
                    Team3.matchups[i] == 'Ravens' or Team3.matchups[i] == 'Colts' or Team3.matchups[i] == 'Jaguars' or
                    Team3.matchups[i] == 'Titans' or Team3.matchups[i] == 'Texans' or Team3.matchups[i] == 'Broncos' or
                    Team3.matchups[i] == 'Chiefs' or Team3.matchups[i] == 'Chargers' or Team3.matchups[
                        i] == 'Raiders' or
                    Team3.matchups[i] == 'Patriots'):
                confMatchups4_3.append(Team3.results[i])
        elif (Team3.getConference() == 'NFC'):
            if (Team3.matchups[i] == 'Commanders' or Team3.matchups[i] == 'Cowboys' or Team3.matchups[i] == 'Giants' or
                    Team3.matchups[i] == 'Eagles' or Team3.matchups[i] == 'Bears' or Team3.matchups[i] == 'Lions' or
                    Team3.matchups[i] == 'Packers' or Team3.matchups[i] == 'Vikings' or Team3.matchups[
                        i] == 'Buccaneers' or
                    Team3.matchups[i] == 'Saints' or Team3.matchups[i] == 'Falcons' or Team3.matchups[
                        i] == 'Panthers' or
                    Team3.matchups[i] == '49ers' or Team3.matchups[i] == 'Cardinals' or Team3.matchups[
                        i] == 'Seahawks' or
                    Team3.matchups[i] == 'Rams'):
                confMatchups4_3.append(Team1.results[i])

    for i in range(17):
        if (Team4.getConference() == 'AFC'):
            if (Team4.matchups[i] == 'Bills' or Team4.matchups[i] == 'Dolphins' or Team4.matchups[i] == 'Jets' or
                    Team4.matchups[i] == 'Browns' or Team4.matchups[i] == 'Bengals' or Team4.matchups[
                        i] == 'Steelers' or
                    Team4.matchups[i] == 'Ravens' or Team4.matchups[i] == 'Colts' or Team4.matchups[i] == 'Jaguars' or
                    Team4.matchups[i] == 'Titans' or Team4.matchups[i] == 'Texans' or Team4.matchups[i] == 'Broncos' or
                    Team4.matchups[i] == 'Chiefs' or Team4.matchups[i] == 'Chargers' or Team4.matchups[
                        i] == 'Raiders' or
                    Team4.matchups[i] == 'Patriots'):
                confMatchups4_4.append(Team4.results[i])
        elif (Team4.getConference() == 'NFC'):
            if (Team4.matchups[i] == 'Commanders' or Team4.matchups[i] == 'Cowboys' or Team4.matchups[i] == 'Giants' or
                    Team4.matchups[i] == 'Eagles' or Team4.matchups[i] == 'Bears' or Team4.matchups[i] == 'Lions' or
                    Team4.matchups[i] == 'Packers' or Team4.matchups[i] == 'Vikings' or Team4.matchups[
                        i] == 'Buccaneers' or
                    Team4.matchups[i] == 'Saints' or Team4.matchups[i] == 'Falcons' or Team4.matchups[
                        i] == 'Panthers' or
                    Team4.matchups[i] == '49ers' or Team4.matchups[i] == 'Cardinals' or Team4.matchups[
                        i] == 'Seahawks' or
                    Team4.matchups[i] == 'Rams'):
                confMatchups4_4.append(Team4.results[i])

    if (confMatchups4_1.count('W') == confMatchups4_2.count('W') and confMatchups4_1.count('W') ==
            confMatchups4_3.count('W') and confMatchups4_1.count('W') == confMatchups4_4.count('W')):
        return (False)
    else:
        return (True)


def confRecord4(Team1, Team2, Team3, Team4):
    order = []
    wins1 = confMatchups4_1.count('W')
    wins2 = confMatchups4_2.count('W')
    wins3 = confMatchups4_3.count('W')
    wins4 = confMatchups4_4.count('W')

    if (wins1 > wins2 and wins2 > wins3 and wins3 > wins4):
        order = [Team1, Team2, Team3, Team4]

    elif (wins1 > wins2 and wins2 > wins4 and wins4 > wins3):
        order = [Team1, Team2, Team4, Team3]

    elif (wins1 > wins3 and wins3 > wins2 and wins2 > wins4):
        order = [Team1, Team3, Team2, Team4]

    elif (wins1 > wins3 and wins3 > wins4 and wins4 > wins2):
        order = [Team1, Team3, Team4, Team2]

    elif (wins1 > wins4 and wins4 > wins3 and wins3 > wins2):
        order = [Team1, Team4, Team3, Team2]

    elif (wins1 > wins4 and wins4 > wins2 and wins2 > wins3):
        order = [Team1, Team4, Team2, Team3]

    elif (wins2 > wins1 and wins1 > wins4 and wins4 > wins3):
        order = [Team2, Team1, Team4, Team3]

    elif (wins2 > wins1 and wins1 > wins3 and wins3 > wins4):
        order = [Team2, Team1, Team3, Team4]

    elif (wins2 > wins3 and wins3 > wins1 and wins1 > wins4):
        order = [Team2, Team3, Team1, Team4]

    elif (wins2 > wins3 and wins3 > wins4 and wins4 > wins1):
        order = [Team2, Team3, Team4, Team1]

    elif (wins2 > wins4 and wins4 > wins1 and wins1 > wins3):
        order = [Team2, Team4, Team1, Team3]

    elif (wins2 > wins4 and wins4 > wins3 and wins3 > wins1):
        order = [Team2, Team4, Team3, Team1]

    elif (wins3 > wins1 and wins1 > wins2 and wins2 > wins4):
        order = [Team3, Team1, Team2, Team4]

    elif (wins3 > wins1 and wins1 > wins4 and wins4 > wins2):
        order = [Team3, Team1, Team4, Team2]

    elif (wins3 > wins2 and wins2 > wins1 and wins1 > wins4):
        order = [Team3, Team2, Team1, Team4]

    elif (wins3 > wins2 and wins2 > wins4 and wins4 > wins1):
        order = [Team3, Team2, Team4, Team1]

    elif (wins3 > wins4 and wins4 > wins1 and wins1 > wins2):
        order = [Team3, Team4, Team1, Team2]

    elif (wins3 > wins4 and wins4 > wins2 and wins2 > wins1):
        order = [Team3, Team4, Team2, Team1]

    elif (wins4 > wins1 and wins1 > wins3 and wins3 > wins2):
        order = [Team4, Team1, Team3, Team2]

    elif (wins4 > wins1 and wins1 > wins2 and wins2 > wins3):
        order = [Team4, Team1, Team2, Team3]

    elif (wins4 > wins3 and wins3 > wins1 and wins1 > wins2):
        order = [Team4, Team3, Team1, Team2]

    elif (wins4 > wins3 and wins3 > wins2 and wins2 > wins1):
        order = [Team4, Team3, Team2, Team1]

    elif (wins4 > wins2 and wins2 > wins3 and wins3 > wins1):
        order = [Team4, Team2, Team3, Team1]

    elif (wins4 > wins2 and wins2 > wins1 and wins1 > wins3):
        order = [Team4, Team2, Team1, Team3]

    elif (wins1 > wins2 and wins2 > wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team1, Team2, result[0], result[1]]

    elif (wins2 > wins1 and wins2 > wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team2, Team1, result[0], result[1]]

    elif (wins1 > wins3 and wins3 > wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team1, Team3, result[0], result[1]]

    elif (wins3 > wins1 and wins1 > wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team3, Team1, result[0], result[1]]

    elif (wins1 > wins4 and wins4 > wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [Team1, Team4, result[0], result[1]]

    elif (wins4 > wins1 and wins1 > wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [Team4, Team1, result[0], result[1]]

    elif (wins2 > wins3 and wins3 > wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [Team2, Team3, result[0], result[1]]

    elif (wins3 > wins2 and wins2 > wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [Team3, Team2, result[0], result[1]]

    elif (wins2 > wins4 and wins4 > wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [Team2, Team4, result[0], result[1]]

    elif (wins4 > wins2 and wins2 > wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [Team4, Team2, result[0], result[1]]

    elif (wins3 > wins4 and wins4 > wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [Team2, Team4, result[0], result[1]]

    elif (wins4 > wins3 and wins3 > wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [Team4, Team3, result[0], result[1]]

    elif (wins1 < wins2 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [result[0], result[1], Team2, Team1]

    elif (wins2 < wins1 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [result[0], result[1], Team1, Team2]

    elif (wins1 < wins3 and wins3 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [result[0], result[1], Team3, Team1]

    elif (wins3 < wins1 and wins1 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [result[0], result[1], Team1, Team3]

    elif (wins1 < wins4 and wins4 < wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team4, Team1]

    elif (wins4 < wins1 and wins1 < wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1, Team4]

    elif (wins2 < wins3 and wins3 < wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [result[0], result[1], Team3, Team2]

    elif (wins3 < wins2 and wins2 < wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [result[0], result[1], Team2, Team3]

    elif (wins2 < wins4 and wins4 < wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team4, Team2]

    elif (wins4 < wins2 and wins2 < wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2, Team4]

    elif (wins3 < wins4 and wins4 < wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team4, Team3]

    elif (wins4 < wins3 and wins3 < wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3, Team4]

    elif (wins1 > wins2 and wins2 == wins3 and wins2 == wins4):
        result = tiebreak3(Team2, Team3, Team4)
        order = [Team1, result[0], result[1], result[2]]

    elif (wins2 > wins1 and wins1 == wins3 and wins1 == wins4):
        result = tiebreak3(Team1, Team3, Team4)
        order = [Team2, result[0], result[1], result[2]]

    elif (wins3 > wins2 and wins2 == wins1 and wins2 == wins4):
        result = tiebreak3(Team2, Team1, Team4)
        order = [Team3, result[0], result[1], result[2]]

    elif (wins4 > wins2 and wins2 == wins3 and wins2 == wins1):
        result = tiebreak3(Team2, Team3, Team1)
        order = [Team4, result[0], result[1], result[2]]

    elif (wins1 < wins2 and wins2 == wins3 and wins2 == wins4):
        result = tiebreak3(Team2, Team3, Team4)
        order = [result[0], result[1], result[2], Team1]

    elif (wins2 < wins1 and wins1 == wins3 and wins1 == wins4):
        result = tiebreak3(Team1, Team3, Team4)
        order = [result[0], result[1], result[2], Team2]

    elif (wins3 < wins2 and wins2 == wins1 and wins2 == wins4):
        result = tiebreak3(Team2, Team1, Team4)
        order = [result[0], result[1], result[2], Team3]

    elif (wins4 < wins2 and wins2 == wins3 and wins2 == wins1):
        result = tiebreak3(Team2, Team3, Team1)
        order = [result[0], result[1], result[2], Team4]

    elif (wins1 > wins3 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team1, result[0], result[1], Team2]

    elif (wins2 > wins3 and wins1 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team2, result[0], result[1], Team1]

    elif (wins1 > wins2 and wins3 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team1, result[0], result[1], Team3]

    elif (wins3 > wins2 and wins1 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team3, result[0], result[1], Team1]

    elif (wins1 > wins3 and wins4 < wins3 and wins3 == wins2):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1], Team4]

    elif (wins4 > wins3 and wins1 < wins3 and wins3 == wins2):
        result = tiebreak2(Team3, Team2)
        order = [Team4, result[0], result[1], Team1]

    elif (wins2 > wins4 and wins3 < wins4 and wins4 == wins1):
        result = tiebreak2(Team4, Team1)
        order = [Team2, result[0], result[1], Team3]

    elif (wins3 > wins4 and wins2 < wins4 and wins4 == wins1):
        result = tiebreak2(Team4, Team1)
        order = [Team3, result[0], result[1], Team2]

    elif (wins2 > wins3 and wins4 < wins3 and wins3 == wins1):
        result = tiebreak2(Team3, Team1)
        order = [Team2, result[0], result[1], Team4]

    elif (wins4 > wins3 and wins2 < wins3 and wins3 == wins1):
        result = tiebreak2(Team3, Team1)
        order = [Team4, result[0], result[1], Team2]

    elif (wins3 > wins2 and wins4 < wins2 and wins2 == wins1):
        result = tiebreak2(Team2, Team1)
        order = [Team3, result[0], result[1], Team4]

    elif (wins4 > wins2 and wins3 < wins2 and wins2 == wins1):
        result = tiebreak2(Team2, Team1)
        order = [Team4, result[0], result[1], Team3]

    elif (wins1 == wins2 and wins3 == wins4 and wins1 > wins3):
        result1 = tiebreak2(Team1, Team2)
        result2 = tiebreak2(Team3, Team4)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins2 and wins3 == wins4 and wins1 < wins3):
        result1 = tiebreak2(Team1, Team2)
        result2 = tiebreak2(Team3, Team4)
        order = [result2[0], result2[1], result1[0], result1[1]]

    elif (wins1 == wins3 and wins2 == wins4 and wins1 > wins2):
        result1 = tiebreak2(Team1, Team3)
        result2 = tiebreak2(Team2, Team4)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins3 and wins2 == wins4 and wins1 < wins2):
        result1 = tiebreak2(Team1, Team3)
        result2 = tiebreak2(Team2, Team4)
        order = [result2[0], result2[1], result1[0], result1[1]]

    elif (wins1 == wins4 and wins2 == wins3 and wins1 > wins2):
        result1 = tiebreak2(Team1, Team4)
        result2 = tiebreak2(Team2, Team3)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins4 and wins2 == wins3 and wins1 < wins2):
        result1 = tiebreak2(Team1, Team4)
        result2 = tiebreak2(Team2, Team3)
        order = [result2[0], result2[1], result1[0], result1[1]]
    else: 
        print ("conf record 4 not working")
        order = [Team1, Team2, Team3, Team4]
    
    #print ("Order of conf record 4 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName() + ", " + order[3].getName())
    return (order)


sovMatchups2_1 = []
sovMatchups2_2 = []
sovWins2_1 = 0
sovWins2_2 = 0


def isStrengthOfVictory2(Team1, Team2):
    global sovMatchups2_1, sovMatchups2_2, sovWins2_1, sovWins2_2
    sovMatchups2_1 = []
    sovMatchups2_2 = []
    sovWins2_1 = 0
    sovWins2_2 = 0
    for i in range(17):
        if Team1.results[i] == 'W':
            sovMatchups2_1.append(Team1.matchups[i])
    for i in range(17):
        if Team2.results[i] == 'W':
            sovMatchups2_2.append(Team2.matchups[i])

    for t in sovMatchups2_1:
        Team = findTeam(t)
        sovWins2_1 = sovWins2_1 + Team.getWins()
    for t in sovMatchups2_2:
        Team = findTeam(t)
        sovWins2_2 = sovWins2_2 + Team.getWins()

    if (sovWins2_1 == sovWins2_2):
        return (False)
    else:
        return (True)


def strengthOfVictory2(Team1, Team2):
    #print("SOV Tie between " + Team1.getName() + " and " + Team2.getName())
    if (sovWins2_1 > sovWins2_2):
        #print (Team1.getName() + " wins on SOV over " + Team2.getName())
        return (Team1)
    else:
        #print (Team2.getName() + " wins on SOV over " + Team1.getName())
        return (Team2)


sovMatchups3_1 = []
sovMatchups3_2 = []
sovMatchups3_3 = []
sovWins3_1 = 0
sovWins3_2 = 0
sovWins3_3 = 0


def isStrengthOfVictory3(Team1, Team2, Team3):
    global sovMatchups3_1, sovMatchups3_2, sovMatchups3_3, sovWins3_1, sovWins3_2, sovWins3_3
    sovMatchups3_1 = []
    sovMatchups3_2 = []
    sovMatchups3_3 = []
    sovWins3_1 = 0
    sovWins3_2 = 0
    sovWins3_3 = 0
    for i in range(17):
        if Team1.results[i] == 'W':
            sovMatchups3_1.append(Team1.matchups[i])
    for i in range(17):
        if Team2.results[i] == 'W':
            sovMatchups3_2.append(Team2.matchups[i])
    for i in range(17):
        if Team3.results[i] == 'W':
            sovMatchups3_3.append(Team3.matchups[i])

    for t in sovMatchups3_1:
        Team = findTeam(t)
        sovWins3_1 += Team.getWins()
    for t in sovMatchups3_2:
        Team = findTeam(t)
        sovWins3_2 += Team.getWins()
    for t in sovMatchups3_3:
        Team = findTeam(t)
        sovWins3_3 += Team.getWins()

    if (sovWins3_1 == sovWins3_2 and sovWins3_3 == sovWins3_1):
        return (False)
    else:
        return (True)


def strengthOfVictory3(Team1, Team2, Team3):
    #print("SOV Tie between " + Team1.getName() + ", " + Team2.getName() + ", and " + Team3.getName())
    order = []
    wins1 = sovWins3_1
    wins2 = sovWins3_2
    wins3 = sovWins3_3
    if (wins1 > wins2 and wins3 > wins1):
        order = [Team3, Team1, Team2]

    elif (wins2 > wins1 and wins3 > wins2):
        order = [Team3, Team2, Team1]

    elif (wins2 > wins3 and wins1 > wins2):
        order = [Team1, Team2, Team3]

    elif (wins3 > wins2 and wins1 > wins3):
        order = [Team1, Team3, Team2]

    elif (wins3 > wins1 and wins2 > wins3):
        order = [Team2, Team3, Team1]

    elif (wins1 > wins3 and wins2 > wins1):
        order = [Team2, Team1, Team3]

    elif (wins1 == wins2 and wins1 > wins3):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3]

    elif (wins1 == wins3 and wins1 > wins2):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2]

    elif (wins3 == wins2 and wins3 > wins1):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1]

    elif (wins1 == wins2 and wins1 < wins3):
        result = tiebreak2(Team1, Team2)
        order = [Team3, result[0], result[1]]

    elif (wins1 == wins3 and wins1 < wins2):
        result = tiebreak2(Team1, Team3)
        order = [Team2, result[0], result[1]]

    elif (wins3 == wins2 and wins3 < wins1):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1]]

    #print ("Order of sov 3 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName())
    return (order)


sovMatchups4_1 = []
sovMatchups4_2 = []
sovMatchups4_3 = []
sovMatchups4_4 = []
sovWins4_1 = 0
sovWins4_2 = 0
sovWins4_3 = 0
sovWins4_4 = 0


def isStrengthOfVictory4(Team1, Team2, Team3, Team4):
    global sovMatchups4_1, sovMatchups4_2, sovMatchups4_3, sovMatchups4_4, sovWins4_1, sovWins4_2, sovWins4_3, sovWins4_4
    sovMatchups4_1 = []
    sovMatchups4_2 = []
    sovMatchups4_3 = []
    sovMatchups4_4 = []
    sovWins4_1 = 0
    sovWins4_2 = 0
    sovWins4_3 = 0
    sovWins4_4 = 0
    for i in range(17):
        if Team1.results[i] == 'W':
            sovMatchups4_1.append(Team1.matchups[i])
    for i in range(17):
        if Team2.results[i] == 'W':
            sovMatchups4_2.append(Team2.matchups[i])
    for i in range(17):
        if Team3.results[i] == 'W':
            sovMatchups4_3.append(Team3.matchups[i])
    for i in range(17):
        if Team4.results[i] == 'W':
            sovMatchups4_4.append(Team4.matchups[i])

    for t in sovMatchups4_1:
        Team = findTeam(t)
        sovWins4_1 += Team.getWins()
    for t in sovMatchups4_2:
        Team = findTeam(t)
        sovWins4_2 += Team.getWins()
    for t in sovMatchups4_3:
        Team = findTeam(t)
        sovWins4_3 += Team.getWins()
    for t in sovMatchups4_4:
        Team = findTeam(t)
        sovWins4_4 += Team.getWins()

    if (sovWins4_1 == sovWins4_2 and sovWins4_3 == sovWins4_1 and sovWins4_1 == sovWins4_4):
        return (False)
    else:
        return (True)


def strengthOfVictory4(Team1, Team2, Team3, Team4):
    #print("SOV Tie between " + Team1.getName() + ", " + Team2.getName() + ", " + Team3.getName() + ", and " + Team4.getName())
    order = []
    wins1 = sovWins4_1
    wins2 = sovWins4_2
    wins3 = sovWins4_3
    wins4 = sovWins4_4

    if (wins1 > wins2 and wins2 > wins3 and wins3 > wins4):
        order = [Team1, Team2, Team3, Team4]

    elif (wins1 > wins2 and wins2 > wins4 and wins4 > wins3):
        order = [Team1, Team2, Team4, Team3]

    elif (wins1 > wins3 and wins3 > wins2 and wins2 > wins4):
        order = [Team1, Team3, Team2, Team4]

    elif (wins1 > wins3 and wins3 > wins4 and wins4 > wins2):
        order = [Team1, Team3, Team4, Team2]

    elif (wins1 > wins4 and wins4 > wins3 and wins3 > wins2):
        order = [Team1, Team4, Team3, Team2]

    elif (wins1 > wins4 and wins4 > wins2 and wins2 > wins3):
        order = [Team1, Team4, Team2, Team3]

    elif (wins2 > wins1 and wins1 > wins4 and wins4 > wins3):
        order = [Team2, Team1, Team4, Team3]

    elif (wins2 > wins1 and wins1 > wins3 and wins3 > wins4):
        order = [Team2, Team1, Team3, Team4]

    elif (wins2 > wins3 and wins3 > wins1 and wins1 > wins4):
        order = [Team2, Team3, Team1, Team4]

    elif (wins2 > wins3 and wins3 > wins4 and wins4 > wins1):
        order = [Team2, Team3, Team4, Team1]

    elif (wins2 > wins4 and wins4 > wins1 and wins1 > wins3):
        order = [Team2, Team4, Team1, Team3]

    elif (wins2 > wins4 and wins4 > wins3 and wins3 > wins1):
        order = [Team2, Team4, Team3, Team1]

    elif (wins3 > wins1 and wins1 > wins2 and wins2 > wins4):
        order = [Team3, Team1, Team2, Team4]

    elif (wins3 > wins1 and wins1 > wins4 and wins4 > wins2):
        order = [Team3, Team1, Team4, Team2]

    elif (wins3 > wins2 and wins2 > wins1 and wins1 > wins4):
        order = [Team3, Team2, Team1, Team4]

    elif (wins3 > wins2 and wins2 > wins4 and wins4 > wins1):
        order = [Team3, Team2, Team4, Team1]

    elif (wins3 > wins4 and wins4 > wins1 and wins1 > wins2):
        order = [Team3, Team4, Team1, Team2]

    elif (wins3 > wins4 and wins4 > wins2 and wins2 > wins1):
        order = [Team3, Team4, Team2, Team1]

    elif (wins4 > wins1 and wins1 > wins3 and wins3 > wins2):
        order = [Team4, Team1, Team3, Team2]

    elif (wins4 > wins1 and wins1 > wins2 and wins2 > wins3):
        order = [Team4, Team1, Team2, Team3]

    elif (wins4 > wins3 and wins3 > wins1 and wins1 > wins2):
        order = [Team4, Team3, Team1, Team2]

    elif (wins4 > wins3 and wins3 > wins2 and wins2 > wins1):
        order = [Team4, Team3, Team2, Team1]

    elif (wins4 > wins2 and wins2 > wins3 and wins3 > wins1):
        order = [Team4, Team2, Team3, Team1]

    elif (wins4 > wins2 and wins2 > wins1 and wins1 > wins3):
        order = [Team4, Team2, Team1, Team3]

    elif (wins1 > wins2 and wins2 > wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team1, Team2, result[0], result[1]]

    elif (wins2 > wins1 and wins2 > wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team2, Team1, result[0], result[1]]

    elif (wins1 > wins3 and wins3 > wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team1, Team3, result[0], result[1]]

    elif (wins3 > wins1 and wins1 > wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team3, Team1, result[0], result[1]]

    elif (wins1 > wins4 and wins4 > wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [Team1, Team4, result[0], result[1]]

    elif (wins4 > wins1 and wins1 > wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [Team4, Team1, result[0], result[1]]

    elif (wins2 > wins3 and wins3 > wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [Team2, Team3, result[0], result[1]]

    elif (wins3 > wins2 and wins2 > wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [Team3, Team2, result[0], result[1]]

    elif (wins2 > wins4 and wins4 > wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [Team2, Team4, result[0], result[1]]

    elif (wins4 > wins2 and wins2 > wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [Team4, Team2, result[0], result[1]]

    elif (wins3 > wins4 and wins4 > wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [Team2, Team4, result[0], result[1]]

    elif (wins4 > wins3 and wins3 > wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [Team4, Team3, result[0], result[1]]

    elif (wins1 < wins2 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [result[0], result[1], Team2, Team1]

    elif (wins2 < wins1 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [result[0], result[1], Team1, Team2]

    elif (wins1 < wins3 and wins3 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [result[0], result[1], Team3, Team1]

    elif (wins3 < wins1 and wins1 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [result[0], result[1], Team1, Team3]

    elif (wins1 < wins4 and wins4 < wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team4, Team1]

    elif (wins4 < wins1 and wins1 < wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1, Team4]

    elif (wins2 < wins3 and wins3 < wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [result[0], result[1], Team3, Team2]

    elif (wins3 < wins2 and wins2 < wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [result[0], result[1], Team2, Team3]

    elif (wins2 < wins4 and wins4 < wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team4, Team2]

    elif (wins4 < wins2 and wins2 < wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2, Team4]

    elif (wins3 < wins4 and wins4 < wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team4, Team3]

    elif (wins4 < wins3 and wins3 < wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3, Team4]

    elif (wins1 > wins2 and wins2 == wins3 and wins2 == wins4):
        result = tiebreak2(Team2, Team3, Team4)
        order = [Team1, result[0], result[1], result[2]]

    elif (wins2 > wins1 and wins1 == wins3 and wins1 == wins4):
        result = tiebreak3(Team1, Team3, Team4)
        order = [Team2, result[0], result[1], result[2]]

    elif (wins3 > wins2 and wins2 == wins1 and wins2 == wins4):
        result = tiebreak3(Team2, Team1, Team4)
        order = [Team3, result[0], result[1], result[2]]

    elif (wins4 > wins2 and wins2 == wins3 and wins2 == wins1):
        result = tiebreak3(Team2, Team3, Team1)
        order = [Team4, result[0], result[1], result[2]]

    elif (wins1 < wins2 and wins2 == wins3 and wins2 == wins4):
        result = tiebreak3(Team2, Team3, Team4)
        order = [result[0], result[1], result[2], Team1]

    elif (wins2 < wins1 and wins1 == wins3 and wins1 == wins4):
        result = tiebreak3(Team1, Team3, Team4)
        order = [result[0], result[1], result[2], Team2]

    elif (wins3 < wins2 and wins2 == wins1 and wins2 == wins4):
        result = tiebreak3(Team2, Team1, Team4)
        order = [result[0], result[1], result[2], Team3]

    elif (wins4 < wins2 and wins2 == wins3 and wins2 == wins1):
        result = tiebreak3(Team2, Team3, Team1)
        order = [result[0], result[1], result[2], Team4]

    elif (wins1 > wins3 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team1, result[0], result[1], Team2]

    elif (wins2 > wins3 and wins1 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team2, result[0], result[1], Team1]

    elif (wins1 > wins2 and wins3 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team1, result[0], result[1], Team3]

    elif (wins3 > wins2 and wins1 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team3, result[0], result[1], Team1]

    elif (wins1 > wins3 and wins4 < wins3 and wins3 == wins2):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1], Team4]

    elif (wins4 > wins3 and wins1 < wins3 and wins3 == wins2):
        result = tiebreak2(Team3, Team2)
        order = [Team4, result[0], result[1], Team1]

    elif (wins2 > wins4 and wins3 < wins4 and wins4 == wins1):
        result = tiebreak2(Team4, Team1)
        order = [Team2, result[0], result[1], Team3]

    elif (wins3 > wins4 and wins2 < wins4 and wins4 == wins1):
        result = tiebreak2(Team4, Team1)
        order = [Team3, result[0], result[1], Team2]

    elif (wins2 > wins3 and wins4 < wins3 and wins3 == wins1):
        result = tiebreak2(Team3, Team1)
        order = [Team2, result[0], result[1], Team4]

    elif (wins4 > wins3 and wins2 < wins3 and wins3 == wins1):
        result = tiebreak2(Team3, Team1)
        order = [Team4, result[0], result[1], Team2]

    elif (wins3 > wins2 and wins4 < wins2 and wins2 == wins1):
        result = tiebreak2(Team2, Team1)
        order = [Team3, result[0], result[1], Team4]

    elif (wins4 > wins2 and wins3 < wins2 and wins2 == wins1):
        result = tiebreak2(Team2, Team1)
        order = [Team4, result[0], result[1], Team3]

    elif (wins1 == wins2 and wins3 == wins4 and wins1 > wins3):
        result1 = tiebreak2(Team1, Team2)
        result2 = tiebreak2(Team3, Team4)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins2 and wins3 == wins4 and wins1 < wins3):
        result1 = tiebreak2(Team1, Team2)
        result2 = tiebreak2(Team3, Team4)
        order = [result2[0], result2[1], result1[0], result1[1]]

    elif (wins1 == wins3 and wins2 == wins4 and wins1 > wins2):
        result1 = tiebreak2(Team1, Team3)
        result2 = tiebreak2(Team2, Team4)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins3 and wins2 == wins4 and wins1 < wins2):
        result1 = tiebreak2(Team1, Team3)
        result2 = tiebreak2(Team2, Team4)
        order = [result2[0], result2[1], result1[0], result1[1]]

    elif (wins1 == wins4 and wins2 == wins3 and wins1 > wins2):
        result1 = tiebreak2(Team1, Team4)
        result2 = tiebreak2(Team2, Team3)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins4 and wins2 == wins3 and wins1 < wins2):
        result1 = tiebreak2(Team1, Team4)
        result2 = tiebreak2(Team2, Team3)
        order = [result2[0], result2[1], result1[0], result1[1]]
    else:
        print ("sov not work")
    
   # print ("Order of sov 4 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName() + ", " + order[3].getName())
    return (order)



sosWins2_1 = 0
sosWins2_2 = 0


def isStrengthOfSchedule2(Team1, Team2):
    global sosWins2_1, sosWins2_2
    sosWins2_1 = 0
    sosWins2_2 = 0

    for t in Team1.matchups:
        Team = findTeam(t)
        sosWins2_1 = sosWins2_1 + Team.getWins()
    for t in Team2.matchups:
        Team = findTeam(t)
        sosWins2_2 = sosWins2_2 + Team.getWins()

    if (sovWins2_1 == sovWins2_2):
        return (False)
    else:
        return (True)


def strengthOfSchedule2(Team1, Team2):
    #print("SOS Tie between " + Team1.getName() + " and " + Team2.getName())
    if (sosWins2_1 > sosWins2_2):
        #print (Team1.getName() + " wins on SOS over " + Team2.getName())
        return (Team1)
    else:
        #print (Team2.getName() + " wins on SOS over " + Team1.getName())
        return (Team2)
    

sosWins3_1 = 0
sosWins3_2 = 0
sosWins3_3 = 0


def isStrengthOfSchedule3(Team1, Team2, Team3):
    global sosWins3_1, sosWins3_2, sosWins3_3
    sosWins3_1 = 0
    sosWins3_2 = 0
    sosWins3_3 = 0

    for t in Team1.matchups:
        Team = findTeam(t)
        sosWins3_1 += Team.getWins()
    for t in Team2.matchups:
        Team = findTeam(t)
        sosWins3_2 += Team.getWins()
    for t in Team3.matchups:
        Team = findTeam(t)
        sosWins3_3 += Team.getWins()

    if (sovWins3_1 == sovWins3_2 and sovWins3_3 == sovWins3_1):
        return (False)
    else:
        return (True)


def strengthOfSchedule3(Team1, Team2, Team3):
    #print("SOS Tie between " + Team1.getName() + ", " + Team2.getName() + ", and " + Team3.getName())
    order = []
    wins1 = sosWins3_1
    wins2 = sosWins3_2
    wins3 = sosWins3_3
    if (wins1 > wins2 and wins3 > wins1):
        order = [Team3, Team1, Team2]

    elif (wins2 > wins1 and wins3 > wins2):
        order = [Team3, Team2, Team1]

    elif (wins2 > wins3 and wins1 > wins2):
        order = [Team1, Team2, Team3]

    elif (wins3 > wins2 and wins1 > wins3):
        order = [Team1, Team3, Team2]

    elif (wins3 > wins1 and wins2 > wins3):
        order = [Team2, Team3, Team1]

    elif (wins1 > wins3 and wins2 > wins1):
        order = [Team2, Team1, Team3]

    elif (wins1 == wins2 and wins1 > wins3):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3]

    elif (wins1 == wins3 and wins1 > wins2):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2]

    elif (wins3 == wins2 and wins3 > wins1):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1]

    elif (wins1 == wins2 and wins1 < wins3):
        result = tiebreak2(Team1, Team2)
        order = [Team3, result[0], result[1]]

    elif (wins1 == wins3 and wins1 < wins2):
        result = tiebreak2(Team1, Team3)
        order = [Team2, result[0], result[1]]

    elif (wins3 == wins2 and wins3 < wins1):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1]]

    #print ("Order of sos 3 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName())
    return (order)


sosWins4_1 = 0
sosWins4_2 = 0
sosWins4_3 = 0
sosWins4_4 = 0


def isStrengthOfSchedule4(Team1, Team2, Team3, Team4):
    global sosWins4_1, sosWins4_2, sosWins4_3, sosWins4_4
    sosWins4_1 = 0
    sosWins4_2 = 0
    sosWins4_3 = 0
    sosWins4_4 = 0

    for t in Team1.matchups:
        Team = findTeam(t)
        sosWins4_1 += Team.getWins()
    for t in Team2.matchups:
        Team = findTeam(t)
        sosWins4_2 += Team.getWins()
    for t in Team3.matchups:
        Team = findTeam(t)
        sosWins4_3 += Team.getWins()
    for t in Team4.matchups:
        Team = findTeam(t)
        sosWins4_4 += Team.getWins()

    if (sosWins4_1 == sosWins4_2 and sosWins4_3 == sosWins4_1 and sosWins4_1 == sosWins4_4):
        return (False)
    else:
        return (True)


def strengthOfSchedule4(Team1, Team2, Team3, Team4):
    #print("SOS Tie between " + Team1.getName() + ", " + Team2.getName() + ", " + Team3.getName() + ", and " + Team4.getName())
    order = []
    wins1 = sosWins4_1
    wins2 = sosWins4_2
    wins3 = sosWins4_3
    wins4 = sosWins4_4

    if (wins1 > wins2 and wins2 > wins3 and wins3 > wins4):
        order = [Team1, Team2, Team3, Team4]

    elif (wins1 > wins2 and wins2 > wins4 and wins4 > wins3):
        order = [Team1, Team2, Team4, Team3]

    elif (wins1 > wins3 and wins3 > wins2 and wins2 > wins4):
        order = [Team1, Team3, Team2, Team4]

    elif (wins1 > wins3 and wins3 > wins4 and wins4 > wins2):
        order = [Team1, Team3, Team4, Team2]

    elif (wins1 > wins4 and wins4 > wins3 and wins3 > wins2):
        order = [Team1, Team4, Team3, Team2]

    elif (wins1 > wins4 and wins4 > wins2 and wins2 > wins3):
        order = [Team1, Team4, Team2, Team3]

    elif (wins2 > wins1 and wins1 > wins4 and wins4 > wins3):
        order = [Team2, Team1, Team4, Team3]

    elif (wins2 > wins1 and wins1 > wins3 and wins3 > wins4):
        order = [Team2, Team1, Team3, Team4]

    elif (wins2 > wins3 and wins3 > wins1 and wins1 > wins4):
        order = [Team2, Team3, Team1, Team4]

    elif (wins2 > wins3 and wins3 > wins4 and wins4 > wins1):
        order = [Team2, Team3, Team4, Team1]

    elif (wins2 > wins4 and wins4 > wins1 and wins1 > wins3):
        order = [Team2, Team4, Team1, Team3]

    elif (wins2 > wins4 and wins4 > wins3 and wins3 > wins1):
        order = [Team2, Team4, Team3, Team1]

    elif (wins3 > wins1 and wins1 > wins2 and wins2 > wins4):
        order = [Team3, Team1, Team2, Team4]

    elif (wins3 > wins1 and wins1 > wins4 and wins4 > wins2):
        order = [Team3, Team1, Team4, Team2]

    elif (wins3 > wins2 and wins2 > wins1 and wins1 > wins4):
        order = [Team3, Team2, Team1, Team4]

    elif (wins3 > wins2 and wins2 > wins4 and wins4 > wins1):
        order = [Team3, Team2, Team4, Team1]

    elif (wins3 > wins4 and wins4 > wins1 and wins1 > wins2):
        order = [Team3, Team4, Team1, Team2]

    elif (wins3 > wins4 and wins4 > wins2 and wins2 > wins1):
        order = [Team3, Team4, Team2, Team1]

    elif (wins4 > wins1 and wins1 > wins3 and wins3 > wins2):
        order = [Team4, Team1, Team3, Team2]

    elif (wins4 > wins1 and wins1 > wins2 and wins2 > wins3):
        order = [Team4, Team1, Team2, Team3]

    elif (wins4 > wins3 and wins3 > wins1 and wins1 > wins2):
        order = [Team4, Team3, Team1, Team2]

    elif (wins4 > wins3 and wins3 > wins2 and wins2 > wins1):
        order = [Team4, Team3, Team2, Team1]

    elif (wins4 > wins2 and wins2 > wins3 and wins3 > wins1):
        order = [Team4, Team2, Team3, Team1]

    elif (wins4 > wins2 and wins2 > wins1 and wins1 > wins3):
        order = [Team4, Team2, Team1, Team3]

    elif (wins1 > wins2 and wins2 > wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team1, Team2, result[0], result[1]]

    elif (wins2 > wins1 and wins2 > wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team2, Team1, result[0], result[1]]

    elif (wins1 > wins3 and wins3 > wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team1, Team3, result[0], result[1]]

    elif (wins3 > wins1 and wins1 > wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team3, Team1, result[0], result[1]]

    elif (wins1 > wins4 and wins4 > wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [Team1, Team4, result[0], result[1]]

    elif (wins4 > wins1 and wins1 > wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [Team4, Team1, result[0], result[1]]

    elif (wins2 > wins3 and wins3 > wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [Team2, Team3, result[0], result[1]]

    elif (wins3 > wins2 and wins2 > wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [Team3, Team2, result[0], result[1]]

    elif (wins2 > wins4 and wins4 > wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [Team2, Team4, result[0], result[1]]

    elif (wins4 > wins2 and wins2 > wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [Team4, Team2, result[0], result[1]]

    elif (wins3 > wins4 and wins4 > wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [Team2, Team4, result[0], result[1]]

    elif (wins4 > wins3 and wins3 > wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [Team4, Team3, result[0], result[1]]

    elif (wins1 < wins2 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [result[0], result[1], Team2, Team1]

    elif (wins2 < wins1 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [result[0], result[1], Team1, Team2]

    elif (wins1 < wins3 and wins3 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [result[0], result[1], Team3, Team1]

    elif (wins3 < wins1 and wins1 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [result[0], result[1], Team1, Team3]

    elif (wins1 < wins4 and wins4 < wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team4, Team1]

    elif (wins4 < wins1 and wins1 < wins2 and wins2 == wins3):
        result = tiebreak2(Team2, Team3)
        order = [result[0], result[1], Team1, Team4]

    elif (wins2 < wins3 and wins3 < wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [result[0], result[1], Team3, Team2]

    elif (wins3 < wins2 and wins2 < wins1 and wins1 == wins4):
        result = tiebreak2(Team1, Team4)
        order = [result[0], result[1], Team2, Team3]

    elif (wins2 < wins4 and wins4 < wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team4, Team2]

    elif (wins4 < wins2 and wins2 < wins1 and wins1 == wins3):
        result = tiebreak2(Team1, Team3)
        order = [result[0], result[1], Team2, Team4]

    elif (wins3 < wins4 and wins4 < wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team4, Team3]

    elif (wins4 < wins3 and wins3 < wins1 and wins1 == wins2):
        result = tiebreak2(Team1, Team2)
        order = [result[0], result[1], Team3, Team4]

    elif (wins1 > wins2 and wins2 == wins3 and wins2 == wins4):
        result = tiebreak2(Team2, Team3, Team4)
        order = [Team1, result[0], result[1], result[2]]

    elif (wins2 > wins1 and wins1 == wins3 and wins1 == wins4):
        result = tiebreak3(Team1, Team3, Team4)
        order = [Team2, result[0], result[1], result[2]]

    elif (wins3 > wins2 and wins2 == wins1 and wins2 == wins4):
        result = tiebreak3(Team2, Team1, Team4)
        order = [Team3, result[0], result[1], result[2]]

    elif (wins4 > wins2 and wins2 == wins3 and wins2 == wins1):
        result = tiebreak3(Team2, Team3, Team1)
        order = [Team4, result[0], result[1], result[2]]

    elif (wins1 < wins2 and wins2 == wins3 and wins2 == wins4):
        result = tiebreak3(Team2, Team3, Team4)
        order = [result[0], result[1], result[2], Team1]

    elif (wins2 < wins1 and wins1 == wins3 and wins1 == wins4):
        result = tiebreak3(Team1, Team3, Team4)
        order = [result[0], result[1], result[2], Team2]

    elif (wins3 < wins2 and wins2 == wins1 and wins2 == wins4):
        result = tiebreak3(Team2, Team1, Team4)
        order = [result[0], result[1], result[2], Team3]

    elif (wins4 < wins2 and wins2 == wins3 and wins2 == wins1):
        result = tiebreak3(Team2, Team3, Team1)
        order = [result[0], result[1], result[2], Team4]

    elif (wins1 > wins3 and wins2 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team1, result[0], result[1], Team2]

    elif (wins2 > wins3 and wins1 < wins3 and wins3 == wins4):
        result = tiebreak2(Team3, Team4)
        order = [Team2, result[0], result[1], Team1]

    elif (wins1 > wins2 and wins3 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team1, result[0], result[1], Team3]

    elif (wins3 > wins2 and wins1 < wins2 and wins2 == wins4):
        result = tiebreak2(Team2, Team4)
        order = [Team3, result[0], result[1], Team1]

    elif (wins1 > wins3 and wins4 < wins3 and wins3 == wins2):
        result = tiebreak2(Team3, Team2)
        order = [Team1, result[0], result[1], Team4]

    elif (wins4 > wins3 and wins1 < wins3 and wins3 == wins2):
        result = tiebreak2(Team3, Team2)
        order = [Team4, result[0], result[1], Team1]

    elif (wins2 > wins4 and wins3 < wins4 and wins4 == wins1):
        result = tiebreak2(Team4, Team1)
        order = [Team2, result[0], result[1], Team3]

    elif (wins3 > wins4 and wins2 < wins4 and wins4 == wins1):
        result = tiebreak2(Team4, Team1)
        order = [Team3, result[0], result[1], Team2]

    elif (wins2 > wins3 and wins4 < wins3 and wins3 == wins1):
        result = tiebreak2(Team3, Team1)
        order = [Team2, result[0], result[1], Team4]

    elif (wins4 > wins3 and wins2 < wins3 and wins3 == wins1):
        result = tiebreak2(Team3, Team1)
        order = [Team4, result[0], result[1], Team2]

    elif (wins3 > wins2 and wins4 < wins2 and wins2 == wins1):
        result = tiebreak2(Team2, Team1)
        order = [Team3, result[0], result[1], Team4]

    elif (wins4 > wins2 and wins3 < wins2 and wins2 == wins1):
        result = tiebreak2(Team2, Team1)
        order = [Team4, result[0], result[1], Team3]

    elif (wins1 == wins2 and wins3 == wins4 and wins1 > wins3):
        result1 = tiebreak2(Team1, Team2)
        result2 = tiebreak2(Team3, Team4)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins2 and wins3 == wins4 and wins1 < wins3):
        result1 = tiebreak2(Team1, Team2)
        result2 = tiebreak2(Team3, Team4)
        order = [result2[0], result2[1], result1[0], result1[1]]

    elif (wins1 == wins3 and wins2 == wins4 and wins1 > wins2):
        result1 = tiebreak2(Team1, Team3)
        result2 = tiebreak2(Team2, Team4)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins3 and wins2 == wins4 and wins1 < wins2):
        result1 = tiebreak2(Team1, Team3)
        result2 = tiebreak2(Team2, Team4)
        order = [result2[0], result2[1], result1[0], result1[1]]

    elif (wins1 == wins4 and wins2 == wins3 and wins1 > wins2):
        result1 = tiebreak2(Team1, Team4)
        result2 = tiebreak2(Team2, Team3)
        order = [result1[0], result1[1], result2[0], result2[1]]

    elif (wins1 == wins4 and wins2 == wins3 and wins1 < wins2):
        result1 = tiebreak2(Team1, Team4)
        result2 = tiebreak2(Team2, Team3)
        order = [result2[0], result2[1], result1[0], result1[1]]
    else:
        print ("sov not work")
    
   # print ("Order of sos 4 tiebreaker: " + order[0].getName() + ", " + order[1].getName() + ", " + 
           #order[2].getName() + ", " + order[3].getName())
    return (order)



def tiebreak2(Team1, Team2):
    #print ("Starting 2 team tiebreaker between " + Team1.getName() + " and " + Team2.getName())
    result = []
    if (Team1.getDivision() == Team2.getDivision()):
        inDiv = True
    else:
        inDiv = False

    if (inDiv):
        func = isDivH2H2(Team1, Team2)
        if (func[0]):
            if (func[1] > func[2]):
                #print (Team1.getName() + " wins via div h2h over " + Team2.getName())
                result = [Team1, Team2]
            else:
                #print (Team1.getName() + " wins via div h2h over " + Team2.getName())
                result = [Team2, Team1]

        elif (isDivRecord2(Team1, Team2)):
            first = divRecord2(Team1, Team2)
            if (first == Team1):
                result = [Team1, Team2]
            else:
                result = [Team2, Team1]

        elif (isCommonRecord2(Team1, Team2)):
            first = commonRecord2(Team1, Team2)
            if (first == Team1):
                result = [Team1, Team2]
            else:
                result = [Team2, Team1]

        elif (isConfRecord2(Team1, Team2)):
            first = confRecord2(Team1, Team2)
            if (first == Team1):
                result = [Team1, Team2]
            else:
                result = [Team2, Team1]

        elif (isStrengthOfVictory2(Team1, Team2)):
            first = strengthOfVictory2(Team1, Team2)
            if (first == Team1):
                result = [Team1, Team2]
            else:
                result = [Team2, Team1]
                
        elif (isStrengthOfSchedule2(Team1, Team2)):
            first = strengthOfSchedule2(Team1, Team2)
            if (first == Team1):
                result = [Team1, Team2]
            else:
                result = [Team2, Team1]

        else:
            result = [Team1, Team2]
            print(
                "ERROR!!! Tiebreaker between " + Team1.getName() + " and " + Team2.getName() + " could not be calculated")
    else:
        if (isH2H2(Team1, Team2)):
            first = h2h2(Team1, Team2)
            if (first == Team1):
                result = [Team1, Team2]
            else:
                result = [Team2, Team1]

        elif (isConfRecord2(Team1, Team2)):
            first = confRecord2(Team1, Team2)
            if (first == Team1):
                result = [Team1, Team2]
            else:
                result = [Team2, Team1]

        elif (isCommonRecord2(Team1, Team2)):
            first = commonRecord2(Team1, Team2)
            if (first == Team1):
                result = [Team1, Team2]
            else:
                result = [Team2, Team1]

        elif (isStrengthOfVictory2(Team1, Team2)):
            first = strengthOfVictory2(Team1, Team2)
            if (first == Team1):
                result = [Team1, Team2]
            else:
                result = [Team2, Team1]
                
        elif (isStrengthOfSchedule2(Team1, Team2)):
            first = strengthOfSchedule2(Team1, Team2)
            if (first == Team1):
                result = [Team1, Team2]
            else:
                result = [Team2, Team1]

        else:
            result = [Team1, Team2]
            print(
                "ERROR!!! Tiebreaker between " + Team1.getName() + " and " + Team2.getName() + " could not be calculated")
    return (result)


def tiebreak3(Team1, Team2, Team3):
    #print ("Starting 3 team tiebreaker between " + Team1.getName() + ", " + Team2.getName() + ", and " + Team3.getName())
    result = []
    if (Team1.getDivision() == Team2.getDivision() and Team1.getDivision() == Team3.getDivision()):
        if (isDivH2H3(Team1, Team2, Team3)):
            result = divH2H3(Team1, Team2, Team3)

        elif (isDivRecord3(Team1, Team2, Team3)):
            result = divRecord3(Team1, Team2, Team3)

        elif (isCommonRecord3(Team1, Team2, Team3)):
            result = commonRecord3(Team1, Team2, Team3)

        elif (isConfRecord3(Team1, Team2, Team3)):
            result = confRecord3(Team1, Team2, Team3)

        elif (isStrengthOfVictory3(Team1, Team2, Team3)):
            result = strengthOfVictory3(Team1, Team2, Team3)
            
        elif (isStrengthOfSchedule3(Team1, Team2, Team3)):
            result = strengthOfSchedule3(Team1, Team2, Team3)

        else:
            result = [Team1, Team2, Team3]
            print("ERROR!!! Tiebreaker between " + Team1.getName() + ", " + Team2.getName() +
                  ", and " + Team3.getName() + " could not be calculated")

    elif (Team1.getDivision() == Team2.getDivision() and not Team1.getDivision == Team3.getDivision()):
        order = tiebreak2(Team1, Team2)
        first = tiebreak2(order[0], Team3)
        if (first[0] == order[0]):
            second = tiebreak2(order[1], Team3)
            result = [first[0], second[0], second[1]]
        else:
            result = [first[0], first[1], order[1]]

    elif (Team2.getDivision() == Team3.getDivision() and not Team2.getDivision == Team1.getDivision()):
        order = tiebreak2(Team2, Team3)
        first = tiebreak2(order[0], Team1)
        if (first[0] == order[0]):
            second = tiebreak2(order[1], Team1)
            result = [first[0], second[0], second[1]]
        else:
            result = [first[0], first[1], order[1]]

    elif (Team1.getDivision() == Team3.getDivision() and not Team1.getDivision == Team2.getDivision()):
        order = tiebreak2(Team1, Team3)
        first = tiebreak2(order[0], Team2)
        if (first[0] == order[0]):
            second = tiebreak2(order[1], Team2)
            result = [first[0], second[0], second[1]]
        else:
            result = [first[0], first[1], order[1]]

    else:
        if (isH2H3(Team1, Team2, Team3)):
            #print ('h2h3')
            result = h2h3(Team1, Team2, Team3)

        elif (isConfRecord3(Team1, Team2, Team3)):
            #print ('conf record 3')
            result = confRecord3(Team1, Team2, Team3)

        elif (isCommonRecord3(Team1, Team2, Team3)):
            #print ('common record 3')
            result = commonRecord3(Team1, Team2, Team3)

        elif (isStrengthOfVictory3(Team1, Team2, Team3)):
            #print ('sov 3')
            result = strengthOfVictory3(Team1, Team2, Team3)
            
        elif (isStrengthOfSchedule3(Team1, Team2, Team3)):
            result = strengthOfSchedule3(Team1, Team2, Team3)

        else:
            result = [Team1, Team2, Team3]
            print("ERROR!!! Tiebreaker between " + Team1.getName() + ", " + Team2.getName() +
                  ", and " + Team3.getName() + " could not be calculated")

    return (result)


def tiebreak4(Team1, Team2, Team3, Team4):
    #print ("Starting 4 team tiebreaker between " + Team1.getName() + ", " + Team2.getName() + ", " + Team3.getName() + 
           #", and " + Team4.getName())
    result = []
    if (Team1.getDivision() == Team2.getDivision() and Team1.getDivision() == Team3.getDivision() and
            Team1.getDivision() == Team4.getDivision):
        if (isDivRecord4(Team1, Team2, Team3, Team4)):
            result = divRecord4(Team1, Team2, Team3, Team4)
        elif (isCommonRecord4(Team1, Team2, Team3, Team4)):
            result = commonRecord4(Team1, Team2, Team3, Team4)
        elif (isConfRecord4(Team1, Team2, Team3, Team4)):
            result = confRecord4(Team1, Team2, Team3, Team4)
        elif (isStrengthOfVictory4(Team1, Team2, Team3, Team4)):
            result = strengthOfVictory4(Team1, Team2, Team3, Team4)
        elif (isStrengthOfSchedule4(Team1, Team2, Team3, Team4)):
            result = strengthOfSchedule4(Team1, Team2, Team3, Team4)

        else:
            result = [Team1, Team2, Team3, Team4]
            print("ERROR!!! Tiebreaker between " + Team1.getName() + ", " + Team2.getName() +
                  ", " + Team3.getName() + ", and" + Team4.getName() + " could not be calculated")

    elif (Team1.getDivision() == Team2.getDivision() and not Team1.getDivision() == Team3.getDivision() and not
    Team1.getDivision() == Team4.getDivision() and not Team3.getDivision == Team4.getDivision()):
        order = tiebreak2(Team1, Team2)
        first = tiebreak3(order[0], Team3, Team4)
        if (first[0] == order[0]):
            second = tiebreak3(order[1], first[1], first[2])
            result = [first[0], second[0], second[1], second[2]]
        elif (first[1] == order[0]):
            second = tiebreak2(order[1], first[2])
            result = [first[0], order[0], second[0], second[1]]
        else:
            result = [first[0], first[1], order[0], order[1]]


    elif (Team1.getDivision() == Team3.getDivision() and not Team1.getDivision() == Team2.getDivision() and not
    Team1.getDivision() == Team4.getDivision() and not Team3.getDivision == Team4.getDivision()):
        order = tiebreak2(Team1, Team3)
        first = tiebreak3(order[0], Team2, Team4)
        if (first[0] == order[0]):
            second = tiebreak3(order[1], first[1], first[2])
            result = [first[0], second[0], second[1], second[2]]
        elif (first[1] == order[0]):
            second = tiebreak2(order[1], first[2])
            result = [first[0], order[0], second[0], second[1]]
        else:
            result = [first[0], first[1], order[0], order[1]]

    elif (Team1.getDivision() == Team4.getDivision() and not Team1.getDivision() == Team2.getDivision() and not
    Team1.getDivision() == Team3.getDivision() and not Team3.getDivision == Team2.getDivision()):
        order = tiebreak2(Team1, Team4)
        first = tiebreak3(order[0], Team3, Team2)
        if (first[0] == order[0]):
            second = tiebreak3(order[1], first[1], first[2])
            result = [first[0], second[0], second[1], second[2]]
        elif (first[1] == order[0]):
            second = tiebreak2(order[1], first[2])
            result = [first[0], order[0], second[0], second[1]]
        else:
            result = [first[0], first[1], order[0], order[1]]

    elif (Team2.getDivision() == Team3.getDivision() and not Team2.getDivision() == Team1.getDivision() and not
    Team1.getDivision() == Team4.getDivision() and not Team3.getDivision == Team4.getDivision()):
        order = tiebreak2(Team1, Team2)
        first = tiebreak3(order[0], Team3, Team4)
        if (first[0] == order[0]):
            second = tiebreak3(order[1], first[1], first[2])
            result = [first[0], second[0], second[1], second[2]]
        elif (first[1] == order[0]):
            second = tiebreak2(order[1], first[2])
            result = [first[0], order[0], second[0], second[1]]
        else:
            result = [first[0], first[1], order[0], order[1]]

    elif (Team2.getDivision() == Team4.getDivision() and not Team2.getDivision() == Team1.getDivision() and not
    Team1.getDivision() == Team3.getDivision() and not Team3.getDivision == Team1.getDivision()):
        order = tiebreak2(Team4, Team2)
        first = tiebreak3(order[0], Team3, Team1)
        if (first[0] == order[0]):
            second = tiebreak3(order[1], first[1], first[2])
            result = [first[0], second[0], second[1], second[2]]
        elif (first[1] == order[0]):
            second = tiebreak2(order[1], first[2])
            result = [first[0], order[0], second[0], second[1]]
        else:
            result = [first[0], first[1], order[0], order[1]]

    elif (Team3.getDivision() == Team4.getDivision() and not Team3.getDivision() == Team1.getDivision() and not
    Team3.getDivision() == Team2.getDivision() and not Team2.getDivision == Team1.getDivision()):
        order = tiebreak2(Team4, Team3)
        first = tiebreak3(order[0], Team2, Team1)
        if (first[0] == order[0]):
            second = tiebreak3(order[1], first[1], first[2])
            result = [first[0], second[0], second[1], second[2]]
        elif (first[1] == order[0]):
            second = tiebreak2(order[1], first[2])
            result = [first[0], order[0], second[0], second[1]]
        else:
            result = [first[0], first[1], order[0], order[1]]

    elif (Team1.getDivision() == Team2.getDivision() and Team1.getDivision() == Team3.getDivision() and not
    Team1.getDivision() == Team4.getDivision()):
        order = tiebreak3(Team1, Team2, Team3)
        first = tiebreak2(order[0], Team4)
        if (first[0] == order[0]):
            second = tiebreak2(order[1], first[1])
            if (second[0] == order[1]):
                third = tiebreak2(order[2], first[1])
                result = [first[0], second[0], third[0], third[1]]
            else:
                result = [first[0], second[0], second[1], order[2]]

        else:
            result = [first[0], order[0], order[1], order[2]]

    elif (Team1.getDivision() == Team2.getDivision() and Team1.getDivision() == Team4.getDivision() and not
    Team1.getDivision() == Team3.getDivision()):
        order = tiebreak3(Team1, Team2, Team4)
        first = tiebreak2(order[0], Team3)
        if (first[0] == order[0]):
            second = tiebreak2(order[1], first[1])
            if (second[0] == order[1]):
                third = tiebreak2(order[2], first[1])
                result = [first[0], second[0], third[0], third[1]]
            else:
                result = [first[0], second[0], second[1], order[2]]

        else:
            result = [first[0], order[0], order[1], order[2]]

    elif (Team1.getDivision() == Team4.getDivision() and Team1.getDivision() == Team3.getDivision() and not
    Team1.getDivision() == Team2.getDivision()):
        order = tiebreak3(Team1, Team4, Team3)
        first = tiebreak2(order[0], Team2)
        if (first[0] == order[0]):
            second = tiebreak2(order[1], first[1])
            if (second[0] == order[1]):
                third = tiebreak2(order[2], first[1])
                result = [first[0], second[0], third[0], third[1]]
            else:
                result = [first[0], second[0], second[1], order[2]]

        else:
            result = [first[0], order[0], order[1], order[2]]

    elif (Team2.getDivision() == Team3.getDivision() and Team2.getDivision() == Team4.getDivision() and not
    Team2.getDivision() == Team1.getDivision()):
        order = tiebreak3(Team4, Team2, Team3)
        first = tiebreak2(order[0], Team1)
        if (first[0] == order[0]):
            second = tiebreak2(order[1], first[1])
            if (second[0] == order[1]):
                third = tiebreak2(order[2], first[1])
                result = [first[0], second[0], third[0], third[1]]
            else:
                result = [first[0], second[0], second[1], order[2]]

        else:
            result = [first[0], order[0], order[1], order[2]]

    elif (Team1.getDivision() == Team2.getDivision() and Team3.getDivision() == Team4.getDivision and not
    Team1.getDivision() == Team3.getDivision()):
        order1 = tiebreak2(Team1, Team2)
        order2 = tiebreak2(Team3, Team4)
        first = tiebreak2(order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak3(order2[0], order1[1], order2[1])
            result = [first[0], second[0], second[1], second[2]]
        else:
            second = tiebreak3(order1[0], order1[1], order2[1])
            result = [first[0], second[0], second[1], second[2]]

    elif (Team1.getDivision() == Team3.getDivision() and Team2.getDivision() == Team4.getDivision and not
    Team1.getDivision() == Team2.getDivision()):
        order1 = tiebreak2(Team1, Team3)
        order2 = tiebreak2(Team2, Team4)
        first = tiebreak2(order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak3(order2[0], order1[1], order2[1])
            result = [first[0], second[0], second[1], second[2]]
        else:
            second = tiebreak3(order1[0], order1[1], order2[1])
            result = [first[0], second[0], second[1], second[2]]

    elif (Team1.getDivision() == Team4.getDivision() and Team3.getDivision() == Team2.getDivision and not
    Team1.getDivision() == Team3.getDivision()):
        order1 = tiebreak2(Team1, Team4)
        order2 = tiebreak2(Team3, Team2)
        first = tiebreak2(order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak3(order2[0], order1[1], order2[1])
            result = [first[0], second[0], second[1], second[2]]
        else:
            second = tiebreak3(order1[0], order1[1], order2[1])
            result = [first[0], second[0], second[1], second[2]]

    else:
        if (isH2H4(Team1, Team2, Team3, Team4)):
            result = h2h4(Team1, Team2, Team3, Team4)
        elif (isConfRecord4(Team1, Team2, Team3, Team4)):
            result = confRecord4(Team1, Team2, Team3, Team4)
        elif (isCommonRecord4(Team1, Team2, Team3, Team4)):
            result = commonRecord4(Team1, Team2, Team3, Team4)
        elif (isStrengthOfVictory4(Team1, Team2, Team3, Team4)):
            result = strengthOfVictory4(Team1, Team2, Team3, Team4)

        else:
            result = [Team1, Team2, Team3, Team4]
            print("ERROR!!! Tiebreaker between " + Team1.getName() + ", " + Team2.getName() +
                  ", " + Team3.getName() + ", and" + Team4.getName() + " could not be calculated")

    return (result)


def tiebreak5(Team1, Team2, Team3, Team4, Team5):
    #print ("Starting 5 team tiebreaker between " + Team1.getName() + ", " + Team2.getName() + ", " + Team3.getName() + 
           #", " + Team4.getName() + ", and " + Team5.getName())
    result = []
    div1 = Team1.getDivision()
    div2 = Team2.getDivision()
    div3 = Team3.getDivision()
    div4 = Team4.getDivision()
    div5 = Team5.getDivision()

    # 4 in one division
    if (div1 == div2 and div1 == div3 and div1 == div4 and not div1 == div5):
        order = tiebreak4(Team1, Team2, Team3, Team4)
        first = tiebreak2(Team5, order[0])
        if (first[0] == order[0]):
            second = tiebreak2(Team5, order[1])
            if (second[0] == order[1]):
                third = tiebreak2(Team5, order[2])
                if (third[0] == order[2]):
                    fourth = tiebreak2(order[3], Team5)
                    result = [order[0], order[1], order[2], fourth[0], fourth[1]]
                else:
                    result = [order[0], order[1], third[0], order[2], order[3]]
            else:
                result = [order[0], second[0], order[1], order[2], order[3]]
        else:
            result = [first[0], order[0], order[1], order[2], order[3]]

    elif (div1 == div2 and div1 == div3 and div1 == div5 and not div1 == div4):
        order = tiebreak4(Team1, Team2, Team3, Team5)
        first = tiebreak2(Team4, order[0])
        if (first[0] == order[0]):
            second = tiebreak2(Team4, order[1])
            if (second[0] == order[1]):
                third = tiebreak2(Team5, order[2])
                if (third[0] == order[2]):
                    fourth = tiebreak2(order[3], Team4)
                    result = [order[0], order[1], order[2], fourth[0], fourth[1]]
                else:
                    result = [order[0], order[1], third[0], order[2], order[3]]
            else:
                result = [order[0], second[0], order[1], order[2], order[3]]
        else:
            result = [first[0], order[0], order[1], order[2], order[3]]

    elif (div1 == div2 and div1 == div4 and div1 == div5 and not div1 == div3):
        order = tiebreak4(Team1, Team2, Team4, Team5)
        first = tiebreak2(Team3, order[0])
        if (first[0] == order[0]):
            second = tiebreak2(Team3, order[1])
            if (second[0] == order[1]):
                third = tiebreak2(Team3, order[2])
                if (third[0] == order[2]):
                    fourth = tiebreak2(order[3], Team3)
                    result = [order[0], order[1], order[2], fourth[0], fourth[1]]
                else:
                    result = [order[0], order[1], third[0], order[2], order[3]]
            else:
                result = [order[0], second[0], order[1], order[2], order[3]]
        else:
            result = [first[0], order[0], order[1], order[2], order[3]]

    elif (div1 == div3 and div1 == div4 and div1 == div5 and not div1 == div2):
        order = tiebreak4(Team1, Team3, Team4, Team5)
        first = tiebreak2(Team2, order[0])
        if (first[0] == order[0]):
            second = tiebreak2(Team2, order[1])
            if (second[0] == order[1]):
                third = tiebreak2(Team2, order[2])
                if (third[0] == order[2]):
                    fourth = tiebreak2(order[3], Team2)
                    result = [order[0], order[1], order[2], fourth[0], fourth[1]]
                else:
                    result = [order[0], order[1], third[0], order[2], order[3]]
            else:
                result = [order[0], second[0], order[1], order[2], order[3]]
        else:
            result = [first[0], order[0], order[1], order[2], order[3]]

    elif (div2 == div3 and div2 == div4 and div2 == div5 and not div1 == div2):
        order = tiebreak4(Team2, Team3, Team4, Team5)
        first = tiebreak2(Team1, order[0])
        if (first[0] == order[0]):
            second = tiebreak2(Team1, order[1])
            if (second[0] == order[1]):
                third = tiebreak2(Team1, order[2])
                if (third[0] == order[2]):
                    fourth = tiebreak2(order[3], Team1)
                    result = [order[0], order[1], order[2], fourth[0], fourth[1]]
                else:
                    result = [order[0], order[1], third[0], order[2], order[3]]
            else:
                result = [order[0], second[0], order[1], order[2], order[3]]
        else:
            result = [first[0], order[0], order[1], order[2], order[3]]

    # 3 in one division, 2 in the other
    elif (div1 == div2 and div1 == div3 and not div1 == div4 and div4 == div5):
        order1 = tiebreak3 (Team1, Team2, Team3)
        order2 = tiebreak2 (Team4, Team5)
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak2(order1[1], order2[0])
            if (second[0] == order1[1]):
                third = tiebreak2(order1[2], order2[0])
                if (third[0] == order1[2]):
                    result = [order1[0], order1[1], order1[2], order2[0], order2[1]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order1[1], order2[1], fourth[0], fourth[1]]
            else:
                third = tiebreak2(order1[1], order2[1])
                if (third[0] == order2[1]):
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order2[0], order1[1], fourth[0], fourth[1]]
        else:
            second = tiebreak2(order1[0], order2[1])
            if (second == order2[1]):
                result = [order2[0], order2[1], order1[0], order1[1], order1[2]]
            else:
                third = tiebreak2(order2[1], order1[1])
                if (third[0] == order2[1]):
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order2[0], order1[0], order1[1], fourth[0], fourth[1]]
                    
    elif (div1 == div2 and div1 == div4 and not div1 == div3 and div3 == div5):
        order1 = tiebreak3 (Team1, Team2, Team4)
        order2 = tiebreak2 (Team3, Team5)
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak2(order1[1], order2[0])
            if (second[0] == order1[1]):
                third = tiebreak2(order1[2], order2[0])
                if (third[0] == order1[2]):
                    result = [order1[0], order1[1], order1[2], order2[0], order2[1]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order1[1], order2[1], fourth[0], fourth[1]]
            else:
                third = tiebreak2(order1[1], order2[1])
                if (third[0] == order2[1]):
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order2[0], order1[1], fourth[0], fourth[1]]
        else:
            second = tiebreak2(order1[0], order2[1])
            if (second == order2[1]):
                result = [order2[0], order2[1], order1[0], order1[1], order1[2]]
            else:
                third = tiebreak2(order2[1], order1[1])
                if (third[0] == order2[1]):
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order2[0], order1[0], order1[1], fourth[0], fourth[1]]

    elif (div1 == div3 and div1 == div4 and not div1 == div2 and div2 == div5):
        order1 = tiebreak3 (Team1, Team3, Team4)
        order2 = tiebreak2 (Team2, Team5)
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak2(order1[1], order2[0])
            if (second[0] == order1[1]):
                third = tiebreak2(order1[2], order2[0])
                if (third[0] == order1[2]):
                    result = [order1[0], order1[1], order1[2], order2[0], order2[1]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order1[1], order2[1], fourth[0], fourth[1]]
            else:
                third = tiebreak2(order1[1], order2[1])
                if (third[0] == order2[1]):
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order2[0], order1[1], fourth[0], fourth[1]]
        else:
            second = tiebreak2(order1[0], order2[1])
            if (second == order2[1]):
                result = [order2[0], order2[1], order1[0], order1[1], order1[2]]
            else:
                third = tiebreak2(order2[1], order1[1])
                if (third[0] == order2[1]):
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order2[0], order1[0], order1[1], fourth[0], fourth[1]]

    elif (div1 == div2 and div1 == div5 and not div1 == div3 and div3 == div4):
        order1 = tiebreak3 (Team1, Team2, Team5)
        order2 = tiebreak2 (Team3, Team4)
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak2(order1[1], order2[0])
            if (second[0] == order1[1]):
                third = tiebreak2(order1[2], order2[0])
                if (third[0] == order1[2]):
                    result = [order1[0], order1[1], order1[2], order2[0], order2[1]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order1[1], order2[1], fourth[0], fourth[1]]
            else:
                third = tiebreak2(order1[1], order2[1])
                if (third[0] == order2[1]):
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order2[0], order1[1], fourth[0], fourth[1]]
        else:
            second = tiebreak2(order1[0], order2[1])
            if (second == order2[1]):
                result = [order2[0], order2[1], order1[0], order1[1], order1[2]]
            else:
                third = tiebreak2(order2[1], order1[1])
                if (third[0] == order2[1]):
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order2[0], order1[0], order1[1], fourth[0], fourth[1]]

    elif (div1 == div3 and div1 == div5 and not div1 == div2 and div2 == div4):
        order1 = tiebreak3 (Team1, Team3, Team5)
        order2 = tiebreak2 (Team2, Team4)
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak2(order1[1], order2[0])
            if (second[0] == order1[1]):
                third = tiebreak2(order1[2], order2[0])
                if (third[0] == order1[2]):
                    result = [order1[0], order1[1], order1[2], order2[0], order2[1]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order1[1], order2[1], fourth[0], fourth[1]]
            else:
                third = tiebreak2(order1[1], order2[1])
                if (third[0] == order2[1]):
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order2[0], order1[1], fourth[0], fourth[1]]
        else:
            second = tiebreak2(order1[0], order2[1])
            if (second == order2[1]):
                result = [order2[0], order2[1], order1[0], order1[1], order1[2]]
            else:
                third = tiebreak2(order2[1], order1[1])
                if (third[0] == order2[1]):
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order2[0], order1[0], order1[1], fourth[0], fourth[1]]

    elif (div1 == div5 and div1 == div4 and not div1 == div3 and div3 == div2):
        order1 = tiebreak3 (Team1, Team5, Team4)
        order2 = tiebreak2 (Team3, Team2)
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak2(order1[1], order2[0])
            if (second[0] == order1[1]):
                third = tiebreak2(order1[2], order2[0])
                if (third[0] == order1[2]):
                    result = [order1[0], order1[1], order1[2], order2[0], order2[1]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order1[1], order2[1], fourth[0], fourth[1]]
            else:
                third = tiebreak2(order1[1], order2[1])
                if (third[0] == order2[1]):
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order2[0], order1[1], fourth[0], fourth[1]]
        else:
            second = tiebreak2(order1[0], order2[1])
            if (second == order2[1]):
                result = [order2[0], order2[1], order1[0], order1[1], order1[2]]
            else:
                third = tiebreak2(order2[1], order1[1])
                if (third[0] == order2[1]):
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order2[0], order1[0], order1[1], fourth[0], fourth[1]]

    elif (div3 == div2 and div3 == div4 and not div1 == div3 and div1 == div5):
        order1 = tiebreak3 (Team3, Team2, Team4)
        order2 = tiebreak2 (Team1, Team5)
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak2(order1[1], order2[0])
            if (second[0] == order1[1]):
                third = tiebreak2(order1[2], order2[0])
                if (third[0] == order1[2]):
                    result = [order1[0], order1[1], order1[2], order2[0], order2[1]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order1[1], order2[1], fourth[0], fourth[1]]
            else:
                third = tiebreak2(order1[1], order2[1])
                if (third[0] == order2[1]):
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order2[0], order1[1], fourth[0], fourth[1]]
        else:
            second = tiebreak2(order1[0], order2[1])
            if (second == order2[1]):
                result = [order2[0], order2[1], order1[0], order1[1], order1[2]]
            else:
                third = tiebreak2(order2[1], order1[1])
                if (third[0] == order2[1]):
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order2[0], order1[0], order1[1], fourth[0], fourth[1]]

    elif (div3 == div2 and div3 == div5 and not div1 == div3 and div1 == div4):
        order1 = tiebreak3 (Team3, Team2, Team5)
        order2 = tiebreak2 (Team1, Team4)
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak2(order1[1], order2[0])
            if (second[0] == order1[1]):
                third = tiebreak2(order1[2], order2[0])
                if (third[0] == order1[2]):
                    result = [order1[0], order1[1], order1[2], order2[0], order2[1]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order1[1], order2[1], fourth[0], fourth[1]]
            else:
                third = tiebreak2(order1[1], order2[1])
                if (third[0] == order2[1]):
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order2[0], order1[1], fourth[0], fourth[1]]
        else:
            second = tiebreak2(order1[0], order2[1])
            if (second == order2[1]):
                result = [order2[0], order2[1], order1[0], order1[1], order1[2]]
            else:
                third = tiebreak2(order2[1], order1[1])
                if (third[0] == order2[1]):
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order2[0], order1[0], order1[1], fourth[0], fourth[1]]

    elif (div4 == div2 and div4 == div5 and not div1 == div4 and div1 == div3):
        order1 = tiebreak3 (Team4, Team2, Team5)
        order2 = tiebreak2 (Team1, Team3)
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak2(order1[1], order2[0])
            if (second[0] == order1[1]):
                third = tiebreak2(order1[2], order2[0])
                if (third[0] == order1[2]):
                    result = [order1[0], order1[1], order1[2], order2[0], order2[1]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order1[1], order2[1], fourth[0], fourth[1]]
            else:
                third = tiebreak2(order1[1], order2[1])
                if (third[0] == order2[1]):
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order2[0], order1[1], fourth[0], fourth[1]]
        else:
            second = tiebreak2(order1[0], order2[1])
            if (second == order2[1]):
                result = [order2[0], order2[1], order1[0], order1[1], order1[2]]
            else:
                third = tiebreak2(order2[1], order1[1])
                if (third[0] == order2[1]):
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order2[0], order1[0], order1[1], fourth[0], fourth[1]]

    elif (div4 == div3 and div4 == div5 and not div1 == div4 and div1 == div2):
        order1 = tiebreak3 (Team4, Team3, Team5)
        order2 = tiebreak2 (Team1, Team2)
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak2(order1[1], order2[0])
            if (second[0] == order1[1]):
                third = tiebreak2(order1[2], order2[0])
                if (third[0] == order1[2]):
                    result = [order1[0], order1[1], order1[2], order2[0], order2[1]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order1[1], order2[1], fourth[0], fourth[1]]
            else:
                third = tiebreak2(order1[1], order2[1])
                if (third[0] == order2[1]):
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order1[0], order2[0], order1[1], fourth[0], fourth[1]]
        else:
            second = tiebreak2(order1[0], order2[1])
            if (second == order2[1]):
                result = [order2[0], order2[1], order1[0], order1[1], order1[2]]
            else:
                third = tiebreak2(order2[1], order1[1])
                if (third[0] == order2[1]):
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2]]
                else:
                    fourth = tiebreak2(order1[2], order2[1])
                    result = [order2[0], order1[0], order1[1], fourth[0], fourth[1]]

    #3 teams in 1 division, 1 in 2 others
    elif (div1 == div2 and div1 == div3 and not div1 == div4 and not div4 == div5):
        first = tiebreak3(Team1, Team2, Team3)
        order1 = tiebreak3(first[0], Team4, Team5)
        if (order1[0] == first[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak3(first[2], order1[1], order1[2])
                result = [first[0], first[1], third[0], third[1], third[2]]
            elif (order2[1] == first[1]):
                fourth = tiebreak2(first[2], order2[2])
                result = [first[0], order2[0], order2[1], fourth[0], fourth[1]]
            else:
                result = [first[0], order2[0], order2[1], first[1], first[2]]
        elif (order1[1] == first[0]):
            order2 = tiebreak2(first[1], order1[2])
            if (order2[0] == first[1]):
                fourth = tiebreak2(order2[1], first[2])
                result = [order1[0], first[0], order2[0], fourth[0], fourth[1]]
            else: 
                result = [order1[0], first[0], order2[0], first[1], first[2]]
        else: 
            result = [order1[0], order1[1], first[0], first[1], first[2]]
    
    elif (div1 == div2 and div1 == div4 and not div1 == div3 and not div3 == div5):
        first = tiebreak3(Team1, Team2, Team4)
        order1 = tiebreak3(first[0], Team3, Team5)
        if (order1[0] == first[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak3(first[2], order1[1], order1[2])
                result = [first[0], first[1], third[0], third[1], third[2]]
            elif (order2[1] == first[1]):
                fourth = tiebreak2(first[2], order2[2])
                result = [first[0], order2[0], order2[1], fourth[0], fourth[1]]
            else:
                result = [first[0], order2[0], order2[1], first[1], first[2]]
        elif (order1[1] == first[0]):
            order2 = tiebreak2(first[1], order1[2])
            if (order2[0] == first[1]):
                fourth = tiebreak2(order2[1], first[2])
                result = [order1[0], first[0], order2[0], fourth[0], fourth[1]]
            else: 
                result = [order1[0], first[0], order2[0], first[1], first[2]]
        else: 
            result = [order1[0], order1[1], first[0], first[1], first[2]]
            
    elif (div1 == div4 and div1 == div3 and not div1 == div2 and not div2 == div5):
        first = tiebreak3(Team1, Team4, Team3)
        order1 = tiebreak3(first[0], Team2, Team5)
        if (order1[0] == first[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak3(first[2], order1[1], order1[2])
                result = [first[0], first[1], third[0], third[1], third[2]]
            elif (order2[1] == first[1]):
                fourth = tiebreak2(first[2], order2[2])
                result = [first[0], order2[0], order2[1], fourth[0], fourth[1]]
            else:
                result = [first[0], order2[0], order2[1], first[1], first[2]]
        elif (order1[1] == first[0]):
            order2 = tiebreak2(first[1], order1[2])
            if (order2[0] == first[1]):
                fourth = tiebreak2(order2[1], first[2])
                result = [order1[0], first[0], order2[0], fourth[0], fourth[1]]
            else: 
                result = [order1[0], first[0], order2[0], first[1], first[2]]
        else: 
            result = [order1[0], order1[1], first[0], first[1], first[2]]
            
    elif (div1 == div2 and div1 == div5 and not div1 == div4 and not div4 == div3):
        first = tiebreak3(Team1, Team2, Team5)
        order1 = tiebreak3(first[0], Team4, Team3)
        if (order1[0] == first[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak3(first[2], order1[1], order1[2])
                result = [first[0], first[1], third[0], third[1], third[2]]
            elif (order2[1] == first[1]):
                fourth = tiebreak2(first[2], order2[2])
                result = [first[0], order2[0], order2[1], fourth[0], fourth[1]]
            else:
                result = [first[0], order2[0], order2[1], first[1], first[2]]
        elif (order1[1] == first[0]):
            order2 = tiebreak2(first[1], order1[2])
            if (order2[0] == first[1]):
                fourth = tiebreak2(order2[1], first[2])
                result = [order1[0], first[0], order2[0], fourth[0], fourth[1]]
            else: 
                result = [order1[0], first[0], order2[0], first[1], first[2]]
        else: 
            result = [order1[0], order1[1], first[0], first[1], first[2]]
            
    elif (div1 == div5 and div1 == div3 and not div1 == div4 and not div4 == div2):
        first = tiebreak3(Team1, Team5, Team3)
        order1 = tiebreak3(first[0], Team4, Team2)
        if (order1[0] == first[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak3(first[2], order1[1], order1[2])
                result = [first[0], first[1], third[0], third[1], third[2]]
            elif (order2[1] == first[1]):
                fourth = tiebreak2(first[2], order2[2])
                result = [first[0], order2[0], order2[1], fourth[0], fourth[1]]
            else:
                result = [first[0], order2[0], order2[1], first[1], first[2]]
        elif (order1[1] == first[0]):
            order2 = tiebreak2(first[1], order1[2])
            if (order2[0] == first[1]):
                fourth = tiebreak2(order2[1], first[2])
                result = [order1[0], first[0], order2[0], fourth[0], fourth[1]]
            else: 
                result = [order1[0], first[0], order2[0], first[1], first[2]]
        else: 
            result = [order1[0], order1[1], first[0], first[1], first[2]]
            
    elif (div1 == div4 and div1 == div5 and not div1 == div2 and not div2 == div3):
        first = tiebreak3(Team1, Team4, Team5)
        order1 = tiebreak3(first[0], Team2, Team3)
        if (order1[0] == first[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak3(first[2], order1[1], order1[2])
                result = [first[0], first[1], third[0], third[1], third[2]]
            elif (order2[1] == first[1]):
                fourth = tiebreak2(first[2], order2[2])
                result = [first[0], order2[0], order2[1], fourth[0], fourth[1]]
            else:
                result = [first[0], order2[0], order2[1], first[1], first[2]]
        elif (order1[1] == first[0]):
            order2 = tiebreak2(first[1], order1[2])
            if (order2[0] == first[1]):
                fourth = tiebreak2(order2[1], first[2])
                result = [order1[0], first[0], order2[0], fourth[0], fourth[1]]
            else: 
                result = [order1[0], first[0], order2[0], first[1], first[2]]
        else: 
            result = [order1[0], order1[1], first[0], first[1], first[2]]
            
    elif (div4 == div2 and div4 == div3 and not div4 == div1 and not div1 == div5):
        first = tiebreak3(Team4, Team2, Team3)
        order1 = tiebreak3(first[0], Team1, Team5)
        if (order1[0] == first[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak3(first[2], order1[1], order1[2])
                result = [first[0], first[1], third[0], third[1], third[2]]
            elif (order2[1] == first[1]):
                fourth = tiebreak2(first[2], order2[2])
                result = [first[0], order2[0], order2[1], fourth[0], fourth[1]]
            else:
                result = [first[0], order2[0], order2[1], first[1], first[2]]
        elif (order1[1] == first[0]):
            order2 = tiebreak2(first[1], order1[2])
            if (order2[0] == first[1]):
                fourth = tiebreak2(order2[1], first[2])
                result = [order1[0], first[0], order2[0], fourth[0], fourth[1]]
            else: 
                result = [order1[0], first[0], order2[0], first[1], first[2]]
        else: 
            result = [order1[0], order1[1], first[0], first[1], first[2]]
            
    elif (div5 == div2 and div5 == div3 and not div5 == div4 and not div4 == div1):
        first = tiebreak3(Team1, Team2, Team3)
        order1 = tiebreak3(first[0], Team4, Team1)
        if (order1[0] == first[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak3(first[2], order1[1], order1[2])
                result = [first[0], first[1], third[0], third[1], third[2]]
            elif (order2[1] == first[1]):
                fourth = tiebreak2(first[2], order2[2])
                result = [first[0], order2[0], order2[1], fourth[0], fourth[1]]
            else:
                result = [first[0], order2[0], order2[1], first[1], first[2]]
        elif (order1[1] == first[0]):
            order2 = tiebreak2(first[1], order1[2])
            if (order2[0] == first[1]):
                fourth = tiebreak2(order2[1], first[2])
                result = [order1[0], first[0], order2[0], fourth[0], fourth[1]]
            else: 
                result = [order1[0], first[0], order2[0], first[1], first[2]]
        else: 
            result = [order1[0], order1[1], first[0], first[1], first[2]]
            
    elif (div5 == div2 and div5 == div4 and not div5 == div3 and not div3 == div1):
        first = tiebreak3(Team5, Team2, Team4)
        order1 = tiebreak3(first[0], Team3, Team1)
        if (order1[0] == first[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak3(first[2], order1[1], order1[2])
                result = [first[0], first[1], third[0], third[1], third[2]]
            elif (order2[1] == first[1]):
                fourth = tiebreak2(first[2], order2[2])
                result = [first[0], order2[0], order2[1], fourth[0], fourth[1]]
            else:
                result = [first[0], order2[0], order2[1], first[1], first[2]]
        elif (order1[1] == first[0]):
            order2 = tiebreak2(first[1], order1[2])
            if (order2[0] == first[1]):
                fourth = tiebreak2(order2[1], first[2])
                result = [order1[0], first[0], order2[0], fourth[0], fourth[1]]
            else: 
                result = [order1[0], first[0], order2[0], first[1], first[2]]
        else: 
            result = [order1[0], order1[1], first[0], first[1], first[2]]
            
    elif (div5 == div4 and div5 == div3 and not div5 == div2 and not div2 == div1):
        first = tiebreak3(Team5, Team4, Team3)
        order1 = tiebreak3(first[0], Team2, Team1)
        if (order1[0] == first[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak3(first[2], order1[1], order1[2])
                result = [first[0], first[1], third[0], third[1], third[2]]
            elif (order2[1] == first[1]):
                fourth = tiebreak2(first[2], order2[2])
                result = [first[0], order2[0], order2[1], fourth[0], fourth[1]]
            else:
                result = [first[0], order2[0], order2[1], first[1], first[2]]
        elif (order1[1] == first[0]):
            order2 = tiebreak2(first[1], order1[2])
            if (order2[0] == first[1]):
                fourth = tiebreak2(order2[1], first[2])
                result = [order1[0], first[0], order2[0], fourth[0], fourth[1]]
            else: 
                result = [order1[0], first[0], order2[0], first[1], first[2]]
        else: 
            result = [order1[0], order1[1], first[0], first[1], first[2]]
            
    #2 teams in 2 divisions, 1 in another
    elif (div1 == div2 and div3 == div4 and not div1 == div3 and not div1 == div5 and not div3 == div5):
        first = tiebreak2(Team1, Team2)
        second = tiebreak2(Team3, Team4)
        order1 = tiebreak3(first[0], second[0], Team5)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]
                    
    elif (div1 == div2 and div3 == div5 and not div1 == div3 and not div1 == div4 and not div3 == div4):
        first = tiebreak2(Team1, Team2)
        second = tiebreak2(Team3, Team5)
        order1 = tiebreak3(first[0], second[0], Team4)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]
            
    elif (div1 == div2 and div5 == div4 and not div1 == div5 and not div1 == div3 and not div3 == div5):
        first = tiebreak2(Team1, Team2)
        second = tiebreak2(Team5, Team4)
        order1 = tiebreak3(first[0], second[0], Team3)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]
    
    elif (div1 == div3 and div2 == div4 and not div1 == div2 and not div1 == div5 and not div2 == div5):
        first = tiebreak2(Team1, Team3)
        second = tiebreak2(Team2, Team4)
        order1 = tiebreak3(first[0], second[0], Team5)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]
        
    elif (div1 == div3 and div2 == div5 and not div1 == div2 and not div1 == div4 and not div2 == div4):
        first = tiebreak2(Team1, Team3)
        second = tiebreak2(Team2, Team5)
        order1 = tiebreak3(first[0], second[0], Team4)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]

    elif (div1 == div4 and div3 == div2 and not div1 == div3 and not div1 == div5 and not div3 == div5):
        first = tiebreak2(Team1, Team4)
        second = tiebreak2(Team3, Team2)
        order1 = tiebreak3(first[0], second[0], Team5)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]
                    
    elif (div1 == div5 and div3 == div2 and not div1 == div3 and not div1 == div4 and not div3 == div4):
        first = tiebreak2(Team1, Team5)
        second = tiebreak2(Team3, Team2)
        order1 = tiebreak3(first[0], second[0], Team4)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]

    elif (div1 == div4 and div5 == div2 and not div1 == div5 and not div1 == div3 and not div3 == div5):
        first = tiebreak2(Team1, Team4)
        second = tiebreak2(Team5, Team2)
        order1 = tiebreak3(first[0], second[0], Team3)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]

    elif (div1 == div5 and div4 == div2 and not div1 == div4 and not div1 == div3 and not div3 == div4):
        first = tiebreak2(Team1, Team5)
        second = tiebreak2(Team4, Team2)
        order1 = tiebreak3(first[0], second[0], Team3)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]

    elif (div1 == div3 and div5 == div4 and not div1 == div5 and not div1 == div2 and not div2 == div5):
        first = tiebreak2(Team1, Team3)
        second = tiebreak2(Team5, Team4)
        order1 = tiebreak3(first[0], second[0], Team2)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]
                    
    elif (div1 == div4 and div5 == div3 and not div1 == div5 and not div1 == div2 and not div2 == div5):
        first = tiebreak2(Team1, Team4)
        second = tiebreak2(Team5, Team3)
        order1 = tiebreak3(first[0], second[0], Team2)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]
                    
    elif (div1 == div5 and div4 == div3 and not div1 == div4 and not div1 == div2 and not div2 == div4):
        first = tiebreak2(Team1, Team5)
        second = tiebreak2(Team4, Team3)
        order1 = tiebreak3(first[0], second[0], Team2)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]

    elif (div5 == div2 and div3 == div4 and not div5 == div3 and not div1 == div5 and not div3 == div1):
        first = tiebreak2(Team5, Team2)
        second = tiebreak2(Team3, Team4)
        order1 = tiebreak3(first[0], second[0], Team1)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]
                    
    elif (div5 == div3 and div2 == div4 and not div5 == div2 and not div1 == div5 and not div2 == div1):
        first = tiebreak2(Team5, Team3)
        second = tiebreak2(Team2, Team4)
        order1 = tiebreak3(first[0], second[0], Team1)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]
                    
    elif (div5 == div4 and div2 == div3 and not div5 == div2 and not div1 == div5 and not div2 == div1):
        first = tiebreak2(Team5, Team4)
        second = tiebreak2(Team2, Team3)
        order1 = tiebreak3(first[0], second[0], Team1)
        if (first[0] == order1[0]):
            order2 = tiebreak3(first[1], order1[1], order1[2])
            if (order2[0] == first[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == second[0]):
                    fourth = tiebreak2(third[1], second[1])
                    result = [first[0], first[1], second[0], fourth[0], fourth[1]]
                else: 
                    result = [first[0], first[1], third[0], third[1], second[1]]
            elif (order2[0] == second[0]):
                third = tiebreak3(order2[1], order2[2], second[1])
                result = [first[0], second[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [first[0], order2[0], third[0], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [first[0], order2[0], third[0], fourth[0], fourth[1]]
        elif (second[0] == order1[0]):
            order2 = tiebreak3(second[1], order1[1], order1[2])
            if (order2[0] == second[1]):
                third = tiebreak2(order2[1], order2[2])
                if (third[0] == first[0]):
                    fourth = tiebreak2(third[1], first[1])
                    result = [second[0], second[1], first[0], fourth[0], fourth[1]]
                else: 
                    result = [second[0], second[1], third[0], third[1], first[1]]
            elif (order2[0] == first[0]):
                third = tiebreak3(order2[1], order2[2], first[1])
                result = [second[0], first[0], third[0], third[1], third[2]]
            else: 
                third = tiebreak2(second[1], first[0])
                if (third[0] == second[1]):
                    result = [second[0], order2[0], third[0], first[0], first[1]]
                else: 
                    fourth = tiebreak2(second[1], first[1])
                    result = [second[0], order2[0], third[0], fourth[0], fourth[1]]
        else: 
            if (order1[1] == first[0]):
                third = tiebreak2(first[1], second[0])
                if (third[0] == first[1]):
                    result = [order1[0], first[0], first[1], second[0], second[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], first[0], third[0], fourth[0], fourth[1]]
            else:
                third = tiebreak2(first[0], second[1])
                if (third[0] == second[1]):
                    result = [order1[0], second[0], second[1], first[0], first[1]]
                else: 
                    fourth = tiebreak2(first[1], second[1])
                    result = [order1[0], second[0], third[0], fourth[0], fourth[1]]

    #2 in one division, 3 others in separate ones
    elif (div1 == div2 and not div1 == div3 and not div1 == div4 and not div1 == div5):
        order = tiebreak2(Team1, Team2)
        first = tiebreak4(order[0], Team3, Team4, Team5)
        if (order[0] == first[0]):
            second = tiebreak4(order[1], first[1], first[2], first[3])
            result = [first[0], second[0], second[1], second[2], second[3]]
        elif (order[0] == first[1]):
            third = tiebreak3(order[1], first[2], first[3])
            result = [first[0], order[0], third[0], third[1], third[2]]
        elif (order[0] == first[2]):
            fourth = tiebreak2(order[1], first[3])
            result = [first[0], first[1], first[2], fourth[0], fourth[1]]
        else: 
            result = [first[0], first[1], first[2], order[0], order[1]]
    
    elif (div1 == div3 and not div1 == div2 and not div1 == div4 and not div1 == div5):
        order = tiebreak2(Team1, Team3)
        first = tiebreak4(order[0], Team2, Team4, Team5)
        if (order[0] == first[0]):
            second = tiebreak4(order[1], first[1], first[2], first[3])
            result = [first[0], second[0], second[1], second[2], second[3]]
        elif (order[0] == first[1]):
            third = tiebreak3(order[1], first[2], first[3])
            result = [first[0], order[0], third[0], third[1], third[2]]
        elif (order[0] == first[2]):
            fourth = tiebreak2(order[1], first[3])
            result = [first[0], first[1], first[2], fourth[0], fourth[1]]
        else: 
            result = [first[0], first[1], first[2], order[0], order[1]]
    
    elif (div1 == div4 and not div1 == div2 and not div1 == div3 and not div1 == div5):
        order = tiebreak2(Team1, Team4)
        first = tiebreak4(order[0], Team2, Team3, Team5)
        if (order[0] == first[0]):
            second = tiebreak4(order[1], first[1], first[2], first[3])
            result = [first[0], second[0], second[1], second[2], second[3]]
        elif (order[0] == first[1]):
            third = tiebreak3(order[1], first[2], first[3])
            result = [first[0], order[0], third[0], third[1], third[2]]
        elif (order[0] == first[2]):
            fourth = tiebreak2(order[1], first[3])
            result = [first[0], first[1], first[2], fourth[0], fourth[1]]
        else: 
            result = [first[0], first[1], first[2], order[0], order[1]]
            
    elif (div1 == div5 and not div1 == div2 and not div1 == div3 and not div1 == div4):
        order = tiebreak2(Team1, Team5)
        first = tiebreak4(order[0], Team2, Team3, Team4)
        if (order[0] == first[0]):
            second = tiebreak4(order[1], first[1], first[2], first[3])
            result = [first[0], second[0], second[1], second[2], second[3]]
        elif (order[0] == first[1]):
            third = tiebreak3(order[1], first[2], first[3])
            result = [first[0], order[0], third[0], third[1], third[2]]
        elif (order[0] == first[2]):
            fourth = tiebreak2(order[1], first[3])
            result = [first[0], first[1], first[2], fourth[0], fourth[1]]
        else: 
            result = [first[0], first[1], first[2], order[0], order[1]]
            
    elif (div3 == div2 and not div3 == div1 and not div3 == div4 and not div3 == div5):
        order = tiebreak2(Team3, Team2)
        first = tiebreak4(order[0], Team1, Team4, Team5)
        if (order[0] == first[0]):
            second = tiebreak4(order[1], first[1], first[2], first[3])
            result = [first[0], second[0], second[1], second[2], second[3]]
        elif (order[0] == first[1]):
            third = tiebreak3(order[1], first[2], first[3])
            result = [first[0], order[0], third[0], third[1], third[2]]
        elif (order[0] == first[2]):
            fourth = tiebreak2(order[1], first[3])
            result = [first[0], first[1], first[2], fourth[0], fourth[1]]
        else: 
            result = [first[0], first[1], first[2], order[0], order[1]]
            
    elif (div4 == div2 and not div4 == div1 and not div3 == div4 and not div4 == div5):
        order = tiebreak2(Team4, Team2)
        first = tiebreak4(order[0], Team1, Team3, Team5)
        if (order[0] == first[0]):
            second = tiebreak4(order[1], first[1], first[2], first[3])
            result = [first[0], second[0], second[1], second[2], second[3]]
        elif (order[0] == first[1]):
            third = tiebreak3(order[1], first[2], first[3])
            result = [first[0], order[0], third[0], third[1], third[2]]
        elif (order[0] == first[2]):
            fourth = tiebreak2(order[1], first[3])
            result = [first[0], first[1], first[2], fourth[0], fourth[1]]
        else: 
            result = [first[0], first[1], first[2], order[0], order[1]]
            
            
    elif (div5 == div2 and not div5 == div1 and not div3 == div5 and not div4 == div5):
        order = tiebreak2(Team5, Team2)
        first = tiebreak4(order[0], Team1, Team3, Team4)
        if (order[0] == first[0]):
            second = tiebreak4(order[1], first[1], first[2], first[3])
            result = [first[0], second[0], second[1], second[2], second[3]]
        elif (order[0] == first[1]):
            third = tiebreak3(order[1], first[2], first[3])
            result = [first[0], order[0], third[0], third[1], third[2]]
        elif (order[0] == first[2]):
            fourth = tiebreak2(order[1], first[3])
            result = [first[0], first[1], first[2], fourth[0], fourth[1]]
        else: 
            result = [first[0], first[1], first[2], order[0], order[1]]
    
    elif (div4 == div3 and not div4 == div1 and not div2 == div4 and not div4 == div5):
        order = tiebreak2(Team4, Team3)
        first = tiebreak4(order[0], Team1, Team2, Team5)
        if (order[0] == first[0]):
            second = tiebreak4(order[1], first[1], first[2], first[3])
            result = [first[0], second[0], second[1], second[2], second[3]]
        elif (order[0] == first[1]):
            third = tiebreak3(order[1], first[2], first[3])
            result = [first[0], order[0], third[0], third[1], third[2]]
        elif (order[0] == first[2]):
            fourth = tiebreak2(order[1], first[3])
            result = [first[0], first[1], first[2], fourth[0], fourth[1]]
        else: 
            result = [first[0], first[1], first[2], order[0], order[1]]
            
    elif (div5 == div3 and not div5 == div1 and not div2 == div5 and not div4 == div5):
        order = tiebreak2(Team5, Team3)
        first = tiebreak4(order[0], Team1, Team2, Team4)
        if (order[0] == first[0]):
            second = tiebreak4(order[1], first[1], first[2], first[3])
            result = [first[0], second[0], second[1], second[2], second[3]]
        elif (order[0] == first[1]):
            third = tiebreak3(order[1], first[2], first[3])
            result = [first[0], order[0], third[0], third[1], third[2]]
        elif (order[0] == first[2]):
            fourth = tiebreak2(order[1], first[3])
            result = [first[0], first[1], first[2], fourth[0], fourth[1]]
        else: 
            result = [first[0], first[1], first[2], order[0], order[1]]
            
    elif (div5 == div4 and not div5 == div1 and not div2 == div5 and not div3 == div5):
        order = tiebreak2(Team5, Team4)
        first = tiebreak4(order[0], Team1, Team2, Team3)
        if (order[0] == first[0]):
            second = tiebreak4(order[1], first[1], first[2], first[3])
            result = [first[0], second[0], second[1], second[2], second[3]]
        elif (order[0] == first[1]):
            third = tiebreak3(order[1], first[2], first[3])
            result = [first[0], order[0], third[0], third[1], third[2]]
        elif (order[0] == first[2]):
            fourth = tiebreak2(order[1], first[3])
            result = [first[0], first[1], first[2], fourth[0], fourth[1]]
        else: 
            result = [first[0], first[1], first[2], order[0], order[1]]
    
    else:
        print ("tiebreak 5 failed")
        result = [Team1, Team2, Team3, Team4, Team5]
    
    return (result)
    

def tiebreak6(Team1, Team2, Team3, Team4, Team5, Team6):
    #print ("Starting 6 team tiebreaker between " + Team1.getName() + ", " + Team2.getName() + ", " + Team3.getName() + 
           #", " + Team4.getName() + ", " + Team5.getName() + ", and " + Team6.getName())
    teamList = [Team1, Team2, Team3, Team4, Team5, Team6]
    
    divCounts = Counter(Team.getDivision() for Team in teamList)
    sortList = sorted(teamList, key=lambda x: (divCounts[x.getDivision()], 
                                               x.getDivision()), reverse=True)
    
    div1 = 2
    div2 = 1
    div3 = 0
    div4 = 0
    
    if (sortList[1].getDivision() == sortList[2].getDivision()):
        if (sortList[2].getDivision() == sortList[3].getDivision()):
            div1 = 4
        else: 
            div1 = 3
    else:
        div2 = 2
        
    if (div1 == 4):
        if (sortList[4].getDivision() == sortList[5].getDivision()):
            div2 = 2
        else: 
            div3 = 1
    elif (div1 == 3):
        if (sortList[3].getDivision() == sortList[4].getDivision()):
            if (sortList[4].getDivision() == sortList[5].getDivision()):
                div2 = 3
            else: 
                div2 = 2
                div3 = 1
        else: 
            div3 = 1
            div4 = 1
    else: 
        if (sortList[4].getDivision() == sortList[5].getDivision()):
            div2 = 2
            div3 = 2
        else: 
            div2 = 2
            div3 = 1
            div4 = 1
    
    if (div1 == 4 and div2 == 2):
        order1 = tiebreak4(sortList[0], sortList[1], sortList[2], sortList[3])
        order2 = tiebreak2(sortList[4], sortList[5])
        result1 = tiebreak2(order1[0], order2[0])
        if (result1[0] == order1[0]):
            result2 = tiebreak2(order1[1], order2[0])
            if (result2[0] == order1[1]):
                result3 = tiebreak2(order1[2], order2[0])
                if (result3[0] == order1[2]):
                    result4 = tiebreak2(order1[3], order2[0])
                    if (result4[0] == order1[3]):
                        result = [order1[0], order1[1], order1[2], order1[3], order2[0], order2[1]]
                    else: 
                        result5 = tiebreak2(order1[3], order2[1])
                        result = [order1[0], order1[1], order1[2], order2[0], result5[0], result5[1]]
                else: 
                    result4 = tiebreak2(order1[2], order2[1])
                    if (result4[0] == order1[2]):
                        result5 = tiebreak2(order1[3], order2[1])
                        result = [order1[0], order1[1], order2[0], order1[2], result5[0], result5[1]]
                    else: 
                        result = [order1[0], order1[1], order2[0], order2[1], order1[2], order1[3]]
            else: 
                result3 = tiebreak2(order1[1], order2[1])
                if (result3[0] == order1[1]):
                    result4 = tiebreak2(order1[2], order2[1])
                    if (result4[0] == order1[2]):
                        result5 = tiebreak2(order1[3], order2[1])
                        result = [order1[0], order2[0], order1[1], order1[2], result5[0], result5[1]]
                    else: 
                        result = [order1[0], order2[0], order1[1], order2[1], order1[2], order1[3]]
                else: 
                    result = [order1[0], order2[0], order2[1], order1[1], order1[2], order1[3]]
        else:
            result2 = tiebreak2(order1[0], order2[1])
            if (result2[0] == order1[0]):
                result3 = tiebreak2(order1[1], order2[1])
                if (result3[0] == order1[1]):
                    result4 = tiebreak2(order1[2], order2[1])
                    if (result4[0] == order1[2]):
                        result5 = tiebreak2(order1[3], order2[1])
                        result = [order2[0], order1[0], order1[1], order1[2], result5[0], result5[1]]
                    else: 
                        result = [order2[0], order1[0], order1[1], order2[1], order1[2], order1[3]]
                else: 
                    result = [order2[0], order1[0], order2[1], order1[1], order1[2], order1[3]]
            else: 
                result = [order2[0], order2[1], order1[0], order1[1], order1[2], order1[3]]
                
    elif (div1 == 4 and div2 == 1):
        order = tiebreak4(sortList[0], sortList[1], sortList[2], sortList[3])
        result1 = tiebreak3(order[0], sortList[4], sortList[5])
        if (result1[0] == order[0]):
            result2 = tiebreak3(order[1], sortList[4], sortList[5])
            if (result2[0] == order[1]):
                result3 = tiebreak3 (order[2], sortList[4], sortList[5])
                if (result3[0] == order[2]):
                    result4 = tiebreak3(order[3], sortList[4], sortList[5])
                    result = [order[0], order[1], order[2], result4[0], result4[1], result4[2]]
                elif (result3[1] == order[2]): 
                    result4 = tiebreak2(result3[2], order[3])
                    result = [order[0], order[1], result3[0], order[2], result4[0], result4[1]]
                else:
                    result = [order[0], order[1], result3[0], result3[1], order[2], order[3]]
            elif (result2[1] == order[1]):
                result3 = tiebreak2(order[2], result2[2])
                if (result3[0] == order[2]):
                    result4 = tiebreak2(order[3], result2[2])
                    result = [order[0], result2[0], order[1], order[2], result4[0], result4[1]]
                else: 
                    result = [order[0], result2[0], order[1], result3[0], order[2], order[3]]
            else:
                result = [order[0], result2[0], result2[1], order[1], order[2], order[3]]
        elif (result1[1] == order[0]):
            result2 = tiebreak2(order[1], result2[2])
            if (result2[0] == order[1]):
                result3 = tiebreak2(order[2], result2[2])
                if (result3[0] == order[2]):
                    result4 = tiebreak2(order[3], result2[2])
                    result = [result1[0], order[0], order[1], order[2], result4[0], result4[1]]
                else: 
                    result = [result1[0], order[0], order[1], result3[0], order[2], order[3]]
            else: 
                result = [result1[0], order[0], result2[0], order[1], order[2], order[3]]
        else:
            result = [result1[0], result1[1], order[0], order[1], order[2], order[3]]
            
    elif (div1 == 3 and div2 == 2):
        order1 = tiebreak3(sortList[0], sortList[1], sortList[2])
        order2 = tiebreak2(sortList[3], sortList[4])
        result1 = tiebreak3(order1[0], order2[0], sortList[5])
        if (result1[0] == order1[0]):
            result2 = tiebreak5(order1[1], order1[2], order2[0], order2[1], sortList[5])
            result = [order1[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
        elif (result1[0] == order2[0]):
            result2 = tiebreak5(order1[1], order1[2], order1[0], order2[1], sortList[5])
            result = [order2[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
        else:
            result2 = tiebreak5 (order1[0], order1[1], order1[2], order2[0], order2[1])
            result = [result1[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
    
    elif (div1 == 3 and div2 == 1):
        order = tiebreak3(sortList[0], sortList[1], sortList[2])
        result1 = tiebreak4(order[0], sortList[3], sortList[4], sortList[5])
        if (result1[0] == order[0]):
            result2 = tiebreak5(order[1], order[2], result1[1], result1[2], result1[3])
            result = [order[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
        elif (result1[0] == sortList[3]):
            result2 = tiebreak5(order[1], order[2], result1[1], result1[2], result1[3])
            result = [result1[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
        elif (result1[0] == sortList[4]):
            result2 = tiebreak5(order[1], order[2], result1[1], result1[2], result1[3])
            result = [result1[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
        else:
            result2 = tiebreak5(order[1], order[2], result1[1], result1[2], result1[3])
            result = [result1[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
            
    elif (div1 == 2 and div3 == 2):
        order1 = tiebreak2(sortList[0], sortList[1])
        order2 = tiebreak2(sortList[2], sortList[3])
        order3 = tiebreak2(sortList[4], sortList[5])
        result1 = tiebreak3(order1[0], order2[0], order3[0])
        if (result1[0] == order1[0]):
            result2 = tiebreak5(order1[1], order2[0], order2[1], order3[0], order3[1])
            result = [order1[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
        elif (result1[0] == order2[0]):
            result2 = tiebreak5(order1[1], order1[0], order2[1], order3[0], order3[1])
            result = [order2[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
        else:
            result2 = tiebreak5(order1[1], order2[0], order2[1], order1[0], order3[1])
            result = [order3[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
            
    else:
        order1 = tiebreak2(sortList[0], sortList[1])
        order2 = tiebreak2(sortList[2], sortList[3])
        result1 = tiebreak4(sortList[4], sortList[5], order1[0], order2[0])
        if (result1[0] == order1[0]):
            result2 = tiebreak5(order1[1], order2[0], order2[1], sortList[4], sortList[5])
            result = [order1[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
        elif (result1[0] == order2[0]):
            result2 = tiebreak5(order1[1], order1[0], order2[1], sortList[4], sortList[5])
            result = [order2[0], result2[0], result2[1], result2[2], result2[3], result2[4]]
        elif (result1[0] == sortList[4]):
            result2 = tiebreak5(order1[1], order2[0], order2[1], order1[0], sortList[5])
            result = [sortList[4], result2[0], result2[1], result2[2], result2[3], result2[4]]
        else:
            result2 = tiebreak5(order1[1], order2[0], order2[1], sortList[4], order1[0])
            result = [sortList[5], result2[0], result2[1], result2[2], result2[3], result2[4]]
            
    
    return (result)
            

def tiebreak7(Team1, Team2, Team3, Team4, Team5, Team6, Team7):
    print ("Starting 7 team tiebreaker between " + Team1.getName() + ", " + Team2.getName() + ", " + Team3.getName() + 
           ", " + Team4.getName() + ", " + Team5.getName() + ", " + Team6.getName() + ", and " + Team7.getName())
    teamList = [Team1, Team2, Team3, Team4, Team5, Team6, Team7]
    
    divCounts = Counter(Team.getDivision() for Team in teamList)
    sortList = sorted(teamList, key=lambda x: (divCounts[x.getDivision()], 
                                               x.getDivision()), reverse=True)
    
    div1 = 2
    div2 = 1
    div3 = 0
    div4 = 0
    
    if (sortList[1].getDivision() == sortList[2].getDivision()):
        if (sortList[2].getDivision() == sortList[3].getDivision()):
            div1 = 4
        else: 
            div1 = 3
    else:
        div2 = 2
        
    if (div1 == 4):
        if (sortList[4].getDivision() == sortList[5].getDivision()):
            if (sortList[5].getDivision() == sortList[6].getDivision()):
                div2 = 3
            else:
                div2 = 2
                div3 = 1
        else: 
            div3 = 1
            div4 = 1
    elif (div1 == 3):
        if (sortList[4].getDivision() == sortList[5].getDivision()):
            div2 = 3
            div3 = 1
        else: 
            div2 = 2
            if (sortList[5].getDivision() == sortList[6].getDivision()):
                div3 = 2
            else:
                div3 = 1
                div4 = 1
    else: 
        div2 = 2
        div3 = 2
        div4 = 1
        
    if (div1 == 4 and div2 == 3):
        order1 = tiebreak4 (sortList[0], sortList[1], sortList[2], sortList[3])
        order2 = tiebreak3 (sortList[4], sortList[5], sortList[6])
        first = tiebreak2 (order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak6 (order1[1], order1[2], order1[3], order2[0], order2[1], order2[2])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        else: 
            second = tiebreak6 (order1[1], order1[2], order1[3], order1[0], order2[1], order2[2])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
    
    elif (div1 == 4 and div2 == 2):
        order1 = tiebreak4 (sortList[0], sortList[1], sortList[2], sortList[3])
        order2 = tiebreak2 (sortList[4], sortList[5])
        first = tiebreak3 (order1[0], order2[0], sortList[6])
        if (first[0] == order1[0]):
            second = tiebreak6 (order1[1], order1[2], order1[3], order2[0], order2[1], sortList[6])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        elif (first[0] == order2[0]): 
            second = tiebreak6 (order1[1], order1[2], order1[3], order1[0], order2[1], sortList[6])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        else: 
            second = tiebreak6 (order1[1], order1[2], order1[3], order1[0], order2[1], order2[0])
            result = [sortList[6], second[0], second[1], second[2], second[3], second[4], second[5]]
        
    elif (div1 == 4 and div2 == 1):
        order = tiebreak4 (sortList[0], sortList[1], sortList[2], sortList[3])
        first = tiebreak4 (order[0], sortList[4], sortList[5], sortList[6])
        if (first[0] == order1[0]):
            second = tiebreak6 (order[1], order[2], order[3], first[2], first[1], first[3])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        elif (first[0] == sortList[4]): 
            second = tiebreak6 (order[1], order[2], order[3], first[2], first[1], first[3])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        elif (first[0] == sortList[5]): 
            second = tiebreak6 (order[1], order[2], order[3], first[2], first[1], first[3])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        else: 
            second = tiebreak6 (order[1], order[2], order[3], first[2], first[1], first[3])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        
    elif (div1 == 3 and div2 == 3):
        order1 = tiebreak3 (sortList[0], sortList[1], sortList[2])
        order2 = tiebreak3 (sortList[3], sortList[4], sortList[5])
        first = tiebreak3 (order1[0], order2[0], sortList[6])
        if (first[0] == order1[0]):
            second = tiebreak6 (order1[1], order1[2], order2[2], order2[0], order2[1], sortList[6])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        elif (first[0] == order2[0]): 
            second = tiebreak6 (order1[1], order1[2], order2[2], order1[0], order2[1], sortList[6])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        else: 
            second = tiebreak6 (order1[1], order1[2], order2[2], order1[0], order2[1], order2[0])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        
    elif (div1 == 3 and div2 == 2 and div3 == 2):
        order1 = tiebreak3 (sortList[0], sortList[1], sortList[2])
        order2 = tiebreak2 (sortList[4], sortList[3])
        order3 = tiebreak2 (sortList[5], sortList[6])
        first = tiebreak3 (order1[0], order2[0], order3[0])
        if (first[0] == order1[0]):
            second = tiebreak6 (order1[1], order1[2], order3[0], order2[0], order2[1], order3[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        elif (first[0] == order2[0]): 
            second = tiebreak6 (order1[1], order1[2], order3[0], order1[0], order2[1], order3[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        else: 
            second = tiebreak6 (order1[1], order1[2], order3[1], order1[0], order2[1], order2[0])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        
    elif (div1 == 3 and div2 == 2 and div3 == 1):
        order1 = tiebreak3 (sortList[0], sortList[1], sortList[2])
        order2 = tiebreak2 (sortList[4], sortList[3])
        first = tiebreak4 (order1[0], order2[0], sortList[5], sortList[6])
        if (first[0] == order1[0]):
            second = tiebreak6 (order1[1], order1[2], order2[0], order2[1], sortList[5], sortList[6])
            result = [order1[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        elif (first[0] == order2[0]):
            second = tiebreak6 (order1[1], order1[2], order1[0], order2[1], sortList[5], sortList[6])
            result = [order2[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        elif (first[0] == sortList[5]):
            second = tiebreak6 (order1[1], order1[2], order1[0], order2[1], order2[0], sortList[6])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        else:
            second = tiebreak6 (order1[1], order1[2], order1[0], order2[1], order2[0], sortList[5])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        
    elif (div1 == 2):
        order1 = tiebreak2 (sortList[0], sortList[1])
        order2 = tiebreak2 (sortList[2], sortList[3])
        order3 = tiebreak2 (sortList[4], sortList[5])
        first = tiebreak4 (order1[0], order2[0], order3[0], sortList[6])
        if (first[0] == order1[0]):
            second = tiebreak6 (order1[1], order2[0], order2[1], order3[0], order3[1], sortList[6])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        elif (first[0] == order2[0]):
            second = tiebreak6 (order1[1], order1[0], order2[1], order3[0], order3[1], sortList[6])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        elif (first[0] == order3[0]):
            second = tiebreak6 (order1[1], order2[0], order2[1], order1[0], order3[1], sortList[6])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        else:
            second = tiebreak6 (order1[1], order2[0], order2[1], order3[0], order3[1], order1[0])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5]]
        
    else:
        print ("Tiebreak7 not working")
        
    return (result)
    
    

def tiebreak8(Team1, Team2, Team3, Team4, Team5, Team6, Team7, Team8):
    print ("Starting 8 team tiebreaker between " + Team1.getName() + ", " + Team2.getName() + ", " + Team3.getName() + 
           ", " + Team4.getName() + ", " + Team5.getName() + ", " + Team6.getName() + ", " +
           Team7.getName() + ", and " + Team8.getName())
    teamList = [Team1, Team2, Team3, Team4, Team5, Team6, Team7, Team8]
    
    divCounts = Counter(Team.getDivision() for Team in teamList)
    sortList = sorted(teamList, key=lambda x: (divCounts[x.getDivision()], 
                                               x.getDivision()), reverse=True)
    
    div1 = 2
    div2 = 2
    div3 = 0
    div4 = 0
    
    if (sortList[1].getDivision() == sortList[2].getDivision()):
        if (sortList[2].getDivision() == sortList[3].getDivision()):
            div1 = 4
        else: 
            div1 = 3
    else:
        div1 = 2
        
    if (div1 == 4):
        if (sortList[4].getDivision() == sortList[5].getDivision()):
            if (sortList[5].getDivision() == sortList[6].getDivision()):
                if (sortList[6].getDivision() == sortList[7].getDivision()):
                    div2 = 4
                else:
                    div2 = 3
                    div3 = 1
            else:
                if (sortList[6].getDivision() == sortList[7].getDivision()):
                    div3 = 2
                else:
                    div3 = 1
                    div4 = 1
        else: 
            if (sortList[6].getDivision() == sortList[7].getDivision()):
                div3 = 2
            else: 
                div3 = 1
                div4 = 1
    elif (div1 == 3):
        if (sortList[4].getDivision() == sortList[5].getDivision()):
            div2 = 3
            if (sortList[6].getDivision() == sortList[7].getDivision()):
                div3 = 2
            else:
                div3 = 1
                div4 = 1
        else: 
            div3 = 2
            div4 = 1
    else: 
        div3 = 2
        div4 = 2
        
    if (div1 == 4 and div2 == 4):
        order1 = tiebreak4(sortList[0], sortList[1], sortList[2], sortList[3]) 
        order2 = tiebreak4(sortList[4], sortList[5], sortList[6],  sortList[7])
        first = tiebreak2(order1[0], order2[0])
        if (first[0] == order1[0]):
            second = tiebreak7(order1[1], order1[2], order1[3], order2[0], order2[1], order2[2], order2[3])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        else:
            second = tiebreak7(order1[1], order1[2], order1[3], order1[0], order2[1], order2[2], order2[3])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
    
    elif (div1 == 4 and div2 == 3):
        order1 = tiebreak4(sortList[0], sortList[1], sortList[2], sortList[3]) 
        order2 = tiebreak3(sortList[4], sortList[5], sortList[6])
        first = tiebreak3(order1[0], order2[0], sortList[7])
        if (first[0] == order1[0]):
            second = tiebreak7(order1[1], order1[2], order1[3], order2[0], order2[1], order2[2], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == order2[0]):
            second = tiebreak7(order1[1], order1[2], order1[3], order1[0], order2[1], order2[2], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        else: 
            second = tiebreak7(order1[1], order1[2], order1[3], order1[0], order2[1], order2[2], order2[0])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        
    elif (div1 == 4 and div2 == 2 and div3 == 2):
        order1 = tiebreak4(sortList[0], sortList[1], sortList[2], sortList[3]) 
        order2 = tiebreak2(sortList[4], sortList[5]) 
        order3 = tiebreak2(sortList[6],  sortList[7])
        first = tiebreak3(order1[0], order2[0], order3[0])
        if (first[0] == order1[0]):
            second = tiebreak7(order1[1], order1[2], order1[3], order2[0], order2[1], order3[0], order3[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == order2[0]):
            second = tiebreak7(order1[1], order1[2], order1[3], order1[0], order2[1], order3[0], order3[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        else: 
            second = tiebreak7(order1[1], order1[2], order1[3], order1[0], order2[0], order2[1], order3[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        
    elif (div1 == 4 and div2 == 2 and div3 == 1):
        order1 = tiebreak4(sortList[0], sortList[1], sortList[2], sortList[3]) 
        order2 = tiebreak2(sortList[4], sortList[5])
        first = tiebreak4(order1[0], order2[0], sortList[6], sortList[7])
        if (first[0] == order1[0]):
            second = tiebreak7(order1[1], order1[2], order1[3], order2[0], order2[1], sortList[6], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == order2[0]):
            second = tiebreak7(order1[1], order1[2], order1[3], order1[0], order2[1], sortList[6], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == sortList[6]): 
            second = tiebreak7(order1[1], order1[2], order1[3], order1[0], order2[0], order2[1], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        else: 
            second = tiebreak7(order1[1], order1[2], order1[3], order1[0], order2[0], order2[1], sortList[6])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
            
        
    elif (div1 == 3 and div2 == 3 and div3 == 2):
        order1 = tiebreak3(sortList[0], sortList[1], sortList[2]) 
        order2 = tiebreak3(sortList[3], sortList[4], sortList[5]) 
        order3 = tiebreak2(sortList[6],  sortList[7])
        first = tiebreak3(order1[0], order2[0], order3[0])
        if (first[0] == order1[0]):
            second = tiebreak7(order1[1], order1[2], order2[2], order2[0], order2[1], order3[0], order3[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == order2[0]):
            second = tiebreak7(order1[1], order1[2], order2[2], order1[0], order2[1], order3[0], order3[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        else: 
            second = tiebreak7(order1[1], order1[2], order2[2], order1[0], order2[0], order2[1], order3[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        
    elif (div1 == 3 and div2 == 3 and div3 == 1):
        order1 = tiebreak3(sortList[0], sortList[1], sortList[2]) 
        order2 = tiebreak3(sortList[3], sortList[4], sortList[5]) 
        first = tiebreak4(order1[0], order2[0], sortList[6], sortList[7])
        if (first[0] == order1[0]):
            second = tiebreak7(order1[1], order1[2], order2[2], order2[0], order2[1], sortList[6], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == order2[0]):
            second = tiebreak7(order1[1], order1[2], order2[2], order1[0], order2[1], sortList[6], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == sortList[6]): 
            second = tiebreak7(order1[1], order1[2], order2[2], order1[0], order2[0], order2[1], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        else: 
            second = tiebreak7(order1[1], order1[2], order2[2], order1[0], order2[0], order2[1], sortList[6])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        
    elif (div1 == 3 and div2 == 2):
        order1 = tiebreak3(sortList[0], sortList[1], sortList[2]) 
        order2 = tiebreak2(sortList[3], sortList[4]) 
        order3 = tiebreak2(sortList[5], sortList[6])
        first = tiebreak4(order1[0], order2[0], order3[0], sortList[7])
        if (first[0] == order1[0]):
            second = tiebreak7(order1[1], order1[2], order3[0], order2[0], order2[1], order3[1], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == order2[0]):
            second = tiebreak7(order1[1], order1[2], order3[0], order1[0], order2[1], order3[1], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == order3[0]): 
            second = tiebreak7(order1[1], order1[2], order3[1], order1[0], order2[0], order2[1], sortList[7])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        else: 
            second = tiebreak7(order1[1], order1[2], order3[0], order1[0], order2[0], order2[1], order3[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        
    else:
        order1 = tiebreak3(sortList[0], sortList[1]) 
        order2 = tiebreak2(sortList[2], sortList[3]) 
        order3 = tiebreak2(sortList[4], sortList[5])
        order4 = tiebreak2(sortList[6], sortList[7])
        first = tiebreak4(order1[0], order2[0], order3[0], order4[0])
        if (first[0] == order1[0]):
            second = tiebreak7(order1[1], order4[0], order3[0], order2[0], order2[1], order3[1], order4[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == order2[0]):
            second = tiebreak7(order1[1], order4[0], order3[0], order1[0], order2[1], order3[1], order4[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        elif (first[0] == order3[0]): 
            second = tiebreak7(order1[1], order4[0], order3[1], order1[0], order2[0], order2[1], order4[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
        else: 
            second = tiebreak7(order1[1], order4[1], order3[0], order1[0], order2[0], order2[1], order3[1])
            result = [first[0], second[0], second[1], second[2], second[3], second[4], second[5], second[6]]
            
    return (result)
        



def divisionStandings():
    AFCE_Standings = []
    AFCN_Standings = []
    AFCS_Standings = []
    AFCW_Standings = []
    NFCE_Standings = []
    NFCN_Standings = []
    NFCS_Standings = []
    NFCW_Standings = []

    #print("AFCE:")
    AFCE_Standings = [Bills, Dolphins, Jets, Patriots]
    AFCE_Standings.sort(key=lambda team: team.getWinPercentage(), reverse=True)
    first_afce = AFCE_Standings[0]
    second_afce = AFCE_Standings[1]
    third_afce = AFCE_Standings[2]
    fourth_afce = AFCE_Standings[3]

    # all 4 division teams tied
    if (first_afce.getWinPercentage() == second_afce.getWinPercentage() and
            first_afce.getWinPercentage() == third_afce.getWinPercentage() and
            first_afce.getWinPercentage() == fourth_afce.getWinPercentage()):
        result = tiebreak4(first_afce, second_afce, third_afce, fourth_afce)
        AFCE_Standings = [result[0], result[1], result[2], result[3]]

    # 3 division teams tied
    elif (first_afce.getWinPercentage() == second_afce.getWinPercentage() and
          first_afce.getWinPercentage() == third_afce.getWinPercentage()):
        result = tiebreak3(first_afce, second_afce, third_afce)
        AFCE_Standings[0] = result[0]
        AFCE_Standings[1] = result[1]
        AFCE_Standings[2] = result[2]

    elif (fourth_afce.getWinPercentage() == second_afce.getWinPercentage() and
          fourth_afce.getWinPercentage() == third_afce.getWinPercentage()):
        result = tiebreak3(fourth_afce, second_afce, third_afce)
        AFCE_Standings[3] = result[2]
        AFCE_Standings[1] = result[0]
        AFCE_Standings[2] = result[1]

    # 2 division teams tied (will need to add rest, this is just top 2)
    elif (first_afce.getWinPercentage() == second_afce.getWinPercentage()):
        result = tiebreak2(first_afce, second_afce)
        AFCE_Standings[0] = result[0]
        AFCE_Standings[1] = result[1]

    elif (third_afce.getWinPercentage() == second_afce.getWinPercentage()):
        result = tiebreak2(third_afce, second_afce)
        AFCE_Standings[1] = result[0]
        AFCE_Standings[2] = result[1]

    elif (third_afce.getWinPercentage() == fourth_afce.getWinPercentage()):
        result = tiebreak2(third_afce, fourth_afce)
        AFCE_Standings[2] = result[0]
        AFCE_Standings[3] = result[1]

    '''
    print (AFCE_Standings[0].getName() + ": " + str(AFCE_Standings[0].getWins()) + "-" + str(AFCE_Standings[0].getLosses()))
    print (AFCE_Standings[1].getName() + ": " + str(AFCE_Standings[1].getWins()) + "-" + str(AFCE_Standings[1].getLosses()))
    print (AFCE_Standings[2].getName() + ": " + str(AFCE_Standings[2].getWins()) + "-" + str(AFCE_Standings[2].getLosses()))
    print (AFCE_Standings[3].getName() + ": " + str(AFCE_Standings[3].getWins()) + "-" + str(AFCE_Standings[3].getLosses()) + "\n")
    '''
    #print("AFCN:")
    AFCN_Standings = [Bengals, Browns, Ravens, Steelers]
    AFCN_Standings.sort(key=lambda team: team.getWinPercentage(), reverse=True)
    first_afcn = AFCN_Standings[0]
    second_afcn = AFCN_Standings[1]
    third_afcn = AFCN_Standings[2]
    fourth_afcn = AFCN_Standings[3]

    # all 4 division teams tied
    if (first_afcn.getWinPercentage() == second_afcn.getWinPercentage() and
            first_afcn.getWinPercentage() == third_afcn.getWinPercentage() and
            first_afcn.getWinPercentage() == fourth_afcn.getWinPercentage()):
        result = tiebreak4(first_afcn, second_afcn, third_afcn, fourth_afcn)
        AFCN_Standings = [result[0], result[1], result[2], result[3]]

    # 3 division teams tied
    elif (first_afcn.getWinPercentage() == second_afcn.getWinPercentage() and
          first_afcn.getWinPercentage() == third_afcn.getWinPercentage()):
        result = tiebreak3(first_afcn, second_afcn, third_afcn)
        AFCN_Standings[0] = result[0]
        AFCN_Standings[1] = result[1]
        AFCN_Standings[2] = result[2]

    elif (fourth_afcn.getWinPercentage() == second_afcn.getWinPercentage() and
          fourth_afcn.getWinPercentage() == third_afcn.getWinPercentage()):
        result = tiebreak3(fourth_afcn, second_afcn, third_afcn)
        AFCN_Standings[3] = result[2]
        AFCN_Standings[1] = result[0]
        AFCN_Standings[2] = result[1]

    # 2 division teams tied (will need to add rest, this is just top 2)
    elif (first_afcn.getWinPercentage() == second_afcn.getWinPercentage()):
        result = tiebreak2(first_afcn, second_afcn)
        AFCN_Standings[0] = result[0]
        AFCN_Standings[1] = result[1]

    elif (third_afcn.getWinPercentage() == second_afcn.getWinPercentage()):
        result = tiebreak2(third_afcn, second_afcn)
        AFCN_Standings[1] = result[0]
        AFCN_Standings[2] = result[1]

    elif (third_afcn.getWinPercentage() == fourth_afcn.getWinPercentage()):
        result = tiebreak2(third_afcn, fourth_afcn)
        AFCN_Standings[2] = result[0]
        AFCN_Standings[3] = result[1]

    '''
    print (AFCN_Standings[0].getName() + ": " + str(AFCN_Standings[0].getWins()) + "-" + str(AFCN_Standings[0].getLosses()))
    print (AFCN_Standings[1].getName() + ": " + str(AFCN_Standings[1].getWins()) + "-" + str(AFCN_Standings[1].getLosses()))
    print (AFCN_Standings[2].getName() + ": " + str(AFCN_Standings[2].getWins()) + "-" + str(AFCN_Standings[2].getLosses()))
    print (AFCN_Standings[3].getName() + ": " + str(AFCN_Standings[3].getWins()) + "-" + str(AFCN_Standings[3].getLosses()) + "\n")
    '''
    #print("AFCS:")
    AFCS_Standings = [Colts, Jaguars, Titans, Texans]
    AFCS_Standings.sort(key=lambda team: team.getWinPercentage(), reverse=True)
    first_afcs = AFCS_Standings[0]
    second_afcs = AFCS_Standings[1]
    third_afcs = AFCS_Standings[2]
    fourth_afcs = AFCS_Standings[3]

    # all 4 division teams tied
    if (first_afcs.getWinPercentage() == second_afcs.getWinPercentage() and
            first_afcs.getWinPercentage() == third_afcs.getWinPercentage() and
            first_afcs.getWinPercentage() == fourth_afcs.getWinPercentage()):
        result = tiebreak4(first_afcs, second_afcs, third_afcs, fourth_afcs)
        AFCS_Standings = [result[0], result[1], result[2], result[3]]

    # 3 division teams tied
    elif (first_afcs.getWinPercentage() == second_afcs.getWinPercentage() and
          first_afcs.getWinPercentage() == third_afcs.getWinPercentage()):
        result = tiebreak3(first_afcs, second_afcs, third_afcs)
        AFCS_Standings[0] = result[0]
        AFCS_Standings[1] = result[1]
        AFCS_Standings[2] = result[2]

    elif (fourth_afcs.getWinPercentage() == second_afcs.getWinPercentage() and
          fourth_afcs.getWinPercentage() == third_afcs.getWinPercentage()):
        result = tiebreak3(fourth_afcs, second_afcs, third_afcs)
        AFCS_Standings[3] = result[2]
        AFCS_Standings[1] = result[0]
        AFCS_Standings[2] = result[1]

    # 2 division teams tied (will need to add rest, this is just top 2)
    elif (first_afcs.getWinPercentage() == second_afcs.getWinPercentage()):
        result = tiebreak2(first_afcs, second_afcs)
        AFCS_Standings[0] = result[0]
        AFCS_Standings[1] = result[1]

    elif (third_afcs.getWinPercentage() == second_afcs.getWinPercentage()):
        result = tiebreak2(third_afcs, second_afcs)
        AFCS_Standings[1] = result[0]
        AFCS_Standings[2] = result[1]

    elif (third_afcs.getWinPercentage() == fourth_afcs.getWinPercentage()):
        result = tiebreak2(third_afcs, fourth_afcs)
        AFCS_Standings[2] = result[0]
        AFCS_Standings[3] = result[1]

    '''
    print (AFCS_Standings[0].getName() + ": " + str(AFCS_Standings[0].getWins()) + "-" + str(AFCS_Standings[0].getLosses()))
    print (AFCS_Standings[1].getName() + ": " + str(AFCS_Standings[1].getWins()) + "-" + str(AFCS_Standings[1].getLosses()))
    print (AFCS_Standings[2].getName() + ": " + str(AFCS_Standings[2].getWins()) + "-" + str(AFCS_Standings[2].getLosses()))
    print (AFCS_Standings[3].getName() + ": " + str(AFCS_Standings[3].getWins()) + "-" + str(AFCS_Standings[3].getLosses()) + "\n")
    '''
    #print("AFCW:")
    AFCW_Standings = [Broncos, Chargers, Chiefs, Raiders]
    AFCW_Standings.sort(key=lambda team: team.getWinPercentage(), reverse=True)
    first_afcw = AFCW_Standings[0]
    second_afcw = AFCW_Standings[1]
    third_afcw = AFCW_Standings[2]
    fourth_afcw = AFCW_Standings[3]

    # all 4 division teams tied
    if (first_afcw.getWinPercentage() == second_afcw.getWinPercentage() and
            first_afcw.getWinPercentage() == third_afcw.getWinPercentage() and
            first_afcw.getWinPercentage() == fourth_afcw.getWinPercentage()):
        result = tiebreak4(first_afcw, second_afcw, third_afcw, fourth_afcw)
        AFCW_Standings = [result[0], result[1], result[2], result[3]]

    # 3 division teams tied
    elif (first_afcw.getWinPercentage() == second_afcw.getWinPercentage() and
          first_afcw.getWinPercentage() == third_afcw.getWinPercentage()):
        result = tiebreak3(first_afcw, second_afcw, third_afcw)
        AFCW_Standings[0] = result[0]
        AFCW_Standings[1] = result[1]
        AFCW_Standings[2] = result[2]

    elif (fourth_afcw.getWinPercentage() == second_afcw.getWinPercentage() and
          fourth_afcw.getWinPercentage() == third_afcw.getWinPercentage()):
        result = tiebreak3(fourth_afcw, second_afcw, third_afcw)
        AFCW_Standings[3] = result[2]
        AFCW_Standings[1] = result[0]
        AFCW_Standings[2] = result[1]

    # 2 division teams tied (will need to add rest, this is just top 2)
    elif (first_afcw.getWinPercentage() == second_afcw.getWinPercentage()):
        result = tiebreak2(first_afcw, second_afcw)
        AFCW_Standings[0] = result[0]
        AFCW_Standings[1] = result[1]

    elif (third_afcw.getWinPercentage() == second_afcw.getWinPercentage()):
        result = tiebreak2(third_afcw, second_afcw)
        AFCW_Standings[1] = result[0]
        AFCW_Standings[2] = result[1]

    elif (third_afcw.getWinPercentage() == fourth_afcw.getWinPercentage()):
        result = tiebreak2(third_afcw, fourth_afcw)
        AFCW_Standings[2] = result[0]
        AFCW_Standings[3] = result[1]

    '''
    print (AFCW_Standings[0].getName() + ": " + str(AFCW_Standings[0].getWins()) + "-" + str(AFCW_Standings[0].getLosses()))
    print (AFCW_Standings[1].getName() + ": " + str(AFCW_Standings[1].getWins()) + "-" + str(AFCW_Standings[1].getLosses()))
    print (AFCW_Standings[2].getName() + ": " + str(AFCW_Standings[2].getWins()) + "-" + str(AFCW_Standings[2].getLosses()))
    print (AFCW_Standings[3].getName() + ": " + str(AFCW_Standings[3].getWins()) + "-" + str(AFCW_Standings[3].getLosses()) + "\n")
    '''
    #print("NFCE:")
    NFCE_Standings = [Commanders, Cowboys, Giants, Eagles]
    NFCE_Standings.sort(key=lambda team: team.getWinPercentage(), reverse=True)
    first_nfce = NFCE_Standings[0]
    second_nfce = NFCE_Standings[1]
    third_nfce = NFCE_Standings[2]
    fourth_nfce = NFCE_Standings[3]

    # all 4 division teams tied
    if (first_nfce.getWinPercentage() == second_nfce.getWinPercentage() and
            first_nfce.getWinPercentage() == third_nfce.getWinPercentage() and
            first_nfce.getWinPercentage() == fourth_nfce.getWinPercentage()):
        result = tiebreak4(first_nfce, second_nfce, third_nfce, fourth_nfce)
        NFCE_Standings = [result[0], result[1], result[2], result[3]]

    # 3 division teams tied
    elif (first_nfce.getWinPercentage() == second_nfce.getWinPercentage() and
          first_nfce.getWinPercentage() == third_nfce.getWinPercentage()):
        result = tiebreak3(first_nfce, second_nfce, third_nfce)
        NFCE_Standings[0] = result[0]
        NFCE_Standings[1] = result[1]
        NFCE_Standings[2] = result[2]

    elif (fourth_nfce.getWinPercentage() == second_nfce.getWinPercentage() and
          fourth_nfce.getWinPercentage() == third_nfce.getWinPercentage()):
        result = tiebreak3(fourth_nfce, second_nfce, third_nfce)
        NFCE_Standings[3] = result[2]
        NFCE_Standings[1] = result[0]
        NFCE_Standings[2] = result[1]

    # 2 division teams tied (will need to add rest, this is just top 2)
    elif (first_nfce.getWinPercentage() == second_nfce.getWinPercentage()):
        result = tiebreak2(first_nfce, second_nfce)
        NFCE_Standings[0] = result[0]
        NFCE_Standings[1] = result[1]

    elif (third_nfce.getWinPercentage() == second_nfce.getWinPercentage()):
        result = tiebreak2(third_nfce, second_nfce)
        NFCE_Standings[1] = result[0]
        NFCE_Standings[2] = result[1]

    elif (third_nfce.getWinPercentage() == fourth_nfce.getWinPercentage()):
        result = tiebreak2(third_nfce, fourth_nfce)
        NFCE_Standings[2] = result[0]
        NFCE_Standings[3] = result[1]

    '''
    print (NFCE_Standings[0].getName() + ": " + str(NFCE_Standings[0].getWins()) + "-" + str(NFCE_Standings[0].getLosses()))
    print (NFCE_Standings[1].getName() + ": " + str(NFCE_Standings[1].getWins()) + "-" + str(NFCE_Standings[1].getLosses()))
    print (NFCE_Standings[2].getName() + ": " + str(NFCE_Standings[2].getWins()) + "-" + str(NFCE_Standings[2].getLosses()))
    print (NFCE_Standings[3].getName() + ": " + str(NFCE_Standings[3].getWins()) + "-" + str(NFCE_Standings[3].getLosses()) + "\n")
    '''
    #print("NFCN:")
    NFCN_Standings = [Bears, Lions, Packers, Vikings]
    NFCN_Standings.sort(key=lambda team: team.getWinPercentage(), reverse=True)
    first_nfcn = NFCN_Standings[0]
    second_nfcn = NFCN_Standings[1]
    third_nfcn = NFCN_Standings[2]
    fourth_nfcn = NFCN_Standings[3]

    # all 4 division teams tied
    if (first_nfcn.getWinPercentage() == second_nfcn.getWinPercentage() and
            first_nfcn.getWinPercentage() == third_nfcn.getWinPercentage() and
            first_nfcn.getWinPercentage() == fourth_nfcn.getWinPercentage()):
        result = tiebreak4(first_nfcn, second_nfcn, third_nfcn, fourth_nfcn)
        NFCN_Standings = [result[0], result[1], result[2], result[3]]

    # 3 division teams tied
    elif (first_nfcn.getWinPercentage() == second_nfcn.getWinPercentage() and
          first_nfcn.getWinPercentage() == third_nfcn.getWinPercentage()):
        result = tiebreak3(first_nfcn, second_nfcn, third_nfcn)
        NFCN_Standings[0] = result[0]
        NFCN_Standings[1] = result[1]
        NFCN_Standings[2] = result[2]

    elif (fourth_nfcn.getWinPercentage() == second_nfcn.getWinPercentage() and
          fourth_nfcn.getWinPercentage() == third_nfcn.getWinPercentage()):
        result = tiebreak3(fourth_nfcn, second_nfcn, third_nfcn)
        NFCN_Standings[3] = result[2]
        NFCN_Standings[1] = result[0]
        NFCN_Standings[2] = result[1]

    # 2 division teams tied (will need to add rest, this is just top 2)
    elif (first_nfcn.getWinPercentage() == second_nfcn.getWinPercentage()):
        result = tiebreak2(first_nfcn, second_nfcn)
        NFCN_Standings[0] = result[0]
        NFCN_Standings[1] = result[1]

    elif (third_nfcn.getWinPercentage() == second_nfcn.getWinPercentage()):
        result = tiebreak2(third_nfcn, second_nfcn)
        NFCN_Standings[1] = result[0]
        NFCN_Standings[2] = result[1]

    elif (third_nfcn.getWinPercentage() == fourth_nfcn.getWinPercentage()):
        result = tiebreak2(third_nfcn, fourth_nfcn)
        NFCN_Standings[2] = result[0]
        NFCN_Standings[3] = result[1]

    '''
    print (NFCN_Standings[0].getName() + ": " + str(NFCN_Standings[0].getWins()) + "-" + str(NFCN_Standings[0].getLosses()))
    print (NFCN_Standings[1].getName() + ": " + str(NFCN_Standings[1].getWins()) + "-" + str(NFCN_Standings[1].getLosses()))
    print (NFCN_Standings[2].getName() + ": " + str(NFCN_Standings[2].getWins()) + "-" + str(NFCN_Standings[2].getLosses()))
    print (NFCN_Standings[3].getName() + ": " + str(NFCN_Standings[3].getWins()) + "-" + str(NFCN_Standings[3].getLosses()) + "\n")
    '''
    #print("NFCS:")
    NFCS_Standings = [Buccaneers, Falcons, Panthers, Saints]
    NFCS_Standings.sort(key=lambda team: team.getWinPercentage(), reverse=True)
    first_nfcs = NFCS_Standings[0]
    second_nfcs = NFCS_Standings[1]
    third_nfcs = NFCS_Standings[2]
    fourth_nfcs = NFCS_Standings[3]

    # all 4 division teams tied
    if (first_nfcs.getWinPercentage() == second_nfcs.getWinPercentage() and
            first_nfcs.getWinPercentage() == third_nfcs.getWinPercentage() and
            first_nfcs.getWinPercentage() == fourth_nfcs.getWinPercentage()):
        result = tiebreak4(first_nfcs, second_nfcs, third_nfcs, fourth_nfcs)
        NFCS_Standings = [result[0], result[1], result[2], result[3]]

    # 3 division teams tied
    elif (first_nfcs.getWinPercentage() == second_nfcs.getWinPercentage() and
          first_nfcs.getWinPercentage() == third_nfcs.getWinPercentage()):
        result = tiebreak3(first_nfcs, second_nfcs, third_nfcs)
        NFCS_Standings[0] = result[0]
        NFCS_Standings[1] = result[1]
        NFCS_Standings[2] = result[2]

    elif (fourth_nfcs.getWinPercentage() == second_nfcs.getWinPercentage() and
          fourth_nfcs.getWinPercentage() == third_nfcs.getWinPercentage()):
        result = tiebreak3(fourth_nfcs, second_nfcs, third_nfcs)
        NFCS_Standings[3] = result[2]
        NFCS_Standings[1] = result[0]
        NFCS_Standings[2] = result[1]

    # 2 division teams tied (will need to add rest, this is just top 2)
    elif (first_nfcs.getWinPercentage() == second_nfcs.getWinPercentage()):
        result = tiebreak2(first_nfcs, second_nfcs)
        NFCS_Standings[0] = result[0]
        NFCS_Standings[1] = result[1]

    elif (third_nfcs.getWinPercentage() == second_nfcs.getWinPercentage()):
        result = tiebreak2(third_nfcs, second_nfcs)
        NFCS_Standings[1] = result[0]
        NFCS_Standings[2] = result[1]

    elif (third_nfcs.getWinPercentage() == fourth_nfcs.getWinPercentage()):
        result = tiebreak2(third_nfcs, fourth_nfcs)
        NFCS_Standings[2] = result[0]
        NFCS_Standings[3] = result[1]

    '''
    print (NFCS_Standings[0].getName() + ": " + str(NFCS_Standings[0].getWins()) + "-" + str(NFCS_Standings[0].getLosses()))
    print (NFCS_Standings[1].getName() + ": " + str(NFCS_Standings[1].getWins()) + "-" + str(NFCS_Standings[1].getLosses()))
    print (NFCS_Standings[2].getName() + ": " + str(NFCS_Standings[2].getWins()) + "-" + str(NFCS_Standings[2].getLosses()))
    print (NFCS_Standings[3].getName() + ": " + str(NFCS_Standings[3].getWins()) + "-" + str(NFCS_Standings[3].getLosses()) + "\n")
    '''
    #print("NFCW:")
    NFCW_Standings = [Niners, Cardinals, Rams, Seahawks]
    NFCW_Standings.sort(key=lambda team: team.getWinPercentage(), reverse=True)
    first_nfcw = NFCW_Standings[0]
    second_nfcw = NFCW_Standings[1]
    third_nfcw = NFCW_Standings[2]
    fourth_nfcw = NFCW_Standings[3]

    # all 4 division teams tied
    if (first_nfcw.getWinPercentage() == second_nfcw.getWinPercentage() and
            first_nfcw.getWinPercentage() == third_nfcw.getWinPercentage() and
            first_nfcw.getWinPercentage() == fourth_nfcw.getWinPercentage()):
        result = tiebreak4(first_nfcw, second_nfcw, third_nfcw, fourth_nfcw)
        NFCW_Standings = [result[0], result[1], result[2], result[3]]

    # 3 division teams tied
    elif (first_nfcw.getWinPercentage() == second_nfcw.getWinPercentage() and
          first_nfcw.getWinPercentage() == third_nfcw.getWinPercentage()):
        result = tiebreak3(first_nfcw, second_nfcw, third_nfcw)
        NFCW_Standings[0] = result[0]
        NFCW_Standings[1] = result[1]
        NFCW_Standings[2] = result[2]

    elif (fourth_nfcw.getWinPercentage() == second_nfcw.getWinPercentage() and
          fourth_nfcw.getWinPercentage() == third_nfcw.getWinPercentage()):
        result = tiebreak3(fourth_nfcw, second_nfcw, third_nfcw)
        NFCW_Standings[3] = result[2]
        NFCW_Standings[1] = result[0]
        NFCW_Standings[2] = result[1]

    # 2 division teams tied (will need to add rest, this is just top 2)
    elif (first_nfcw.getWinPercentage() == second_nfcw.getWinPercentage()):
        result = tiebreak2(first_nfcw, second_nfcw)
        NFCW_Standings[0] = result[0]
        NFCW_Standings[1] = result[1]

    elif (third_nfcw.getWinPercentage() == second_nfcw.getWinPercentage()):
        result = tiebreak2(third_nfcw, second_nfcw)
        NFCW_Standings[1] = result[0]
        NFCW_Standings[2] = result[1]

    elif (third_nfcw.getWinPercentage() == fourth_nfcw.getWinPercentage()):
        result = tiebreak2(third_nfcw, fourth_nfcw)
        NFCW_Standings[2] = result[0]
        NFCW_Standings[3] = result[1]

    '''
    print (NFCW_Standings[0].getName() + ": " + str(NFCW_Standings[0].getWins()) + "-" + str(NFCW_Standings[0].getLosses()))
    print (NFCW_Standings[1].getName() + ": " + str(NFCW_Standings[1].getWins()) + "-" + str(NFCW_Standings[1].getLosses()))
    print (NFCW_Standings[2].getName() + ": " + str(NFCW_Standings[2].getWins()) + "-" + str(NFCW_Standings[2].getLosses()))
    print (NFCW_Standings[3].getName() + ": " + str(NFCW_Standings[3].getWins()) + "-" + str(NFCW_Standings[3].getLosses()) + "\n")
    '''
    return ([AFCE_Standings[0], AFCN_Standings[0], AFCS_Standings[0], AFCW_Standings[0], NFCE_Standings[0],
             NFCN_Standings[0], NFCS_Standings[0], NFCW_Standings[0]])


def playoffStandings():
    afcRest = []
    nfcRest = []
    afcWC = []
    nfcWC = []
    divLeaders = divisionStandings()

    afcDivLeaders = [divLeaders[0], divLeaders[1], divLeaders[2], divLeaders[3]]
    nfcDivLeaders = [divLeaders[4], divLeaders[5], divLeaders[6], divLeaders[7]]
    afcDivLeaders.sort(key=lambda team: team.getWinPercentage(), reverse=True)
    nfcDivLeaders.sort(key=lambda team: team.getWinPercentage(), reverse=True)

    aleader1 = afcDivLeaders[0]
    aleader2 = afcDivLeaders[1]
    aleader3 = afcDivLeaders[2]
    aleader4 = afcDivLeaders[3]
    nleader1 = nfcDivLeaders[0]
    nleader2 = nfcDivLeaders[1]
    nleader3 = nfcDivLeaders[2]
    nleader4 = nfcDivLeaders[3]

    # all 4 division leaders tied
    if (aleader1.getWinPercentage() == aleader2.getWinPercentage() and
            aleader1.getWinPercentage() == aleader3.getWinPercentage() and
            aleader1.getWinPercentage() == aleader4.getWinPercentage()):
        result = tiebreak4(aleader1, aleader2, aleader3, aleader4)
        afcDivLeaders = [result[0], result[1], result[2], result[3]]

    # 3 division leaders tied
    elif (aleader1.getWinPercentage() == aleader2.getWinPercentage() and
          aleader1.getWinPercentage() == aleader3.getWinPercentage()):
        result = tiebreak3(aleader1, aleader2, aleader3)
        afcDivLeaders[0] = result[0]
        afcDivLeaders[1] = result[1]
        afcDivLeaders[2] = result[2]

    elif (aleader4.getWinPercentage() == aleader2.getWinPercentage() and
          aleader4.getWinPercentage() == aleader3.getWinPercentage()):
        result = tiebreak3(aleader4, aleader2, aleader3)
        afcDivLeaders[3] = result[2]
        afcDivLeaders[1] = result[0]
        afcDivLeaders[2] = result[1]

    # 2 division leaders tied
    elif (aleader1.getWinPercentage() == aleader2.getWinPercentage()):
        result = tiebreak2(aleader1, aleader2)
        afcDivLeaders[0] = result[0]
        afcDivLeaders[1] = result[1]

    elif (aleader3.getWinPercentage() == aleader2.getWinPercentage()):
        result = tiebreak2(aleader3, aleader2)
        afcDivLeaders[1] = result[0]
        afcDivLeaders[2] = result[1]

    elif (aleader3.getWinPercentage() == aleader4.getWinPercentage()):
        result = tiebreak2(aleader3, aleader4)
        afcDivLeaders[2] = result[0]
        afcDivLeaders[3] = result[1]

    # 4 division leaders tied
    if (nleader1.getWinPercentage() == nleader2.getWinPercentage() and
            nleader1.getWinPercentage() == nleader3.getWinPercentage() and
            nleader1.getWinPercentage() == nleader4.getWinPercentage()):
        result = tiebreak4(nleader1, nleader2, nleader3, nleader4)
        nfcDivLeaders = [result[0], result[1], result[2], result[3]]

    # 3 division leaders tied
    elif (nleader1.getWinPercentage() == nleader2.getWinPercentage() and
          nleader1.getWinPercentage() == nleader3.getWinPercentage()):
        result = tiebreak3(nleader1, nleader2, nleader3)
        nfcDivLeaders[0] = result[0]
        nfcDivLeaders[1] = result[1]
        nfcDivLeaders[2] = result[2]

    elif (nleader4.getWinPercentage() == nleader2.getWinPercentage() and
          nleader4.getWinPercentage() == nleader3.getWinPercentage()):
        result = tiebreak3(nleader4, nleader2, nleader3)
        nfcDivLeaders[3] = result[2]
        nfcDivLeaders[1] = result[0]
        nfcDivLeaders[2] = result[1]

    # 2 division teams tied 
    elif (nleader1.getWinPercentage() == nleader2.getWinPercentage()):
        result = tiebreak2(nleader1, nleader2)
        nfcDivLeaders[0] = result[0]
        nfcDivLeaders[1] = result[1]

    elif (nleader3.getWinPercentage() == nleader2.getWinPercentage()):
        result = tiebreak2(nleader3, nleader2)
        nfcDivLeaders[1] = result[0]
        nfcDivLeaders[2] = result[1]

    elif (nleader3.getWinPercentage() == nleader4.getWinPercentage()):
        result = tiebreak2(nleader3, nleader4)
        nfcDivLeaders[2] = result[0]
        nfcDivLeaders[3] = result[1]

    for i in range(16):
        if (not AFC[i].getName() == afcDivLeaders[0].getName() and not AFC[i].getName() == afcDivLeaders[
            1].getName() and
                not AFC[i].getName() == afcDivLeaders[2].getName() and not AFC[i].getName() == afcDivLeaders[
                    3].getName()):
            afcRest.append(AFC[i])

    for i in range(16):
        if (not NFC[i].getName() == nfcDivLeaders[0].getName() and not NFC[i].getName() == nfcDivLeaders[
            1].getName() and
                not NFC[i].getName() == nfcDivLeaders[2].getName() and not NFC[i].getName() == nfcDivLeaders[
                    3].getName()):
            nfcRest.append(NFC[i])

    afcRest.sort(key=lambda team: team.getWinPercentage(), reverse=True)
    nfcRest.sort(key=lambda team: team.getWinPercentage(), reverse=True)

    aRest1 = afcRest[0]
    aRest2 = afcRest[1]
    aRest3 = afcRest[2]
    aRest4 = afcRest[3]
    aRest5 = afcRest[4]
    aRest6 = afcRest[5]
    aRest7 = afcRest[6]
    aRest8 = afcRest[7]
    aRest9 = afcRest[8]
    aRest10 = afcRest[9]
    aRest11 = afcRest[10]
    nRest1 = nfcRest[0]
    nRest2 = nfcRest[1]
    nRest3 = nfcRest[2]
    nRest4 = nfcRest[3]
    nRest5 = nfcRest[4]
    nRest6 = nfcRest[5]
    nRest7 = nfcRest[6]
    nRest8 = nfcRest[7]
    nRest9 = nfcRest[8]
    nRest10 = nfcRest[9]
    nRest11 = nfcRest[10]

    afcWC = [aRest1, aRest2, aRest3]
    nfcWC = [nRest1, nRest2, nRest3]
    
    
    #8 teams tied
    if (aRest1.getWinPercentage() == aRest2.getWinPercentage() and
            aRest1.getWinPercentage() == aRest3.getWinPercentage() and
            aRest1.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest1.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest1.getWinPercentage() == aRest6.getWinPercentage() and
            aRest1.getWinPercentage() == aRest7.getWinPercentage() and
            aRest1.getWinPercentage() == aRest8.getWinPercentage() and
            not aRest1.getWinPercentage() == aRest9.getWinPercentage()):
        result = tiebreak8(aRest1, aRest2, aRest3, aRest4, aRest5, aRest6, aRest7, aRest8)
        afcWC = [result[0], result[1], result[2]]
        
    elif (aRest7.getWinPercentage() == aRest2.getWinPercentage() and
            aRest7.getWinPercentage() == aRest3.getWinPercentage() and
            aRest7.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest6.getWinPercentage() and
            aRest7.getWinPercentage() == aRest8.getWinPercentage() and
            aRest7.getWinPercentage() == aRest9.getWinPercentage() and
            not aRest7.getWinPercentage() == aRest10.getWinPercentage()):
        result = tiebreak8(aRest7, aRest2, aRest3, aRest4, aRest5, aRest6, aRest8, aRest9)
        afcWC = [aRest1, result[0], result[1]]
        
    elif (aRest7.getWinPercentage() == aRest8.getWinPercentage() and
            aRest7.getWinPercentage() == aRest3.getWinPercentage() and
            aRest7.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest6.getWinPercentage() and 
            aRest8.getWinPercentage() == aRest9.getWinPercentage() and
            aRest9.getWinPercentage() == aRest10.getWinPercentage() and
            not aRest9.getWinPercentage() == aRest11.getWinPercentage() and
            aRest1.getWinPercentage() == aRest2.getWinPercentage()):
        result1 = tiebreak8(aRest7, aRest8, aRest3, aRest4, aRest5, aRest6, aRest9, aRest10)
        result2 = tiebreak2(aRest1, aRest2)
        afcWC = [result2[0], result2[1], result1[0]]
        
    elif (aRest7.getWinPercentage() == aRest8.getWinPercentage() and
            aRest7.getWinPercentage() == aRest3.getWinPercentage() and
            aRest7.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest6.getWinPercentage() and 
            aRest8.getWinPercentage() == aRest9.getWinPercentage() and
            aRest9.getWinPercentage() == aRest10.getWinPercentage() and
            not aRest9.getWinPercentage() == aRest11.getWinPercentage() and
            not aRest1.getWinPercentage() == aRest2.getWinPercentage()):
        result = tiebreak8(aRest7, aRest8, aRest3, aRest4, aRest5, aRest6, aRest9, aRest10)
        afcWC = [aRest1, aRest2, result[0]]
    
    
    #7 teams tied
    elif (aRest1.getWinPercentage() == aRest2.getWinPercentage() and
            aRest1.getWinPercentage() == aRest3.getWinPercentage() and
            aRest1.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest1.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest1.getWinPercentage() == aRest6.getWinPercentage() and
            aRest1.getWinPercentage() == aRest7.getWinPercentage() and 
            not aRest1.getWinPercentage() == aRest8.getWinPercentage()):
        result = tiebreak7(aRest1, aRest2, aRest3, aRest4, aRest5, aRest6, aRest7)
        afcWC = [result[0], result[1], result[2]]
        
    elif (aRest7.getWinPercentage() == aRest2.getWinPercentage() and
            aRest7.getWinPercentage() == aRest3.getWinPercentage() and
            aRest7.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest6.getWinPercentage() and
            aRest7.getWinPercentage() == aRest8.getWinPercentage() and 
            not aRest7.getWinPercentage() == aRest9.getWinPercentage()):
        result = tiebreak7(aRest7, aRest2, aRest3, aRest4, aRest5, aRest6, aRest8)
        afcWC = [aRest1, result[0], result[1]]
        
    elif (aRest7.getWinPercentage() == aRest8.getWinPercentage() and
            aRest7.getWinPercentage() == aRest3.getWinPercentage() and
            aRest7.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest6.getWinPercentage() and 
            aRest8.getWinPercentage() == aRest9.getWinPercentage() and
            not aRest9.getWinPercentage() == aRest10.getWinPercentage() and
            aRest1.getWinPercentage() == aRest2.getWinPercentage()):
        result1 = tiebreak7(aRest7, aRest8, aRest3, aRest4, aRest5, aRest6, aRest9)
        result2 = tiebreak2(aRest1, aRest2)
        afcWC = [result2[0], result2[1], result1[0]]
        
    elif (aRest7.getWinPercentage() == aRest8.getWinPercentage() and
            aRest7.getWinPercentage() == aRest3.getWinPercentage() and
            aRest7.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest6.getWinPercentage() and 
            aRest8.getWinPercentage() == aRest9.getWinPercentage() and
            not aRest9.getWinPercentage() == aRest10.getWinPercentage() and
            not aRest1.getWinPercentage() == aRest2.getWinPercentage()):
        result = tiebreak7(aRest7, aRest8, aRest3, aRest4, aRest5, aRest6, aRest9)
        afcWC = [aRest1, aRest2, result[0]]
    
    
    #6 teams tied
    elif (aRest1.getWinPercentage() == aRest2.getWinPercentage() and
            aRest1.getWinPercentage() == aRest3.getWinPercentage() and
            aRest1.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest1.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest1.getWinPercentage() == aRest6.getWinPercentage()):
        result = tiebreak6(aRest1, aRest2, aRest3, aRest4, aRest5, aRest6)
        afcWC = [result[0], result[1], result[2]]
        
    elif (aRest7.getWinPercentage() == aRest2.getWinPercentage() and
            aRest7.getWinPercentage() == aRest3.getWinPercentage() and
            aRest7.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest6.getWinPercentage()):
        result = tiebreak6(aRest7, aRest2, aRest3, aRest4, aRest5, aRest6)
        afcWC = [aRest1, result[0], result[1]]
        
    elif (aRest7.getWinPercentage() == aRest8.getWinPercentage() and
            aRest7.getWinPercentage() == aRest3.getWinPercentage() and
            aRest7.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest6.getWinPercentage() and 
            not aRest8.getWinPercentage() == aRest9.getWinPercentage() and
            aRest1.getWinPercentage() == aRest2.getWinPercentage()):
        result1 = tiebreak6(aRest7, aRest8, aRest3, aRest4, aRest5, aRest6)
        result2 = tiebreak2(aRest1, aRest2)
        afcWC = [result2[0], result2[1], result1[0]]
        
    elif (aRest7.getWinPercentage() == aRest8.getWinPercentage() and
            aRest7.getWinPercentage() == aRest3.getWinPercentage() and
            aRest7.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest5.getWinPercentage() and 
            aRest7.getWinPercentage() == aRest6.getWinPercentage() and 
            not aRest1.getWinPercentage() == aRest2.getWinPercentage()):
        result = tiebreak6(aRest7, aRest8, aRest3, aRest4, aRest5, aRest6)
        afcWC = [aRest1, aRest2, result[0]]
    
    
    #5 teams tied
    elif (aRest1.getWinPercentage() == aRest2.getWinPercentage() and
            aRest1.getWinPercentage() == aRest3.getWinPercentage() and
            aRest1.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest1.getWinPercentage() == aRest5.getWinPercentage()):
        result = tiebreak5(aRest1, aRest2, aRest3, aRest4, aRest5)
        afcWC = [result[0], result[1], result[2]]
        
    elif (aRest6.getWinPercentage() == aRest2.getWinPercentage() and
            aRest6.getWinPercentage() == aRest3.getWinPercentage() and
            aRest6.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest6.getWinPercentage() == aRest5.getWinPercentage()):
        result = tiebreak5(aRest6, aRest2, aRest3, aRest4, aRest5)
        afcWC = [aRest1, result[0], result[1]]
        
    elif (aRest6.getWinPercentage() == aRest7.getWinPercentage() and
            aRest6.getWinPercentage() == aRest3.getWinPercentage() and
            aRest6.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest6.getWinPercentage() == aRest5.getWinPercentage() and
            aRest1.getWinPercentage() == aRest2.getWinPercentage()):
        result1 = tiebreak5(aRest6, aRest7, aRest3, aRest4, aRest5)
        result2 = tiebreak2(aRest1, aRest2)
        afcWC = [result2[0], result2[1], result1[0]]
        
    elif (aRest6.getWinPercentage() == aRest7.getWinPercentage() and
            aRest6.getWinPercentage() == aRest3.getWinPercentage() and
            aRest6.getWinPercentage() == aRest4.getWinPercentage() and 
            aRest6.getWinPercentage() == aRest5.getWinPercentage() and
            not aRest1.getWinPercentage() == aRest2.getWinPercentage()):
        result = tiebreak5(aRest6, aRest7, aRest3, aRest4, aRest5)
        afcWC = [aRest1, aRest2, result[0]]
    
    
    # 4 teams tied
    elif (aRest1.getWinPercentage() == aRest2.getWinPercentage() and
            aRest1.getWinPercentage() == aRest3.getWinPercentage() and
            aRest1.getWinPercentage() == aRest4.getWinPercentage()):
        result1 = tiebreak4(aRest1, aRest2, aRest3, aRest4)
        afcWC = [result1[0], result1[1], result1[2]]

    elif (aRest5.getWinPercentage() == aRest2.getWinPercentage() and
          aRest5.getWinPercentage() == aRest3.getWinPercentage() and
          aRest5.getWinPercentage() == aRest4.getWinPercentage()):
        result1 = tiebreak4(aRest5, aRest2, aRest3, aRest4)
        afcWC = [aRest1, result1[0], result1[1]]

    elif (aRest5.getWinPercentage() == aRest6.getWinPercentage() and
          aRest5.getWinPercentage() == aRest3.getWinPercentage() and
          aRest5.getWinPercentage() == aRest4.getWinPercentage() and
          aRest1.getWinPercentage() == aRest2.getWinPercentage()):
        result1 = tiebreak4(aRest5, aRest6, aRest3, aRest4)
        result2 = tiebreak2(aRest1, aRest2)
        afcWC = [result2[0], result2[1], result1[0]]
        
    elif (aRest5.getWinPercentage() == aRest6.getWinPercentage() and
          aRest5.getWinPercentage() == aRest3.getWinPercentage() and
          aRest5.getWinPercentage() == aRest4.getWinPercentage() and
          not aRest1.getWinPercentage() == aRest2.getWinPercentage()):
        result1 = tiebreak4(aRest5, aRest6, aRest3, aRest4)
        afcWC = [aRest1, aRest2, result1[0]]

    # 3 teams tied
    elif (aRest1.getWinPercentage() == aRest2.getWinPercentage() and
          aRest3.getWinPercentage() == aRest1.getWinPercentage()):
        result1 = tiebreak3(aRest1, aRest2, aRest3)
        afcWC = [result1[0], result1[1], result1[2]]

    elif (aRest4.getWinPercentage() == aRest2.getWinPercentage() and
          aRest3.getWinPercentage() == aRest4.getWinPercentage()):
        result1 = tiebreak3(aRest4, aRest2, aRest3)
        afcWC = [aRest1, result1[0], result1[1]]

    elif (aRest3.getWinPercentage() == aRest4.getWinPercentage() and
          aRest3.getWinPercentage == aRest5.getWinPercentage() and 
          aRest1.getWinPercentage == aRest2.getWinPercentage()):
        result1 = tiebreak3(aRest4, aRest5, aRest3)
        result2 = tiebreak2(aRest1, aRest2)
        afcWC = [result2[0], result2[1], result1[0]]

    elif (aRest3.getWinPercentage() == aRest4.getWinPercentage() and
          aRest3.getWinPercentage == aRest5.getWinPercentage() and 
          not aRest1.getWinPercentage == aRest2.getWinPercentage()):
        result1 = tiebreak3(aRest4, aRest5, aRest3)
        afcWC = [aRest1, aRest2, result1[0]]

    # 2 team tiebreakers
    elif (aRest1.getWinPercentage() == aRest2.getWinPercentage() and
          aRest3.getWinPercentage() == aRest4.getWinPercentage() and 
          not aRest1.getWinPercentage() == aRest3.getWinPercentage()):
        result1 = tiebreak2(aRest1, aRest2)
        result2 = tiebreak2(aRest3, aRest4)
        afcWC = [result1[0], result1[1], result2[0]]
        
    elif (not aRest1.getWinPercentage() == aRest2.getWinPercentage() and
          aRest3.getWinPercentage() == aRest4.getWinPercentage() and 
          not aRest2.getWinPercentage() == aRest3.getWinPercentage()):
        result = tiebreak2(aRest3, aRest4)
        afcWC = [aRest1, aRest2, result[0]]
        
    elif (not aRest1.getWinPercentage() == aRest2.getWinPercentage() and
          aRest3.getWinPercentage() == aRest2.getWinPercentage()):
        result = tiebreak2(aRest3, aRest2)
        afcWC = [aRest1, result[0], result[1]]
        
    elif (aRest1.getWinPercentage() == aRest2.getWinPercentage() and
          not aRest3.getWinPercentage() == aRest2.getWinPercentage()):
        result = tiebreak2(aRest1, aRest2)
        afcWC = [result[0], result[1], aRest3]
        
    elif (not aRest1.getWinPercentage() == aRest2.getWinPercentage() and
          not aRest3.getWinPercentage() == aRest2.getWinPercentage()):
        afcWC = [aRest1, aRest2, aRest3]
        
    else:
        print ("9+ team tiebreaker")


    #8 teams tied
    if (nRest1.getWinPercentage() == nRest2.getWinPercentage() and
            nRest1.getWinPercentage() == nRest3.getWinPercentage() and
            nRest1.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest1.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest1.getWinPercentage() == nRest6.getWinPercentage() and
            nRest1.getWinPercentage() == nRest7.getWinPercentage() and
            nRest1.getWinPercentage() == nRest8.getWinPercentage() and
            not nRest1.getWinPercentage() == nRest9.getWinPercentage()):
        result = tiebreak8(nRest1, nRest2, nRest3, nRest4, nRest5, nRest6, nRest7, nRest8)
        nfcWC = [result[0], result[1], result[2]]
        
    elif (nRest7.getWinPercentage() == nRest2.getWinPercentage() and
            nRest7.getWinPercentage() == nRest3.getWinPercentage() and
            nRest7.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest6.getWinPercentage() and
            nRest7.getWinPercentage() == nRest8.getWinPercentage() and
            nRest7.getWinPercentage() == nRest9.getWinPercentage() and
            not nRest7.getWinPercentage() == nRest10.getWinPercentage()):
        result = tiebreak8(nRest7, nRest2, nRest3, nRest4, nRest5, nRest6, nRest8, nRest9)
        nfcWC = [nRest1, result[0], result[1]]
        
    elif (nRest7.getWinPercentage() == nRest8.getWinPercentage() and
            nRest7.getWinPercentage() == nRest3.getWinPercentage() and
            nRest7.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest6.getWinPercentage() and 
            nRest8.getWinPercentage() == nRest9.getWinPercentage() and
            nRest9.getWinPercentage() == nRest10.getWinPercentage() and
            not nRest9.getWinPercentage() == nRest11.getWinPercentage() and
            nRest1.getWinPercentage() == nRest2.getWinPercentage()):
        result1 = tiebreak8(nRest7, nRest8, nRest3, nRest4, nRest5, nRest6, nRest9, nRest10)
        result2 = tiebreak2(nRest1, nRest2)
        nfcWC = [result2[0], result2[1], result1[0]]
        
    elif (nRest7.getWinPercentage() == nRest8.getWinPercentage() and
            nRest7.getWinPercentage() == nRest3.getWinPercentage() and
            nRest7.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest6.getWinPercentage() and 
            nRest8.getWinPercentage() == nRest9.getWinPercentage() and
            nRest9.getWinPercentage() == nRest10.getWinPercentage() and
            not nRest9.getWinPercentage() == nRest11.getWinPercentage() and
            not nRest1.getWinPercentage() == nRest2.getWinPercentage()):
        result = tiebreak8(nRest7, nRest8, nRest3, nRest4, nRest5, nRest6, nRest9, nRest10)
        nfcWC = [nRest1, nRest2, result[0]]


    #7 teams tied
    if (nRest1.getWinPercentage() == nRest2.getWinPercentage() and
            nRest1.getWinPercentage() == nRest3.getWinPercentage() and
            nRest1.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest1.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest1.getWinPercentage() == nRest6.getWinPercentage() and
            nRest1.getWinPercentage() == nRest7.getWinPercentage() and 
            not nRest1.getWinPercentage() == nRest8.getWinPercentage()):
        result = tiebreak7(nRest1, nRest2, nRest3, nRest4, nRest5, nRest6, nRest7)
        nfcWC = [result[0], result[1], result[2]]
        
    elif (nRest7.getWinPercentage() == nRest2.getWinPercentage() and
            nRest7.getWinPercentage() == nRest3.getWinPercentage() and
            nRest7.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest6.getWinPercentage() and
            nRest7.getWinPercentage() == nRest8.getWinPercentage() and 
            not nRest7.getWinPercentage() == nRest9.getWinPercentage()):
        result = tiebreak7(nRest7, nRest2, nRest3, nRest4, nRest5, nRest6, nRest8)
        nfcWC = [nRest1, result[0], result[1]]
        
    elif (nRest7.getWinPercentage() == nRest8.getWinPercentage() and
            nRest7.getWinPercentage() == nRest3.getWinPercentage() and
            nRest7.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest6.getWinPercentage() and 
            nRest8.getWinPercentage() == nRest9.getWinPercentage() and
            not nRest9.getWinPercentage() == nRest10.getWinPercentage() and
            nRest1.getWinPercentage() == nRest2.getWinPercentage()):
        result1 = tiebreak7(nRest7, nRest8, nRest3, nRest4, nRest5, nRest6, nRest9)
        result2 = tiebreak2(nRest1, nRest2)
        nfcWC = [result2[0], result2[1], result1[0]]
        
    elif (nRest7.getWinPercentage() == nRest8.getWinPercentage() and
            nRest7.getWinPercentage() == nRest3.getWinPercentage() and
            nRest7.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest6.getWinPercentage() and 
            nRest8.getWinPercentage() == nRest9.getWinPercentage() and
            not nRest9.getWinPercentage() == nRest10.getWinPercentage() and
            not nRest1.getWinPercentage() == nRest2.getWinPercentage()):
        result = tiebreak7(nRest7, nRest8, nRest3, nRest4, nRest5, nRest6, nRest9)
        nfcWC = [nRest1, nRest2, result[0]]


    #6 teams tied
    elif (nRest1.getWinPercentage() == nRest2.getWinPercentage() and
            nRest1.getWinPercentage() == nRest3.getWinPercentage() and
            nRest1.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest1.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest1.getWinPercentage() == nRest6.getWinPercentage()):
        result = tiebreak6(nRest1, nRest2, nRest3, nRest4, nRest5, nRest6)
        nfcWC = [result[0], result[1], result[2]]
        
    elif (nRest7.getWinPercentage() == nRest2.getWinPercentage() and
            nRest7.getWinPercentage() == nRest3.getWinPercentage() and
            nRest7.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest6.getWinPercentage()):
        result = tiebreak6(nRest7, nRest2, nRest3, nRest4, nRest5, nRest6)
        nfcWC = [nRest1, result[0], result[1]]
        
    elif (nRest7.getWinPercentage() == nRest8.getWinPercentage() and
            nRest7.getWinPercentage() == nRest3.getWinPercentage() and
            nRest7.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest6.getWinPercentage() and 
            not nRest8.getWinPercentage() == nRest9.getWinPercentage() and
            nRest1.getWinPercentage() == nRest2.getWinPercentage()):
        result1 = tiebreak6(nRest7, nRest8, nRest3, nRest4, nRest5, nRest6)
        result2 = tiebreak2(nRest1, nRest2)
        nfcWC = [result2[0], result2[1], result1[0]]
        
    elif (nRest7.getWinPercentage() == nRest8.getWinPercentage() and
            nRest7.getWinPercentage() == nRest3.getWinPercentage() and
            nRest7.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest5.getWinPercentage() and 
            nRest7.getWinPercentage() == nRest6.getWinPercentage() and 
            not nRest1.getWinPercentage() == nRest2.getWinPercentage()):
        result = tiebreak6(nRest7, nRest8, nRest3, nRest4, nRest5, nRest6)
        nfcWC = [nRest1, nRest2, result[0]]
    
    
    #5 teams tied
    elif (nRest1.getWinPercentage() == nRest2.getWinPercentage() and
            nRest1.getWinPercentage() == nRest3.getWinPercentage() and
            nRest1.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest1.getWinPercentage() == nRest5.getWinPercentage()):
        result = tiebreak5(nRest1, nRest2, nRest3, nRest4, nRest5)
        nfcWC = [result[0], result[1], result[2]]
        
    elif (nRest6.getWinPercentage() == nRest2.getWinPercentage() and
            nRest6.getWinPercentage() == nRest3.getWinPercentage() and
            nRest6.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest6.getWinPercentage() == nRest5.getWinPercentage()):
        result = tiebreak5(nRest6, nRest2, nRest3, nRest4, nRest5)
        nfcWC = [nRest1, result[0], result[1]]
        
    elif (nRest6.getWinPercentage() == nRest7.getWinPercentage() and
            nRest6.getWinPercentage() == nRest3.getWinPercentage() and
            nRest6.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest6.getWinPercentage() == nRest5.getWinPercentage() and
            nRest1.getWinPercentage() == nRest2.getWinPercentage()):
        result1 = tiebreak5(nRest6, nRest7, nRest3, nRest4, nRest5)
        result2 = tiebreak2(nRest1, nRest2)
        nfcWC = [result2[0], result2[1], result1[0]]
        
    elif (nRest6.getWinPercentage() == nRest7.getWinPercentage() and
            nRest6.getWinPercentage() == nRest3.getWinPercentage() and
            nRest6.getWinPercentage() == nRest4.getWinPercentage() and 
            nRest6.getWinPercentage() == nRest5.getWinPercentage() and
            not nRest1.getWinPercentage() == nRest2.getWinPercentage()):
        result = tiebreak5(nRest6, nRest7, nRest3, nRest4, nRest5)
        nfcWC = [nRest1, nRest2, result[0]]
    
    
    # 4 teams tied
    elif (nRest1.getWinPercentage() == nRest2.getWinPercentage() and
            nRest1.getWinPercentage() == nRest3.getWinPercentage() and
            nRest1.getWinPercentage() == nRest4.getWinPercentage()):
        result1 = tiebreak4(nRest1, nRest2, nRest3, nRest4)
        nfcWC = [result1[0], result1[1], result1[2]]

    elif (nRest5.getWinPercentage() == nRest2.getWinPercentage() and
          nRest5.getWinPercentage() == nRest3.getWinPercentage() and
          nRest5.getWinPercentage() == nRest4.getWinPercentage()):
        result1 = tiebreak4(nRest5, nRest2, nRest3, nRest4)
        nfcWC = [nRest1, result1[0], result1[1]]

    elif (nRest5.getWinPercentage() == nRest6.getWinPercentage() and
          nRest5.getWinPercentage() == nRest3.getWinPercentage() and
          nRest5.getWinPercentage() == nRest4.getWinPercentage() and
          nRest1.getWinPercentage() == nRest2.getWinPercentage()):
        result1 = tiebreak4(nRest5, nRest6, nRest3, nRest4)
        result2 = tiebreak2(nRest1, nRest2)
        nfcWC = [result2[0], result2[1], result1[0]]
        
    elif (nRest5.getWinPercentage() == nRest6.getWinPercentage() and
          nRest5.getWinPercentage() == nRest3.getWinPercentage() and
          nRest5.getWinPercentage() == nRest4.getWinPercentage() and
          not nRest1.getWinPercentage() == nRest2.getWinPercentage()):
        result1 = tiebreak4(nRest5, nRest6, nRest3, nRest4)
        nfcWC = [nRest1, nRest2, result1[0]]

    # 3 teams tied
    elif (nRest1.getWinPercentage() == nRest2.getWinPercentage() and
          nRest3.getWinPercentage() == nRest1.getWinPercentage()):
        result1 = tiebreak3(nRest1, nRest2, nRest3)
        nfcWC = [result1[0], result1[1], result1[2]]

    elif (nRest4.getWinPercentage() == nRest2.getWinPercentage() and
          nRest3.getWinPercentage() == nRest4.getWinPercentage()):
        result1 = tiebreak3(nRest4, nRest2, nRest3)
        nfcWC = [nRest1, result1[0], result1[1]]

    elif (nRest3.getWinPercentage() == nRest4.getWinPercentage() and
          nRest3.getWinPercentage == nRest5.getWinPercentage() and 
          nRest1.getWinPercentage == nRest2.getWinPercentage()):
        result1 = tiebreak3(nRest4, nRest5, nRest3)
        result2 = tiebreak2(nRest1, nRest2)
        nfcWC = [result2[0], result2[1], result1[0]]

    elif (nRest3.getWinPercentage() == nRest4.getWinPercentage() and
          nRest3.getWinPercentage == nRest5.getWinPercentage() and 
          not nRest1.getWinPercentage == nRest2.getWinPercentage()):
        result1 = tiebreak3(nRest4, nRest5, nRest3)
        nfcWC = [nRest1, nRest2, result1[0]]

    # 2 team tiebreakers
    elif (nRest1.getWinPercentage() == nRest2.getWinPercentage() and
          nRest3.getWinPercentage() == nRest4.getWinPercentage() and 
          not nRest1.getWinPercentage() == nRest3.getWinPercentage()):
        result1 = tiebreak2(nRest1, nRest2)
        result2 = tiebreak2(nRest3, nRest4)
        nfcWC = [result1[0], result1[1], result2[0]]
        
    elif (not nRest1.getWinPercentage() == nRest2.getWinPercentage() and
          nRest3.getWinPercentage() == nRest4.getWinPercentage() and 
          not nRest2.getWinPercentage() == nRest3.getWinPercentage()):
        result = tiebreak2(nRest3, nRest4)
        nfcWC = [nRest1, nRest2, result[0]]
        
    elif (not nRest1.getWinPercentage() == nRest2.getWinPercentage() and
          nRest3.getWinPercentage() == nRest2.getWinPercentage()):
        result = tiebreak2(nRest3, nRest2)
        nfcWC = [nRest1, result[0], result[1]]
        
    elif (nRest1.getWinPercentage() == nRest2.getWinPercentage() and
          not nRest3.getWinPercentage() == nRest2.getWinPercentage()):
        result = tiebreak2(nRest1, nRest2)
        nfcWC = [result[0], result[1], nRest3]
        
    elif (not nRest1.getWinPercentage() == nRest2.getWinPercentage() and
          not nRest3.getWinPercentage() == nRest2.getWinPercentage()):
        nfcWC = [nRest1, nRest2, nRest3]
        
    else:
        print ("9+ team tiebreaker")



    playoffs = [afcDivLeaders[0], afcDivLeaders[1], afcDivLeaders[2], afcDivLeaders[3], afcWC[0], afcWC[1], afcWC[2],
                nfcDivLeaders[0], nfcDivLeaders[1], nfcDivLeaders[2], nfcDivLeaders[3], nfcWC[0], nfcWC[1], nfcWC[2]]

    '''
    print("AFC:")
    print("1. " + afcDivLeaders[0].getName() + ": " + str(afcDivLeaders[0].getWins()) + "-" + str(afcDivLeaders[0].getLosses()))
    print("2. " + afcDivLeaders[1].getName() + ": " + str(afcDivLeaders[1].getWins()) + "-" + str(afcDivLeaders[1].getLosses()))
    print("3. " + afcDivLeaders[2].getName() + ": " + str(afcDivLeaders[2].getWins()) + "-" + str(afcDivLeaders[2].getLosses()))
    print("4. " + afcDivLeaders[3].getName() + ": " + str(afcDivLeaders[3].getWins()) + "-" + str(afcDivLeaders[3].getLosses()))
    print("5. " + afcWC[0].getName() + ": " + str(afcWC[0].getWins()) + "-" + str(afcWC[0].getLosses()))
    print("6. " + afcWC[1].getName() + ": " + str(afcWC[1].getWins()) + "-" + str(afcWC[1].getLosses()))
    print("7. " + afcWC[2].getName() + ": " + str(afcWC[2].getWins()) + "-" + str(afcWC[2].getLosses()))
    '''
    '''
    print("NFC:")
    print("1. " + nfcDivLeaders[0].getName() + ": " + str(nfcDivLeaders[0].getWins()) + "-" + str(nfcDivLeaders[0].getLosses()))
    print("2. " + nfcDivLeaders[1].getName() + ": " + str(nfcDivLeaders[1].getWins()) + "-" + str(nfcDivLeaders[1].getLosses()))
    print("3. " + nfcDivLeaders[2].getName() + ": " + str(nfcDivLeaders[2].getWins()) + "-" + str(nfcDivLeaders[2].getLosses()))
    print("4. " + nfcDivLeaders[3].getName() + ": " + str(nfcDivLeaders[3].getWins()) + "-" + str(nfcDivLeaders[3].getLosses()))
    print("5. " + nfcWC[0].getName() + ": " + str(nfcWC[0].getWins()) + "-" + str(nfcWC[0].getLosses()))
    print("6. " + nfcWC[1].getName() + ": " + str(nfcWC[1].getWins()) + "-" + str(nfcWC[1].getLosses()))
    print("7. " + nfcWC[2].getName() + ": " + str(nfcWC[2].getWins()) + "-" + str(nfcWC[2].getLosses()))
    '''

    return (playoffs)


def resetStandings():
    for team in teamList:
        #print(f"Resetting standings for {team.name}")
        # Get games for this team (home or away)
        team_games = df[(df['homeTeam'] == team.name) | (df['awayTeam'] == team.name)]
        
        # Track game indices in team's schedule
        game_index = 0
        for index, row in team_games.iterrows():
            # Check if game has no result (homeScore and awayScore both 0)
            if row['homeScore'] == 0 and row['awayScore'] == 0:
                team.results[game_index] = 'NA'
                print(f"Game between {row['homeTeam']} and {row['awayTeam']} is reset to 'NA'")
            game_index += 1

def resetSimStandings(df):
    for team in teamList:
        team_games = df[(df['homeTeam'] == team.name) | (df['awayTeam'] == team.name)]
        game_index = 0
        for index, row in team_games.iterrows():
            if row['homeScore'] == 0 and row['awayScore'] == 0:
                team.results[game_index] = 'NA'
            game_index += 1


def trackScenarios(playoffs, remSchedules, Team, spot):
    resultTeamLists = []
    opponentTeamLists = []
    resultsList = []
    for schedule in remSchedules:
        resultTeamList = []
        opponentTeamList = []
        results = []
        for i in range(len(schedule)):
            if (i % 3 == 0):
                resultTeamList.append(schedule[i])
            elif (i % 3 == 1):
                opponentTeamList.append(schedule[i])
            else:
                results.append(schedule[i])
        resultTeamLists.append(resultTeamList)
        opponentTeamLists.append(opponentTeamList)
        resultsList.append(results)
       
    afc = 'false'
    if (Team.getConference() == 'AFC'):
        afc = 'true'
    
    team = Team.getName()
    if (not spot == '1' and not spot == '2' and not spot == '3' and not spot == '4' and not spot == '5' and 
        not spot == '6' and not spot == '7' and not spot == 'p' and not spot == 'd' and not spot == 'o'):
        print ("Invalid character for trackScenarios")
        return 0
    
    spotList = []
    if (spot == '1'):
        if (afc == 'true'):
            for i in range(len(playoffs)):
                if (playoffs[i][0] == Team):
                    spotList.append(resultsList[i])
        else:
            for i in range(len(playoffs)):
                if (playoffs[i][7] == Team):
                    spotList.append(resultsList[i])
    
    elif (spot == '2'):
        if (afc == 'true'):
            for i in range(len(playoffs)):
                if (playoffs[i][1] == Team):
                    spotList.append(resultsList[i])
        else:
            for i in range(len(playoffs)):
                if (playoffs[i][8] == Team):
                    spotList.append(resultsList[i])
                    
    elif (spot == '3'):
        if (afc == 'true'):
            for i in range(len(playoffs)):
                if (playoffs[i][2] == Team):
                    spotList.append(resultsList[i])
        else:
            for i in range(len(playoffs)):
                if (playoffs[i][9] == Team):
                    spotList.append(resultsList[i])
                    
    elif (spot == '4'):
        if (afc == 'true'):
            for i in range(len(playoffs)):
                if (playoffs[i][3] == Team):
                    spotList.append(resultsList[i])
        else:
            for i in range(len(playoffs)):
                if (playoffs[i][10] == Team):
                    spotList.append(resultsList[i])
                    
    elif (spot == '5'):
        if (afc == 'true'):
            for i in range(len(playoffs)):
                if (playoffs[i][4] == Team):
                    spotList.append(resultsList[i])
        else:
            for i in range(len(playoffs)):
                if (playoffs[i][11] == Team):
                    spotList.append(resultsList[i])
                    
    elif (spot == '6'):
        if (afc == 'true'):
            for i in range(len(playoffs)):
                if (playoffs[i][5] == Team):
                    spotList.append(resultsList[i])
        else:
            for i in range(len(playoffs)):
                if (playoffs[i][12] == Team):
                    spotList.append(resultsList[i])
                    
    elif (spot == '7'):
        if (afc == 'true'):
            for i in range(len(playoffs)):
                if (playoffs[i][6] == Team):
                    spotList.append(resultsList[i])
        else:
            for i in range(len(playoffs)):
                if (playoffs[i][13] == Team):
                    spotList.append(resultsList[i])
                    
    elif (spot == 'd'):
        if (afc == 'true'):
            for i in range(len(playoffs)):
                if (playoffs[i][0] == Team or playoffs[i][1] == Team or playoffs[i][2] == Team or playoffs[i][3] == Team):
                    spotList.append(resultsList[i])
        else:
            for i in range(len(playoffs)):
                if (playoffs[i][7] == Team or playoffs[i][8] == Team or playoffs[i][9] == Team or playoffs[i][10] == Team):
                    spotList.append(resultsList[i])
                    
    elif (spot == 'p'):
        if (afc == 'true'):
            for i in range(len(playoffs)):
                if (playoffs[i][0] == Team or playoffs[i][1] == Team or playoffs[i][2] == Team or playoffs[i][3] == Team
                    or playoffs[i][4] == Team or playoffs[i][5] == Team or playoffs[i][6] == Team):
                    spotList.append(resultsList[i])
        else:
            for i in range(len(playoffs)):
                if (playoffs[i][7] == Team or playoffs[i][8] == Team or playoffs[i][9] == Team or playoffs[i][10] == Team
                    or playoffs[i][11] == Team or playoffs[i][12] == Team or playoffs[i][13] == Team):
                    spotList.append(resultsList[i])
                    
    elif (spot == 'o'):
        if (afc == 'true'):
            for i in range(len(playoffs)):
                if (not playoffs[i][0] == Team and not playoffs[i][1] == Team and not playoffs[i][2] == Team and not
                    playoffs[i][3] == Team and not playoffs[i][4] == Team and not playoffs[i][5] == Team and not
                    playoffs[i][6] == Team):
                    spotList.append(resultsList[i])
        else:
            for i in range(len(playoffs)):
                if (not playoffs[i][7] == Team and not playoffs[i][8] == Team and not playoffs[i][9] == Team and not
                    playoffs[i][10] == Team and not playoffs[i][11] == Team and not playoffs[i][12] == Team and not
                    playoffs[i][13] == Team):
                    spotList.append(resultsList[i])
                    
    #findPatterns(spotList, resultsList, Team, resultTeamLists, opponentTeamLists, spot)
    



def playoffPercentages():
    bills1, bills2, bills3, bills4, bills5, bills6, bills7, billsOut = 0, 0, 0, 0, 0, 0, 0, 0
    dolphins1, dolphins2, dolphins3, dolphins4, dolphins5, dolphins6, dolphins7, dolphinsOut = 0, 0, 0, 0, 0, 0, 0, 0
    jets1, jets2, jets3, jets4, jets5, jets6, jets7, jetsOut = 0, 0, 0, 0, 0, 0, 0, 0
    patriots1, patriots2, patriots3, patriots4, patriots5, patriots6, patriots7, patriotsOut = 0, 0, 0, 0, 0, 0, 0, 0
    browns1, browns2, browns3, browns4, browns5, browns6, browns7, brownsOut = 0, 0, 0, 0, 0, 0, 0, 0
    bengals1, bengals2, bengals3, bengals4, bengals5, bengals6, bengals7, bengalsOut = 0, 0, 0, 0, 0, 0, 0, 0
    ravens1, ravens2, ravens3, ravens4, ravens5, ravens6, ravens7, ravensOut = 0, 0, 0, 0, 0, 0, 0, 0
    steelers1, steelers2, steelers3, steelers4, steelers5, steelers6, steelers7, steelersOut = 0, 0, 0, 0, 0, 0, 0, 0
    colts1, colts2, colts3, colts4, colts5, colts6, colts7, coltsOut = 0, 0, 0, 0, 0, 0, 0, 0
    jaguars1, jaguars2, jaguars3, jaguars4, jaguars5, jaguars6, jaguars7, jaguarsOut = 0, 0, 0, 0, 0, 0, 0, 0
    titans1, titans2, titans3, titans4, titans5, titans6, titans7, titansOut = 0, 0, 0, 0, 0, 0, 0, 0
    texans1, texans2, texans3, texans4, texans5, texans6, texans7, texansOut = 0, 0, 0, 0, 0, 0, 0, 0
    broncos1, broncos2, broncos3, broncos4, broncos5, broncos6, broncos7, broncosOut = 0, 0, 0, 0, 0, 0, 0, 0
    chargers1, chargers2, chargers3, chargers4, chargers5, chargers6, chargers7, chargersOut = 0, 0, 0, 0, 0, 0, 0, 0
    chiefs1, chiefs2, chiefs3, chiefs4, chiefs5, chiefs6, chiefs7, chiefsOut = 0, 0, 0, 0, 0, 0, 0, 0
    raiders1, raiders2, raiders3, raiders4, raiders5, raiders6, raiders7, raidersOut = 0, 0, 0, 0, 0, 0, 0, 0
    commanders1, commanders2, commanders3, commanders4, commanders5, commanders6, commanders7, commandersOut = 0, 0, 0, 0, 0, 0, 0, 0
    cowboys1, cowboys2, cowboys3, cowboys4, cowboys5, cowboys6, cowboys7, cowboysOut = 0, 0, 0, 0, 0, 0, 0, 0
    eagles1, eagles2, eagles3, eagles4, eagles5, eagles6, eagles7, eaglesOut = 0, 0, 0, 0, 0, 0, 0, 0
    giants1, giants2, giants3, giants4, giants5, giants6, giants7, giantsOut = 0, 0, 0, 0, 0, 0, 0, 0
    bears1, bears2, bears3, bears4, bears5, bears6, bears7, bearsOut = 0, 0, 0, 0, 0, 0, 0, 0
    lions1, lions2, lions3, lions4, lions5, lions6, lions7, lionsOut = 0, 0, 0, 0, 0, 0, 0, 0
    packers1, packers2, packers3, packers4, packers5, packers6, packers7, packersOut = 0, 0, 0, 0, 0, 0, 0, 0
    vikings1, vikings2, vikings3, vikings4, vikings5, vikings6, vikings7, vikingsOut = 0, 0, 0, 0, 0, 0, 0, 0
    buccaneers1, buccaneers2, buccaneers3, buccaneers4, buccaneers5, buccaneers6, buccaneers7, buccaneersOut = 0, 0, 0, 0, 0, 0, 0, 0
    falcons1, falcons2, falcons3, falcons4, falcons5, falcons6, falcons7, falconsOut = 0, 0, 0, 0, 0, 0, 0, 0
    saints1, saints2, saints3, saints4, saints5, saints6, saints7, saintsOut = 0, 0, 0, 0, 0, 0, 0, 0
    panthers1, panthers2, panthers3, panthers4, panthers5, panthers6, panthers7, panthersOut = 0, 0, 0, 0, 0, 0, 0, 0
    cardinals1, cardinals2, cardinals3, cardinals4, cardinals5, cardinals6, cardinals7, cardinalsOut = 0, 0, 0, 0, 0, 0, 0, 0
    niners1, niners2, niners3, niners4, niners5, niners6, niners7, ninersOut = 0, 0, 0, 0, 0, 0, 0, 0
    rams1, rams2, rams3, rams4, rams5, rams6, rams7, ramsOut = 0, 0, 0, 0, 0, 0, 0, 0
    seahawks1, seahawks2, seahawks3, seahawks4, seahawks5, seahawks6, seahawks7, seahawksOut = 0, 0, 0, 0, 0, 0, 0, 0


    playoffsList = []
    remSchedules= []
    for i in range(5000):
        remSchedule = []
        for i in range(17):
            if (not Bills.results[i] == 'W' and not Bills.results[i] == 'L' and not Bills.results[i] == 'T'):
                game = Bills.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Bills')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Bills.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Bills.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Bills.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Dolphins.results[i] == 'W' and not Dolphins.results[i] == 'L' and not Dolphins.results[i] == 'T'):
                game = Dolphins.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Dolphins')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Dolphins.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Dolphins.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Dolphins.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Jets.results[i] == 'W' and not Jets.results[i] == 'L' and not Jets.results[i] == 'T'):
                game = Jets.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Jets')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Jets.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Jets.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Jets.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Patriots.results[i] == 'W' and not Patriots.results[i] == 'L' and not Patriots.results[i] == 'T'):
                game = Patriots.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Patriots')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Patriots.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Patriots.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Patriots.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Browns.results[i] == 'W' and not Browns.results[i] == 'L' and not Browns.results[i] == 'T'):
                game = Browns.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Browns')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Browns.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Browns.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Browns.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Bengals.results[i] == 'W' and not Bengals.results[i] == 'L' and not Bengals.results[i] == 'T'):
                game = Bengals.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Bengals')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Bengals.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Bengals.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Bengals.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Ravens.results[i] == 'W' and not Ravens.results[i] == 'L' and not Ravens.results[i] == 'T'):
                game = Ravens.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Ravens')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Ravens.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Ravens.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Ravens.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Steelers.results[i] == 'W' and not Steelers.results[i] == 'L' and not Steelers.results[i] == 'T'):
                game = Steelers.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Steelers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Steelers.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Steelers.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Steelers.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Colts.results[i] == 'W' and not Colts.results[i] == 'L' and not Colts.results[i] == 'T'):
                game = Colts.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Colts')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Colts.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Colts.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Colts.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Jaguars.results[i] == 'W' and not Jaguars.results[i] == 'L' and not Jaguars.results[i] == 'T'):
                game = Jaguars.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Jaguars')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Jaguars.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Jaguars.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Jaguars.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Titans.results[i] == 'W' and not Titans.results[i] == 'L' and not Titans.results[i] == 'T'):
                game = Titans.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Titans')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Titans.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Titans.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Titans.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Texans.results[i] == 'W' and not Texans.results[i] == 'L' and not Texans.results[i] == 'T'):
                game = Texans.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Texans')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Texans.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Texans.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Texans.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Broncos.results[i] == 'W' and not Broncos.results[i] == 'L' and not Broncos.results[i] == 'T'):
                game = Broncos.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Broncos')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Broncos.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Broncos.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Broncos.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Chargers.results[i] == 'W' and not Chargers.results[i] == 'L' and not Chargers.results[i] == 'T'):
                game = Chargers.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Chargers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Chargers.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Chargers.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Chargers.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Chiefs.results[i] == 'W' and not Chiefs.results[i] == 'L' and not Chiefs.results[i] == 'T'):
                game = Chiefs.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Chiefs')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Chiefs.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Chiefs.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Chiefs.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Raiders.results[i] == 'W' and not Raiders.results[i] == 'L' and not Raiders.results[i] == 'T'):
                game = Raiders.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Raiders')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Raiders.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Raiders.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Raiders.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Cowboys.results[i] == 'W' and not Cowboys.results[i] == 'L' and not Cowboys.results[i] == 'T'):
                game = Cowboys.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Cowboys')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Cowboys.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Cowboys.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Cowboys.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Commanders.results[i] == 'W' and not Commanders.results[i] == 'L' and not Commanders.results[i] == 'T'):
                game = Commanders.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Commanders')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Commanders.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Commanders.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Commanders.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Eagles.results[i] == 'W' and not Eagles.results[i] == 'L' and not Eagles.results[i] == 'T'):
                game = Eagles.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Eagles')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Eagles.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Eagles.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Eagles.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Giants.results[i] == 'W' and not Giants.results[i] == 'L' and not Giants.results[i] == 'T'):
                game = Giants.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Giants')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Giants.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Giants.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Giants.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Bears.results[i] == 'W' and not Bears.results[i] == 'L' and not Bears.results[i] == 'T'):
                game = Bears.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Bears')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Bears.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Bears.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Bears.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Lions.results[i] == 'W' and not Lions.results[i] == 'L' and not Lions.results[i] == 'T'):
                game = Lions.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Lions')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Lions.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Lions.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Lions.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Packers.results[i] == 'W' and not Packers.results[i] == 'L' and not Packers.results[i] == 'T'):
                game = Packers.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Packers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Packers.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Packers.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Packers.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Vikings.results[i] == 'W' and not Vikings.results[i] == 'L' and not Vikings.results[i] == 'T'):
                game = Vikings.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Vikings')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Vikings.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Vikings.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Vikings.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Buccaneers.results[i] == 'W' and not Buccaneers.results[i] == 'L' and not Buccaneers.results[i] == 'T'):
                game = Buccaneers.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Buccaneers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Buccaneers.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Buccaneers.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Buccaneers.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Falcons.results[i] == 'W' and not Falcons.results[i] == 'L' and not Falcons.results[i] == 'T'):
                game = Falcons.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Falcons')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Falcons.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Falcons.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Falcons.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Saints.results[i] == 'W' and not Saints.results[i] == 'L' and not Saints.results[i] == 'T'):
                game = Saints.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Saints')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Saints.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Saints.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Saints.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Panthers.results[i] == 'W' and not Panthers.results[i] == 'L' and not Panthers.results[i] == 'T'):
                game = Panthers.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Panthers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Panthers.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Panthers.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Panthers.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Cardinals.results[i] == 'W' and not Cardinals.results[i] == 'L' and not Cardinals.results[i] == 'T'):
                game = Cardinals.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Cardinals')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Cardinals.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Cardinals.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Cardinals.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Niners.results[i] == 'W' and not Niners.results[i] == 'L' and not Niners.results[i] == 'T'):
                game = Niners.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('49ers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Niners.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Niners.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Niners.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Rams.results[i] == 'W' and not Rams.results[i] == 'L' and not Rams.results[i] == 'T'):
                game = Rams.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Rams')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Rams.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Rams.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Rams.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Seahawks.results[i] == 'W' and not Seahawks.results[i] == 'L' and not Seahawks.results[i] == 'T'):
                game = Seahawks.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Seahawks')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Seahawks.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Seahawks.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Seahawks.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        playoffs = playoffStandings()
        playoffsList.append(playoffs)
        remSchedules.append(remSchedule)
        for team in playoffs:
            if (team == Bills):
                if (playoffs[0] == Bills):
                    bills1 += 1
                elif (playoffs[1] == Bills):
                    bills2 += 1
                elif (playoffs[2] == Bills):
                    bills3 += 1
                elif (playoffs[3] == Bills):
                    bills4 += 1
                elif (playoffs[4] == Bills):
                    bills5 += 1
                elif (playoffs[5] == Bills):
                    bills6 += 1
                elif (playoffs[6] == Bills):
                    bills7 += 1
                else:
                    billsOut += 1

            if (team == Dolphins):
                if (playoffs[0] == Dolphins):
                    dolphins1 += 1
                elif (playoffs[1] == Dolphins):
                    dolphins2 += 1
                elif (playoffs[2] == Dolphins):
                    dolphins3 += 1
                elif (playoffs[3] == Dolphins):
                    dolphins4 += 1
                elif (playoffs[4] == Dolphins):
                    dolphins5 += 1
                elif (playoffs[5] == Dolphins):
                    dolphins6 += 1
                elif (playoffs[6] == Dolphins):
                    dolphins7 += 1
                else:
                    dolphinsOut += 1
            if (team == Jets):
                if (playoffs[0] == Jets):
                    jets1 += 1
                elif (playoffs[1] == Jets):
                    jets2 += 1
                elif (playoffs[2] == Jets):
                    jets3 += 1
                elif (playoffs[3] == Jets):
                    jets4 += 1
                elif (playoffs[4] == Jets):
                    jets5 += 1
                elif (playoffs[5] == Jets):
                    jets6 += 1
                elif (playoffs[6] == Jets):
                    jets7 += 1
                else:
                    jetsOut += 1

            if (team == Patriots):
                if (playoffs[0] == Patriots):
                    patriots1 += 1
                elif (playoffs[1] == Patriots):
                    patriots2 += 1
                elif (playoffs[2] == Patriots):
                    patriots3 += 1
                elif (playoffs[3] == Patriots):
                    patriots4 += 1
                elif (playoffs[4] == Patriots):
                    patriots5 += 1
                elif (playoffs[5] == Patriots):
                    patriots6 += 1
                elif (playoffs[6] == Patriots):
                    patriots7 += 1
                else:
                    patriotsOut += 1

            if (team == Browns):
                if (playoffs[0] == Browns):
                    browns1 += 1
                elif (playoffs[1] == Browns):
                    browns2 += 1
                elif (playoffs[2] == Browns):
                    browns3 += 1
                elif (playoffs[3] == Browns):
                    browns4 += 1
                elif (playoffs[4] == Browns):
                    browns5 += 1
                elif (playoffs[5] == Browns):
                    browns6 += 1
                elif (playoffs[6] == Browns):
                    browns7 += 1
                else:
                    brownsOut += 1

            if (team == Bengals):
                if (playoffs[0] == Bengals):
                    bengals1 += 1
                elif (playoffs[1] == Bengals):
                    bengals2 += 1
                elif (playoffs[2] == Bengals):
                    bengals3 += 1
                elif (playoffs[3] == Bengals):
                    bengals4 += 1
                elif (playoffs[4] == Bengals):
                    bengals5 += 1
                elif (playoffs[5] == Bengals):
                    bengals6 += 1
                elif (playoffs[6] == Bengals):
                    bengals7 += 1
                else:
                    bengalsOut += 1

            if (team == Ravens):
                if (playoffs[0] == Ravens):
                    ravens1 += 1
                elif (playoffs[1] == Ravens):
                    ravens2 += 1
                elif (playoffs[2] == Ravens):
                    ravens3 += 1
                elif (playoffs[3] == Ravens):
                    ravens4 += 1
                elif (playoffs[4] == Ravens):
                    ravens5 += 1
                elif (playoffs[5] == Ravens):
                    ravens6 += 1
                elif (playoffs[6] == Ravens):
                    ravens7 += 1
                else:
                    ravensOut += 1

            if (team == Steelers):
                if (playoffs[0] == Steelers):
                    steelers1 += 1
                elif (playoffs[1] == Steelers):
                    steelers2 += 1
                elif (playoffs[2] == Steelers):
                    steelers3 += 1
                elif (playoffs[3] == Steelers):
                    steelers4 += 1
                elif (playoffs[4] == Steelers):
                    steelers5 += 1
                elif (playoffs[5] == Steelers):
                    steelers6 += 1
                elif (playoffs[6] == Steelers):
                    steelers7 += 1
                else:
                    steelersOut += 1

            if (team == Colts):
                if (playoffs[0] == Colts):
                    colts1 += 1
                elif (playoffs[1] == Colts):
                    colts2 += 1
                elif (playoffs[2] == Colts):
                    colts3 += 1
                elif (playoffs[3] == Colts):
                    colts4 += 1
                elif (playoffs[4] == Colts):
                    colts5 += 1
                elif (playoffs[5] == Colts):
                    colts6 += 1
                elif (playoffs[6] == Colts):
                    colts7 += 1
                else:
                    coltsOut += 1

            if (team == Jaguars):
                if (playoffs[0] == Jaguars):
                    jaguars1 += 1
                elif (playoffs[1] == Jaguars):
                    jaguars2 += 1
                elif (playoffs[2] == Jaguars):
                    jaguars3 += 1
                elif (playoffs[3] == Jaguars):
                    jaguars4 += 1
                elif (playoffs[4] == Jaguars):
                    jaguars5 += 1
                elif (playoffs[5] == Jaguars):
                    jaguars6 += 1
                elif (playoffs[6] == Jaguars):
                    jaguars7 += 1
                else:
                    jaguarsOut += 1

            if (team == Titans):
                if (playoffs[0] == Titans):
                    titans1 += 1
                elif (playoffs[1] == Titans):
                    titans2 += 1
                elif (playoffs[2] == Titans):
                    titans3 += 1
                elif (playoffs[3] == Titans):
                    titans4 += 1
                elif (playoffs[4] == Titans):
                    titans5 += 1
                elif (playoffs[5] == Titans):
                    titans6 += 1
                elif (playoffs[6] == Titans):
                    titans7 += 1
                else:
                    titansOut += 1

            if (team == Texans):
                if (playoffs[0] == Texans):
                    texans1 += 1
                elif (playoffs[1] == Texans):
                    texans2 += 1
                elif (playoffs[2] == Texans):
                    texans3 += 1
                elif (playoffs[3] == Texans):
                    texans4 += 1
                elif (playoffs[4] == Texans):
                    texans5 += 1
                elif (playoffs[5] == Texans):
                    texans6 += 1
                elif (playoffs[6] == Texans):
                    texans7 += 1
                else:
                    texansOut += 1

            if (team == Broncos):
                if (playoffs[0] == Broncos):
                    broncos1 += 1
                elif (playoffs[1] == Broncos):
                    broncos2 += 1
                elif (playoffs[2] == Broncos):
                    broncos3 += 1
                elif (playoffs[3] == Broncos):
                    broncos4 += 1
                elif (playoffs[4] == Broncos):
                    broncos5 += 1
                elif (playoffs[5] == Broncos):
                    broncos6 += 1
                elif (playoffs[6] == Broncos):
                    broncos7 += 1
                else:
                    broncosOut += 1

            if (team == Chargers):
                if (playoffs[0] == Chargers):
                    chargers1 += 1
                elif (playoffs[1] == Chargers):
                    chargers2 += 1
                elif (playoffs[2] == Chargers):
                    chargers3 += 1
                elif (playoffs[3] == Chargers):
                    chargers4 += 1
                elif (playoffs[4] == Chargers):
                    chargers5 += 1
                elif (playoffs[5] == Chargers):
                    chargers6 += 1
                elif (playoffs[6] == Chargers):
                    chargers7 += 1
                else:
                    chargersOut += 1

            if (team == Chiefs):
                if (playoffs[0] == Chiefs):
                    chiefs1 += 1
                elif (playoffs[1] == Chiefs):
                    chiefs2 += 1
                elif (playoffs[2] == Chiefs):
                    chiefs3 += 1
                elif (playoffs[3] == Chiefs):
                    chiefs4 += 1
                elif (playoffs[4] == Chiefs):
                    chiefs5 += 1
                elif (playoffs[5] == Chiefs):
                    chiefs6 += 1
                elif (playoffs[6] == Chiefs):
                    chiefs7 += 1
                else:
                    chiefsOut += 1

            if (team == Raiders):
                if (playoffs[0] == Raiders):
                    raiders1 += 1
                elif (playoffs[1] == Raiders):
                    raiders2 += 1
                elif (playoffs[2] == Raiders):
                    raiders3 += 1
                elif (playoffs[3] == Raiders):
                    raiders4 += 1
                elif (playoffs[4] == Raiders):
                    raiders5 += 1
                elif (playoffs[5] == Raiders):
                    raiders6 += 1
                elif (playoffs[6] == Raiders):
                    raiders7 += 1
                else:
                    raidersOut += 1

            if (team == Cowboys):
                if (playoffs[7] == Cowboys):
                    cowboys1 += 1
                elif (playoffs[8] == Cowboys):
                    cowboys2 += 1
                elif (playoffs[9] == Cowboys):
                    cowboys3 += 1
                elif (playoffs[10] == Cowboys):
                    cowboys4 += 1
                elif (playoffs[11] == Cowboys):
                    cowboys5 += 1
                elif (playoffs[12] == Cowboys):
                    cowboys6 += 1
                elif (playoffs[13] == Cowboys):
                    cowboys7 += 1
                else:
                    cowboysOut += 1

            if (team == Commanders):
                if (playoffs[7] == Commanders):
                    commanders1 += 1
                elif (playoffs[8] == Commanders):
                    commanders2 += 1
                elif (playoffs[9] == Commanders):
                    commanders3 += 1
                elif (playoffs[10] == Commanders):
                    commanders4 += 1
                elif (playoffs[11] == Commanders):
                    commanders5 += 1
                elif (playoffs[12] == Commanders):
                    commanders6 += 1
                elif (playoffs[13] == Commanders):
                    commanders7 += 1
                else:
                    commandersOut += 1

            if (team == Eagles):
                if (playoffs[7] == Eagles):
                    eagles1 += 1
                elif (playoffs[8] == Eagles):
                    eagles2 += 1
                elif (playoffs[9] == Eagles):
                    eagles3 += 1
                elif (playoffs[10] == Eagles):
                    eagles4 += 1
                elif (playoffs[11] == Eagles):
                    eagles5 += 1
                elif (playoffs[12] == Eagles):
                    eagles6 += 1
                elif (playoffs[13] == Eagles):
                    eagles7 += 1
                else:
                    eaglesOut += 1

            if (team == Giants):
                if (playoffs[7] == Giants):
                    giants1 += 1
                elif (playoffs[8] == Giants):
                    giants2 += 1
                elif (playoffs[9] == Giants):
                    giants3 += 1
                elif (playoffs[10] == Giants):
                    giants4 += 1
                elif (playoffs[11] == Giants):
                    giants5 += 1
                elif (playoffs[12] == Giants):
                    giants6 += 1
                elif (playoffs[13] == Giants):
                    giants7 += 1
                else:
                    giantsOut += 1

            if (team == Bears):
                if (playoffs[7] == Bears):
                    bears1 += 1
                elif (playoffs[8] == Bears):
                    bears2 += 1
                elif (playoffs[9] == Bears):
                    bears3 += 1
                elif (playoffs[10] == Bears):
                    bears4 += 1
                elif (playoffs[11] == Bears):
                    bears5 += 1
                elif (playoffs[12] == Bears):
                    bears6 += 1
                elif (playoffs[13] == Bears):
                    bears7 += 1
                else:
                    bearsOut += 1

            if (team == Lions):
                if (playoffs[7] == Lions):
                    lions1 += 1
                elif (playoffs[8] == Lions):
                    lions2 += 1
                elif (playoffs[9] == Lions):
                    lions3 += 1
                elif (playoffs[10] == Lions):
                    lions4 += 1
                elif (playoffs[11] == Lions):
                    lions5 += 1
                elif (playoffs[12] == Lions):
                    lions6 += 1
                elif (playoffs[13] == Lions):
                    lions7 += 1
                else:
                    lionsOut += 1

            if (team == Packers):
                if (playoffs[7] == Packers):
                    packers1 += 1
                elif (playoffs[8] == Packers):
                    packers2 += 1
                elif (playoffs[9] == Packers):
                    packers3 += 1
                elif (playoffs[10] == Packers):
                    packers4 += 1
                elif (playoffs[11] == Packers):
                    packers5 += 1
                elif (playoffs[12] == Packers):
                    packers6 += 1
                elif (playoffs[13] == Packers):
                    packers7 += 1
                else:
                    packersOut += 1

            if (team == Vikings):
                if (playoffs[7] == Vikings):
                    vikings1 += 1
                elif (playoffs[8] == Vikings):
                    vikings2 += 1
                elif (playoffs[9] == Vikings):
                    vikings3 += 1
                elif (playoffs[10] == Vikings):
                    vikings4 += 1
                elif (playoffs[11] == Vikings):
                    vikings5 += 1
                elif (playoffs[12] == Vikings):
                    vikings6 += 1
                elif (playoffs[13] == Vikings):
                    vikings7 += 1
                else:
                    vikingsOut += 1

            if (team == Buccaneers):
                if (playoffs[7] == Buccaneers):
                    buccaneers1 += 1
                elif (playoffs[8] == Buccaneers):
                    buccaneers2 += 1
                elif (playoffs[9] == Buccaneers):
                    buccaneers3 += 1
                elif (playoffs[10] == Buccaneers):
                    buccaneers4 += 1
                elif (playoffs[11] == Buccaneers):
                    buccaneers5 += 1
                elif (playoffs[12] == Buccaneers):
                    buccaneers6 += 1
                elif (playoffs[13] == Buccaneers):
                    buccaneers7 += 1
                else:
                    buccaneersOut += 1

            if (team == Falcons):
                if (playoffs[7] == Falcons):
                    falcons1 += 1
                elif (playoffs[8] == Falcons):
                    falcons2 += 1
                elif (playoffs[9] == Falcons):
                    falcons3 += 1
                elif (playoffs[10] == Falcons):
                    falcons4 += 1
                elif (playoffs[11] == Falcons):
                    falcons5 += 1
                elif (playoffs[12] == Falcons):
                    falcons6 += 1
                elif (playoffs[13] == Falcons):
                    falcons7 += 1
                else:
                    falconsOut += 1

            if (team == Saints):
                if (playoffs[7] == Saints):
                    saints1 += 1
                elif (playoffs[8] == Saints):
                    saints2 += 1
                elif (playoffs[9] == Saints):
                    saints3 += 1
                elif (playoffs[10] == Saints):
                    saints4 += 1
                elif (playoffs[11] == Saints):
                    saints5 += 1
                elif (playoffs[12] == Saints):
                    saints6 += 1
                elif (playoffs[13] == Saints):
                    saints7 += 1
                else:
                    saintsOut += 1

            if (team == Panthers):
                if (playoffs[7] == Panthers):
                    panthers1 += 1
                elif (playoffs[8] == Panthers):
                    panthers2 += 1
                elif (playoffs[9] == Panthers):
                    panthers3 += 1
                elif (playoffs[10] == Panthers):
                    panthers4 += 1
                elif (playoffs[11] == Panthers):
                    panthers5 += 1
                elif (playoffs[12] == Panthers):
                    panthers6 += 1
                elif (playoffs[13] == Panthers):
                    panthers7 += 1
                else:
                    panthersOut += 1

            if (team == Cardinals):
                if (playoffs[7] == Cardinals):
                    cardinals1 += 1
                elif (playoffs[8] == Cardinals):
                    cardinals2 += 1
                elif (playoffs[9] == Cardinals):
                    cardinals3 += 1
                elif (playoffs[10] == Cardinals):
                    cardinals4 += 1
                elif (playoffs[11] == Cardinals):
                    cardinals5 += 1
                elif (playoffs[12] == Cardinals):
                    cardinals6 += 1
                elif (playoffs[13] == Cardinals):
                    cardinals7 += 1
                else:
                    cardinalsOut += 1

            if (team == Niners):
                if (playoffs[7] == Niners):
                    niners1 += 1
                elif (playoffs[8] == Niners):
                    niners2 += 1
                elif (playoffs[9] == Niners):
                    niners3 += 1
                elif (playoffs[10] == Niners):
                    niners4 += 1
                elif (playoffs[11] == Niners):
                    niners5 += 1
                elif (playoffs[12] == Niners):
                    niners6 += 1
                elif (playoffs[13] == Niners):
                    niners7 += 1
                else:
                    ninersOut += 1

            if (team == Rams):
                if (playoffs[7] == Rams):
                    rams1 += 1
                elif (playoffs[8] == Rams):
                    rams2 += 1
                elif (playoffs[9] == Rams):
                    rams3 += 1
                elif (playoffs[10] == Rams):
                    rams4 += 1
                elif (playoffs[11] == Rams):
                    rams5 += 1
                elif (playoffs[12] == Rams):
                    rams6 += 1
                elif (playoffs[13] == Rams):
                    rams7 += 1
                else:
                    ramsOut += 1

            if (team == Seahawks):
                if (playoffs[7] == Seahawks):
                    seahawks1 += 1
                elif (playoffs[8] == Seahawks):
                    seahawks2 += 1
                elif (playoffs[9] == Seahawks):
                    seahawks3 += 1
                elif (playoffs[10] == Seahawks):
                    seahawks4 += 1
                elif (playoffs[11] == Seahawks):
                    seahawks5 += 1
                elif (playoffs[12] == Seahawks):
                    seahawks6 += 1
                elif (playoffs[13] == Seahawks):
                    seahawks7 += 1
                else:
                    seahawksOut += 1

        resetStandings()

    #trackScenarios(playoffsList, remSchedules, Patriots, '1')

    billsPlayoffs = (bills1 + bills2 + bills3 + bills4 + bills5 + bills6 + bills7) / 100.0
    billsDiv = (bills1 + bills2 + bills3 + bills4) / 100.0
    billsOut = 100 - billsPlayoffs
    dolphinsPlayoffs = (dolphins1 + dolphins2 + dolphins3 + dolphins4 + dolphins5 + dolphins6 + dolphins7) / 100.0
    dolphinsDiv = (dolphins1 + dolphins2 + dolphins3 + dolphins4) / 100.0
    dolphinsOut = 100 - dolphinsPlayoffs
    jetsPlayoffs = (jets1 + jets2 + jets3 + jets4 + jets5 + jets6 + jets7) / 100.0
    jetsDiv = (jets1 + jets2 + jets3 + jets4) / 100.0
    jetsOut = 100 - jetsPlayoffs
    patriotsPlayoffs = (patriots1 + patriots2 + patriots3 + patriots4 + patriots5 + patriots6 + patriots7) / 100.0
    patriotsDiv = (patriots1 + patriots2 + patriots3 + patriots4) / 100.0
    patriotsOut = 100 - patriotsPlayoffs
    brownsPlayoffs = (browns1 + browns2 + browns3 + browns4 + browns5 + browns6 + browns7) / 100.0
    brownsDiv = (browns1 + browns2 + browns3 + browns4) / 100.0
    brownsOut = 100 - brownsPlayoffs
    bengalsPlayoffs = (bengals1 + bengals2 + bengals3 + bengals4 + bengals5 + bengals6 + bengals7) / 100.0
    bengalsDiv = (bengals1 + bengals2 + bengals3 + bengals4) / 100.0
    bengalsOut = 100 - bengalsPlayoffs
    ravensPlayoffs = (ravens1 + ravens2 + ravens3 + ravens4 + ravens5 + ravens6 + ravens7) / 100.0
    ravensDiv = (ravens1 + ravens2 + ravens3 + ravens4) / 100.0
    ravensOut = 100 - ravensPlayoffs
    steelersPlayoffs = (steelers1 + steelers2 + steelers3 + steelers4 + steelers5 + steelers6 + steelers7) / 100.0
    steelersDiv = (steelers1 + steelers2 + steelers3 + steelers4) / 100.0
    steelersOut = 100 - steelersPlayoffs
    coltsPlayoffs = (colts1 + colts2 + colts3 + colts4 + colts5 + colts6 + colts7) / 100.0
    coltsDiv = (colts1 + colts2 + colts3 + colts4) / 100.0
    coltsOut = 100 - coltsPlayoffs
    jaguarsPlayoffs = (jaguars1 + jaguars2 + jaguars3 + jaguars4 + jaguars5 + jaguars6 + jaguars7) / 100.0
    jaguarsDiv = (jaguars1 + jaguars2 + jaguars3 + jaguars4) / 100.0
    jaguarsOut = 100 - jaguarsPlayoffs
    titansPlayoffs = (titans1 + titans2 + titans3 + titans4 + titans5 + titans6 + titans7) / 100.0
    titansDiv = (titans1 + titans2 + titans3 + titans4) / 100.0
    titansOut = 100 - titansPlayoffs
    texansPlayoffs = (texans1 + texans2 + texans3 + texans4 + texans5 + texans6 + texans7) / 100.0
    texansDiv = (texans1 + texans2 + texans3 + texans4) / 100.0
    texansOut = 100 - texansPlayoffs
    broncosPlayoffs = (broncos1 + broncos2 + broncos3 + broncos4 + broncos5 + broncos6 + broncos7) / 100.0
    broncosDiv = (broncos1 + broncos2 + broncos3 + broncos4) / 100.0
    broncosOut = 100 - broncosPlayoffs
    chargersPlayoffs = (chargers1 + chargers2 + chargers3 + chargers4 + chargers5 + chargers6 + chargers7) / 100.0
    chargersDiv = (chargers1 + chargers2 + chargers3 + chargers4) / 100.0
    chargersOut = 100 - chargersPlayoffs
    chiefsPlayoffs = (chiefs1 + chiefs2 + chiefs3 + chiefs4 + chiefs5 + chiefs6 + chiefs7) / 100.0
    chiefsDiv = (chiefs1 + chiefs2 + chiefs3 + chiefs4) / 100.0
    chiefsOut = 100 - chiefsPlayoffs
    raidersPlayoffs = (raiders1 + raiders2 + raiders3 + raiders4 + raiders5 + raiders6 + raiders7) / 100.0
    raidersDiv = (raiders1 + raiders2 + raiders3 + raiders4) / 100.0
    raidersOut = 100 - raidersPlayoffs
    cowboysPlayoffs = (cowboys1 + cowboys2 + cowboys3 + cowboys4 + cowboys5 + cowboys6 + cowboys7) / 100.0
    cowboysDiv = (cowboys1 + cowboys2 + cowboys3 + cowboys4) / 100.0
    cowboysOut = 100 - cowboysPlayoffs
    commandersPlayoffs = (
                                     commanders1 + commanders2 + commanders3 + commanders4 + commanders5 + commanders6 + commanders7) / 100.0
    commandersDiv = (commanders1 + commanders2 + commanders3 + commanders4) / 100.0
    commandersOut = 100 - commandersPlayoffs
    eaglesPlayoffs = (eagles1 + eagles2 + eagles3 + eagles4 + eagles5 + eagles6 + eagles7) / 100.0
    eaglesDiv = (eagles1 + eagles2 + eagles3 + eagles4) / 100.0
    eaglesOut = 100 - eaglesPlayoffs
    giantsPlayoffs = (giants1 + giants2 + giants3 + giants4 + giants5 + giants6 + giants7) / 100.0
    giantsDiv = (giants1 + giants2 + giants3 + giants4) / 100.0
    giantsOut = 100 - giantsPlayoffs
    bearsPlayoffs = (bears1 + bears2 + bears3 + bears4 + bears5 + bears6 + bears7) / 100.0
    bearsDiv = (bears1 + bears2 + bears3 + bears4) / 100.0
    bearsOut = 100 - bearsPlayoffs
    lionsPlayoffs = (lions1 + lions2 + lions3 + lions4 + lions5 + lions6 + lions7) / 100.0
    lionsDiv = (lions1 + lions2 + lions3 + lions4) / 100.0
    lionsOut = 100 - lionsPlayoffs
    packersPlayoffs = (packers1 + packers2 + packers3 + packers4 + packers5 + packers6 + packers7) / 100.0
    packersDiv = (packers1 + packers2 + packers3 + packers4) / 100.0
    packersOut = 100 - packersPlayoffs
    vikingsPlayoffs = (vikings1 + vikings2 + vikings3 + vikings4 + vikings5 + vikings6 + vikings7) / 100.0
    vikingsDiv = (vikings1 + vikings2 + vikings3 + vikings4) / 100.0
    vikingsOut = 100 - vikingsPlayoffs
    buccaneersPlayoffs = (
                                     buccaneers1 + buccaneers2 + buccaneers3 + buccaneers4 + buccaneers5 + buccaneers6 + buccaneers7) / 100.0
    buccaneersDiv = (buccaneers1 + buccaneers2 + buccaneers3 + buccaneers4) / 100.0
    buccaneersOut = 100 - buccaneersPlayoffs
    falconsPlayoffs = (falcons1 + falcons2 + falcons3 + falcons4 + falcons5 + falcons6 + falcons7) / 100.0
    falconsDiv = (falcons1 + falcons2 + falcons3 + falcons4) / 100.0
    falconsOut = 100 - falconsPlayoffs
    saintsPlayoffs = (saints1 + saints2 + saints3 + saints4 + saints5 + saints6 + saints7) / 100.0
    saintsDiv = (saints1 + saints2 + saints3 + saints4) / 100.0
    saintsOut = 100 - saintsPlayoffs
    panthersPlayoffs = (panthers1 + panthers2 + panthers3 + panthers4 + panthers5 + panthers6 + panthers7) / 100.0
    panthersDiv = (panthers1 + panthers2 + panthers3 + panthers4) / 100.0
    panthersOut = 100 - panthersPlayoffs
    cardinalsPlayoffs = (
                                    cardinals1 + cardinals2 + cardinals3 + cardinals4 + cardinals5 + cardinals6 + cardinals7) / 100.0
    cardinalsDiv = (cardinals1 + cardinals2 + cardinals3 + cardinals4) / 100.0
    cardinalsOut = 100 - cardinalsPlayoffs
    ninersPlayoffs = (niners1 + niners2 + niners3 + niners4 + niners5 + niners6 + niners7) / 100.0
    ninersDiv = (niners1 + niners2 + niners3 + niners4) / 100.0
    ninersOut = 100 - ninersPlayoffs
    ramsPlayoffs = (rams1 + rams2 + rams3 + rams4 + rams5 + rams6 + rams7) / 100.0
    ramsDiv = (rams1 + rams2 + rams3 + rams4) / 100.0
    ramsOut = 100 - ramsPlayoffs
    seahawksPlayoffs = (seahawks1 + seahawks2 + seahawks3 + seahawks4 + seahawks5 + seahawks6 + seahawks7) / 100.0
    seahawksDiv = (seahawks1 + seahawks2 + seahawks3 + seahawks4) / 100.0
    seahawksOut = 100 - seahawksPlayoffs
    '''
    print("bills miss playoffs: " + str(billsOut) + "%")
    print("bills win division:  " + str(billsDiv) + "%")
    print("bills make playoffs: " + str(billsPlayoffs) + "%")
    print("bills 1 seed: " + str((bills1/100.0)) + "%")
    print("bills 2 seed: " + str((bills2 / 100.0)) + "%")
    print("bills 3 seed: " + str((bills3 / 100.0)) + "%")
    print("bills 4 seed: " + str((bills4 / 100.0)) + "%")
    print("bills 5 seed: " + str((bills5 / 100.0)) + "%")
    print("bills 6 seed: " + str((bills6 / 100.0)) + "%")
    print("bills 7 seed: " + str((bills7 / 100.0)) + "%\n")

    print("dolphins miss playoffs: " + str(dolphinsOut) + "%")
    print("dolphins win division:  " + str(dolphinsDiv) + "%")
    print("dolphins make playoffs: " + str(dolphinsPlayoffs) + "%")
    print("dolphins 1 seed: " + str((dolphins1 / 100.0)) + "%")
    print("dolphins 2 seed: " + str((dolphins2 / 100.0)) + "%")
    print("dolphins 3 seed: " + str((dolphins3 / 100.0)) + "%")
    print("dolphins 4 seed: " + str((dolphins4 / 100.0)) + "%")
    print("dolphins 5 seed: " + str((dolphins5 / 100.0)) + "%")
    print("dolphins 6 seed: " + str((dolphins6 / 100.0)) + "%")
    print("dolphins 7 seed: " + str((dolphins7 / 100.0)) + "%\n")

    print("jets miss playoffs: " + str(jetsOut) + "%")
    print("jets win division:  " + str(jetsDiv) + "%")
    print("jets make playoffs: " + str(jetsPlayoffs) + "%")
    print("jets 1 seed: " + str((jets1 / 100.0)) + "%")
    print("jets 2 seed: " + str((jets2 / 100.0)) + "%")
    print("jets 3 seed: " + str((jets3 / 100.0)) + "%")
    print("jets 4 seed: " + str((jets4 / 100.0)) + "%")
    print("jets 5 seed: " + str((jets5 / 100.0)) + "%")
    print("jets 6 seed: " + str((jets6 / 100.0)) + "%")
    print("jets 7 seed: " + str((jets7 / 100.0)) + "%\n")

    print("patriots miss playoffs: " + str(patriotsOut) + "%")
    print("patriots win division:  " + str(patriotsDiv) + "%")
    print("patriots make playoffs: " + str(patriotsPlayoffs) + "%")
    print("patriots 1 seed: " + str((patriots1 / 100.0)) + "%")
    print("patriots 2 seed: " + str((patriots2 / 100.0)) + "%")
    print("patriots 3 seed: " + str((patriots3 / 100.0)) + "%")
    print("patriots 4 seed: " + str((patriots4 / 100.0)) + "%")
    print("patriots 5 seed: " + str((patriots5 / 100.0)) + "%")
    print("patriots 6 seed: " + str((patriots6 / 100.0)) + "%")
    print("patriots 7 seed: " + str((patriots7 / 100.0)) + "%\n")

    print("browns miss playoffs: " + str(brownsOut) + "%")
    print("browns win division:  " + str(brownsDiv) + "%")
    print("browns make playoffs: " + str(brownsPlayoffs) + "%")
    print("browns 1 seed: " + str((browns1 / 100.0)) + "%")
    print("browns 2 seed: " + str((browns2 / 100.0)) + "%")
    print("browns 3 seed: " + str((browns3 / 100.0)) + "%")
    print("browns 4 seed: " + str((browns4 / 100.0)) + "%")
    print("browns 5 seed: " + str((browns5 / 100.0)) + "%")
    print("browns 6 seed: " + str((browns6 / 100.0)) + "%")
    print("browns 7 seed: " + str((browns7 / 100.0)) + "%\n")

    print("bengals miss playoffs: " + str(bengalsOut) + "%")
    print("bengals win division:  " + str(bengalsDiv) + "%")
    print("bengals make playoffs: " + str(bengalsPlayoffs) + "%")
    print("bengals 1 seed: " + str((bengals1 / 100.0)) + "%")
    print("bengals 2 seed: " + str((bengals2 / 100.0)) + "%")
    print("bengals 3 seed: " + str((bengals3 / 100.0)) + "%")
    print("bengals 4 seed: " + str((bengals4 / 100.0)) + "%")
    print("bengals 5 seed: " + str((bengals5 / 100.0)) + "%")
    print("bengals 6 seed: " + str((bengals6 / 100.0)) + "%")
    print("bengals 7 seed: " + str((bengals7 / 100.0)) + "%\n")

    print("ravens miss playoffs: " + str(ravensOut) + "%")
    print("ravens win division:  " + str(ravensDiv) + "%")
    print("ravens make playoffs: " + str(ravensPlayoffs) + "%")
    print("ravens 1 seed: " + str((ravens1 / 100.0)) + "%")
    print("ravens 2 seed: " + str((ravens2 / 100.0)) + "%")
    print("ravens 3 seed: " + str((ravens3 / 100.0)) + "%")
    print("ravens 4 seed: " + str((ravens4 / 100.0)) + "%")
    print("ravens 5 seed: " + str((ravens5 / 100.0)) + "%")
    print("ravens 6 seed: " + str((ravens6 / 100.0)) + "%")
    print("ravens 7 seed: " + str((ravens7 / 100.0)) + "%\n")

    print("steelers miss playoffs: " + str(steelersOut) + "%")
    print("steelers win division:  " + str(steelersDiv) + "%")
    print("steelers make playoffs: " + str(steelersPlayoffs) + "%")
    print("steelers 1 seed: " + str((steelers1 / 100.0)) + "%")
    print("steelers 2 seed: " + str((steelers2 / 100.0)) + "%")
    print("steelers 3 seed: " + str((steelers3 / 100.0)) + "%")
    print("steelers 4 seed: " + str((steelers4 / 100.0)) + "%")
    print("steelers 5 seed: " + str((steelers5 / 100.0)) + "%")
    print("steelers 6 seed: " + str((steelers6 / 100.0)) + "%")
    print("steelers 7 seed: " + str((steelers7 / 100.0)) + "%\n")

    print("colts miss playoffs: " + str(coltsOut) + "%")
    print("colts win division:  " + str(coltsDiv) + "%")
    print("colts make playoffs: " + str(coltsPlayoffs) + "%")
    print("colts 1 seed: " + str((colts1 / 100.0)) + "%")
    print("colts 2 seed: " + str((colts2 / 100.0)) + "%")
    print("colts 3 seed: " + str((colts3 / 100.0)) + "%")
    print("colts 4 seed: " + str((colts4 / 100.0)) + "%")
    print("colts 5 seed: " + str((colts5 / 100.0)) + "%")
    print("colts 6 seed: " + str((colts6 / 100.0)) + "%")
    print("colts 7 seed: " + str((colts7 / 100.0)) + "%\n")

    print("jaguars miss playoffs: " + str(jaguarsOut) + "%")
    print("jaguars win division:  " + str(jaguarsDiv) + "%")
    print("jaguars make playoffs: " + str(jaguarsPlayoffs) + "%")
    print("jaguars 1 seed: " + str((jaguars1 / 100.0)) + "%")
    print("jaguars 2 seed: " + str((jaguars2 / 100.0)) + "%")
    print("jaguars 3 seed: " + str((jaguars3 / 100.0)) + "%")
    print("jaguars 4 seed: " + str((jaguars4 / 100.0)) + "%")
    print("jaguars 5 seed: " + str((jaguars5 / 100.0)) + "%")
    print("jaguars 6 seed: " + str((jaguars6 / 100.0)) + "%")
    print("jaguars 7 seed: " + str((jaguars7 / 100.0)) + "%\n")

    print("titans miss playoffs: " + str(titansOut) + "%")
    print("titans win division:  " + str(titansDiv) + "%")
    print("titans make playoffs: " + str(titansPlayoffs) + "%")
    print("titans 1 seed: " + str((titans1 / 100.0)) + "%")
    print("titans 2 seed: " + str((titans2 / 100.0)) + "%")
    print("titans 3 seed: " + str((titans3 / 100.0)) + "%")
    print("titans 4 seed: " + str((titans4 / 100.0)) + "%")
    print("titans 5 seed: " + str((titans5 / 100.0)) + "%")
    print("titans 6 seed: " + str((titans6 / 100.0)) + "%")
    print("titans 7 seed: " + str((titans7 / 100.0)) + "%\n")

    print("texans miss playoffs: " + str(texansOut) + "%")
    print("texans win division:  " + str(texansDiv) + "%")
    print("texans make playoffs: " + str(texansPlayoffs) + "%")
    print("texans 1 seed: " + str((texans1 / 100.0)) + "%")
    print("texans 2 seed: " + str((texans2 / 100.0)) + "%")
    print("texans 3 seed: " + str((texans3 / 100.0)) + "%")
    print("texans 4 seed: " + str((texans4 / 100.0)) + "%")
    print("texans 5 seed: " + str((texans5 / 100.0)) + "%")
    print("texans 6 seed: " + str((texans6 / 100.0)) + "%")
    print("texans 7 seed: " + str((texans7 / 100.0)) + "%\n")

    print("broncos miss playoffs: " + str(broncosOut) + "%")
    print("broncos win division:  " + str(broncosDiv) + "%")
    print("broncos make playoffs: " + str(broncosPlayoffs) + "%")
    print("broncos 1 seed: " + str((broncos1 / 100.0)) + "%")
    print("broncos 2 seed: " + str((broncos2 / 100.0)) + "%")
    print("broncos 3 seed: " + str((broncos3 / 100.0)) + "%")
    print("broncos 4 seed: " + str((broncos4 / 100.0)) + "%")
    print("broncos 5 seed: " + str((broncos5 / 100.0)) + "%")
    print("broncos 6 seed: " + str((broncos6 / 100.0)) + "%")
    print("broncos 7 seed: " + str((broncos7 / 100.0)) + "%\n")

    print("chargers miss playoffs: " + str(chargersOut) + "%")
    print("chargers win division:  " + str(chargersDiv) + "%")
    print("chargers make playoffs: " + str(chargersPlayoffs) + "%")
    print("chargers 1 seed: " + str((chargers1 / 100.0)) + "%")
    print("chargers 2 seed: " + str((chargers2 / 100.0)) + "%")
    print("chargers 3 seed: " + str((chargers3 / 100.0)) + "%")
    print("chargers 4 seed: " + str((chargers4 / 100.0)) + "%")
    print("chargers 5 seed: " + str((chargers5 / 100.0)) + "%")
    print("chargers 6 seed: " + str((chargers6 / 100.0)) + "%")
    print("chargers 7 seed: " + str((chargers7 / 100.0)) + "%\n")

    print("chiefs miss playoffs: " + str(chiefsOut) + "%")
    print("chiefs win division:  " + str(chiefsDiv) + "%")
    print("chiefs make playoffs: " + str(chiefsPlayoffs) + "%")
    print("chiefs 1 seed: " + str((chiefs1 / 100.0)) + "%")
    print("chiefs 2 seed: " + str((chiefs2 / 100.0)) + "%")
    print("chiefs 3 seed: " + str((chiefs3 / 100.0)) + "%")
    print("chiefs 4 seed: " + str((chiefs4 / 100.0)) + "%")
    print("chiefs 5 seed: " + str((chiefs5 / 100.0)) + "%")
    print("chiefs 6 seed: " + str((chiefs6 / 100.0)) + "%")
    print("chiefs 7 seed: " + str((chiefs7 / 100.0)) + "%\n")

    print("raiders miss playoffs: " + str(raidersOut) + "%")
    print("raiders win division:  " + str(raidersDiv) + "%")
    print("raiders make playoffs: " + str(raidersPlayoffs) + "%")
    print("raiders 1 seed: " + str((raiders1 / 100.0)) + "%")
    print("raiders 2 seed: " + str((raiders2 / 100.0)) + "%")
    print("raiders 3 seed: " + str((raiders3 / 100.0)) + "%")
    print("raiders 4 seed: " + str((raiders4 / 100.0)) + "%")
    print("raiders 5 seed: " + str((raiders5 / 100.0)) + "%")
    print("raiders 6 seed: " + str((raiders6 / 100.0)) + "%")
    print("raiders 7 seed: " + str((raiders7 / 100.0)) + "%\n")

    print("cowboys miss playoffs: " + str(cowboysOut) + "%")
    print("cowboys win division:  " + str(cowboysDiv) + "%")
    print("cowboys make playoffs: " + str(cowboysPlayoffs) + "%")
    print("cowboys 1 seed: " + str((cowboys1 / 100.0)) + "%")
    print("cowboys 2 seed: " + str((cowboys2 / 100.0)) + "%")
    print("cowboys 3 seed: " + str((cowboys3 / 100.0)) + "%")
    print("cowboys 4 seed: " + str((cowboys4 / 100.0)) + "%")
    print("cowboys 5 seed: " + str((cowboys5 / 100.0)) + "%")
    print("cowboys 6 seed: " + str((cowboys6 / 100.0)) + "%")
    print("cowboys 7 seed: " + str((cowboys7 / 100.0)) + "%\n")

    print("commanders miss playoffs: " + str(commandersOut) + "%")
    print("commanders win division:  " + str(commandersDiv) + "%")
    print("commanders make playoffs: " + str(commandersPlayoffs) + "%")
    print("commanders 1 seed: " + str((commanders1 / 100.0)) + "%")
    print("commanders 2 seed: " + str((commanders2 / 100.0)) + "%")
    print("commanders 3 seed: " + str((commanders3 / 100.0)) + "%")
    print("commanders 4 seed: " + str((commanders4 / 100.0)) + "%")
    print("commanders 5 seed: " + str((commanders5 / 100.0)) + "%")
    print("commanders 6 seed: " + str((commanders6 / 100.0)) + "%")
    print("commanders 7 seed: " + str((commanders7 / 100.0)) + "%\n")

    print("eagles miss playoffs: " + str(eaglesOut) + "%")
    print("eagles win division:  " + str(eaglesDiv) + "%")
    print("eagles make playoffs: " + str(eaglesPlayoffs) + "%")
    print("eagles 1 seed: " + str((eagles1 / 100.0)) + "%")
    print("eagles 2 seed: " + str((eagles2 / 100.0)) + "%")
    print("eagles 3 seed: " + str((eagles3 / 100.0)) + "%")
    print("eagles 4 seed: " + str((eagles4 / 100.0)) + "%")
    print("eagles 5 seed: " + str((eagles5 / 100.0)) + "%")
    print("eagles 6 seed: " + str((eagles6 / 100.0)) + "%")
    print("eagles 7 seed: " + str((eagles7 / 100.0)) + "%\n")

    print("giants miss playoffs: " + str(giantsOut) + "%")
    print("giants win division:  " + str(giantsDiv) + "%")
    print("giants make playoffs: " + str(giantsPlayoffs) + "%")
    print("giants 1 seed: " + str((giants1 / 100.0)) + "%")
    print("giants 2 seed: " + str((giants2 / 100.0)) + "%")
    print("giants 3 seed: " + str((giants3 / 100.0)) + "%")
    print("giants 4 seed: " + str((giants4 / 100.0)) + "%")
    print("giants 5 seed: " + str((giants5 / 100.0)) + "%")
    print("giants 6 seed: " + str((giants6 / 100.0)) + "%")
    print("giants 7 seed: " + str((giants7 / 100.0)) + "%\n")

    print("bears miss playoffs: " + str(bearsOut) + "%")
    print("bears win division:  " + str(bearsDiv) + "%")
    print("bears make playoffs: " + str(bearsPlayoffs) + "%")
    print("bears 1 seed: " + str((bears1 / 100.0)) + "%")
    print("bears 2 seed: " + str((bears2 / 100.0)) + "%")
    print("bears 3 seed: " + str((bears3 / 100.0)) + "%")
    print("bears 4 seed: " + str((bears4 / 100.0)) + "%")
    print("bears 5 seed: " + str((bears5 / 100.0)) + "%")
    print("bears 6 seed: " + str((bears6 / 100.0)) + "%")
    print("bears 7 seed: " + str((bears7 / 100.0)) + "%\n")

    print("lions miss playoffs: " + str(lionsOut) + "%")
    print("lions win division:  " + str(lionsDiv) + "%")
    print("lions make playoffs: " + str(lionsPlayoffs) + "%")
    print("lions 1 seed: " + str((lions1 / 100.0)) + "%")
    print("lions 2 seed: " + str((lions2 / 100.0)) + "%")
    print("lions 3 seed: " + str((lions3 / 100.0)) + "%")
    print("lions 4 seed: " + str((lions4 / 100.0)) + "%")
    print("lions 5 seed: " + str((lions5 / 100.0)) + "%")
    print("lions 6 seed: " + str((lions6 / 100.0)) + "%")
    print("lions 7 seed: " + str((lions7 / 100.0)) + "%\n")

    print("packers miss playoffs: " + str(packersOut) + "%")
    print("packers win division:  " + str(packersDiv) + "%")
    print("packers make playoffs: " + str(packersPlayoffs) + "%")
    print("packers 1 seed: " + str((packers1 / 100.0)) + "%")
    print("packers 2 seed: " + str((packers2 / 100.0)) + "%")
    print("packers 3 seed: " + str((packers3 / 100.0)) + "%")
    print("packers 4 seed: " + str((packers4 / 100.0)) + "%")
    print("packers 5 seed: " + str((packers5 / 100.0)) + "%")
    print("packers 6 seed: " + str((packers6 / 100.0)) + "%")
    print("packers 7 seed: " + str((packers7 / 100.0)) + "%\n")

    print("vikings miss playoffs: " + str(vikingsOut) + "%")
    print("vikings win division:  " + str(vikingsDiv) + "%")
    print("vikings make playoffs: " + str(vikingsPlayoffs) + "%")
    print("vikings 1 seed: " + str((vikings1 / 100.0)) + "%")
    print("vikings 2 seed: " + str((vikings2 / 100.0)) + "%")
    print("vikings 3 seed: " + str((vikings3 / 100.0)) + "%")
    print("vikings 4 seed: " + str((vikings4 / 100.0)) + "%")
    print("vikings 5 seed: " + str((vikings5 / 100.0)) + "%")
    print("vikings 6 seed: " + str((vikings6 / 100.0)) + "%")
    print("vikings 7 seed: " + str((vikings7 / 100.0)) + "%\n")

    print("buccaneers miss playoffs: " + str(buccaneersOut) + "%")
    print("buccaneers win division:  " + str(buccaneersDiv) + "%")
    print("buccaneers make playoffs: " + str(buccaneersPlayoffs) + "%")
    print("buccaneers 1 seed: " + str((buccaneers1 / 100.0)) + "%")
    print("buccaneers 2 seed: " + str((buccaneers2 / 100.0)) + "%")
    print("buccaneers 3 seed: " + str((buccaneers3 / 100.0)) + "%")
    print("buccaneers 4 seed: " + str((buccaneers4 / 100.0)) + "%")
    print("buccaneers 5 seed: " + str((buccaneers5 / 100.0)) + "%")
    print("buccaneers 6 seed: " + str((buccaneers6 / 100.0)) + "%")
    print("buccaneers 7 seed: " + str((buccaneers7 / 100.0)) + "%\n")

    print("falcons miss playoffs: " + str(falconsOut) + "%")
    print("falcons win division:  " + str(falconsDiv) + "%")
    print("falcons make playoffs: " + str(falconsPlayoffs) + "%")
    print("falcons 1 seed: " + str((falcons1 / 100.0)) + "%")
    print("falcons 2 seed: " + str((falcons2 / 100.0)) + "%")
    print("falcons 3 seed: " + str((falcons3 / 100.0)) + "%")
    print("falcons 4 seed: " + str((falcons4 / 100.0)) + "%")
    print("falcons 5 seed: " + str((falcons5 / 100.0)) + "%")
    print("falcons 6 seed: " + str((falcons6 / 100.0)) + "%")
    print("falcons 7 seed: " + str((falcons7 / 100.0)) + "%\n")

    print("saints miss playoffs: " + str(saintsOut) + "%")
    print("saints win division:  " + str(saintsDiv) + "%")
    print("saints make playoffs: " + str(saintsPlayoffs) + "%")
    print("saints 1 seed: " + str((saints1 / 100.0)) + "%")
    print("saints 2 seed: " + str((saints2 / 100.0)) + "%")
    print("saints 3 seed: " + str((saints3 / 100.0)) + "%")
    print("saints 4 seed: " + str((saints4 / 100.0)) + "%")
    print("saints 5 seed: " + str((saints5 / 100.0)) + "%")
    print("saints 6 seed: " + str((saints6 / 100.0)) + "%")
    print("saints 7 seed: " + str((saints7 / 100.0)) + "%\n")

    print("panthers miss playoffs: " + str(panthersOut) + "%")
    print("panthers win division:  " + str(panthersDiv) + "%")
    print("panthers make playoffs: " + str(panthersPlayoffs) + "%")
    print("panthers 1 seed: " + str((panthers1 / 100.0)) + "%")
    print("panthers 2 seed: " + str((panthers2 / 100.0)) + "%")
    print("panthers 3 seed: " + str((panthers3 / 100.0)) + "%")
    print("panthers 4 seed: " + str((panthers4 / 100.0)) + "%")
    print("panthers 5 seed: " + str((panthers5 / 100.0)) + "%")
    print("panthers 6 seed: " + str((panthers6 / 100.0)) + "%")
    print("panthers 7 seed: " + str((panthers7 / 100.0)) + "%\n")

    print("cardinals miss playoffs: " + str(cardinalsOut) + "%")
    print("cardinals win division:  " + str(cardinalsDiv) + "%")
    print("cardinals make playoffs: " + str(cardinalsPlayoffs) + "%")
    print("cardinals 1 seed: " + str((cardinals1 / 100.0)) + "%")
    print("cardinals 2 seed: " + str((cardinals2 / 100.0)) + "%")
    print("cardinals 3 seed: " + str((cardinals3 / 100.0)) + "%")
    print("cardinals 4 seed: " + str((cardinals4 / 100.0)) + "%")
    print("cardinals 5 seed: " + str((cardinals5 / 100.0)) + "%")
    print("cardinals 6 seed: " + str((cardinals6 / 100.0)) + "%")
    print("cardinals 7 seed: " + str((cardinals7 / 100.0)) + "%\n")

    print("niners miss playoffs: " + str(ninersOut) + "%")
    print("niners win division:  " + str(ninersDiv) + "%")
    print("niners make playoffs: " + str(ninersPlayoffs) + "%")
    print("niners 1 seed: " + str((niners1 / 100.0)) + "%")
    print("niners 2 seed: " + str((niners2 / 100.0)) + "%")
    print("niners 3 seed: " + str((niners3 / 100.0)) + "%")
    print("niners 4 seed: " + str((niners4 / 100.0)) + "%")
    print("niners 5 seed: " + str((niners5 / 100.0)) + "%")
    print("niners 6 seed: " + str((niners6 / 100.0)) + "%")
    print("niners 7 seed: " + str((niners7 / 100.0)) + "%\n")

    print("rams miss playoffs: " + str(ramsOut) + "%")
    print("rams win division:  " + str(ramsDiv) + "%")
    print("rams make playoffs: " + str(ramsPlayoffs) + "%")
    print("rams 1 seed: " + str((rams1 / 100.0)) + "%")
    print("rams 2 seed: " + str((rams2 / 100.0)) + "%")
    print("rams 3 seed: " + str((rams3 / 100.0)) + "%")
    print("rams 4 seed: " + str((rams4 / 100.0)) + "%")
    print("rams 5 seed: " + str((rams5 / 100.0)) + "%")
    print("rams 6 seed: " + str((rams6 / 100.0)) + "%")
    print("rams 7 seed: " + str((rams7 / 100.0)) + "%\n")

    print("seahawks miss playoffs: " + str(seahawksOut) + "%")
    print("seahawks win division:  " + str(seahawksDiv) + "%")
    print("seahawks make playoffs: " + str(seahawksPlayoffs) + "%")
    print("seahawks 1 seed: " + str((seahawks1 / 100.0)) + "%")
    print("seahawks 2 seed: " + str((seahawks2 / 100.0)) + "%")
    print("seahawks 3 seed: " + str((seahawks3 / 100.0)) + "%")
    print("seahawks 4 seed: " + str((seahawks4 / 100.0)) + "%")
    print("seahawks 5 seed: " + str((seahawks5 / 100.0)) + "%")
    print("seahawks 6 seed: " + str((seahawks6 / 100.0)) + "%")
    print("seahawks 7 seed: " + str((seahawks7 / 100.0)) + "%\n")
    '''
    name_to_id = dict(zip(teamMap['teamName'], teamMap['teamId']))

    odds_data = []

    odds_data.append({
        'teamId': name_to_id['Bills'],
        'division': billsDiv * 2.0,
        'playoffs': billsPlayoffs * 2.0,
        'oneseed': bills1 / 50.0,
        'twoseed': bills2 / 50.0,
        'threeseed': bills3 / 50.0,
        'fourseed': bills4 / 50.0,
        'fiveseed': bills5 / 50.0,
        'sixseed': bills6 / 50.0,
        'sevenseed': bills7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Dolphins'],
        'division': dolphinsDiv * 2.0,
        'playoffs': dolphinsPlayoffs * 2.0,
        'oneseed': dolphins1 / 50.0,
        'twoseed': dolphins2 / 50.0,
        'threeseed': dolphins3 / 50.0,
        'fourseed': dolphins4 / 50.0,
        'fiveseed': dolphins5 / 50.0,
        'sixseed': dolphins6 / 50.0,
        'sevenseed': dolphins7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Jets'],
        'division': jetsDiv * 2.0,
        'playoffs': jetsPlayoffs * 2.0,
        'oneseed': jets1 / 50.0,
        'twoseed': jets2 / 50.0,
        'threeseed': jets3 / 50.0,
        'fourseed': jets4 / 50.0,
        'fiveseed': jets5 / 50.0,
        'sixseed': jets6 / 50.0,
        'sevenseed': jets7 / 50.0
    })
    odds_data.append({
        'teamId': name_to_id['Patriots'],
        'division': patriotsDiv * 2.0,
        'playoffs': patriotsPlayoffs * 2.0,
        'oneseed': patriots1 / 50.0,
        'twoseed': patriots2 / 50.0,
        'threeseed': patriots3 / 50.0,
        'fourseed': patriots4 / 50.0,
        'fiveseed': patriots5 / 50.0,
        'sixseed': patriots6 / 50.0,
        'sevenseed': patriots7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Bengals'],
        'division': bengalsDiv * 2.0,
        'playoffs': bengalsPlayoffs * 2.0,
        'oneseed': bengals1 / 50.0,
        'twoseed': bengals2 / 50.0,
        'threeseed': bengals3 / 50.0,
        'fourseed': bengals4 / 50.0,
        'fiveseed': bengals5 / 50.0,
        'sixseed': bengals6 / 50.0,
        'sevenseed': bengals7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Browns'],
        'division': brownsDiv * 2.0,
        'playoffs': brownsPlayoffs * 2.0,
        'oneseed': browns1 / 50.0,
        'twoseed': browns2 / 50.0,
        'threeseed': browns3 / 50.0,
        'fourseed': browns4 / 50.0,
        'fiveseed': browns5 / 50.0,
        'sixseed': browns6 / 50.0,
        'sevenseed': browns7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Ravens'],
        'division': ravensDiv * 2.0,
        'playoffs': ravensPlayoffs * 2.0,
        'oneseed': ravens1 / 50.0,
        'twoseed': ravens2 / 50.0,
        'threeseed': ravens3 / 50.0,
        'fourseed': ravens4 / 50.0,
        'fiveseed': ravens5 / 50.0,
        'sixseed': ravens6 / 50.0,
        'sevenseed': ravens7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Steelers'],
        'division': steelersDiv * 2.0,
        'playoffs': steelersPlayoffs * 2.0,
        'oneseed': steelers1 / 50.0,
        'twoseed': steelers2 / 50.0,
        'threeseed': steelers3 / 50.0,
        'fourseed': steelers4 / 50.0,
        'fiveseed': steelers5 / 50.0,
        'sixseed': steelers6 / 50.0,
        'sevenseed': steelers7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Colts'],
        'division': coltsDiv * 2.0,
        'playoffs': coltsPlayoffs * 2.0,
        'oneseed': colts1 / 50.0,
        'twoseed': colts2 / 50.0,
        'threeseed': colts3 / 50.0,
        'fourseed': colts4 / 50.0,
        'fiveseed': colts5 / 50.0,
        'sixseed': colts6 / 50.0,
        'sevenseed': colts7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Jaguars'],
        'division': jaguarsDiv * 2.0,
        'playoffs': jaguarsPlayoffs * 2.0,
        'oneseed': jaguars1 / 50.0,
        'twoseed': jaguars2 / 50.0,
        'threeseed': jaguars3 / 50.0,
        'fourseed': jaguars4 / 50.0,
        'fiveseed': jaguars5 / 50.0,
        'sixseed': jaguars6 / 50.0,
        'sevenseed': jaguars7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Titans'],
        'division': titansDiv * 2.0,
        'playoffs': titansPlayoffs * 2.0,
        'oneseed': titans1 / 50.0,
        'twoseed': titans2 / 50.0,
        'threeseed': titans3 / 50.0,
        'fourseed': titans4 / 50.0,
        'fiveseed': titans5 / 50.0,
        'sixseed': titans6 / 50.0,
        'sevenseed': titans7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Texans'],
        'division': texansDiv * 2.0,
        'playoffs': texansPlayoffs * 2.0,
        'oneseed': texans1 / 50.0,
        'twoseed': texans2 / 50.0,
        'threeseed': texans3 / 50.0,
        'fourseed': texans4 / 50.0,
        'fiveseed': texans5 / 50.0,
        'sixseed': texans6 / 50.0,
        'sevenseed': texans7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Chiefs'],
        'division': chiefsDiv * 2.0,
        'playoffs': chiefsPlayoffs * 2.0,
        'oneseed': chiefs1 / 50.0,
        'twoseed': chiefs2 / 50.0,
        'threeseed': chiefs3 / 50.0,
        'fourseed': chiefs4 / 50.0,
        'fiveseed': chiefs5 / 50.0,
        'sixseed': chiefs6 / 50.0,
        'sevenseed': chiefs7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Broncos'],
        'division': broncosDiv * 2.0,
        'playoffs': broncosPlayoffs * 2.0,
        'oneseed': broncos1 / 50.0,
        'twoseed': broncos2 / 50.0,
        'threeseed': broncos3 / 50.0,
        'fourseed': broncos4 / 50.0,
        'fiveseed': broncos5 / 50.0,
        'sixseed': broncos6 / 50.0,
        'sevenseed': broncos7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Chargers'],
        'division': chargersDiv * 2.0,
        'playoffs': chargersPlayoffs * 2.0,
        'oneseed': chargers1 / 50.0,
        'twoseed': chargers2 / 50.0,
        'threeseed': chargers3 / 50.0,
        'fourseed': chargers4 / 50.0,
        'fiveseed': chargers5 / 50.0,
        'sixseed': chargers6 / 50.0,
        'sevenseed': chargers7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Raiders'],
        'division': raidersDiv * 2.0,
        'playoffs': raidersPlayoffs * 2.0,
        'oneseed': raiders1 / 50.0,
        'twoseed': raiders2 / 50.0,
        'threeseed': raiders3 / 50.0,
        'fourseed': raiders4 / 50.0,
        'fiveseed': raiders5 / 50.0,
        'sixseed': raiders6 / 50.0,
        'sevenseed': raiders7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Cowboys'],
        'division': cowboysDiv * 2.0,
        'playoffs': cowboysPlayoffs * 2.0,
        'oneseed': cowboys1 / 50.0,
        'twoseed': cowboys2 / 50.0,
        'threeseed': cowboys3 / 50.0,
        'fourseed': cowboys4 / 50.0,
        'fiveseed': cowboys5 / 50.0,
        'sixseed': cowboys6 / 50.0,
        'sevenseed': cowboys7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Commanders'],
        'division': commandersDiv * 2.0,
        'playoffs': commandersPlayoffs * 2.0,
        'oneseed': commanders1 / 50.0,
        'twoseed': commanders2 / 50.0,
        'threeseed': commanders3 / 50.0,
        'fourseed': commanders4 / 50.0,
        'fiveseed': commanders5 / 50.0,
        'sixseed': commanders6 / 50.0,
        'sevenseed': commanders7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Eagles'],
        'division': eaglesDiv * 2.0,
        'playoffs': eaglesPlayoffs * 2.0,
        'oneseed': eagles1 / 50.0,
        'twoseed': eagles2 / 50.0,
        'threeseed': eagles3 / 50.0,
        'fourseed': eagles4 / 50.0,
        'fiveseed': eagles5 / 50.0,
        'sixseed': eagles6 / 50.0,
        'sevenseed': eagles7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Giants'],
        'division': giantsDiv * 2.0,
        'playoffs': giantsPlayoffs * 2.0,
        'oneseed': giants1 / 50.0,
        'twoseed': giants2 / 50.0,
        'threeseed': giants3 / 50.0,
        'fourseed': giants4 / 50.0,
        'fiveseed': giants5 / 50.0,
        'sixseed': giants6 / 50.0,
        'sevenseed': giants7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Bears'],
        'division': bearsDiv * 2.0,
        'playoffs': bearsPlayoffs * 2.0,
        'oneseed': bears1 / 50.0,
        'twoseed': bears2 / 50.0,
        'threeseed': bears3 / 50.0,
        'fourseed': bears4 / 50.0,
        'fiveseed': bears5 / 50.0,
        'sixseed': bears6 / 50.0,
        'sevenseed': bears7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Lions'],
        'division': lionsDiv * 2.0,
        'playoffs': lionsPlayoffs * 2.0,
        'oneseed': lions1 / 50.0,
        'twoseed': lions2 / 50.0,
        'threeseed': lions3 / 50.0,
        'fourseed': lions4 / 50.0,
        'fiveseed': lions5 / 50.0,
        'sixseed': lions6 / 50.0,
        'sevenseed': lions7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Packers'],
        'division': packersDiv * 2.0,
        'playoffs': packersPlayoffs * 2.0,
        'oneseed': packers1 / 50.0,
        'twoseed': packers2 / 50.0,
        'threeseed': packers3 / 50.0,
        'fourseed': packers4 / 50.0,
        'fiveseed': packers5 / 50.0,
        'sixseed': packers6 / 50.0,
        'sevenseed': packers7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Vikings'],
        'division': vikingsDiv * 2.0,
        'playoffs': vikingsPlayoffs * 2.0,
        'oneseed': vikings1 / 50.0,
        'twoseed': vikings2 / 50.0,
        'threeseed': vikings3 / 50.0,
        'fourseed': vikings4 / 50.0,
        'fiveseed': vikings5 / 50.0,
        'sixseed': vikings6 / 50.0,
        'sevenseed': vikings7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Buccaneers'],
        'division': buccaneersDiv * 2.0,
        'playoffs': buccaneersPlayoffs * 2.0,
        'oneseed': buccaneers1 / 50.0,
        'twoseed': buccaneers2 / 50.0,
        'threeseed': buccaneers3 / 50.0,
        'fourseed': buccaneers4 / 50.0,
        'fiveseed': buccaneers5 / 50.0,
        'sixseed': buccaneers6 / 50.0,
        'sevenseed': buccaneers7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Falcons'],
        'division': falconsDiv * 2.0,
        'playoffs': falconsPlayoffs * 2.0,
        'oneseed': falcons1 / 50.0,
        'twoseed': falcons2 / 50.0,
        'threeseed': falcons3 / 50.0,
        'fourseed': falcons4 / 50.0,
        'fiveseed': falcons5 / 50.0,
        'sixseed': falcons6 / 50.0,
        'sevenseed': falcons7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Panthers'],
        'division': panthersDiv * 2.0,
        'playoffs': panthersPlayoffs * 2.0,
        'oneseed': panthers1 / 50.0,
        'twoseed': panthers2 / 50.0,
        'threeseed': panthers3 / 50.0,
        'fourseed': panthers4 / 50.0,
        'fiveseed': panthers5 / 50.0,
        'sixseed': panthers6 / 50.0,
        'sevenseed': panthers7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Saints'],
        'division': saintsDiv * 2.0,
        'playoffs': saintsPlayoffs * 2.0,
        'oneseed': saints1 / 50.0,
        'twoseed': saints2 / 50.0,
        'threeseed': saints3 / 50.0,
        'fourseed': saints4 / 50.0,
        'fiveseed': saints5 / 50.0,
        'sixseed': saints6 / 50.0,
        'sevenseed': saints7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Cardinals'],
        'division': cardinalsDiv * 2.0,
        'playoffs': cardinalsPlayoffs * 2.0,
        'oneseed': cardinals1 / 50.0,
        'twoseed': cardinals2 / 50.0,
        'threeseed': cardinals3 / 50.0,
        'fourseed': cardinals4 / 50.0,
        'fiveseed': cardinals5 / 50.0,
        'sixseed': cardinals6 / 50.0,
        'sevenseed': cardinals7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['49ers'],
        'division': ninersDiv * 2.0,
        'playoffs': ninersPlayoffs * 2.0,
        'oneseed': niners1 / 50.0,
        'twoseed': niners2 / 50.0,
        'threeseed': niners3 / 50.0,
        'fourseed': niners4 / 50.0,
        'fiveseed': niners5 / 50.0,
        'sixseed': niners6 / 50.0,
        'sevenseed': niners7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Rams'],
        'division': ramsDiv * 2.0,
        'playoffs': ramsPlayoffs * 2.0,
        'oneseed': rams1 / 50.0,
        'twoseed': rams2 / 50.0,
        'threeseed': rams3 / 50.0,
        'fourseed': rams4 / 50.0,
        'fiveseed': rams5 / 50.0,
        'sixseed': rams6 / 50.0,
        'sevenseed': rams7 / 50.0
    })


    odds_data.append({
        'teamId': name_to_id['Seahawks'],
        'division': seahawksDiv * 2.0,
        'playoffs': seahawksPlayoffs * 2.0,
        'oneseed': seahawks1 / 50.0,
        'twoseed': seahawks2 / 50.0,
        'threeseed': seahawks3 / 50.0,
        'fourseed': seahawks4 / 50.0,
        'fiveseed': seahawks5 / 50.0,
        'sixseed': seahawks6 / 50.0,
        'sevenseed': seahawks7 / 50.0
    })







    supabase.table('PlayoffOdds').delete().neq('teamId', -1).execute() # Clear all rows
    supabase.table('PlayoffOdds').insert(odds_data).execute()

    print("Playoff odds inserted into Supabase successfully.")



    
def simulate_odds(games_json):
    # Convert JSON to DataFrame
    games_df = pd.DataFrame(games_json)

    # Map team IDs to team names
    games_df['homeTeam'] = games_df['homeTeamId'].map(dict(zip(teamMap['teamId'], teamMap['teamName'])))
    games_df['awayTeam'] = games_df['awayTeamId'].map(dict(zip(teamMap['teamId'], teamMap['teamName'])))

    # Drop ID columns
    games_df = games_df.drop(['homeTeamId', 'awayTeamId'], axis=1)


    df = games_df
    #print (df)
    fillSchedules(df)


    bills1, bills2, bills3, bills4, bills5, bills6, bills7, billsOut = 0, 0, 0, 0, 0, 0, 0, 0
    dolphins1, dolphins2, dolphins3, dolphins4, dolphins5, dolphins6, dolphins7, dolphinsOut = 0, 0, 0, 0, 0, 0, 0, 0
    jets1, jets2, jets3, jets4, jets5, jets6, jets7, jetsOut = 0, 0, 0, 0, 0, 0, 0, 0
    patriots1, patriots2, patriots3, patriots4, patriots5, patriots6, patriots7, patriotsOut = 0, 0, 0, 0, 0, 0, 0, 0
    browns1, browns2, browns3, browns4, browns5, browns6, browns7, brownsOut = 0, 0, 0, 0, 0, 0, 0, 0
    bengals1, bengals2, bengals3, bengals4, bengals5, bengals6, bengals7, bengalsOut = 0, 0, 0, 0, 0, 0, 0, 0
    ravens1, ravens2, ravens3, ravens4, ravens5, ravens6, ravens7, ravensOut = 0, 0, 0, 0, 0, 0, 0, 0
    steelers1, steelers2, steelers3, steelers4, steelers5, steelers6, steelers7, steelersOut = 0, 0, 0, 0, 0, 0, 0, 0
    colts1, colts2, colts3, colts4, colts5, colts6, colts7, coltsOut = 0, 0, 0, 0, 0, 0, 0, 0
    jaguars1, jaguars2, jaguars3, jaguars4, jaguars5, jaguars6, jaguars7, jaguarsOut = 0, 0, 0, 0, 0, 0, 0, 0
    titans1, titans2, titans3, titans4, titans5, titans6, titans7, titansOut = 0, 0, 0, 0, 0, 0, 0, 0
    texans1, texans2, texans3, texans4, texans5, texans6, texans7, texansOut = 0, 0, 0, 0, 0, 0, 0, 0
    broncos1, broncos2, broncos3, broncos4, broncos5, broncos6, broncos7, broncosOut = 0, 0, 0, 0, 0, 0, 0, 0
    chargers1, chargers2, chargers3, chargers4, chargers5, chargers6, chargers7, chargersOut = 0, 0, 0, 0, 0, 0, 0, 0
    chiefs1, chiefs2, chiefs3, chiefs4, chiefs5, chiefs6, chiefs7, chiefsOut = 0, 0, 0, 0, 0, 0, 0, 0
    raiders1, raiders2, raiders3, raiders4, raiders5, raiders6, raiders7, raidersOut = 0, 0, 0, 0, 0, 0, 0, 0
    commanders1, commanders2, commanders3, commanders4, commanders5, commanders6, commanders7, commandersOut = 0, 0, 0, 0, 0, 0, 0, 0
    cowboys1, cowboys2, cowboys3, cowboys4, cowboys5, cowboys6, cowboys7, cowboysOut = 0, 0, 0, 0, 0, 0, 0, 0
    eagles1, eagles2, eagles3, eagles4, eagles5, eagles6, eagles7, eaglesOut = 0, 0, 0, 0, 0, 0, 0, 0
    giants1, giants2, giants3, giants4, giants5, giants6, giants7, giantsOut = 0, 0, 0, 0, 0, 0, 0, 0
    bears1, bears2, bears3, bears4, bears5, bears6, bears7, bearsOut = 0, 0, 0, 0, 0, 0, 0, 0
    lions1, lions2, lions3, lions4, lions5, lions6, lions7, lionsOut = 0, 0, 0, 0, 0, 0, 0, 0
    packers1, packers2, packers3, packers4, packers5, packers6, packers7, packersOut = 0, 0, 0, 0, 0, 0, 0, 0
    vikings1, vikings2, vikings3, vikings4, vikings5, vikings6, vikings7, vikingsOut = 0, 0, 0, 0, 0, 0, 0, 0
    buccaneers1, buccaneers2, buccaneers3, buccaneers4, buccaneers5, buccaneers6, buccaneers7, buccaneersOut = 0, 0, 0, 0, 0, 0, 0, 0
    falcons1, falcons2, falcons3, falcons4, falcons5, falcons6, falcons7, falconsOut = 0, 0, 0, 0, 0, 0, 0, 0
    saints1, saints2, saints3, saints4, saints5, saints6, saints7, saintsOut = 0, 0, 0, 0, 0, 0, 0, 0
    panthers1, panthers2, panthers3, panthers4, panthers5, panthers6, panthers7, panthersOut = 0, 0, 0, 0, 0, 0, 0, 0
    cardinals1, cardinals2, cardinals3, cardinals4, cardinals5, cardinals6, cardinals7, cardinalsOut = 0, 0, 0, 0, 0, 0, 0, 0
    niners1, niners2, niners3, niners4, niners5, niners6, niners7, ninersOut = 0, 0, 0, 0, 0, 0, 0, 0
    rams1, rams2, rams3, rams4, rams5, rams6, rams7, ramsOut = 0, 0, 0, 0, 0, 0, 0, 0
    seahawks1, seahawks2, seahawks3, seahawks4, seahawks5, seahawks6, seahawks7, seahawksOut = 0, 0, 0, 0, 0, 0, 0, 0


    playoffsList = []
    #remSchedules= []
    for i in range(1000):
        remSchedule = []
        for i in range(17):
            if (not Bills.results[i] == 'W' and not Bills.results[i] == 'L' and not Bills.results[i] == 'T'):
                game = Bills.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Bills')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Bills.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Bills.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Bills.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')
        #print (Bills.matchups)
        #print (Bills.results)

        for i in range(17):
            if (not Dolphins.results[i] == 'W' and not Dolphins.results[i] == 'L' and not Dolphins.results[i] == 'T'):
                game = Dolphins.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Dolphins')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Dolphins.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Dolphins.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Dolphins.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Jets.results[i] == 'W' and not Jets.results[i] == 'L' and not Jets.results[i] == 'T'):
                game = Jets.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Jets')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Jets.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Jets.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Jets.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Patriots.results[i] == 'W' and not Patriots.results[i] == 'L' and not Patriots.results[i] == 'T'):
                game = Patriots.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Patriots')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Patriots.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Patriots.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Patriots.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Browns.results[i] == 'W' and not Browns.results[i] == 'L' and not Browns.results[i] == 'T'):
                game = Browns.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Browns')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Browns.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Browns.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Browns.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Bengals.results[i] == 'W' and not Bengals.results[i] == 'L' and not Bengals.results[i] == 'T'):
                game = Bengals.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Bengals')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Bengals.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Bengals.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Bengals.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Ravens.results[i] == 'W' and not Ravens.results[i] == 'L' and not Ravens.results[i] == 'T'):
                game = Ravens.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Ravens')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Ravens.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Ravens.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Ravens.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Steelers.results[i] == 'W' and not Steelers.results[i] == 'L' and not Steelers.results[i] == 'T'):
                game = Steelers.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Steelers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Steelers.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Steelers.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Steelers.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Colts.results[i] == 'W' and not Colts.results[i] == 'L' and not Colts.results[i] == 'T'):
                game = Colts.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Colts')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Colts.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Colts.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Colts.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Jaguars.results[i] == 'W' and not Jaguars.results[i] == 'L' and not Jaguars.results[i] == 'T'):
                game = Jaguars.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Jaguars')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Jaguars.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Jaguars.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Jaguars.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Titans.results[i] == 'W' and not Titans.results[i] == 'L' and not Titans.results[i] == 'T'):
                game = Titans.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Titans')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Titans.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Titans.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Titans.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Texans.results[i] == 'W' and not Texans.results[i] == 'L' and not Texans.results[i] == 'T'):
                game = Texans.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Texans')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Texans.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Texans.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Texans.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Broncos.results[i] == 'W' and not Broncos.results[i] == 'L' and not Broncos.results[i] == 'T'):
                game = Broncos.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Broncos')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Broncos.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Broncos.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Broncos.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Chargers.results[i] == 'W' and not Chargers.results[i] == 'L' and not Chargers.results[i] == 'T'):
                game = Chargers.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Chargers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Chargers.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Chargers.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Chargers.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Chiefs.results[i] == 'W' and not Chiefs.results[i] == 'L' and not Chiefs.results[i] == 'T'):
                game = Chiefs.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Chiefs')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Chiefs.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Chiefs.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Chiefs.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Raiders.results[i] == 'W' and not Raiders.results[i] == 'L' and not Raiders.results[i] == 'T'):
                game = Raiders.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Raiders')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Raiders.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Raiders.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Raiders.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Cowboys.results[i] == 'W' and not Cowboys.results[i] == 'L' and not Cowboys.results[i] == 'T'):
                game = Cowboys.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Cowboys')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Cowboys.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Cowboys.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Cowboys.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Commanders.results[i] == 'W' and not Commanders.results[i] == 'L' and not Commanders.results[i] == 'T'):
                game = Commanders.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Commanders')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Commanders.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Commanders.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Commanders.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Eagles.results[i] == 'W' and not Eagles.results[i] == 'L' and not Eagles.results[i] == 'T'):
                game = Eagles.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Eagles')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Eagles.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Eagles.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Eagles.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Giants.results[i] == 'W' and not Giants.results[i] == 'L' and not Giants.results[i] == 'T'):
                game = Giants.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Giants')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Giants.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Giants.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Giants.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Bears.results[i] == 'W' and not Bears.results[i] == 'L' and not Bears.results[i] == 'T'):
                game = Bears.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Bears')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Bears.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Bears.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Bears.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Lions.results[i] == 'W' and not Lions.results[i] == 'L' and not Lions.results[i] == 'T'):
                game = Lions.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Lions')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Lions.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Lions.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Lions.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Packers.results[i] == 'W' and not Packers.results[i] == 'L' and not Packers.results[i] == 'T'):
                game = Packers.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Packers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Packers.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Packers.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Packers.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Vikings.results[i] == 'W' and not Vikings.results[i] == 'L' and not Vikings.results[i] == 'T'):
                game = Vikings.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Vikings')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Vikings.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Vikings.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Vikings.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Buccaneers.results[i] == 'W' and not Buccaneers.results[i] == 'L' and not Buccaneers.results[i] == 'T'):
                game = Buccaneers.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Buccaneers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Buccaneers.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Buccaneers.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Buccaneers.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Falcons.results[i] == 'W' and not Falcons.results[i] == 'L' and not Falcons.results[i] == 'T'):
                game = Falcons.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Falcons')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Falcons.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Falcons.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Falcons.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Saints.results[i] == 'W' and not Saints.results[i] == 'L' and not Saints.results[i] == 'T'):
                game = Saints.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Saints')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Saints.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Saints.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Saints.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Panthers.results[i] == 'W' and not Panthers.results[i] == 'L' and not Panthers.results[i] == 'T'):
                game = Panthers.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Panthers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Panthers.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Panthers.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Panthers.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Cardinals.results[i] == 'W' and not Cardinals.results[i] == 'L' and not Cardinals.results[i] == 'T'):
                game = Cardinals.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Cardinals')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Cardinals.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Cardinals.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Cardinals.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Niners.results[i] == 'W' and not Niners.results[i] == 'L' and not Niners.results[i] == 'T'):
                game = Niners.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('49ers')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Niners.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Niners.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Niners.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Rams.results[i] == 'W' and not Rams.results[i] == 'L' and not Rams.results[i] == 'T'):
                game = Rams.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Rams')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Rams.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Rams.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Rams.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        for i in range(17):
            if (not Seahawks.results[i] == 'W' and not Seahawks.results[i] == 'L' and not Seahawks.results[i] == 'T'):
                game = Seahawks.matchups[i]
                opponent = findTeam(game)
                remSchedule.append('Seahawks')
                remSchedule.append(game)
                winChance = 0.0
                winDifference = Seahawks.getWinPercentage() - opponent.getWinPercentage()
                if (winDifference == 0):
                    winChance = 0.5
                elif (winDifference < 0.83):
                    winChance = 0.5 + (winDifference * 0.6)
                else:
                    winChance = 0.99
                round(winChance, 2)
                winChance *= 100
                rand = random.randint(1, 100)
                if (rand <= winChance):
                    Seahawks.results[i] = 'W'
                    opponent.results[i] = 'L'
                    remSchedule.append('W')
                else:
                    Seahawks.results[i] = 'L'
                    opponent.results[i] = 'W'
                    remSchedule.append('L')

        playoffs = playoffStandings()
        playoffsList.append(playoffs)
        #remSchedules.append(remSchedule)
        for team in playoffs:
            if (team == Bills):
                if (playoffs[0] == Bills):
                    bills1 += 1
                elif (playoffs[1] == Bills):
                    bills2 += 1
                elif (playoffs[2] == Bills):
                    bills3 += 1
                elif (playoffs[3] == Bills):
                    bills4 += 1
                elif (playoffs[4] == Bills):
                    bills5 += 1
                elif (playoffs[5] == Bills):
                    bills6 += 1
                elif (playoffs[6] == Bills):
                    bills7 += 1
                else:
                    billsOut += 1

            if (team == Dolphins):
                if (playoffs[0] == Dolphins):
                    dolphins1 += 1
                elif (playoffs[1] == Dolphins):
                    dolphins2 += 1
                elif (playoffs[2] == Dolphins):
                    dolphins3 += 1
                elif (playoffs[3] == Dolphins):
                    dolphins4 += 1
                elif (playoffs[4] == Dolphins):
                    dolphins5 += 1
                elif (playoffs[5] == Dolphins):
                    dolphins6 += 1
                elif (playoffs[6] == Dolphins):
                    dolphins7 += 1
                else:
                    dolphinsOut += 1
            if (team == Jets):
                if (playoffs[0] == Jets):
                    jets1 += 1
                elif (playoffs[1] == Jets):
                    jets2 += 1
                elif (playoffs[2] == Jets):
                    jets3 += 1
                elif (playoffs[3] == Jets):
                    jets4 += 1
                elif (playoffs[4] == Jets):
                    jets5 += 1
                elif (playoffs[5] == Jets):
                    jets6 += 1
                elif (playoffs[6] == Jets):
                    jets7 += 1
                else:
                    jetsOut += 1

            if (team == Patriots):
                if (playoffs[0] == Patriots):
                    patriots1 += 1
                elif (playoffs[1] == Patriots):
                    patriots2 += 1
                elif (playoffs[2] == Patriots):
                    patriots3 += 1
                elif (playoffs[3] == Patriots):
                    patriots4 += 1
                elif (playoffs[4] == Patriots):
                    patriots5 += 1
                elif (playoffs[5] == Patriots):
                    patriots6 += 1
                elif (playoffs[6] == Patriots):
                    patriots7 += 1
                else:
                    patriotsOut += 1

            if (team == Browns):
                if (playoffs[0] == Browns):
                    browns1 += 1
                elif (playoffs[1] == Browns):
                    browns2 += 1
                elif (playoffs[2] == Browns):
                    browns3 += 1
                elif (playoffs[3] == Browns):
                    browns4 += 1
                elif (playoffs[4] == Browns):
                    browns5 += 1
                elif (playoffs[5] == Browns):
                    browns6 += 1
                elif (playoffs[6] == Browns):
                    browns7 += 1
                else:
                    brownsOut += 1

            if (team == Bengals):
                if (playoffs[0] == Bengals):
                    bengals1 += 1
                elif (playoffs[1] == Bengals):
                    bengals2 += 1
                elif (playoffs[2] == Bengals):
                    bengals3 += 1
                elif (playoffs[3] == Bengals):
                    bengals4 += 1
                elif (playoffs[4] == Bengals):
                    bengals5 += 1
                elif (playoffs[5] == Bengals):
                    bengals6 += 1
                elif (playoffs[6] == Bengals):
                    bengals7 += 1
                else:
                    bengalsOut += 1

            if (team == Ravens):
                if (playoffs[0] == Ravens):
                    ravens1 += 1
                elif (playoffs[1] == Ravens):
                    ravens2 += 1
                elif (playoffs[2] == Ravens):
                    ravens3 += 1
                elif (playoffs[3] == Ravens):
                    ravens4 += 1
                elif (playoffs[4] == Ravens):
                    ravens5 += 1
                elif (playoffs[5] == Ravens):
                    ravens6 += 1
                elif (playoffs[6] == Ravens):
                    ravens7 += 1
                else:
                    ravensOut += 1

            if (team == Steelers):
                if (playoffs[0] == Steelers):
                    steelers1 += 1
                elif (playoffs[1] == Steelers):
                    steelers2 += 1
                elif (playoffs[2] == Steelers):
                    steelers3 += 1
                elif (playoffs[3] == Steelers):
                    steelers4 += 1
                elif (playoffs[4] == Steelers):
                    steelers5 += 1
                elif (playoffs[5] == Steelers):
                    steelers6 += 1
                elif (playoffs[6] == Steelers):
                    steelers7 += 1
                else:
                    steelersOut += 1

            if (team == Colts):
                if (playoffs[0] == Colts):
                    colts1 += 1
                elif (playoffs[1] == Colts):
                    colts2 += 1
                elif (playoffs[2] == Colts):
                    colts3 += 1
                elif (playoffs[3] == Colts):
                    colts4 += 1
                elif (playoffs[4] == Colts):
                    colts5 += 1
                elif (playoffs[5] == Colts):
                    colts6 += 1
                elif (playoffs[6] == Colts):
                    colts7 += 1
                else:
                    coltsOut += 1

            if (team == Jaguars):
                if (playoffs[0] == Jaguars):
                    jaguars1 += 1
                elif (playoffs[1] == Jaguars):
                    jaguars2 += 1
                elif (playoffs[2] == Jaguars):
                    jaguars3 += 1
                elif (playoffs[3] == Jaguars):
                    jaguars4 += 1
                elif (playoffs[4] == Jaguars):
                    jaguars5 += 1
                elif (playoffs[5] == Jaguars):
                    jaguars6 += 1
                elif (playoffs[6] == Jaguars):
                    jaguars7 += 1
                else:
                    jaguarsOut += 1

            if (team == Titans):
                if (playoffs[0] == Titans):
                    titans1 += 1
                elif (playoffs[1] == Titans):
                    titans2 += 1
                elif (playoffs[2] == Titans):
                    titans3 += 1
                elif (playoffs[3] == Titans):
                    titans4 += 1
                elif (playoffs[4] == Titans):
                    titans5 += 1
                elif (playoffs[5] == Titans):
                    titans6 += 1
                elif (playoffs[6] == Titans):
                    titans7 += 1
                else:
                    titansOut += 1

            if (team == Texans):
                if (playoffs[0] == Texans):
                    texans1 += 1
                elif (playoffs[1] == Texans):
                    texans2 += 1
                elif (playoffs[2] == Texans):
                    texans3 += 1
                elif (playoffs[3] == Texans):
                    texans4 += 1
                elif (playoffs[4] == Texans):
                    texans5 += 1
                elif (playoffs[5] == Texans):
                    texans6 += 1
                elif (playoffs[6] == Texans):
                    texans7 += 1
                else:
                    texansOut += 1

            if (team == Broncos):
                if (playoffs[0] == Broncos):
                    broncos1 += 1
                elif (playoffs[1] == Broncos):
                    broncos2 += 1
                elif (playoffs[2] == Broncos):
                    broncos3 += 1
                elif (playoffs[3] == Broncos):
                    broncos4 += 1
                elif (playoffs[4] == Broncos):
                    broncos5 += 1
                elif (playoffs[5] == Broncos):
                    broncos6 += 1
                elif (playoffs[6] == Broncos):
                    broncos7 += 1
                else:
                    broncosOut += 1

            if (team == Chargers):
                if (playoffs[0] == Chargers):
                    chargers1 += 1
                elif (playoffs[1] == Chargers):
                    chargers2 += 1
                elif (playoffs[2] == Chargers):
                    chargers3 += 1
                elif (playoffs[3] == Chargers):
                    chargers4 += 1
                elif (playoffs[4] == Chargers):
                    chargers5 += 1
                elif (playoffs[5] == Chargers):
                    chargers6 += 1
                elif (playoffs[6] == Chargers):
                    chargers7 += 1
                else:
                    chargersOut += 1

            if (team == Chiefs):
                if (playoffs[0] == Chiefs):
                    chiefs1 += 1
                elif (playoffs[1] == Chiefs):
                    chiefs2 += 1
                elif (playoffs[2] == Chiefs):
                    chiefs3 += 1
                elif (playoffs[3] == Chiefs):
                    chiefs4 += 1
                elif (playoffs[4] == Chiefs):
                    chiefs5 += 1
                elif (playoffs[5] == Chiefs):
                    chiefs6 += 1
                elif (playoffs[6] == Chiefs):
                    chiefs7 += 1
                else:
                    chiefsOut += 1

            if (team == Raiders):
                if (playoffs[0] == Raiders):
                    raiders1 += 1
                elif (playoffs[1] == Raiders):
                    raiders2 += 1
                elif (playoffs[2] == Raiders):
                    raiders3 += 1
                elif (playoffs[3] == Raiders):
                    raiders4 += 1
                elif (playoffs[4] == Raiders):
                    raiders5 += 1
                elif (playoffs[5] == Raiders):
                    raiders6 += 1
                elif (playoffs[6] == Raiders):
                    raiders7 += 1
                else:
                    raidersOut += 1

            if (team == Cowboys):
                if (playoffs[7] == Cowboys):
                    cowboys1 += 1
                elif (playoffs[8] == Cowboys):
                    cowboys2 += 1
                elif (playoffs[9] == Cowboys):
                    cowboys3 += 1
                elif (playoffs[10] == Cowboys):
                    cowboys4 += 1
                elif (playoffs[11] == Cowboys):
                    cowboys5 += 1
                elif (playoffs[12] == Cowboys):
                    cowboys6 += 1
                elif (playoffs[13] == Cowboys):
                    cowboys7 += 1
                else:
                    cowboysOut += 1

            if (team == Commanders):
                if (playoffs[7] == Commanders):
                    commanders1 += 1
                elif (playoffs[8] == Commanders):
                    commanders2 += 1
                elif (playoffs[9] == Commanders):
                    commanders3 += 1
                elif (playoffs[10] == Commanders):
                    commanders4 += 1
                elif (playoffs[11] == Commanders):
                    commanders5 += 1
                elif (playoffs[12] == Commanders):
                    commanders6 += 1
                elif (playoffs[13] == Commanders):
                    commanders7 += 1
                else:
                    commandersOut += 1

            if (team == Eagles):
                if (playoffs[7] == Eagles):
                    eagles1 += 1
                elif (playoffs[8] == Eagles):
                    eagles2 += 1
                elif (playoffs[9] == Eagles):
                    eagles3 += 1
                elif (playoffs[10] == Eagles):
                    eagles4 += 1
                elif (playoffs[11] == Eagles):
                    eagles5 += 1
                elif (playoffs[12] == Eagles):
                    eagles6 += 1
                elif (playoffs[13] == Eagles):
                    eagles7 += 1
                else:
                    eaglesOut += 1

            if (team == Giants):
                if (playoffs[7] == Giants):
                    giants1 += 1
                elif (playoffs[8] == Giants):
                    giants2 += 1
                elif (playoffs[9] == Giants):
                    giants3 += 1
                elif (playoffs[10] == Giants):
                    giants4 += 1
                elif (playoffs[11] == Giants):
                    giants5 += 1
                elif (playoffs[12] == Giants):
                    giants6 += 1
                elif (playoffs[13] == Giants):
                    giants7 += 1
                else:
                    giantsOut += 1

            if (team == Bears):
                if (playoffs[7] == Bears):
                    bears1 += 1
                elif (playoffs[8] == Bears):
                    bears2 += 1
                elif (playoffs[9] == Bears):
                    bears3 += 1
                elif (playoffs[10] == Bears):
                    bears4 += 1
                elif (playoffs[11] == Bears):
                    bears5 += 1
                elif (playoffs[12] == Bears):
                    bears6 += 1
                elif (playoffs[13] == Bears):
                    bears7 += 1
                else:
                    bearsOut += 1

            if (team == Lions):
                if (playoffs[7] == Lions):
                    lions1 += 1
                elif (playoffs[8] == Lions):
                    lions2 += 1
                elif (playoffs[9] == Lions):
                    lions3 += 1
                elif (playoffs[10] == Lions):
                    lions4 += 1
                elif (playoffs[11] == Lions):
                    lions5 += 1
                elif (playoffs[12] == Lions):
                    lions6 += 1
                elif (playoffs[13] == Lions):
                    lions7 += 1
                else:
                    lionsOut += 1

            if (team == Packers):
                if (playoffs[7] == Packers):
                    packers1 += 1
                elif (playoffs[8] == Packers):
                    packers2 += 1
                elif (playoffs[9] == Packers):
                    packers3 += 1
                elif (playoffs[10] == Packers):
                    packers4 += 1
                elif (playoffs[11] == Packers):
                    packers5 += 1
                elif (playoffs[12] == Packers):
                    packers6 += 1
                elif (playoffs[13] == Packers):
                    packers7 += 1
                else:
                    packersOut += 1

            if (team == Vikings):
                if (playoffs[7] == Vikings):
                    vikings1 += 1
                elif (playoffs[8] == Vikings):
                    vikings2 += 1
                elif (playoffs[9] == Vikings):
                    vikings3 += 1
                elif (playoffs[10] == Vikings):
                    vikings4 += 1
                elif (playoffs[11] == Vikings):
                    vikings5 += 1
                elif (playoffs[12] == Vikings):
                    vikings6 += 1
                elif (playoffs[13] == Vikings):
                    vikings7 += 1
                else:
                    vikingsOut += 1

            if (team == Buccaneers):
                if (playoffs[7] == Buccaneers):
                    buccaneers1 += 1
                elif (playoffs[8] == Buccaneers):
                    buccaneers2 += 1
                elif (playoffs[9] == Buccaneers):
                    buccaneers3 += 1
                elif (playoffs[10] == Buccaneers):
                    buccaneers4 += 1
                elif (playoffs[11] == Buccaneers):
                    buccaneers5 += 1
                elif (playoffs[12] == Buccaneers):
                    buccaneers6 += 1
                elif (playoffs[13] == Buccaneers):
                    buccaneers7 += 1
                else:
                    buccaneersOut += 1

            if (team == Falcons):
                if (playoffs[7] == Falcons):
                    falcons1 += 1
                elif (playoffs[8] == Falcons):
                    falcons2 += 1
                elif (playoffs[9] == Falcons):
                    falcons3 += 1
                elif (playoffs[10] == Falcons):
                    falcons4 += 1
                elif (playoffs[11] == Falcons):
                    falcons5 += 1
                elif (playoffs[12] == Falcons):
                    falcons6 += 1
                elif (playoffs[13] == Falcons):
                    falcons7 += 1
                else:
                    falconsOut += 1

            if (team == Saints):
                if (playoffs[7] == Saints):
                    saints1 += 1
                elif (playoffs[8] == Saints):
                    saints2 += 1
                elif (playoffs[9] == Saints):
                    saints3 += 1
                elif (playoffs[10] == Saints):
                    saints4 += 1
                elif (playoffs[11] == Saints):
                    saints5 += 1
                elif (playoffs[12] == Saints):
                    saints6 += 1
                elif (playoffs[13] == Saints):
                    saints7 += 1
                else:
                    saintsOut += 1

            if (team == Panthers):
                if (playoffs[7] == Panthers):
                    panthers1 += 1
                elif (playoffs[8] == Panthers):
                    panthers2 += 1
                elif (playoffs[9] == Panthers):
                    panthers3 += 1
                elif (playoffs[10] == Panthers):
                    panthers4 += 1
                elif (playoffs[11] == Panthers):
                    panthers5 += 1
                elif (playoffs[12] == Panthers):
                    panthers6 += 1
                elif (playoffs[13] == Panthers):
                    panthers7 += 1
                else:
                    panthersOut += 1

            if (team == Cardinals):
                if (playoffs[7] == Cardinals):
                    cardinals1 += 1
                elif (playoffs[8] == Cardinals):
                    cardinals2 += 1
                elif (playoffs[9] == Cardinals):
                    cardinals3 += 1
                elif (playoffs[10] == Cardinals):
                    cardinals4 += 1
                elif (playoffs[11] == Cardinals):
                    cardinals5 += 1
                elif (playoffs[12] == Cardinals):
                    cardinals6 += 1
                elif (playoffs[13] == Cardinals):
                    cardinals7 += 1
                else:
                    cardinalsOut += 1

            if (team == Niners):
                if (playoffs[7] == Niners):
                    niners1 += 1
                elif (playoffs[8] == Niners):
                    niners2 += 1
                elif (playoffs[9] == Niners):
                    niners3 += 1
                elif (playoffs[10] == Niners):
                    niners4 += 1
                elif (playoffs[11] == Niners):
                    niners5 += 1
                elif (playoffs[12] == Niners):
                    niners6 += 1
                elif (playoffs[13] == Niners):
                    niners7 += 1
                else:
                    ninersOut += 1

            if (team == Rams):
                if (playoffs[7] == Rams):
                    rams1 += 1
                elif (playoffs[8] == Rams):
                    rams2 += 1
                elif (playoffs[9] == Rams):
                    rams3 += 1
                elif (playoffs[10] == Rams):
                    rams4 += 1
                elif (playoffs[11] == Rams):
                    rams5 += 1
                elif (playoffs[12] == Rams):
                    rams6 += 1
                elif (playoffs[13] == Rams):
                    rams7 += 1
                else:
                    ramsOut += 1

            if (team == Seahawks):
                if (playoffs[7] == Seahawks):
                    seahawks1 += 1
                elif (playoffs[8] == Seahawks):
                    seahawks2 += 1
                elif (playoffs[9] == Seahawks):
                    seahawks3 += 1
                elif (playoffs[10] == Seahawks):
                    seahawks4 += 1
                elif (playoffs[11] == Seahawks):
                    seahawks5 += 1
                elif (playoffs[12] == Seahawks):
                    seahawks6 += 1
                elif (playoffs[13] == Seahawks):
                    seahawks7 += 1
                else:
                    seahawksOut += 1

        resetSimStandings(df)

    #trackScenarios(playoffsList, remSchedules, Patriots, '1')

    billsPlayoffs = (bills1 + bills2 + bills3 + bills4 + bills5 + bills6 + bills7) / 100.0
    billsDiv = (bills1 + bills2 + bills3 + bills4) / 100.0
    billsOut = 100 - billsPlayoffs
    dolphinsPlayoffs = (dolphins1 + dolphins2 + dolphins3 + dolphins4 + dolphins5 + dolphins6 + dolphins7) / 100.0
    dolphinsDiv = (dolphins1 + dolphins2 + dolphins3 + dolphins4) / 100.0
    dolphinsOut = 100 - dolphinsPlayoffs
    jetsPlayoffs = (jets1 + jets2 + jets3 + jets4 + jets5 + jets6 + jets7) / 100.0
    jetsDiv = (jets1 + jets2 + jets3 + jets4) / 100.0
    jetsOut = 100 - jetsPlayoffs
    patriotsPlayoffs = (patriots1 + patriots2 + patriots3 + patriots4 + patriots5 + patriots6 + patriots7) / 100.0
    patriotsDiv = (patriots1 + patriots2 + patriots3 + patriots4) / 100.0
    patriotsOut = 100 - patriotsPlayoffs
    brownsPlayoffs = (browns1 + browns2 + browns3 + browns4 + browns5 + browns6 + browns7) / 100.0
    brownsDiv = (browns1 + browns2 + browns3 + browns4) / 100.0
    brownsOut = 100 - brownsPlayoffs
    bengalsPlayoffs = (bengals1 + bengals2 + bengals3 + bengals4 + bengals5 + bengals6 + bengals7) / 100.0
    bengalsDiv = (bengals1 + bengals2 + bengals3 + bengals4) / 100.0
    bengalsOut = 100 - bengalsPlayoffs
    ravensPlayoffs = (ravens1 + ravens2 + ravens3 + ravens4 + ravens5 + ravens6 + ravens7) / 100.0
    ravensDiv = (ravens1 + ravens2 + ravens3 + ravens4) / 100.0
    ravensOut = 100 - ravensPlayoffs
    steelersPlayoffs = (steelers1 + steelers2 + steelers3 + steelers4 + steelers5 + steelers6 + steelers7) / 100.0
    steelersDiv = (steelers1 + steelers2 + steelers3 + steelers4) / 100.0
    steelersOut = 100 - steelersPlayoffs
    coltsPlayoffs = (colts1 + colts2 + colts3 + colts4 + colts5 + colts6 + colts7) / 100.0
    coltsDiv = (colts1 + colts2 + colts3 + colts4) / 100.0
    coltsOut = 100 - coltsPlayoffs
    jaguarsPlayoffs = (jaguars1 + jaguars2 + jaguars3 + jaguars4 + jaguars5 + jaguars6 + jaguars7) / 100.0
    jaguarsDiv = (jaguars1 + jaguars2 + jaguars3 + jaguars4) / 100.0
    jaguarsOut = 100 - jaguarsPlayoffs
    titansPlayoffs = (titans1 + titans2 + titans3 + titans4 + titans5 + titans6 + titans7) / 100.0
    titansDiv = (titans1 + titans2 + titans3 + titans4) / 100.0
    titansOut = 100 - titansPlayoffs
    texansPlayoffs = (texans1 + texans2 + texans3 + texans4 + texans5 + texans6 + texans7) / 100.0
    texansDiv = (texans1 + texans2 + texans3 + texans4) / 100.0
    texansOut = 100 - texansPlayoffs
    broncosPlayoffs = (broncos1 + broncos2 + broncos3 + broncos4 + broncos5 + broncos6 + broncos7) / 100.0
    broncosDiv = (broncos1 + broncos2 + broncos3 + broncos4) / 100.0
    broncosOut = 100 - broncosPlayoffs
    chargersPlayoffs = (chargers1 + chargers2 + chargers3 + chargers4 + chargers5 + chargers6 + chargers7) / 100.0
    chargersDiv = (chargers1 + chargers2 + chargers3 + chargers4) / 100.0
    chargersOut = 100 - chargersPlayoffs
    chiefsPlayoffs = (chiefs1 + chiefs2 + chiefs3 + chiefs4 + chiefs5 + chiefs6 + chiefs7) / 100.0
    chiefsDiv = (chiefs1 + chiefs2 + chiefs3 + chiefs4) / 100.0
    chiefsOut = 100 - chiefsPlayoffs
    raidersPlayoffs = (raiders1 + raiders2 + raiders3 + raiders4 + raiders5 + raiders6 + raiders7) / 100.0
    raidersDiv = (raiders1 + raiders2 + raiders3 + raiders4) / 100.0
    raidersOut = 100 - raidersPlayoffs
    cowboysPlayoffs = (cowboys1 + cowboys2 + cowboys3 + cowboys4 + cowboys5 + cowboys6 + cowboys7) / 100.0
    cowboysDiv = (cowboys1 + cowboys2 + cowboys3 + cowboys4) / 100.0
    cowboysOut = 100 - cowboysPlayoffs
    commandersPlayoffs = (
                                     commanders1 + commanders2 + commanders3 + commanders4 + commanders5 + commanders6 + commanders7) / 100.0
    commandersDiv = (commanders1 + commanders2 + commanders3 + commanders4) / 100.0
    commandersOut = 100 - commandersPlayoffs
    eaglesPlayoffs = (eagles1 + eagles2 + eagles3 + eagles4 + eagles5 + eagles6 + eagles7) / 100.0
    eaglesDiv = (eagles1 + eagles2 + eagles3 + eagles4) / 100.0
    eaglesOut = 100 - eaglesPlayoffs
    giantsPlayoffs = (giants1 + giants2 + giants3 + giants4 + giants5 + giants6 + giants7) / 100.0
    giantsDiv = (giants1 + giants2 + giants3 + giants4) / 100.0
    giantsOut = 100 - giantsPlayoffs
    bearsPlayoffs = (bears1 + bears2 + bears3 + bears4 + bears5 + bears6 + bears7) / 100.0
    bearsDiv = (bears1 + bears2 + bears3 + bears4) / 100.0
    bearsOut = 100 - bearsPlayoffs
    lionsPlayoffs = (lions1 + lions2 + lions3 + lions4 + lions5 + lions6 + lions7) / 100.0
    lionsDiv = (lions1 + lions2 + lions3 + lions4) / 100.0
    lionsOut = 100 - lionsPlayoffs
    packersPlayoffs = (packers1 + packers2 + packers3 + packers4 + packers5 + packers6 + packers7) / 100.0
    packersDiv = (packers1 + packers2 + packers3 + packers4) / 100.0
    packersOut = 100 - packersPlayoffs
    vikingsPlayoffs = (vikings1 + vikings2 + vikings3 + vikings4 + vikings5 + vikings6 + vikings7) / 100.0
    vikingsDiv = (vikings1 + vikings2 + vikings3 + vikings4) / 100.0
    vikingsOut = 100 - vikingsPlayoffs
    buccaneersPlayoffs = (
                                     buccaneers1 + buccaneers2 + buccaneers3 + buccaneers4 + buccaneers5 + buccaneers6 + buccaneers7) / 100.0
    buccaneersDiv = (buccaneers1 + buccaneers2 + buccaneers3 + buccaneers4) / 100.0
    buccaneersOut = 100 - buccaneersPlayoffs
    falconsPlayoffs = (falcons1 + falcons2 + falcons3 + falcons4 + falcons5 + falcons6 + falcons7) / 100.0
    falconsDiv = (falcons1 + falcons2 + falcons3 + falcons4) / 100.0
    falconsOut = 100 - falconsPlayoffs
    saintsPlayoffs = (saints1 + saints2 + saints3 + saints4 + saints5 + saints6 + saints7) / 100.0
    saintsDiv = (saints1 + saints2 + saints3 + saints4) / 100.0
    saintsOut = 100 - saintsPlayoffs
    panthersPlayoffs = (panthers1 + panthers2 + panthers3 + panthers4 + panthers5 + panthers6 + panthers7) / 100.0
    panthersDiv = (panthers1 + panthers2 + panthers3 + panthers4) / 100.0
    panthersOut = 100 - panthersPlayoffs
    cardinalsPlayoffs = (
                                    cardinals1 + cardinals2 + cardinals3 + cardinals4 + cardinals5 + cardinals6 + cardinals7) / 100.0
    cardinalsDiv = (cardinals1 + cardinals2 + cardinals3 + cardinals4) / 100.0
    cardinalsOut = 100 - cardinalsPlayoffs
    ninersPlayoffs = (niners1 + niners2 + niners3 + niners4 + niners5 + niners6 + niners7) / 100.0
    ninersDiv = (niners1 + niners2 + niners3 + niners4) / 100.0
    ninersOut = 100 - ninersPlayoffs
    ramsPlayoffs = (rams1 + rams2 + rams3 + rams4 + rams5 + rams6 + rams7) / 100.0
    ramsDiv = (rams1 + rams2 + rams3 + rams4) / 100.0
    ramsOut = 100 - ramsPlayoffs
    seahawksPlayoffs = (seahawks1 + seahawks2 + seahawks3 + seahawks4 + seahawks5 + seahawks6 + seahawks7) / 100.0
    seahawksDiv = (seahawks1 + seahawks2 + seahawks3 + seahawks4) / 100.0
    seahawksOut = 100 - seahawksPlayoffs


    return json.dumps([{
        'teamId': int(teamMap.loc[teamMap['teamName'] == ('49ers' if team == 'Niners' else team), 'teamId'].iloc[0]),
        'playoffs': locals()[f'{team.lower()}Playoffs'] * 10.0,
        'division': locals()[f'{team.lower()}Div'] * 10.0,
        'oneseed': locals()[f'{team.lower()}1'] / 10.0,
        'twoseed': locals()[f'{team.lower()}2'] / 10.0,
        'threeseed': locals()[f'{team.lower()}3'] / 10.0,
        'fourseed': locals()[f'{team.lower()}4'] / 10.0,
        'fiveseed': locals()[f'{team.lower()}5'] / 10.0,
        'sixseed': locals()[f'{team.lower()}6'] / 10.0,
        'sevenseed': locals()[f'{team.lower()}7'] / 10.0
    } for team in ['Bills', 'Dolphins', 'Jets', 'Patriots', 'Bengals', 'Browns', 'Ravens', 'Steelers', 'Colts', 'Jaguars', 'Titans', 'Texans', 'Broncos', 'Chiefs', 'Chargers', 'Raiders', 'Commanders', 'Cowboys', 'Giants', 'Eagles', 'Bears', 'Lions', 'Packers', 'Vikings', 'Buccaneers', 'Falcons', 'Saints', 'Panthers', 'Cardinals', 'Niners', 'Rams', 'Seahawks']])       
        
    
#divisionStandings()
#playoffPercentages()

#test_json = [{'homeTeamId': 775290905, 'awayTeamId': 775290893, 'homeScore': 39, 'awayScore': 28}, {'homeTeamId': 775290882, 'awayTeamId': 775290901, 'homeScore': 31, 'awayScore': 28}, {'homeTeamId': 775290903, 'awayTeamId': 775290881, 'homeScore': 29, 'awayScore': 12}, {'homeTeamId': 775290915, 'awayTeamId': 775290909, 'homeScore': 28, 'awayScore': 41}, {'homeTeamId': 775290894, 'awayTeamId': 775290899, 'homeScore': 14, 'awayScore': 31}, {'homeTeamId': 775290910, 'awayTeamId': 775290885, 'homeScore': 17, 'awayScore': 31}, {'homeTeamId': 775290911, 'awayTeamId': 775290880, 'homeScore': 3, 'awayScore': 35}, {'homeTeamId': 775290902, 'awayTeamId': 775290883, 'homeScore': 20, 'awayScore': 35}, {'homeTeamId': 775290895, 'awayTeamId': 775290907, 'homeScore': 0, 'awayScore': 19}, {'homeTeamId': 775290913, 'awayTeamId': 775290912, 'homeScore': 23, 'awayScore': 28}, {'homeTeamId': 775290887, 'awayTeamId': 775290906, 'homeScore': 28, 'awayScore': 52}, {'homeTeamId': 775290892, 'awayTeamId': 775290884, 'homeScore': 20, 'awayScore': 50}, {'homeTeamId': 775290891, 'awayTeamId': 775290896, 'homeScore': 29, 'awayScore': 27}, {'homeTeamId': 775290916, 'awayTeamId': 775290897, 'homeScore': 13, 'awayScore': 40}, {'homeTeamId': 775290914, 'awayTeamId': 775290886, 'homeScore': 0, 'awayScore': 35}, {'homeTeamId': 775290908, 'awayTeamId': 775290890, 'homeScore': 41, 'awayScore': 37}, {'homeTeamId': 775290896, 'awayTeamId': 775290894, 'homeScore': 28, 'awayScore': 49}, {'homeTeamId': 775290890, 'awayTeamId': 775290891, 'homeScore': 27, 'awayScore': 13}, {'homeTeamId': 775290885, 'awayTeamId': 775290882, 'homeScore': 48, 'awayScore': 29}, {'homeTeamId': 775290893, 'awayTeamId': 775290899, 'homeScore': 14, 'awayScore': 10}, {'homeTeamId': 775290902, 'awayTeamId': 775290913, 'homeScore': 31, 'awayScore': 28}, {'homeTeamId': 775290907, 'awayTeamId': 775290908, 'homeScore': 24, 'awayScore': 28}, {'homeTeamId': 775290897, 'awayTeamId': 775290886, 'homeScore': 18, 'awayScore': 28}, {'homeTeamId': 775290892, 'awayTeamId': 775290895, 'homeScore': 44, 'awayScore': 21}, {'homeTeamId': 775290901, 'awayTeamId': 775290906, 'homeScore': 33, 'awayScore': 40}, {'homeTeamId': 775290911, 'awayTeamId': 775290887, 'homeScore': 33, 'awayScore': 14}, {'homeTeamId': 775290884, 'awayTeamId': 775290915, 'homeScore': 31, 'awayScore': 27}, {'homeTeamId': 775290912, 'awayTeamId': 775290880, 'homeScore': 43, 'awayScore': 34}, {'homeTeamId': 775290909, 'awayTeamId': 775290914, 'homeScore': 42, 'awayScore': 14}, {'homeTeamId': 775290905, 'awayTeamId': 775290903, 'homeScore': 25, 'awayScore': 22}, {'homeTeamId': 775290883, 'awayTeamId': 775290910, 'homeScore': 7, 'awayScore': 28}, {'homeTeamId': 775290881, 'awayTeamId': 775290916, 'homeScore': 18, 'awayScore': 10}, {'homeTeamId': 775290883, 'awayTeamId': 775290895, 'homeScore': 16, 'awayScore': 12}, {'homeTeamId': 775290916, 'awayTeamId': 775290882, 'homeScore': 28, 'awayScore': 42}, {'homeTeamId': 775290896, 'awayTeamId': 775290909, 'homeScore': 42, 'awayScore': 38}, {'homeTeamId': 775290885, 'awayTeamId': 775290905, 'homeScore': 42, 'awayScore': 27}, {'homeTeamId': 775290893, 'awayTeamId': 775290908, 'homeScore': 21, 'awayScore': 44}, {'homeTeamId': 775290886, 'awayTeamId': 775290902, 'homeScore': 38, 'awayScore': 24}, {'homeTeamId': 775290907, 'awayTeamId': 775290913, 'homeScore': 14, 'awayScore': 21}, {'homeTeamId': 775290906, 'awayTeamId': 775290897, 'homeScore': 35, 'awayScore': 25}, {'homeTeamId': 775290915, 'awayTeamId': 775290892, 'homeScore': 17, 'awayScore': 43}, {'homeTeamId': 775290901, 'awayTeamId': 775290914, 'homeScore': 28, 'awayScore': 21}, {'homeTeamId': 775290881, 'awayTeamId': 775290894, 'homeScore': 21, 'awayScore': 34}, {'homeTeamId': 775290912, 'awayTeamId': 775290911, 'homeScore': 38, 'awayScore': 21}, {'homeTeamId': 775290890, 'awayTeamId': 775290884, 'homeScore': 45, 'awayScore': 28}, {'homeTeamId': 775290880, 'awayTeamId': 775290887, 'homeScore': 39, 'awayScore': 38}, {'homeTeamId': 775290899, 'awayTeamId': 775290891, 'homeScore': 23, 'awayScore': 12}, {'homeTeamId': 775290910, 'awayTeamId': 775290903, 'homeScore': 28, 'awayScore': 25}, {'homeTeamId': 775290887, 'awayTeamId': 775290912, 'homeScore': 28, 'awayScore': 31}, {'homeTeamId': 775290913, 'awayTeamId': 775290916, 'homeScore': 38, 'awayScore': 27}, {'homeTeamId': 775290914, 'awayTeamId': 775290915, 'homeScore': 35, 'awayScore': 41}, {'homeTeamId': 775290903, 'awayTeamId': 775290885, 'homeScore': 28, 'awayScore': 42}, {'homeTeamId': 775290899, 'awayTeamId': 775290890, 'homeScore': 20, 'awayScore': 21}, {'homeTeamId': 775290897, 'awayTeamId': 775290893, 'homeScore': 35, 'awayScore': 30}, {'homeTeamId': 775290907, 'awayTeamId': 775290906, 'homeScore': 28, 'awayScore': 31}, {'homeTeamId': 775290883, 'awayTeamId': 775290911, 'homeScore': 31, 'awayScore': 28}, {'homeTeamId': 775290886, 'awayTeamId': 775290896, 'homeScore': 17, 'awayScore': 20}, {'homeTeamId': 775290908, 'awayTeamId': 775290881, 'homeScore': 33, 'awayScore': 21}, {'homeTeamId': 775290880, 'awayTeamId': 775290901, 'homeScore': 28, 'awayScore': 21}, {'homeTeamId': 775290909, 'awayTeamId': 775290892, 'homeScore': 37, 'awayScore': 27}, {'homeTeamId': 775290891, 'awayTeamId': 775290910, 'homeScore': 24, 'awayScore': 26}, {'homeTeamId': 775290894, 'awayTeamId': 775290905, 'homeScore': 34, 'awayScore': 31}, {'homeTeamId': 775290895, 'awayTeamId': 775290902, 'homeScore': 21, 'awayScore': 31}, {'homeTeamId': 775290884, 'awayTeamId': 775290882, 'homeScore': 14, 'awayScore': 42}, {'homeTeamId': 775290895, 'awayTeamId': 775290910, 'homeScore': 0, 'awayScore': 31}, {'homeTeamId': 775290882, 'awayTeamId': 775290881, 'homeScore': 28, 'awayScore': 30}, {'homeTeamId': 775290903, 'awayTeamId': 775290916, 'homeScore': 28, 'awayScore': 31}, {'homeTeamId': 775290915, 'awayTeamId': 775290890, 'homeScore': 14, 'awayScore': 42}, {'homeTeamId': 775290899, 'awayTeamId': 775290880, 'homeScore': 31, 'awayScore': 28}, {'homeTeamId': 775290914, 'awayTeamId': 775290884, 'homeScore': 10, 'awayScore': 20}, {'homeTeamId': 775290907, 'awayTeamId': 775290897, 'homeScore': 34, 'awayScore': 28}, {'homeTeamId': 775290905, 'awayTeamId': 775290906, 'homeScore': 21, 'awayScore': 27}, {'homeTeamId': 775290913, 'awayTeamId': 775290892, 'homeScore': 14, 'awayScore': 21}, {'homeTeamId': 775290908, 'awayTeamId': 775290901, 'homeScore': 48, 'awayScore': 38}, {'homeTeamId': 775290909, 'awayTeamId': 775290911, 'homeScore': 42, 'awayScore': 45}, {'homeTeamId': 775290883, 'awayTeamId': 775290891, 'homeScore': 24, 'awayScore': 21}, {'homeTeamId': 775290893, 'awayTeamId': 775290912, 'homeScore': 21, 'awayScore': 31}, {'homeTeamId': 775290894, 'awayTeamId': 775290887, 'homeScore': 28, 'awayScore': 31}, {'homeTeamId': 775290882, 'awayTeamId': 775290913, 'homeScore': 42, 'awayScore': 39}, {'homeTeamId': 775290901, 'awayTeamId': 775290909, 'homeScore': 28, 'awayScore': 38}, {'homeTeamId': 775290885, 'awayTeamId': 775290895, 'homeScore': 29, 'awayScore': 22}, {'homeTeamId': 775290902, 'awayTeamId': 775290906, 'homeScore': 7, 'awayScore': 38}, {'homeTeamId': 775290915, 'awayTeamId': 775290907, 'homeScore': 0, 'awayScore': 23}, {'homeTeamId': 775290881, 'awayTeamId': 775290911, 'homeScore': 33, 'awayScore': 36}, {'homeTeamId': 775290916, 'awayTeamId': 775290896, 'homeScore': 35, 'awayScore': 38}, {'homeTeamId': 775290891, 'awayTeamId': 775290908, 'homeScore': 31, 'awayScore': 17}, {'homeTeamId': 775290884, 'awayTeamId': 775290899, 'homeScore': 7, 'awayScore': 10}, {'homeTeamId': 775290890, 'awayTeamId': 775290892, 'homeScore': 41, 'awayScore': 21}, {'homeTeamId': 775290887, 'awayTeamId': 775290905, 'homeScore': 27, 'awayScore': 14}, {'homeTeamId': 775290894, 'awayTeamId': 775290893, 'homeScore': 13, 'awayScore': 20}, {'homeTeamId': 775290880, 'awayTeamId': 775290897, 'homeScore': 24, 'awayScore': 23}, {'homeTeamId': 775290903, 'awayTeamId': 775290886, 'homeScore': 23, 'awayScore': 30}, {'homeTeamId': 775290912, 'awayTeamId': 775290914, 'homeScore': 45, 'awayScore': 28}, {'homeTeamId': 775290890, 'awayTeamId': 775290916, 'homeScore': 56, 'awayScore': 7}, {'homeTeamId': 775290882, 'awayTeamId': 775290902, 'homeScore': 31, 'awayScore': 25}, {'homeTeamId': 775290896, 'awayTeamId': 775290899, 'homeScore': 14, 'awayScore': 29}, {'homeTeamId': 775290907, 'awayTeamId': 775290885, 'homeScore': 42, 'awayScore': 38}, {'homeTeamId': 775290914, 'awayTeamId': 775290880, 'homeScore': 0, 'awayScore': 35}, {'homeTeamId': 775290910, 'awayTeamId': 775290881, 'homeScore': 7, 'awayScore': 0}, {'homeTeamId': 775290906, 'awayTeamId': 775290883, 'homeScore': 24, 'awayScore': 20}, {'homeTeamId': 775290897, 'awayTeamId': 775290895, 'homeScore': 42, 'awayScore': 21}, {'homeTeamId': 775290911, 'awayTeamId': 775290886, 'homeScore': 22, 'awayScore': 34}, {'homeTeamId': 775290892, 'awayTeamId': 775290915, 'homeScore': 31, 'awayScore': 21}, {'homeTeamId': 775290884, 'awayTeamId': 775290894, 'homeScore': 6, 'awayScore': 20}, {'homeTeamId': 775290913, 'awayTeamId': 775290905, 'homeScore': 21, 'awayScore': 24}, {'homeTeamId': 775290891, 'awayTeamId': 775290893, 'homeScore': 27, 'awayScore': 13}, {'homeTeamId': 775290893, 'awayTeamId': 775290894, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290916, 'awayTeamId': 775290903, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290891, 'awayTeamId': 775290884, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290905, 'awayTeamId': 775290910, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290890, 'awayTeamId': 775290914, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290882, 'awayTeamId': 775290887, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290885, 'awayTeamId': 775290913, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290902, 'awayTeamId': 775290907, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290892, 'awayTeamId': 775290901, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290895, 'awayTeamId': 775290886, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290915, 'awayTeamId': 775290911, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290906, 'awayTeamId': 775290912, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290908, 'awayTeamId': 775290899, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290883, 'awayTeamId': 775290896, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290880, 'awayTeamId': 775290881, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290897, 'awayTeamId': 775290909, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290886, 'awayTeamId': 775290897, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290882, 'awayTeamId': 775290910, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290891, 'awayTeamId': 775290890, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290899, 'awayTeamId': 775290893, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290881, 'awayTeamId': 775290885, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290901, 'awayTeamId': 775290902, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290907, 'awayTeamId': 775290883, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290896, 'awayTeamId': 775290908, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290914, 'awayTeamId': 775290887, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290911, 'awayTeamId': 775290906, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290912, 'awayTeamId': 775290892, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290884, 'awayTeamId': 775290905, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290880, 'awayTeamId': 775290915, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290909, 'awayTeamId': 775290903, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290894, 'awayTeamId': 775290916, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290913, 'awayTeamId': 775290895, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290909, 'awayTeamId': 775290880, 'homeScore': 45, 'awayScore': 42}, {'homeTeamId': 775290885, 'awayTeamId': 775290916, 'homeScore': 14, 'awayScore': 21}, {'homeTeamId': 775290911, 'awayTeamId': 775290899, 'homeScore': 37, 'awayScore': 40}, {'homeTeamId': 775290896, 'awayTeamId': 775290884, 'homeScore': 49, 'awayScore': 28}, {'homeTeamId': 775290902, 'awayTeamId': 775290894, 'homeScore': 38, 'awayScore': 37}, {'homeTeamId': 775290892, 'awayTeamId': 775290908, 'homeScore': 14, 'awayScore': 41}, {'homeTeamId': 775290910, 'awayTeamId': 775290914, 'homeScore': 42, 'awayScore': 7}, {'homeTeamId': 775290906, 'awayTeamId': 775290895, 'homeScore': 38, 'awayScore': 34}, {'homeTeamId': 775290912, 'awayTeamId': 775290886, 'homeScore': 28, 'awayScore': 31}, {'homeTeamId': 775290887, 'awayTeamId': 775290915, 'homeScore': 31, 'awayScore': 24}, {'homeTeamId': 775290890, 'awayTeamId': 775290893, 'homeScore': 30, 'awayScore': 41}, {'homeTeamId': 775290882, 'awayTeamId': 775290903, 'homeScore': 34, 'awayScore': 17}, {'homeTeamId': 775290883, 'awayTeamId': 775290907, 'homeScore': 31, 'awayScore': 27}, {'homeTeamId': 775290901, 'awayTeamId': 775290891, 'homeScore': 27, 'awayScore': 34}, {'homeTeamId': 775290899, 'awayTeamId': 775290896, 'homeScore': 34, 'awayScore': 7}, {'homeTeamId': 775290902, 'awayTeamId': 775290884, 'homeScore': 10, 'awayScore': 27}, {'homeTeamId': 775290901, 'awayTeamId': 775290912, 'homeScore': 34, 'awayScore': 42}, {'homeTeamId': 775290910, 'awayTeamId': 775290909, 'homeScore': 34, 'awayScore': 23}, {'homeTeamId': 775290895, 'awayTeamId': 775290890, 'homeScore': 20, 'awayScore': 38}, {'homeTeamId': 775290913, 'awayTeamId': 775290885, 'homeScore': 42, 'awayScore': 24}, {'homeTeamId': 775290886, 'awayTeamId': 775290880, 'homeScore': 31, 'awayScore': 21}, {'homeTeamId': 775290911, 'awayTeamId': 775290907, 'homeScore': 18, 'awayScore': 35}, {'homeTeamId': 775290906, 'awayTeamId': 775290894, 'homeScore': 31, 'awayScore': 28}, {'homeTeamId': 775290892, 'awayTeamId': 775290887, 'homeScore': 34, 'awayScore': 37}, {'homeTeamId': 775290908, 'awayTeamId': 775290915, 'homeScore': 42, 'awayScore': 7}, {'homeTeamId': 775290905, 'awayTeamId': 775290882, 'homeScore': 14, 'awayScore': 31}, {'homeTeamId': 775290891, 'awayTeamId': 775290903, 'homeScore': 22, 'awayScore': 25}, {'homeTeamId': 775290897, 'awayTeamId': 775290883, 'homeScore': 42, 'awayScore': 35}, {'homeTeamId': 775290893, 'awayTeamId': 775290881, 'homeScore': 38, 'awayScore': 35}, {'homeTeamId': 775290903, 'awayTeamId': 775290905, 'homeScore': 49, 'awayScore': 32}, {'homeTeamId': 775290894, 'awayTeamId': 775290891, 'homeScore': 27, 'awayScore': 17}, {'homeTeamId': 775290910, 'awayTeamId': 775290882, 'homeScore': 21, 'awayScore': 28}, {'homeTeamId': 775290896, 'awayTeamId': 775290881, 'homeScore': 7, 'awayScore': 24}, {'homeTeamId': 775290906, 'awayTeamId': 775290909, 'homeScore': 34, 'awayScore': 28}, {'homeTeamId': 775290885, 'awayTeamId': 775290880, 'homeScore': 24, 'awayScore': 22}, {'homeTeamId': 775290902, 'awayTeamId': 775290897, 'homeScore': 36, 'awayScore': 38}, {'homeTeamId': 775290892, 'awayTeamId': 775290914, 'homeScore': 24, 'awayScore': 28}, {'homeTeamId': 775290886, 'awayTeamId': 775290887, 'homeScore': 35, 'awayScore': 14}, {'homeTeamId': 775290895, 'awayTeamId': 775290911, 'homeScore': 32, 'awayScore': 32}, {'homeTeamId': 775290915, 'awayTeamId': 775290901, 'homeScore': 42, 'awayScore': 35}, {'homeTeamId': 775290912, 'awayTeamId': 775290916, 'homeScore': 21, 'awayScore': 20}, {'homeTeamId': 775290907, 'awayTeamId': 775290902, 'homeScore': 31, 'awayScore': 25}, {'homeTeamId': 775290895, 'awayTeamId': 775290893, 'homeScore': 7, 'awayScore': 21}, {'homeTeamId': 775290915, 'awayTeamId': 775290914, 'homeScore': 41, 'awayScore': 21}, {'homeTeamId': 775290913, 'awayTeamId': 775290882, 'homeScore': 19, 'awayScore': 35}, {'homeTeamId': 775290901, 'awayTeamId': 775290890, 'homeScore': 27, 'awayScore': 49}, {'homeTeamId': 775290899, 'awayTeamId': 775290905, 'homeScore': 24, 'awayScore': 20}, {'homeTeamId': 775290883, 'awayTeamId': 775290886, 'homeScore': 31, 'awayScore': 9}, {'homeTeamId': 775290897, 'awayTeamId': 775290906, 'homeScore': 10, 'awayScore': 41}, {'homeTeamId': 775290916, 'awayTeamId': 775290881, 'homeScore': 35, 'awayScore': 21}, {'homeTeamId': 775290887, 'awayTeamId': 775290880, 'homeScore': 44, 'awayScore': 22}, {'homeTeamId': 775290909, 'awayTeamId': 775290912, 'homeScore': 46, 'awayScore': 49}, {'homeTeamId': 775290884, 'awayTeamId': 775290891, 'homeScore': 10, 'awayScore': 27}, {'homeTeamId': 775290885, 'awayTeamId': 775290910, 'homeScore': 24, 'awayScore': 27}, {'homeTeamId': 775290896, 'awayTeamId': 775290903, 'homeScore': 35, 'awayScore': 28}, {'homeTeamId': 775290908, 'awayTeamId': 775290894, 'homeScore': 31, 'awayScore': 21}, {'homeTeamId': 775290913, 'awayTeamId': 775290883, 'homeScore': 14, 'awayScore': 28}, {'homeTeamId': 775290890, 'awayTeamId': 775290908, 'homeScore': 26, 'awayScore': 32}, {'homeTeamId': 775290903, 'awayTeamId': 775290894, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290886, 'awayTeamId': 775290911, 'homeScore': 31, 'awayScore': 21}, {'homeTeamId': 775290885, 'awayTeamId': 775290915, 'homeScore': 42, 'awayScore': 28}, {'homeTeamId': 775290916, 'awayTeamId': 775290893, 'homeScore': 25, 'awayScore': 19}, {'homeTeamId': 775290902, 'awayTeamId': 775290895, 'homeScore': 31, 'awayScore': 28}, {'homeTeamId': 775290905, 'awayTeamId': 775290881, 'homeScore': 33, 'awayScore': 42}, {'homeTeamId': 775290897, 'awayTeamId': 775290912, 'homeScore': 14, 'awayScore': 38}, {'homeTeamId': 775290901, 'awayTeamId': 775290892, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290910, 'awayTeamId': 775290913, 'homeScore': 45, 'awayScore': 14}, {'homeTeamId': 775290908, 'awayTeamId': 775290884, 'homeScore': 24, 'awayScore': 27}, {'homeTeamId': 775290887, 'awayTeamId': 775290909, 'homeScore': 31, 'awayScore': 30}, {'homeTeamId': 775290883, 'awayTeamId': 775290882, 'homeScore': 0, 'awayScore': 28}, {'homeTeamId': 775290891, 'awayTeamId': 775290914, 'homeScore': 21, 'awayScore': 20}, {'homeTeamId': 775290890, 'awayTeamId': 775290896, 'homeScore': 35, 'awayScore': 38}, {'homeTeamId': 775290893, 'awayTeamId': 775290884, 'homeScore': 21, 'awayScore': 24}, {'homeTeamId': 775290907, 'awayTeamId': 775290899, 'homeScore': 41, 'awayScore': 38}, {'homeTeamId': 775290884, 'awayTeamId': 775290908, 'homeScore': 28, 'awayScore': 33}, {'homeTeamId': 775290892, 'awayTeamId': 775290897, 'homeScore': 37, 'awayScore': 34}, {'homeTeamId': 775290881, 'awayTeamId': 775290899, 'homeScore': 0, 'awayScore': 14}, {'homeTeamId': 775290902, 'awayTeamId': 775290885, 'homeScore': 34, 'awayScore': 21}, {'homeTeamId': 775290886, 'awayTeamId': 775290907, 'homeScore': 14, 'awayScore': 28}, {'homeTeamId': 775290895, 'awayTeamId': 775290883, 'homeScore': 27, 'awayScore': 38}, {'homeTeamId': 775290916, 'awayTeamId': 775290910, 'homeScore': 17, 'awayScore': 42}, {'homeTeamId': 775290906, 'awayTeamId': 775290911, 'homeScore': 38, 'awayScore': 22}, {'homeTeamId': 775290914, 'awayTeamId': 775290901, 'homeScore': 7, 'awayScore': 27}, {'homeTeamId': 775290912, 'awayTeamId': 775290887, 'homeScore': 31, 'awayScore': 28}, {'homeTeamId': 775290880, 'awayTeamId': 775290909, 'homeScore': 52, 'awayScore': 37}, {'homeTeamId': 775290893, 'awayTeamId': 775290903, 'homeScore': 14, 'awayScore': 34}, {'homeTeamId': 775290890, 'awayTeamId': 775290913, 'homeScore': 48, 'awayScore': 25}, {'homeTeamId': 775290905, 'awayTeamId': 775290896, 'homeScore': 31, 'awayScore': 38}, {'homeTeamId': 775290896, 'awayTeamId': 775290893, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290913, 'awayTeamId': 775290910, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290901, 'awayTeamId': 775290915, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290886, 'awayTeamId': 775290906, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290914, 'awayTeamId': 775290892, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290897, 'awayTeamId': 775290911, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290907, 'awayTeamId': 775290895, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290883, 'awayTeamId': 775290902, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290899, 'awayTeamId': 775290894, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290881, 'awayTeamId': 775290903, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290882, 'awayTeamId': 775290885, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290908, 'awayTeamId': 775290891, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290880, 'awayTeamId': 775290912, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290884, 'awayTeamId': 775290890, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290909, 'awayTeamId': 775290887, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290916, 'awayTeamId': 775290905, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290912, 'awayTeamId': 775290909, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290893, 'awayTeamId': 775290896, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290881, 'awayTeamId': 775290905, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290894, 'awayTeamId': 775290890, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290899, 'awayTeamId': 775290916, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290885, 'awayTeamId': 775290883, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290911, 'awayTeamId': 775290902, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290910, 'awayTeamId': 775290907, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290887, 'awayTeamId': 775290897, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290915, 'awayTeamId': 775290891, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290906, 'awayTeamId': 775290886, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290914, 'awayTeamId': 775290908, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290884, 'awayTeamId': 775290901, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290903, 'awayTeamId': 775290913, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290895, 'awayTeamId': 775290882, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290892, 'awayTeamId': 775290880, 'homeScore': 0, 'awayScore': 0}, {'homeTeamId': 775290914, 'awayTeamId': 775290883, 'homeScore': 13, 'awayScore': 28}, {'homeTeamId': 775290915, 'awayTeamId': 775290912, 'homeScore': 30, 'awayScore': 31}, {'homeTeamId': 775290882, 'awayTeamId': 775290907, 'homeScore': 25, 'awayScore': 21}, {'homeTeamId': 775290903, 'awayTeamId': 775290899, 'homeScore': 14, 'awayScore': 17}, {'homeTeamId': 775290910, 'awayTeamId': 775290902, 'homeScore': 34, 'awayScore': 42}, {'homeTeamId': 775290881, 'awayTeamId': 775290913, 'homeScore': 14, 'awayScore': 31}, {'homeTeamId': 775290905, 'awayTeamId': 775290916, 'homeScore': 29, 'awayScore': 31}, {'homeTeamId': 775290891, 'awayTeamId': 775290892, 'homeScore': 43, 'awayScore': 21}, {'homeTeamId': 775290887, 'awayTeamId': 775290901, 'homeScore': 41, 'awayScore': 28}, {'homeTeamId': 775290908, 'awayTeamId': 775290885, 'homeScore': 13, 'awayScore': 35}, {'homeTeamId': 775290894, 'awayTeamId': 775290896, 'homeScore': 45, 'awayScore': 44}, {'homeTeamId': 775290911, 'awayTeamId': 775290897, 'homeScore': 17, 'awayScore': 24}, {'homeTeamId': 775290909, 'awayTeamId': 775290886, 'homeScore': 53, 'awayScore': 55}, {'homeTeamId': 775290880, 'awayTeamId': 775290906, 'homeScore': 45, 'awayScore': 28}]
#results = simulate_odds(test_json)
#print (results)

#r = tiebreak2(Panthers, Commanders)
#print (r[0].getName() + r[1].getName())

