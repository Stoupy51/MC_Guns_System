""" The scoreboard sidebar and the prep-phase shooting block. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers.text import Text


# Functions
def write_zombies_sidebar() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Sidebar HUD.
	write_versioned_function("zombies/create_sidebar", f"""
scoreboard objectives add {ns}.zb_sidebar dummy

# Seed the displayed round to the upcoming round (game.round + 1) so the sidebar
# shows "Round 1" immediately during prep instead of a stale value until start_round runs
execute store result score #zb_round {ns}.data run data get storage {ns}:zombies game.round
scoreboard players add #zb_round {ns}.data 1

# Prep context: game_tick isn't maintaining #zb_alive yet (and a previous game may have left a
# stale value), so seed it once here before the (now rescan-free) refresh_sidebar.
execute store result score #zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]

function {ns}:v{version}/zombies/refresh_sidebar
scoreboard objectives setdisplay sidebar {ns}.zb_sidebar
""")

	write_versioned_function("zombies/refresh_sidebar", f"""
# Zombie count (#zb_alive) is recomputed every tick by game_tick.
scoreboard players operation #zb_total {ns}.data = #zb_alive {ns}.data
scoreboard players operation #zb_total {ns}.data += #zb_to_spawn {ns}.data
execute if score #zb_total {ns}.data matches ..-1 run scoreboard players set #zb_total {ns}.data 0

# Initialize sidebar contents
data modify storage {ns}:temp zb_sb set value [[{{text:"Round",color:"red"}},{{score:{{name:"#zb_round",objective:"{ns}.data"}},color:"gold"}}],[{{text:"Zombies",color:"red"}},{{score:{{name:"#zb_total",objective:"{ns}.data"}},color:"gold"}}]," "]

# Rank players for sidebar display
scoreboard players set @a {ns}.zb.sb_rank 0
tag @a remove {ns}.zb_sb_cand
tag @a[scores={{{ns}.zb.in_game=1}}] add {ns}.zb_sb_cand
function {ns}:v{version}/zombies/sidebar_rank_players

# Build sidebar via macro
function {ns}:v{version}/zombies/build_sidebar with storage {ns}:temp
""")

	# Rank players and append to sidebar (up to 8 players)
	sidebar_rank_code = ""
	for i in range(1, 9):
		sidebar_rank_code += f"""
execute unless entity @a[tag={ns}.zb_sb_cand] run return 0
execute as @a[tag={ns}.zb_sb_cand,limit=1] run scoreboard players set @s {ns}.zb.sb_rank {i}
tag @a[scores={{{ns}.zb.sb_rank={i}}}] remove {ns}.zb_sb_cand
data modify storage {ns}:temp zb_sb append value [{Text.player(ns, f"@a[scores={{{ns}.zb.sb_rank={i}}}]", side="zb", color="green")},{{score:{{name:"@a[scores={{{ns}.zb.sb_rank={i}}}]",objective:"{ns}.zb.points"}},color:"yellow"}}]
"""
	sidebar_rank_code += f"\ntag @a remove {ns}.zb_sb_cand\n"
	write_versioned_function("zombies/sidebar_rank_players", sidebar_rank_code)

	write_versioned_function("zombies/build_sidebar", f"""
scoreboard players reset * {ns}.zb_sidebar
$function #bs.sidebar:create {{objective:"{ns}.zb_sidebar",display_name:{{text:"Zombies",color:"dark_green",bold:true}},contents:$(zb_sb)}}
""")

	# Block shooting during prep
	write_versioned_function("player/right_click", f"""
# Block shooting during zombies prep phase
execute if score @s {ns}.zb.in_game matches 1 if data storage {ns}:zombies game{{state:"preparing"}} run return run scoreboard players set @s {ns}.pending_clicks 0
""", prepend=True)

