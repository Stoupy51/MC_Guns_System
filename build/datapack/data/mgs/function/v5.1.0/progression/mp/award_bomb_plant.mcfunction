
#> mgs:v5.1.0/progression/mp/award_bomb_plant
#
# @executed	as @a[tag=mgs.snd_carrier,limit=1] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_planted
#			mgs:v5.1.0/multiplayer/gamemodes/demo/site_planted [ as @a[tag=mgs.xp_earner] ]
#

# S&D or Demolition plant, to whoever was channeling it
scoreboard players add @s mgs.mp.xp_total 20
scoreboard players add @s mgs.mp.xp_prog 20
scoreboard players add @s mgs.mp.xp_session 20
function mgs:v5.1.0/progression/mp/settle

