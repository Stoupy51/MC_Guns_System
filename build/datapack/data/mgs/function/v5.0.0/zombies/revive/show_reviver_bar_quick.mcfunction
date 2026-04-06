
#> mgs:v5.0.0/zombies/revive/show_reviver_bar_quick
#
# @executed	as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] & facing entity @s eyes
#
# @within	mgs:v5.0.0/zombies/revive/check_reviver
#

title @s actionbar [[{"text":"⚡ ","color":"aqua"}, {"translate":"mgs.reviving"}],{"score":{"name":"@p[tag=mgs.downed,sort=nearest,distance=..2.5]","objective":"mgs.zb.revive_p"},"color":"green"},{"text":"/30t","color":"gray"}]

