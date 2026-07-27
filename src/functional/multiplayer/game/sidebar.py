""" Per-gamemode sidebar HUDs. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_multiplayer_sidebar() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Sidebar HUD.

	# Build sidebar content components for reuse
	sb_timer = (
		f'[" ⏱ ",'
		f'[{{score:{{name:"#timer_min",objective:"{ns}.data"}},"color":"yellow"}},'
		f'{{text:":"}},'
		f'{{score:{{name:"#timer_tens",objective:"{ns}.data"}}}},'
		f'{{score:{{name:"#timer_ones",objective:"{ns}.data"}}}}]]'
	)
	sb_red = f'[["", " 🔴 ",{{text:"Red",color:"red"}}],[" ",{{score:{{name:"#red",objective:"{ns}.mp.team"}},color:"white"}}]]'
	sb_blue = f'[["", " 🔵 ",{{text:"Blue",color:"blue"}}],[" ",{{score:{{name:"#blue",objective:"{ns}.mp.team"}},color:"white"}}]]'
	sb_limit = f'[{{text:" First to ",color:"gray"}},{{score:{{name:"#score_limit",objective:"{ns}.data"}},color:"white"}}]'
	sb_spacer = '" "'

	## Team sidebar (TDM/SND) — takes $(title) macro arg
	write_versioned_function("multiplayer/create_sidebar_team", f"""
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"$(title)",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	# FFA sidebar refresh: ranks players by kills, builds sidebar with top 10 Doubles as the sidebar's creation path — start calls it directly for the ffa gamemode Called every second from timer_display and on kills
	ffa_rank_code = f"""
# Initialize sidebar header in storage
data modify storage {ns}:temp ffa_sb set value [{sb_timer},{sb_spacer},{sb_limit},{sb_spacer}]

# Reset ranks and tag candidates
scoreboard players set @a {ns}.mp.ffa_rank 0
tag @a[scores={{{ns}.mp.in_game=1..}}] add {ns}.ffa_candidate
"""
	for i in range(1, 11):
		ffa_rank_code += f"""
# Rank {i}
execute unless entity @a[tag={ns}.ffa_candidate] run return run function {ns}:v{version}/multiplayer/build_sidebar_ffa with storage {ns}:temp
scoreboard players set #ffa_max {ns}.data -1
execute as @a[tag={ns}.ffa_candidate] run scoreboard players operation #ffa_max {ns}.data > @s {ns}.mp.kills
tag @a remove {ns}.ffa_top
execute as @a[tag={ns}.ffa_candidate] if score @s {ns}.mp.kills = #ffa_max {ns}.data run tag @s add {ns}.ffa_top
execute as @p[tag={ns}.ffa_top,sort=arbitrary] run scoreboard players set @s {ns}.mp.ffa_rank {i}
tag @a[tag={ns}.ffa_top] remove {ns}.ffa_top
execute as @a[scores={{{ns}.mp.ffa_rank={i}}}] run tag @s remove {ns}.ffa_candidate
data modify storage {ns}:temp ffa_sb append value [[{{text:" {i}. ",color:"gold"}},{{selector:"@a[scores={{{ns}.mp.ffa_rank={i}}}]",color:"yellow"}}],{{score:{{name:"@a[scores={{{ns}.mp.ffa_rank={i}}}]",objective:"{ns}.mp.kills"}},color:"white"}}]
"""
	ffa_rank_code += f"""
# Build
function {ns}:v{version}/multiplayer/build_sidebar_ffa with storage {ns}:temp
"""
	write_versioned_function("multiplayer/refresh_sidebar_ffa", ffa_rank_code)

	## FFA sidebar build (macro function)
	write_versioned_function("multiplayer/build_sidebar_ffa", f"""
tag @a remove {ns}.ffa_candidate
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Free For All",color:"gold",bold:true}},contents:$(ffa_sb)}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	## Domination sidebar — shows team scores + point ownership per zone Point status display helper (0=⚪, 1=🔴, 2=🔵) — updated each tick via refresh We build DOM point lines that reference #dom_owner_X scores Since sidebar can't do conditionals, we use a helper function to rebuild sidebar each score_tick
	write_versioned_function("multiplayer/create_sidebar_dom", f"""
function {ns}:v{version}/multiplayer/refresh_sidebar_dom
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	# DOM sidebar refresh: rebuilds the sidebar content with current point ownership Called every score_tick (every 5 seconds) and on point captures
	write_versioned_function("multiplayer/refresh_sidebar_dom", f"""
# Build point status strings based on ownership scores
# Zone A
execute if score #dom_owner_a {ns}.data matches 0 run data modify storage {ns}:temp dom_sb.a set value '[" ",{{"text":"A: ","color":"gray"}},"⚪ ",{{"text":"Neutral","color":"gray"}}]'
execute if score #dom_owner_a {ns}.data matches 1 run data modify storage {ns}:temp dom_sb.a set value '[" ",{{"text":"A: ","color":"red"}},"🔴 ",{{"text":"Red","color":"red"}}]'
execute if score #dom_owner_a {ns}.data matches 2 run data modify storage {ns}:temp dom_sb.a set value '[" ",{{"text":"A: ","color":"blue"}},"🔵 ",{{"text":"Blue","color":"blue"}}]'

# Zone B
execute if score #dom_owner_b {ns}.data matches 0 run data modify storage {ns}:temp dom_sb.b set value '[" ",{{"text":"B: ","color":"gray"}},"⚪ ",{{"text":"Neutral","color":"gray"}}]'
execute if score #dom_owner_b {ns}.data matches 1 run data modify storage {ns}:temp dom_sb.b set value '[" ",{{"text":"B: ","color":"red"}},"🔴 ",{{"text":"Red","color":"red"}}]'
execute if score #dom_owner_b {ns}.data matches 2 run data modify storage {ns}:temp dom_sb.b set value '[" ",{{"text":"B: ","color":"blue"}},"🔵 ",{{"text":"Blue","color":"blue"}}]'

# Zone C
execute if score #dom_owner_c {ns}.data matches 0 run data modify storage {ns}:temp dom_sb.c set value '[" ",{{"text":"C: ","color":"gray"}},"⚪ ",{{"text":"Neutral","color":"gray"}}]'
execute if score #dom_owner_c {ns}.data matches 1 run data modify storage {ns}:temp dom_sb.c set value '[" ",{{"text":"C: ","color":"red"}},"🔴 ",{{"text":"Red","color":"red"}}]'
execute if score #dom_owner_c {ns}.data matches 2 run data modify storage {ns}:temp dom_sb.c set value '[" ",{{"text":"C: ","color":"blue"}},"🔵 ",{{"text":"Blue","color":"blue"}}]'

# Build sidebar with dynamic point entries
function {ns}:v{version}/multiplayer/build_sidebar_dom with storage {ns}:temp dom_sb
""")

	write_versioned_function("multiplayer/build_sidebar_dom", f"""
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Domination",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},$(a),$(b),$(c),{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	## Hardpoint sidebar — shows team scores + controlling team + time to move
	write_versioned_function("multiplayer/create_sidebar_hp", f"""
scoreboard players reset * {ns}.sidebar
function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Hardpoint",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},[{{text:" Zone: ",color:"dark_purple"}},{{score:{{name:"#hp_rotate_sec",objective:"{ns}.data"}},color:"white"}},{{text:"s left",color:"gray"}}],{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

