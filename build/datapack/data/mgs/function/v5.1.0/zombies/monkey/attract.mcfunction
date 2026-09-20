
#> mgs:v5.1.0/zombies/monkey/attract
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/monkey/tick
#

# Existing escorts near the monkey (stuck rescue / PaP lure): redirect them to it by flagging
# their trader — the "existing escort" case, handled without summoning a second taxi.
execute as @e[tag=mgs.zombie_round,tag=mgs.zb_escorted,distance=..40] at @s run function mgs:v5.1.0/zombies/escort/redirect_to_monkey

# Un-escorted zombies: start a fresh monkey-targeted escort on every one of them. Dogs excluded
# (escort can't freeze a wolf — see the header); the re-grab floor skips whatever is already at the
# monkey.
execute as @e[tag=mgs.zombie_round,tag=!mgs.zb_dog,tag=!mgs.zb_rising,tag=!mgs.zb_escorted,tag=!mgs.zb_escort_failed,distance=6..40] at @s run function mgs:v5.1.0/zombies/monkey/pull_one

