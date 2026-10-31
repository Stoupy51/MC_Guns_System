
#> mgs:v5.3.0/multiplayer/show_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/config/menu with storage mgs:temp
#			mgs:v5.3.0/players/list_multiplayer with storage mgs:temp
#			mgs:v5.3.0/players/list_zombies with storage mgs:temp
#			mgs:v5.3.0/players/list_missions with storage mgs:temp
#			mgs:v5.3.0/zombies/map_select with storage mgs:temp
#			mgs:v5.3.0/zombies/knife_camo/menu with storage mgs:temp
#			mgs:v5.3.0/zombies/mystery_box/pool/dialog_global with storage mgs:temp
#			mgs:v5.3.0/zombies/mystery_box/pool/dialog_map with storage mgs:temp
#			mgs:v5.3.0/multiplayer/select_class with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/hub with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_primary_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_secondary_pistol_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_secondary_overkill_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_scope_primary_full with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_scope_primary_no4 with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_scope_primary_1only with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_scope_secondary_4only with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_primary_camo_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_secondary_camo_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_equip1_camo_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_equip2_camo_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_knife_camo_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_primary_mags_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_secondary_mags_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_equip_slot1_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_equip_slot2_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/editor/show_perks_dialog with storage mgs:temp
#			mgs:v5.3.0/multiplayer/my_loadouts/browse with storage mgs:temp
#			mgs:v5.3.0/multiplayer/my_loadouts/browse_fav_only with storage mgs:temp
#			mgs:v5.3.0/multiplayer/my_loadouts/manage_build_public with storage mgs:temp
#			mgs:v5.3.0/multiplayer/my_loadouts/manage_build_private with storage mgs:temp
#			mgs:v5.3.0/multiplayer/marketplace/browse with storage mgs:temp
#			mgs:v5.3.0/multiplayer/marketplace/browse_fav_only with storage mgs:temp
#			mgs:v5.3.0/multiplayer/marketplace/browse_likes with storage mgs:temp
#			mgs:v5.3.0/multiplayer/map_select with storage mgs:temp
#			mgs:v5.3.0/missions/map_select with storage mgs:temp
#			mgs:v5.3.0/stats/menu/zb_dialog with storage mgs:temp
#			mgs:v5.3.0/stats/menu/mp_dialog with storage mgs:temp
#			mgs:v5.3.0/stats/menu/mi_dialog with storage mgs:temp
#			mgs:v5.3.0/stats/menu/players_list with storage mgs:temp
#			mgs:v5.3.0/stats/board/menu with storage mgs:temp
#			mgs:v5.3.0/stats/board/maps with storage mgs:temp
#			mgs:v5.3.0/stats/board/show with storage mgs:temp
#			mgs:v5.3.0/stats/admin/boards with storage mgs:temp
#			mgs:v5.3.0/maps/editor/settings with storage mgs:temp
#			mgs:v5.3.0/maps/editor/export with storage mgs:temp
#			mgs:v5.3.0/maps/editor/delete_confirm with storage mgs:temp
#			mgs:v5.3.0/maps/editor/form/open/zombie_spawn with storage mgs:temp [ as @a[tag=mgs.ed_form_user] ]
#			mgs:v5.3.0/maps/editor/form/open/special_spawn with storage mgs:temp [ as @a[tag=mgs.ed_form_user] ]
#			mgs:v5.3.0/maps/editor/form/open/mystery_box_pos with storage mgs:temp [ as @a[tag=mgs.ed_form_user] ]
#
# @args		dialog (unknown)
#

$dialog show @s $(dialog)

