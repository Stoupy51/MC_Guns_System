
#> mgs:v5.1.0/zombies/revive/spawn_downed_body
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/on_down
#			mgs:v5.1.0/zombies/revive/on_down
#

# Body position: an explicit mgs:temp _body_at overrides the default LastDeathLocation
execute unless data storage mgs:temp _body_at run data modify storage mgs:temp _body_at set from entity @s LastDeathLocation.pos

# Read the position at full float precision (multiply by 1000, store as double 0.001)
execute store result score #rv_y_raw mgs.data run data get storage mgs:temp _body_at[1] 1000
scoreboard players add #rv_y_raw mgs.data 2000
execute store result storage mgs:temp rv_x double 0.001 run data get storage mgs:temp _body_at[0] 1000
execute store result storage mgs:temp rv_y double 0.001 run data get storage mgs:temp _body_at[1] 1000
execute store result storage mgs:temp rv_z double 0.001 run data get storage mgs:temp _body_at[2] 1000
execute store result storage mgs:temp rv_y_hud double 0.001 run scoreboard players get #rv_y_raw mgs.data
data remove storage mgs:temp _body_at

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

