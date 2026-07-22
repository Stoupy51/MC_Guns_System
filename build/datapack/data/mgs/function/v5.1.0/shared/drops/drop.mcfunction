
#> mgs:v5.1.0/shared/drops/drop
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/drop_held_weapon
#			mgs:v5.1.0/missions/drop_enemy_weapon
#

# Only guns drop: knives, grenades and whatever else a capture step may have grabbed are ignored
execute unless data storage mgs:temp _dropw.components."minecraft:custom_data".mgs.gun run return 0
execute if data storage mgs:temp _dropw.components."minecraft:custom_data".mgs.stats.grenade_type run return 0

# Bake the ammo count into the dropped item (a held gun's own custom data only refreshes a few
# seconds after shooting stops); an empty gun drops with 50% of its magazine capacity instead
execute store result score #drop_half mgs.data run data get storage mgs:temp _dropw.components."minecraft:custom_data".mgs.stats.capacity
scoreboard players operation #drop_half mgs.data /= #2 mgs.data
execute if score #drop_ammo mgs.data matches ..0 run scoreboard players operation #drop_ammo mgs.data = #drop_half mgs.data
execute store result storage mgs:temp _dropw.components."minecraft:custom_data".mgs.stats.remaining_bullets int 1 run scoreboard players get #drop_ammo mgs.data

# Death drops carry one spare magazine at 50% capacity, embedded in the gun's custom data
# (swap drops never run this, so a swapped-away gun is not halved and carries no free magazine)
data modify storage mgs:temp _dropmag_args set value {}
data modify storage mgs:temp _dropmag_args.bw set from storage mgs:temp _dropw.components."minecraft:custom_data".mgs.stats.base_weapon
data remove storage mgs:temp _dropmag
function mgs:v5.1.0/shared/drops/mag_lookup
execute if data storage mgs:temp _dropmag_args.mag run function mgs:v5.1.0/shared/drops/capture_mag with storage mgs:temp _dropmag_args
execute if data storage mgs:temp _dropmag run data modify storage mgs:temp _dropw.components."minecraft:custom_data".mgs.drop_mag set from storage mgs:temp _dropmag

# Mid-air deaths: Bookshelf raycast straight down, the drop spawns on the first block surface below
data modify storage mgs:input with set value {}
data modify storage mgs:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage mgs:input with.piercing set value 0
data modify storage mgs:input with.max_distance set value 100
data modify storage mgs:input with.ignored_blocks set value "#mgs:v5.1.0/empty"
data modify storage mgs:input with.on_entry_point set value "function mgs:v5.1.0/shared/drops/spawn"
scoreboard players set #drop_spawned mgs.data 0
execute rotated ~ 90 run function #bs.raycast:run with storage mgs:input

# Nothing below within range (died over the void) -> drop at the death position
execute if score #drop_spawned mgs.data matches 0 run function mgs:v5.1.0/shared/drops/spawn

