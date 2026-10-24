
#> mgs:v5.2.0/zombies/powerups/spawn_display
#
# @executed	at @s
#
# @within	mgs:v5.2.0/zombies/max_ammo_at_self with storage mgs:temp _pu_spawn
#			mgs:v5.2.0/zombies/powerups/do_spawn_random with storage mgs:temp _pu_spawn
#			mgs:v5.2.0/zombies/powerups/intercept_item with storage mgs:temp _pu_spawn
#
# @args		x (int)
#			y (int)
#			z (int)
#			uid (int)
#

$execute if data storage mgs:temp _pu_spawn{"type":"max_ammo"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:amethyst_shard",type_num:1,label:'{"translate":"mgs.max_ammo","fallback":"Max Ammo","color":"aqua","bold":true}'}
$execute if data storage mgs:temp _pu_spawn{"type":"insta_kill"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:fermented_spider_eye",type_num:2,label:'{"translate":"mgs.insta_kill","fallback":"Insta Kill","color":"red","bold":true}'}
$execute if data storage mgs:temp _pu_spawn{"type":"double_points"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:gold_ingot",type_num:3,label:'{"translate":"mgs.double_points","fallback":"Double Points","color":"yellow","bold":true}'}
$execute if data storage mgs:temp _pu_spawn{"type":"carpenter"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:oak_log",type_num:4,label:'{"translate":"mgs.carpenter","fallback":"Carpenter","color":"gold","bold":true}'}
$execute if data storage mgs:temp _pu_spawn{"type":"nuke"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:tnt",type_num:5,label:'{"translate":"mgs.nuke","fallback":"Nuke","color":"red","bold":true}'}
$execute if data storage mgs:temp _pu_spawn{"type":"unlimited_ammo"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:blaze_rod",type_num:6,label:'{"translate":"mgs.unlimited_ammo","fallback":"Unlimited Ammo","color":"green","bold":true}'}
$execute if data storage mgs:temp _pu_spawn{"type":"random_perk"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:glass_bottle",type_num:7,label:'{"translate":"mgs.random_perk","fallback":"Random Perk","color":"light_purple","bold":true}'}
$execute if data storage mgs:temp _pu_spawn{"type":"free_pap"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:diamond",type_num:8,label:'{"translate":"mgs.free_pap","fallback":"Free PAP","color":"aqua","bold":true}'}
$execute if data storage mgs:temp _pu_spawn{"type":"cash_drop"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:emerald",type_num:9,label:'{"translate":"mgs.cash_drop","fallback":"Cash Drop","color":"green","bold":true}'}
$execute if data storage mgs:temp _pu_spawn{"type":"fire_sale"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:firework_star",type_num:10,label:'{"translate":"mgs.fire_sale","fallback":"Fire Sale","color":"light_purple","bold":true}'}
$execute if data storage mgs:temp _pu_spawn{"type":"bonfire_sale"} run function mgs:v5.2.0/zombies/powerups/spawn_type {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:campfire",type_num:11,label:'{"translate":"mgs.bonfire_sale","fallback":"Bonfire Sale","color":"gold","bold":true}'}

