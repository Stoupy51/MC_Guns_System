
#> mgs:v5.0.0/zombies/perks/apply
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.0.0/zombies/powerups/try_perk/juggernog {perk_id:"juggernog"} [ as @p[tag=mgs.pu_collecting] ]
#			mgs:v5.0.0/zombies/powerups/try_perk/speed_cola {perk_id:"speed_cola"} [ as @p[tag=mgs.pu_collecting] ]
#			mgs:v5.0.0/zombies/powerups/try_perk/double_tap {perk_id:"double_tap"} [ as @p[tag=mgs.pu_collecting] ]
#			mgs:v5.0.0/zombies/powerups/try_perk/quick_revive {perk_id:"quick_revive"} [ as @p[tag=mgs.pu_collecting] ]
#			mgs:v5.0.0/zombies/powerups/try_perk/mule_kick {perk_id:"mule_kick"} [ as @p[tag=mgs.pu_collecting] ]
#			mgs:v5.0.0/zombies/perks/on_right_click with storage mgs:temp _pk_data
#
# @args		perk_id (string)
#

# Set perk scoreboard for the player
$scoreboard players set @s mgs.zb.perk.$(perk_id) 1

# Call perk-specific effect function
$function mgs:v5.0.0/zombies/perks/apply/$(perk_id)

