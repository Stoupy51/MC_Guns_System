""" Player death, spectating and respawning. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers.titles import TitleTimes


# Functions
def write_missions_death() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Run as the victim when a bullet or explosion would be lethal (utils/signal_and_damage); `{ns}:input with` may hold amount and attacker.
	# The player is healed instead of dying, so vanilla never moves them to the world spawn and the respawn teleport below has a valid position.
	write_versioned_function("missions/simulate_death", f"""
# A second bullet in the same tick, or an OOB kill on top of one.
execute if score @s {ns}.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Healed so the player never really dies.
effect give @s instant_health 1 100 true
scoreboard players add @s {ns}.mi.deaths 1

# Hit effects, hitmarker and DPS, for hits.
execute if data storage {ns}:input with.amount run function #{ns}:signals/damage with storage {ns}:input with

# No vanilla death: the body is still where it fell, so the camera stays there instead of snapping to a teammate.
scoreboard players set @s {ns}.mi.died_here 1

function {ns}:v{version}/missions/enter_death_spectate
""")

	## Vanilla-death fallback (fall, lava, drowning, the OOB kill) for what the simulated path cannot intercept.
	## Vanilla already moved the player, so they respawn at a mission spawn.
	write_versioned_function("missions/on_respawn", f"""
scoreboard players set @s {ns}.mp.death_count 0

# Already handled as a simulated death in the same tick.
execute if score @s {ns}.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

scoreboard players add @s {ns}.mi.deaths 1
scoreboard players set @s {ns}.mi.died_here 0

function {ns}:v{version}/missions/enter_death_spectate
""")

	## Run as the dying player, for both paths above.
	write_versioned_function("missions/enter_death_spectate", f"""
# First, while the gun is still held: it can be picked up for 30 s.
execute at @s run function {ns}:v{version}/multiplayer/drop_held_weapon

# 3 s of spectating before the respawn.
gamemode spectator @s
scoreboard players set @s {ns}.mp.spectate_timer 60

# A simulated death keeps the camera at the death point; a vanilla death already moved the player, so they spectate a teammate.
execute unless score @s {ns}.mi.died_here matches 1 run function {ns}:v{version}/missions/spectate_random_player

{TitleTimes.RESPAWN.cmd()}
title @s title ["☠"]
title @s subtitle [{{"text":"Respawning in 3 seconds...","color":"gray"}}]
execute at @s run playsound minecraft:entity.player.hurt ambient @s
""")

	write_versioned_function("missions/spectate_random_player", f"""
execute as @r[scores={{{ns}.mi.in_game=1}},gamemode=!spectator] run spectate @s @p[scores={{{ns}.mp.spectate_timer=1..}},sort=nearest]
""")

	write_versioned_function("missions/actual_respawn", f"""
spectate @s

gamemode adventure @s

function {ns}:v{version}/missions/respawn_tp
scoreboard players set @s {ns}.mi.died_here 0

# The stamina system owns the hunger bar.
scoreboard players set @s {ns}.stam_seen 0

# Lost on death.
execute unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

item replace entity @s hotbar.3 with compass[custom_data={{{ns}:{{compass:true}}}}]

execute if data storage {ns}:missions game.map.respawn_commands[0] at @s run function {ns}:v{version}/shared/run_respawn_commands {{mode:"missions"}}

# Run as the respawning player.
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"respawn"}}
""")

