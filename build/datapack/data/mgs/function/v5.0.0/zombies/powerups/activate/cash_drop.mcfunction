
#> mgs:v5.0.0/zombies/powerups/activate/cash_drop
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/dispatch_activate
#

# Roll 4..16 * 100 = 400..1600 points
execute store result score #pu_cash mgs.data run random value 4..16
scoreboard players operation #pu_cash mgs.data *= #100 mgs.data

# Double the reward if double_points is active for the collecting player
execute if score @p[tag=mgs.pu_collecting] mgs.special.double_points matches 1.. run scoreboard players operation #pu_cash mgs.data *= #2 mgs.data

# Award to all alive in-game players
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run scoreboard players operation @s mgs.zb.points += #pu_cash mgs.data

# Announce with amount
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.cash_drop","color":"green","bold":true},{"text":"+","color":"gold"},{"score":{"name":"#pu_cash","objective":"mgs.data"},"color":"gold","bold":true},[{"text":" ","color":"gold"}, {"translate":"mgs.points_each"}]]
playsound minecraft:entity.player.levelup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

