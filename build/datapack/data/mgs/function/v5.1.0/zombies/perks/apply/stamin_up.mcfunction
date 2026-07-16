
#> mgs:v5.1.0/zombies/perks/apply/stamin_up
#
# @within	???
#

attribute @s minecraft:movement_speed modifier add mgs:stamin_up 0.07 add_multiplied_total
scoreboard players set @s mgs.stam_bonus 200
scoreboard players add @s mgs.stam 200
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🏃 ",{"translate":"mgs.stamin_up_sprint_longer_move_faster","color":"yellow"}]

