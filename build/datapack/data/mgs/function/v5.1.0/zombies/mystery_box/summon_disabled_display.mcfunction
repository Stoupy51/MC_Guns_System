
#> mgs:v5.1.0/zombies/mystery_box/summon_disabled_display
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/refresh_disabled [ as @e[tag=...] & at @s ]
#

execute if entity @n[tag=mgs.mb_display,distance=..3] run return 0
data modify storage mgs:temp _mb_dis.yaw set value 0.0f
data modify storage mgs:temp _mb_dis.yaw set from entity @s Rotation[0]
execute unless entity @s[tag=mgs.roam_hidden] run function mgs:v5.1.0/zombies/mystery_box/summon_disabled_at with storage mgs:temp _mb_dis
execute if entity @s[tag=mgs.roam_hidden] positioned ~ ~512 ~ run function mgs:v5.1.0/zombies/mystery_box/summon_disabled_at with storage mgs:temp _mb_dis

