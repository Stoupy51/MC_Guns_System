
# ruff: noqa: E501
# Player/team management menus (shared across multiplayer, zombies, and missions)
#
# Admins open a "Manage Players" dialog from each mode's setup menu. It renders one row per online
# player: their name (tinted by status, click to refresh) followed by that mode's assignment buttons
# — Red/Blue/Remove for multiplayer, Join/Remove for zombies & missions. Assigning is one click.
#
# Players are independent of a game until assigned here (or via the self-service "+ Join" button):
# assignment sets the mode's *.in_game flag (the opt-in link) plus the vanilla team, and — if a game
# is already live — runs that mode's late-join flow so the player is fully set up (loadout, spawn).
#
# A specific player is targeted from a dialog button via their Bookshelf SUID (`bs.id`, assigned per
# player in player_config): a run_command button runs as the clicker, so it wraps the real action in
# `execute as @a[scores={bs.id=<N>}] run ...` to redirect it onto the chosen player.
#
# SNBT here is brace-dense, so bodies use `%NS%`/`%VER%` sentinels (replaced below) instead of
# f-string `{{ }}` escaping, keeping the dialog JSON readable.
from stewbeet import LootTable, Mem, set_json_encoder, write_versioned_function


def write_player_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	def wf(path: str, body: str) -> None:
		write_versioned_function(path, body.replace("%NS%", ns).replace("%VER%", version))

	# Loot table that yields a player head filled with the loot-context player's profile ("this").
	# Dialog labels don't resolve @-selector text components, so we can't show a player by selector;
	# instead we fill a head from each player, read the username out of its profile component, and
	# bake that literal string into the dialog (see players/append_self).
	Mem.ctx.data[ns].loot_tables["players/name_head"] = set_json_encoder(LootTable({
		"pools": [{
			"rolls": 1,
			"entries": [{
				"type": "minecraft:item",
				"name": "minecraft:player_head",
				"functions": [{"function": "minecraft:fill_player_head", "entity": "this"}],
			}],
		}],
	}))

	## ---- Player list builder (recursive over online players) ----

	# append_self (run as each @a): append this player's bs.id, real name, and a status color.
	# Color reflects the player's current link to the active mode (requires _plr_mode set beforehand):
	# red/blue for their multiplayer team, green when in the zombies/mission game, gray when independent.
	# The name is read from a player head filled with @s's profile (dialog labels can't render selectors).
	wf("players/append_self", """
data modify storage %NS%:temp _plr_entry set value {color:"gray",name:"???"}
execute store result storage %NS%:temp _plr_entry.id int 1 run scoreboard players get @s bs.id
execute if data storage %NS%:temp {_plr_mode:"multiplayer"} if score @s %NS%.mp.team matches 1 run data modify storage %NS%:temp _plr_entry.color set value "red"
execute if data storage %NS%:temp {_plr_mode:"multiplayer"} if score @s %NS%.mp.team matches 2 run data modify storage %NS%:temp _plr_entry.color set value "blue"
execute if data storage %NS%:temp {_plr_mode:"zombies"} if score @s %NS%.zb.in_game matches 1 run data modify storage %NS%:temp _plr_entry.color set value "green"
execute if data storage %NS%:temp {_plr_mode:"missions"} if score @s %NS%.mi.in_game matches 1 run data modify storage %NS%:temp _plr_entry.color set value "green"

# Resolve the real username: fill an invisible probe's head with @s's profile ("this" in the loot
# table), then read the name out of its profile component (dual path covers both equipment NBT formats).
execute at @s run summon armor_stand ~ ~ ~ {Tags:["%NS%_name_probe"],Invisible:1b,NoGravity:1b}
loot replace entity @e[type=armor_stand,tag=%NS%_name_probe,limit=1] armor.head loot %NS%:players/name_head
data modify storage %NS%:temp _plr_entry.name set from entity @e[type=armor_stand,tag=%NS%_name_probe,limit=1] ArmorItems[3].components."minecraft:profile".name
data modify storage %NS%:temp _plr_entry.name set from entity @e[type=armor_stand,tag=%NS%_name_probe,limit=1] equipment.head.components."minecraft:profile".name
kill @e[type=armor_stand,tag=%NS%_name_probe]

data modify storage %NS%:temp _plr_iter append from storage %NS%:temp _plr_entry
""")

	# list_iter: pop one player entry, inject the mode, append its button, recurse (mirrors shared/maps/select_iter).
	wf("players/list_iter", """
execute unless data storage %NS%:temp _plr_iter[0] run return fail

# Inject the mode into the first entry for the macro
data modify storage %NS%:temp _plr_entry set from storage %NS%:temp _plr_iter[0]
data modify storage %NS%:temp _plr_entry.mode set from storage %NS%:temp _plr_mode

# Append one button for this player
function %NS%:v%VER%/players/list_entry with storage %NS%:temp _plr_entry

# Advance
data remove storage %NS%:temp _plr_iter[0]
execute if data storage %NS%:temp _plr_iter[0] run function %NS%:v%VER%/players/list_iter
""")

	# list_entry (macro {id, name, color, mode}): dispatch to that mode's row builder.
	wf("players/list_entry", """
$function %NS%:v%VER%/players/row_$(mode) {id:$(id),name:"$(name)",color:"$(color)"}
""")

	# Row builders (macro {id, name, color}): append one button per grid cell, left to right, so each
	# player occupies one full row — their name followed by their assignment buttons. Assigning a team
	# is therefore a single click from the list, instead of list → per-player menu → button.
	# The leading name button just re-opens the list: the dialog stays open after a click
	# (after_action:"none"), so the status colors need a manual refresh to catch up.
	# The number of buttons per row MUST equal the dialog's `columns` in list_body below.
	name_btn: str = '{label:{text:"$(name)",color:"$(color)"},tooltip:{text:"Refresh the list"},action:{type:"run_command",command:"/function %NS%:v%VER%/players/list_%MODE%"}}'

	def action_btn(label: str, color: str, tooltip: str, fn: str) -> str:
		""" A row button that redirects onto the target player via their SUID (it runs as the clicker). """
		return (
			f'{{label:{{text:"{label}",color:"{color}"}},tooltip:{{text:"{tooltip}"}},action:{{type:"run_command",'
			f'command:"/execute as @a[scores={{bs.id=$(id)}}] run function %NS%:v%VER%/players/{fn}"}}}}'
		)

	rows: dict[str, list[str]] = {
		"multiplayer": [
			action_btn("Red", "red", "Move to Red team", "mp_to_red"),
			action_btn("Blue", "blue", "Move to Blue team", "mp_to_blue"),
			action_btn("Remove", "gray", "Remove from the game (spectator)", "mp_remove"),
		],
		"zombies": [
			action_btn("Join", "green", "Add to the zombies game", "zb_join"),
			action_btn("Remove", "gray", "Remove from the game (spectator)", "zb_remove"),
		],
		"missions": [
			action_btn("Join", "green", "Add to the mission", "mi_join"),
			action_btn("Remove", "gray", "Remove from the game (spectator)", "mi_remove"),
		],
	}
	for mode, buttons in rows.items():
		wf(f"players/row_{mode}", "\n".join(
			f"$data modify storage %NS%:temp dialog.actions append value {b}"
			for b in [name_btn.replace("%MODE%", mode), *buttons]
		))

	# Per-mode list wrappers: materialize online players, build the base dialog, iterate, then show it.
	# Only the mode string, title color, and Back target differ between the three.
	list_body: str = """
# Materialize the online players into a fresh list (mode is set first so append_self can color by status)
data modify storage %NS%:temp _plr_mode set value "%MODE%"
data modify storage %NS%:temp _plr_iter set value []
execute as @a run function %NS%:v%VER%/players/append_self

# Base dialog (one row per player, stays open after a pick, Back returns to setup)
data modify storage %NS%:temp dialog set value {type:"minecraft:multi_action",title:["","👥 ",{text:"Manage Players",color:"%COLOR%",bold:true}],body:[{type:"minecraft:plain_message",contents:{text:"One row per player — click a name to refresh",color:"gray"}}],actions:[],columns:%COLUMNS%,pause:false,after_action:"none",exit_action:{label:{text:"◀ Back",color:"gray"},tooltip:{text:"Return to setup"},action:{type:"run_command",command:"/function %NS%:v%VER%/%BACK%"}}}

# Append one button per player
execute if data storage %NS%:temp _plr_iter[0] run function %NS%:v%VER%/players/list_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage %NS%:temp dialog.actions[0] run data modify storage %NS%:temp dialog.actions append value {label:{text:"No players online",color:"red"},tooltip:{text:"Nobody to manage"},action:{type:"run_command",command:"/function %NS%:v%VER%/%BACK%"}}

# Show the completed dialog
function %NS%:v%VER%/multiplayer/show_dialog with storage %NS%:temp
"""
	# columns == buttons per row in that mode's row builder above (name + assignment buttons).
	for mode, color, back, columns in [
		("multiplayer", "gold", "multiplayer/setup", 4),
		("zombies", "dark_green", "zombies/setup", 3),
		("missions", "aqua", "missions/setup", 3),
	]:
		wf(f"players/list_{mode}", list_body
			.replace("%MODE%", mode).replace("%COLOR%", color)
			.replace("%BACK%", back).replace("%COLUMNS%", str(columns)))

	## ---- Assignment actions (run AS the target @s) ----
	# If a game is live and the player isn't in it yet, run that mode's late-join flow (full setup),
	# then force the chosen team (overriding late-join's auto-assign for multiplayer). Pre-game, only
	# the *.in_game opt-in and team score are set; the start function establishes the vanilla team.

	wf("players/mp_to_red", """
execute if score @s %NS%.mp.in_game matches 0 if data storage %NS%:multiplayer game{state:"active"} run function %NS%:v%VER%/multiplayer/join_game
execute if score @s %NS%.mp.in_game matches 0 if data storage %NS%:multiplayer game{state:"preparing"} run function %NS%:v%VER%/multiplayer/join_game
scoreboard players set @s %NS%.mp.in_game 1
scoreboard players set @s %NS%.mp.team 1
execute if data storage %NS%:multiplayer game{state:"active"} run team join %NS%.red @s
execute if data storage %NS%:multiplayer game{state:"preparing"} run team join %NS%.red @s
tellraw @s ["",{"text":"Assigned to ","color":"white"},{"text":"Red Team","color":"red","bold":true}]
""")

	wf("players/mp_to_blue", """
execute if score @s %NS%.mp.in_game matches 0 if data storage %NS%:multiplayer game{state:"active"} run function %NS%:v%VER%/multiplayer/join_game
execute if score @s %NS%.mp.in_game matches 0 if data storage %NS%:multiplayer game{state:"preparing"} run function %NS%:v%VER%/multiplayer/join_game
scoreboard players set @s %NS%.mp.in_game 1
scoreboard players set @s %NS%.mp.team 2
execute if data storage %NS%:multiplayer game{state:"active"} run team join %NS%.blue @s
execute if data storage %NS%:multiplayer game{state:"preparing"} run team join %NS%.blue @s
tellraw @s ["",{"text":"Assigned to ","color":"white"},{"text":"Blue Team","color":"blue","bold":true}]
""")

	wf("players/mp_remove", """
scoreboard players set @s %NS%.mp.team 0
scoreboard players set @s %NS%.mp.in_game 0
team leave @s
execute if data storage %NS%:multiplayer game{state:"active"} run gamemode spectator @s
tellraw @s [{"text":"Removed from the game","color":"gray"}]
""")

	wf("players/zb_join", """
execute if score @s %NS%.zb.in_game matches 0 if data storage %NS%:zombies game{state:"active"} run function %NS%:v%VER%/zombies/join_game
execute if score @s %NS%.zb.in_game matches 0 if data storage %NS%:zombies game{state:"preparing"} run function %NS%:v%VER%/zombies/join_game
scoreboard players set @s %NS%.zb.in_game 1
execute if data storage %NS%:zombies game{state:"active"} run team join %NS%.zombies @s
execute if data storage %NS%:zombies game{state:"preparing"} run team join %NS%.zombies @s
tellraw @s ["",{"text":"Joined the ","color":"white"},{"text":"Zombies game","color":"dark_green","bold":true}]
""")

	wf("players/zb_remove", """
scoreboard players set @s %NS%.zb.in_game 0
team leave @s
execute if data storage %NS%:zombies game{state:"active"} run gamemode spectator @s
tellraw @s [{"text":"Removed from the zombies game","color":"gray"}]
""")

	wf("players/mi_join", """
execute if score @s %NS%.mi.in_game matches 0 if data storage %NS%:missions game{state:"active"} run function %NS%:v%VER%/missions/join_game
execute if score @s %NS%.mi.in_game matches 0 if data storage %NS%:missions game{state:"preparing"} run function %NS%:v%VER%/missions/join_game
scoreboard players set @s %NS%.mi.in_game 1
scoreboard players set @s %NS%.mp.team 1
execute if data storage %NS%:missions game{state:"active"} run team join %NS%.blue @s
execute if data storage %NS%:missions game{state:"preparing"} run team join %NS%.blue @s
tellraw @s ["",{"text":"Joined the ","color":"white"},{"text":"Mission","color":"aqua","bold":true}]
""")

	wf("players/mi_remove", """
scoreboard players set @s %NS%.mi.in_game 0
scoreboard players set @s %NS%.mp.team 0
team leave @s
execute if data storage %NS%:missions game{state:"active"} run gamemode spectator @s
tellraw @s [{"text":"Removed from the mission","color":"gray"}]
""")
