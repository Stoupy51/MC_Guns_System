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

	## Team sidebar (TDM) — takes $(title) macro arg
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
	# Each zone line is two components — the label on the left, the owner on the right. They used to be
	# four (" ", "A: ", the emoji, the owner name), which bs.sidebar cannot lay out: only the first two
	# would have had a side, so the zone rows never rendered at all.
	dom_zone_states: list[tuple[int, str, str, str]] = [
		(0, "gray", "⚪ ", "Neutral"),
		(1, "red",  "🔴 ", "Red"),
		(2, "blue", "🔵 ", "Blue"),
	]
	dom_zone_lines: str = "\n".join(
		f'execute if score #dom_owner_{zone.lower()} {ns}.data matches {owner} run data modify storage {ns}:temp dom_sb.{zone.lower()} set value '
		f"'[[\" \",{{\"text\":\"{zone}\",\"color\":\"{color}\"}}],[\"{emoji}\",{{\"text\":\"{name}\",\"color\":\"{color}\"}}]]'"
		for zone in ("A", "B", "C")
		for owner, color, emoji, name in dom_zone_states
	)
	write_versioned_function("multiplayer/refresh_sidebar_dom", f"""
# Build point status strings based on ownership scores
{dom_zone_lines}

# Build sidebar with dynamic point entries
function {ns}:v{version}/multiplayer/build_sidebar_dom with storage {ns}:temp dom_sb
""")

	write_versioned_function("multiplayer/build_sidebar_dom", f"""
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Domination",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},$(a),$(b),$(c),{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	## Search & Destroy sidebar — round number, round wins, which side attacks, bomb state.
	## The ⏱ line is the ROUND clock here (and the bomb fuse once planted): the gamemode writes #mp_timer
	## itself, because a match time limit cannot arbitrate a first-to-4 format.
	## Rebuilt rather than refreshed for the same reason as domination: the attacking side and the bomb
	## state are text, and no score component can express text.
	##
	## Every line is EXACTLY two components — `[left, right]`. bs.sidebar renders one entry as a left half
	## and a right half, so a third top-level component is not laid out anywhere and the line silently
	## disappears. Anything richer than one component per side has to be wrapped in its own array.
	sb_snd_round = f'[{{text:" Round ",color:"gray"}},{{score:{{name:"#snd_round",objective:"{ns}.data"}},color:"white"}}]'
	sb_snd_limit = f'[{{text:" First to ",color:"gray"}},{{score:{{name:"#snd_win_threshold",objective:"{ns}.data"}},color:"white"}}]'

	write_versioned_function("multiplayer/create_sidebar_snd", f"""
function {ns}:v{version}/multiplayer/refresh_sidebar_snd
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	write_versioned_function("multiplayer/refresh_sidebar_snd", f"""
# Which side is attacking
execute if score #snd_attackers {ns}.data matches 1 run data modify storage {ns}:temp snd_sb.atk set value '[[" ⚔ ",{{"text":"Attack","color":"gray"}}],{{"text":"Red","color":"red"}}]'
execute if score #snd_attackers {ns}.data matches 2 run data modify storage {ns}:temp snd_sb.atk set value '[[" ⚔ ",{{"text":"Attack","color":"gray"}}],{{"text":"Blue","color":"blue"}}]'

# Bomb state: on the ground, on someone's back, or ticking
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

	## Demolition sidebar — round wins, which side attacks, and the state of each bomb site.
	## Site state is read off the site MARKERS (mgs.demo_state), so the rows are built by testing tagged
	## entities rather than fake-player scores: a site is intact, planted or destroyed independently.
	## The ⏱ line is the round clock, which this mode freezes while any bomb is down.
	sb_demo_round = f'[{{text:" Round ",color:"gray"}},{{score:{{name:"#demo_round",objective:"{ns}.data"}},color:"white"}}]'
	demo_site_states: list[tuple[str, str, str, str]] = [
		("demo_state=0", "Intact",    "gray",      "🔹 "),
		("demo_state=1", "PLANTED",   "red",       "💣 "),
		("demo_state=2", "Destroyed", "dark_gray", "💥 "),
	]
	demo_site_lines: str = "\n".join(
		f'execute if entity @e[tag={ns}.demo_obj,tag={ns}.demo_site_{letter},scores={{{ns}.{state}}}] run data modify storage {ns}:temp demo_sb.{letter.lower()} set value '
		f"'[[\" \",{{\"text\":\"Site {letter}\",\"color\":\"{color}\"}}],[\"{emoji}\",{{\"text\":\"{name}\",\"color\":\"{color}\"}}]]'"
		for letter in ("A", "B")
		for state, name, color, emoji in demo_site_states
	)

	write_versioned_function("multiplayer/create_sidebar_demo", f"""
function {ns}:v{version}/multiplayer/refresh_sidebar_demo
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	write_versioned_function("multiplayer/refresh_sidebar_demo", f"""
# Which side is attacking (in overtime both are, and the row says so)
execute if score #demo_attackers {ns}.data matches 1 run data modify storage {ns}:temp demo_sb.atk set value '[[" ⚔ ",{{"text":"Attack","color":"gray"}}],{{"text":"Red","color":"red"}}]'
execute if score #demo_attackers {ns}.data matches 2 run data modify storage {ns}:temp demo_sb.atk set value '[[" ⚔ ",{{"text":"Attack","color":"gray"}}],{{"text":"Blue","color":"blue"}}]'
execute if score #demo_round {ns}.data matches 3.. run data modify storage {ns}:temp demo_sb.atk set value '[[" ⚡ ",{{"text":"Overtime","color":"gray"}}],{{"text":"Both","color":"gold"}}]'

# One row per site, read off that site's own marker. Both rows stay meaningful in overtime: the sites are
# the same two, they just belong to nobody, so there is no third layout to describe here.
data modify storage {ns}:temp demo_sb.a set value '[[" ",{{"text":"Site A","color":"dark_gray"}}],{{"text":"—","color":"dark_gray"}}]'
data modify storage {ns}:temp demo_sb.b set value '[[" ",{{"text":"Site B","color":"dark_gray"}}],{{"text":"—","color":"dark_gray"}}]'
{demo_site_lines}

function {ns}:v{version}/multiplayer/build_sidebar_demo with storage {ns}:temp demo_sb
""")

	write_versioned_function("multiplayer/build_sidebar_demo", f"""
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Demolition",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},{sb_demo_round},$(atk),{sb_spacer},$(a),$(b)]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	## Hardpoint sidebar — shows team scores + controlling team + time to move
	## The rotation line was three components (label, seconds, "s left"), one too many for a two-sided
	## entry, so it never rendered: the seconds and the unit now share the right half.
	sb_hp_rotate = (
		f'[{{text:" Zone",color:"dark_purple"}},'
		f'[{{score:{{name:"#hp_rotate_sec",objective:"{ns}.data"}},color:"white"}},{{text:"s left",color:"gray"}}]]'
	)
	write_versioned_function("multiplayer/create_sidebar_hp", f"""
scoreboard players reset * {ns}.sidebar
function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Hardpoint",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},{sb_hp_rotate},{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

