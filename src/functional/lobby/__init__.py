""" The public lobby: players queue for a mode, vote for its game and map, and play with no operator around.

Off until an operator enables it from the configuration menu. The three modes run side by side, each with its own queue and vote.
"""
# Imports
from stewbeet import Mem, write_load_file, write_tick_file

from .admin import write_lobby_admin
from .players import write_lobby_players, write_queue_players
from .queues import queues
from .vote import write_queue_vote, write_vote_helpers


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## queue: 0 none, else the queue id. choice: the slot voted for. seen: the last second a player was online, #now being the current one.
	write_load_file(f"""
scoreboard objectives add {ns}.lobby.queue dummy
scoreboard objectives add {ns}.lobby.choice dummy
scoreboard objectives add {ns}.lobby.vote trigger
scoreboard objectives add {ns}.lobby.seen dummy
""")
	write_tick_file(f"execute if score #public_lobby {ns}.config matches 1 run function {ns}:v{version}/lobby/tick")

	write_vote_helpers()
	for queue in queues():
		write_queue_vote(queue)
		write_queue_players(queue)
	write_lobby_players()
	write_lobby_admin()

