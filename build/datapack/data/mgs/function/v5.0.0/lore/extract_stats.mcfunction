
#> mgs:v5.0.0/lore/extract_stats
#
# @within	mgs:v5.0.0/utils/update_all_lore {"slot":"$(slot)"}
#
# @args		slot (string)
#

# Copy item from player to item_display
$item replace entity @s contents from entity @p[tag=mgs.update_lore] $(slot)

# Check if item is a gun
execute store result score #is_gun mgs.data if data entity @s item.components."minecraft:custom_data".mgs.gun
execute store result score #is_grenade mgs.data if data entity @s item.components."minecraft:custom_data".mgs.stats.grenade_type

# Read numeric stats into scores
execute store result score #lore_damage mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.damage
execute store result score #lore_capacity mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity
execute store result score #lore_remaining mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.remaining_bullets
execute store result score #lore_reload mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.reload_time
execute store result score #lore_cooldown mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.cooldown
execute store result score #lore_pellets mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.pellet_count
execute store result score #lore_decay mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.decay 10000
execute store result score #lore_switch mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.switch
execute store result score #has_pellets mgs.data if data entity @s item.components."minecraft:custom_data".mgs.stats.pellet_count

# If remaining_bullets is -1 (weapon-switch marker), use player's scoreboard value instead
execute if score #lore_remaining mgs.data matches -1 store result score #lore_remaining mgs.data run scoreboard players get @p[tag=mgs.update_lore] mgs.remaining_bullets

# Read grenade-specific stats
execute store result score #lore_expl_damage mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.expl_damage
execute store result score #lore_expl_radius mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.expl_radius
execute store result score #lore_grenade_fuse mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.grenade_fuse
execute store result score #has_expl_damage mgs.data if data entity @s item.components."minecraft:custom_data".mgs.stats.expl_damage
execute store result score #has_expl_radius mgs.data if data entity @s item.components."minecraft:custom_data".mgs.stats.expl_radius

# Read grenade type string into temp storage
data modify storage mgs:temp grenade_type set from entity @s item.components."minecraft:custom_data".mgs.stats.grenade_type

# Save footer (last lore line, usually branding/attribution)
data modify storage mgs:temp lore_footer set from entity @s item.components."minecraft:lore"[-1]

# Clean up item_display
kill @s

