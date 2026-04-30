
#> mgs:v5.0.0/zombies/revive/check_solo_qr
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/downed_tick
#

# Only trigger if there are no other alive in-game players besides this downed player
execute store result score #zb_other_alive mgs.data if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator]
execute if score #zb_other_alive mgs.data matches 0 run function mgs:v5.0.0/zombies/revive/solo_qr_tick

