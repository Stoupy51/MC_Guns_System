
#> mgs:v5.1.0/zombies/barricades/on_remover_valid
#
# @executed	positioned ^ ^ ^-1
#
# @within	mgs:v5.1.0/zombies/barricades/handle_removing
#

# @s = removing zombie, at zombie position (via at @s in handle_removing selector)
scoreboard players set #barricade_remover_valid mgs.data 1
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.3 0.3 0.02 1

# Pounding on the boards. This runs EVERY tick of the 40-tick teardown, so it needs a budget or it is a
# machine gun of wood hits. Budgeted per player rather than per barricade: several players can stand at
# the same window, and each should hear it at a sane rate. `as` does not move the execution position, so
# ~ ~ ~ below is still the zombie.
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] unless score @s mgs.zb.barricade.bang_at > #total_tick mgs.data run function mgs:v5.1.0/zombies/barricades/bang_for

