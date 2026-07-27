""" Game over, stopping a game and the operator-only fast restart. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.dialogs import Dialogs
from ....helpers.lifecycle import GameLifecycle
from ....helpers.ranked import RankedStats


# Functions
def write_zombies_over() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Game Over.

	zb_stat_line: str = (
		'tellraw @a ["","  ","🎖 ",{"selector":"@s"}," — Kills: ",'
		f'{{"score":{{"name":"@s","objective":"{ns}.zb.kills"}},"color":"green"}}," | Downs: ",'
		f'{{"score":{{"name":"@s","objective":"{ns}.zb.downs"}},"color":"red"}}," | Points: ",'
		f'{{"score":{{"name":"@s","objective":"{ns}.zb.points"}},"color":"gold"}}]'
	)
	zb_ranked_stats: str = RankedStats.write_ranked_stats_functions(
		ns, version, "zombies/announce_stats", "zb.in_game", "zb.kills", zb_stat_line
	)

	write_versioned_function("zombies/game_over", f"""
# Set state to ended
data modify storage {ns}:zombies game.state set value "ended"

# Snapshot the roster so a fast restart still works after the scheduled auto-stop clears
# {ns}.zb.in_game 5 seconds from now (see zombies/restart).
tag @a remove {ns}.zb_last_roster
tag @a[scores={{{ns}.zb.in_game=1}}] add {ns}.zb_last_roster

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 80 20
title @a[scores={{{ns}.zb.in_game=1}}] title {{"text":"GAME OVER","color":"dark_red","bold":true}}

# Calculate final round
execute store result score #final_round {ns}.data run data get storage {ns}:zombies game.round

# Performance summary
tellraw @a ["","\\n",{{"text":"═══════ GAME OVER ═══════","color":"dark_red","bold":true}}]
tellraw @a ["","  ","🧟 ",{{"text":"Final Round: ","color":"gray"}},{{"score":{{"name":"#final_round","objective":"{ns}.data"}},"color":"red","bold":true}}]

# Per-player stats, best first. The bare selector component renders the player's team colour.
{zb_ranked_stats}

tellraw @a ["",{{"text":"═════════════════════════","color":"dark_red","bold":true}},"\\n"]

# Signal game end
function #{ns}:zombies/on_game_end

# Stop all sounds and play gameover sound
stopsound @a
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/game_over ambient @s ~ ~ ~ 0.25 1.0

# Offer a one-click fast restart. suggest_command only runs at permission level 2, so it is a
# no-op for non-operators — exactly the operator-gated restart the design calls for.
tellraw @a ["",{MGS_TAG}," ",{Dialogs.btn("⟲ Fast Restart", f"/function {ns}:v{version}/zombies/restart", "green", "Restart with the same map, variant and players (operators only)")}]

# End game after 5 seconds
schedule function {ns}:v{version}/zombies/stop 100t
""")

	# Game Stop.
	write_versioned_function("zombies/stop", f"""
# Various cleanup to set to lobby state
data modify storage {ns}:zombies game.state set value "lobby"
schedule clear {ns}:v{version}/zombies/end_prep
schedule clear {ns}:v{version}/zombies/start_round

# Drop any admin freeze (the attribute/NoAI restore below is part of the normal cleanup)
scoreboard players set #zb_freeze {ns}.data 0
tag @e[tag={ns}.zb_frozen_ai] remove {ns}.zb_frozen_ai
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:max_health base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:entity_interaction_range base reset
effect clear @a[scores={{{ns}.zb.in_game=1}}]
gamemode adventure @a[scores={{{ns}.zb.in_game=1}},gamemode=spectator]
kill @e[tag={ns}.zombie_round]
kill @e[tag={ns}.gm_entity]

# Remove forceload (only if bounds were set)
execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/shared/remove_forceload

scoreboard objectives setdisplay sidebar
scoreboard objectives remove {ns}.zb_sidebar
gamerule advance_time true

{GameLifecycle.regen_disable_lines(ns)}

# Announce
tellraw @a [{MGS_TAG},{{"text":"Zombies game ended.","color":"red"}}]
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/shared/maps/call_script_at_base {{script:"leave"}}

# Reset in-game state
scoreboard players set @a {ns}.zb.in_game 0
scoreboard players set @a {ns}.zb.points 0
scoreboard players set @a {ns}.zb.kills 0
scoreboard players set @a {ns}.zb.downs 0
scoreboard players set @a {ns}.zb.passive 0
scoreboard players set @a {ns}.zb.ability 0
scoreboard players set @a {ns}.zb.ability_cd 0
scoreboard players set @a {ns}.zb.prev_kills 0
scoreboard players set @a {ns}.mp.spectate_timer 0
tag @a[tag={ns}.give_class_menu] remove {ns}.give_class_menu
""")

	# Fast restart: stop the current game and immediately start a new one with the same map, variant and roster.
	## Reachable only through /function (permission level 2), so it stays operator-only.
	write_versioned_function("zombies/restart", f"""
# Roster = players still in the game; if the auto-stop already cleared in_game, fall back to the
# snapshot game_over took. Tag them so the roster survives the stop cleanup below.
execute if entity @a[scores={{{ns}.zb.in_game=1}}] run tag @a[scores={{{ns}.zb.in_game=1}}] add {ns}.zb_restart
execute unless entity @a[scores={{{ns}.zb.in_game=1}}] run tag @a[tag={ns}.zb_last_roster] add {ns}.zb_restart
execute unless entity @a[tag={ns}.zb_restart] run return run tellraw @s [{MGS_TAG},{{"text":"Nothing to restart — no players from the last game.","color":"red"}}]

# Bail before tearing anything down if no map is selected (start would reject it anyway).
execute if data storage {ns}:zombies game{{map_id:""}} run return run function {ns}:v{version}/zombies/restart_no_map

# Cancel the pending auto-stop from game_over, then run the normal teardown.
schedule clear {ns}:v{version}/zombies/stop
function {ns}:v{version}/zombies/stop

# Re-opt the roster back in (stop set in_game 0) and start fresh — stop kept game.map_id / variant.
scoreboard players set @a[tag={ns}.zb_restart] {ns}.zb.in_game 1
tag @a[tag={ns}.zb_restart] remove {ns}.zb_restart
tellraw @a [{MGS_TAG},{{"text":"An operator restarted the game.","color":"yellow"}}]
function {ns}:v{version}/zombies/start
""")

	## Error path kept out of restart so the map-missing guard can both warn and drop the roster tag.
	write_versioned_function("zombies/restart_no_map", f"""
tag @a[tag={ns}.zb_restart] remove {ns}.zb_restart
tellraw @s [{MGS_TAG},{{"text":"No map selected — open the setup menu first.","color":"red"}}]
""")

