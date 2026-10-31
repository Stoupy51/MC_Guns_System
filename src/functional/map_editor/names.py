""" Keeping each marker's name, rotation and drawn shapes in step with its data, rebuilt only after an edit. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..map_editor_defs import ALL_ELEMENTS
from ..zombies.game.lifecycle.spawns import ARRIVALS, SPECIAL_SPAWNS, ZOMBIE_SPAWNS

# Constants
SPAWN_NAME: str = "$(group)$(rounds) $(entity)$(arrival_flag)$(power_flag)"
""" How a zombie or special spawn reads in the editor: "Zombie Spawn g2 r5-12 spider ceiling power". """
EDITOR_NAMES: dict[str, str] = {
	"zombie_spawn": f"Zombie Spawn {SPAWN_NAME}",
	"special_spawn": f"Special Spawn {SPAWN_NAME}",
	"player_spawn_zb": "Player Spawn $(group)",
	"door": "Door link $(link_id) $(price)pts$(rounds)",
	"wallbuy": "Wallbuy $(weapon_id)",
	"perk_machine": "Perk Machine $(perk_id)",
	"trap": "Trap type $(type)",
	"mystery_box_pos": "Mystery Box $(location_name)",
}
""" Names built from a marker's configuration; every other element is named after its kind. """
DEFAULT_ARRIVALS: dict[str, str] = {"zombie_spawn": ZOMBIE_SPAWNS.defaults["arrival"], "special_spawn": SPECIAL_SPAWNS.defaults["arrival"]}


# Functions
def write_editor_names() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Run as each marker once a second: the comparison costs a read, the rebuild only runs after an edit.
	write_versioned_function("maps/editor/sync_marker", f"""
data modify storage {ns}:temp _ed_sig set value {{}}
data modify storage {ns}:temp _ed_sig set from entity @s data
data remove storage {ns}:temp _ed_sig._ed
data remove storage {ns}:temp _ed_sig._disp_sig
execute store success score #ed_changed {ns}.data run data modify entity @s data._ed.sig set from storage {ns}:temp _ed_sig
execute if score #ed_changed {ns}.data matches 1 run function {ns}:v{version}/maps/editor/refresh_marker
""")

	dispatch: str = "\n".join(
		f"execute if entity @s[tag={ns}.element.{etype}] run return run function {ns}:v{version}/maps/editor/name/{etype}"
		for etype in ALL_ELEMENTS
	)
	write_versioned_function("maps/editor/refresh_marker", f"""
execute if data entity @s data.yaw run data modify entity @s Rotation[0] set from entity @s data.yaw
execute if entity @s[tag={ns}.element.zombie_spawn] run function {ns}:v{version}/maps/editor/spawn_shapes
execute if entity @s[tag={ns}.element.special_spawn] run function {ns}:v{version}/maps/editor/spawn_shapes

# The data, plus what a name shows that is not plain data.
data modify storage {ns}:temp _ed_name set value {{group:"",rounds:"",entity:"",arrival_flag:"",power_flag:""}}
data modify storage {ns}:temp _ed_name merge from entity @s data
execute if data entity @s data.group_id run function {ns}:v{version}/maps/editor/name/group with entity @s data
execute if data entity @s data.min_round run function {ns}:v{version}/maps/editor/name/rounds
execute if data entity @s data.mob.entity run function {ns}:v{version}/maps/editor/name/entity
execute if data entity @s data{{power:1b}} run data modify storage {ns}:temp _ed_name.power_flag set value " power"
{dispatch}
""")

	write_versioned_function("maps/editor/name/group", f"""
$data modify storage {ns}:temp _ed_name.group set value "g$(group_id)"
""")

	## " r5-12", " r5+" or " r1-12"; nothing for a marker used every round. Doors have no max_round.
	write_versioned_function("maps/editor/name/rounds", f"""
execute store result score #ed_rmin {ns}.data run data get entity @s data.min_round
scoreboard players set #ed_rmax {ns}.data 0
execute if data entity @s data.max_round store result score #ed_rmax {ns}.data run data get entity @s data.max_round
execute if score #ed_rmin {ns}.data matches ..0 if score #ed_rmax {ns}.data matches ..0 run return 0
execute if score #ed_rmin {ns}.data matches ..0 run scoreboard players set #ed_rmin {ns}.data 1
execute store result storage {ns}:temp _ed_rounds.min int 1 run scoreboard players get #ed_rmin {ns}.data
execute store result storage {ns}:temp _ed_rounds.max int 1 run scoreboard players get #ed_rmax {ns}.data
execute if score #ed_rmax {ns}.data matches ..0 run return run function {ns}:v{version}/maps/editor/name/rounds_from with storage {ns}:temp _ed_rounds
function {ns}:v{version}/maps/editor/name/rounds_between with storage {ns}:temp _ed_rounds
""")
	write_versioned_function("maps/editor/name/rounds_from", f"""
$data modify storage {ns}:temp _ed_name.rounds set value " r$(min)+"
""")
	write_versioned_function("maps/editor/name/rounds_between", f"""
$data modify storage {ns}:temp _ed_name.rounds set value " r$(min)-$(max)"
""")

	write_versioned_function("maps/editor/name/entity", f"""
data modify storage {ns}:temp _ed_name.entity set from entity @s data.mob.entity
data modify storage {ns}:temp _ed_name.prefix set value ""
data modify storage {ns}:temp _ed_name.prefix set string storage {ns}:temp _ed_name.entity 0 10
execute if data storage {ns}:temp _ed_name{{prefix:"minecraft:"}} run data modify storage {ns}:temp _ed_name.entity set string storage {ns}:temp _ed_name.entity 10
""")

	write_marker_names(ns, version)
	write_spawn_shapes(ns, version)


def write_marker_names(ns: str, version: str) -> None:
	""" Write maps/editor/name/<etype>, giving a marker of that element its name from the data in {ns}:temp _ed_name. """
	for etype, einfo in ALL_ELEMENTS.items():
		template: str | None = EDITOR_NAMES.get(etype)
		if template is None:
			write_versioned_function(f"maps/editor/name/{etype}", f'data modify entity @s CustomName set value "{einfo.name}"')
			continue
		# A spawn shows its arrival only when it is not its kind's default.
		arrival_flags: str = "\n".join(
			f'execute if data storage {ns}:temp _ed_name{{arrival:"{arrival}"}} run data modify storage {ns}:temp _ed_name.arrival_flag set value " {arrival}"'
			for arrival in ARRIVALS if etype in DEFAULT_ARRIVALS and arrival != DEFAULT_ARRIVALS[etype]
		)
		write_versioned_function(f"maps/editor/name/{etype}", f"""
{arrival_flags}
function {ns}:v{version}/maps/editor/name/{etype}_apply with storage {ns}:temp _ed_name
""")
		write_versioned_function(f"maps/editor/name/{etype}_apply", f'$data modify entity @s CustomName set value "{template}"')


def write_spawn_shapes(ns: str, version: str) -> None:
	""" Write the activation box and walk-to spot a spawn marker keeps in data._ed, and the particles drawing them. """
	## Run as a zombie or special spawn marker: the activation box and the walk-to spot, in world coordinates, for the particles.
	write_versioned_function("maps/editor/spawn_shapes", f"""
tag @s remove {ns}.ed_box
tag @s remove {ns}.ed_walk
execute store result score #ed_x {ns}.data run data get entity @s Pos[0]
execute store result score #ed_y {ns}.data run data get entity @s Pos[1]
execute store result score #ed_z {ns}.data run data get entity @s Pos[2]
execute if data entity @s data.activation_box[5] run function {ns}:v{version}/maps/editor/spawn_box
execute if data entity @s data.walk_to[2] run function {ns}:v{version}/maps/editor/spawn_walk
""")

	# The players a selector [x,y,z,dx,dy,dz] catches are those touching the blocks x to x+dx, so the box ends one block past them.
	axes: tuple[str, ...] = ("x", "y", "z")
	write_versioned_function("maps/editor/spawn_box", "\n".join([
		f"tag @s add {ns}.ed_box",
		*(
			f"execute store result score #ed_{axis}1 {ns}.data run data get entity @s data.activation_box[{index}]\n"
			f"scoreboard players operation #ed_{axis}1 {ns}.data += #ed_{axis} {ns}.data\n"
			f"execute store result score #ed_{axis}2 {ns}.data run data get entity @s data.activation_box[{index + 3}]\n"
			f"scoreboard players operation #ed_{axis}2 {ns}.data += #ed_{axis}1 {ns}.data\n"
			f"scoreboard players add #ed_{axis}2 {ns}.data 1\n"
			f"execute store result entity @s data._ed.box.{axis}1 int 1 run scoreboard players get #ed_{axis}1 {ns}.data\n"
			f"execute store result entity @s data._ed.box.{axis}2 int 1 run scoreboard players get #ed_{axis}2 {ns}.data"
			for index, axis in enumerate(axes)
		),
	]))

	## From the centre of the marker's block to the centre of the block it names, in tenths so negative coordinates centre right.
	write_versioned_function("maps/editor/spawn_walk", "\n".join([
		f"tag @s add {ns}.ed_walk",
		*(
			f"execute store result score #ed_w{axis} {ns}.data run data get entity @s data.walk_to[{index}]\n"
			f"scoreboard players operation #ed_w{axis} {ns}.data += #ed_{axis} {ns}.data\n"
			f"scoreboard players operation #ed_w{axis} {ns}.data *= #10 {ns}.data\n"
			f"execute store result entity @s data._ed.walk.{axis} double 0.1 run scoreboard players add #ed_w{axis} {ns}.data 5\n"
			f"scoreboard players operation #ed_{axis} {ns}.data *= #10 {ns}.data\n"
			f"execute store result entity @s data._ed.walk.from_{axis} double 0.1 run scoreboard players add #ed_{axis} {ns}.data 5"
			for index, axis in enumerate(axes)
		),
	]))

	# Drawn every 4 ticks, each trail living a second: green box edges and a gold path from the spawn to its spot.
	viewers: str = f"@a[scores={{{ns}.mp.map_edit=1}},distance=..48]"
	write_versioned_function("maps/editor/draw_box", "\n".join(
		f"$particle trail{{target:[{end}],color:5635925,duration:20}} {start} 0 0 0 0 1 force {viewers}" for start, end in box_edges()
	))
	write_versioned_function("maps/editor/draw_walk", f"""
$particle trail{{target:[$(x),$(y),$(z)],color:16755200,duration:20}} $(from_x) $(from_y) $(from_z) 0 0 0 0 1 force {viewers}
$particle dust{{color:[1.0,0.67,0.0],scale:1.5}} $(x) $(y) $(z) 0.15 0.15 0.15 0 3 force {viewers}
""")


def box_edges() -> list[tuple[str, str]]:
	""" The 12 edges of a box whose corners are the macro arguments x1 to z2: each start as coordinates, each end as a list's items.

	>>> box_edges()[0]
	('$(x1) $(y1) $(z1)', '$(x2),$(y1),$(z1)')
	"""
	axes: tuple[str, ...] = ("x", "y", "z")
	edges: list[tuple[str, str]] = []
	for axis in axes:
		others: list[str] = [other for other in axes if other != axis]
		for first, second in (("1", "1"), ("1", "2"), ("2", "1"), ("2", "2")):
			corner: dict[str, str] = {axis: "1", others[0]: first, others[1]: second}
			edges.append((" ".join(f"$({a}{corner[a]})" for a in axes), ",".join(f"$({a}{'2' if a == axis else corner[a]})" for a in axes)))
	return edges

