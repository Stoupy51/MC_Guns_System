
# Base for the five multiplayer game-mode variants (FFA, TDM, DOM, HP, SnD): removes the per-file
# ns/version boilerplate and the repeated `multiplayer/gamemodes/<key>/` path prefix.
from abc import ABC, abstractmethod

from stewbeet import Mem, write_versioned_function


class GameModeVariant(ABC):
    """ Abstract base for a single multiplayer game-mode (a strategy plugged into the mode).

    Subclasses set :attr:`key` (e.g. ``"tdm"``) and implement :meth:`generate`, writing their
    functions via :meth:`sub`, which prepends the shared path so each variant only names the leaf.
    """

    #: Short identifier used in the function path (e.g. "ffa", "tdm", "dom", "hp", "snd").
    key: str = ""

    @property
    def ns(self) -> str:
        """ The project namespace (e.g. ``"mgs"``), read lazily — `Mem.ctx` only exists mid-pipeline. """
        return Mem.ctx.project_id

    @property
    def version(self) -> str:
        """ The project version string (e.g. ``"5.1.0"``). """
        return Mem.ctx.project_version

    @property
    def prefix(self) -> str:
        """ The shared versioned path prefix for this variant's functions. """
        return f"multiplayer/gamemodes/{self.key}"

    def sub(self, name: str, body: str) -> None:
        """ Write one of this variant's functions at ``<prefix>/<name>``. """
        write_versioned_function(f"{self.prefix}/{name}", body)

    @abstractmethod
    def generate(self) -> None:
        """ Emit all functions/tags for this variant. """
        raise NotImplementedError

    def __call__(self) -> None:
        self.generate()
