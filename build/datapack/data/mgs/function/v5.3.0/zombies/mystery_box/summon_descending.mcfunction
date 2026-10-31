
#> mgs:v5.3.0/zombies/mystery_box/summon_descending
#
# @executed	as @n[tag=mgs.mystery_box_active] & at @s & positioned ~ ~-0.9 ~
#
# @within	mgs:v5.3.0/zombies/mystery_box/move_anim_transition [ as @n[tag=mgs.mystery_box_active] & at @s & positioned ~ ~-0.9 ~ ]
#

execute if score @s mgs.mb.roll matches 0 run execute positioned ^ ^8.44 ^ run function mgs:v5.3.0/zombies/mystery_box/summon_presence {extra_tags:""}
execute if score @s mgs.mb.roll matches 1 run execute positioned ^-8.44 ^ ^ run function mgs:v5.3.0/zombies/mystery_box/summon_presence {extra_tags:""}
execute if score @s mgs.mb.roll matches 2 run execute positioned ^ ^-8.44 ^ run function mgs:v5.3.0/zombies/mystery_box/summon_presence {extra_tags:""}
execute if score @s mgs.mb.roll matches 3 run execute positioned ^8.44 ^ ^ run function mgs:v5.3.0/zombies/mystery_box/summon_presence {extra_tags:""}

