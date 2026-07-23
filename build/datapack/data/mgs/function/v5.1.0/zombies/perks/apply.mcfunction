
#> mgs:v5.1.0/zombies/perks/apply
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.1.0/zombies/powerups/activate/random_perk with storage mgs:temp _pool [ as @p[tag=mgs.pu_collecting] ]
#			mgs:v5.1.0/zombies/perks/on_right_click with storage mgs:temp _pk_data
#			mgs:v5.1.0/zombies/wunderfizz/grant/juggernog with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/speed_cola with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/double_tap with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/quick_revive with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/mule_kick with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/stamin_up with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/phd_flopper with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/deadshot with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/timeslip with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/electric_cherry with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/tombstone with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/whos_who with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/dying_wish with storage mgs:temp _wf_grant
#			mgs:v5.1.0/zombies/wunderfizz/grant/widows_wine with storage mgs:temp _wf_grant
#
# @args		perk_id (unknown)
#

# Set perk scoreboard for the player
$scoreboard players set @s mgs.zb.perk.$(perk_id) 1

# Owning the perk voids any chip-in progress toward it (including perks granted for free by the
# random-perk power-up), so a re-purchase after going down starts from zero.
$scoreboard players set @s mgs.zb.perkpaid.$(perk_id) 0

# Call perk-specific effect function
$function mgs:v5.1.0/zombies/perks/apply/$(perk_id)

