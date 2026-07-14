
#> mgs:v5.1.0/zombies/revive/check_solo_qr
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/downed_tick
#

# Only trigger in a TRUE solo game: @s must be the only in-game player. Teammates being
# downed or bled-out does NOT make the game solo — in co-op, a downed player with Quick
# Revive must never self-revive (all players down with no reviver = game over instead).
execute store result score #zb_ingame_total mgs.data if entity @a[scores={mgs.zb.in_game=1}]
execute if score #zb_ingame_total mgs.data matches 2.. run return 0
function mgs:v5.1.0/zombies/revive/solo_qr_tick

