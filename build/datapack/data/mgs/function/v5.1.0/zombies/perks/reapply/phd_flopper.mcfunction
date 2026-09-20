
#> mgs:v5.1.0/zombies/perks/reapply/phd_flopper
#
# @executed	as @a[distance=..2,gamemode=!spectator,scores={mgs.zb.in_game=1,mgs.zb.downed=0}]
#
# @within	mgs:v5.1.0/zombies/perks/tombstone_collect
#			mgs:v5.1.0/zombies/whos_who/revive_complete
#

attribute @s minecraft:fall_damage_multiplier base set 0
scoreboard players set @s mgs.special.phd_flopper 1

