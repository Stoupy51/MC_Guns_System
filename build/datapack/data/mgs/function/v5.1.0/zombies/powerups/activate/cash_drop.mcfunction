
#> mgs:v5.1.0/zombies/powerups/activate/cash_drop
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/dispatch_activate
#

# Roll 4..16 * 100 = 400..1600 points
execute store result score #pu_cash mgs.data run random value 4..16
scoreboard players operation #pu_cash mgs.data *= #100 mgs.data

# Double the reward if double_points is active for the collecting player
execute if score @p[tag=mgs.pu_collecting] mgs.special.double_points matches 1.. run scoreboard players operation #pu_cash mgs.data *= #2 mgs.data

# Award to all in-game players
execute as @a[scores={mgs.zb.in_game=1}] run scoreboard players operation @s mgs.zb.points += #pu_cash mgs.data

# Announce with amount
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.cash_drop_2","color":"green","bold":true},{"text":"+","color":"gold"},{"score":{"name":"#pu_cash","objective":"mgs.data"},"color":"gold","bold":true},[{"text":" ","color":"gold"}, {"translate":"mgs.points_each"}]]
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/bonus_points ambient @s ~ ~ ~ 0.7 1.0

