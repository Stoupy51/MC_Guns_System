
#> mgs:v5.4.2/multiplayer/vanilla_kill_credit
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/on_respawn
#

execute as @a[tag=mgs.temp_killer] run function #mgs:signals/on_kill

# Melee, fall and fire never go through the raycast, so no headshot; cleared so a previous bullet kill cannot leak into it.
scoreboard players set #mp_kill_headshot mgs.data 0
function mgs:v5.4.2/multiplayer/random_kill_message

