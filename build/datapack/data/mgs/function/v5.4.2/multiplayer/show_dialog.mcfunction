
#> mgs:v5.4.2/multiplayer/show_dialog
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/config/menu with storage mgs:temp
#			mgs:v5.4.2/players/list_multiplayer with storage mgs:temp
#			mgs:v5.4.2/players/list_zombies with storage mgs:temp
#			mgs:v5.4.2/players/list_missions with storage mgs:temp
#			mgs:v5.4.2/zombies/map_select with storage mgs:temp
#			mgs:v5.4.2/zombies/knife_camo/menu with storage mgs:temp
#			mgs:v5.4.2/zombies/mystery_box/pool/dialog_global with storage mgs:temp
#			mgs:v5.4.2/zombies/mystery_box/pool/dialog_map with storage mgs:temp
#			mgs:v5.4.2/zombies/save/save_menu with storage mgs:temp
#			mgs:v5.4.2/zombies/save/request with storage mgs:temp
#			mgs:v5.4.2/zombies/save/load_menu with storage mgs:temp
#			mgs:v5.4.2/zombies/save/delete_ask with storage mgs:temp
#			mgs:v5.4.2/multiplayer/select_class with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/hub with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_primary_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_secondary_pistol_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_secondary_overkill_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_scope_primary_full with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_scope_primary_no4 with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_scope_primary_1only with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_scope_secondary_4only with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_primary_camo_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_secondary_camo_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_equip1_camo_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_equip2_camo_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_knife_camo_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_primary_mags_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_secondary_mags_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_equip_slot1_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_equip_slot2_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/show_perks_dialog with storage mgs:temp
#			mgs:v5.4.2/multiplayer/my_loadouts/browse with storage mgs:temp
#			mgs:v5.4.2/multiplayer/my_loadouts/browse_fav_only with storage mgs:temp
#			mgs:v5.4.2/multiplayer/my_loadouts/manage_build_public with storage mgs:temp
#			mgs:v5.4.2/multiplayer/my_loadouts/manage_build_private with storage mgs:temp
#			mgs:v5.4.2/multiplayer/marketplace/browse with storage mgs:temp
#			mgs:v5.4.2/multiplayer/marketplace/browse_fav_only with storage mgs:temp
#			mgs:v5.4.2/multiplayer/marketplace/browse_likes with storage mgs:temp
#			mgs:v5.4.2/multiplayer/map_select with storage mgs:temp
#			mgs:v5.4.2/missions/map_select with storage mgs:temp
#			mgs:v5.4.2/stats/menu/zb_dialog with storage mgs:temp
#			mgs:v5.4.2/stats/menu/mp_dialog with storage mgs:temp
#			mgs:v5.4.2/stats/menu/mi_dialog with storage mgs:temp
#			mgs:v5.4.2/stats/menu/players_list with storage mgs:temp
#			mgs:v5.4.2/stats/board/menu with storage mgs:temp
#			mgs:v5.4.2/stats/board/maps with storage mgs:temp
#			mgs:v5.4.2/stats/board/show with storage mgs:temp
#			mgs:v5.4.2/stats/admin/boards with storage mgs:temp
#			mgs:v5.4.2/maps/editor/settings with storage mgs:temp
#			mgs:v5.4.2/maps/editor/export with storage mgs:temp
#			mgs:v5.4.2/maps/editor/delete_confirm with storage mgs:temp
#			mgs:v5.4.2/maps/editor/invite with storage mgs:temp
#			mgs:v5.4.2/maps/editor/form/open/zombie_spawn with storage mgs:temp [ as @a[tag=mgs.ed_form_user] ]
#			mgs:v5.4.2/maps/editor/form/open/special_spawn with storage mgs:temp [ as @a[tag=mgs.ed_form_user] ]
#			mgs:v5.4.2/maps/editor/form/open/mystery_box_pos with storage mgs:temp [ as @a[tag=mgs.ed_form_user] ]
#			mgs:v5.4.2/maps/editor/form/open/wallbuy with storage mgs:temp [ as @a[tag=mgs.ed_form_user] ]
#			mgs:v5.4.2/maps/editor/form/open/perk_machine with storage mgs:temp [ as @a[tag=mgs.ed_form_user] ]
#			mgs:v5.4.2/maps/editor/form/open/trap with storage mgs:temp [ as @a[tag=mgs.ed_form_user] ]
#
# @args		dialog (unknown)
#

scoreboard players set #dialog_shown mgs.data 1
$dialog show @s $(dialog)

