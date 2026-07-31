
#> mgs:v5.1.0/progression/mp/award_bomb_defuse
#
# @executed	as @a[tag=mgs.xp_earner]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_defused [ as @a[tag=mgs.xp_earner] ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/site_defused [ as @a[tag=mgs.xp_earner] ]
#

# S&D or Demolition defuse; worth more than a plant, it is rarer
scoreboard players add @s mgs.mp.xp_total 25
scoreboard players add @s mgs.mp.xp_prog 25
scoreboard players add @s mgs.mp.xp_session 25
function mgs:v5.1.0/progression/mp/settle

