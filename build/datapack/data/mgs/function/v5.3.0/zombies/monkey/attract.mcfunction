
#> mgs:v5.3.0/zombies/monkey/attract
#
# @executed	at @s
#
# @within	mgs:v5.3.0/zombies/monkey/tick
#

execute if score #zb_special_round mgs.data matches 1 run return 0

# Zombies already escorted (stuck rescue, PaP lure) are redirected by flagging their trader.
execute as @e[tag=mgs.zombie_round,tag=mgs.zb_escorted,distance=..40] at @s run function mgs:v5.3.0/zombies/escort/redirect_to_monkey

# Every other zombie gets a monkey escort; zombies already at the monkey are skipped.
execute as @e[tag=mgs.zombie_round,tag=!mgs.zb_rising,tag=!mgs.zb_escorted,tag=!mgs.zb_escort_failed,distance=6..40] at @s run function mgs:v5.3.0/zombies/monkey/pull_one

