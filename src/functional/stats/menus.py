""" The stats dialogs: one player's page per mode, and the known players, 10 per page. Built per viewer from `mgs:stats`. """
# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_versioned_function

from ...config.catalogs import TRIG_PLAYER_STATS_BASE, TRIG_PLAYERS_PAGE_BASE
from ..multiplayer.gamemodes.dispatch import GAMEMODES
from .catalog import GAMEMODE_NAMES, MODES, MULTIPLAYER, StatMode


# Classes
@dataclass(frozen=True)
class Ratio:
	""" A value computed at display, shown with one decimal. """
	field: str
	label: str
	numerator: str
	denominator: str
	scale: int
	""" 10 for a plain ratio, 1000 for a percentage. """
	suffix: str = ""


# Constants
PAGE_SIZE: int = 10
""" Players listed per page. """
STAT_PAGES: int = 4
""" Trigger values reserved per player, one per mode and a spare, so `TRIG_PLAYER_STATS_BASE + index * 4 + mode`. """
RATIOS: dict[str, tuple[Ratio, ...]] = {
	"mp": (
		Ratio(field="kd", label="K/D", numerator="kills", denominator="deaths", scale=10),
		Ratio(field="win_rate", label="Win rate", numerator="wins", denominator="games", scale=1000, suffix="%"),
	),
	"mi": (Ratio(field="kd", label="K/D", numerator="kills", denominator="deaths", scale=10),),
}
""" Per mode, the ratios computed at display. A zero denominator counts as 1. """


# Functions
def write_stats_menus() -> None:
	""" Write the trigger entry points, the per-mode stats pages and the players list. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	base: str = f"{ns}:v{version}/stats/menu"

	write_versioned_function("stats/menu/mine", f"""
scoreboard players operation #st_i {ns}.data = @s {ns}.st.index
scoreboard players set #st_m {ns}.data 0
function {base}/view
""")

	write_versioned_function("stats/menu/view_trigger", f"""
scoreboard players operation #st_m {ns}.data = @s {ns}.player.config
scoreboard players remove #st_m {ns}.data {TRIG_PLAYER_STATS_BASE}
scoreboard players operation #st_i {ns}.data = #st_m {ns}.data
scoreboard players operation #st_i {ns}.data /= #{STAT_PAGES} {ns}.data
scoreboard players operation #st_m {ns}.data %= #{STAT_PAGES} {ns}.data
function {base}/view
""")

	## #st_i is the known index, #st_m the mode. An online player is snapshotted first, so their page is current.
	write_versioned_function("stats/menu/view", f"""
data modify storage {ns}:temp _sv set value {{}}
execute store result storage {ns}:temp _sv.i int 1 run scoreboard players get #st_i {ns}.data
function {base}/fetch with storage {ns}:temp _sv
execute unless data storage {ns}:temp _sv.p run return fail

{chr(10).join(f"execute if score #st_m {ns}.data matches {index} run function {base}/{mode.key}" for index, mode in enumerate(MODES))}
""")
	write_versioned_function("stats/menu/fetch", f"""
$execute as @a[scores={{{ns}.st.index=$(i)}}] run function {base}/refresh_self
$data modify storage {ns}:temp _sv.uuid set from storage {ns}:stats known[$(i)]
function {base}/fetch_entry with storage {ns}:temp _sv
""")
	write_versioned_function("stats/menu/fetch_entry", f'$data modify storage {ns}:temp _sv.p set from storage {ns}:stats players."$(uuid)"')
	write_versioned_function("stats/menu/refresh_self", f"""
data modify storage {ns}:temp _st_one set value {{}}
data modify storage {ns}:temp _st_one.uuid set from entity @s UUID
function {ns}:v{version}/stats/snapshot/by_uuid with storage {ns}:temp _st_one
""")

	for index, mode in enumerate(MODES):
		write_mode_page(ns, version, index, mode)

	write_players_page(ns, version)


def write_mode_page(ns: str, version: str, index: int, mode: StatMode) -> None:
	""" Write one mode's page: flatten the entry into `_sv.d`, add the computed fields, then show the dialog. """
	base: str = f"{ns}:v{version}/stats/menu"
	flat: str = f"{ns}:temp _sv.d"

	prepare: list[str] = [
		f"data modify storage {flat} set from storage {ns}:temp _sv.p.{mode.key}",
		f"data modify storage {flat}.name set from storage {ns}:temp _sv.p.name",
		f"data modify storage {flat}.i set from storage {ns}:temp _sv.i",
	]
	prepare += [
		f"execute store result storage {flat}.{stat.key} int {stat.scale} run data get storage {flat}.{stat.key}"
		for stat in mode.stats if stat.scale != 1
	]
	prepare += [
		f"execute store result score #st_t {ns}.data run data get storage {flat}.time",
		f"scoreboard players operation #st_t {ns}.data /= #60 {ns}.data",
		f"scoreboard players operation #st_n {ns}.data = #st_t {ns}.data",
		f"execute store result storage {flat}.time_h int 1 run scoreboard players operation #st_n {ns}.data /= #60 {ns}.data",
		f"execute store result storage {flat}.time_m int 1 run scoreboard players operation #st_t {ns}.data %= #60 {ns}.data",
	]
	for ratio in RATIOS.get(mode.key, ()):
		prepare += [
			f"execute store result score #st_n {ns}.data run data get storage {flat}.{ratio.numerator} {ratio.scale}",
			f"execute store result score #st_d {ns}.data run data get storage {flat}.{ratio.denominator}",
			f"execute if score #st_d {ns}.data matches 0 run scoreboard players set #st_d {ns}.data 1",
			f"scoreboard players operation #st_n {ns}.data /= #st_d {ns}.data",
			f"scoreboard players operation #st_d {ns}.data = #st_n {ns}.data",
			f"execute store result storage {flat}.{ratio.field}_i int 1 run scoreboard players operation #st_n {ns}.data /= #10 {ns}.data",
			f"execute store result storage {flat}.{ratio.field}_d int 1 run scoreboard players operation #st_d {ns}.data %= #10 {ns}.data",
		]
	if mode is MULTIPLAYER:
		prepare += [
			f"data modify storage {flat}.{gamemode}_{key} set from storage {ns}:temp _sv.p.mp.modes.{gamemode}.{key}"
			for gamemode in GAMEMODES for key in ("games", "wins")
		]

	write_versioned_function(f"stats/menu/{mode.key}", "\n".join(prepare) + f"\nfunction {base}/{mode.key}_dialog with storage {flat}\n")

	lines: list[str] = [
		f'{{text:"{stat.label}",color:"gray"}},": ",{{text:"$({stat.key})",color:"white"}}'
		for stat in mode.stats if stat.key != "time"
	]
	lines.append('{text:"Time played",color:"gray"},": ",{text:"$(time_h)h $(time_m)m",color:"white"}')
	lines += [
		f'{{text:"{ratio.label}",color:"gray"}},": ",{{text:"$({ratio.field}_i).$({ratio.field}_d){ratio.suffix}",color:"white"}}'
		for ratio in RATIOS.get(mode.key, ())
	]
	if mode is MULTIPLAYER:
		lines += [
			f'{{text:"{GAMEMODE_NAMES[gamemode]}",color:"gray"}},": ",{{text:"$({gamemode}_wins) / $({gamemode}_games)",color:"white"}},{{text:" wins",color:"gray"}}'
			for gamemode in GAMEMODES
		]
	body: str = ',"\\n",'.join(lines)

	tabs: str = ",".join(
		f'{{label:{{text:"{other.label}",color:"{"gold" if other is mode else "gray"}"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(trigger_{other.key})"}}}}'
		for other in MODES
	)
	write_versioned_function(f"stats/menu/{mode.key}_dialog", f"""
$scoreboard players set #st_t {ns}.data $(i)
scoreboard players operation #st_t {ns}.data *= #{STAT_PAGES} {ns}.data
scoreboard players add #st_t {ns}.data {TRIG_PLAYER_STATS_BASE - 1}
{chr(10).join(f"execute store result storage {ns}:temp _sv.t.trigger_{other.key} int 1 run scoreboard players add #st_t {ns}.data 1" for other in MODES)}
$data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["",{{text:"$(name)",color:"gold",bold:true}},{{text:" - {mode.label}",color:"yellow"}}],body:[{{type:"minecraft:plain_message",width:300,contents:["",{body}]}}],actions:[],columns:3,after_action:"close",exit_action:{{label:{{translate:"gui.done"}}}}}}
function {base}/{mode.key}_tabs with storage {ns}:temp _sv.t
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
	write_versioned_function(f"stats/menu/{mode.key}_tabs", f"""
$data modify storage {ns}:temp dialog.actions set value [{tabs}]
data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Players",color:"yellow"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_PLAYERS_PAGE_BASE}"}}}}
data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Settings",color:"aqua"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 1"}}}}
""")


def write_players_page(ns: str, version: str) -> None:
	""" Write the known players list, 10 per page, for viewing stats (trigger) and for the admin reset (function). """
	base: str = f"{ns}:v{version}/stats/menu"
	actions: dict[str, tuple[str, str]] = {
		"view": (f"/trigger {ns}.player.config set $(trigger)", f"/trigger {ns}.player.config set $(page_trigger)"),
		"reset": (f"/function {ns}:v{version}/stats/admin/reset {{i:$(i)}}", f"/function {ns}:v{version}/stats/admin/players {{page:$(page)}}"),
	}

	write_versioned_function("stats/menu/players_page", f"""
scoreboard players operation #st_page {ns}.data = @s {ns}.player.config
scoreboard players remove #st_page {ns}.data {TRIG_PLAYERS_PAGE_BASE}
function {base}/players_list {{kind:"view",title:"Players"}}
""")
	write_versioned_function("stats/admin/players", f"""
$scoreboard players set #st_page {ns}.data $(page)
function {base}/players_list {{kind:"reset",title:"Reset Player Stats"}}
""")

	## #st_page is the page; a page past the end shows no players and a Previous button.
	write_versioned_function("stats/menu/players_list", f"""
scoreboard players operation #st_i {ns}.data = #st_page {ns}.data
scoreboard players operation #st_i {ns}.data *= #{PAGE_SIZE} {ns}.data
scoreboard players operation #st_end {ns}.data = #st_i {ns}.data
scoreboard players add #st_end {ns}.data {PAGE_SIZE}
execute store result score #st_total {ns}.data run data get storage {ns}:stats known

data modify storage {ns}:temp _sp set value {{}}
$data modify storage {ns}:temp _sp.kind set value "$(kind)"
execute store result storage {ns}:temp _sp.total int 1 run scoreboard players get #st_total {ns}.data
$data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","👥 ",{{text:"$(title)",color:"gold",bold:true}}],body:[],actions:[],columns:2,after_action:"close",exit_action:{{label:{{translate:"gui.done"}}}}}}
function {base}/players_body with storage {ns}:temp _sp
function {base}/players_next

execute store result storage {ns}:temp _sp.page int 1 run scoreboard players remove #st_page {ns}.data 1
execute store result storage {ns}:temp _sp.page_trigger int 1 run scoreboard players add #st_page {ns}.data {TRIG_PLAYERS_PAGE_BASE}
$execute if score #st_page {ns}.data matches {TRIG_PLAYERS_PAGE_BASE}.. run function {base}/players_prev_$(kind) with storage {ns}:temp _sp
execute store result storage {ns}:temp _sp.page int 1 run scoreboard players remove #st_page {ns}.data {TRIG_PLAYERS_PAGE_BASE - 2}
execute store result storage {ns}:temp _sp.page_trigger int 1 run scoreboard players add #st_page {ns}.data {TRIG_PLAYERS_PAGE_BASE}
$execute if score #st_end {ns}.data < #st_total {ns}.data run function {base}/players_more_$(kind) with storage {ns}:temp _sp
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
	write_versioned_function("stats/menu/players_body", f'$data modify storage {ns}:temp dialog.body append value {{type:"minecraft:plain_message",contents:["",{{text:"Known players",color:"gray"}},": ",{{text:"$(total)",color:"white"}}]}}')

	write_versioned_function("stats/menu/players_next", f"""
execute if score #st_i {ns}.data >= #st_end {ns}.data run return 0
execute if score #st_i {ns}.data >= #st_total {ns}.data run return 0

execute store result storage {ns}:temp _sp.i int 1 run scoreboard players get #st_i {ns}.data
scoreboard players operation #st_t {ns}.data = #st_i {ns}.data
scoreboard players operation #st_t {ns}.data *= #{STAT_PAGES} {ns}.data
execute store result storage {ns}:temp _sp.trigger int 1 run scoreboard players add #st_t {ns}.data {TRIG_PLAYER_STATS_BASE}
function {base}/players_uuid with storage {ns}:temp _sp

scoreboard players add #st_i {ns}.data 1
function {base}/players_next
""")
	write_versioned_function("stats/menu/players_uuid", f"""
$data modify storage {ns}:temp _sp.uuid set from storage {ns}:stats known[$(i)]
function {base}/players_name with storage {ns}:temp _sp
""")
	write_versioned_function("stats/menu/players_name", f"""
$data modify storage {ns}:temp _sp.name set from storage {ns}:stats players."$(uuid)".name
$function {base}/players_button_$(kind) with storage {ns}:temp _sp
""")
	for kind, (button, page) in actions.items():
		write_versioned_function(f"stats/menu/players_button_{kind}", f'$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"yellow"}},action:{{type:"run_command",command:"{button}"}}}}')
		write_versioned_function(f"stats/menu/players_prev_{kind}", f'$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Previous page",color:"aqua"}},action:{{type:"run_command",command:"{page}"}}}}')
		write_versioned_function(f"stats/menu/players_more_{kind}", f'$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Next page",color:"aqua"}},action:{{type:"run_command",command:"{page}"}}}}')

