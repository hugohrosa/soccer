import json
import pickle

DB = 'datasets/uk_premier_league/season'
FILENAME = 'season_stats.json'

STATS = ['touches', 'total_tackle', 'aerial_lost', 'man_of_the_match', 'total_pass', 'aerial_won', 'accurate_pass',
         'goal_assist', 'fouls', 'won_contest', 'blocked_scoring_att', 'post_scoring_att', 'total_scoring_att',
         'total_pass', 'goals', 'yellow_card', 'red_card']

players = dict()

for yr in range(14, 18, 1):
    with open(DB + str(yr) + '-' + str(yr+1) + '/' + FILENAME, 'r') as json_file:
        data = json.load(json_file)

        for match in data:
            for team in data[match]:
                for name in data[match][team]['Player_stats']:
                    detail = data[match][team]['Player_stats'][name]['player_details']
                    match_stats = data[match][team]['Player_stats'][name]['Match_stats']

                    if detail['player_position_info'] != 'Sub':  # only extract data from starting players
                        # clear some unneeded information
                        detail.pop('player_position_value', None)
                        # detail.pop('player_rating', None)
                        match_stats.pop('formation_place', None)

                        # convert match stats to int
                        match_stats = {k: int(v) for k, v in match_stats.items()}

                        # treat players who've played in more than one position and their stats as "separate players"
                        pid = detail['player_id'] + '-' + detail['player_position_info']

                        if pid not in players.keys():
                            players[pid] = detail
                            players[pid]['player_ratings'] = [float(detail['player_rating'])]
                            players[pid].update(match_stats)
                            players[pid]['list_games_played'] = [match]  # to register how many matches player
                        else:
                            if match not in players[pid]['list_games_played']:
                                players[pid]['list_games_played'].append(match)
                                players[pid]['player_ratings'].append(float(detail['player_rating']))

                                for k, v in match_stats.items():
                                    if k in players[pid] and k != 'f':
                                        players[pid][k] += v

# per game stats
final_players = []   # only players with more than 5 games played
positions = []
ratings = []
for pid, player in players.items():
    n_matches = len(player['list_games_played'])

    if n_matches < 5:
        continue
    else:
        player.pop('list_games_played', None)
        avg_rating = sum([r for r in player['player_ratings']]) / n_matches
        player.pop('player_ratings', None)

        for s in STATS:
            if s in player:
                player[s + '_per_game'] = player[s] / n_matches

        # additional success ratio stats
        if 'accurate_pass' in player and 'total_pass' in player:
            player['passing_rate'] = player['accurate_pass'] / player['total_pass']
        if 'goals' in player and 'total_scoring_att' in player:
            player['goal_per_shot_rate'] = player['goals'] / player['total_scoring_att']
        if 'goal_assist' in player and 'accurate_pass' in player:
            player['assist_rate_per_pass'] = player['goal_assist'] / player['accurate_pass']

        positions.append(player['player_position_info'])
        ratings.append(avg_rating)
        player.pop('player_position_info', None)
        player.pop('player_id')
        player.pop('player_name')
        final_players.append(player)

with open('uk_players_stats.pkl', 'wb') as p:
    pickle.dump(final_players, p)
with open('uk_players_positions.pkl', 'wb') as p:
    pickle.dump(positions, p)
with open('uk_players_avg_ratings.pkl', 'wb') as p:
    pickle.dump(ratings, p)


