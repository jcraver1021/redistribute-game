from ngame import *
from tester import rotate_strategies


def winnings_total(players):
    # type: (List[Player]) -> str
    """Sum the winnings of all players"""
    return 'Total: ${}'.format(sum(map(lambda p: p.winnings, players)))


def print_players(players):
    # type: (List[Player]) -> None
    """Print the winnings of the players"""
    for player in players:
        print(player)
    print(winnings_total(players))
    print()


# This is our mechanism for this game; punish payers who repeat their strategies
def repeat_mechanism(payoff, players, game, penalty=lambda x: x):
    # type: (np.array, List[Player], NPlayerGame, Optional[Callable]) -> np.array
    """Punish players for repeating their strategy"""
    x = np.copy(payoff)
    for i, player in enumerate(players):
        history = player.history[game][i]
        n = len(history)
        j = n - 2
        while n > 0 and j >= 0 and history[-1] == 0 and history[-1] == history[j]:
            j -= 1
        x[i] -= penalty(n - j - 2)
    return x


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

strategy_home = build_strategy(2, BuildMode.PURE, i=0)
strategy_away = build_strategy(2, BuildMode.PURE, i=1)
strategy_mixed = build_strategy(2, BuildMode.UNIFORM)

print("Mixed: No Mechanism")
players = Player.make_n_players(3, names)
rotate_strategies(game, players, [[strategy_mixed]] * 3, 1000)
print_players(players)

print("Mixed: Repeat Mechanism")
players = Player.make_n_players(3, names)
rotate_strategies(game, players, [[strategy_mixed]] * 3, 1000, mechanism=repeat_mechanism)
print_players(players)

print("Staying Home: No Mechanism")
players = Player.make_n_players(3, names)
rotate_strategies(game, players, [[strategy_home]] * 3, 1000)
print_players(players)

print("Staying Home: Repeat Mechanism")
players = Player.make_n_players(3, names)
rotate_strategies(game, players, [[strategy_home]] * 3, 1000, mechanism=repeat_mechanism)
print_players(players)

rotation = [
    [
        strategy_away,
    ],
    [
        strategy_home,
        strategy_away
    ],
    [
        strategy_away,
        strategy_home
    ]
]

print("Two-Day Rotation: No Mechanism")
players = Player.make_n_players(3, names)
rotate_strategies(game, players, rotation, 1000)
print_players(players)

print("Two-Day Rotation: Repeat Mechanism")
players = Player.make_n_players(3, names)
rotate_strategies(game, players, rotation, 1000, mechanism=repeat_mechanism)
print_players(players)

rotation = [
    [
        strategy_home,
        strategy_away,
    ],
    [
        strategy_away,
        strategy_home,
        strategy_away,
        strategy_away
    ],
    [
        strategy_away,
        strategy_home,
        strategy_away,
        strategy_away
    ]
]

print("Four-Day Rotation: No Mechanism")
players = Player.make_n_players(3, names)
rotate_strategies(game, players, rotation, 1000)
print_players(players)

print("Four-Day Rotation: Repeat Mechanism")
players = Player.make_n_players(3, names)
rotate_strategies(game, players, rotation, 1000, mechanism=repeat_mechanism)
print_players(players)

rotation = [
    [
        strategy_home,
        strategy_away,
        strategy_home
    ],
    [
        strategy_away,
        strategy_away,
        strategy_away,
        strategy_away,
        strategy_home,
        strategy_away
    ],
    [
        strategy_away,
        strategy_home,
        strategy_away,
        strategy_away,
        strategy_away,
        strategy_away
    ]
]
print("Six-Day Rotation: No Mechanism")
players = Player.make_n_players(3, names)
rotate_strategies(game, players, rotation, 1000)
print_players(players)

print("Six-Day Rotation: Repeat Mechanism")
players = Player.make_n_players(3, names)
rotate_strategies(game, players, rotation, 1000, mechanism=repeat_mechanism)
print_players(players)
