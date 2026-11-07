
#> mgs:v5.4.0/multiplayer/custom/set_default
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/player/config/process
#

# The trigger value carries the loadout id.
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 60000

scoreboard players operation @s mgs.mp.default = #loadout_id mgs.data

tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.default_loadout_set_it_will_auto_apply_when_a_game_starts","fallback":"Default loadout set! It will auto-apply when a game starts","color":"green"}]

