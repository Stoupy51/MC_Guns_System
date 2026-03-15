
#> mgs:v5.0.0/zombies/perks/setup_iter
#
# @within	mgs:v5.0.0/zombies/perks/setup
#			mgs:v5.0.0/zombies/perks/setup_iter
#

# Assign incrementing ID
scoreboard players add #pk_counter mgs.data 1

# Read relative position and convert to absolute
execute store result score #pkx mgs.data run data get storage mgs:temp _pk_iter[0].pos[0]
execute store result score #pky mgs.data run data get storage mgs:temp _pk_iter[0].pos[1]
execute store result score #pkz mgs.data run data get storage mgs:temp _pk_iter[0].pos[2]
scoreboard players operation #pkx mgs.data += #gm_base_x mgs.data
scoreboard players operation #pky mgs.data += #gm_base_y mgs.data
scoreboard players operation #pkz mgs.data += #gm_base_z mgs.data

# Store absolute position for macro
execute store result storage mgs:temp _pk.x int 1 run scoreboard players get #pkx mgs.data
execute store result storage mgs:temp _pk.y int 1 run scoreboard players get #pky mgs.data
execute store result storage mgs:temp _pk.z int 1 run scoreboard players get #pkz mgs.data

# Summon interaction entity
function mgs:v5.0.0/zombies/perks/place_at with storage mgs:temp _pk

# Set scoreboards on entity
scoreboard players operation @n[tag=mgs.pk_new] mgs.zb.perk.id = #pk_counter mgs.data
execute store result score @n[tag=mgs.pk_new] mgs.zb.perk.price run data get storage mgs:temp _pk_iter[0].price
# Store power requirement as 1/0 (true stored as 1b in NBT, data get returns 1)
execute store result score @n[tag=mgs.pk_new] mgs.zb.perk.power run data get storage mgs:temp _pk_iter[0].power

# Store perk_id in indexed storage for later lookup
execute store result storage mgs:temp _pk_store.id int 1 run scoreboard players get #pk_counter mgs.data
data modify storage mgs:temp _pk_store.perk_id set from storage mgs:temp _pk_iter[0].perk_id
data modify storage mgs:temp _pk_store.name set from storage mgs:temp _pk_iter[0].perk_id
execute if data storage mgs:temp _pk_iter[0].name run data modify storage mgs:temp _pk_store.name set from storage mgs:temp _pk_iter[0].name
function mgs:v5.0.0/zombies/perks/store_data with storage mgs:temp _pk_store

# Register Bookshelf events
execute as @n[tag=mgs.pk_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.0/zombies/perks/on_right_click",executor:"source"}
execute as @n[tag=mgs.pk_new] run function #bs.interaction:on_hover {run:"function mgs:v5.0.0/zombies/perks/on_hover",executor:"source"}
tag @n[tag=mgs.pk_new] remove mgs.pk_new

# Continue iteration
data remove storage mgs:temp _pk_iter[0]
execute if data storage mgs:temp _pk_iter[0] run function mgs:v5.0.0/zombies/perks/setup_iter

