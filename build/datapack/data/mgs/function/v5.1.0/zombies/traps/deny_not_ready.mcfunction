
#> mgs:v5.1.0/zombies/traps/deny_not_ready
#
# @executed	as @e[tag=mgs._trap_new_bs]
#
# @within	mgs:v5.1.0/zombies/traps/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.trap_is_on_cooldown_and_not_ready_yet","color":"yellow"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

