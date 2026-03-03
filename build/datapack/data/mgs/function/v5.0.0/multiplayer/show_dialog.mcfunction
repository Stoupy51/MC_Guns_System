
#> mgs:v5.0.0/multiplayer/show_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/select_class with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_primary_dialog_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/scope/primary_full_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/scope/primary_no4_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/scope/primary_1only_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_primary_mags_dialog_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_secondary_dialog_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/scope/secondary_4only_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_secondary_mags_dialog_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_equip_slot1_dialog_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_equip_slot2_dialog_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_perks_dialog_macro with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_confirm with storage mgs:temp
#			mgs:v5.0.0/multiplayer/my_loadouts/browse with storage mgs:temp
#			mgs:v5.0.0/multiplayer/marketplace/browse with storage mgs:temp
#
# @args		dialog (unknown)
#

$dialog show @s $(dialog)

