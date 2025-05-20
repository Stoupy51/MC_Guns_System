
#> stoupgun:v5.0.0/load/valid_dependencies
#
# @within	stoupgun:v5.0.0/load/secondary
#			stoupgun:v5.0.0/load/valid_dependencies 1t replace
#

# Waiting for a player to get the game version, but stop function if no player found
execute unless entity @p run schedule function stoupgun:v5.0.0/load/valid_dependencies 1t replace
execute unless entity @p run return 0
execute store result score #game_version stoupgun.data run data get entity @p DataVersion

# Check if the game version is supported
scoreboard players set #mcload_error stoupgun.data 0
execute unless score #game_version stoupgun.data matches 4429.. run scoreboard players set #mcload_error stoupgun.data 1

# Decode errors
execute if score #mcload_error stoupgun.data matches 1 run tellraw @a {"translate":"stoupgun_error_this_version_is_made_for_minecraft_25w21a","color":"red"}
execute if score #dependency_error stoupgun.data matches 1 run tellraw @a {"translate":"stoupgun_error_libraries_are_missingplease_download_the_right_st","color":"red"}
execute if score #dependency_error stoupgun.data matches 1 unless score $bs.block.major load.status matches 3.. run tellraw @a {"translate":"stoupgun.bookshelf_block_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 if score $bs.block.major load.status matches 3 unless score $bs.block.minor load.status matches 0.. run tellraw @a {"translate":"stoupgun.bookshelf_block_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 if score $bs.block.major load.status matches 3 if score $bs.block.minor load.status matches 0 unless score $bs.block.patch load.status matches 2.. run tellraw @a {"translate":"stoupgun.bookshelf_block_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 unless score $bs.math.major load.status matches 3.. run tellraw @a {"translate":"stoupgun.bookshelf_math_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 if score $bs.math.major load.status matches 3 unless score $bs.math.minor load.status matches 0.. run tellraw @a {"translate":"stoupgun.bookshelf_math_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 if score $bs.math.major load.status matches 3 if score $bs.math.minor load.status matches 0 unless score $bs.math.patch load.status matches 2.. run tellraw @a {"translate":"stoupgun.bookshelf_math_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 unless score $bs.position.major load.status matches 3.. run tellraw @a {"translate":"stoupgun.bookshelf_position_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 if score $bs.position.major load.status matches 3 unless score $bs.position.minor load.status matches 0.. run tellraw @a {"translate":"stoupgun.bookshelf_position_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 if score $bs.position.major load.status matches 3 if score $bs.position.minor load.status matches 0 unless score $bs.position.patch load.status matches 2.. run tellraw @a {"translate":"stoupgun.bookshelf_position_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 unless score $bs.random.major load.status matches 3.. run tellraw @a {"translate":"stoupgun.bookshelf_random_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 if score $bs.random.major load.status matches 3 unless score $bs.random.minor load.status matches 0.. run tellraw @a {"translate":"stoupgun.bookshelf_random_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 if score $bs.random.major load.status matches 3 if score $bs.random.minor load.status matches 0 unless score $bs.random.patch load.status matches 2.. run tellraw @a {"translate":"stoupgun.bookshelf_random_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 unless score $bs.raycast.major load.status matches 3.. run tellraw @a {"translate":"stoupgun.bookshelf_raycast_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 if score $bs.raycast.major load.status matches 3 unless score $bs.raycast.minor load.status matches 0.. run tellraw @a {"translate":"stoupgun.bookshelf_raycast_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}
execute if score #dependency_error stoupgun.data matches 1 if score $bs.raycast.major load.status matches 3 if score $bs.raycast.minor load.status matches 0 unless score $bs.raycast.patch load.status matches 2.. run tellraw @a {"translate":"stoupgun.bookshelf_raycast_v3_0_2","color":"gold","click_event":{"action":"open_url","url":"https://github.com/mcbookshelf/bookshelf/releases"}}

# Load StoupGun
execute if score #game_version stoupgun.data matches 1.. if score #mcload_error stoupgun.data matches 0 if score #dependency_error stoupgun.data matches 0 run function stoupgun:v5.0.0/load/confirm_load

