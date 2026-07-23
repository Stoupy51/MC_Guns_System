
#> mgs:v5.1.0/zombies/whos_who/on_down
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/revive/on_down
#			mgs:v5.1.0/zombies/revive/void_revive_whos_who
#

# Snapshot perks + inventory (for recovery on revive) — BEFORE anything is stripped
scoreboard players operation @s mgs.zb.wwp.juggernog = @s mgs.zb.perk.juggernog
scoreboard players operation @s mgs.zb.wwp.speed_cola = @s mgs.zb.perk.speed_cola
scoreboard players operation @s mgs.zb.wwp.double_tap = @s mgs.zb.perk.double_tap
execute store success score @s mgs.zb.wwp.quick_revive if entity @s[tag=mgs.perk.quick_revive]
scoreboard players operation @s mgs.zb.wwp.mule_kick = @s mgs.zb.perk.mule_kick
scoreboard players operation @s mgs.zb.wwp.stamin_up = @s mgs.zb.perk.stamin_up
scoreboard players operation @s mgs.zb.wwp.phd_flopper = @s mgs.zb.perk.phd_flopper
scoreboard players operation @s mgs.zb.wwp.deadshot = @s mgs.zb.perk.deadshot
scoreboard players operation @s mgs.zb.wwp.timeslip = @s mgs.zb.perk.timeslip
scoreboard players operation @s mgs.zb.wwp.electric_cherry = @s mgs.zb.perk.electric_cherry
scoreboard players operation @s mgs.zb.wwp.tombstone = @s mgs.zb.perk.tombstone
scoreboard players operation @s mgs.zb.wwp.whos_who = @s mgs.zb.perk.whos_who
scoreboard players operation @s mgs.zb.wwp.dying_wish = @s mgs.zb.perk.dying_wish
scoreboard players operation @s mgs.zb.wwp.widows_wine = @s mgs.zb.perk.widows_wine

# Fresh body id, kept in zb.ww.id: a later normal down assigns a new zb.downed_id, and the body
# link must survive that (this used to orphan the mannequin)
scoreboard players add #downed_id_next mgs.data 1
scoreboard players operation @s mgs.zb.downed_id = #downed_id_next mgs.data
scoreboard players operation @s mgs.zb.ww.id = #downed_id_next mgs.data
execute store result storage mgs:temp _ww_id.id int 1 run scoreboard players get @s mgs.zb.ww.id
function mgs:v5.1.0/zombies/whos_who/snapshot_inv with storage mgs:temp _ww_id

# Drop the body at the death spot: the EXACT same revivable mannequin + HUD as a normal down
# (same tags, same visuals, same revive interactions)
function mgs:v5.1.0/zombies/revive/spawn_downed_body

# Strip perks (the doppelganger starts fresh)
function mgs:v5.1.0/zombies/perks/lose_all

# Doppelganger loadout: wipe everything and hand back only the starting knife + pistol kit
clear @s
gamemode adventure @s
function mgs:v5.1.0/zombies/inventory/give_respawn_loadout

# Respawn the doppelganger at the unlocked player spawn nearest to the body but at least 10 blocks
# away from it (falls back to the nearest one at all if none is that far)
tag @s add mgs.spawn_pending
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.ww.id
scoreboard players set #has_candidate mgs.data 0
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s store success score #has_candidate mgs.data run tag @n[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked,distance=10..] add mgs.spawn_candidate
execute if score #has_candidate mgs.data matches 0 as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run tag @n[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked] add mgs.spawn_candidate
execute as @n[tag=mgs.spawn_candidate] run function mgs:v5.1.0/zombies/tp_to_spawn
tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
tag @a[tag=mgs.spawn_pending] remove mgs.spawn_pending

# Enter doppelganger state (the shared revive core reads zb.bleed / zb.revive_p on the owner)
tag @s add mgs.ww_active
scoreboard players set @s mgs.zb.bleed 1200
scoreboard players set @s mgs.zb.revive_p 0

# Announce
title @s times 5 40 15
title @s title ["👥"]
title @s subtitle [{"translate":"mgs.whos_who_revive_your_body_or_fight_on","color":"dark_aqua"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"aqua"},{"translate":"mgs.went_down_but_plays_on_as_a_doppelganger","color":"gray"}]

