""" Trap scoreboards, the turret id predicate and summoning each trap's entities. """
# Imports
from stewbeet import (
	JsonDict,
	Mem,
	Predicate,
	set_json_encoder,
	write_load_file,
	write_versioned_function,
)


# Functions
def write_trap_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Matches the trap id of the turret being processed, cheaper in a selector than `execute as @e[...] if score`.
	id_ref: JsonDict = {"type": "minecraft:score", "target": {"type": "minecraft:fixed", "name": "#turret_tid"}, "score": f"{ns}.data"}
	Mem.ctx.data[ns].predicates[f"v{version}/zombies/traps/turret_id_match"] = set_json_encoder(Predicate({
		"type": "minecraft:entity_scores",
		"entity": "this",
		"scores": {f"{ns}.zb.trap.id": {"min": id_ref, "max": id_ref}},
	}), max_level=-1)

	write_load_file(f"""
scoreboard objectives add {ns}.zb.trap.id dummy
scoreboard objectives add {ns}.zb.trap.price dummy
scoreboard objectives add {ns}.zb.trap.power dummy
scoreboard objectives add {ns}.zb.trap.type dummy
scoreboard objectives add {ns}.zb.trap.dur dummy
scoreboard objectives add {ns}.zb.trap.cd_max dummy
# 1 when the activator owns Timeslip (cooldown at 75%).
scoreboard objectives add {ns}.zb.trap.timeslip dummy
scoreboard objectives add {ns}.zb.trap.timer dummy
scoreboard objectives add {ns}.zb.trap.cd dummy
scoreboard objectives add {ns}.zb.trap.rx dummy
scoreboard objectives add {ns}.zb.trap.ry dummy
scoreboard objectives add {ns}.zb.trap.rz dummy
""")

	write_versioned_function("zombies/traps/setup", f"""
scoreboard players set #trap_counter {ns}.data 0
data modify storage {ns}:temp _trap_iter set from storage {ns}:zombies game.map.traps
execute if data storage {ns}:temp _trap_iter[0] run function {ns}:v{version}/zombies/traps/setup_iter
""")

	write_versioned_function("zombies/traps/setup_iter", f"""
scoreboard players add #trap_counter {ns}.data 1

execute store result score #tix {ns}.data run data get storage {ns}:temp _trap_iter[0].pos[0]
execute store result score #tiy {ns}.data run data get storage {ns}:temp _trap_iter[0].pos[1]
execute store result score #tiz {ns}.data run data get storage {ns}:temp _trap_iter[0].pos[2]
scoreboard players operation #tix {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #tiy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #tiz {ns}.data += #gm_base_z {ns}.data

# Effect centre = interaction position + offset_pos.
execute store result score #tx {ns}.data run data get storage {ns}:temp _trap_iter[0].offset_pos[0]
execute store result score #ty {ns}.data run data get storage {ns}:temp _trap_iter[0].offset_pos[1]
execute store result score #tz {ns}.data run data get storage {ns}:temp _trap_iter[0].offset_pos[2]
scoreboard players operation #tx {ns}.data += #tix {ns}.data
scoreboard players operation #ty {ns}.data += #tiy {ns}.data
scoreboard players operation #tz {ns}.data += #tiz {ns}.data

execute store result storage {ns}:temp _trap.cx int 1 run scoreboard players get #tx {ns}.data
execute store result storage {ns}:temp _trap.cy int 1 run scoreboard players get #ty {ns}.data
execute store result storage {ns}:temp _trap.cz int 1 run scoreboard players get #tz {ns}.data
execute store result storage {ns}:temp _trap.ix int 1 run scoreboard players get #tix {ns}.data
execute store result storage {ns}:temp _trap.iy int 1 run scoreboard players get #tiy {ns}.data
execute store result storage {ns}:temp _trap.iz int 1 run scoreboard players get #tiz {ns}.data

function {ns}:v{version}/zombies/traps/place_at with storage {ns}:temp _trap

# type is also stored here for the hover text.
scoreboard players operation @n[tag={ns}._trap_new_i] {ns}.zb.trap.id = #trap_counter {ns}.data
execute store result score @n[tag={ns}._trap_new_i] {ns}.zb.trap.price run data get storage {ns}:temp _trap_iter[0].price
execute store result score @n[tag={ns}._trap_new_i] {ns}.zb.trap.power run data get storage {ns}:temp _trap_iter[0].power
execute store result score @n[tag={ns}._trap_new_i] {ns}.zb.trap.type run data get storage {ns}:temp _trap_iter[0].type
tag @e[tag={ns}._trap_new_i] remove {ns}._trap_new_i

scoreboard players operation @n[tag={ns}._trap_new_m] {ns}.zb.trap.id = #trap_counter {ns}.data
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.type run data get storage {ns}:temp _trap_iter[0].type
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.dur run data get storage {ns}:temp _trap_iter[0].duration
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.cd_max run data get storage {ns}:temp _trap_iter[0].cooldown
scoreboard players set @n[tag={ns}._trap_new_m] {ns}.zb.trap.timer 0
scoreboard players set @n[tag={ns}._trap_new_m] {ns}.zb.trap.cd 0

execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.rx run data get storage {ns}:temp _trap_iter[0].effect_radius[0]
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.ry run data get storage {ns}:temp _trap_iter[0].effect_radius[1]
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.rz run data get storage {ns}:temp _trap_iter[0].effect_radius[2]
tag @e[tag={ns}._trap_new_m] remove {ns}._trap_new_m

execute as @e[tag={ns}._trap_new_bs] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/traps/on_right_click",executor:"source"}}
execute as @e[tag={ns}._trap_new_bs] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/traps/on_hover",executor:"source"}}
tag @e[tag={ns}._trap_new_bs] remove {ns}._trap_new_bs

# Turrets (type 2) get a fixed base and a head that aims; the head carries the trap id for turret_fire.
execute store result score #trap_type {ns}.data run data get storage {ns}:temp _trap_iter[0].type
data modify storage {ns}:temp _trap.yaw set value 0.0f
execute if data storage {ns}:temp _trap_iter[0].rotation[0] run data modify storage {ns}:temp _trap.yaw set from storage {ns}:temp _trap_iter[0].rotation[0]
execute if score #trap_type {ns}.data matches 2 run function {ns}:v{version}/zombies/traps/place_turret_at with storage {ns}:temp _trap
execute if score #trap_type {ns}.data matches 2 run scoreboard players operation @n[tag={ns}._trap_new_head] {ns}.zb.trap.id = #trap_counter {ns}.data
execute if score #trap_type {ns}.data matches 2 run tag @e[tag={ns}._trap_new_head] remove {ns}._trap_new_head

data remove storage {ns}:temp _trap_iter[0]
execute if data storage {ns}:temp _trap_iter[0] run function {ns}:v{version}/zombies/traps/setup_iter
""")

	write_versioned_function("zombies/traps/place_at", f"""
# height -2.0 makes a downward hitbox, raised 2 blocks right after, so it covers the 2-block turret (as the perk machine does).
$execute positioned $(ix) $(iy) $(iz) run summon minecraft:interaction ~ ~2 ~ {{width:1.1f,height:-2.0f,response:true,Tags:["{ns}.trap_interact","{ns}.gm_entity","bs.entity.interaction","{ns}._trap_new_i","{ns}._trap_new_bs"]}}

$summon minecraft:marker $(cx) $(cy) $(cz) {{Tags:["{ns}.trap_center","{ns}.gm_entity","{ns}._trap_new_m"]}}
""")

	## Both models are built around their origin (the head around its pivot), so they are summoned in place; teleport_duration smooths the re-aim.
	## The base sits on the floor at the block centre, the head mount 1.625 up in the base's yoke (1.5 to 1.75).
	write_versioned_function("zombies/traps/place_turret_at", f"""
$execute positioned $(cx) $(cy) $(cz) run summon minecraft:item_display ~ ~.5 ~ {{Rotation:[$(yaw)f,0f],Tags:["{ns}.trap_base","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:iron_block",count:1,components:{{"minecraft:item_model":"{ns}:turret_base"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2f,2f,2f]}}}}
$execute positioned $(cx) $(cy) $(cz) positioned ~ ~1.625 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw)f,0f],Tags:["{ns}.trap_head","{ns}.gm_entity","{ns}._trap_new_head"],item_display:"fixed",billboard:"fixed",teleport_duration:5,item:{{id:"minecraft:netherite_block",count:1,components:{{"minecraft:item_model":"{ns}:turret_head"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}}}
""")

