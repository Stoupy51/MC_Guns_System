""" Every recorded stat, per mode, and the per-player objectives a username change carries over. """
# Imports
from dataclasses import dataclass

from ..multiplayer.gamemodes.dispatch import GAMEMODES


# Classes
@dataclass(frozen=True)
class PlayerStat:
	""" One stat: a score per player, copied into `mgs:stats players."<uuid>".<mode>.<key>` by the snapshot.

	>>> PlayerStat(key="doors", label="Doors opened", objective="mgs.st.zb.doors").owned
	True
	>>> PlayerStat(key="kills", label="Kills", objective="mgs.adv.zb.kills").owned
	False
	"""
	key: str
	label: str
	objective: str
	sources: tuple[str, ...] = ()
	""" Award keys of the mode's XP side whose `award_<key>` function adds 1; empty when a site of its own feeds it. """
	scale: int = 1
	""" Shown value per unit, ex: 100 for a counter of hundreds of points. """

	@property
	def owned(self) -> bool:
		""" Declared and fed by this feature, rather than borrowed from the challenges or the levels. """
		return self.objective.startswith("mgs.st.")


@dataclass(frozen=True)
class StatMode:
	""" A mode's stats, and where its game state lives. """
	key: str
	""" Storage key and objective segment: `zb`, `mp` or `mi`. """
	label: str
	award_side: str
	""" XP side whose award functions feed `PlayerStat.sources`; Missions pays into the multiplayer side. """
	storage: str
	""" `mgs:<storage> game.state` is "active" while a game runs. """
	stats: tuple[PlayerStat, ...]

	@property
	def in_game(self) -> str:
		return f"mgs.{self.key}.in_game"

	def stat(self, key: str) -> PlayerStat:
		""" The row of one stat, ex: `ZOMBIES.stat("downs")`. """
		return next(stat for stat in self.stats if stat.key == key)


# Constants
ZOMBIES: StatMode = StatMode(key="zb", label="Zombies", award_side="zb", storage="zombies", stats=(
	PlayerStat(key="games",         label="Games played",       objective="mgs.st.zb.games", sources=("game_over",)),
	PlayerStat(key="rounds",        label="Rounds survived",    objective="mgs.st.zb.rounds"),
	PlayerStat(key="best_round",    label="Best round",         objective="mgs.adv.zb.best_round"),
	PlayerStat(key="kills",         label="Kills",              objective="mgs.adv.zb.kills"),
	PlayerStat(key="headshots",     label="Headshots",          objective="mgs.adv.zb.headshots"),
	PlayerStat(key="downs",         label="Downs",              objective="mgs.st.zb.downs"),
	PlayerStat(key="deaths",        label="Bleed-outs",         objective="mgs.st.zb.deaths"),
	PlayerStat(key="revives",       label="Revives",            objective="mgs.adv.zb.revives"),
	PlayerStat(key="points_earned", label="Points earned",      objective="mgs.st.zb.points_earned"),
	PlayerStat(key="points_spent",  label="Points spent",       objective="mgs.adv.zb.spending", scale=100),
	PlayerStat(key="doors",         label="Doors opened",       objective="mgs.st.zb.doors", sources=("door",)),
	PlayerStat(key="boxes",         label="Mystery boxes",      objective="mgs.st.zb.boxes"),
	PlayerStat(key="wallbuys",      label="Wall weapons bought", objective="mgs.st.zb.wallbuys"),
	PlayerStat(key="perks",         label="Perks",              objective="mgs.adv.zb.perks"),
	PlayerStat(key="pap",           label="Pack-a-Punch",       objective="mgs.adv.zb.pap"),
	PlayerStat(key="traps",         label="Traps",              objective="mgs.st.zb.traps", sources=("trap",)),
	PlayerStat(key="powerups",      label="Power-ups",          objective="mgs.st.zb.powerups", sources=("powerup",)),
	PlayerStat(key="barricades",    label="Barricades repaired", objective="mgs.st.zb.barricades", sources=("barricade",)),
	PlayerStat(key="power",         label="Power turned on",    objective="mgs.st.zb.power", sources=("power",)),
	PlayerStat(key="time",          label="Time played",        objective="mgs.st.zb.time"),
))
MULTIPLAYER: StatMode = StatMode(key="mp", label="Multiplayer", award_side="mp", storage="multiplayer", stats=(
	PlayerStat(key="games",      label="Games played", objective="mgs.st.mp.games", sources=("match_win", "match_loss")),
	PlayerStat(key="wins",       label="Wins",         objective="mgs.adv.mp.wins"),
	PlayerStat(key="losses",     label="Losses",       objective="mgs.st.mp.losses", sources=("match_loss",)),
	PlayerStat(key="kills",      label="Kills",        objective="mgs.adv.mp.kills"),
	PlayerStat(key="deaths",     label="Deaths",       objective="mgs.st.mp.deaths"),
	PlayerStat(key="headshots",  label="Headshots",    objective="mgs.adv.mp.headshots"),
	PlayerStat(key="captures",   label="Captures",     objective="mgs.st.mp.captures", sources=("dom_capture", "hp_capture")),
	PlayerStat(key="plants",     label="Bomb plants",  objective="mgs.st.mp.plants", sources=("bomb_plant",)),
	PlayerStat(key="defuses",    label="Bomb defuses", objective="mgs.st.mp.defuses", sources=("bomb_defuse",)),
	PlayerStat(key="objectives", label="Objectives",   objective="mgs.adv.mp.objectives"),
	PlayerStat(key="time",       label="Time played",  objective="mgs.st.mp.time"),
))
MISSIONS: StatMode = StatMode(key="mi", label="Missions", award_side="mp", storage="missions", stats=(
	PlayerStat(key="games",     label="Missions played", objective="mgs.st.mi.games"),
	PlayerStat(key="completed", label="Completed",       objective="mgs.adv.mi.completed"),
	PlayerStat(key="kills",     label="Kills",           objective="mgs.adv.mi.kills"),
	PlayerStat(key="headshots", label="Headshots",       objective="mgs.st.mi.headshots", sources=("mission_headshot",)),
	PlayerStat(key="deaths",    label="Deaths",          objective="mgs.st.mi.deaths"),
	PlayerStat(key="time",      label="Time played",     objective="mgs.st.mi.time"),
))
MODES: tuple[StatMode, ...] = (ZOMBIES, MULTIPLAYER, MISSIONS)
""" In dialog order; a mode's index is its offset in `TRIG_PLAYER_STATS_BASE` values. """

GAMEMODE_NAMES: dict[str, str] = {
	"ffa": "Free For All", "tdm": "Team Deathmatch", "dom": "Domination",
	"hp": "Hardpoint", "snd": "Search and Destroy", "demo": "Demolition",
}
""" Display name of every id of `GAMEMODES`, for the per-gamemode games and wins. """

PERSISTENT_OBJECTIVES: tuple[str, ...] = (
	"bs.id",
	"mgs.st.index",
	"mgs.mp.xp_total", "mgs.mp.xp_level", "mgs.mp.xp_prog",
	"mgs.zb.xp_total", "mgs.zb.xp_level", "mgs.zb.xp_prog", "mgs.zb.xp_spent_acc",
	"mgs.adv.mp.kills", "mgs.adv.mp.headshots", "mgs.adv.mp.wins", "mgs.adv.mp.objectives",
	"mgs.adv.zb.kills", "mgs.adv.zb.headshots", "mgs.adv.zb.best_round", "mgs.adv.zb.revives",
	"mgs.adv.zb.perks", "mgs.adv.zb.pap", "mgs.adv.zb.box", "mgs.adv.zb.spending",
	"mgs.adv.mi.kills", "mgs.adv.mi.completed",
	"mgs.player.hitmarker", "mgs.player.damage_debug",
	"mgs.mp.class", "mgs.mp.default", "mgs.mp.pid", "mgs.zb.passive", "mgs.zb.ability", "mgs.zb.knife_camo",
	*(stat.objective for mode in MODES for stat in mode.stats if stat.owned),
	*(f"mgs.st.mp.{gamemode}.{key}" for gamemode in GAMEMODES for key in ("games", "wins")),
)
""" Every score that outlives a game, copied from the old holder to the new one when a player's name changes.
Scores are held by name, so a renamed player would otherwise start over, `mgs.mp.pid` (owner of their custom loadouts) included. """

