
# Base class for all functional generators.
#
# Every generator in this codebase used to open with the same two lines
# (`ns = Mem.ctx.project_id` / `version = Mem.ctx.project_version`) and then call
# `write_versioned_function(...)` with f-strings full of `{ns}` / `{version}`.
# `Generator` captures that boilerplate once. Subclasses only implement `generate()`.
#
# IMPORTANT: `Mem.ctx` is only valid *during* the beet pipeline, so `ns`/`version` are
# read lazily (as properties), never at import/definition time. Instantiate generators
# inside the wrapper function that runs at generate time, not at module scope.
from abc import ABC, abstractmethod

from stewbeet import (
    Mem,
    write_function,
    write_load_file,
    write_tick_file,
    write_versioned_function,
)


class McfunctionGenerator(ABC):
    """ Base class for objects that emit mcfunctions for the datapack.

    Provides the namespace/version context and thin wrappers around the stewbeet
    `write_*` helpers so subclasses never repeat the `ns`/`version` boilerplate.
    Subclasses implement :meth:`generate`; calling the instance runs it, making an
    instance a drop-in replacement for the old module-level ``main()`` functions.
    """

    @property
    def ns(self) -> str:
        """ The project namespace (e.g. ``"mgs"``), read lazily from the beet context. """
        return Mem.ctx.project_id

    @property
    def version(self) -> str:
        """ The project version string (e.g. ``"5.0.1"``), read lazily from the context. """
        return Mem.ctx.project_version

    def func(self, path: str, body: str, **kwargs: object) -> None:
        """ Write a versioned function at ``<ns>:v<version>/<path>``.

        Thin wrapper around :func:`stewbeet.write_versioned_function`.

        Args:
            path  (str): Versioned function path (without namespace/version prefix).
            body  (str): The mcfunction body.
            kwargs: Forwarded to ``write_versioned_function`` (e.g. ``prepend``, ``tags``).
        """
        write_versioned_function(path, body, **kwargs)  # type: ignore[arg-type]

    def raw_function(self, path: str, body: str, **kwargs: object) -> None:
        """ Write a non-versioned function at the exact ``path`` given (e.g. ``"mgs:config"``).

        Thin wrapper around :func:`stewbeet.write_function`.
        """
        write_function(path, body, **kwargs)  # type: ignore[arg-type]

    def load(self, body: str, **kwargs: object) -> None:
        """ Append (or prepend) lines to the datapack load function. """
        write_load_file(body, **kwargs)  # type: ignore[arg-type]

    def tick(self, body: str, **kwargs: object) -> None:
        """ Append lines to the datapack tick function. """
        write_tick_file(body, **kwargs)  # type: ignore[arg-type]

    @abstractmethod
    def generate(self) -> None:
        """ Emit all functions/tags for this generator. Implemented by subclasses. """
        raise NotImplementedError

    def __call__(self) -> None:
        """ Run :meth:`generate`, so an instance can be used like the old ``main()``. """
        self.generate()
