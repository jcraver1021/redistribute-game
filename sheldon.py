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


game = NPlayerGame(
    np.array(
        [1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 4, 4,
         -4, 1, 1, 4, 1, -4, 4, -4, 1, 6, -4, -4]).reshape((2, 2, 2, 3)))

mixed = build_strategy(2, BuildMode.UNIFORM)
players = Player.make_n_players(3, names)
for i, player in enumerate(players):
    player.learn(game, i, mixed)

print('Random Sheldon')
game.run(players, 1000)
for player in players:
    print(player)
print(winnings_total(players))

stayhome = build_strategy(2, BuildMode.PURE, i=0)
players = Player.make_n_players(3, names)
for i, player in enumerate(players):
    player.learn(game, i, stayhome)

print('Stay at home')
game.run(players, 1000)
for player in players:
    print(player)
print(winnings_total(players))

party = build_strategy(2, BuildMode.PURE, i=1)
players = Player.make_n_players(3, names)
for i, player in enumerate(players):
    player.learn(game, i, stayhome if i == 0 else party)

print('What happens if Sheldon stays home?')
game.run(players, 1000)
for player in players:
    print(player)
print(winnings_total(players))
