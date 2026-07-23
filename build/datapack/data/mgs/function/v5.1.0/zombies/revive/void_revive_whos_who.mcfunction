
#> mgs:v5.1.0/zombies/revive/void_revive_whos_who
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/full_death
#

gamemode adventure @s
function mgs:v5.1.0/zombies/revive/respawn_near_player
data modify storage mgs:temp _body_at set from entity @s Pos
function mgs:v5.1.0/zombies/whos_who/on_down

