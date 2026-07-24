
#> mgs:v5.1.0/zombies/revive/do_round_respawn
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=spectator]
#
# @within	mgs:v5.1.0/zombies/revive/round_respawn [ as @a[scores={mgs.zb.in_game=1},gamemode=spectator] ]
#

# If this player was still DOWNED (mannequin alive) when the round ended, fully tear that state
# down first — otherwise their mannequin/HUD/camera would be orphaned and they'd stay "downed".
execute if entity @s[tag=mgs.downed_spectator] run function mgs:v5.1.0/zombies/revive/clear_downed_state

# Restore adventure mode
spectate @s
gamemode adventure @s

# Teleport to a player spawn near a random alive teammate
function mgs:v5.1.0/zombies/revive/respawn_near_player

# Heal and reset stamina to full (the stamina system owns the hunger bar)
scoreboard players set @s mgs.stam_seen 0
effect give @s minecraft:instant_health 1 255 true

# Restore max health (check for Juggernog perk)
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Re-give starting weapon on respawn
function mgs:v5.1.0/zombies/inventory/give_respawn_loadout

# Tombstone: if this player bled out with a Tombstone marker, activate it + start the 60s recovery timer
function mgs:v5.1.0/zombies/perks/tombstone_on_respawn

# Call map respawn script (executed as the respawning player)
function mgs:v5.1.0/shared/maps/call_script_at_base {script:"respawn"}

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"green"},[{"text":" ","color":"gray"}, {"translate":"mgs.has_respawned"}]]

