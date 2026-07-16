
#> mgs:v5.1.0/zombies/perks/override_perk_model
#
# @within	mgs:v5.1.0/zombies/perks/setup_iter with storage mgs:temp _pk_disp
#			mgs:v5.1.0/maps/editor/displays/perk_machine with storage mgs:temp _pk_disp
#
# @args		perk_id (unknown)
#

$data modify storage mgs:temp _pk_disp.item_model set value "mgs:perk_machine_$(perk_id)"

