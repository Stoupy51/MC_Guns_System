""" Going down: spawning the mannequin, its name HUD and the teleport macros. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from .shared import BLEED_OUT_TICKS, HUD_OFFSET_Y_THOUSANDTHS


# Functions
def write_going_down() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# On Down: called from on_respawn when player dies in zombies
	write_versioned_function("zombies/revive/on_down", f"""
# Dying Wish (highest priority): if owned and off cooldown, cheat death with a berserk instead of
# going down. Returns before any downed state is set. Must stay ABOVE the Who's Who branch.
execute if score @s {ns}.zb.perk.dying_wish matches 1 if score @s {ns}.zb.dw_cd matches ..0 run return run function {ns}:v{version}/zombies/perks/dying_wish_trigger

# A doppelganger going down again forfeits their unrevived body first (BO2 rule): the body and its
# inventory snapshot are silently discarded, then this down proceeds (as a normal down — or as a
# fresh Who's Who if the perk was rebought meanwhile)
execute if entity @s[tag={ns}.ww_active] run function {ns}:v{version}/zombies/whos_who/forfeit

# Who's Who: keep playing as a doppelganger with a pistol instead of entering the downed state; the
# body drops as a revivable mannequin anyone (including the owner) can revive. Works solo AND co-op.
# Because this sits above the normal-down path (where solo Quick Revive's auto-revive lives), owning
# Who's Who takes priority over Quick Revive in solo. Above Tombstone.
execute if score @s {ns}.zb.perk.whos_who matches 1 run return run function {ns}:v{version}/zombies/whos_who/on_down

# Mark player as downed
scoreboard players set @s {ns}.zb.downed 1
scoreboard players set @s {ns}.zb.bleed {BLEED_OUT_TICKS}
scoreboard players set @s {ns}.zb.revive_p 0
tag @s add {ns}.downed_spectator

# Reset death counter (already set 0 by on_respawn caller, but be safe)
scoreboard players set @s {ns}.mp.death_count 0

# Assign a unique downed ID and drop the revivable body (mannequin + name HUD) at the death spot
scoreboard players add #downed_id_next {ns}.data 1
scoreboard players operation @s {ns}.zb.downed_id = #downed_id_next {ns}.data
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/revive/spawn_downed_body

# Electric Cherry: discharge a full-strength shock at the down spot (BO behavior), before the
# perk is stripped. used==cap==1 makes it the maximum-size discharge.
scoreboard players set #ec_used {ns}.data 1
scoreboard players set #ec_cap {ns}.data 1
execute if score @s {ns}.special.electric_cherry matches 1 at @s run function {ns}:v{version}/zombies/perks/electric_cherry_shock

# Tombstone: spawn a recovery marker at the death spot (snapshots the owner's perks HERE, before
# they are stripped). No-op solo or when unowned. Only reached on the normal-down path (Who's Who,
# which returns earlier, takes priority so a marker never spawns for a doppelganger).
execute if score @s {ns}.zb.perk.tombstone matches 1 run function {ns}:v{version}/zombies/perks/tombstone_on_down

# Solo Quick Revive: snapshot ownership HERE, one line before lose_all strips the perk.
# full_death can read the live tag because it decides in the same function; the normal-down auto-revive
# cannot — it runs from downed_tick a tick later, by which point lose_all has already removed
# {ns}.perk.quick_revive. That check therefore always failed, downed_tick fell through to its
# "nobody can revive this player" instant bleed-out, and a solo game ended the moment the player
# went down. Recomputed on every down, so a stale arm can never leak into a later one.
tag @s remove {ns}.zb_qr_armed
execute if entity @s[tag={ns}.perk.quick_revive] run tag @s add {ns}.zb_qr_armed

# Remove all perks when going down
function {ns}:v{version}/zombies/perks/lose_all

# Player enters spectator mode
gamemode spectator @s

# Summon invisible item_display as camera vehicle (spectator will ride it for locked third-person view)
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.downed_cam","{ns}.downed_cam_new","{ns}.gm_entity"],teleport_duration:1}}

# Copy downed_id to camera entity for unique identification
scoreboard players operation @n[tag={ns}.downed_cam_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id

# Teleport camera to THIS player's mannequin (id-matched: with Who's Who bodies around, "nearest
# mannequin" could be someone else's), will be offset each tick
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run tp @n[tag={ns}.downed_cam_new] ^ ^2 ^-3
tag @e[tag={ns}.downed_cam_new] remove {ns}.downed_cam_new

# Mount the spectator player into the camera entity (locks them in place)
execute as @e[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tag @s add {ns}.downed_mine_temp
ride @s mount @n[tag={ns}.downed_mine_temp]
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

# Announce
title @s title ["☠"]
title @s subtitle [{{"text":"You are down! A teammate can revive you.","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"red"}},{{"text":" is down!","color":"gray"}}]
""")

	## Spawn the revivable body for @s: a mannequin wearing their armor + skin, with the name HUD above it.
	## Shared by the normal down AND Who's Who — the body is the exact same entity kind either way (same tags, same visuals, same revive interactions).
	## Position defaults to @s's LastDeathLocation, but a caller may pre-set {ns}:temp _body_at (a [x,y,z] pos list) to override it — used by the void/out-of-bounds revive, where the death spot is unusable so the body drops at a safe spawn instead.
	## Requires @s {ns}.zb.downed_id already set to a fresh id; leaves the body position in storage temp rv_x/rv_y/rv_z for the caller.
	write_versioned_function("zombies/revive/spawn_downed_body", f"""
# Body position: an explicit {ns}:temp _body_at overrides the default LastDeathLocation
execute unless data storage {ns}:temp _body_at run data modify storage {ns}:temp _body_at set from entity @s LastDeathLocation.pos

# Read the position at full float precision (multiply by 1000, store as double 0.001)
execute store result score #rv_y_raw {ns}.data run data get storage {ns}:temp _body_at[1] 1000
scoreboard players add #rv_y_raw {ns}.data {HUD_OFFSET_Y_THOUSANDTHS}
execute store result storage {ns}:temp rv_x double 0.001 run data get storage {ns}:temp _body_at[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get storage {ns}:temp _body_at[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get storage {ns}:temp _body_at[2] 1000
execute store result storage {ns}:temp rv_y_hud double 0.001 run scoreboard players get #rv_y_raw {ns}.data
data remove storage {ns}:temp _body_at

# Summon mannequin (crouching pose, invulnerable, temp tag for targeting)
summon minecraft:mannequin ~ ~.5 ~ {{Invulnerable:1b,pose:"swimming",hide_description:true,Tags:["{ns}.downed_mannequin","{ns}.downed_new","{ns}.gm_entity"]}}

# Copy the player's downed_id to the mannequin so we can find it uniquely later
scoreboard players operation @n[tag={ns}.downed_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id

# Copy player armor to mannequin
data modify entity @n[tag={ns}.downed_new] equipment set from entity @s equipment

# Copy player head item (which contains the profile component) to get their skin
# Use the get_username loot table to generate a player_head with profile, then copy profile from it
loot replace entity @n[tag={ns}.downed_new] weapon.mainhand loot {ns}:get_username
data modify entity @n[tag={ns}.downed_new] profile set from entity @n[tag={ns}.downed_new] equipment.mainhand.components."minecraft:profile"

# Capture the owner's literal name for the HUD before clearing the hand. A "nearest downed
# spectator" selector must never be used for the name: on_down runs at the shared respawn
# point, so same-tick batch downs all resolve the selector to the same tied player
data modify storage {ns}:temp rv_name set from entity @n[tag={ns}.downed_new] equipment.mainhand.components."minecraft:profile".name
execute unless data storage {ns}:temp rv_name run data modify storage {ns}:temp rv_name set value "???"
item replace entity @n[tag={ns}.downed_new] weapon.mainhand with minecraft:air

# Summon text_display HUD above mannequin (temp tag, teleported below; name set right after via macro)
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.downed_hud","{ns}.downed_hud_new","{ns}.gm_entity"],billboard:"vertical",shadow:1b,see_through:0b,teleport_duration:1,transformation:{{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},text:[{{"text":"...","color":"yellow"}},{{"text":" ↓","color":"yellow"}}]}}
function {ns}:v{version}/zombies/revive/set_hud_name with storage {ns}:temp

# Copy the player's downed_id to the HUD so it can be id-matched (never "nearest") later
scoreboard players operation @n[tag={ns}.downed_hud_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id

# Teleport mannequin and HUD to death location
function {ns}:v{version}/zombies/revive/tp_to_death with storage {ns}:temp

# Remove temp tags so future queries don't accidentally match
tag @e[tag={ns}.downed_new] remove {ns}.downed_new
tag @e[tag={ns}.downed_hud_new] remove {ns}.downed_hud_new
""")

	## Macro: write the owner's literal name into the freshly summoned HUD (player names are [A-Za-z0-9_])
	write_versioned_function("zombies/revive/set_hud_name", f"""
$data modify entity @n[tag={ns}.downed_hud_new] text set value [{{"text":"$(rv_name)","color":"yellow"}},{{"text":" ↓","color":"yellow"}}]
""")

	## Macro: teleport mannequin and HUD to death location
	write_versioned_function("zombies/revive/tp_to_death", f"""
$tp @n[tag={ns}.downed_new] $(rv_x) $(rv_y) $(rv_z)
$tp @n[tag={ns}.downed_hud_new] $(rv_x) $(rv_y_hud) $(rv_z)
""")

	## Macro: teleport revived player to the mannequin's last position
	write_versioned_function("zombies/revive/tp_revive_pos", """
$tp @s $(rv_x) $(rv_y) $(rv_z)
""")

