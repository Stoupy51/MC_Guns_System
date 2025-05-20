
#> stoupgun:v5.0.0/ammo/search_lore_loop
#
# @within	stoupgun:v5.0.0/ammo/modify_lore {"slot":"$(slot)"}
#			stoupgun:v5.0.0/ammo/search_lore_loop {"slot":"$(slot)"}
#

# Check if lore finishes by format `number/number`, ex: "30", {"text":"/"}, "30"
scoreboard players set #success stoupgun.data 0
data modify storage stoupgun:temp lore_extra set from storage stoupgun:temp copy[0].extra
data modify storage stoupgun:temp lore_slash set from storage stoupgun:temp lore_extra[-2]
execute if data storage stoupgun:temp lore_slash{"text":"/"} unless data storage stoupgun:temp lore_extra[-3].text unless data storage stoupgun:temp lore_extra[-1].text run scoreboard players set #success stoupgun.data 1

# If it is, prepare arguments and modify the line
execute if score #success stoupgun.data matches 1 run data modify storage stoupgun:input with set value {}
execute if score #success stoupgun.data matches 1 store result storage stoupgun:input with.index int 1 run scoreboard players get #index stoupgun.data
execute if score #success stoupgun.data matches 1 store result storage stoupgun:input with.remaining_bullets int 1 run scoreboard players get @s stoupgun.remaining_bullets
execute if score #success stoupgun.data matches 1 run data modify storage stoupgun:input with.capacity set from storage stoupgun:temp components."minecraft:custom_data".stoupgun.stats.capacity
$execute if score #success stoupgun.data matches 1 run data modify storage stoupgun:input with.slot set value "$(slot)"
execute if score #success stoupgun.data matches 1 summon item_display run return run function stoupgun:v5.0.0/ammo/found_line with storage stoupgun:input with

# Continue loop if not
data remove storage stoupgun:temp copy[0]
scoreboard players add #index stoupgun.data 1
$execute if data storage stoupgun:temp copy[0] run function stoupgun:v5.0.0/ammo/search_lore_loop {"slot":"$(slot)"}

