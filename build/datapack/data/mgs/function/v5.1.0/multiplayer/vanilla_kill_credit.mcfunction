
#> mgs:v5.1.0/multiplayer/vanilla_kill_credit
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/on_respawn
#

execute as @a[tag=mgs.temp_killer] run function #mgs:signals/on_kill

# No headshots on this path: it is reached by vanilla damage (melee, fall, fire), none of which goes
# through the raycast that decides headshots. Cleared explicitly so a previous bullet kill cannot leak
# its marker onto an unrelated knife kill.
scoreboard players set #mp_kill_headshot mgs.data 0
function mgs:v5.1.0/multiplayer/random_kill_message

