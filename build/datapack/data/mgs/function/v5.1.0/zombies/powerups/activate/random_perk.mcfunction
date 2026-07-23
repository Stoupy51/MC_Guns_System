
#> mgs:v5.1.0/zombies/powerups/activate/random_perk
#
# @within	mgs:v5.1.0/zombies/admin/powerup_random_perk
#			mgs:v5.1.0/zombies/powerups/dispatch_activate
#

# Pick a random unowned perk from the map's placed perks for the collecting player
tag @p[tag=mgs.pu_collecting] add mgs.pool_target
scoreboard players set #pool_all_perks mgs.data 0
function mgs:v5.1.0/zombies/perks/pool/choose
tag @a[tag=mgs.pool_target] remove mgs.pool_target

# Nothing available: the collector already owns every perk placed on this map
execute if score #pool_chosen mgs.data matches ..-1 run return run tellraw @p[tag=mgs.pu_collecting] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_already_own_every_perk_on_the_map","color":"yellow"}]

# Grant the chosen perk to the collector
execute as @p[tag=mgs.pu_collecting] run function mgs:v5.1.0/zombies/perks/apply with storage mgs:temp _pool

# Announce + sound
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.random_perk_dropped_for","color":"light_purple"},{"selector":"@p[tag=mgs.pu_collecting]","color":"light_purple","bold":true},{"text":"!","color":"light_purple"}]
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/random_perk ambient @s ~ ~ ~ 0.7 1.0

