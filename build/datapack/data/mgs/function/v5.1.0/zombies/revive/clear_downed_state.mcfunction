
#> mgs:v5.1.0/zombies/revive/clear_downed_state
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=spectator]
#
# @within	mgs:v5.1.0/zombies/revive/do_round_respawn
#

scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute as @e[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run kill @s
execute as @e[tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run kill @s
execute as @e[tag=mgs.downed_cam,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run kill @s
ride @s dismount
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

