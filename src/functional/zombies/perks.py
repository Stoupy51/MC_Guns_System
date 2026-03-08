
# Perk Machine System
# Stationary machines where players buy gameplay-enhancing perks.
# Available perks: juggernog, speed_cola, double_tap, quick_revive
from stewbeet import Mem, write_load_file, write_tag, write_versioned_function

from ..helpers import MGS_TAG


def generate_perks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Perk machine entity scoreboards
	write_load_file(f"""
# Perk machine entity scoreboards
scoreboard objectives add {ns}.zb.perk.id dummy
scoreboard objectives add {ns}.zb.perk.price dummy
scoreboard objectives add {ns}.zb.perk.power dummy
""")

	## Signal function tag for extensibility
	write_tag("zombies/on_new_perk", Mem.ctx.data[ns].function_tags, [])

	## Setup: iterate perk compounds, summon interaction entities
	write_versioned_function("zombies/perks/setup", f"""
scoreboard players set #pk_counter {ns}.data 0
data modify storage {ns}:zombies perk_data set value {{}}
data modify storage {ns}:temp _pk_iter set from storage {ns}:zombies game.map.perks
execute if data storage {ns}:temp _pk_iter[0] run function {ns}:v{version}/zombies/perks/setup_iter
""")

	write_versioned_function("zombies/perks/setup_iter", f"""
# Assign incrementing ID
scoreboard players add #pk_counter {ns}.data 1

# Read relative position and convert to absolute
execute store result score #pkx {ns}.data run data get storage {ns}:temp _pk_iter[0].pos[0]
execute store result score #pky {ns}.data run data get storage {ns}:temp _pk_iter[0].pos[1]
execute store result score #pkz {ns}.data run data get storage {ns}:temp _pk_iter[0].pos[2]
scoreboard players operation #pkx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #pky {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #pkz {ns}.data += #gm_base_z {ns}.data

# Store absolute position for macro
execute store result storage {ns}:temp _pk.x int 1 run scoreboard players get #pkx {ns}.data
execute store result storage {ns}:temp _pk.y int 1 run scoreboard players get #pky {ns}.data
execute store result storage {ns}:temp _pk.z int 1 run scoreboard players get #pkz {ns}.data

# Summon interaction entity
function {ns}:v{version}/zombies/perks/place_at with storage {ns}:temp _pk

# Set scoreboards on entity
scoreboard players operation @n[tag=_pk_new] {ns}.zb.perk.id = #pk_counter {ns}.data
execute store result score @n[tag=_pk_new] {ns}.zb.perk.price run data get storage {ns}:temp _pk_iter[0].price
# Store power requirement as 1/0 (true stored as 1b in NBT, data get returns 1)
execute store result score @n[tag=_pk_new] {ns}.zb.perk.power run data get storage {ns}:temp _pk_iter[0].power

# Store perk_id in indexed storage for later lookup
execute store result storage {ns}:temp _pk_store.id int 1 run scoreboard players get #pk_counter {ns}.data
data modify storage {ns}:temp _pk_store.perk_id set from storage {ns}:temp _pk_iter[0].perk_id
function {ns}:v{version}/zombies/perks/store_data with storage {ns}:temp _pk_store

# Register Bookshelf events
execute as @n[tag=_pk_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/perks/on_right_click",executor:"source"}}
execute as @n[tag=_pk_new] run function #bs.interaction:on_hover_enter {{run:"function {ns}:v{version}/zombies/perks/on_hover_enter",executor:"source"}}
execute as @n[tag=_pk_new] run function #bs.interaction:on_hover_leave {{run:"function {ns}:v{version}/zombies/perks/on_hover_leave",executor:"source"}}
tag @n[tag=_pk_new] remove _pk_new

# Continue iteration
data remove storage {ns}:temp _pk_iter[0]
execute if data storage {ns}:temp _pk_iter[0] run function {ns}:v{version}/zombies/perks/setup_iter
""")

	write_versioned_function("zombies/perks/place_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.0f,height:1.0f,response:true,Tags:["{ns}.perk_machine","{ns}.gm_entity","bs.entity.interaction","_pk_new"]}}
""")

	write_versioned_function("zombies/perks/store_data", f"""
$data modify storage {ns}:zombies perk_data."$(id)" set value {{perk_id:"$(perk_id)"}}
""")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/perks/on_right_click", f"""
# Guard: game must be active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# Check power requirement
execute store result score #pk_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.power
execute if score #pk_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},{{"text":" ⚡ Requires power!","color":"red"}}]

# Look up perk_id
execute store result storage {ns}:temp _pk_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.id
function {ns}:v{version}/zombies/perks/lookup_perk with storage {ns}:temp _pk_buy

# Check if player already has this perk
function {ns}:v{version}/zombies/perks/check_owned with storage {ns}:temp _pk_data
execute if score #pk_owned {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},{{"text":" Already have this perk!","color":"yellow"}}]

# Get price and check points
execute store result score #pk_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.price
execute unless score @s {ns}.zb.points >= #pk_price {ns}.data run return run tellraw @s [{MGS_TAG},{{"text":" Not enough points!","color":"red"}}]

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #pk_price {ns}.data

# Apply perk effect (sets scoreboard + calls specific perk function)
function {ns}:v{version}/zombies/perks/apply with storage {ns}:temp _pk_data

# Signal
function #{ns}:zombies/on_new_perk

# Sound
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.5
""")

	write_versioned_function("zombies/perks/lookup_perk", f"""
$data modify storage {ns}:temp _pk_data set from storage {ns}:zombies perk_data."$(id)"
""")

	write_versioned_function("zombies/perks/check_owned", f"""
scoreboard players set #pk_owned {ns}.data 0
$execute if score @s {ns}.zb.perk.$(perk_id) matches 1 run scoreboard players set #pk_owned {ns}.data 1
""")

	write_versioned_function("zombies/perks/apply", f"""
# Set perk scoreboard for the player
$scoreboard players set @s {ns}.zb.perk.$(perk_id) 1

# Call perk-specific effect function
$function {ns}:v{version}/zombies/perks/apply/$(perk_id)
""")

	## Per-perk effect functions
	write_versioned_function("zombies/perks/apply/juggernog", f"""
# Increase max health to 40 HP
attribute @s minecraft:max_health base set 40
data modify entity @s Health set value 40f
tellraw @s [{MGS_TAG},{{"text":" 🍺 Juggernog! Max HP: 40","color":"dark_red","bold":true}}]
""")

	write_versioned_function("zombies/perks/apply/speed_cola", f"""
tag @s add {ns}.perk.speed_cola
tellraw @s [{MGS_TAG},{{"text":" ⚡ Speed Cola! Faster reload","color":"green","bold":true}}]
""")

	write_versioned_function("zombies/perks/apply/double_tap", f"""
tag @s add {ns}.perk.double_tap
tellraw @s [{MGS_TAG},{{"text":" 🔥 Double Tap! More damage","color":"gold","bold":true}}]
""")

	write_versioned_function("zombies/perks/apply/quick_revive", f"""
tag @s add {ns}.perk.quick_revive
tellraw @s [{MGS_TAG},{{"text":" 💚 Quick Revive! You can revive teammates","color":"aqua","bold":true}}]
""")

	## Hover events (executor: "source" = player)
	write_versioned_function("zombies/perks/on_hover_enter", f"""
execute store result score #pk_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.price
title @s times 0 40 10
title @s title [{{"text":"🥤 Perk Machine","color":"dark_purple"}}]
title @s subtitle [{{"text":"Cost: ","color":"gray"}},{{"score":{{"name":"#pk_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}]
""")

	write_versioned_function("zombies/perks/on_hover_leave", """
title @s clear
""")

	## Hook into game start: reset perk scoreboards
	write_versioned_function("zombies/start", f"""
# Reset perk scoreboards
scoreboard players set @a {ns}.zb.perk.juggernog 0
scoreboard players set @a {ns}.zb.perk.speed_cola 0
scoreboard players set @a {ns}.zb.perk.double_tap 0
scoreboard players set @a {ns}.zb.perk.quick_revive 0
""")

	## Hook into preload_complete: setup perk machines
	write_versioned_function("zombies/preload_complete", f"""
# Setup perk machines
execute if data storage {ns}:zombies game.map.perks[0] run function {ns}:v{version}/zombies/perks/setup
""")

	## Hook into stop: remove perk effects
	write_versioned_function("zombies/stop", f"""
# Reset perk effects
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:max_health base set 20
tag @a remove {ns}.perk.speed_cola
tag @a remove {ns}.perk.double_tap
tag @a remove {ns}.perk.quick_revive
""")
