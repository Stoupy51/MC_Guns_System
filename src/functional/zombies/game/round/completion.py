""" Ending a round, the dog-round reward and grenade replenishment. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers.probes import Probe
from ....progression import Xp


# Functions
def write_round_completion() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/round_complete", f"""
# -1 stops this from firing again every tick.
scoreboard players set #zb_to_spawn {ns}.data -1

# No Max Ammo fallback here: it drops at the last hound's body (dog_death), never at a player.

function #{ns}:zombies/on_round_end

# Split because only the roster earned the survival XP; the signal above set #xp_gain.
execute store result score #completed_round {ns}.data run data get storage {ns}:zombies game.round
tellraw @a[scores={{{ns}.zb.in_game=1}}] ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"green"}},{{"score":{{"name":"#completed_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" complete! Next round in 5 seconds...","color":"green"}},{Xp.suffix("zb", "round_survived")}]
tellraw @a[scores={{{ns}.zb.in_game=0}}] ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"green"}},{{"score":{{"name":"#completed_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" complete! Next round in 5 seconds...","color":"green"}}]
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/round_end_generic ambient @s ~ ~ ~ 0.3 1.0

schedule function {ns}:v{version}/zombies/start_round 5s

function {ns}:v{version}/zombies/revive/round_respawn
""")

	## #zb_alive only counts materialized dogs, so with portals still telegraphing every late kill looked like the last.
	## Count the live pack without this corpse, plus the portals that have not struck.
	write_versioned_function("zombies/dog_death", f"""
tag @s remove {ns}.zb_dog

scoreboard players operation #zb_dog_left {ns}.data = #zb_dog_pending {ns}.data
scoreboard players operation #zb_dog_left {ns}.data += #zb_to_spawn {ns}.data
execute store result score #zb_dog_alive {ns}.data if entity @e[tag={ns}.zb_dog]
scoreboard players operation #zb_dog_left {ns}.data += #zb_dog_alive {ns}.data

# ammo_done also covers two hounds dying in the same tick.
execute if score #zb_dog_left {ns}.data matches ..0 if score #zb_dog_ammo_done {ns}.data matches 0 run function {ns}:v{version}/zombies/dog_max_ammo_at_self
""")

	## Run as the last hound where it died. A fixed reward, so it skips the shuffle bag and the drop roll.
	write_versioned_function("zombies/dog_max_ammo_at_self", f"""
scoreboard players set #zb_dog_ammo_done {ns}.data 1
scoreboard players add #pu_uid {ns}.data 1
data modify storage {ns}:temp _pu_spawn set value {{x:0,y:0,z:0,uid:0,type:"max_ammo"}}
{Probe.pos()}
data modify storage {ns}:temp _pu_spawn.x set from storage {ns}:temp _probe_pos[0]
data modify storage {ns}:temp _pu_spawn.y set from storage {ns}:temp _probe_pos[1]
data modify storage {ns}:temp _pu_spawn.z set from storage {ns}:temp _probe_pos[2]
execute store result storage {ns}:temp _pu_spawn.uid int 1 run scoreboard players get #pu_uid {ns}.data
function {ns}:v{version}/zombies/powerups/spawn_display with storage {ns}:temp _pu_spawn
""")

	write_versioned_function("zombies/start_round", f"""
# +2, capped at 4.
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:v{version}/zombies/inventory/replenish_grenades
""")

	## Run every 5 s once 60 s passed since the last spawn: zombies more than 32 blocks from every player glow for 6 s.
	write_versioned_function("zombies/glow_stuck_zombies", f"""
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run tag @e[tag={ns}.zombie_round,distance=..32] add {ns}.zb_near_player

effect give @e[tag={ns}.zombie_round,tag=!{ns}.zb_near_player] glowing 6 0 true

tag @e[tag={ns}.zb_near_player] remove {ns}.zb_near_player
""")

