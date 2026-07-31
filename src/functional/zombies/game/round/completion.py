""" Ending a round, the dog-round reward and grenade replenishment. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....progression import Xp


# Functions
def write_round_completion() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Round Completion.

	write_versioned_function("zombies/round_complete", f"""
# Guard: prevent re-triggering every tick
scoreboard players set #zb_to_spawn {ns}.data -1

# NOTE: no Max Ammo fallback here on purpose. The drop belongs at the last hound's body, so it is
# only ever spawned by dog_death. A round that ends without one (Nuke, death watch missed) simply
# doesn't get it — better than granting it at a player, which reads as an automatic refill.

# Signal round end
function #{ns}:zombies/on_round_end

# Announce. Split because only the roster earned the survival XP; #xp_gain was set by the signal above.
execute store result score #completed_round {ns}.data run data get storage {ns}:zombies game.round
tellraw @a[scores={{{ns}.zb.in_game=1}}] ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"green"}},{{"score":{{"name":"#completed_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" complete! Next round in 5 seconds...","color":"green"}},{Xp.suffix("zb", "round_survived")}]
tellraw @a[scores={{{ns}.zb.in_game=0}}] ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"green"}},{{"score":{{"name":"#completed_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" complete! Next round in 5 seconds...","color":"green"}}]
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/round_end_generic ambient @s ~ ~ ~ 0.3 1.0

# Schedule next round after 5 seconds
schedule function {ns}:v{version}/zombies/start_round 5s

# Respawn all bled-out (spectator) players for the next round
function {ns}:v{version}/zombies/revive/round_respawn
""")

	## Dog death.
	# #zb_alive is the wrong thing to test here, since it only counts materialized dogs.
	# Once #zb_to_spawn hits 0 with portals still telegraphing it reads 1 while several hounds are inbound.
	# That made each of the last few kills look like "the last one".
	## Count the live pack directly instead, after dropping this corpse out of it, and add the portals that haven't struck.
	write_versioned_function("zombies/dog_death", f"""
tag @s remove {ns}.zb_dog

scoreboard players operation #zb_dog_left {ns}.data = #zb_dog_pending {ns}.data
scoreboard players operation #zb_dog_left {ns}.data += #zb_to_spawn {ns}.data
execute store result score #zb_dog_alive {ns}.data if entity @e[tag={ns}.zb_dog]
scoreboard players operation #zb_dog_left {ns}.data += #zb_dog_alive {ns}.data

# ammo_done also covers the same-tick case: two hounds dying together both see the pack empty.
execute if score #zb_dog_left {ns}.data matches ..0 if score #zb_dog_ammo_done {ns}.data matches 0 run function {ns}:v{version}/zombies/dog_max_ammo_at_self
""")

	## Primary path: @s is the last hound, still standing where it died.
	## Bypasses the shuffle bag and drop roll — it's a fixed reward, so it names the type itself.
	write_versioned_function("zombies/dog_max_ammo_at_self", f"""
scoreboard players set #zb_dog_ammo_done {ns}.data 1
scoreboard players add #pu_uid {ns}.data 1
data modify storage {ns}:temp _pu_spawn set value {{x:0,y:0,z:0,uid:0,type:"max_ammo"}}
data modify storage {ns}:temp _pu_spawn.x set from entity @s Pos[0]
data modify storage {ns}:temp _pu_spawn.y set from entity @s Pos[1]
data modify storage {ns}:temp _pu_spawn.z set from entity @s Pos[2]
execute store result storage {ns}:temp _pu_spawn.uid int 1 run scoreboard players get #pu_uid {ns}.data
function {ns}:v{version}/zombies/powerups/spawn_display with storage {ns}:temp _pu_spawn
""")

	# Grenade Replenishment (appended to start_round).

	write_versioned_function("zombies/start_round", f"""
# Replenish grenades for all alive players (+2, cap at 4)
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:v{version}/zombies/inventory/replenish_grenades
""")

	# Stuck Zombie Glow.

	## Apply glowing to zombies far from all players (stuck/unreachable).
	## Called every 5s (100 ticks) once 60s have passed since the last zombie spawned.
	## Applies glowing for 6s (120 ticks) and clears it on zombies that moved near a player.
	write_versioned_function("zombies/glow_stuck_zombies", f"""
# Tag zombies currently within 32 blocks of any alive player
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run tag @e[tag={ns}.zombie_round,distance=..32] add {ns}.zb_near_player

# Apply glowing for 6 seconds to zombies far from all players
effect give @e[tag={ns}.zombie_round,tag=!{ns}.zb_near_player] glowing 6 0 true

# Cleanup temp tag
tag @e[tag={ns}.zb_near_player] remove {ns}.zb_near_player
""")

