
#> mgs:v5.1.0/progression/mp/award_bomb_pickup
#
# @executed	as @a[tag=mgs.xp_earner]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/try_pickup [ as @a[tag=mgs.xp_earner] ]
#

# Picking the S&D bomb up off the ground; small on purpose
scoreboard players add @s mgs.mp.xp_total 2
scoreboard players add @s mgs.mp.xp_prog 2
scoreboard players add @s mgs.mp.xp_session 2
function mgs:v5.1.0/progression/mp/settle

