""" Leaderboards in `mgs:stats leaderboards`: kept sorted by insertion, shown in dialogs and in holograms placed with the map editor.

Every list holds `{uuid, value}` entries, with `players` on the map boards; names and levels are resolved when a board is shown.
The level boards sort by banked XP, which orders players as their levels do.
"""
# Imports
from stewbeet import Mem, write_versioned_function

from ...config.catalogs import TRIG_LB_MI_MAP_BASE, TRIG_LB_ZB_MAP_BASE, TRIG_LEADERBOARDS
from ..helpers import MGS_TAG

# Constants
TOP: int = 10
""" Rows shown by a board. """
ZB_FILTERS: int = 8
""" Trigger values per Zombies map: all players, then 1 to 7 players. """
HOLOGRAM_RANGE: int = 24
""" Blocks within which a player makes a hologram appear. """


# Functions
def write_boards() -> None:
	""" Write the insertion, the updates, the rendering, the dialogs, the holograms and the admin reset. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	write_insertion(ns, version)
	write_updates(ns, version)
	write_render(ns, version)
	write_board_dialogs(ns, version)
	write_holograms(ns, version)
	write_board_admin(ns, version)


def write_insertion(ns: str, version: str) -> None:
	""" Write `stats/board/insert`: keep the better of the player's entries, at its sorted place, and leave the rank in #lb_k. """
	base: str = f"{ns}:v{version}/stats/board"

	## Macro {path, uuid, value}, with #lb_desc 1 for higher first and the new entry in `{ns}:temp _lb.entry`. Fails when the old entry was as good.
	write_versioned_function("stats/board/insert", f"""
$scoreboard players set #lb_new {ns}.data $(value)
$execute store success score #lb_has {ns}.data store result score #lb_old {ns}.data run data get storage {ns}:stats leaderboards.$(path)[{{uuid:$(uuid)}}].value
execute if score #lb_has {ns}.data matches 1 if score #lb_desc {ns}.data matches 1 if score #lb_old {ns}.data >= #lb_new {ns}.data run return fail
execute if score #lb_has {ns}.data matches 1 if score #lb_desc {ns}.data matches 0 if score #lb_old {ns}.data <= #lb_new {ns}.data run return fail

$data remove storage {ns}:stats leaderboards.$(path)[{{uuid:$(uuid)}}]
$execute unless data storage {ns}:stats leaderboards.$(path) run data modify storage {ns}:stats leaderboards.$(path) set value []
$data modify storage {ns}:temp _lb_walk set from storage {ns}:stats leaderboards.$(path)
scoreboard players set #lb_k {ns}.data 0
function {base}/walk
execute store result storage {ns}:temp _lb.k int 1 run scoreboard players get #lb_k {ns}.data
function {base}/insert_at with storage {ns}:temp _lb
scoreboard players add #lb_k {ns}.data 1
return 1
""")
	## Equal values stay ahead of the newcomer.
	write_versioned_function("stats/board/walk", f"""
execute unless data storage {ns}:temp _lb_walk[0] run return 0
execute store result score #lb_v {ns}.data run data get storage {ns}:temp _lb_walk[0].value
execute if score #lb_desc {ns}.data matches 1 if score #lb_v {ns}.data < #lb_new {ns}.data run return 0
execute if score #lb_desc {ns}.data matches 0 if score #lb_v {ns}.data > #lb_new {ns}.data run return 0
scoreboard players add #lb_k {ns}.data 1
data remove storage {ns}:temp _lb_walk[0]
function {base}/walk
""")
	write_versioned_function("stats/board/insert_at", f"$data modify storage {ns}:stats leaderboards.$(path) insert $(k) from storage {ns}:temp _lb.entry")


def write_updates(ns: str, version: str) -> None:
	""" Write the level boards' update (login and game ends), the Zombies map boards and the Missions times. """
	base: str = f"{ns}:v{version}/stats/board"

	## Macro {uuid, name}: the banked XP of both sides.
	sides: str = "\n".join(
		f'data modify storage {ns}:temp _lb set value {{path:"level_{side}",entry:{{}}}}\n'
		f"$data modify storage {ns}:temp _lb.uuid set value $(uuid)\n"
		f"data modify storage {ns}:temp _lb.entry.uuid set from storage {ns}:temp _lb.uuid\n"
		f"$execute store result storage {ns}:temp _lb.value int 1 store result storage {ns}:temp _lb.entry.value int 1 run scoreboard players get $(name) {ns}.{side}.xp_total\n"
		f"function {base}/insert with storage {ns}:temp _lb"
		for side in ("mp", "zb")
	)
	write_versioned_function("stats/board/levels", f"scoreboard players set #lb_desc {ns}.data 1\n{sides}")

	## Macro {uuid, name, map_id}, with the round in #final_round and the player count in #lb_n. The player-count list decides the record.
	write_versioned_function("stats/board/zb_round", f"""
scoreboard players set #lb_desc {ns}.data 1
$data modify storage {ns}:temp _lb set value {{uuid:$(uuid),name:"$(name)",map_id:"$(map_id)",entry:{{uuid:$(uuid)}},path:'zb_map."$(map_id)".all'}}
execute store result storage {ns}:temp _lb.value int 1 store result storage {ns}:temp _lb.entry.value int 1 run scoreboard players get #final_round {ns}.data
execute store result storage {ns}:temp _lb.entry.players int 1 run scoreboard players get #lb_n {ns}.data
function {base}/insert with storage {ns}:temp _lb

execute store result storage {ns}:temp _lb.n int 1 run scoreboard players get #lb_n {ns}.data
function {base}/zb_round_bucket with storage {ns}:temp _lb
""")
	write_versioned_function("stats/board/zb_round_bucket", f"""
$data modify storage {ns}:temp _lb.path set value 'zb_map."$(map_id)"."$(n)"'
execute store success score #lb_rec {ns}.data run function {base}/insert with storage {ns}:temp _lb
execute if score #lb_rec {ns}.data matches 1 store result storage {ns}:temp _lb.rank int 1 run scoreboard players get #lb_k {ns}.data
execute if score #lb_rec {ns}.data matches 1 run function {base}/announce with storage {ns}:temp _lb
""")

	## Macro {uuid, name, map_id}, with the mission time in #mi_timer (ticks); a lower time is better.
	write_versioned_function("stats/board/mi_time", f"""
scoreboard players set #lb_desc {ns}.data 0
$data modify storage {ns}:temp _lb set value {{uuid:$(uuid),entry:{{uuid:$(uuid)}},path:'mi_map."$(map_id)"'}}
execute store result storage {ns}:temp _lb.value int 1 store result storage {ns}:temp _lb.entry.value int 1 run scoreboard players get #mi_timer {ns}.data
execute store result storage {ns}:temp _lb.entry.players int 1 run scoreboard players get #lb_n {ns}.data
function {base}/insert with storage {ns}:temp _lb
""")

	## Macro {name, value, n, rank}: to the player, when online.
	write_versioned_function("stats/board/announce", f'$tellraw $(name) [{MGS_TAG},{{"text":"New record! ","color":"gold","bold":true}},{{"text":"Round $(value) with $(n) players on this map, rank #$(rank)","color":"yellow"}}]')


def write_render(ns: str, version: str) -> None:
	""" Write `stats/board/render`: the top rows of a board as text components in `{ns}:temp _lb_lines`. """
	base: str = f"{ns}:v{version}/stats/board"
	write_versioned_function("stats/board/render", f"""
data modify storage {ns}:temp _lb_lines set value []
$data modify storage {ns}:temp _lb_walk set from storage {ns}:stats leaderboards.$(path)
scoreboard players set #lb_k {ns}.data 0
$function {base}/render_next {{kind:"$(kind)"}}
""")
	write_versioned_function("stats/board/render_next", f"""
execute unless data storage {ns}:temp _lb_walk[0] run return 0
execute if score #lb_k {ns}.data matches {TOP}.. run return 0

scoreboard players add #lb_k {ns}.data 1
data modify storage {ns}:temp _lb_row set from storage {ns}:temp _lb_walk[0]
execute store result storage {ns}:temp _lb_row.rank int 1 run scoreboard players get #lb_k {ns}.data
execute store result score #lb_v {ns}.data run data get storage {ns}:temp _lb_row.value 0.05
execute store result storage {ns}:temp _lb_row.min int 1 run scoreboard players operation #lb_v {ns}.data /= #60 {ns}.data
execute store result score #lb_v {ns}.data run data get storage {ns}:temp _lb_row.value 0.05
execute store result score #lb_s {ns}.data run scoreboard players operation #lb_v {ns}.data %= #60 {ns}.data
data modify storage {ns}:temp _lb_row.pad set value ""
execute if score #lb_s {ns}.data matches ..9 run data modify storage {ns}:temp _lb_row.pad set value "0"
execute store result storage {ns}:temp _lb_row.sec int 1 run scoreboard players get #lb_s {ns}.data
function {base}/row_player with storage {ns}:temp _lb_row
$function {base}/row_$(kind) with storage {ns}:temp _lb_row

data remove storage {ns}:temp _lb_walk[0]
$function {base}/render_next {{kind:"$(kind)"}}
""")
	write_versioned_function("stats/board/row_player", f"""
$data modify storage {ns}:temp _lb_row.name set from storage {ns}:stats players."$(uuid)".name
$data modify storage {ns}:temp _lb_row.level set from storage {ns}:stats players."$(uuid)".level
data modify storage {ns}:temp _lb_row.lmp set from storage {ns}:temp _lb_row.level.mp
data modify storage {ns}:temp _lb_row.lzb set from storage {ns}:temp _lb_row.level.zb
""")
	head: str = '{text:"#$(rank) ",color:"gold"},{text:"$(name)",color:"yellow"}'
	rows: dict[str, str] = {
		"level_mp": '{text:" - Level $(lmp)",color:"aqua"}',
		"level_zb": '{text:" - Level $(lzb)",color:"aqua"}',
		"zb_map": '{text:" - Round $(value)",color:"red"},{text:" ($(players)P)",color:"gray"}',
		"mi_map": '{text:" - $(min):$(pad)$(sec)",color:"aqua"},{text:" ($(players)P)",color:"gray"}',
	}
	for kind, tail in rows.items():
		write_versioned_function(f"stats/board/row_{kind}", f'$data modify storage {ns}:temp _lb_lines append value ["",{head},{tail},"\\n"]')


def write_board_dialogs(ns: str, version: str) -> None:
	""" Write the leaderboards menu, the map lists and a board's page with the viewer's rank. """
	base: str = f"{ns}:v{version}/stats/board"
	trigger: str = f"/trigger {ns}.player.config set"
	menu: str = ",".join((
		f'{{label:{{text:"Multiplayer Level",color:"gold"}},action:{{type:"run_command",command:"{trigger} {TRIG_LEADERBOARDS + 1}"}}}}',
		f'{{label:{{text:"Zombies Level",color:"green"}},action:{{type:"run_command",command:"{trigger} {TRIG_LEADERBOARDS + 2}"}}}}',
		f'{{label:{{text:"Zombies Maps",color:"red"}},action:{{type:"run_command",command:"{trigger} {TRIG_LEADERBOARDS + 3}"}}}}',
		f'{{label:{{text:"Missions Maps",color:"aqua"}},action:{{type:"run_command",command:"{trigger} {TRIG_LEADERBOARDS + 4}"}}}}',
		f'{{label:{{text:"Settings",color:"gray"}},action:{{type:"run_command",command:"{trigger} 1"}}}}',
	))
	write_versioned_function("stats/board/menu", f"""
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","🏆 ",{{text:"Leaderboards",color:"gold",bold:true}}],actions:[{menu}],columns:2,after_action:"close",exit_action:{{label:{{translate:"gui.done"}}}}}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## Run from the trigger dispatch, as the viewer.
	write_versioned_function("stats/board/dispatch", f"""
execute if score @s {ns}.player.config matches {TRIG_LEADERBOARDS} run return run function {base}/menu
execute if score @s {ns}.player.config matches {TRIG_LEADERBOARDS + 1} run return run function {base}/show {{path:"level_mp",kind:"level_mp",title:"Multiplayer Level",filters:0b}}
execute if score @s {ns}.player.config matches {TRIG_LEADERBOARDS + 2} run return run function {base}/show {{path:"level_zb",kind:"level_zb",title:"Zombies Level",filters:0b}}
execute if score @s {ns}.player.config matches {TRIG_LEADERBOARDS + 3} run return run function {base}/maps {{mode:"zombies",base:{TRIG_LB_ZB_MAP_BASE},step:{ZB_FILTERS}}}
execute if score @s {ns}.player.config matches {TRIG_LEADERBOARDS + 4} run return run function {base}/maps {{mode:"missions",base:{TRIG_LB_MI_MAP_BASE},step:1}}
execute if score @s {ns}.player.config matches {TRIG_LB_ZB_MAP_BASE}..{TRIG_LB_ZB_MAP_BASE + 999} run return run function {base}/zb_map_trigger
execute if score @s {ns}.player.config matches {TRIG_LB_MI_MAP_BASE}..{TRIG_LB_ZB_MAP_BASE - 1} run return run function {base}/mi_map_trigger
""")

	## Macro {mode, base, step}: one button per map of the mode, its trigger `base + index * step`.
	write_versioned_function("stats/board/maps", f"""
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","🏆 ",{{text:"Pick a map",color:"gold",bold:true}}],actions:[],columns:2,after_action:"close",exit_action:{{label:{{translate:"gui.done"}}}}}}
$data modify storage {ns}:temp _lb_maps set from storage {ns}:maps $(mode)
$scoreboard players set #lb_t {ns}.data $(base)
$scoreboard players set #lb_step {ns}.data $(step)
function {base}/maps_next
data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Back",color:"gray"}},action:{{type:"run_command",command:"{trigger} {TRIG_LEADERBOARDS}"}}}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
	write_versioned_function("stats/board/maps_next", f"""
execute unless data storage {ns}:temp _lb_maps[0] run return 0
execute store result storage {ns}:temp _lb_maps[0].trigger int 1 run scoreboard players get #lb_t {ns}.data
function {base}/maps_button with storage {ns}:temp _lb_maps[0]
scoreboard players operation #lb_t {ns}.data += #lb_step {ns}.data
data remove storage {ns}:temp _lb_maps[0]
function {base}/maps_next
""")
	write_versioned_function("stats/board/maps_button", f'$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"yellow"}},action:{{type:"run_command",command:"{trigger} $(trigger)"}}}}')

	## The map index and the filter come out of the trigger value; filter 0 is every player count.
	for mode, trigger_base, step, filters in (("zb", TRIG_LB_ZB_MAP_BASE, ZB_FILTERS, "1b"), ("mi", TRIG_LB_MI_MAP_BASE, 1, "0b")):
		write_versioned_function(f"stats/board/{mode}_map_trigger", f"""
scoreboard players set #lb_step {ns}.data {step}
scoreboard players operation #lb_t {ns}.data = @s {ns}.player.config
scoreboard players remove #lb_t {ns}.data {trigger_base}
scoreboard players operation #lb_f {ns}.data = #lb_t {ns}.data
scoreboard players operation #lb_f {ns}.data %= #lb_step {ns}.data
scoreboard players operation #lb_t {ns}.data /= #lb_step {ns}.data
data modify storage {ns}:temp _lb_view set value {{kind:"{mode}_map",filters:{filters}}}
execute store result storage {ns}:temp _lb_view.i int 1 run scoreboard players get #lb_t {ns}.data
execute store result storage {ns}:temp _lb_view.f int 1 run scoreboard players get #lb_f {ns}.data
execute store result storage {ns}:temp _lb_view.trigger int 1 run scoreboard players operation #lb_t {ns}.data *= #lb_step {ns}.data
execute store result storage {ns}:temp _lb_view.trigger int 1 run scoreboard players add #lb_t {ns}.data {trigger_base}
function {base}/{mode}_map_view with storage {ns}:temp _lb_view
""")
	write_versioned_function("stats/board/zb_map_view", f"""
$data modify storage {ns}:temp _lb_view.map set from storage {ns}:maps zombies[$(i)]
$data modify storage {ns}:temp _lb_view.bucket set value "$(f)"
execute if data storage {ns}:temp _lb_view{{f:0}} run data modify storage {ns}:temp _lb_view.bucket set value "all"
data modify storage {ns}:temp _lb_view.id set from storage {ns}:temp _lb_view.map.id
data modify storage {ns}:temp _lb_view.name set from storage {ns}:temp _lb_view.map.name
function {base}/zb_map_path with storage {ns}:temp _lb_view
""")
	write_versioned_function("stats/board/zb_map_path", f"""
$data modify storage {ns}:temp _lb_view.path set value 'zb_map."$(id)"."$(bucket)"'
$data modify storage {ns}:temp _lb_view.title set value "$(name)"
function {base}/show with storage {ns}:temp _lb_view
""")
	write_versioned_function("stats/board/mi_map_view", f"""
$data modify storage {ns}:temp _lb_view.map set from storage {ns}:maps missions[$(i)]
data modify storage {ns}:temp _lb_view.id set from storage {ns}:temp _lb_view.map.id
data modify storage {ns}:temp _lb_view.name set from storage {ns}:temp _lb_view.map.name
function {base}/mi_map_path with storage {ns}:temp _lb_view
""")
	write_versioned_function("stats/board/mi_map_path", f"""
$data modify storage {ns}:temp _lb_view.path set value 'mi_map."$(id)"'
$data modify storage {ns}:temp _lb_view.title set value "$(name)"
function {base}/show with storage {ns}:temp _lb_view
""")

	## Macro {path, kind, title, filters}, `filters` rendered as 1 or 0: the top rows, the viewer's rank, and for a Zombies map the player count filters.
	filter_buttons: list[str] = [
		f'{{label:{{text:"{label}",color:"aqua"}},action:{{type:"run_command",command:"{trigger} $(f{index})"}}}}'
		for index, label in enumerate(("All", "1 player", "2 players", "3 players", "4 players"))
	]
	write_versioned_function("stats/board/show", f"""
$function {base}/render {{path:'$(path)',kind:"$(kind)"}}
$data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","🏆 ",{{text:"$(title)",color:"gold",bold:true}}],body:[{{type:"minecraft:plain_message",width:300,contents:[""]}}],actions:[],columns:3,after_action:"close",exit_action:{{label:{{translate:"gui.done"}}}}}}
data modify storage {ns}:temp dialog.body[0].contents append from storage {ns}:temp _lb_lines[]
execute unless data storage {ns}:temp _lb_lines[0] run data modify storage {ns}:temp dialog.body[0].contents append value {{text:"No entries yet",color:"gray"}}

$data modify storage {ns}:temp _lb_walk set from storage {ns}:stats leaderboards.$(path)
data modify storage {ns}:temp _lb_me set from entity @s UUID
scoreboard players set #lb_k {ns}.data 1
execute store success score #lb_found {ns}.data run function {base}/find_me
execute if score #lb_found {ns}.data matches 1 store result storage {ns}:temp _lb_rank.k int 1 run scoreboard players get #lb_k {ns}.data
execute if score #lb_found {ns}.data matches 1 run function {base}/show_rank with storage {ns}:temp _lb_rank

$data modify storage {ns}:temp _lb_f set value $(filters)
execute if data storage {ns}:temp {{_lb_f:1}} run function {base}/filters with storage {ns}:temp _lb_view
data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Back",color:"gray"}},action:{{type:"run_command",command:"{trigger} {TRIG_LEADERBOARDS}"}}}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
	write_versioned_function("stats/board/find_me", f"""
execute unless data storage {ns}:temp _lb_walk[0] run return fail
data modify storage {ns}:temp _lb_cmp set from storage {ns}:temp _lb_walk[0].uuid
execute store success score #lb_diff {ns}.data run data modify storage {ns}:temp _lb_cmp set from storage {ns}:temp _lb_me
execute if score #lb_diff {ns}.data matches 0 run return 1
scoreboard players add #lb_k {ns}.data 1
data remove storage {ns}:temp _lb_walk[0]
return run function {base}/find_me
""")
	write_versioned_function("stats/board/show_rank", f'$data modify storage {ns}:temp dialog.body append value {{type:"minecraft:plain_message",contents:["",{{text:"Your rank",color:"gray"}},": ",{{text:"#$(k)",color:"gold"}}]}}')
	write_versioned_function("stats/board/filters", "\n".join((
		f"$scoreboard players set #lb_t {ns}.data $(trigger)",
		*(f"execute store result storage {ns}:temp _lb_view.f{index} int 1 run scoreboard players add #lb_t {ns}.data {min(index, 1)}" for index in range(5)),
		f"function {base}/filters_add with storage {ns}:temp _lb_view",
	)))
	write_versioned_function("stats/board/filters_add", "\n".join(f"$data modify storage {ns}:temp dialog.actions append value {button}" for button in filter_buttons))


def write_holograms(ns: str, version: str) -> None:
	""" Write the Zombies map holograms: a marker per placed leaderboard, showing its board while a player is near. """
	base: str = f"{ns}:v{version}/stats/board"

	## Run at the end of zombies/preload_complete; a `map_id` left empty means the map being played.
	write_versioned_function("zombies/preload_complete", f"""
data modify storage {ns}:temp _lb_iter set from storage {ns}:zombies game.map.leaderboards
execute if data storage {ns}:temp _lb_iter[0] run function {base}/holo_setup
execute if data storage {ns}:zombies game.map.leaderboards[0] run schedule function {base}/holo_tick 1s replace
""")
	write_versioned_function("stats/board/holo_setup", f"""
data modify storage {ns}:temp _lb_h set from storage {ns}:temp _lb_iter[0]
execute unless data storage {ns}:temp _lb_h.map_id run data modify storage {ns}:temp _lb_h.map_id set value ""
execute if data storage {ns}:temp _lb_h{{map_id:""}} run data modify storage {ns}:temp _lb_h.map_id set from storage {ns}:zombies game.map_id
execute store result storage {ns}:temp _lb_h.x int 1 run data get storage {ns}:temp _lb_h.pos[0]
execute store result storage {ns}:temp _lb_h.y int 1 run data get storage {ns}:temp _lb_h.pos[1]
execute store result storage {ns}:temp _lb_h.z int 1 run data get storage {ns}:temp _lb_h.pos[2]
function {base}/holo_place with storage {ns}:temp _lb_h

data remove storage {ns}:temp _lb_iter[0]
execute if data storage {ns}:temp _lb_iter[0] run function {base}/holo_setup
""")
	## Positions are relative to the map's base, like every saved element.
	write_versioned_function("stats/board/holo_place", f"""
$scoreboard players set #lbx {ns}.data $(x)
$scoreboard players set #lby {ns}.data $(y)
$scoreboard players set #lbz {ns}.data $(z)
execute store result storage {ns}:temp _lb_h.x int 1 run scoreboard players operation #lbx {ns}.data += #gm_base_x {ns}.data
execute store result storage {ns}:temp _lb_h.y int 1 run scoreboard players operation #lby {ns}.data += #gm_base_y {ns}.data
execute store result storage {ns}:temp _lb_h.z int 1 run scoreboard players operation #lbz {ns}.data += #gm_base_z {ns}.data
data modify storage {ns}:temp _lb_h.kind set from storage {ns}:temp _lb_h.board
function {base}/holo_path with storage {ns}:temp _lb_h
""")
	write_versioned_function("stats/board/holo_path", f"""
$data modify storage {ns}:temp _lb_h.path set value "$(board)"
$execute if data storage {ns}:temp _lb_h{{board:"zb_map"}} run data modify storage {ns}:temp _lb_h.path set value 'zb_map."$(map_id)"."$(players)"'
$execute if data storage {ns}:temp _lb_h{{board:"mi_map"}} run data modify storage {ns}:temp _lb_h.path set value 'mi_map."$(map_id)"'
$summon minecraft:marker $(x).5 $(y) $(z).5 {{CustomName:"Leaderboard",Tags:["{ns}.leaderboard","{ns}.zombies_entity","{ns}.lb_new"]}}
data modify entity @n[type=minecraft:marker,tag={ns}.lb_new] data.lb set from storage {ns}:temp _lb_h
tag @e[type=minecraft:marker,tag={ns}.lb_new] remove {ns}.lb_new
""")

	write_versioned_function("stats/board/holo_tick", f"""
execute as @e[type=minecraft:marker,tag={ns}.leaderboard] at @s run function {base}/holo_one
execute if entity @e[type=minecraft:marker,tag={ns}.leaderboard] run schedule function {base}/holo_tick 1s replace
""")
	write_versioned_function("stats/board/holo_one", f"""
execute if entity @s[tag={ns}.lb_shown] unless entity @a[distance=..{HOLOGRAM_RANGE}] run function {base}/holo_hide
execute if entity @s[tag=!{ns}.lb_shown] if entity @a[distance=..{HOLOGRAM_RANGE}] run function {base}/holo_show
""")
	write_versioned_function("stats/board/holo_hide", f"""
tag @s remove {ns}.lb_shown
kill @e[type=minecraft:text_display,tag={ns}.lb_text,distance=..0.1]
""")
	titles: str = "\n".join(
		f'execute if data entity @s data.lb{{kind:"{kind}"}} run data modify storage {ns}:temp _lb_text set value ["",{{text:"{title}",color:"gold",bold:true}},"\\n"]'
		for kind, title in (("level_mp", "Multiplayer Level"), ("level_zb", "Zombies Level"), ("zb_map", "Best Rounds"), ("mi_map", "Best Times"))
	)
	write_versioned_function("stats/board/holo_show", f"""
tag @s add {ns}.lb_shown
function {base}/render with entity @s data.lb
{titles}
data modify storage {ns}:temp _lb_text append from storage {ns}:temp _lb_lines[]
execute unless data storage {ns}:temp _lb_lines[0] run data modify storage {ns}:temp _lb_text append value {{text:"No entries yet",color:"gray"}}
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.lb_text","{ns}.zombies_entity","{ns}.lb_new"],billboard:"vertical",alignment:"center",default_background:true}}
data modify entity @n[type=minecraft:text_display,tag={ns}.lb_new] text set from storage {ns}:temp _lb_text
tag @e[type=minecraft:text_display,tag={ns}.lb_new] remove {ns}.lb_new
""")
	## After an update, so the next tick rebuilds every shown board.
	write_versioned_function("stats/board/refresh_holograms", f"""
kill @e[type=minecraft:text_display,tag={ns}.lb_text]
tag @e[type=minecraft:marker,tag={ns}.leaderboard] remove {ns}.lb_shown
""")


def write_board_admin(ns: str, version: str) -> None:
	""" Write the operator dialog resetting one map's leaderboard. """
	base: str = f"{ns}:v{version}/stats/board"
	write_versioned_function("stats/admin/boards", f"""
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:{{text:"Reset a Map Leaderboard",color:"red",bold:true}},actions:[],columns:2,exit_action:{{label:{{translate:"gui.done"}}}}}}
data modify storage {ns}:temp _lb_maps set from storage {ns}:maps zombies
function {base}/admin_next {{board:"zb_map",label:"Zombies"}}
data modify storage {ns}:temp _lb_maps set from storage {ns}:maps missions
function {base}/admin_next {{board:"mi_map",label:"Missions"}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
	write_versioned_function("stats/board/admin_next", f"""
execute unless data storage {ns}:temp _lb_maps[0] run return 0
$data modify storage {ns}:temp _lb_maps[0].board set value "$(board)"
$data modify storage {ns}:temp _lb_maps[0].label set value "$(label)"
function {base}/admin_button with storage {ns}:temp _lb_maps[0]
data remove storage {ns}:temp _lb_maps[0]
$function {base}/admin_next {{board:"$(board)",label:"$(label)"}}
""")
	write_versioned_function("stats/board/admin_button", f'$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(label): $(name)",color:"yellow"}},action:{{type:"run_command",command:"/function {ns}:v{version}/stats/admin/reset_board {{board:$(board),id:$(id)}}"}}}}')
	write_versioned_function("stats/admin/reset_board", f"""
$data remove storage {ns}:stats leaderboards.$(board)."$(id)"
function {base}/refresh_holograms
$tellraw @s [{MGS_TAG},{{"text":"Leaderboard reset: $(id)","color":"yellow"}}]
""")

