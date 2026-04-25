
#> mgs:v5.0.0/zombies/inventory/refresh_info_item
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.0.0/zombies/game_tick [ as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] ]
#			mgs:v5.0.0/zombies/inventory/give_starting_loadout
#			mgs:v5.0.0/zombies/inventory/recreate_critical_items
#

# Resolve scoreboard values into storage so lore lines render concrete numbers.
execute store result storage mgs:temp info.round int 1 run scoreboard players get #zb_round mgs.data
execute store result storage mgs:temp info.points int 1 run scoreboard players get @s mgs.zb.points
execute store result storage mgs:temp info.kills int 1 run scoreboard players get @s mgs.zb.kills
execute store result storage mgs:temp info.downs int 1 run scoreboard players get @s mgs.zb.downs

function mgs:v5.0.0/zombies/inventory/refresh_info_item_render with storage mgs:temp info
function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.8",group:"hotbar",index:8}

