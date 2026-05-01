
#> mgs:v5.0.0/zombies/powerups/activate/random_perk
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/dispatch_activate
#

# Count unowned perks (bail early if all owned — prevents unnecessary iteration)
scoreboard players set #pu_perk_avail mgs.data 0
execute if score @p[tag=mgs.pu_collecting] mgs.zb.perk.juggernog matches 0 run scoreboard players add #pu_perk_avail mgs.data 1
execute if score @p[tag=mgs.pu_collecting] mgs.zb.perk.speed_cola matches 0 run scoreboard players add #pu_perk_avail mgs.data 1
execute if score @p[tag=mgs.pu_collecting] mgs.zb.perk.double_tap matches 0 run scoreboard players add #pu_perk_avail mgs.data 1
execute if score @p[tag=mgs.pu_collecting] mgs.zb.perk.quick_revive matches 0 run scoreboard players add #pu_perk_avail mgs.data 1
execute if score @p[tag=mgs.pu_collecting] mgs.zb.perk.mule_kick matches 0 run scoreboard players add #pu_perk_avail mgs.data 1
execute if score #pu_perk_avail mgs.data matches 0 run return run tellraw @p[tag=mgs.pu_collecting] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_already_own_every_perk","color":"yellow"}]

# Pick a random starting index and walk through the list to find an unowned perk
execute store result score #pu_perk_roll mgs.data run random value 0..4
scoreboard players set #pu_perk_applied mgs.data 0
scoreboard players set #pu_perk_tries mgs.data 0
function mgs:v5.0.0/zombies/powerups/random_perk_iter

# Announce if a perk was successfully granted
execute if score #pu_perk_applied mgs.data matches 1 run tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.random_perk_dropped_for","color":"light_purple"},{"selector":"@p[tag=mgs.pu_collecting]","color":"light_purple","bold":true},{"text":"!","color":"light_purple"}]
execute if score #pu_perk_applied mgs.data matches 1 run playsound minecraft:entity.player.levelup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

