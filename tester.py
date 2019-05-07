from ngame import *


def rotate_strategies(game, players, strategies, n, mechanism=identity_mechanism):
    # type: (NPlayerGame, List[Player], List[List[np.array]]], int, Optional[Callable]) -> None
    """Rotate each player through a list of strategies

    Args:
        game: An NPlayerGame instance
        players: A list of Player objects
        strategies: A list of lists of strategies for each player
        n: The number of times to repeat the game
        mechanism: The mechanism to apply to the game
    """
    num_players = len(players)
    indices = [0] * num_players
    for _ in range(n):
        for i in range(num_players):
            players[i].learn(game, i, strategies[i][indices[i]])
            indices[i] += 1
            if indices[i] >= len(strategies[i]):
                indices[i] = 0
        game.run(players, mechanism=mechanism)
