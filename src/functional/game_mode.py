
# Shared base for the three "game modes" (multiplayer, zombies, missions).
#
# These three subsystems each emit a full game lifecycle (start/stop/join/spawns/
# teleport/sidebar/prep). An audit of the *generated* output (see REFACTOR_PLAN.md, P4)
# showed their bodies genuinely diverge — multiplayer is team-based, zombies/missions are
# not, and each has distinct mechanics — so only the functions that are byte-identical
# across modes live here. The rest stay as mode-specific methods on the subclasses.
#
# Truly shared (identical generated output modulo the mode segment):
#   - <mode>/tp_player_at        : the spawn teleport macro
#   - <mode>/summon_spawn_at      : the spawn marker (zombies adds one extra tag)
from .generator import McfunctionGenerator


class GameMode(McfunctionGenerator):
    """ Base for a full game-mode generator (multiplayer / zombies / missions).

    Subclasses set :attr:`mode` (the namespace path + storage segment, e.g. ``"zombies"``)
    and implement :meth:`generate`, calling the shared lifecycle helpers below for the
    functions that are identical across modes. Mode-specific functions remain methods on
    the subclass.
    """

    #: Path/storage segment for this mode, e.g. "multiplayer" | "zombies" | "missions".
    mode: str = ""

    def write_tp_player_at(self) -> None:
        """ Write ``<mode>/tp_player_at`` — the macro that teleports @s to a spawn
        position and yaw. Identical across all modes. """
        self.func(f"{self.mode}/tp_player_at", "$tp @s $(x) $(y) $(z) $(yaw) 0")

    def write_summon_spawn_at(self, extra_spawn_tags: tuple[str, ...] = ()) -> None:
        """ Write ``<mode>/summon_spawn_at`` — the macro that summons a spawn-point marker.

        Args:
            extra_spawn_tags: extra tag suffixes (without the ``<ns>.`` prefix) to add to
                the marker. Zombies passes ``("new_spawn",)``; multiplayer/missions pass none.
        """
        ns: str = self.ns
        tags: str = f'"{ns}.spawn_point","$(tag)","{ns}.gm_entity"'
        for tag in extra_spawn_tags:
            tags += f',"{ns}.{tag}"'
        self.func(f"{self.mode}/summon_spawn_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:[{tags}],data:{{yaw:$(yaw)}}}}
""")
