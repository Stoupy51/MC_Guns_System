
#> mgs:v5.2.0/zombies/rejoin
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/zombies/on_rejoin
#

execute if score #zb_freeze mgs.data matches 1.. run function mgs:v5.2.0/zombies/freeze_player
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s"},[{"text":" ","color":"green"}, {"translate":"mgs.is_back_in_the_game"}]]

# A body is removed while its owner is away (revive/orphan_check). A downed player then comes back as at a round end, a doppelganger without a body forfeits it.
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute if entity @s[tag=mgs.downed_spectator] unless entity @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.2.0/zombies/revive/downed_id_match] run function mgs:v5.2.0/zombies/revive/do_round_respawn
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.ww.id
execute if entity @s[tag=mgs.ww_active] unless entity @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.2.0/zombies/revive/downed_id_match] run function mgs:v5.2.0/zombies/whos_who/forfeit

