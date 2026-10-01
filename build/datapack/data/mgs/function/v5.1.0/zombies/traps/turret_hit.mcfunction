
#> mgs:v5.1.0/zombies/traps/turret_hit
#
# @within	string in mgs:v5.1.0/zombies/traps/turret_shoot
#

particle minecraft:crit ~ ~1 ~ 0.2 0.3 0.2 0.1 8 force @a[distance=..48]

# 45% of the zombie's max health.
execute if entity @s[tag=mgs.zombie_round] store result storage mgs:temp _trap_dmg.amount int 1 run attribute @s minecraft:max_health get 0.45
execute if entity @s[tag=mgs.zombie_round] run data modify storage mgs:temp _trap_dmg.type set value "mgs:bullet"
execute if entity @s[tag=mgs.zombie_round] run return run function mgs:v5.1.0/zombies/traps/apply_trap_damage with storage mgs:temp _trap_dmg

execute if entity @s[type=player,gamemode=!creative,gamemode=!spectator] if score @s mgs.zb.in_game matches 1.. run damage @s 2 mgs:bullet

