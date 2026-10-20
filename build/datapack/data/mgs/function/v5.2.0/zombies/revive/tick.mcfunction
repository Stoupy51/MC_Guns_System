
#> mgs:v5.2.0/zombies/revive/tick
#
# @within	mgs:v5.2.0/zombies/game_tick
#

execute as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}] at @s run function mgs:v5.2.0/zombies/revive/downed_tick

# Every second, bodies whose owner is gone.
scoreboard players operation #rv_sweep_mod mgs.data = #total_tick mgs.data
scoreboard players operation #rv_sweep_mod mgs.data %= #20 mgs.data
execute if score #rv_sweep_mod mgs.data matches 0 as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin] run function mgs:v5.2.0/zombies/revive/orphan_check

