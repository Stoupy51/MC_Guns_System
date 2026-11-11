
#> mgs:v5.4.2/zombies/revive/void_revive_whos_who
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/revive/full_death
#

gamemode adventure @s
function mgs:v5.4.2/zombies/revive/respawn_near_player
execute at @s summon minecraft:marker run function mgs:v5.4.2/shared/probe_pos
data modify storage mgs:temp _body_at set from storage mgs:temp _probe_pos
function mgs:v5.4.2/zombies/whos_who/on_down

