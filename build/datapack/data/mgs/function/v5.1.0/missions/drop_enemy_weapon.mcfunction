
#> mgs:v5.1.0/missions/drop_enemy_weapon
#
# @executed	at @s
#
# @within	mgs:v5.1.0/raycast/apply_damage [ at @s ]
#			mgs:v5.1.0/projectile/damage_entity [ at @s ]
#			mgs:v5.1.0/missions/check_enemy_dead
#

tag @s add mgs.drop_done

data remove storage mgs:temp _dropw
data modify storage mgs:temp _dropw set from entity @s equipment.mainhand

# Mob guns never track live ammo on a scoreboard: 0 makes the drop carry half a magazine,
# the same deal a player's empty gun leaves behind
scoreboard players set #drop_ammo mgs.data 0
function mgs:v5.1.0/shared/drops/drop

