""" Player death, spectating and respawning. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_missions_death() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Death handling.
	# Simulated death (@s = victim, `{ns}:input with` may hold amount/attacker).
	# Called from utils/signal_and_damage when a bullet/explosion would be lethal, exactly like multiplayer: the player is healed instead of dying, so vanilla never respawns them at the world spawn and their position stays valid for the respawn teleport below.
	write_versioned_function("missions/simulate_death", f"""
# Ignore duplicate deaths (a second bullet landing in the same tick, or an OOB kill on top of one)
execute if score @s {ns}.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Heal to prevent the actual death & Increment mission death stats
effect give @s instant_health 1 100 true
scoreboard players add @s {ns}.mi.deaths 1

# Fire the damage signal (hit effects, hitmarker, DPS) if this came from a hit
execute if data storage {ns}:input with.amount run function #{ns}:signals/damage with storage {ns}:input with

# No vanilla death happened, so the body is still standing where it fell: the spectate flow below
# leaves the camera right there instead of snapping to a teammate
scoreboard players set @s {ns}.mi.died_here 1

function {ns}:v{version}/missions/enter_death_spectate
""")

	## On Respawn: the vanilla-death fallback (fall damage, lava, drowning, the OOB kill) for everything the simulated path can't intercept.
	## Vanilla already respawned the player elsewhere by now, so their position is worthless — these respawn at a mission spawn.
	write_versioned_function("missions/on_respawn", f"""
# Reset death counter
scoreboard players set @s {ns}.mp.death_count 0

# Already in death spectate -> this vanilla death was already processed as a simulated death
execute if score @s {ns}.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Increment mission death stats
scoreboard players add @s {ns}.mi.deaths 1
scoreboard players set @s {ns}.mi.died_here 0

function {ns}:v{version}/missions/enter_death_spectate
""")

	## Shared death-spectate flow (@s = dying player), used by both paths above
	write_versioned_function("missions/enter_death_spectate", f"""
# Drop the held gun on the ground (pickable for 30s) before anything else, while still holding it
execute at @s run function {ns}:v{version}/multiplayer/drop_held_weapon

# Set player to spectator mode for 3 seconds (60 ticks) before actual respawn
gamemode spectator @s
scoreboard players set @s {ns}.mp.spectate_timer 60

# Simulated death: the camera is already at the death point, leave it there. A vanilla death has
# teleported the player to the world spawn by now, so those fall back to spectating a teammate.
execute unless score @s {ns}.mi.died_here matches 1 run function {ns}:v{version}/missions/spectate_random_player

# Announce respawn delay to the dying player
title @s title ["☠"]
title @s subtitle [{{"text":"Respawning in 3 seconds...","color":"gray"}}]
execute at @s run playsound minecraft:entity.player.hurt ambient @s
""")

	## Spectate a random alive in-game player (fallback)
	write_versioned_function("missions/spectate_random_player", f"""
# Pick a random alive in-game player (not self, not spectator)
execute as @r[scores={{{ns}.mi.in_game=1}},gamemode=!spectator] run spectate @s @p[scores={{{ns}.mp.spectate_timer=1..}},sort=nearest]
""")

	## Actual respawn: called when spectate timer reaches 0
	write_versioned_function("missions/actual_respawn", f"""
# Stop spectating
spectate @s

# Switch back to adventure
gamemode adventure @s

# Teleport to random mission spawn point
function {ns}:v{version}/missions/respawn_tp
scoreboard players set @s {ns}.mi.died_here 0

# Reset stamina to full (the stamina system owns the hunger bar)
scoreboard players set @s {ns}.stam_seen 0

# Re-apply class loadout (lost on death)
execute unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# Re-give compass
item replace entity @s hotbar.3 with compass[custom_data={{{ns}:{{compass:true}}}}]

# Run map-defined respawn commands on this player (if any)
execute if data storage {ns}:missions game.map.respawn_commands[0] at @s run function {ns}:v{version}/shared/run_respawn_commands {{mode:"missions"}}

# Call map respawn script (executed as the respawning player)
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"respawn"}}
""")

