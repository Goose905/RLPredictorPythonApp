from flask import Flask, render_template, jsonify, request
import urllib.parse
import xgboost as xgb
from datetime import date
import csv
# Run web server after installing required packages:
# pip install flask xgboost
# To run the server, use the command:
# flask --app Webserver run

app = Flask(__name__)

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

def build_feature_vector(playersData, matchSummary):
    featureVector = []
    matchDate = matchSummary['date'].split(" ")[0]
    team1Stats = {}
    team2Stats = {}
    overallAverageStats = get_overall_averages_over_time(playersData, "2021-10-01", matchDate)
    for j in range(1,7):
        playerName = matchSummary[f'P{j}_player_name']
        playerAverages = {}
        try:
            playerAverages = average_player_stats_over_time(playersData, playerName, "2021-10-01", matchDate)
        except (KeyError, ZeroDivisionError):
            playerAverages = overallAverageStats
        for key in playerAverages.keys():
            if(j <= 3):
                if(key not in team1Stats.keys()):
                    team1Stats[key] = 0
                team1Stats[key] += playerAverages[key]
            else:
                if(key not in team2Stats.keys()):
                    team2Stats[key] = 0
                team2Stats[key] += playerAverages[key]
    team1Stats = {key: team1Stats[key] / 3 for key in team1Stats.keys()}
    team2Stats = {key: team2Stats[key] / 3 for key in team2Stats.keys()}
    for key in team1Stats.keys():
        featureVector.append(team1Stats[key])
    for key in team2Stats.keys():
        featureVector.append(team2Stats[key])
    return featureVector

xgb_model = xgb.Booster()
xgb_model.load_model('xgb_model.json')

playerData = {}
with open("reformattedPlayersData.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        playerName = row[0]
        matchDate = row[1]
        matchData = row[2:]
        if playerName not in playerData:
            playerData[playerName] = []
        matchDict = {'date': matchDate}
        for i, value in enumerate(matchData):
            matchDict[str(i)] = int(value) if value.isdigit() else float(value) if '.' in value else value
        playerData[playerName].append(matchDict)

@app.route('/')
def home():
    return render_template('index.html', players=sorted(list(playerData.keys())))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    teamOnePlayers = data.getlist('TeamOnePlayers')
    teamTwoPlayers = data.getlist('TeamTwoPlayers')
    matchDate = data.get('matchDate')
    P1Name = teamOnePlayers[0]
    P2Name = teamOnePlayers[1]
    P3Name = teamOnePlayers[2]
    P4Name = teamTwoPlayers[0]
    P5Name = teamTwoPlayers[1]
    P6Name = teamTwoPlayers[2]
    matchSummary = {
        'P1_player_name': P1Name,
        'P2_player_name': P2Name,
        'P3_player_name': P3Name,
        'P4_player_name': P4Name,
        'P5_player_name': P5Name,
        'P6_player_name': P6Name,
        'date': matchDate
    }
    feature_vector = build_feature_vector(playerData, matchSummary)
    prediction = xgb_model.predict(xgb.DMatrix([feature_vector]))
    predicted_winner = "Team 1" if prediction[0] > 0.5 else "Team 2"
    confidence = prediction[0] if prediction[0] > 0.5 else 1 - prediction[0]
    response = {
        "predicted_winner": predicted_winner,
        "confidence": str(confidence)
    }
    return jsonify(response)

@app.route('/players', methods=['GET'])
def get_players():
    players_list = sorted(list(playerData.keys()))
    return jsonify(players_list)

@app.route('/match', methods=['GET'])
def get_player_stats():
    match_date = request.args.get('date')
    team1_players = [urllib.parse.unquote(player) for player in request.args.get('team1').split(',')]
    team2_players = [urllib.parse.unquote(player) for player in request.args.get('team2').split(',')]
    players = []
    overall_stats = get_overall_averages_over_time(playerData, "2021-10-01", match_date)
    for player in team1_players + team2_players:
        try:
            player_stats = average_player_stats_over_time(playerData, player, "2021-10-01", match_date)
            players.append({"name": player, "stats": list(player_stats.values())})
        except (KeyError, ZeroDivisionError):
            player_stats = overall_stats
            players.append({"name": player, "stats": list(player_stats.values())})
    return render_template('matchSummary.html', players=players)