
#> mgs:v5.0.1/zombies/traps/turret_hit
#
# @executed	as @e[tag=mgs.trap_head,predicate=mgs:v5.0.1/zombies/traps/turret_id_match] & at @s & facing entity @n[tag=mgs._turret_target] eyes & positioned ^ ^ ^1
#
# @within	mgs:v5.0.1/zombies/traps/turret_shoot
#

# Impact particles
particle minecraft:crit ~ ~1 ~ 0.2 0.3 0.2 0.1 8 force @a[distance=..48]

# Zombie hit: 45% of its max health
execute if entity @s[tag=mgs.zombie_round] store result storage mgs:temp _trap_dmg.amount int 1 run attribute @s minecraft:max_health get 0.45
execute if entity @s[tag=mgs.zombie_round] run data modify storage mgs:temp _trap_dmg.type set value "mgs:bullet"
execute if entity @s[tag=mgs.zombie_round] run return run function mgs:v5.0.1/zombies/traps/apply_trap_damage with storage mgs:temp _trap_dmg

# Player caught between the turret and the zombies: 2 damage
execute if entity @s[type=player,gamemode=!creative,gamemode=!spectator] if score @s mgs.zb.in_game matches 1.. run damage @s 2 mgs:bullet

