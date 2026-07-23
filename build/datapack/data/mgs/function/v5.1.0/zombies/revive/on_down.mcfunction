
#> mgs:v5.1.0/zombies/revive/on_down
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/on_respawn
#

# Dying Wish (highest priority): if owned and off cooldown, cheat death with a berserk instead of
# going down. Returns before any downed state is set. Must stay ABOVE the Who's Who branch.
execute if score @s mgs.zb.perk.dying_wish matches 1 if score @s mgs.zb.dw_cd matches ..0 run return run function mgs:v5.1.0/zombies/perks/dying_wish_trigger

# Who's Who (co-op only): keep playing as a doppelganger with a pistol instead of entering the
# downed state; the body drops as a revivable mannequin. Above Tombstone. Disabled solo (a solo
# doppelganger down is game over — falls through to the normal down below).
execute store result score #ww_ingame mgs.data if entity @a[scores={mgs.zb.in_game=1}]
execute if score @s mgs.zb.perk.whos_who matches 1 if score #ww_ingame mgs.data matches 2.. run return run function mgs:v5.1.0/zombies/whos_who/on_down

# Mark player as downed
scoreboard players set @s mgs.zb.downed 1
scoreboard players set @s mgs.zb.bleed 1200
scoreboard players set @s mgs.zb.revive_p 0
tag @s add mgs.downed_spectator

# Reset death counter (already set 0 by on_respawn caller, but be safe)
scoreboard players set @s mgs.mp.death_count 0

# Read death position at full float precision (multiply by 1000, store as double 0.001)
execute store result score #rv_y_raw mgs.data run data get entity @s LastDeathLocation.pos[1] 1000
scoreboard players add #rv_y_raw mgs.data 2000
execute store result storage mgs:temp rv_x double 0.001 run data get entity @s LastDeathLocation.pos[0] 1000
execute store result storage mgs:temp rv_y double 0.001 run data get entity @s LastDeathLocation.pos[1] 1000
execute store result storage mgs:temp rv_z double 0.001 run data get entity @s LastDeathLocation.pos[2] 1000
execute store result storage mgs:temp rv_y_hud double 0.001 run scoreboard players get #rv_y_raw mgs.data

# Assign a unique downed ID to this player and their mannequin
scoreboard players add #downed_id_next mgs.data 1
scoreboard players operation @s mgs.zb.downed_id = #downed_id_next mgs.data

# Summon mannequin (crouching pose, invulnerable, temp tag for targeting)
summon minecraft:mannequin ~ ~.5 ~ {Invulnerable:1b,pose:"swimming",hide_description:true,Tags:["mgs.downed_mannequin","mgs.downed_new","mgs.gm_entity"]}

# Copy the player's downed_id to the mannequin so we can find it uniquely later
scoreboard players operation @n[tag=mgs.downed_new] mgs.zb.downed_id = @s mgs.zb.downed_id

# Copy player armor to mannequin
data modify entity @n[tag=mgs.downed_new] equipment set from entity @s equipment

# Copy player head item (which contains the profile component) to get their skin
# Use the get_username loot table to generate a player_head with profile, then copy profile from it
loot replace entity @n[tag=mgs.downed_new] weapon.mainhand loot mgs:get_username
data modify entity @n[tag=mgs.downed_new] profile set from entity @n[tag=mgs.downed_new] equipment.mainhand.components."minecraft:profile"

# Capture the owner's literal name for the HUD before clearing the hand. A "nearest downed
# spectator" selector must never be used for the name: on_down runs at the shared respawn
# point, so same-tick batch downs all resolve the selector to the same tied player
data modify storage mgs:temp rv_name set from entity @n[tag=mgs.downed_new] equipment.mainhand.components."minecraft:profile".name
execute unless data storage mgs:temp rv_name run data modify storage mgs:temp rv_name set value "???"
item replace entity @n[tag=mgs.downed_new] weapon.mainhand with minecraft:air

# Summon text_display HUD above mannequin (temp tag, teleported below; name set right after via macro)
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.downed_hud","mgs.downed_hud_new","mgs.gm_entity"],billboard:"vertical",shadow:1b,see_through:0b,teleport_duration:1,transformation:{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},text:[{"text":"...","color":"yellow"},{"text":" ↓","color":"yellow"}]}
function mgs:v5.1.0/zombies/revive/set_hud_name with storage mgs:temp

# Copy the player's downed_id to the HUD so it can be id-matched (never "nearest") later
scoreboard players operation @n[tag=mgs.downed_hud_new] mgs.zb.downed_id = @s mgs.zb.downed_id

# Teleport mannequin and HUD to death location
function mgs:v5.1.0/zombies/revive/tp_to_death with storage mgs:temp

# Remove temp tags so future queries don't accidentally match
tag @e[tag=mgs.downed_new] remove mgs.downed_new
tag @e[tag=mgs.downed_hud_new] remove mgs.downed_hud_new

# Electric Cherry: discharge a full-strength shock at the down spot (BO behavior), before the
# perk is stripped. used==cap==1 makes it the maximum-size discharge.
scoreboard players set #ec_used mgs.data 1
scoreboard players set #ec_cap mgs.data 1
execute if score @s mgs.special.electric_cherry matches 1 at @s run function mgs:v5.1.0/zombies/perks/electric_cherry_shock

# Tombstone: spawn a recovery marker at the death spot (snapshots the owner's perks HERE, before
# they are stripped). No-op solo or when unowned. Only reached on the normal-down path (Who's Who,
# which returns earlier, takes priority so a marker never spawns for a doppelganger).
execute if score @s mgs.zb.perk.tombstone matches 1 run function mgs:v5.1.0/zombies/perks/tombstone_on_down

# Remove all perks when going down
function mgs:v5.1.0/zombies/perks/lose_all

# Player enters spectator mode
gamemode spectator @s

# Summon invisible item_display as camera vehicle (spectator will ride it for locked third-person view)
summon minecraft:item_display ~ ~ ~ {Tags:["mgs.downed_cam","mgs.downed_cam_new","mgs.gm_entity"],teleport_duration:1}

# Copy downed_id to camera entity for unique identification
scoreboard players operation @n[tag=mgs.downed_cam_new] mgs.zb.downed_id = @s mgs.zb.downed_id

# Teleport camera to mannequin position (will be offset each tick)
execute as @n[tag=mgs.downed_mannequin] at @s run tp @n[tag=mgs.downed_cam_new] ^ ^2 ^-3
tag @e[tag=mgs.downed_cam_new] remove mgs.downed_cam_new

# Mount the spectator player into the camera entity (locks them in place)
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute as @e[tag=mgs.downed_cam,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run tag @s add mgs.downed_mine_temp
ride @s mount @n[tag=mgs.downed_mine_temp]
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp

# Announce
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.you_are_down_a_teammate_can_revive_you","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"red"},[{"text":" ","color":"gray"}, {"translate":"mgs.is_down"}]]

