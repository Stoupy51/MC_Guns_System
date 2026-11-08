
#> mgs:v5.4.1/progression/mp/award_bomb_defuse
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/gamemodes/snd/bomb_defused [ as @a[tag=mgs.xp_earner] ]
#			mgs:v5.4.1/multiplayer/gamemodes/demo/site_defused [ as @a[tag=mgs.xp_earner] ]
#

# S&D or Demolition defuse; worth more than a plant, it is rarer
scoreboard players add @s mgs.mp.xp_total 25
scoreboard players add @s mgs.mp.xp_prog 25
scoreboard players add @s mgs.mp.xp_session 25

# Observers of this award
scoreboard players add @s mgs.adv.mp.objectives 1
function mgs:v5.4.1/progression/adv/mp/objectives/check
function mgs:v5.4.1/progression/mp/settle

scoreboard players add @s mgs.st.mp.defuses 1

