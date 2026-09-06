
#> mgs:v5.1.0/zombies/adv/on_round_end
#
# @within	#mgs:zombies/on_round_end
#

execute store result score #adv_round mgs.data run data get storage mgs:zombies game.round
execute as @a[scores={mgs.zb.in_game=1}] run scoreboard players operation @s mgs.adv.zb.best_round > #adv_round mgs.data

# Solo run: exactly one player on the roster, deep enough to be worth saying so
execute store result score #adv_roster mgs.data if entity @a[scores={mgs.zb.in_game=1}]
execute if score #adv_roster mgs.data matches 1 if score #adv_round mgs.data matches 20.. as @a[scores={mgs.zb.in_game=1}] run advancement grant @s only mgs:challenges/zb/solo_run

## sourceMappingURL=on_round_end.mcfunction.map
