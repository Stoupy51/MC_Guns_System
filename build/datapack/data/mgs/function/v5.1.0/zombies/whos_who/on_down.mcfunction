
#> mgs:v5.1.0/zombies/whos_who/on_down
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/revive/on_down
#

# Read the death location (branch runs before the normal flow computes it)
execute store result storage mgs:temp rv_x double 0.001 run data get entity @s LastDeathLocation.pos[0] 1000
execute store result storage mgs:temp rv_y double 0.001 run data get entity @s LastDeathLocation.pos[1] 1000
execute store result storage mgs:temp rv_z double 0.001 run data get entity @s LastDeathLocation.pos[2] 1000

# Snapshot perks + inventory (for recovery on revive) — BEFORE anything is stripped
scoreboard players operation @s mgs.zb.wwp.juggernog = @s mgs.zb.perk.juggernog
scoreboard players operation @s mgs.zb.wwp.speed_cola = @s mgs.zb.perk.speed_cola
scoreboard players operation @s mgs.zb.wwp.double_tap = @s mgs.zb.perk.double_tap
scoreboard players operation @s mgs.zb.wwp.quick_revive = @s mgs.zb.perk.quick_revive
scoreboard players operation @s mgs.zb.wwp.mule_kick = @s mgs.zb.perk.mule_kick
scoreboard players operation @s mgs.zb.wwp.stamin_up = @s mgs.zb.perk.stamin_up
scoreboard players operation @s mgs.zb.wwp.phd_flopper = @s mgs.zb.perk.phd_flopper
scoreboard players operation @s mgs.zb.wwp.deadshot = @s mgs.zb.perk.deadshot
scoreboard players operation @s mgs.zb.wwp.timeslip = @s mgs.zb.perk.timeslip
scoreboard players operation @s mgs.zb.wwp.electric_cherry = @s mgs.zb.perk.electric_cherry
scoreboard players operation @s mgs.zb.wwp.tombstone = @s mgs.zb.perk.tombstone
scoreboard players operation @s mgs.zb.wwp.whos_who = @s mgs.zb.perk.whos_who
scoreboard players operation @s mgs.zb.wwp.dying_wish = @s mgs.zb.perk.dying_wish
scoreboard players operation @s mgs.zb.wwp.widows_wine = @s mgs.zb.perk.widows_wine

# Assign a fresh downed_id for the body mannequin (same counter as the revive system)
scoreboard players add #downed_id_next mgs.data 1
scoreboard players operation @s mgs.zb.downed_id = #downed_id_next mgs.data
execute store result storage mgs:temp _ww_id.id int 1 run scoreboard players get @s mgs.zb.downed_id
function mgs:v5.1.0/zombies/whos_who/snapshot_inv with storage mgs:temp _ww_id

# Summon the body mannequin wearing the owner's armor/skin, and a HUD above it, at the death spot
summon minecraft:mannequin ~ ~.5 ~ {Invulnerable:1b,pose:"swimming",hide_description:true,Tags:["mgs.ww_body","mgs.ww_body_new","mgs.gm_entity"]}
scoreboard players operation @n[tag=mgs.ww_body_new] mgs.zb.downed_id = @s mgs.zb.downed_id
data modify entity @n[tag=mgs.ww_body_new] equipment set from entity @s equipment
loot replace entity @n[tag=mgs.ww_body_new] weapon.mainhand loot mgs:get_username
data modify entity @n[tag=mgs.ww_body_new] profile set from entity @n[tag=mgs.ww_body_new] equipment.mainhand.components."minecraft:profile"
data modify storage mgs:temp rv_name set from entity @n[tag=mgs.ww_body_new] equipment.mainhand.components."minecraft:profile".name
execute unless data storage mgs:temp rv_name run data modify storage mgs:temp rv_name set value "???"
item replace entity @n[tag=mgs.ww_body_new] weapon.mainhand with minecraft:air
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.ww_hud","mgs.ww_hud_new","mgs.gm_entity"],billboard:"vertical",shadow:1b,see_through:0b,teleport_duration:1,transformation:{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},text:[{"text":"...","color":"dark_aqua"},{"text":" ↓","color":"dark_aqua"}]}
scoreboard players operation @n[tag=mgs.ww_hud_new] mgs.zb.downed_id = @s mgs.zb.downed_id
function mgs:v5.1.0/zombies/whos_who/set_hud_name with storage mgs:temp
function mgs:v5.1.0/zombies/whos_who/tp_body with storage mgs:temp
tag @e[tag=mgs.ww_body_new] remove mgs.ww_body_new
tag @e[tag=mgs.ww_hud_new] remove mgs.ww_hud_new

# Strip perks (the doppelganger starts fresh)
function mgs:v5.1.0/zombies/perks/lose_all

# Doppelganger loadout: wipe everything and hand back only the starting knife + pistol kit
clear @s
gamemode adventure @s
function mgs:v5.1.0/zombies/inventory/give_respawn_loadout

# Keep the player where they respawned near a teammate is jarring — put them at their body so they
# can choose to self-revive or fight on
function mgs:v5.1.0/zombies/revive/tp_revive_pos with storage mgs:temp

# Enter doppelganger state
tag @s add mgs.ww_active
scoreboard players set @s mgs.zb.ww.bleed 1200
scoreboard players set @s mgs.zb.ww.rev 0

# Announce
title @s times 5 40 15
title @s title ["👥"]
title @s subtitle [{"translate":"mgs.whos_who_revive_your_body_or_fight_on","color":"dark_aqua"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"aqua"},{"translate":"mgs.went_down_but_plays_on_as_a_doppelganger","color":"gray"}]

