from ngame import *


def try_game(game, players, strategies, n=1):
    """Teach players a game and then run it"""
    for i in range(len(players)):
        players[i].learn(game, i, strategies[i])
    game.run(players, n)


def winnings_total(players):
    """Sum the winnings of all players"""
    return sum(map(lambda p: p.winnings, players))

# Scenario: Players 1 and 2 want to use a resource.
#   Each gains 0 if they do not attempt to access it, 1 if they get sole access,
#   and -1 if they attempt to access it together.


# Build the game
game = NPlayerGame(np.array([0, 0, 0, 1, 1, 0, -1, -1]).reshape((2, 2, 2)))
print(game.payoff.shape)

# The equilibrium points consist of combinations of 3 strategies:
choose_first = build_strategy(2, BuildMode.PURE, i=0)
choose_last = build_strategy(2, BuildMode.PURE, i=1)
mixed = build_strategy(2, BuildMode.UNIFORM)

# There are 4 equilibrium points:
settings = [
    [choose_first, choose_first],
    [choose_first, choose_last],
    [choose_last, choose_first],
    [mixed, mixed]
]

# See how the equilibria pan out for each player
for setting in settings:
    players = Player.make_n_players(2)
    try_game(game, players, setting, 100)
    print('Setting: {}'.format(setting))
    for i, player in enumerate(players):
        print('Player {} winnings: {}'.format(i, player.winnings))
    print('Total winnings: {}'.format(winnings_total(players)))
    print()

# Now compare it to an artificial solution
# Each player will go when they are first, but we will alternate positions each time
players = Player.make_n_players(2)
for player in players:
    player.learn(game, 0, choose_first)
    player.learn(game, 1, choose_last)
for _ in range(100):
    game.run(players)
    players.reverse()

print('Alternating Usage')
for i, player in enumerate(players):
    print('Player {} winnings: {}'.format(i, player.winnings))
print('Total winnings: {}'.format(winnings_total(players)))
