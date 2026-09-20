
#> mgs:v5.1.0/zombies/xp/on_round_end
#
# @within	#mgs:zombies/on_round_end
#

execute store result score #xp_gain mgs.data run data get storage mgs:zombies game.round
scoreboard players operation #xp_gain mgs.data *= #2 mgs.data
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/progression/zb/award_round_survived

