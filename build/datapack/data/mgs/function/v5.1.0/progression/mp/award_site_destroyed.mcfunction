
#> mgs:v5.1.0/progression/mp/award_site_destroyed
#
# @executed	as @a[tag=mgs.xp_earner]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/site_destroyed [ as @a[tag=mgs.xp_earner] ]
#

# A Demolition site actually going down, to the attackers in the blast
scoreboard players add @s mgs.mp.xp_total 20
scoreboard players add @s mgs.mp.xp_prog 20
scoreboard players add @s mgs.mp.xp_session 20

# Observers of this award
scoreboard players add @s mgs.adv.mp.objectives 1
function mgs:v5.1.0/progression/mp/settle

## sourceMappingURL=award_site_destroyed.mcfunction.map
