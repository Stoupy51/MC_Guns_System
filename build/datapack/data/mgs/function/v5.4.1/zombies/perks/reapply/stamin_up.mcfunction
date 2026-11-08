
#> mgs:v5.4.1/zombies/perks/reapply/stamin_up
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/perks/tombstone_collect
#			mgs:v5.4.1/zombies/whos_who/revive_complete
#

attribute @s minecraft:movement_speed modifier add mgs:stamin_up 0.07 add_multiplied_total
scoreboard players set @s mgs.stam_bonus 300
scoreboard players add @s mgs.stam 300

