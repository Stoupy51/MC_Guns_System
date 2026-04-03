
#> mgs:v5.0.0/zombies/traps/deny_not_ready
#
# @executed	as @e[tag=_trap_new_bs]
#
# @within	mgs:v5.0.0/zombies/traps/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.trap_is_on_cooldown_and_not_ready_yet","color":"yellow"}]
function mgs:v5.0.0/zombies/feedback/sound_deny

