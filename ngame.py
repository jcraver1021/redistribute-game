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


_build_method = {
    BuildMode.PURE: lambda n, i: np.array([1 if j == i else 0 for j in range(n)]),
    BuildMode.UNIFORM: lambda n: _normalize(np.ones(n)),
    BuildMode.RANDOM: lambda n: _normalize(np.random.random(n))
}  # type: Dict[BuildMode, Callable]


def build_strategy(n, mode, **kwargs):
    # type: (int, BuildMode, Optional[Dict[Any, Any]]) -> np.array
    """
    Build a player's strategy vector

    Args:
        n: The size of the vector
        mode: Which mode to use when building the vector
        kwargs: Arguments for specific build modes
            PURE: requires i (int), which is the active strategy
    """
    return _build_method[mode](n, **kwargs)


def get_next_name():
    global _calls
    _calls += 1
    return 'Player {}'.format(_calls)


class Player:
    def __init__(self, name):
        # type: (str) -> None
        """
        Initialize a player with 0 winnings and an empty history.

        Args:
            name: Player name
        """

        # State maintained on player level
        self.winnings = 0.0  # type: float
        self.name = name

        # State maintained on game level
        self.strategies = {}  # type: Dict[NPlayerGame, Dict[int, np.array]]
        self.history = {}  # type: Dict[NPlayerGame, Dict[int, List[int]]]

    @classmethod
    def make_n_players(cls, n, names=None):
        # type: (int) -> List[Player]
        """
        Make a list of n players

        Args:
            n: Number of players to make
            names: Player names (must be iterable of length n)
        Return:
            List of new players
        """
        if names:
            if len(names) != n:
                raise(ValueError('{} names were given, but the number of players is {}'.format(len(names), n)))
            return [Player(name) for name in names]
        else:
            return [Player('Player {}'.format(i)) for i in range(n)]

    def learn(self, game, i, strategy):
        # type: (NPlayerGame, int, np.array) -> None
        """
        Learn (or relearn) a strategy for a game

        Args:
            game: The NPlayerGame this strategy applies to
            i: Which player you are in this setting
            strategy: A numpy array representing the probability that this player will use
                each strategy at their disposal
        Raises:
            ValueError if the vector is not 1-dimensional or the l-1 magnitude of the
                strategy vector is not close to 1
        """
        if len(strategy.shape) != 1:
            raise ValueError('Strategy should be a vector but has shape {}'.format(strategy.shape))
        magnitude = np.linalg.norm(strategy, ord=1)
        if not np.isclose(magnitude, 1):
            raise ValueError('Strategy vector is magnitude {}, not 1'.format(magnitude))

        if game not in self.strategies:
            self.strategies[game] = {}
            self.history[game] = {}
        self.strategies[game][i] = strategy
        # You can relearn strategies, but we want to remember what you did
        if i not in self.history[game]:
            self.history[game][i] = []

    def play(self, game, i):
        # type: (NPlayerGame, int) -> int
        """
        Choose a strategy based on the stored probabilities for that game.

        Choice of strategy is appended to personal history.

        Args:
            game: The NPlayerGame instance to play
            i: Which player you are in this setting
        """
        strategies = self.strategies[game][i]
        self.history[game][i].append(np.random.choice(len(strategies), p=strategies))
        return self.history[game][i][-1]

    def pay(self, winnings):
        # type: (float) -> None
        """
        Add the new winnings to the total

        Args:
            winnings: The amount won from the last game
        """
        self.winnings += winnings

    def __str__(self):
        return '{}: ${}'.format(self.name, self.winnings)


def identity_mechanism(x, y, z):
    # type: (Any, Any, Any) -> Any
    return x


class NPlayerGame:
    def __init__(self, payoff):
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

        self.payoff = payoff  # type: np.array
        self.n = n  # type: int

    def run(self, players, n=1, mechanism=identity_mechanism):
        # type: (List[Player], Optional[int], Optional[Callable]) -> None
        """
        Run the game n times

        Args:
            players: Players playing the game
            n: times to run the game
            mechanism: mechanism to adjust payoff based on other factors
        """
        if len(players) != self.n:
            raise ValueError(
                'The game is for {} players, but the number of players is {}'.format(self.n, len(players)))

        for i in range(n):
            plays = tuple(player.play(self, j) for j, player in enumerate(players))
            payoff = mechanism(self.payoff[plays], players, self)
            for player, winnings in zip(players, payoff):
                player.pay(winnings)


if __name__ == '__main__':
    A = np.random.random((5, 6, 7, 3)) - 0.5
    game = NPlayerGame(A)
    P = Player.make_n_players(A.shape[-1])
    for i, p in enumerate(P):
        p.learn(game, i, build_strategy(A.shape[i], BuildMode.RANDOM))
    print('Game:\n{}'.format(game.payoff))
    game.run(P, 20)
    for i, p in enumerate(P):
        print(p)
        print('{} played {}'.format(p.name, p.history))

