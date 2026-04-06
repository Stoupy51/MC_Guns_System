
#> mgs:v5.0.0/zombies/revive/downed_tick
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/tick [ at @s ]
#

# Decrement bleed timer
scoreboard players remove @s mgs.zb.bleed 1

# Check if any teammate is reviving (within range and looking at downed player)
# Reset progress if no one is nearby
scoreboard players set #zb_reviving mgs.data 0
execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] facing entity @s eyes run function mgs:v5.0.0/zombies/revive/check_reviver

# If someone is actively reviving, increment progress
execute if score #zb_reviving mgs.data matches 1.. run function mgs:v5.0.0/zombies/revive/progress_tick

# If no one is reviving, decay progress
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.revive_p matches 1.. run scoreboard players remove @s mgs.zb.revive_p 2

# Show bleed timer on actionbar
execute store result storage mgs:temp _rv_sec int 1 run scoreboard players get @s mgs.zb.bleed
function mgs:v5.0.0/zombies/revive/show_bleed_bar

# Bleed out: time's up
execute if score @s mgs.zb.bleed matches ..0 run function mgs:v5.0.0/zombies/revive/bleed_out

