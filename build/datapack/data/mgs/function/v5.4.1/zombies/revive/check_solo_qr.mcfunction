
#> mgs:v5.4.1/zombies/revive/check_solo_qr
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/revive/downed_tick
#

# Only when @s is the only in-game player: in co-op a downed Quick Revive owner never self-revives.
execute store result score #zb_ingame_total mgs.data if entity @a[scores={mgs.zb.in_game=1}]
execute if score #zb_ingame_total mgs.data matches 2.. run return 0
function mgs:v5.4.1/zombies/revive/solo_qr_tick

