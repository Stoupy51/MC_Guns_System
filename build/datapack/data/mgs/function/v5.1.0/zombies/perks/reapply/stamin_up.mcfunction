
#> mgs:v5.1.0/zombies/perks/reapply/stamin_up
#
# @executed	as @a[distance=..2,gamemode=!spectator,scores={mgs.zb.in_game=1,mgs.zb.downed=0}]
#
# @within	mgs:v5.1.0/zombies/perks/tombstone_collect
#			mgs:v5.1.0/zombies/whos_who/revive_complete
#

attribute @s minecraft:movement_speed modifier add mgs:stamin_up 0.07 add_multiplied_total
scoreboard players set @s mgs.stam_bonus 200
scoreboard players add @s mgs.stam 200

