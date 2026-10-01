
#> mgs:v5.1.0/zombies/revive/do_round_respawn
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=spectator]
#
# @within	mgs:v5.1.0/zombies/revive/round_respawn [ as @a[scores={mgs.zb.in_game=1},gamemode=spectator] ]
#

# Still downed: tear that state down, or the mannequin, HUD and camera would be orphaned.
execute if entity @s[tag=mgs.downed_spectator] run function mgs:v5.1.0/zombies/revive/clear_downed_state

spectate @s
gamemode adventure @s

function mgs:v5.1.0/zombies/revive/respawn_near_player

# The stamina system owns the hunger bar.
scoreboard players set @s mgs.stam_seen 0
effect give @s minecraft:instant_health 1 255 true

execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

function mgs:v5.1.0/zombies/inventory/give_respawn_loadout

# Tombstone: activate the marker and its 60 s recovery timer.
function mgs:v5.1.0/zombies/perks/tombstone_on_respawn

# Run as the respawning player.
function mgs:v5.1.0/shared/maps/call_script_at_base {script:"respawn"}

tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"green"}],[{"text":" ","color":"gray"}, {"translate":"mgs.has_respawned"}]]

