
#> mgs:v5.4.1/zombies/jockey/link
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/death_watch_tick [ as @e[type=minecraft:marker,tag=mgs.death_watch] ]
#

tag @s add mgs.zb_jockey_linked

# The last hit stamp of either part pays the kill's power-up roll.
scoreboard players set #zb_jk_hit mgs.data 0
scoreboard players operation #zb_jk_hit mgs.data = @s mgs.zb.player_hit
execute if entity @s[tag=mgs.zb_jockey_rider] on vehicle run function mgs:v5.4.1/zombies/jockey/kill_mate
execute unless entity @s[tag=mgs.zb_jockey_rider] on passengers if entity @s[tag=mgs.zb_jockey_rider] run function mgs:v5.4.1/zombies/jockey/kill_mate

