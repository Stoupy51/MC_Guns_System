""" Machine state, summoning each cabinet and lighting up the active one. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function


# Functions
def write_wunderfizz_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## State objectives
	write_load_file(f"""
# Der Wunderfizz machine + spin state
scoreboard objectives add {ns}.zb.wf.id dummy
scoreboard objectives add {ns}.zb.wf.price dummy
scoreboard objectives add {ns}.zb.wf.power dummy
scoreboard objectives add {ns}.zb.wf.allperks dummy
# Spin display (orb): countdown timer (>0 spinning, <=0 ready window), buyer pid, chosen perk index
scoreboard objectives add {ns}.zb.wf.anim dummy
scoreboard objectives add {ns}.zb.wf.buyer dummy
scoreboard objectives add {ns}.zb.wf.perk dummy
# 1 when the buyer owns Timeslip (this orb spins 2x faster, like the Mystery Box)
scoreboard objectives add {ns}.zb.wf.timeslip dummy
# 1 when this pull will roam the machine (teddy bear) instead of granting a perk
scoreboard objectives add {ns}.zb.wf.willmove dummy
# Points paid for this pull, so a roam (bear) can refund the buyer
scoreboard objectives add {ns}.zb.wf.paid dummy
# Stable per-player buyer id (lazy)
scoreboard objectives add {ns}.zb.wf_pid dummy
""")

	## Setup: iterate wunderfizz compounds, summon interaction + a persistent machine display each, then pick ONE active spot (prefer can_start_on markers), light it up and park the rest.
	write_versioned_function("zombies/wunderfizz/setup", f"""
scoreboard players set #wf_counter {ns}.data 0
data modify storage {ns}:temp _wf_iter set from storage {ns}:zombies game.map.wunderfizz
execute if data storage {ns}:temp _wf_iter[0] run function {ns}:v{version}/zombies/wunderfizz/setup_iter

# Pick the active spot: a random can_start_on marker, else any marker
execute as @n[tag={ns}.wunderfizz_machine,tag={ns}.wf_can_start,sort=random] run tag @s add {ns}.wf_active
execute unless entity @e[tag={ns}.wf_active] as @n[tag={ns}.wunderfizz_machine,sort=random] run tag @s add {ns}.wf_active

scoreboard players set #wf_uses {ns}.data 0
scoreboard players set #wf_move_timer {ns}.data 0

# Live model on the active cabinet, grayed disabled model on the rest, and park inactive interactions
function {ns}:v{version}/zombies/wunderfizz/sync_displays
function {ns}:v{version}/zombies/wunderfizz/sync_visibility
""")

	write_versioned_function("zombies/wunderfizz/setup_iter", f"""
scoreboard players add #wf_counter {ns}.data 1

# Relative -> absolute position
execute store result score #wfx {ns}.data run data get storage {ns}:temp _wf_iter[0].pos[0]
execute store result score #wfy {ns}.data run data get storage {ns}:temp _wf_iter[0].pos[1]
execute store result score #wfz {ns}.data run data get storage {ns}:temp _wf_iter[0].pos[2]
scoreboard players operation #wfx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #wfy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #wfz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _wf.x int 1 run scoreboard players get #wfx {ns}.data
execute store result storage {ns}:temp _wf.y int 1 run scoreboard players get #wfy {ns}.data
execute store result storage {ns}:temp _wf.z int 1 run scoreboard players get #wfz {ns}.data
data modify storage {ns}:temp _wf.rotation set from storage {ns}:temp _wf_iter[0].rotation

# Summon interaction entity
function {ns}:v{version}/zombies/wunderfizz/place_at with storage {ns}:temp _wf

# Metadata on the interaction entity
scoreboard players operation @n[tag={ns}.wf_new] {ns}.zb.wf.id = #wf_counter {ns}.data
execute store result score @n[tag={ns}.wf_new] {ns}.zb.wf.price run data get storage {ns}:temp _wf_iter[0].price
execute store result score @n[tag={ns}.wf_new] {ns}.zb.wf.power run data get storage {ns}:temp _wf_iter[0].power
execute store result score @n[tag={ns}.wf_new] {ns}.zb.wf.allperks run data get storage {ns}:temp _wf_iter[0].all_perks

# Roam start-eligibility (default eligible when the field is absent, like the Mystery Box)
execute unless data storage {ns}:temp _wf_iter[0].can_start_on run tag @n[tag={ns}.wf_new] add {ns}.wf_can_start
data modify storage {ns}:temp _wf_cso set value 0b
execute if data storage {ns}:temp _wf_iter[0].can_start_on run data modify storage {ns}:temp _wf_cso set from storage {ns}:temp _wf_iter[0].can_start_on
execute if data storage {ns}:temp {{_wf_cso:1b}} run tag @n[tag={ns}.wf_new] add {ns}.wf_can_start

# Bookshelf events
execute as @n[tag={ns}.wf_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/wunderfizz/on_right_click",executor:"source"}}
execute as @n[tag={ns}.wf_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/wunderfizz/on_hover",executor:"source"}}

# Machine display (perk-machine pipeline, custom Wunderfizz model unless the map overrode it).
# Summoned as the DEFAULT (disabled) model; sync_displays lights up the active one afterwards.
data modify storage {ns}:temp _wf_disp.tag set value "{ns}.wf_display"
data modify storage {ns}:temp _wf_disp.item_id set value ""
data modify storage {ns}:temp _wf_disp.item_model set value ""
data modify storage {ns}:temp _wf_disp.yaw set value 0.0
execute if data storage {ns}:temp _wf_iter[0].display_item run data modify storage {ns}:temp _wf_disp.item_id set from storage {ns}:temp _wf_iter[0].display_item
execute if data storage {ns}:temp _wf_iter[0].item_model run data modify storage {ns}:temp _wf_disp.item_model set from storage {ns}:temp _wf_iter[0].item_model
execute if data storage {ns}:temp _wf_disp{{item_id:""}} run data modify storage {ns}:temp _wf_disp.item_id set value "minecraft:potion"
execute if data storage {ns}:temp _wf_disp{{item_model:""}} run data modify storage {ns}:temp _wf_disp.item_model set value "{ns}:der_wunderfizz"
execute if data storage {ns}:temp _wf_iter[0].rotation[0] run data modify storage {ns}:temp _wf_disp.yaw set from storage {ns}:temp _wf_iter[0].rotation[0]
execute as @n[tag={ns}.wf_new] at @s align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _wf_disp

# Link the freshly summoned display to this position id (there is exactly one unlinked display now)
scoreboard players operation @e[tag={ns}.wf_display,tag=!{ns}.wf_linked] {ns}.zb.wf.id = @n[tag={ns}.wf_new] {ns}.zb.wf.id
tag @e[tag={ns}.wf_display,tag=!{ns}.wf_linked] add {ns}.wf_linked

execute as @n[tag={ns}.wf_new] at @s run tp @s ~ ~2 ~
tag @n[tag={ns}.wf_new] add {ns}.wunderfizz_machine
tag @n[tag={ns}.wf_new] remove {ns}.wf_new

data remove storage {ns}:temp _wf_iter[0]
execute if data storage {ns}:temp _wf_iter[0] run function {ns}:v{version}/zombies/wunderfizz/setup_iter
""")

	write_versioned_function("zombies/wunderfizz/place_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.2f,height:-2.0f,response:true,Rotation:$(rotation),Tags:["{ns}.wunderfizz_machine","{ns}.gm_entity","bs.entity.interaction","{ns}.wf_new"]}}
""")

	## Light up the active cabinet (live model), gray out every other (disabled model).
	## Displays are persistent and id-linked to their spot, so roaming is just a model swap.
	write_versioned_function("zombies/wunderfizz/sync_displays", f"""
execute as @e[tag={ns}.wf_display] run function {ns}:v{version}/zombies/wunderfizz/set_display_disabled
scoreboard players set #wf_active_id {ns}.data -1
execute as @n[tag={ns}.wf_active] run scoreboard players operation #wf_active_id {ns}.data = @s {ns}.zb.wf.id
execute as @e[tag={ns}.wf_display] if score @s {ns}.zb.wf.id = #wf_active_id {ns}.data run function {ns}:v{version}/zombies/wunderfizz/set_display_live
""")

	write_versioned_function("zombies/wunderfizz/set_display_live", f"""
data modify entity @s item.components."minecraft:item_model" set value "{ns}:der_wunderfizz"
""")
	write_versioned_function("zombies/wunderfizz/set_display_disabled", f"""
data modify entity @s item.components."minecraft:item_model" set value "{ns}:der_wunderfizz_disabled"
""")

	## Keep only the active machine's interaction entity reachable; park the rest ±512 out of reach (shared roaming primitive) so an inactive cabinet can't be hovered/clicked.
	write_versioned_function("zombies/wunderfizz/sync_visibility", f"""
execute as @e[tag={ns}.wunderfizz_machine] at @s run function {ns}:v{version}/zombies/wunderfizz/sync_visibility_one
""")
	write_versioned_function("zombies/wunderfizz/sync_visibility_one", f"""
execute if entity @s[tag={ns}.wf_active] if entity @s[tag={ns}.roam_hidden] run function {ns}:v{version}/zombies/roaming/interaction_show
execute unless entity @s[tag={ns}.wf_active] unless entity @s[tag={ns}.roam_hidden] run function {ns}:v{version}/zombies/roaming/interaction_hide
""")

