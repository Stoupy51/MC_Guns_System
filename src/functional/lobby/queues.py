""" The three queues of the public lobby, and the match presets the Multiplayer vote offers. """
# Imports
from dataclasses import dataclass

from stewbeet import Mem

from ..multiplayer.gamemodes.bomb.snd.rounds import WIN_ROUNDS

# Constants
MAX_SLOTS: int = 8
""" Vote options shown at once, the Random slot included. """

FIRST_ROUND_TICKS: int = 400
""" Voting time once the first vote is cast. """

SECOND_ROUND_TICKS: int = 200
""" Voting time of the Multiplayer map round. """

SPEED_UP_TICKS: int = 100
""" Time left once every player of the queue has voted. """

AWAY_SECONDS: int = 600
""" A player offline longer than this logs back in the lobby, and a game with no player online for this long is stopped. """


# Classes
@dataclass(frozen=True)
class Preset:
	""" A Multiplayer match the vote offers: a gamemode and the limits that suit it. """
	gamemode: str
	label: str
	color: str
	description: str
	score_limit: int
	time_limit: int
	min_players: int
	map_field: str
	""" Path of a list a map needs non-empty to be playable in this gamemode, like `domination`. """

	def option_snbt(self) -> str:
		""" The vote option, which also carries what the map round reads. """
		return (
			f'{{label:{{text:"{self.label}",color:"{self.color}"}},hover:{{text:"{self.description}"}},'
			f'gamemode:"{self.gamemode}",score_limit:{self.score_limit},time_limit:{self.time_limit},mode:"multiplayer",field:"{self.map_field}"}}'
		)


@dataclass(frozen=True)
class Queue:
	""" One mode's queue: who waits for it, its vote and how a player leaves its game. """
	mode: str
	""" Storage and function folder of the mode, like `multiplayer`. """
	prefix: str
	""" Score prefix of the mode, like `mp` in `mgs.mp.in_game`. """
	queue_id: int
	""" Value of `mgs.lobby.queue`, also the tens of the vote trigger values. """
	label: str
	emoji: str
	color: str
	min_players: int
	map_field: str
	""" Path of a list a map needs non-empty to be offered, empty for Multiplayer whose presets carry their own. """
	joinable_states: tuple[str, ...]
	leave_lines: str
	""" Run as a player of the game who goes back to the lobby; ends with them out of the game and in the lobby. """

	@property
	def in_game(self) -> str:
		return f"{Mem.ctx.project_id}.{self.prefix}.in_game"

	@property
	def members(self) -> str:
		""" Selector of the online players of this queue, in its game or waiting in the lobby. """
		return f"@a[scores={{{Mem.ctx.project_id}.lobby.queue={self.queue_id}}}]"


PRESETS: list[Preset] = [
	Preset(gamemode="ffa", label="Free For All", color="green", description="First to 30 kills, 10 minutes", score_limit=30, time_limit=12000, min_players=2, map_field="spawning_points.general"),
	Preset(gamemode="tdm", label="Team Deathmatch", color="yellow", description="First team to 50 kills, 10 minutes", score_limit=50, time_limit=12000, min_players=2, map_field="spawning_points.red"),
	Preset(gamemode="dom", label="Domination", color="aqua", description="First team to 200 points, 10 minutes", score_limit=200, time_limit=12000, min_players=4, map_field="domination"),
	Preset(gamemode="hp", label="Hardpoint", color="dark_purple", description="First team to 200 points, 10 minutes", score_limit=200, time_limit=12000, min_players=4, map_field="hardpoint"),
	Preset(gamemode="snd", label="Search and Destroy", color="gold", description=f"First team to {WIN_ROUNDS} rounds, no respawn", score_limit=30, time_limit=12000, min_players=4, map_field="search_and_destroy"),
	Preset(gamemode="demo", label="Demolition", color="red", description="Destroy both sites, one attack per team", score_limit=30, time_limit=12000, min_players=4, map_field="search_and_destroy"),
]
""" Ten minute matches, with a score a full lobby reaches in about that time. """


# Functions
def queues() -> list[Queue]:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	return [
		Queue(
			mode="multiplayer", prefix="mp", queue_id=1, label="Multiplayer", emoji="⚔", color="red",
			min_players=min(preset.min_players for preset in PRESETS), map_field="",
			joinable_states=("active", "preparing"),
			leave_lines=f"""
function {ns}:v{version}/shared/maps/call_script_at_base {{mode:"multiplayer",script:"leave"}}
function {ns}:v{version}/multiplayer/reset_player
""",
		),
		Queue(
			mode="zombies", prefix="zb", queue_id=2, label="Zombies", emoji="🧟", color="dark_green",
			min_players=1, map_field="spawning_points.players",
			joinable_states=("active",),
			leave_lines=f"function {ns}:v{version}/zombies/reset_player",
		),
		Queue(
			mode="missions", prefix="mi", queue_id=3, label="Missions", emoji="🎯", color="gold",
			min_players=1, map_field="spawning_points.mission",
			joinable_states=("active",),
			leave_lines=f"function {ns}:v{version}/missions/reset_player",
		),
	]

