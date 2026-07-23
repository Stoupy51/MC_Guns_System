
#> mgs:v5.1.0/zombies/revive/on_down
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/on_respawn
#

# Dying Wish (highest priority): if owned and off cooldown, cheat death with a berserk instead of
# going down. Returns before any downed state is set. Must stay ABOVE the Who's Who branch.
execute if score @s mgs.zb.perk.dying_wish matches 1 if score @s mgs.zb.dw_cd matches ..0 run return run function mgs:v5.1.0/zombies/perks/dying_wish_trigger

# A doppelganger going down again forfeits their unrevived body first (BO2 rule): the body and its
# inventory snapshot are silently discarded, then this down proceeds (as a normal down — or as a
# fresh Who's Who if the perk was rebought meanwhile)
execute if entity @s[tag=mgs.ww_active] run function mgs:v5.1.0/zombies/whos_who/forfeit

# Who's Who: keep playing as a doppelganger with a pistol instead of entering the downed state; the
# body drops as a revivable mannequin anyone (including the owner) can revive. Works solo AND co-op.
# Because this sits above the normal-down path (where solo Quick Revive's auto-revive lives), owning
# Who's Who takes priority over Quick Revive in solo. Above Tombstone.
execute if score @s mgs.zb.perk.whos_who matches 1 run return run function mgs:v5.1.0/zombies/whos_who/on_down

# Mark player as downed
scoreboard players set @s mgs.zb.downed 1
scoreboard players set @s mgs.zb.bleed 1200
scoreboard players set @s mgs.zb.revive_p 0
tag @s add mgs.downed_spectator

# Reset death counter (already set 0 by on_respawn caller, but be safe)
scoreboard players set @s mgs.mp.death_count 0

# Assign a unique downed ID and drop the revivable body (mannequin + name HUD) at the death spot
scoreboard players add #downed_id_next mgs.data 1
scoreboard players operation @s mgs.zb.downed_id = #downed_id_next mgs.data
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
function mgs:v5.1.0/zombies/revive/spawn_downed_body

# Electric Cherry: discharge a full-strength shock at the down spot (BO behavior), before the
# perk is stripped. used==cap==1 makes it the maximum-size discharge.
scoreboard players set #ec_used mgs.data 1
scoreboard players set #ec_cap mgs.data 1
execute if score @s mgs.special.electric_cherry matches 1 at @s run function mgs:v5.1.0/zombies/perks/electric_cherry_shock

# Tombstone: spawn a recovery marker at the death spot (snapshots the owner's perks HERE, before
# they are stripped). No-op solo or when unowned. Only reached on the normal-down path (Who's Who,
# which returns earlier, takes priority so a marker never spawns for a doppelganger).
execute if score @s mgs.zb.perk.tombstone matches 1 run function mgs:v5.1.0/zombies/perks/tombstone_on_down

# Remove all perks when going down
function mgs:v5.1.0/zombies/perks/lose_all

# Player enters spectator mode
gamemode spectator @s

# Summon invisible item_display as camera vehicle (spectator will ride it for locked third-person view)
summon minecraft:item_display ~ ~ ~ {Tags:["mgs.downed_cam","mgs.downed_cam_new","mgs.gm_entity"],teleport_duration:1}

# Copy downed_id to camera entity for unique identification
scoreboard players operation @n[tag=mgs.downed_cam_new] mgs.zb.downed_id = @s mgs.zb.downed_id

# Teleport camera to THIS player's mannequin (id-matched: with Who's Who bodies around, "nearest
# mannequin" could be someone else's), will be offset each tick
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run tp @n[tag=mgs.downed_cam_new] ^ ^2 ^-3
tag @e[tag=mgs.downed_cam_new] remove mgs.downed_cam_new

# Mount the spectator player into the camera entity (locks them in place)
execute as @e[tag=mgs.downed_cam,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run tag @s add mgs.downed_mine_temp
ride @s mount @n[tag=mgs.downed_mine_temp]
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp

# Announce
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.you_are_down_a_teammate_can_revive_you","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"red"},[{"text":" ","color":"gray"}, {"translate":"mgs.is_down"}]]

