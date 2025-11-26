import pandas as pd
from datetime import date
import random
import time

def get_training_and_testing_data(df, trainingPortion = 0.8):
    trainingMatches = round(df.shape[0] * trainingPortion)
    dataCopy = df.copy(deep=True)
    training_data = dataCopy.iloc[0:trainingMatches]
    testing_data = dataCopy.iloc[trainingMatches:]
    return training_data, testing_data

def map_matches_to_players(df):
    players = {}
    for row in df.iloc[:].itertuples():
        for i in range(1, 7):
            PName = getattr(row, f'P{i}_player_name')
            PCarId = getattr(row, f'P{i}_car_id')
            matchDate = getattr(row, 'date')
            PScore = getattr(row, f'P{i}_score')
            PGoals = getattr(row, f'P{i}_goals')
            PAssists = getattr(row, f'P{i}_assists')
            PSaves = getattr(row, f'P{i}_saves')
            PShots = getattr(row, f'P{i}_shots')
            PShotsConceded = getattr(row, f'P{i}_shots_conceded')
            PGoalsConceded = getattr(row, f'P{i}_goals_conceded')
            PGoalsConcededLastDefender = getattr(row, f'P{i}_goals_conceded_while_last_defender')
            PShootingPercentage = getattr(row, f'P{i}_shooting_percentage')
            PBPM = getattr(row, f'P{i}_bpm')
            PAvgBoostAmount = getattr(row, f'P{i}_avg_boost_amount')
            PBoostCollected = getattr(row, f'P{i}_amount_collected')
            PAmountCollectedBigPads = getattr(row, f'P{i}_amount_collected_big_pads')
            PAmountCollectedSmallPads = getattr(row, f'P{i}_amount_collected_small_pads')
            PCountCollectedBigPads = getattr(row, f'P{i}_count_collected_big_pads')
            PCountCollectedSmallPads = getattr(row, f'P{i}_count_collected_small_pads')
            PAmountStolen = getattr(row, f'P{i}_amount_stolen')
            PAmountStolenBigPads = getattr(row, f'P{i}_amount_stolen_big_pads')
            PAmountStolenSmallPads = getattr(row, f'P{i}_amount_stolen_small_pads')
            PCountStolenBigPads = getattr(row, f'P{i}_count_stolen_big_pads')
            PCountStolenSmallPads = getattr(row, f'P{i}_count_stolen_small_pads')
            P0BoostTime = getattr(row, f'P{i}_0_boost_time')
            P100BoostTime = getattr(row, f'P{i}_100_boost_time')
            PAmountUsedWhileSupersonic = getattr(row, f'P{i}_amount_used_while_supersonic')
            PAmountOverfillTotal = getattr(row, f'P{i}_amount_overfill_total')
            PAmountOverfillStolen = getattr(row, f'P{i}_amount_overfill_stolen')
            PAvgSpeed = getattr(row, f'P{i}_avg_speed')
            PTotalDistance = getattr(row, f'P{i}_total_distance')
            PTimeSlowSpeed = getattr(row, f'P{i}_time_slow_speed')
            PPercentageSlowSpeed = getattr(row, f'P{i}_percentage_slow_speed')
            PTimeBoostSpeed = getattr(row, f'P{i}_time_boost_speed')
            PPercentageBoostSpeed = getattr(row, f'P{i}_percentage_boost_speed')
            PTimeSupersonicSpeed = getattr(row, f'P{i}_time_supersonic_speed')
            PPercentageSupersonicSpeed = getattr(row, f'P{i}_percentage_supersonic_speed')
            PTimeOnGround = getattr(row, f'P{i}_time_on_ground')
            PPercentageOnGround = getattr(row, f'P{i}_percentage_on_ground')
            PTimeLowInAir = getattr(row, f'P{i}_time_low_in_air')
            PPercentageLowInAir = getattr(row, f'P{i}_percentage_low_in_air')
            PTimeHighInAir = getattr(row, f'P{i}_time_high_in_air')
            PPercentageHighInAir = getattr(row, f'P{i}_percentage_high_in_air')
            PTimePowerslide = getattr(row, f'P{i}_time_powerslide')
            PAvgPowerslideTime = getattr(row, f'P{i}_avg_powerslide_time')
            PCountPowerslide = getattr(row, f'P{i}_count_powerslide')
            PTimeMostBack = getattr(row, f'P{i}_time_most_back')
            PPercentageMostBack = getattr(row, f'P{i}_percentage_most_back')
            PTimeMostForward = getattr(row, f'P{i}_time_most_forward')
            PPercentageMostForward = getattr(row, f'P{i}_percentage_most_forward')
            PTimeInFrontOfBall = getattr(row, f'P{i}_time_in_front_of_ball')
            PPercentageInFrontOfBall = getattr(row, f'P{i}_percentage_in_front_of_ball')
            PTimeBehindBall = getattr(row, f'P{i}_time_behind_ball')
            PPercentageBehindBall = getattr(row, f'P{i}_percentage_behind_ball')
            PTimeDefensiveHalf = getattr(row, f'P{i}_time_defensive_half')
            PPercentageDefensiveHalf = getattr(row, f'P{i}_percentage_defensive_half')
            PTimeOffensiveHalf = getattr(row, f'P{i}_time_offensive_half')
            PPercentageOffensiveHalf = getattr(row, f'P{i}_percentage_offensive_half')
            PTimeDefensiveThird = getattr(row, f'P{i}_time_defensive_third')
            PPercentageDefensiveThird = getattr(row, f'P{i}_percentage_defensive_third')
            PTimeNeutralThird = getattr(row, f'P{i}_time_neutral_third')
            PPercentageNeutralThird = getattr(row, f'P{i}_percentage_neutral_third')
            PTimeOffensiveThird = getattr(row, f'P{i}_time_offensive_third')
            PPercentageOffensiveThird = getattr(row, f'P{i}_percentage_offensive_third')
            PAvgDistanceToBall = getattr(row, f'P{i}_avg_distance_to_ball')
            PAvgDistanceToBallHasPossession = getattr(row, f'P{i}_avg_distance_to_ball_has_possession')
            PAvgDistanceToBallNoPossession = getattr(row, f'P{i}_avg_distance_to_ball_no_possession')
            PAvgDistanceToTeamMates = getattr(row, f'P{i}_avg_distance_to_team_mates')
            PDemosInflicted = getattr(row, f'P{i}_demos_inflicted')
            match = {
                    'date': matchDate,
                    'score': PScore,
                    'goals': PGoals,
                    'assists': PAssists,
                    'saves': PSaves,
                    'shots': PShots,
                    'shots_conceded': PShotsConceded,
                    'goals_conceded': PGoalsConceded,
                    'goals_conceded_last_defender': PGoalsConcededLastDefender,
                    'shooting_percentage': PShootingPercentage,
                    'bpm': PBPM,
                    'avg_boost_amount': PAvgBoostAmount,
                    'boost_collected': PBoostCollected,
                    'amount_collected_big_pads': PAmountCollectedBigPads,
                    'amount_collected_small_pads': PAmountCollectedSmallPads,
                    'count_collected_big_pads': PCountCollectedBigPads,
                    'count_collected_small_pads': PCountCollectedSmallPads,
                    'amount_stolen': PAmountStolen,
                    'amount_stolen_big_pads': PAmountStolenBigPads,
                    'amount_stolen_small_pads': PAmountStolenSmallPads,
                    'count_stolen_big_pads': PCountStolenBigPads,
                    'count_stolen_small_pads': PCountStolenSmallPads,
                    '0_boost_time': P0BoostTime,
                    '100_boost_time': P100BoostTime,
                    'amount_used_while_supersonic': PAmountUsedWhileSupersonic,
                    'amount_overfill_total': PAmountOverfillTotal,
                    'amount_overfill_stolen': PAmountOverfillStolen,
                    'avg_speed': PAvgSpeed,
                    'total_distance': PTotalDistance,
                    'time_slow_speed': PTimeSlowSpeed,
                    'percentage_slow_speed': PPercentageSlowSpeed,
                    'time_boost_speed': PTimeBoostSpeed,
                    'percentage_boost_speed': PPercentageBoostSpeed,
                    'time_supersonic_speed': PTimeSupersonicSpeed,
                    'percentage_supersonic_speed': PPercentageSupersonicSpeed,
                    'time_on_ground': PTimeOnGround,
                    'percentage_on_ground': PPercentageOnGround,
                    'time_low_in_air': PTimeLowInAir,
                    'percentage_low_in_air': PPercentageLowInAir,
                    'time_high_in_air': PTimeHighInAir,
                    'percentage_high_in_air': PPercentageHighInAir,
                    'time_powerslide': PTimePowerslide,
                    'avg_powerslide_time': PAvgPowerslideTime,
                    'count_powerslide': PCountPowerslide,
                    'time_most_back': PTimeMostBack,
                    'percentage_most_back': PPercentageMostBack,
                    'time_most_forward': PTimeMostForward,
                    'percentage_most_forward': PPercentageMostForward,
                    'time_in_front_of_ball': PTimeInFrontOfBall,
                    'percentage_in_front_of_ball': PPercentageInFrontOfBall,
                    'time_behind_ball': PTimeBehindBall,
                    'percentage_behind_ball': PPercentageBehindBall,
                    'time_defensive_half': PTimeDefensiveHalf,
                    'percentage_defensive_half': PPercentageDefensiveHalf,
                    'time_offensive_half': PTimeOffensiveHalf,
                    'percentage_offensive_half': PPercentageOffensiveHalf,
                    'time_defensive_third': PTimeDefensiveThird,
                    'percentage_defensive_third': PPercentageDefensiveThird,
                    'time_neutral_third': PTimeNeutralThird,
                    'percentage_neutral_third': PPercentageNeutralThird,
                    'time_offensive_third': PTimeOffensiveThird,
                    'percentage_offensive_third': PPercentageOffensiveThird,
                    'avg_distance_to_ball': PAvgDistanceToBall,
                    'avg_distance_to_ball_has_possession': PAvgDistanceToBallHasPossession,
                    'avg_distance_to_ball_no_possession': PAvgDistanceToBallNoPossession,
                    'avg_distance_to_team_mates': PAvgDistanceToTeamMates,
                    'demos_inflicted': PDemosInflicted,
            }
            if(PName not in players.keys()):
                players[PName] = []
            players[PName].append(match)
    return players
        
def get_match_data(fileName):
    data = pd.read_csv(f"{fileName}")
    data['result'] = data['result'].map({'win': 1, 'loss': -1})
    data.dropna(inplace=True, axis=0, subset=['result'])
    matchData = data.drop(columns=['replay_id', 'replay_title', 'map', 'team_name', 'opposing_team_name'])                
    return matchData

def average_player_stats_over_time(players, playerName, startDate = "YYYY-MM-DD", endDate = "YYYY-MM-DD"):
    if(playerName not in players.keys()):
        raise KeyError("Player name does not exist in list of players")
    if(startDate == "YYYY-MM-DD" or endDate == "YYYY-MM-DD"):
        raise ValueError("startDate or endDate have an incorrect value. Please provide a valid date in the YYYY-MM-DD format")
    averageStats = {}
    for key in next(iter(players.values()))[0].keys():
        if(key != "date"):
            averageStats[key] = 0
    matchesAnalyzed = 0
    startDate = startDate.split("-")
    endDate = endDate.split("-")
    for match in players[playerName]:
        matchDate = match['date'].split(" ")[0].split("-")
        if(date(int(matchDate[0]), int(matchDate[1]), int(matchDate[2])) < date(int(startDate[0]), int(startDate[1]), int(startDate[2]))):
            continue
        if(date(int(matchDate[0]), int(matchDate[1]), int(matchDate[2])) > date(int(endDate[0]),int(endDate[1]),int(endDate[2]))):
            break
        for key in averageStats.keys():
            averageStats[key] += match[key]
        matchesAnalyzed += 1
    for key in averageStats.keys():
        averageStats[key] /= matchesAnalyzed
    return averageStats

def get_overall_averages_over_time(players, startDate = "YYYY-MM-DD", endDate = "YYYY-MM-DD"):
    matchesAnalyzed = 0
    averageStats = {}
    if(startDate == "YYYY-MM-DD" or endDate == "YYYY-MM-DD"):
        raise ValueError("startDate or endDate have an incorrect value. Please provide a valid date in the YYYY-MM-DD format")
    for key in next(iter(players.values()))[0].keys():
        if(key != "date"):
            averageStats[key] = 0
    startDate = startDate.split("-")
    endDate = endDate.split("-")
    for playerName in players:
        player = players[playerName]
        for match in player:
            matchDate = match['date'].split(" ")[0].split("-")
            if(date(int(matchDate[0]), int(matchDate[1]), int(matchDate[2])) < date(int(startDate[0]),int(startDate[1]),int(startDate[2]))):
                continue
            if(date(int(matchDate[0]), int(matchDate[1]), int(matchDate[2])) > date(int(endDate[0]),int(endDate[1]),int(endDate[2]))):
                break
            for key in averageStats.keys():
                averageStats[key] += match[key]
            matchesAnalyzed += 1
    for key in averageStats.keys():
        averageStats[key] /= matchesAnalyzed
    return averageStats

def get_match_data_for_model(matchData, startDate = "YYYY-MM-DD", randomSeed = True):
    if(startDate == "YYYY-MM-DD"):
        raise ValueError("startDate is not not set")
    matchDataForModel = matchData[['date','result','P1_player_name','P2_player_name','P3_player_name','P4_player_name','P5_player_name','P6_player_name']]
    matchDataForModel = matchDataForModel[matchDataForModel['date'] > startDate]
    random.seed(1)
    if(randomSeed):
        random.seed(int(round(time.time() * 1000)))
    for index, match in matchDataForModel.iterrows():
        if(random.random() < .5):
            matchDataForModel.loc[index, 'result'] = -1 * match['result']
            for i in range(1,4):
                tempPlayerName = match[f"P{i}_player_name"]
                matchDataForModel.loc[index,f"P{i}_player_name"] = match[f"P{i + 3}_player_name"]
                matchDataForModel.loc[index,f"P{i+3}_player_name"] = tempPlayerName
    return matchDataForModel
    

matchData = get_match_data("Sorted_Matches.csv")
print(f"Match data loaded, {matchData.shape[0]} matches")
playersData = map_matches_to_players(matchData)
print("Player historical data loaded")
matchDataForModel = get_match_data_for_model(matchData, startDate="2022-05-10")
print(f"Match summaries for model formatted and retrieved ({matchData.shape[0] - matchDataForModel.shape[0]} matches filtered out to form baseline performance stats)")
print(f"Match summaries: {matchDataForModel[matchDataForModel['result'] == 1].shape[0]} wins | {matchDataForModel[matchDataForModel['result'] == -1].shape[0]} losses")
train, test = get_training_and_testing_data(matchDataForModel)
print(f"training({train.shape[0]} matches) and test({test.shape[0]} matches) summaries retrieved for model")

print(average_player_stats_over_time(playersData, "MaJicBear", "2021-10-01", "2022-05-10"))
print(get_overall_averages_over_time(playersData, "2021-10-01", "2022-05-10"))