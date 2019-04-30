from ngame import *


def try_game(game, players, strategies, n=1):
    """Teach players a game and then run it"""
    for i in range(len(players)):
        players[i].learn(game, i, strategies[i])
    game.run(players, n)


def winnings_total(players):
    """Sum the winnings of all players"""
    return 'Total: ${}'.format(sum(map(lambda p: p.winnings, players)))


names = ['Sheldon', 'Raj', 'Leonard']


game_payoff = np.ones((2, 2, 2, 3))
game_payoff[0, 0, 1] = [1, 1, -1]
game_payoff[0, 1, 0] = [1, -1, 1]
game_payoff[1, 0, 0] = [-4, 1, 1]
game_payoff[1, 1, 0] = [4, -4, 1]
game_payoff[1, 0, 1] = [4, 1, -4]
game_payoff[0, 1, 1] = [1, 4, 4]
game_payoff[1, 1, 1] = [6, -4, -4]
game = NPlayerGame(game_payoff)

print('Random Sheldon')
mixed = build_strategy(2, BuildMode.UNIFORM)
players = Player.make_n_players(3, names)
for i, player in enumerate(players):
    player.learn(game, i, mixed)
game.run(players, 1000)
for player in players:
    print(player)
print(winnings_total(players))
print()

print('Stay at home')
stayhome = build_strategy(2, BuildMode.PURE, i=0)
players = Player.make_n_players(3, names)
for i, player in enumerate(players):
    player.learn(game, i, stayhome)
game.run(players, 1000)
for player in players:
    print(player)
print(winnings_total(players))
print()

print('What happens if Sheldon stays home?')
party = build_strategy(2, BuildMode.PURE, i=1)
players = Player.make_n_players(3, names)
for i, player in enumerate(players):
    player.learn(game, i, stayhome if i == 0 else party)
game.run(players, 1000)
for player in players:
    print(player)
print(winnings_total(players))
print()

print('What happens if everyone else stays home?')
players = Player.make_n_players(3, names)
for i, player in enumerate(players):
    player.learn(game, i, stayhome if i != 0 else party)
game.run(players, 1000)
for player in players:
    print(player)
print(winnings_total(players))
print()


# This is our mechanism for this game; punish payers who repeat their strategies
def repeat_mechanism(payoff, players, game, penalty=lambda x: x):
    # type: (np.array, List[Player], NPlayerGame) -> np.array
    """Punish players for repeating their strategy"""
    x = np.copy(payoff)
    for i, player in enumerate(players):
        history = player.history[game][i]
        n = len(history)
        j = n - 2
        while n > 0 and j >= 0 and history[-1] == history[j]:
            j -= 1
        x[i] -= penalty(n - j - 2)
    return x


# Now try random
print('Random Sheldon')
players = Player.make_n_players(3, names)
for i, player in enumerate(players):
    player.learn(game, i, mixed)
game.run(players, 1000, mechanism=repeat_mechanism)
for player in players:
    print(player)
print(winnings_total(players))
print()

# And party
print('What happens if Sheldon stays home?')
players = Player.make_n_players(3, names)
for i, player in enumerate(players):
    player.learn(game, i, stayhome if i == 0 else party)
game.run(players, 1000, mechanism=repeat_mechanism)
for player in players:
    print(player)
print(winnings_total(players))
print()

# The strategy now is to do whichever option hurts less
print('Try to deal with the mechanism')
players = Player.make_n_players(3, names)
for i in range(1000):
    for j, player in enumerate(players):
        player.learn(game, j, stayhome)
        if i > 0:
            player.history[game][j].append(0)
            if j == 0:
                worst_case = -4
            else:
                worst_case = -1
            potential = repeat_mechanism(np.ones(3), players, game)[j]
            if potential < worst_case:
                player.learn(game, j, party)
            elif potential == worst_case:
                player.learn(game, j, mixed)
            player.history[game][j].pop()
    if i % 10 == 0 :
    	if (players[1].strategies[game][1] == players[2].strategies[game][2]).all():
			current_strat = players[1].strategies[game][1]
			player_id = np.random.randint(2) + 1
			players[player_id].learn(game, player_id, np.ones(2) - party)
    game.run(players, mechanism=repeat_mechanism)
for player in players:
    print(player)
print(winnings_total(players))
