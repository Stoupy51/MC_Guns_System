
#> mgs:v5.0.1/zombies/revive/clear_downed_state
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=spectator]
#
# @within	mgs:v5.0.1/zombies/revive/do_round_respawn
#

scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data at @s run kill @n[tag=mgs.downed_hud,distance=..3]
execute as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run kill @s
execute as @e[tag=mgs.downed_cam] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run kill @s
ride @s dismount
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

