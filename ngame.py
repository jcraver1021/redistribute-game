import numpy as np

from enum import Enum
from typing import Any, Dict, Callable, List, Optional


def _normalize(x, order=1.0):
    # type: (np.array, Optional[float]) -> np.array
    """
    Normalize a numpy array using the given l-norm

    Args:
        x: a numpy array
        order: which l-norm to use (default 1)
    Returns:
        The array normalized. Returns the original if it is magnitude 0.
    """
    magnitude = np.linalg.norm(x, ord=order)
    if magnitude != 0:
        return x / magnitude
    else:
        return x


class BuildMode(Enum):
    """
    Modes of building a player's strategy vector
    """
    PURE = 0
    UNIFORM = 1
    RANDOM = 2


class Player:
    def __init__(self, strategies):
        # type: (np.array) -> None
        """
        Initialize a player with a set of strategies, 0 winnings, and an empty history.

        Args:
            strategies: A numpy array representing the probability that this player will use
                each strategy at their disposal
        Raises:
            ValueError if the vector is not 1-dimensional or the l-1 magnitude of the
                strategy vector is not close to 1
        """
        if len(strategies.shape) != 1:
            raise ValueError('Strategy should be a vector but has shape {}'.format(strategies.shape))
        magnitude = np.linalg.norm(strategies, ord=1)
        if not np.isclose(magnitude, 1):
            raise ValueError('Strategy vector is magnitude {}, not 1'.format(magnitude))

        self.strategies = strategies  # type: np.array

        # Accounts maintained on player level
        self.winnings = 0.0  # type: float
        self.history = []  # type: List[int]

    # Maps build mode to method
    _build_method = {
        BuildMode.PURE: lambda n, i: np.array([1 if j == i else 0 for j in range(n)]),
        BuildMode.UNIFORM: lambda n: _normalize(np.ones(n)),
        BuildMode.RANDOM: lambda n: _normalize(np.random.random(n))
    }  # type: Dict[BuildMode, Callable]

    @classmethod
    def build_player(cls, n, mode, **kwargs):
        # type: (int, BuildMode, Optional[Dict[Any, Any]]) -> Player
        """
        Build a player using the specified build mode

        Args:
            n: number of strategies the player has
            mode: the build mode to use
            kwargs: Optional arguments
                PURE: requires i (int)
        """
        return Player(Player._build_method[mode](n, **kwargs))

    def play(self):
        # type: () -> int
        """
        Choose a strategy based on the stored probabilities.

        Choice of strategy is appended to personal history.
        """
        self.history.append(np.random.choice(len(self.strategies), p=self.strategies))
        return self.history[-1]

    def pay(self, winnings):
        # type: (float) -> None
        """
        Add the new winnings to the total

        Args:
            winnings: The amount won from the last game
        """
        self.winnings += winnings


class NPlayerGame:
    def __init__(self, payoff, players):
        """
        An N-Player game based on a set n+1-dimensional array.
        The number of players and the number of strategies each player has are interpreted solely
        from the shape of the array.

        The first N dimensions represent the player strategies
        The last dimension is the payoff to each player.

        Args:
            payoff: A n-dimensional array representing the payoffs to each player
        Raises:
            ValueError if the final dimension is not equal to the length of the array's shape minus 1
        """

        n = len(payoff.shape) - 1
        if n != payoff.shape[-1]:
            raise ValueError(
                'Shape of strategy product is {}; final dimension should be {}, not {}'.format(
                    payoff.shape[:-1], n, payoff.shape[-1]))

        if len(players) != n:
            raise ValueError(
                'The game is for {} players, but the number of players is {}'.format(n, len(players)))

        self.payoff = payoff  # type: np.array
        self.n = n  # type: int
        self.players = players  # type: List[Player]

    def run(self, n=1):
        # type: (Optional[int]) -> None
        """
        Run the game n times

        Args:
            n: times to run the game
        """
        for _ in range(n):
            plays = tuple(player.play() for player in self.players)
            for player, winnings in zip(self.players, self.payoff[plays]):
                player.pay(winnings)


if __name__ == '__main__':
    A = np.random.random((5, 6, 7, 3)) - 0.5
    P = [Player.build_player(3, BuildMode.RANDOM) for _ in range(3)]
    game = NPlayerGame(A, P)
    print('Game:\n{}'.format(game.payoff))
    game.run(20)
    for i, p in enumerate(P):
        print('Player {} has {}'.format(i, p.winnings))
        print('Player {} played {}'.format(i, p.history))

