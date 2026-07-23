
#> mgs:v5.1.0/zombies/inventory/refresh_info_item
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] ]
#			mgs:v5.1.0/zombies/inventory/give_starting_loadout
#			mgs:v5.1.0/zombies/inventory/recreate_critical_items
#

# Resolve scoreboard values into storage so lore lines render concrete numbers.
execute store result storage mgs:temp info.round int 1 run scoreboard players get #zb_round mgs.data
execute store result storage mgs:temp info.points int 1 run scoreboard players get @s mgs.zb.points
execute store result storage mgs:temp info.kills int 1 run scoreboard players get @s mgs.zb.kills
execute store result storage mgs:temp info.downs int 1 run scoreboard players get @s mgs.zb.downs

# Build the base lore list with baked numbers, then append a line per owned perk.
function mgs:v5.1.0/zombies/inventory/build_info_lore with storage mgs:temp info
scoreboard players set #info_perk_count mgs.data 0
execute if score @s mgs.zb.perk.juggernog matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.speed_cola matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.double_tap matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.quick_revive matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.mule_kick matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.stamin_up matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.phd_flopper matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.deadshot matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.timeslip matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.electric_cherry matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.tombstone matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.whos_who matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.dying_wish matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score @s mgs.zb.perk.widows_wine matches 1 run scoreboard players add #info_perk_count mgs.data 1
execute if score #info_perk_count mgs.data matches 1.. run data modify storage mgs:temp info.lore append value {"text":"","italic":false}
execute if score #info_perk_count mgs.data matches 1.. run data modify storage mgs:temp info.lore append value {"translate":"mgs.perks_3","color":"light_purple","italic":false}
execute if score @s mgs.zb.perk.juggernog matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Juggernog","color":"red","italic":false}
execute if score @s mgs.zb.perk.speed_cola matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Speed Cola","color":"green","italic":false}
execute if score @s mgs.zb.perk.double_tap matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Double Tap","color":"yellow","italic":false}
execute if score @s mgs.zb.perk.quick_revive matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Quick Revive","color":"aqua","italic":false}
execute if score @s mgs.zb.perk.mule_kick matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Mule Kick","color":"dark_green","italic":false}
execute if score @s mgs.zb.perk.stamin_up matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Stamin-Up","color":"gold","italic":false}
execute if score @s mgs.zb.perk.phd_flopper matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 PhD Flopper","color":"dark_purple","italic":false}
execute if score @s mgs.zb.perk.deadshot matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Deadshot Daiquiri","color":"dark_green","italic":false}
execute if score @s mgs.zb.perk.timeslip matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Timeslip","color":"light_purple","italic":false}
execute if score @s mgs.zb.perk.electric_cherry matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Electric Cherry","color":"blue","italic":false}
execute if score @s mgs.zb.perk.tombstone matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Tombstone","color":"gold","italic":false}
execute if score @s mgs.zb.perk.whos_who matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Who's Who","color":"dark_aqua","italic":false}
execute if score @s mgs.zb.perk.dying_wish matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Dying Wish","color":"blue","italic":false}
execute if score @s mgs.zb.perk.widows_wine matches 1 run data modify storage mgs:temp info.lore append value {"text":"\u2022 Widow's Wine","color":"dark_red","italic":false}

function mgs:v5.1.0/zombies/inventory/refresh_info_item_render with storage mgs:temp info
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.8",group:"hotbar",index:8}

# Keep the perk display items (inventory.26 and down) in sync with the same cadence
function mgs:v5.1.0/zombies/inventory/refresh_perk_items

