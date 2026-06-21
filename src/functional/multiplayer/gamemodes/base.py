
# Base class for the five multiplayer game-mode variants (FFA, TDM, DOM, HP, SnD).
#
# Every variant emits functions under `multiplayer/gamemodes/<key>/...` and shares the
# same lifecycle contract (at minimum: setup, tick, on_kill, cleanup; plus mode-specific
# helpers). `GameModeVariant` removes the per-file `ns`/`version` boilerplate and the
# repeated `multiplayer/gamemodes/<key>/` path prefix.
from stewbeet import write_versioned_function

from ...generator import McfunctionGenerator


class GameModeVariant(McfunctionGenerator):
    """ Abstract base for a single multiplayer game-mode (strategy plugged into the mode).

    Subclasses set :attr:`key` (e.g. ``"tdm"``) and implement :meth:`generate`, writing
    their functions via :meth:`sub`, which prepends the shared
    ``multiplayer/gamemodes/<key>/`` path so each variant only names the leaf function.
    """

    #: Short identifier used in the function path (e.g. "ffa", "tdm", "dom", "hp", "snd").
    key: str = ""

    @property
    def prefix(self) -> str:
        """ The shared versioned path prefix for this variant's functions. """
        return f"multiplayer/gamemodes/{self.key}"

    def sub(self, name: str, body: str) -> None:
        """ Write one of this variant's functions at ``<prefix>/<name>``. """
        write_versioned_function(f"{self.prefix}/{name}", body)
