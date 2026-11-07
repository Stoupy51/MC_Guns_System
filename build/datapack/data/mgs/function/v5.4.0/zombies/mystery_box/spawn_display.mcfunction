
#> mgs:v5.4.0/zombies/mystery_box/spawn_display
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/mystery_box/try_use
#

summon minecraft:item_display ~ ~-0.9 ~ {Tags:["mgs.mb_display","mgs.zombies_entity","mgs.mb_display_new"],item_display:"fixed",item:{id:"minecraft:nether_star",count:1,components:{"minecraft:item_model":"air"}},billboard:"fixed"}
tp @n[tag=mgs.mb_display_new] ~ ~-0.9 ~ ~ ~
scoreboard players operation @n[tag=mgs.mb_display_new] mgs.mb.roll = @n[tag=bs.interaction.target] mgs.mb.roll
execute as @n[tag=mgs.mb_display_new] run function mgs:v5.4.0/zombies/mystery_box/display_rest

