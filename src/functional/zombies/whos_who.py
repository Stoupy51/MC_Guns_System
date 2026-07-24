
# ruff: noqa: E501
# Who's Who — instead of going down, the owner keeps playing as a "doppelganger" with only a knife +
# pistol, while their body drops as a NORMAL revivable downed body (revive/spawn_downed_body): same
# mannequin, same HUD, same revive interactions — any alive player (doppelgangers included, and the
# owner themselves) revives it through the shared revive core. On revive the owner gets everything
# back (exact inventory slots + perks minus Who's Who); if the body bleeds out, the doppelganger
# fights on with just the pistol (perks stay lost). Going down again as a doppelganger forfeits the
# unrevived body (BO2 rule), then downs normally. Works solo (self-revive), takes priority over solo
# Quick Revive and Tombstone. Called from revive/on_down.
#
# The owner stays a normal ALIVE player (never zb.downed), tagged {ns}.ww_active, ticked from
# game_tick. The body link lives in {ns}.zb.ww.id — NOT zb.downed_id, which a later normal down
# overwrites (that used to orphan the mannequin). Bleed/revive progress reuse the owner's normal
# zb.bleed / zb.revive_p scores so the shared revive core works unchanged.
from stewbeet import Mem, write_load_file, write_versioned_function

from ..core.feedback import zb_sound
from ..helpers import MGS_TAG
from .perks import PERK_DEFINITIONS
from .revive import BLEED_OUT_TICKS, revive_body_detect, revive_body_progress


def generate_whos_who() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	perk_ids: list[str] = list(PERK_DEFINITIONS)

	# quick_revive: score 1 can also mean "solo uses exhausted" (rebuy-block) with no active tag —
	# only snapshot a QR that is actually active, or the revive would grant one back for free.
	ww_snapshot: str = "\n".join(
		f"execute store success score @s {ns}.zb.wwp.{pid} if entity @s[tag={ns}.perk.quick_revive]"
		if pid == "quick_revive"
		else f"scoreboard players operation @s {ns}.zb.wwp.{pid} = @s {ns}.zb.perk.{pid}"
		for pid in perk_ids
	)
	ww_clear: str = "\n".join(f"scoreboard players set @s {ns}.zb.wwp.{pid} 0" for pid in perk_ids)
	ww_restore_lines: list[str] = []
	for pid, pdata in PERK_DEFINITIONS.items():
		if pid == "whos_who":
			continue  # Who's Who is not restored on revive (BO rule) — must be rebought
		ww_restore_lines.append(f"execute if score @s {ns}.zb.wwp.{pid} matches 1 run scoreboard players set @s {ns}.zb.perk.{pid} 1")
		if pdata.get("commands"):
			# reapply/<pid> (effect-only, no chat) is generated in perks.py's Tombstone section
			ww_restore_lines.append(f"execute if score @s {ns}.zb.wwp.{pid} matches 1 run function {ns}:v{version}/zombies/perks/reapply/{pid}")
	ww_restore: str = "\n".join(ww_restore_lines)

	## State objectives
	write_load_file(f"""
# Who's Who: the owner's body link (zb.ww.id survives later normal downs, unlike zb.downed_id) +
# perk snapshot for recovery. Bleed/revive progress live on the owner's normal zb.bleed /
# zb.revive_p scores (the shared revive core reads those).
scoreboard objectives add {ns}.zb.ww.id dummy
{chr(10).join(f"scoreboard objectives add {ns}.zb.wwp.{pid} dummy" for pid in perk_ids)}
""")

	## Called from revive/on_down (@s = player). Takes over the down entirely.
	write_versioned_function("zombies/whos_who/on_down", f"""
# Snapshot perks + inventory (for recovery on revive) — BEFORE anything is stripped
{ww_snapshot}

# Fresh body id, kept in zb.ww.id: a later normal down assigns a new zb.downed_id, and the body
# link must survive that (this used to orphan the mannequin)
scoreboard players add #downed_id_next {ns}.data 1
scoreboard players operation @s {ns}.zb.downed_id = #downed_id_next {ns}.data
scoreboard players operation @s {ns}.zb.ww.id = #downed_id_next {ns}.data
execute store result storage {ns}:temp _ww_id.id int 1 run scoreboard players get @s {ns}.zb.ww.id
function {ns}:v{version}/zombies/whos_who/snapshot_inv with storage {ns}:temp _ww_id

# Drop the body at the death spot: the EXACT same revivable mannequin + HUD as a normal down
# (same tags, same visuals, same revive interactions)
function {ns}:v{version}/zombies/revive/spawn_downed_body

# Strip perks (the doppelganger starts fresh)
function {ns}:v{version}/zombies/perks/lose_all

# Doppelganger loadout: wipe everything and hand back only the starting knife + pistol kit
clear @s
gamemode adventure @s
function {ns}:v{version}/zombies/inventory/give_respawn_loadout

# Respawn the doppelganger at the unlocked player spawn nearest to the body but at least 10 blocks
# away from it (falls back to the nearest one at all if none is that far)
tag @s add {ns}.spawn_pending
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.ww.id
scoreboard players set #has_candidate {ns}.data 0
execute as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s store success score #has_candidate {ns}.data run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked,distance=10..] add {ns}.spawn_candidate
execute if score #has_candidate {ns}.data matches 0 as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate
execute as @n[tag={ns}.spawn_candidate] run function {ns}:v{version}/zombies/tp_to_spawn
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending

# Enter doppelganger state (the shared revive core reads zb.bleed / zb.revive_p on the owner)
tag @s add {ns}.ww_active
scoreboard players set @s {ns}.zb.bleed {BLEED_OUT_TICKS}
scoreboard players set @s {ns}.zb.revive_p 0

# Announce
title @s times 5 40 15
title @s title ["👥"]
title @s subtitle [{{"text":"Who's Who — revive your body, or fight on!","color":"dark_aqua"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"aqua"}},{{"text":" went down — but plays on as a doppelganger!","color":"gray"}}]
""")

	## Macro: store @s Inventory keyed by body id (for recovery on revive)
	write_versioned_function("zombies/whos_who/snapshot_inv", f"""
$data modify storage {ns}:zombies ww_inv."$(id)" set from entity @s Inventory
""")

	## Macro: load a snapshot by id into the shared restore buffer, then drop the snapshot
	write_versioned_function("zombies/whos_who/load_snapshot", f"""
$data modify storage {ns}:temp _restore.items set from storage {ns}:zombies ww_inv."$(id)"
$data remove storage {ns}:zombies ww_inv."$(id)"
""")

	## Macro: discard a snapshot by id (bleed out / forfeit — nothing is recovered)
	write_versioned_function("zombies/whos_who/discard_snapshot", f"""
$data remove storage {ns}:zombies ww_inv."$(id)"
""")

	## Per-tick, per doppelganger (hooked into game_tick). @s = the ww_active owner.
	write_versioned_function("zombies/whos_who/tick", f"""
execute as @a[tag={ns}.ww_active,scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/whos_who/owner_tick
""")

	## Owner tick: the body is a normal downed mannequin, so the whole revive flow (reviver
	## detection incl. the owner themselves, progress bar, HUD colors, Quick Revive threshold)
	## is the shared revive core — only the completion/bleed-out outcomes are Who's Who-specific.
	write_versioned_function("zombies/whos_who/owner_tick", f"""
# The body is id-linked via zb.ww.id (NOT zb.downed_id, which a later normal down overwrites)
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.ww.id

{revive_body_detect()}

{revive_body_progress(f"{ns}:v{version}/zombies/whos_who/revive_complete")}

# Body bled out: doppelganger fights on with just the pistol (perks stay lost)
execute if score @s {ns}.zb.bleed matches ..0 run function {ns}:v{version}/zombies/whos_who/bleed_out
""")

	## Revive complete (@s = doppelganger owner, whoever revived the body): restore perks (minus
	## Who's Who) + the exact snapshotted inventory + health, then drop body + doppelganger state.
	write_versioned_function("zombies/whos_who/revive_complete", f"""
{ww_restore}
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40

# Restore the snapshotted inventory into the exact original slots (players can't be data-modified,
# so this goes through the shared inventory/restore_inventory system)
execute store result storage {ns}:temp _ww_id.id int 1 run scoreboard players get @s {ns}.zb.ww.id
function {ns}:v{version}/zombies/whos_who/load_snapshot with storage {ns}:temp _ww_id
function {ns}:v{version}/zombies/inventory/restore_inventory
function {ns}:v{version}/zombies/inventory/refresh_perk_items
effect give @s minecraft:instant_health 1 255 true

# Remove the body and clear doppelganger state + snapshot
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.ww.id
function {ns}:v{version}/zombies/revive/hide_body
{ww_clear}
tag @s remove {ns}.ww_active
scoreboard players set @s {ns}.zb.ww.id 0
scoreboard players set @s {ns}.zb.bleed 0
scoreboard players set @s {ns}.zb.revive_p 0

title @s times 5 40 15
title @s title ["❤"]
title @s subtitle [{{"text":"Body revived — you are whole again!","color":"green"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"green"}},{{"text":"'s body was revived — they are whole again!","color":"gray"}}]
{zb_sound('success')}
""")

	## Body bled out (@s = doppelganger owner): keep playing with the pistol, perks stay lost
	write_versioned_function("zombies/whos_who/bleed_out", f"""
function {ns}:v{version}/zombies/whos_who/forfeit
title @s title ["☠"]
title @s subtitle [{{"text":"Your body bled out — fight on with your pistol.","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"dark_aqua"}},{{"text":"'s body bled out.","color":"gray"}}]
""")

	## Silently discard @s's body + snapshot and leave doppelganger state (no revive, no restore).
	## Used by bleed_out, and by revive/on_down + full_death when a doppelganger goes down again
	## (BO2 rule: downing again forfeits the unrevived body — it must never outlive its owner state).
	write_versioned_function("zombies/whos_who/forfeit", f"""
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.ww.id
function {ns}:v{version}/zombies/revive/hide_body
execute store result storage {ns}:temp _ww_id.id int 1 run scoreboard players get @s {ns}.zb.ww.id
function {ns}:v{version}/zombies/whos_who/discard_snapshot with storage {ns}:temp _ww_id
{ww_clear}
tag @s remove {ns}.ww_active
scoreboard players set @s {ns}.zb.ww.id 0
scoreboard players set @s {ns}.zb.bleed 0
scoreboard players set @s {ns}.zb.revive_p 0
""")

	## Hook: tick doppelgangers
	write_versioned_function("zombies/game_tick", f"""
execute if data storage {ns}:zombies game{{state:"active"}} run function {ns}:v{version}/zombies/whos_who/tick
""")

	## Hook: cleanup on game start/stop (the bodies share the downed_mannequin/downed_hud tags and
	## are already killed by revive.py's start/stop hooks)
	write_versioned_function("zombies/start", f"""
tag @a remove {ns}.ww_active
scoreboard players set @a {ns}.zb.ww.id 0
data modify storage {ns}:zombies ww_inv set value {{}}
""")
	write_versioned_function("zombies/stop", f"""
tag @a remove {ns}.ww_active
scoreboard players set @a {ns}.zb.ww.id 0
data modify storage {ns}:zombies ww_inv set value {{}}
""")
