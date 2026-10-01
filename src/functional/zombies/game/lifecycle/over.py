""" Game over, stopping a game and the operator-only fast restart. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.dialogs import Dialogs
from ....helpers.lifecycle import GameLifecycle
from ....helpers.ranked import RankedStats
from ....helpers.text import Text
from ....helpers.titles import TitleTimes
from ....progression import Xp


# Functions
def write_zombies_over() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	zb_stat_line: str = (
		f'tellraw @a ["","  ","🎖 ",{Text.player(ns, "@s", side="zb")}," | Kills: ",'
		f'{{"score":{{"name":"@s","objective":"{ns}.zb.kills"}},"color":"green"}}," | Downs: ",'
		f'{{"score":{{"name":"@s","objective":"{ns}.zb.downs"}},"color":"red"}}," | Points: ",'
		f'{{"score":{{"name":"@s","objective":"{ns}.zb.points"}},"color":"gold"}}]'
	)
	zb_ranked_stats: str = RankedStats.write_ranked_stats_functions(
		ns, version, "zombies/announce_stats", "zb.in_game", "zb.kills", zb_stat_line
	)

	write_versioned_function("zombies/game_over", f"""
data modify storage {ns}:zombies game.state set value "ended"

# The roster snapshot lets a fast restart work after the auto-stop clears in_game 5 s later (see zombies/restart).
tag @a remove {ns}.zb_last_roster
tag @a[scores={{{ns}.zb.in_game=1}}] add {ns}.zb_last_roster

{TitleTimes.BANNER.cmd(f'@a[scores={{{ns}.zb.in_game=1}}]')}
title @a[scores={{{ns}.zb.in_game=1}}] title {{"text":"GAME OVER","color":"dark_red","bold":true}}

execute store result score #final_round {ns}.data run data get storage {ns}:zombies game.round

# Paid here so the Final Round line can show the amount.
function {ns}:v{version}/zombies/xp/on_game_over

# The Final Round line is split because only the roster earned the bonus.
tellraw @a ["","\\n",{{"text":"GAME OVER","color":"dark_red","bold":true}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] ["","  ","🧟 ",{{"text":"Final Round: ","color":"gray"}},{{"score":{{"name":"#final_round","objective":"{ns}.data"}},"color":"red","bold":true}},{Xp.suffix("zb", "game_over")}]
tellraw @a[scores={{{ns}.zb.in_game=0}}] ["","  ","🧟 ",{{"text":"Final Round: ","color":"gray"}},{{"score":{{"name":"#final_round","objective":"{ns}.data"}},"color":"red","bold":true}}]

# Best first; the bare selector component renders the team colour.
{zb_ranked_stats}

tellraw @a ""

function #{ns}:zombies/on_game_end

stopsound @a
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/game_over ambient @s ~ ~ ~ 0.3 1.0

# suggest_command only runs at permission level 2, so the restart is operator-only.
tellraw @a ["",{MGS_TAG}," ",{Dialogs.btn("⟲ Fast Restart", f"/function {ns}:v{version}/zombies/restart", "green", "Restart with the same map, variant and players (operators only)")}]

schedule function {ns}:v{version}/zombies/stop 100t
""")

	write_versioned_function("zombies/stop", f"""
data modify storage {ns}:zombies game.state set value "lobby"
schedule clear {ns}:v{version}/zombies/end_prep
schedule clear {ns}:v{version}/zombies/start_round

# The attribute and NoAI restore below is part of the normal cleanup.
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

execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/shared/remove_forceload

scoreboard objectives setdisplay sidebar
scoreboard objectives remove {ns}.zb_sidebar
gamerule advance_time true

{GameLifecycle.regen_disable_lines(ns)}

tellraw @a [{MGS_TAG},{{"text":"Zombies game ended.","color":"red"}}]
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/shared/maps/call_script_at_base {{script:"leave"}}

scoreboard players set @a {ns}.zb.in_game 0
# The XP spend tracker is reset too, or the reset reads as points spent (see xp).
scoreboard players set @a {ns}.zb.points 0
scoreboard players set @a {ns}.zb.xp_pts_prev 0
scoreboard players set @a {ns}.zb.xp_spent_acc 0
scoreboard players set @a {ns}.zb.kills 0
scoreboard players set @a {ns}.zb.downs 0
scoreboard players set @a {ns}.zb.passive 0
scoreboard players set @a {ns}.zb.ability 0
scoreboard players set @a {ns}.zb.ability_cd 0
scoreboard players set @a {ns}.zb.prev_kills 0
scoreboard players set @a {ns}.mp.spectate_timer 0
tag @a[tag={ns}.give_class_menu] remove {ns}.give_class_menu
""")

	# Fast restart with the same map, variant and roster. Only reachable through /function, so operator-only.
	write_versioned_function("zombies/restart", f"""
# Roster: players still in game, else the snapshot game_over took. Tagged so it survives the stop below.
execute if entity @a[scores={{{ns}.zb.in_game=1}}] run tag @a[scores={{{ns}.zb.in_game=1}}] add {ns}.zb_restart
execute unless entity @a[scores={{{ns}.zb.in_game=1}}] run tag @a[tag={ns}.zb_last_roster] add {ns}.zb_restart
execute unless entity @a[tag={ns}.zb_restart] run return run tellraw @s [{MGS_TAG},{{"text":"Nothing to restart: no players from the last game.","color":"red"}}]

# Before tearing anything down.
execute if data storage {ns}:zombies game{{map_id:""}} run return run function {ns}:v{version}/zombies/restart_no_map

# Cancels the auto-stop scheduled by game_over.
schedule clear {ns}:v{version}/zombies/stop
function {ns}:v{version}/zombies/stop

# stop kept game.map_id and the variant.
scoreboard players set @a[tag={ns}.zb_restart] {ns}.zb.in_game 1
tag @a[tag={ns}.zb_restart] remove {ns}.zb_restart
tellraw @a [{MGS_TAG},{{"text":"An operator restarted the game.","color":"yellow"}}]
function {ns}:v{version}/zombies/start
""")

	## Warns and drops the roster tag.
	write_versioned_function("zombies/restart_no_map", f"""
tag @a[tag={ns}.zb_restart] remove {ns}.zb_restart
tellraw @s [{MGS_TAG},{{"text":"No map selected. Open the setup menu first.","color":"red"}}]
""")

