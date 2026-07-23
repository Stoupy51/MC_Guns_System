
# ruff: noqa: E501
# Revive System (Black Ops Zombies-style, mannequin-based)
# When a player takes lethal damage, they enter a "downed" state.
# A mannequin is spawned at their death location wearing their armor/skin.
# The player spectates the mannequin and can crawl (slow movement via WASD input predicates).
# Teammates revive by standing near the mannequin. After 60s without revive, player bleed out.
# Solo + Quick Revive: auto-revive after 10s, up to 3 times.
from stewbeet import JsonDict, Mem, Predicate, set_json_encoder, write_load_file, write_versioned_function

from ..helpers import MGS_TAG

# Revive configuration
BLEED_OUT_TICKS: int = 1200		# 60 seconds to be revived before bleed out
REVIVE_TICKS: int = 60			# 3 seconds of proximity to revive
REVIVE_RANGE: float = 2.5		# Blocks range for revive interaction
QUICK_REVIVE_TICKS: int = 30	# 1.5 seconds with Quick Revive perk
SOLO_QR_TICKS: int = 200		# 10 seconds for solo Quick Revive auto-revive
SOLO_QR_MAX: int = 3			# Total solo self-revives allowed per game; each use requires rebuying QR
CRAWL_SPEED: float = 0.06		# Blocks per tick for downed crawl movement
# HUD text display height above mannequin
HUD_OFFSET_Y_THOUSANDTHS: int = 2000  # 2.0 blocks * 1000 (for scoreboard math)


def revive_body_detect() -> str:
	"""Shared per-tick upkeep for one revivable body (normal down AND Who's Who).

	Emitted into the caller's tick function. Contract: @s = the downed-state holder (a spectating
	downed player, or an alive Who's Who doppelganger) carrying `zb.bleed`/`zb.revive_p`, with
	#my_downed_id already set to the body's downed_id. Decrements the bleed timer and detects
	revivers around the id-matched mannequin into #zb_reviving. The reviver selector excludes
	downed/spectating players but includes doppelgangers — and for a Who's Who body, the owner
	themselves (self-revive).
	"""
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	return f"""
# ── Shared body upkeep (revive.py::revive_body_detect) ──
# Decrement bleed timer (real-time via #tick_delta)
scoreboard players operation @s {ns}.zb.bleed -= #tick_delta {ns}.data

# Check for revivers: alive non-downed players within range of THIS body (id-matched, since with
# several bodies 'nearest mannequin' could be someone else's)
scoreboard players set #zb_reviving {ns}.data 0
execute as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE}] run scoreboard players set #zb_reviving {ns}.data 1
""".strip()


def revive_body_progress(complete_function: str) -> str:
	"""Shared revive progress for one revivable body: progress/decay on `zb.revive_p`, the reviver
	progress bar, HUD recolor by urgency, and the (Quick Revive-aware) completion thresholds.

	Same contract as revive_body_detect (which must be emitted above this block). On completion the
	block `return run`s `complete_function`, so the caller's lines below (bleed-out checks) are
	skipped on the revive tick.
	"""
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	return f"""
# ── Shared revive progress (revive.py::revive_body_progress) ──
# If someone is reviving (=1), increment progress; if solo QR (=2), skip (solo_qr_tick handles it);
# if none (=0), decay at double speed. Real-time via #tick_delta.
execute if score #zb_reviving {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.revive_p += #tick_delta {ns}.data
scoreboard players operation #rv_decay {ns}.data = #tick_delta {ns}.data
scoreboard players operation #rv_decay {ns}.data *= #2 {ns}.data
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.revive_p matches 1.. run scoreboard players operation @s {ns}.zb.revive_p -= #rv_decay {ns}.data

# Show the revive progress bar to the revivers (snapshot @s's progress first: a reviver cannot
# reliably re-select the downed player, see show_reviver_bar)
scoreboard players operation #rv_reviver_disp {ns}.data = @s {ns}.zb.revive_p
execute if score #zb_reviving {ns}.data matches 1 as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE}] run function {ns}:v{version}/zombies/revive/show_reviver_bar

# Update HUD text_display color based on revive state / bleed timer
execute if score #zb_reviving {ns}.data matches 1.. run function {ns}:v{version}/zombies/revive/hud_white
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.bleed matches 400.. run function {ns}:v{version}/zombies/revive/hud_yellow
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.bleed matches 200..399 run function {ns}:v{version}/zombies/revive/hud_gold
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.bleed matches ..199 run function {ns}:v{version}/zombies/revive/hud_red

# Revive complete (faster threshold if a reviver AT THE BODY has Quick Revive). return run: the
# caller's bleed-out checks below must not run on the completion tick (zb.bleed was reset to 0)
execute if score #zb_reviving {ns}.data matches 1 run scoreboard players set #rv_qr_near {ns}.data 0
execute if score #zb_reviving {ns}.data matches 1 as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE},tag={ns}.perk.quick_revive] run scoreboard players set #rv_qr_near {ns}.data 1
execute if score #zb_reviving {ns}.data matches 1 if score #rv_qr_near {ns}.data matches 1 if score @s {ns}.zb.revive_p matches {QUICK_REVIVE_TICKS}.. run return run function {complete_function}
execute if score #zb_reviving {ns}.data matches 1 if score #rv_qr_near {ns}.data matches 0 if score @s {ns}.zb.revive_p matches {REVIVE_TICKS}.. run return run function {complete_function}
""".strip()


def generate_revive() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Input predicates (used to move the mannequin via spectator player input)
	def player_input(key: str) -> JsonDict:
		return {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"minecraft:type_specific/player": {"input": {key: True}}}}
	Mem.ctx.data[ns].predicates[f"v{version}/input/forward"]  = set_json_encoder(Predicate(player_input("forward")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/backward"] = set_json_encoder(Predicate(player_input("backward")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/left"]     = set_json_encoder(Predicate(player_input("left")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/right"]    = set_json_encoder(Predicate(player_input("right")))

	## Predicate: does `this` entity's downed_id match the downed player currently being processed?
	## Lets a selector pick the matching mannequin/cam/hud directly via predicate=... instead of
	## `as @e[tag=...] if score @s {ns}.zb.downed_id = #my_downed_id ...` — one selector pass, the
	## id test folded into selection (same trick as zombies/traps/turret_id_match).
	downed_id_ref: JsonDict = {"type": "minecraft:score", "target": {"type": "minecraft:fixed", "name": "#my_downed_id"}, "score": f"{ns}.data"}
	Mem.ctx.data[ns].predicates[f"v{version}/zombies/revive/downed_id_match"] = set_json_encoder(Predicate({
		"condition": "minecraft:entity_scores",
		"entity": "this",
		"scores": {f"{ns}.zb.downed_id": {"min": downed_id_ref, "max": downed_id_ref}},
	}), max_level=-1)
	Mem.ctx.data[ns].predicates[f"v{version}/input/any"]      = set_json_encoder(Predicate({"condition": "minecraft:any_of", "terms": [player_input("forward"), player_input("backward"), player_input("left"), player_input("right")]}))

	## Scoreboards
	write_load_file(f"""
# Revive system scoreboards
scoreboard objectives add {ns}.zb.downed dummy
scoreboard objectives add {ns}.zb.bleed dummy
scoreboard objectives add {ns}.zb.revive_p dummy

# Solo Quick Revive uses remaining
scoreboard objectives add {ns}.zb.qr_uses dummy

# Unique downed ID: links player to their specific mannequin
scoreboard objectives add {ns}.zb.downed_id dummy
""")

	# ──────────────────────────────────────────────────────────────────────────
	## On Down: called from on_respawn when player dies in zombies
	# ──────────────────────────────────────────────────────────────────────────
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

	## Spawn the revivable body for @s: a mannequin wearing their armor + skin, with the name HUD
	## above it. Shared by the normal down AND Who's Who — the body is the exact same entity kind
	## either way (same tags, same visuals, same revive interactions). Position defaults to @s's
	## LastDeathLocation, but a caller may pre-set {ns}:temp _body_at (a [x,y,z] pos list) to override
	## it — used by the void/out-of-bounds revive, where the death spot is unusable so the body drops
	## at a safe spawn instead. Requires @s {ns}.zb.downed_id already set to a fresh id; leaves the
	## body position in storage temp rv_x/rv_y/rv_z for the caller.
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

	# ──────────────────────────────────────────────────────────────────────────
	## Tick: process all downed spectating players
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/tick", f"""
# Process each spectating (downed) player
execute as @a[tag={ns}.downed_spectator,scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/revive/downed_tick
""")

	## Downed tick: per-player (run as the spectating downed player)
	write_versioned_function("zombies/revive/downed_tick", f"""
# Identify THIS player's downed entities for the id-matching predicate, then tag the mannequin ONCE
# as downed_mine_temp. Every per-mannequin command below reuses that tag (or a single dispatch into
# move_mannequin) instead of re-selecting the mannequin ~11x per tick.
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
tag @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] add {ns}.downed_mine_temp

# Read crawl inputs into scratch scores while @s is still the player (predicate self-checks on @s,
# no entity scan). These drive the mannequin's local velocity inside move_mannequin.
# Also snapshot the owner's yaw (x100): move_mannequin must not use a "nearest downed spectator"
# lookup, which binds to the wrong owner when several mannequins are close together.
execute store result score #rv_yaw {ns}.data run data get entity @s Rotation[0] 100
scoreboard players set #crawl_vx {ns}.data 0
scoreboard players set #crawl_vz {ns}.data 0
execute if entity @s[predicate={ns}:v{version}/input/forward] run scoreboard players set #crawl_vz {ns}.data {int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/backward] run scoreboard players set #crawl_vz {ns}.data -{int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/left] run scoreboard players set #crawl_vx {ns}.data {int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/right] run scoreboard players set #crawl_vx {ns}.data -{int(CRAWL_SPEED * 1000)}

# Third-person camera: position the cam item_display 2 up / 3 behind the mannequin (using the
# mannequin's CURRENT rotation, i.e. before this tick's yaw sync — same order as before), then
# re-mount the player onto the cam so the view follows it.
execute at @n[tag={ns}.downed_mine_temp] as @e[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tp @s ^ ^2 ^-3
ride @s mount @n[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match]

# All remaining per-mannequin work (yaw sync, crawl motion, HUD anchor) in ONE pass over the tagged
# mannequin instead of re-selecting it for each command.
execute as @n[tag={ns}.downed_mine_temp] at @s run function {ns}:v{version}/zombies/revive/move_mannequin

# Done with the per-tick mannequin tag
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

{revive_body_detect()}

# Solo Quick Revive auto-revive: if no teammates in-game and player has quick_revive + uses left
execute if score #zb_reviving {ns}.data matches 0 if entity @s[tag={ns}.perk.quick_revive] unless score #zb_solo_revive_block {ns}.data matches 1 run function {ns}:v{version}/zombies/revive/check_solo_qr

# Show bleed timer on downed player's actionbar ONLY when not in solo QR (which has its own actionbar)
# Compute display: whole seconds and tenths digit (sec = bleed/20, tenth = (bleed%20)/2)
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_sec {ns}.data = @s {ns}.zb.bleed
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_sec {ns}.data /= #20 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data = @s {ns}.zb.bleed
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data %= #20 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data /= #2 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run data modify storage smithed.actionbar:input message set value {{json:[{{"text":"☠ Bleeding out: ","color":"red"}},{{"score":{{"name":"#rv_disp_sec","objective":"{ns}.data"}},"color":"gray"}},{{"text":".","color":"gray"}},{{"score":{{"name":"#rv_disp_tenth","objective":"{ns}.data"}},"color":"gray"}},{{"text":"s","color":"dark_gray"}}],priority:"override",freeze:2}}
execute if score #zb_reviving {ns}.data matches ..1 run function #smithed.actionbar:message

{revive_body_progress(f"{ns}:v{version}/zombies/revive/revive_complete")}

# Bleed out: time's up
execute if score @s {ns}.zb.bleed matches ..0 run function {ns}:v{version}/zombies/revive/bleed_out

# Instant bleed out: if no healthy players remain and no solo QR auto-revive is active,
# there is no hope of revive — end the suspense immediately
execute if score #zb_reviving {ns}.data matches 0 unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run function {ns}:v{version}/zombies/revive/bleed_out
""")

	## All per-mannequin downed work in one pass. @s = the downed player's mannequin, executed at it
	## (dispatched once per downed player from downed_tick after tagging the mannequin downed_mine_temp).
	## Folds the former ~11 separate `@e[tag=downed_mannequin,predicate=...]` selections into a single
	## entity selection; everything here is @s (the mannequin) or a local @p/@n lookup. Crawl direction
	## arrives via #crawl_vx/#crawl_vz (set on the player before dispatch). Order matches the old inline
	## version: yaw sync first, then velocity, then local->canonical, then motion, then HUD anchor.
	write_versioned_function("zombies/revive/move_mannequin", f"""
# Sync mannequin yaw from the owner's look direction (snapshotted into #rv_yaw x100 by downed_tick)
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #rv_yaw {ns}.data
data modify entity @s Rotation[1] set value 0.0f

# Crawl motion via Bookshelf physics. XZ from the crawl-input scratch scores (0 when no input is held);
# Y a constant downward pull so the mannequin doesn't float off ledges (set_motion overrides gravity).
scoreboard players operation @s bs.vel.x = #crawl_vx {ns}.data
scoreboard players set @s bs.vel.y -400
scoreboard players operation @s bs.vel.z = #crawl_vz {ns}.data
function #bs.move:local_to_canonical
function #bs.move:set_motion {{scale:0.001}}

# Keep the HUD text_display anchored 2 blocks above the mannequin (id-matched via #my_downed_id)
tp @n[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] ~ ~2 ~
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Solo Quick Revive check: auto-revive if alone in game
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/check_solo_qr", f"""
# Only trigger in a TRUE solo game: @s must be the only in-game player. Teammates being
# downed or bled-out does NOT make the game solo — in co-op, a downed player with Quick
# Revive must never self-revive (all players down with no reviver = game over instead).
execute store result score #zb_ingame_total {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}}]
execute if score #zb_ingame_total {ns}.data matches 2.. run return 0
function {ns}:v{version}/zombies/revive/solo_qr_tick
""")

	## Solo QR tick: auto-increment revive progress (uses {SOLO_QR_TICKS} ticks total)
	write_versioned_function("zombies/revive/solo_qr_tick", f"""
# Check player has uses remaining
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run return 0

# Signal solo reviving so decay logic is skipped (set #zb_reviving=2)
scoreboard players set #zb_reviving {ns}.data 2

# Increment revive_p at normal speed (real-time via #tick_delta)
scoreboard players operation @s {ns}.zb.revive_p += #tick_delta {ns}.data

# Show solo QR auto-revive actionbar with seconds display
scoreboard players operation #rv_qr_sec {ns}.data = @s {ns}.zb.revive_p
scoreboard players operation #rv_qr_sec {ns}.data /= #20 {ns}.data
scoreboard players operation #rv_qr_tenth {ns}.data = @s {ns}.zb.revive_p
scoreboard players operation #rv_qr_tenth {ns}.data %= #20 {ns}.data
scoreboard players operation #rv_qr_tenth {ns}.data /= #2 {ns}.data
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚡ Solo Quick Revive: ","color":"aqua"}},{{"score":{{"name":"#rv_qr_sec","objective":"{ns}.data"}},"color":"green"}},{{"text":".","color":"green"}},{{"score":{{"name":"#rv_qr_tenth","objective":"{ns}.data"}},"color":"green"}},{{"text":"s / {SOLO_QR_TICKS // 20}.{(SOLO_QR_TICKS % 20) // 2}s","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message

# Auto-revive once threshold reached
execute if score @s {ns}.zb.revive_p matches {SOLO_QR_TICKS}.. run function {ns}:v{version}/zombies/revive/solo_qr_complete
""")

	## Solo QR complete: consume one use then revive
	write_versioned_function("zombies/revive/solo_qr_complete", f"""
# Consume one Quick Revive use
scoreboard players add @s {ns}.zb.qr_uses 1

# Always remove the QR tag so the player must rebuy each time
tag @s remove {ns}.perk.quick_revive

# If all {SOLO_QR_MAX} uses are exhausted, keep the perk score at 1 to permanently block rebuy
# Otherwise reset to 0 so the machine allows a new purchase
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {ns}.zb.perk.quick_revive 1
execute unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {ns}.zb.perk.quick_revive 0
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive exhausted! ({SOLO_QR_MAX}/{SOLO_QR_MAX}) No more self-revives this game.","color":"dark_red"}}]
execute unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive used! ({SOLO_QR_MAX - 1 if SOLO_QR_MAX > 1 else 0}/{SOLO_QR_MAX}) Rebuy for another self-revive.","color":"gray"}}]

# Proceed with revive
function {ns}:v{version}/zombies/revive/revive_complete
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Reviver actionbar (run as the reviving player, context @s = reviver, nearest downed = target)
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/show_reviver_bar", f"""
# #rv_reviver_disp holds the downed player's revive progress (snapshotted in downed_tick while
# @s was the downed player — the reviver cannot re-select them: they spectate a camera entity
# that sits outside the revive range, which used to make this display a stuck "0").
# Convert ticks to seconds for display: sec = p/20, tenth = (p%20)/2
scoreboard players operation #rv_rev_sec {ns}.data = #rv_reviver_disp {ns}.data
scoreboard players operation #rv_rev_sec {ns}.data /= #20 {ns}.data
scoreboard players operation #rv_rev_tenth {ns}.data = #rv_reviver_disp {ns}.data
scoreboard players operation #rv_rev_tenth {ns}.data %= #20 {ns}.data
scoreboard players operation #rv_rev_tenth {ns}.data /= #2 {ns}.data

# Check if reviver has Quick Revive perk
execute if entity @s[tag={ns}.perk.quick_revive] run function {ns}:v{version}/zombies/revive/show_reviver_bar_quick
execute unless entity @s[tag={ns}.perk.quick_revive] run function {ns}:v{version}/zombies/revive/show_reviver_bar_normal
""")

	write_versioned_function("zombies/revive/show_reviver_bar_normal", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"Reviving... ","color":"yellow"}},{{"score":{{"name":"#rv_rev_sec","objective":"{ns}.data"}},"color":"green"}},{{"text":".","color":"green"}},{{"score":{{"name":"#rv_rev_tenth","objective":"{ns}.data"}},"color":"green"}},{{"text":"s / {REVIVE_TICKS // 20}.{(REVIVE_TICKS % 20) // 2}s","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/revive/show_reviver_bar_quick", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚡ Reviving... ","color":"aqua"}},{{"score":{{"name":"#rv_rev_sec","objective":"{ns}.data"}},"color":"green"}},{{"text":".","color":"green"}},{{"score":{{"name":"#rv_rev_tenth","objective":"{ns}.data"}},"color":"green"}},{{"text":"s / {QUICK_REVIVE_TICKS // 20}.{(QUICK_REVIVE_TICKS % 20) // 2}s","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message
""")

	# ──────────────────────────────────────────────────────────────────────────
	## HUD color update helpers (run as downed spectator, update nearest downed_hud)
	# ──────────────────────────────────────────────────────────────────────────
	# Recolor only: the name was written once as a literal string in on_down (set_hud_name) and
	# must never be replaced by a "nearest" selector (wrong-owner ties, see on_down)
	for hud_color in ("white", "yellow", "gold", "red"):
		write_versioned_function(f"zombies/revive/hud_{hud_color}", f"""
data modify entity @n[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] text[0].color set value "{hud_color}"
data modify entity @n[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] text[1].color set value "{hud_color}"
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Revive complete: restore the downed player (run as downed spectator)
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/revive_complete", f"""
# Remove downed state
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Identify THIS player's mannequin by downed_id — with several downed players,
# a 'nearest mannequin' lookup could consume someone else's mannequin and revive at the wrong place
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
tag @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] add {ns}.downed_mine_temp

# Store mannequin position before hiding it. Track read success: if the mannequin is missing,
# the storage would keep a stale position (this is how players ended up respawning at 0 0 0)
scoreboard players set #rv_pos_ok {ns}.data 0
execute store success score #rv_pos_ok {ns}.data run data get entity @n[tag={ns}.downed_mine_temp] Pos
execute store result storage {ns}:temp rv_x double 0.001 run data get entity @n[tag={ns}.downed_mine_temp] Pos[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get entity @n[tag={ns}.downed_mine_temp] Pos[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get entity @n[tag={ns}.downed_mine_temp] Pos[2] 1000
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

# Hide mannequin + HUD and kill the camera
function {ns}:v{version}/zombies/revive/hide_body

# Dismount from camera entity and restore adventure mode
ride @s dismount
gamemode adventure @s

# Teleport player to where the mannequin was; if it couldn't be found, fall back to a safe
# spawn point near a teammate instead of teleporting to a stale position (e.g. 0 0 0)
execute if score #rv_pos_ok {ns}.data matches 1 run function {ns}:v{version}/zombies/revive/tp_revive_pos with storage {ns}:temp
execute unless score #rv_pos_ok {ns}.data matches 1 run function {ns}:v{version}/zombies/revive/respawn_near_player

# Restore max health (check for Juggernog perk)
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Heal to full and reset stamina to full (the stamina system owns the hunger bar)
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s {ns}.stam_seen 0

# Tombstone: revived → discard the pending marker + perk snapshot (nothing to recover)
function {ns}:v{version}/zombies/perks/tombstone_on_revived

# Announce
title @s title ["❤"]
title @s subtitle [{{"text":"You have been revived!","color":"green"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"green"}},{{"text":" has been revived!","color":"gray"}}]
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Bleed out: player couldn't be revived in time (run as downed spectator)
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/bleed_out", f"""
# Remove downed state
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Hide THIS player's mannequin and HUD (id-matched: a "nearest" lookup could hide another downed
# player's mannequin when both went down together)
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id

# Tombstone: snapshot the inventory now (still intact) if a marker is waiting for this player
function {ns}:v{version}/zombies/perks/tombstone_on_bleed_out

function {ns}:v{version}/zombies/revive/hide_body

# Dismount then enter full spectator mode to watch until next round
ride @s dismount
gamemode spectator @s

# Spectate a random alive in-game player
execute as @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,limit=1] run spectate @s
# Fallback if no alive players: teleport spectator somewhere reasonable
execute unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run tp @s ~ ~ ~

# Announce
title @s title ["☠"]
title @s subtitle [{{"text":"You bled out. Respawning next round...","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"dark_red"}},{{"text":" has bled out.","color":"gray"}}]
""")

	## Hide @s's body (mannequin + HUD, id-matched via #my_downed_id) by teleporting it far below
	## the world (avoids the kill animation/drops), strip the tags, and kill the camera if any.
	## Shared by revive_complete, bleed_out and the Who's Who paths (no camera there — no-op).
	write_versioned_function("zombies/revive/hide_body", f"""
tag @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] add {ns}.downed_mine_temp
tp @n[tag={ns}.downed_mine_temp] ~ -10000 ~
execute as @e[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tp @s ~ -10000 ~
tag @n[tag={ns}.downed_mine_temp] remove {ns}.downed_mannequin
execute as @e[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tag @s remove {ns}.downed_hud
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp
execute as @e[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match] run kill @s
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Round end respawn: revive all spectating (bled-out) players
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/round_respawn", f"""
# Respawn all spectator (bled-out) players
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=spectator] run function {ns}:v{version}/zombies/revive/do_round_respawn
""")

	write_versioned_function("zombies/revive/do_round_respawn", f"""
# If this player was still DOWNED (mannequin alive) when the round ended, fully tear that state
# down first — otherwise their mannequin/HUD/camera would be orphaned and they'd stay "downed".
execute if entity @s[tag={ns}.downed_spectator] run function {ns}:v{version}/zombies/revive/clear_downed_state

# Restore adventure mode
spectate @s
gamemode adventure @s

# Teleport to a player spawn near a random alive teammate
function {ns}:v{version}/zombies/revive/respawn_near_player

# Heal and reset stamina to full (the stamina system owns the hunger bar)
scoreboard players set @s {ns}.stam_seen 0
effect give @s minecraft:instant_health 1 255 true

# Restore max health (check for Juggernog perk)
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Re-give starting weapon on respawn
function {ns}:v{version}/zombies/inventory/give_respawn_loadout

# Tombstone: if this player bled out with a Tombstone marker, activate it + start the 60s recovery timer
function {ns}:v{version}/zombies/perks/tombstone_on_respawn

# Call map respawn script (executed as the respawning player)
function {ns}:v{version}/shared/maps/call_respawn_script_at_base

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"green"}},{{"text":" has respawned!","color":"gray"}}]
""")

	## Fully tear down @s's downed mannequin/HUD/camera (matched by downed_id) and dismount.
	## Used when a still-downed player is force-revived at round end.
	write_versioned_function("zombies/revive/clear_downed_state", f"""
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @e[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] run kill @s
execute as @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] run kill @s
execute as @e[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match] run kill @s
ride @s dismount
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator
""")

	## Teleport @s to the unlocked player spawn nearest to a random alive teammate (so respawned
	## players rejoin near the action rather than at an arbitrary spawn).
	write_versioned_function("zombies/revive/respawn_near_player", f"""
tag @s add {ns}.spawn_pending
# #has_candidate stays 0 if there is no alive teammate (the `as @r` body never runs, so its
# `store success` never writes); the success flag then replaces a global @e existence scan.
scoreboard players set #has_candidate {ns}.data 0
execute as @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,limit=1] at @s store success score #has_candidate {ns}.data run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate
# Fallback: if no alive teammate, use the unlocked player spawn nearest to @s
execute if score #has_candidate {ns}.data matches 0 run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate
execute as @n[tag={ns}.spawn_candidate] run function {ns}:v{version}/zombies/tp_to_spawn
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Full death: instant elimination with NO mannequin (e.g. falling out of the world).
	## The player goes straight to bled-out spectator and is respawned at the next round end.
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/full_death", f"""
# A doppelganger's unrevived body is forfeited (same rule as going down again)
execute if entity @s[tag={ns}.ww_active] run function {ns}:v{version}/zombies/whos_who/forfeit

# A revive perk saves you from the void instead of a full elimination. Checked BEFORE lose_all
# strips the perks. Who's Who takes priority over solo Quick Revive (same order as revive/on_down):
# - Who's Who: keep playing as a doppelganger; the body can't live in the void, so it drops at a spawn.
# - Solo Quick Revive: in a solo game with uses left, spend one and respawn at a spawn point.
execute if score @s {ns}.zb.perk.whos_who matches 1 run return run function {ns}:v{version}/zombies/revive/void_revive_whos_who
execute store result score #zb_ingame_total {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}}]
execute if entity @s[tag={ns}.perk.quick_revive] if score #zb_ingame_total {ns}.data matches ..1 unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run return run function {ns}:v{version}/zombies/revive/void_revive_solo_qr

# Count it as a down and strip perks (same as a normal down/bleed-out)
scoreboard players add @s {ns}.zb.downs 1
function {ns}:v{version}/zombies/perks/lose_all

# Defensively clear any downed state (no mannequin is created on this path)
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Enter spectator and watch a random alive teammate (respawn handled at round end)
gamemode spectator @s
execute as @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,limit=1] run spectate @s
execute unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run tp @s ~ ~ ~

# Announce
title @s title ["☠"]
title @s subtitle [{{"text":"You fell out of the world!","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"dark_red"}},{{"text":" fell out of the world.","color":"gray"}}]
""")

	## Who's Who saved you from the void (@s = the falling player, perks still intact). Respawn at a
	## safe spawn first (the death spot is the void), then run the normal Who's Who down with the body
	## anchored at that spawn — the doppelganger flow then relocates itself ≥10 blocks from the body.
	write_versioned_function("zombies/revive/void_revive_whos_who", f"""
gamemode adventure @s
function {ns}:v{version}/zombies/revive/respawn_near_player
data modify storage {ns}:temp _body_at set from entity @s Pos
function {ns}:v{version}/zombies/whos_who/on_down
""")

	## Solo Quick Revive saved you from the void (@s = the falling player, solo game, uses left).
	## Spend one use and respawn at a spawn point. Perks are still stripped (any down loses them),
	## consistent with a normal solo QR self-revive; the QR rebuy bookkeeping mirrors solo_qr_complete.
	write_versioned_function("zombies/revive/void_revive_solo_qr", f"""
# Consume one Quick Revive use (same rebuy bookkeeping as solo_qr_complete)
scoreboard players add @s {ns}.zb.qr_uses 1
tag @s remove {ns}.perk.quick_revive
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {ns}.zb.perk.quick_revive 1
execute unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {ns}.zb.perk.quick_revive 0
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive exhausted! ({SOLO_QR_MAX}/{SOLO_QR_MAX}) No more self-revives this game.","color":"dark_red"}}]
execute unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive used! ({SOLO_QR_MAX - 1 if SOLO_QR_MAX > 1 else 0}/{SOLO_QR_MAX}) Rebuy for another self-revive.","color":"gray"}}]

# Count the down and strip perks (any down loses them), then clear any downed state defensively
scoreboard players add @s {ns}.zb.downs 1
function {ns}:v{version}/zombies/perks/lose_all
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Respawn at a safe spawn, healthy
gamemode adventure @s
function {ns}:v{version}/zombies/revive/respawn_near_player
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s {ns}.stam_seen 0

# Announce
title @s times 5 40 15
title @s title ["⚡"]
title @s subtitle [{{"text":"Quick Revive pulled you back from the void!","color":"aqua"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"aqua"}},{{"text":" fell out — but Quick Revive pulled them back!","color":"gray"}}]
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Hook: reset revive state on game start
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/start", f"""
# Reset revive state
scoreboard players set @a {ns}.zb.downed 0
scoreboard players set @a {ns}.zb.bleed 0
scoreboard players set @a {ns}.zb.revive_p 0
scoreboard players set @a {ns}.zb.qr_uses 0
scoreboard players set @a {ns}.zb.downed_id 0
scoreboard players set #downed_id_next {ns}.data 0
tag @a remove {ns}.downed_spectator
kill @e[tag={ns}.downed_mannequin]
kill @e[tag={ns}.downed_hud]
kill @e[tag={ns}.downed_cam]
kill @e[tag={ns}.tombstone]
data modify storage {ns}:zombies tombstone_inv set value {{}}
""")

	## Hook: reset revive state on game stop
	write_versioned_function("zombies/stop", f"""
# Reset revive state
scoreboard players set @a {ns}.zb.downed 0
scoreboard players set @a {ns}.zb.bleed 0
scoreboard players set @a {ns}.zb.revive_p 0
scoreboard players set @a {ns}.zb.qr_uses 0
scoreboard players set @a {ns}.zb.downed_id 0
scoreboard players set #downed_id_next {ns}.data 0
tag @a remove {ns}.downed_spectator
kill @e[tag={ns}.downed_mannequin]
kill @e[tag={ns}.downed_hud]
kill @e[tag={ns}.downed_cam]
kill @e[tag={ns}.tombstone]
data modify storage {ns}:zombies tombstone_inv set value {{}}
""")

