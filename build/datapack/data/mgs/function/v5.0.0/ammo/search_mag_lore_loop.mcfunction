
#> mgs:v5.0.0/ammo/search_mag_lore_loop
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/modify_mag_lore {"slot":"$(slot)"}
#			mgs:v5.0.0/ammo/search_mag_lore_loop {"slot":"$(slot)"}
#
# @args		slot (string)
#

# Check if current lore line matches ammo format (number/number)
scoreboard players set #success mgs.data 0
data modify storage mgs:temp lore_extra set from storage mgs:temp copy[0].extra
data modify storage mgs:temp lore_slash set from storage mgs:temp lore_extra[-2]
execute if data storage mgs:temp lore_slash{"text":"/"} unless data storage mgs:temp lore_extra[-3].text unless data storage mgs:temp lore_extra[-1].text run scoreboard players set #success mgs.data 1

# If ammo line found, prepare data for modification
execute if score #success mgs.data matches 1 run data modify storage mgs:input with set value {}
execute if score #success mgs.data matches 1 store result storage mgs:input with.index int 1 run scoreboard players get #index mgs.data
execute if score #success mgs.data matches 1 store result storage mgs:input with.remaining_bullets int 1 run scoreboard players get #bullets mgs.data
execute if score #success mgs.data matches 1 run data modify storage mgs:input with.capacity set from storage mgs:temp capacity
$execute if score #success mgs.data matches 1 run data modify storage mgs:input with.slot set value "$(slot)"
execute if score #success mgs.data matches 1 summon item_display run return run function mgs:v5.0.0/ammo/found_mag_lore_line with storage mgs:input with

# Continue searching if not found
data remove storage mgs:temp copy[0]
scoreboard players add #index mgs.data 1
$execute if data storage mgs:temp copy[0] run function mgs:v5.0.0/ammo/search_mag_lore_loop {"slot":"$(slot)"}

