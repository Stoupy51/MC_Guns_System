
#> mgs:v5.1.0/zombies/monkey/attract
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/monkey/tick
#

# Existing escorts near the monkey (stuck rescue / PaP lure): redirect them to it by flagging
# their trader — the "existing escort" case, handled without summoning a second taxi.
execute as @e[tag=mgs.zombie_round,tag=mgs.zb_escorted,distance=..40] at @s run function mgs:v5.1.0/zombies/escort/redirect_to_monkey

# Un-escorted zombies: start a fresh monkey-targeted escort on the nearest ones (cap-gated by
# escort's MAX_ESCORTS). Dogs excluded (escort can't freeze a wolf); the re-grab floor skips
# zombies already gathered at the monkey (they were released within MONKEY_RELEASE).
execute as @e[tag=mgs.zombie_round,tag=!mgs.zb_dog,tag=!mgs.zb_rising,tag=!mgs.zb_escorted,tag=!mgs.zb_escort_failed,distance=6..40,sort=nearest,limit=16] at @s if score #zb_escort_count mgs.data matches ..15 run function mgs:v5.1.0/zombies/monkey/pull_one

