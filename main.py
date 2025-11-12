import pandas as pd

def split_dataset_by_date(df, date):
    before_date = df[df['date'] < date]
    on_or_after_date = df[df['date'] >= date]
    return before_date, on_or_after_date

def get_training_and_testing_data(df, split_date):
    training_data, testing_data = split_dataset_by_date(df, split_date)
    training_data = training_data.drop(columns=['replay_id','replay_title','map','date','team_name','opposing_team_name', 'P1_player_name', 'P1_car_name', 'P2_player_name', 'P2_car_name', 'P3_player_name', 'P3_car_name', 'P4_player_name', 'P4_car_name', 'P5_player_name', 'P5_car_name', 'P6_player_name', 'P6_car_name'])
    testing_data = testing_data.drop(columns=['replay_id','replay_title','map','date','team_name','opposing_team_name', 'P1_player_name', 'P1_car_name', 'P2_player_name', 'P2_car_name', 'P3_player_name', 'P3_car_name', 'P4_player_name', 'P4_car_name', 'P5_player_name', 'P5_car_name', 'P6_player_name', 'P6_car_name'])
    return training_data, testing_data

data = pd.read_csv('Sorted_Matches.csv')
data['result'] = data['result'].map({'win': 1, 'loss': 0})
data.dropna(inplace=True, axis=0, subset=['result'])
playerData = data.drop(columns=['replay_id', 'replay_title', 'map', 'date', 'team_name', 'opposing_team_name'])
players = {}
matchCount = 0
for row in data.iloc[:5000].itertuples():
    if(matchCount >= 5000):
        break
    for i in range(1, 7):
        PName = getattr(row, f'P{i}_player_name')
        PCarId = getattr(row, f'P{i}_car_id')
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
        if PName in players:
            players[PName]['games_played'] += 1
            players[PName]['stats']['score'] += PScore
            players[PName]['stats']['goals'] += PGoals
            players[PName]['stats']['assists'] += PAssists
            players[PName]['stats']['saves'] += PSaves
            players[PName]['stats']['shots'] += PShots
            players[PName]['stats']['shots_conceded'] += PShotsConceded
            players[PName]['stats']['goals_conceded'] += PGoalsConceded
            players[PName]['stats']['goals_conceded_last_defender'] += PGoalsConcededLastDefender
            players[PName]['stats']['shooting_percentage'] += PShootingPercentage
            players[PName]['stats']['bpm'] += PBPM
            players[PName]['stats']['avg_boost_amount'] += PAvgBoostAmount
            players[PName]['stats']['boost_collected'] += PBoostCollected
            players[PName]['stats']['amount_collected_big_pads'] += PAmountCollectedBigPads
            players[PName]['stats']['amount_collected_small_pads'] += PAmountCollectedSmallPads
            players[PName]['stats']['count_collected_big_pads'] += PCountCollectedBigPads
            players[PName]['stats']['count_collected_small_pads'] += PCountCollectedSmallPads
            players[PName]['stats']['amount_stolen'] += PAmountStolen
            players[PName]['stats']['amount_stolen_big_pads'] += PAmountStolenBigPads
            players[PName]['stats']['amount_stolen_small_pads'] += PAmountStolenSmallPads
            players[PName]['stats']['count_stolen_big_pads'] += PCountStolenBigPads
            players[PName]['stats']['count_stolen_small_pads'] += PCountStolenSmallPads
            players[PName]['stats']['0_boost_time'] += P0BoostTime
            players[PName]['stats']['100_boost_time'] += P100BoostTime
            players[PName]['stats']['amount_used_while_supersonic'] += PAmountUsedWhileSupersonic
            players[PName]['stats']['amount_overfill_total'] += PAmountOverfillTotal
            players[PName]['stats']['amount_overfill_stolen'] += PAmountOverfillStolen
            players[PName]['stats']['avg_speed'] += PAvgSpeed
            players[PName]['stats']['total_distance'] += PTotalDistance
            players[PName]['stats']['time_slow_speed'] += PTimeSlowSpeed
            players[PName]['stats']['percentage_slow_speed'] += PPercentageSlowSpeed
            players[PName]['stats']['time_boost_speed'] += PTimeBoostSpeed
            players[PName]['stats']['percentage_boost_speed'] += PPercentageBoostSpeed
            players[PName]['stats']['time_supersonic_speed'] += PTimeSupersonicSpeed
            players[PName]['stats']['percentage_supersonic_speed'] += PPercentageSupersonicSpeed
            players[PName]['stats']['time_on_ground'] += PTimeOnGround
            players[PName]['stats']['percentage_on_ground'] += PPercentageOnGround
            players[PName]['stats']['time_low_in_air'] += PTimeLowInAir
            players[PName]['stats']['percentage_low_in_air'] += PPercentageLowInAir
            players[PName]['stats']['time_high_in_air'] += PTimeHighInAir
            players[PName]['stats']['percentage_high_in_air'] += PPercentageHighInAir
            players[PName]['stats']['time_powerslide'] += PTimePowerslide
            players[PName]['stats']['avg_powerslide_time'] += PAvgPowerslideTime
            players[PName]['stats']['count_powerslide'] += PCountPowerslide
            players[PName]['stats']['time_most_back'] += PTimeMostBack
            players[PName]['stats']['percentage_most_back'] += PPercentageMostBack
            players[PName]['stats']['time_most_forward'] += PTimeMostForward
            players[PName]['stats']['percentage_most_forward'] += PPercentageMostForward
            players[PName]['stats']['time_in_front_of_ball'] += PTimeInFrontOfBall
            players[PName]['stats']['percentage_in_front_of_ball'] += PPercentageInFrontOfBall
            players[PName]['stats']['time_behind_ball'] += PTimeBehindBall
            players[PName]['stats']['percentage_behind_ball'] += PPercentageBehindBall
            players[PName]['stats']['time_defensive_half'] += PTimeDefensiveHalf
            players[PName]['stats']['percentage_defensive_half'] += PPercentageDefensiveHalf
            players[PName]['stats']['time_offensive_half'] += PTimeOffensiveHalf
            players[PName]['stats']['percentage_offensive_half'] += PPercentageOffensiveHalf
            players[PName]['stats']['time_defensive_third'] += PTimeDefensiveThird
            players[PName]['stats']['percentage_defensive_third'] += PPercentageDefensiveThird
            players[PName]['stats']['time_neutral_third'] += PTimeNeutralThird
            players[PName]['stats']['percentage_neutral_third'] += PPercentageNeutralThird
            players[PName]['stats']['time_offensive_third'] += PTimeOffensiveThird
            players[PName]['stats']['percentage_offensive_third'] += PPercentageOffensiveThird
            players[PName]['stats']['avg_distance_to_ball'] += PAvgDistanceToBall
            players[PName]['stats']['avg_distance_to_ball_has_possession'] += PAvgDistanceToBallHasPossession
            players[PName]['stats']['avg_distance_to_ball_no_possession'] += PAvgDistanceToBallNoPossession
            players[PName]['stats']['avg_distance_to_team_mates'] += PAvgDistanceToTeamMates
            players[PName]['stats']['demos_inflicted'] += PDemosInflicted
        else:
            players[PName] = {
                'games_played': 1,
                'stats': {
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
            }
    matchCount += 1
average_stats = {}
total_players = len(players)

for player in players.values():
    for stat, value in player['stats'].items():
        if(stat not in average_stats):
            average_stats[stat] = 0
        if(value is not None):
            average_stats[stat] += value / player['games_played']

# Calculate the averages
for stat in average_stats:
    average_stats[stat] /= total_players

print("Average Statistics:")
for stat, value in average_stats.items():
    print(f"{stat}: {value}")
