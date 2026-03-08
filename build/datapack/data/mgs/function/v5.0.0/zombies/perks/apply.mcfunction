
#> mgs:v5.0.0/zombies/perks/apply
#
# @within	mgs:v5.0.0/zombies/perks/on_right_click with storage mgs:temp _pk_data
#
# @args		perk_id (unknown)
#

# Set perk scoreboard for the player
$scoreboard players set @s mgs.zb.perk.$(perk_id) 1

# Call perk-specific effect function
$function mgs:v5.0.0/zombies/perks/apply/$(perk_id)

