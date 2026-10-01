""" Per-gamemode sidebar HUDs. """
# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_versioned_function

from ...helpers.text import Text
from ..gamemodes.bomb.demo.rounds import TIEBREAK_ROUND


# Classes
@dataclass(frozen=True)
class RowState:
	""" One state of a sidebar row: the score value it shows for, then how the right half reads. """
	value: int
	name: str
	color: str
	emoji: str


DOM_ZONE_STATES: tuple[RowState, ...] = (
	RowState(value=0, name="Neutral", color="gray", emoji="⚪ "),
	RowState(value=1, name="Red", color="red", emoji="🔴 "),
	RowState(value=2, name="Blue", color="blue", emoji="🔵 "),
)
""" Owner of a domination zone (`#dom_owner_<zone>`). """
DEMO_SITE_STATES: tuple[RowState, ...] = (
	RowState(value=0, name="Intact", color="gray", emoji="🔹 "),
	RowState(value=1, name="PLANTED", color="red", emoji="💣 "),
	RowState(value=2, name="Destroyed", color="dark_gray", emoji="💥 "),
)
""" State of a demolition bomb site, read off its marker (`mgs.demo_state`). """


# Functions
def write_multiplayer_sidebar() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

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

	## Team sidebar (TDM), with a $(title) macro argument.
	write_versioned_function("multiplayer/create_sidebar_team", f"""
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"$(title)",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	# FFA: ranks players by kills (top 10). Also creates the sidebar (start calls it for ffa); runs every second and on kills.
	ffa_rank_code = f"""
data modify storage {ns}:temp ffa_sb set value [{sb_timer},{sb_spacer},{sb_limit},{sb_spacer}]

scoreboard players set @a {ns}.mp.ffa_rank 0
tag @a[scores={{{ns}.mp.in_game=1..}}] add {ns}.ffa_candidate
"""
	for i in range(1, 11):
		ffa_rank_code += f"""
execute unless entity @a[tag={ns}.ffa_candidate] run return run function {ns}:v{version}/multiplayer/build_sidebar_ffa with storage {ns}:temp
scoreboard players set #ffa_max {ns}.data -1
execute as @a[tag={ns}.ffa_candidate] run scoreboard players operation #ffa_max {ns}.data > @s {ns}.mp.kills
tag @a remove {ns}.ffa_top
execute as @a[tag={ns}.ffa_candidate] if score @s {ns}.mp.kills = #ffa_max {ns}.data run tag @s add {ns}.ffa_top
execute as @p[tag={ns}.ffa_top,sort=arbitrary] run scoreboard players set @s {ns}.mp.ffa_rank {i}
tag @a[tag={ns}.ffa_top] remove {ns}.ffa_top
execute as @a[scores={{{ns}.mp.ffa_rank={i}}}] run tag @s remove {ns}.ffa_candidate
data modify storage {ns}:temp ffa_sb append value [[{{text:" {i}. ",color:"gold"}},{Text.player(ns, f"@a[scores={{{ns}.mp.ffa_rank={i}}}]", color="yellow")}],{{score:{{name:"@a[scores={{{ns}.mp.ffa_rank={i}}}]",objective:"{ns}.mp.kills"}},color:"white"}}]
"""
	ffa_rank_code += f"""
function {ns}:v{version}/multiplayer/build_sidebar_ffa with storage {ns}:temp
"""
	write_versioned_function("multiplayer/refresh_sidebar_ffa", ffa_rank_code)

	write_versioned_function("multiplayer/build_sidebar_ffa", f"""
tag @a remove {ns}.ffa_candidate
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Free For All",color:"gold",bold:true}},contents:$(ffa_sb)}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	## Domination: rebuilt on each score tick, since the sidebar cannot express conditionals.
	write_versioned_function("multiplayer/create_sidebar_dom", f"""
function {ns}:v{version}/multiplayer/refresh_sidebar_dom
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	# Runs every score tick (5 s) and on captures. Each zone line is exactly two components (label left, owner right):
	# bs.sidebar lays out only two halves.
	dom_zone_lines: str = "\n".join(
		f'execute if score #dom_owner_{zone.lower()} {ns}.data matches {s.value} run data modify storage {ns}:temp dom_sb.{zone.lower()} set value '
		f"'[[\" \",{{\"text\":\"{zone}\",\"color\":\"{s.color}\"}}],[\"{s.emoji}\",{{\"text\":\"{s.name}\",\"color\":\"{s.color}\"}}]]'"
		for zone in ("A", "B", "C")
		for s in DOM_ZONE_STATES
	)
	write_versioned_function("multiplayer/refresh_sidebar_dom", f"""
{dom_zone_lines}

function {ns}:v{version}/multiplayer/build_sidebar_dom with storage {ns}:temp dom_sb
""")

	write_versioned_function("multiplayer/build_sidebar_dom", f"""
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Domination",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},$(a),$(b),$(c),{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	## Search & Destroy: the ⏱ line is the round clock, then the fuse once planted. Rebuilt like domination, since the attacking side and bomb state are text.
	## Every line is exactly [left, right]: bs.sidebar drops a third top-level component, so richer content goes in its own array.
	sb_snd_round = f'[{{text:" Round ",color:"gray"}},{{score:{{name:"#snd_round",objective:"{ns}.data"}},color:"white"}}]'
	sb_snd_limit = f'[{{text:" First to ",color:"gray"}},{{score:{{name:"#snd_win_threshold",objective:"{ns}.data"}},color:"white"}}]'

	write_versioned_function("multiplayer/create_sidebar_snd", f"""
function {ns}:v{version}/multiplayer/refresh_sidebar_snd
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	write_versioned_function("multiplayer/refresh_sidebar_snd", f"""
execute if score #snd_attackers {ns}.data matches 1 run data modify storage {ns}:temp snd_sb.atk set value '[[" ⚔ ",{{"text":"Attack","color":"gray"}}],{{"text":"Red","color":"red"}}]'
execute if score #snd_attackers {ns}.data matches 2 run data modify storage {ns}:temp snd_sb.atk set value '[[" ⚔ ",{{"text":"Attack","color":"gray"}}],{{"text":"Blue","color":"blue"}}]'

execute if score #snd_bomb_state {ns}.data matches 0 run data modify storage {ns}:temp snd_sb.bomb set value '[[" 💣 ",{{"text":"Bomb","color":"gray"}}],{{"text":"Loose","color":"gray"}}]'
execute if score #snd_bomb_state {ns}.data matches 0 if entity @a[tag={ns}.snd_carrier] run data modify storage {ns}:temp snd_sb.bomb set value '[[" 💣 ",{{"text":"Bomb","color":"gray"}}],{{"text":"Carried","color":"gold"}}]'
execute if score #snd_bomb_state {ns}.data matches 2 run data modify storage {ns}:temp snd_sb.bomb set value '[[" 💣 ",{{"text":"Bomb","color":"gray"}}],{{"text":"PLANTED","color":"red","bold":true}}]'

function {ns}:v{version}/multiplayer/build_sidebar_snd with storage {ns}:temp snd_sb
""")

	write_versioned_function("multiplayer/build_sidebar_snd", f"""
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Search & Destroy",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},{sb_snd_round},$(atk),$(bomb),{sb_spacer},{sb_snd_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	## Demolition: site rows are read off the site markers (mgs.demo_state), each intact, planted or destroyed on its own.
	## The ⏱ line is the round clock, frozen while a bomb is down.
	sb_demo_round = f'[{{text:" Round ",color:"gray"}},{{score:{{name:"#demo_round",objective:"{ns}.data"}},color:"white"}}]'
	demo_site_lines: str = "\n".join(
		f'execute if entity @e[tag={ns}.demo_obj,tag={ns}.demo_site_{letter},scores={{{ns}.demo_state={s.value}}}] run data modify storage {ns}:temp demo_sb.{letter.lower()} set value '
		f"'[[\" \",{{\"text\":\"Site {letter}\",\"color\":\"{s.color}\"}}],[\"{s.emoji}\",{{\"text\":\"{s.name}\",\"color\":\"{s.color}\"}}]]'"
		for letter in ("A", "B")
		for s in DEMO_SITE_STATES
	)

	write_versioned_function("multiplayer/create_sidebar_demo", f"""
function {ns}:v{version}/multiplayer/refresh_sidebar_demo
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	write_versioned_function("multiplayer/refresh_sidebar_demo", f"""
# Label and team are stored apart, so the decider only relabels the left half.
data modify storage {ns}:temp demo_sb.atk_label set value '[" ⚔ ",{{"text":"Attack","color":"gray"}}]'
execute if score #demo_round {ns}.data matches {TIEBREAK_ROUND}.. run data modify storage {ns}:temp demo_sb.atk_label set value '[" ⚡ ",{{"text":"Decider","color":"gold"}}]'
data modify storage {ns}:temp demo_sb.atk_team set value '{{"text":"—","color":"dark_gray"}}'
execute if score #demo_attackers {ns}.data matches 1 run data modify storage {ns}:temp demo_sb.atk_team set value '{{"text":"Red","color":"red"}}'
execute if score #demo_attackers {ns}.data matches 2 run data modify storage {ns}:temp demo_sb.atk_team set value '{{"text":"Blue","color":"blue"}}'

data modify storage {ns}:temp demo_sb.a set value '[[" ",{{"text":"Site A","color":"dark_gray"}}],{{"text":"—","color":"dark_gray"}}]'
data modify storage {ns}:temp demo_sb.b set value '[[" ",{{"text":"Site B","color":"dark_gray"}}],{{"text":"—","color":"dark_gray"}}]'
{demo_site_lines}

function {ns}:v{version}/multiplayer/build_sidebar_demo with storage {ns}:temp demo_sb
""")

	write_versioned_function("multiplayer/build_sidebar_demo", f"""
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Demolition",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},{sb_demo_round},[$(atk_label),$(atk_team)],{sb_spacer},$(a),$(b)]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	## Hardpoint: team scores, controlling team, time to move. The seconds and their unit share the right half (two components per line).
	sb_hp_rotate = (
		f'[{{text:" Zone",color:"dark_purple"}},'
		f'[{{score:{{name:"#hp_rotate_sec",objective:"{ns}.data"}},color:"white"}},{{text:"s left",color:"gray"}}]]'
	)
	write_versioned_function("multiplayer/create_sidebar_hp", f"""
scoreboard players reset * {ns}.sidebar
function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Hardpoint",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},{sb_hp_rotate},{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

