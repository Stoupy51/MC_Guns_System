
#> mgs:v5.0.0/load/valid_dependencies
#
# @within	mgs:v5.0.0/load/secondary
#			mgs:v5.0.0/load/valid_dependencies 1t replace [ scheduled ]
#

# Waiting for a player to get the game version, but stop function if no player found
execute unless entity @p run schedule function mgs:v5.0.0/load/valid_dependencies 1t replace
execute unless entity @p run return 0
execute store result score #game_version mgs.data run data get entity @p DataVersion

# Check if the game version is supported
scoreboard players set #mcload_error mgs.data 0
execute unless score #game_version mgs.data matches 4669.. run scoreboard players set #mcload_error mgs.data 1

# Decode errors
execute if score #mcload_error mgs.data matches 1 run tellraw @a {"translate": "mgs.mc_guns_system_error_this_version_is_made_for_minecraft_1_21_11","color":"red"}
execute if score #dependency_error mgs.data matches 1 run tellraw @a {"translate": "mgs.mc_guns_system_error_libraries_are_missingplease_download_the_ri","color":"red"}
execute if score #dependency_error mgs.data matches 1 unless score $bs.block.major load.status matches 3.. run tellraw @a {"translate": "mgs.bookshelf_block_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.block.major load.status matches 3 unless score $bs.block.minor load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_block_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.block.major load.status matches 3 if score $bs.block.minor load.status matches 2 unless score $bs.block.patch load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_block_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 unless score $bs.hitbox.major load.status matches 3.. run tellraw @a {"translate": "mgs.bookshelf_hitbox_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.hitbox.major load.status matches 3 unless score $bs.hitbox.minor load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_hitbox_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.hitbox.major load.status matches 3 if score $bs.hitbox.minor load.status matches 2 unless score $bs.hitbox.patch load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_hitbox_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 unless score $bs.math.major load.status matches 3.. run tellraw @a {"translate": "mgs.bookshelf_math_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.math.major load.status matches 3 unless score $bs.math.minor load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_math_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.math.major load.status matches 3 if score $bs.math.minor load.status matches 2 unless score $bs.math.patch load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_math_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 unless score $bs.position.major load.status matches 3.. run tellraw @a {"translate": "mgs.bookshelf_position_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.position.major load.status matches 3 unless score $bs.position.minor load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_position_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.position.major load.status matches 3 if score $bs.position.minor load.status matches 2 unless score $bs.position.patch load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_position_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 unless score $bs.random.major load.status matches 3.. run tellraw @a {"translate": "mgs.bookshelf_random_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.random.major load.status matches 3 unless score $bs.random.minor load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_random_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.random.major load.status matches 3 if score $bs.random.minor load.status matches 2 unless score $bs.random.patch load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_random_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 unless score $bs.raycast.major load.status matches 3.. run tellraw @a {"translate": "mgs.bookshelf_raycast_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.raycast.major load.status matches 3 unless score $bs.raycast.minor load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_raycast_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error mgs.data matches 1 if score $bs.raycast.major load.status matches 3 if score $bs.raycast.minor load.status matches 2 unless score $bs.raycast.patch load.status matches 2.. run tellraw @a {"translate": "mgs.bookshelf_raycast_v3_2_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}

# Load MC Guns System
execute if score #game_version mgs.data matches 1.. if score #mcload_error mgs.data matches 0 if score #dependency_error mgs.data matches 0 run function mgs:v5.0.0/load/confirm_load

