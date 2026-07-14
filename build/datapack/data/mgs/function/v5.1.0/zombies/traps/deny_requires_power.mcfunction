
#> mgs:v5.1.0/zombies/traps/deny_requires_power
#
# @executed	as @e[tag=mgs._trap_new_bs]
#
# @within	mgs:v5.1.0/zombies/traps/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.this_trap_requires_power","color":"red"}]
function mgs:v5.1.0/zombies/feedback/sound_deny

