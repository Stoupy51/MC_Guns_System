
#> mgs:v5.2.0/zombies/revive/orphan_check
#
# @executed	as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin]
#
# @within	mgs:v5.2.0/zombies/revive/tick [ as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin] ]
#

scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
scoreboard players set #rv_owner_here mgs.data 0
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run scoreboard players set #rv_owner_here mgs.data 1
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.zb.ww.id = #my_downed_id mgs.data run scoreboard players set #rv_owner_here mgs.data 1
execute if score #rv_owner_here mgs.data matches 1 run return 0

execute as @e[tag=mgs.downed_hud,predicate=mgs:v5.2.0/zombies/revive/downed_id_match] run kill @s
execute as @e[tag=mgs.downed_cam,predicate=mgs:v5.2.0/zombies/revive/downed_id_match] run kill @s
kill @s

