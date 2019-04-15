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
        Initialize a player with a set of strategies

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

        self.strategies = strategies

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
        Choose a strategy based on the stored probabilities
        """
        return np.random.choice(len(self.strategies), p=self.strategies)


class NPlayerGame:
    def __init__(self, payoff):
        """
        An N-Player game based on a set n+1-dimensional array.
        The number of players and the number of strategies each player has are interpreted solely
        from the shape of the array.

        The first N dimensions represent the player strategies
        The last dimension is the

        Args:
            payoff: A n-dimensional array representing the payoffs to each player
        Raises:
            ValueError if the final dimension is not equal to the length of the array's shape minus 1
        """

        if len(payoff.shape) != payoff.shape[-1] + 1:
            raise ValueError(
                'Shape of strategy product is {}; final dimension should be {}, not {}'.format(
                    payoff.shape[:-1], len(payoff.shape) - 1, payoff.shape[-1]))

        self.payoff = payoff  # type: np.array
        self.n = len(payoff.shape) - 1  # type: int
        self.winnings = np.zeros(self.n)  # type: np.array
        # TODO: This should really be moved to a factory method; please do so and then have constructor check sizes
        self.players = list(map(
            lambda strategies: Player.build_player(strategies, BuildMode.RANDOM),
            payoff.shape[:-1]))  # type: List[Player]

    def run(self, n=1):
        # type: (Optional[int]) -> None
        """
        Run the game n times

        Args:
            n: times to run the game
        """
        for _ in range(n):
            self.winnings += self.payoff[tuple(player.play() for player in self.players)]


if __name__ == '__main__':
    A = np.random.random((5, 6, 7, 3))
    game = NPlayerGame(A)
    game.run(20)
    print(game.winnings)

