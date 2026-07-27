""" Player/team management menus, shared across multiplayer, zombies and missions.

Admins open a "Manage Players" dialog from each mode's setup menu; it renders one row per online
player, with that mode's assignment buttons. Players are independent of a game until assigned here
(or via self-service "+ Join"): assignment sets the mode's *.in_game flag plus the vanilla team,
and runs the late-join flow if a game is already live.

A player is targeted from a dialog button via their Bookshelf SUID (`bs.id`): a run_command button
runs as the clicker, so it wraps the action in `execute as @a[scores={bs.id=<N>}] run ...`.

"""
# ruff: noqa: E501
from stewbeet import LootTable, Mem, set_json_encoder, write_versioned_function


def write_player_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Dialog labels don't resolve @-selector text components, so a player's name is baked in as a literal.
	# Fill a head from their profile ("this"), then read the username back out.
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

	# Append @s's bs.id, real name and status colour; needs _plr_mode set beforehand
	write_versioned_function("players/append_self", f"""
data modify storage {ns}:temp _plr_entry set value {{color:"gray",name:"???"}}
execute store result storage {ns}:temp _plr_entry.id int 1 run scoreboard players get @s bs.id
execute if data storage {ns}:temp {{_plr_mode:"multiplayer"}} if score @s {ns}.mp.team matches 1 run data modify storage {ns}:temp _plr_entry.color set value "red"
execute if data storage {ns}:temp {{_plr_mode:"multiplayer"}} if score @s {ns}.mp.team matches 2 run data modify storage {ns}:temp _plr_entry.color set value "blue"
execute if data storage {ns}:temp {{_plr_mode:"zombies"}} if score @s {ns}.zb.in_game matches 1 run data modify storage {ns}:temp _plr_entry.color set value "green"
execute if data storage {ns}:temp {{_plr_mode:"missions"}} if score @s {ns}.mi.in_game matches 1 run data modify storage {ns}:temp _plr_entry.color set value "green"

# Resolve the real username: fill an invisible probe's head with @s's profile ("this" in the loot
# table), then read the name out of its profile component (dual path covers both equipment NBT formats).
execute at @s run summon armor_stand ~ ~ ~ {{Tags:["{ns}_name_probe"],Invisible:1b,NoGravity:1b}}
loot replace entity @e[type=armor_stand,tag={ns}_name_probe,limit=1] armor.head loot {ns}:players/name_head
data modify storage {ns}:temp _plr_entry.name set from entity @e[type=armor_stand,tag={ns}_name_probe,limit=1] ArmorItems[3].components."minecraft:profile".name
data modify storage {ns}:temp _plr_entry.name set from entity @e[type=armor_stand,tag={ns}_name_probe,limit=1] equipment.head.components."minecraft:profile".name
kill @e[type=armor_stand,tag={ns}_name_probe]

data modify storage {ns}:temp _plr_iter append from storage {ns}:temp _plr_entry
""")

	# Pop one entry, inject the mode, append its button, recurse (mirrors shared/maps/select_iter)
	write_versioned_function("players/list_iter", f"""
execute unless data storage {ns}:temp _plr_iter[0] run return fail

# Inject the mode into the first entry for the macro
data modify storage {ns}:temp _plr_entry set from storage {ns}:temp _plr_iter[0]
data modify storage {ns}:temp _plr_entry.mode set from storage {ns}:temp _plr_mode

# Append one button for this player
function {ns}:v{version}/players/list_entry with storage {ns}:temp _plr_entry

# Advance
data remove storage {ns}:temp _plr_iter[0]
execute if data storage {ns}:temp _plr_iter[0] run function {ns}:v{version}/players/list_iter
""")

	# Macro {id, name, color, mode}: dispatch to that mode's row builder
	write_versioned_function("players/list_entry", f"""
$function {ns}:v{version}/players/row_$(mode) {{id:$(id),name:"$(name)",color:"$(color)"}}
""")

	# Row builders (macro {id, name, color}): one button per grid cell, so assigning is a single click.
	# The name button re-opens the list, since the dialog stays open and the colours need a refresh.
	# Buttons per row MUST equal the dialog's `columns` in list_body below.
	name_btn: str = f'{{label:{{text:"$(name)",color:"$(color)"}},tooltip:{{text:"Refresh the list"}},action:{{type:"run_command",command:"/function {ns}:v{version}/players/list_%MODE%"}}}}'

	def action_btn(label: str, color: str, tooltip: str, fn: str) -> str:
		""" A row button that redirects onto the target player via their SUID (it runs as the clicker). """
		return (
			f'{{label:{{text:"{label}",color:"{color}"}},tooltip:{{text:"{tooltip}"}},action:{{type:"run_command",'
			f'command:"/execute as @a[scores={{bs.id=$(id)}}] run function {ns}:v{version}/players/{fn}"}}}}'
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
		write_versioned_function(f"players/row_{mode}", "\n".join(
			f"$data modify storage {ns}:temp dialog.actions append value {b}"
			for b in [name_btn.replace("%MODE%", mode), *buttons]
		))

	# Per-mode wrappers; only the mode string, title colour and Back target differ
	list_body: str = f"""
# Materialize the online players into a fresh list (mode is set first so append_self can color by status)
data modify storage {ns}:temp _plr_mode set value "%MODE%"
data modify storage {ns}:temp _plr_iter set value []
execute as @a run function {ns}:v{version}/players/append_self

# Base dialog (one row per player, stays open after a pick, Back returns to setup)
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","👥 ",{{text:"Manage Players",color:"%COLOR%",bold:true}}],body:[{{type:"minecraft:plain_message",contents:{{text:"One row per player — click a name to refresh",color:"gray"}}}}],actions:[],columns:%COLUMNS%,pause:false,after_action:"none",exit_action:{{label:["","◀ ",{{text:"Back",color:"gray"}}],tooltip:{{text:"Return to setup"}},action:{{type:"run_command",command:"/function {ns}:v{version}/%BACK%"}}}}}}

# Append one button per player
execute if data storage {ns}:temp _plr_iter[0] run function {ns}:v{version}/players/list_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage {ns}:temp dialog.actions[0] run data modify storage {ns}:temp dialog.actions append value {{label:{{text:"No players online",color:"red"}},tooltip:{{text:"Nobody to manage"}},action:{{type:"run_command",command:"/function {ns}:v{version}/%BACK%"}}}}

# Show the completed dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
"""
	# columns == buttons per row in that mode's row builder above
	for mode, color, back, columns in [
		("multiplayer", "gold", "multiplayer/setup", 4),
		("zombies", "dark_green", "zombies/setup", 3),
		("missions", "aqua", "missions/setup", 3),
	]:
		write_versioned_function(f"players/list_{mode}", list_body
			.replace("%MODE%", mode).replace("%COLOR%", color)
			.replace("%BACK%", back).replace("%COLUMNS%", str(columns)))

	# Assignment actions, run AS the target @s.
	# A live game runs the late-join flow first, then the chosen team overrides its auto-assign.
	write_versioned_function("players/mp_to_red", f"""
execute if score @s {ns}.mp.in_game matches 0 if data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/join_game
execute if score @s {ns}.mp.in_game matches 0 if data storage {ns}:multiplayer game{{state:"preparing"}} run function {ns}:v{version}/multiplayer/join_game
scoreboard players set @s {ns}.mp.in_game 1
scoreboard players set @s {ns}.mp.team 1
execute if data storage {ns}:multiplayer game{{state:"active"}} run team join {ns}.red @s
execute if data storage {ns}:multiplayer game{{state:"preparing"}} run team join {ns}.red @s
tellraw @s ["",{{"text":"Assigned to ","color":"white"}},{{"text":"Red Team","color":"red","bold":true}}]
""")

	write_versioned_function("players/mp_to_blue", f"""
execute if score @s {ns}.mp.in_game matches 0 if data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/join_game
execute if score @s {ns}.mp.in_game matches 0 if data storage {ns}:multiplayer game{{state:"preparing"}} run function {ns}:v{version}/multiplayer/join_game
scoreboard players set @s {ns}.mp.in_game 1
scoreboard players set @s {ns}.mp.team 2
execute if data storage {ns}:multiplayer game{{state:"active"}} run team join {ns}.blue @s
execute if data storage {ns}:multiplayer game{{state:"preparing"}} run team join {ns}.blue @s
tellraw @s ["",{{"text":"Assigned to ","color":"white"}},{{"text":"Blue Team","color":"blue","bold":true}}]
""")

	write_versioned_function("players/mp_remove", f"""
scoreboard players set @s {ns}.mp.team 0
scoreboard players set @s {ns}.mp.in_game 0
team leave @s
execute if data storage {ns}:multiplayer game{{state:"active"}} run gamemode spectator @s
tellraw @s [{{"text":"Removed from the game","color":"gray"}}]
""")

	write_versioned_function("players/zb_join", f"""
execute if score @s {ns}.zb.in_game matches 0 if data storage {ns}:zombies game{{state:"active"}} run function {ns}:v{version}/zombies/join_game
execute if score @s {ns}.zb.in_game matches 0 if data storage {ns}:zombies game{{state:"preparing"}} run function {ns}:v{version}/zombies/join_game
scoreboard players set @s {ns}.zb.in_game 1
execute if data storage {ns}:zombies game{{state:"active"}} run team join {ns}.zombies @s
execute if data storage {ns}:zombies game{{state:"preparing"}} run team join {ns}.zombies @s
tellraw @s ["",{{"text":"Joined the ","color":"white"}},{{"text":"Zombies game","color":"dark_green","bold":true}}]
""")

	write_versioned_function("players/zb_remove", f"""
scoreboard players set @s {ns}.zb.in_game 0
team leave @s
execute if data storage {ns}:zombies game{{state:"active"}} run gamemode spectator @s
tellraw @s [{{"text":"Removed from the zombies game","color":"gray"}}]
""")

	write_versioned_function("players/mi_join", f"""
execute if score @s {ns}.mi.in_game matches 0 if data storage {ns}:missions game{{state:"active"}} run function {ns}:v{version}/missions/join_game
execute if score @s {ns}.mi.in_game matches 0 if data storage {ns}:missions game{{state:"preparing"}} run function {ns}:v{version}/missions/join_game
scoreboard players set @s {ns}.mi.in_game 1
scoreboard players set @s {ns}.mp.team 1
execute if data storage {ns}:missions game{{state:"active"}} run team join {ns}.blue @s
execute if data storage {ns}:missions game{{state:"preparing"}} run team join {ns}.blue @s
tellraw @s ["",{{"text":"Joined the ","color":"white"}},{{"text":"Mission","color":"aqua","bold":true}}]
""")

	write_versioned_function("players/mi_remove", f"""
scoreboard players set @s {ns}.mi.in_game 0
scoreboard players set @s {ns}.mp.team 0
team leave @s
execute if data storage {ns}:missions game{{state:"active"}} run gamemode spectator @s
tellraw @s [{{"text":"Removed from the mission","color":"gray"}}]
""")

