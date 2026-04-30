
#> mgs:v5.0.0/zombies/revive/hud_yellow
#
# @within	???
#

data modify entity @n[tag=mgs.downed_hud] text[0] set value {"selector":"@a[tag=mgs.downed_spectator,sort=nearest,limit=1]","color":"yellow"}
data modify entity @n[tag=mgs.downed_hud] text[1] set value {"text":" ↓","color":"yellow"}

