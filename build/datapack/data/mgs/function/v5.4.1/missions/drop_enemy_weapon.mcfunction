
#> mgs:v5.4.1/missions/drop_enemy_weapon
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/raycast/apply_damage [ at @s ]
#			mgs:v5.4.1/projectile/damage_entity [ at @s ]
#			mgs:v5.4.1/missions/check_enemy_dead
#

tag @s add mgs.drop_done

data remove storage mgs:temp _dropw
data modify storage mgs:temp _dropw set from entity @s equipment.mainhand

# Mob guns track no live ammo: 0 makes the drop carry half a magazine, like a player's empty gun.
scoreboard players set #drop_ammo mgs.data 0
function mgs:v5.4.1/shared/drops/drop

