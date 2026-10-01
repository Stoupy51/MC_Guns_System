
#> mgs:v5.1.0/zombies/revive/spawn_downed_body
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/on_down
#			mgs:v5.1.0/zombies/revive/on_down
#

execute unless data storage mgs:temp _body_at run data modify storage mgs:temp _body_at set from entity @s LastDeathLocation.pos

# Full float precision: x1000, stored back as double 0.001.
execute store result score #rv_y_raw mgs.data run data get storage mgs:temp _body_at[1] 1000
scoreboard players add #rv_y_raw mgs.data 2000
execute store result storage mgs:temp rv_x double 0.001 run data get storage mgs:temp _body_at[0] 1000
execute store result storage mgs:temp rv_y double 0.001 run data get storage mgs:temp _body_at[1] 1000
execute store result storage mgs:temp rv_z double 0.001 run data get storage mgs:temp _body_at[2] 1000
execute store result storage mgs:temp rv_y_hud double 0.001 run scoreboard players get #rv_y_raw mgs.data
data remove storage mgs:temp _body_at

# Glowing, so the squad finds a body on the floor in a horde before it bleeds out.
summon minecraft:mannequin ~ ~1.5 ~ {Invulnerable:1b,Glowing:1b,pose:"swimming",hide_description:true,Tags:["mgs.downed_mannequin","mgs.downed_new","mgs.gm_entity"]}

scoreboard players operation @n[tag=mgs.downed_new] mgs.zb.downed_id = @s mgs.zb.downed_id

data modify entity @n[tag=mgs.downed_new] equipment set from entity @s equipment

# The get_username loot table gives a player_head with the profile, for the skin.
loot replace entity @n[tag=mgs.downed_new] weapon.mainhand loot mgs:get_username
data modify entity @n[tag=mgs.downed_new] profile set from entity @n[tag=mgs.downed_new] equipment.mainhand.components."minecraft:profile"

# Take the name from the profile: on_down runs at the shared respawn point, so a nearest-spectator
# selector would give the same player to every down of the same tick.
data modify storage mgs:temp rv_name set from entity @n[tag=mgs.downed_new] equipment.mainhand.components."minecraft:profile".name
execute unless data storage mgs:temp rv_name run data modify storage mgs:temp rv_name set value "???"
item replace entity @n[tag=mgs.downed_new] weapon.mainhand with minecraft:air

# see_through, so the name reads through walls and zombies.
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.downed_hud","mgs.downed_hud_new","mgs.gm_entity"],billboard:"vertical",shadow:1b,see_through:1b,teleport_duration:1,transformation:{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},text:[{"text":"...","color":"yellow"},{"text":" ↓","color":"yellow"}]}
function mgs:v5.1.0/zombies/revive/set_hud_name with storage mgs:temp

scoreboard players operation @n[tag=mgs.downed_hud_new] mgs.zb.downed_id = @s mgs.zb.downed_id

function mgs:v5.1.0/zombies/revive/tp_to_death with storage mgs:temp

tag @e[tag=mgs.downed_new] remove mgs.downed_new
tag @e[tag=mgs.downed_hud_new] remove mgs.downed_hud_new

