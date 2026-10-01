
#> mgs:v5.1.0/zombies/perks/apply
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.1.0/zombies/powerups/activate/random_perk with storage mgs:temp _pool [ as @p[tag=mgs.pu_collecting] ]
#			mgs:v5.1.0/zombies/perks/on_right_click with storage mgs:temp _pk_data
#			mgs:v5.1.0/zombies/wunderfizz/collect with storage mgs:temp _wf_grant
#
# @args		perk_id (unknown)
#

$scoreboard players set @s mgs.zb.perk.$(perk_id) 1

# Owning the perk (even from the random-perk power-up) clears its chip-in progress, so a rebuy after going down starts at zero.
$scoreboard players set @s mgs.zb.perkpaid.$(perk_id) 0

$function mgs:v5.1.0/zombies/perks/apply/$(perk_id)

