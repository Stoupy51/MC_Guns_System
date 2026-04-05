
#> mgs:v5.0.0/shared/load_base_coordinates
#
# @within	mgs:v5.0.0/shared/summon_oob {mode:"$(mode)"}
#			mgs:v5.0.0/zombies/start {mode:"zombies"}
#			mgs:v5.0.0/multiplayer/start {mode:"multiplayer"}
#			mgs:v5.0.0/multiplayer/gamemodes/dom/setup {mode:"multiplayer"}
#			mgs:v5.0.0/multiplayer/gamemodes/hp/setup {mode:"multiplayer"}
#			mgs:v5.0.0/multiplayer/gamemodes/snd/setup {mode:"multiplayer"}
#			mgs:v5.0.0/missions/start {mode:"missions"}
#
# @args		mode (string)
#

$execute store result score #gm_base_x mgs.data run data get storage mgs:$(mode) game.map.base_coordinates[0]
$execute store result score #gm_base_y mgs.data run data get storage mgs:$(mode) game.map.base_coordinates[1]
$execute store result score #gm_base_z mgs.data run data get storage mgs:$(mode) game.map.base_coordinates[2]

