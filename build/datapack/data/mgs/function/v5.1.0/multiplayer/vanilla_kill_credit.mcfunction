
#> mgs:v5.1.0/multiplayer/vanilla_kill_credit
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/on_respawn
#

execute as @a[tag=mgs.temp_killer] run function #mgs:signals/on_kill
function mgs:v5.1.0/multiplayer/random_kill_message

