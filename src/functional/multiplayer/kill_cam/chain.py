""" The final kill chain: the final killer's run of kills leading to the kill that ended the match. """
# Imports
from stewbeet import Mem, write_versioned_function

from .shared import CHAIN_GAP, MAX_CHAIN


# Functions
def write_kill_cam_chain() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## The final kill is the last death logged (see kill_cam/start). Leaves #kc_killer, #kc_final_t, #kc_chain_start and #kc_chain_len.
	write_versioned_function("multiplayer/kill_cam/resolve_chain", f"""
execute store result score #kc_killer {ns}.data run data get storage {ns}:kill_cam deaths[-1].killer
execute store result score #kc_final_t {ns}.data run data get storage {ns}:kill_cam deaths[-1].t
execute store result score #kc_oldest {ns}.data run data get storage {ns}:kill_cam frames[0].t
scoreboard players set #kc_chain_len {ns}.data 1
scoreboard players operation #kc_chain_start {ns}.data = #kc_final_t {ns}.data

data modify storage {ns}:temp _kc_walk set from storage {ns}:kill_cam deaths
data remove storage {ns}:temp _kc_walk[-1]
execute if data storage {ns}:temp _kc_walk[0] run function {ns}:v{version}/multiplayer/kill_cam/chain_step
data remove storage {ns}:temp _kc_walk
""")

	## One death back from the chain start: a kill by the killer extends the chain, the killer's own death ends it, any other death is skipped.
	write_versioned_function("multiplayer/kill_cam/chain_step", f"""
execute store result score #kc_t {ns}.data run data get storage {ns}:temp _kc_walk[-1].t
execute if score #kc_t {ns}.data < #kc_oldest {ns}.data run return 0
execute store result score #kc_victim {ns}.data run data get storage {ns}:temp _kc_walk[-1].victim
execute if score #kc_victim {ns}.data = #kc_killer {ns}.data run return 0

# An absent killer reads as 0, which no bs.id is.
execute store result score #kc_by {ns}.data run data get storage {ns}:temp _kc_walk[-1].killer
scoreboard players operation #kc_gap {ns}.data = #kc_chain_start {ns}.data
scoreboard players operation #kc_gap {ns}.data -= #kc_t {ns}.data
execute if score #kc_by {ns}.data = #kc_killer {ns}.data if score #kc_gap {ns}.data matches {CHAIN_GAP + 1}.. run return 0
execute if score #kc_by {ns}.data = #kc_killer {ns}.data run scoreboard players add #kc_chain_len {ns}.data 1
execute if score #kc_by {ns}.data = #kc_killer {ns}.data run scoreboard players operation #kc_chain_start {ns}.data = #kc_t {ns}.data
execute if score #kc_chain_len {ns}.data matches {MAX_CHAIN}.. run return 0

data remove storage {ns}:temp _kc_walk[-1]
execute if data storage {ns}:temp _kc_walk[0] run function {ns}:v{version}/multiplayer/kill_cam/chain_step
""")

