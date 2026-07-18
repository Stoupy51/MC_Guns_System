
#> mgs:v5.1.0/multiplayer/show_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/menu with storage mgs:temp
#			mgs:v5.1.0/players/list_multiplayer with storage mgs:temp
#			mgs:v5.1.0/players/list_zombies with storage mgs:temp
#			mgs:v5.1.0/players/list_missions with storage mgs:temp
#			mgs:v5.1.0/zombies/map_select with storage mgs:temp
#			mgs:v5.1.0/multiplayer/select_class with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/hub with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_primary_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_secondary_pistol_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_secondary_overkill_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_scope_primary_full_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_scope_primary_no4_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_scope_primary_1only_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_scope_secondary_4only_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_primary_camo_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_secondary_camo_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_equip1_camo_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_equip2_camo_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_primary_mags_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_secondary_mags_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_equip_slot1_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_equip_slot2_dialog_macro with storage mgs:temp
#			mgs:v5.1.0/multiplayer/editor/show_perks_dialog with storage mgs:temp
#			mgs:v5.1.0/multiplayer/my_loadouts/browse with storage mgs:temp
#			mgs:v5.1.0/multiplayer/my_loadouts/browse_fav_only with storage mgs:temp
#			mgs:v5.1.0/multiplayer/my_loadouts/manage_build_public with storage mgs:temp
#			mgs:v5.1.0/multiplayer/my_loadouts/manage_build_private with storage mgs:temp
#			mgs:v5.1.0/multiplayer/marketplace/browse with storage mgs:temp
#			mgs:v5.1.0/multiplayer/marketplace/browse_fav_only with storage mgs:temp
#			mgs:v5.1.0/multiplayer/marketplace/browse_likes with storage mgs:temp
#			mgs:v5.1.0/multiplayer/map_select with storage mgs:temp
#			mgs:v5.1.0/missions/map_select with storage mgs:temp
#
# @args		dialog (unknown)
#

$dialog show @s $(dialog)

