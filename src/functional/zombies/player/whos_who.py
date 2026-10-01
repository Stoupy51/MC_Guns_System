""" Who's Who: instead of going down, the owner plays on as a doppelganger with a knife and pistol.

The body drops as a normal revivable mannequin, so the shared revive core handles detection, progress, HUD and Quick Revive.
On revive the owner gets their inventory and perks back minus Who's Who; if the body bleeds out, the doppelganger keeps only the pistol.
Going down again forfeits the unrevived body (BO2 rule). Works solo, and outranks solo Quick Revive and Tombstone.

The owner stays a normal alive player (never zb.downed), tagged ww_active.
The body link lives in zb.ww.id, not zb.downed_id, which a later normal down would overwrite.
Bleed and revive progress use the owner's normal scores, so the revive core works unchanged.
"""
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ...core.feedback import ZombiesFeedback
from ...helpers import MGS_TAG
from ...helpers.text import Text
from ...helpers.titles import TitleTimes
from ..machines.perks.definitions import PERK_DEFINITIONS
from .revive.shared import BLEED_OUT_TICKS, revive_body_detect, revive_body_progress


# Functions
def generate_whos_who() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	# Who's Who never gives itself back (Black Ops rule).
	perk_ids: list[str] = [pid for pid in PERK_DEFINITIONS if pid != "whos_who"]

	# Only an active Quick Revive is snapshotted: score 1 can also mean "solo uses exhausted".
	ww_snapshot: str = "\n".join(
		f"execute store success score @s {ns}.zb.wwp.{pid} if entity @s[tag={ns}.perk.quick_revive]"
		if pid == "quick_revive"
		else f"scoreboard players operation @s {ns}.zb.wwp.{pid} = @s {ns}.zb.perk.{pid}"
		for pid in perk_ids
	)
	ww_clear: str = "\n".join(f"scoreboard players set @s {ns}.zb.wwp.{pid} 0" for pid in perk_ids)
	ww_restore_lines: list[str] = []
	for pid in perk_ids:
		pdata = PERK_DEFINITIONS[pid]
		ww_restore_lines.append(f"execute if score @s {ns}.zb.wwp.{pid} matches 1 run scoreboard players set @s {ns}.zb.perk.{pid} 1")
		if pdata.commands:
			# reapply/<pid> (no chat, jingle or XP) is generated in perks/tombstone.
			ww_restore_lines.append(f"execute if score @s {ns}.zb.wwp.{pid} matches 1 run function {ns}:v{version}/zombies/perks/reapply/{pid}")
	ww_restore: str = "\n".join(ww_restore_lines)

	write_load_file(f"""
# zb.ww.id links the owner to the body and survives later normal downs, unlike zb.downed_id.
# Bleed and revive progress use the owner's normal zb.bleed and zb.revive_p scores.
scoreboard objectives add {ns}.zb.ww.id dummy
{chr(10).join(f"scoreboard objectives add {ns}.zb.wwp.{pid} dummy" for pid in perk_ids)}
""")

	# Run from revive/on_down as the player; replaces the down entirely.
	write_versioned_function("zombies/whos_who/on_down", f"""
# Before anything is stripped.
{ww_snapshot}

# Kept in zb.ww.id, since a later normal down assigns a new zb.downed_id.
scoreboard players add #downed_id_next {ns}.data 1
scoreboard players operation @s {ns}.zb.downed_id = #downed_id_next {ns}.data
scoreboard players operation @s {ns}.zb.ww.id = #downed_id_next {ns}.data
execute store result storage {ns}:temp _ww_id.id int 1 run scoreboard players get @s {ns}.zb.ww.id
function {ns}:v{version}/zombies/whos_who/snapshot_inv with storage {ns}:temp _ww_id

# The same revivable mannequin and HUD as a normal down.
function {ns}:v{version}/zombies/revive/spawn_downed_body

function {ns}:v{version}/zombies/perks/lose_all

# Only the starting knife and pistol kit.
clear @s
gamemode adventure @s
function {ns}:v{version}/zombies/inventory/give_respawn_loadout

# At the unlocked player spawn nearest the body but at least 10 blocks away (else the nearest one).
tag @s add {ns}.spawn_pending
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.ww.id
scoreboard players set #has_candidate {ns}.data 0
execute as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s store success score #has_candidate {ns}.data run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked,distance=10..] add {ns}.spawn_candidate
execute if score #has_candidate {ns}.data matches 0 as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate
execute as @n[tag={ns}.spawn_candidate] run function {ns}:v{version}/shared/tp_to_spawn {{mode:"zombies"}}
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending

tag @s add {ns}.ww_active
scoreboard players set @s {ns}.zb.bleed {BLEED_OUT_TICKS}
scoreboard players set @s {ns}.zb.revive_p 0

{TitleTimes.EVENT.cmd()}
title @s title ["👥"]
title @s subtitle [{{"text":"Who's Who: revive your body, or fight on!","color":"dark_aqua"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="aqua")},{{"text":" went down but plays on as a doppelganger!","color":"gray"}}]
""")

	write_versioned_function("zombies/whos_who/snapshot_inv", f"""
$data modify storage {ns}:zombies ww_inv."$(id)" set from entity @s Inventory
""")

	write_versioned_function("zombies/whos_who/load_snapshot", f"""
$data modify storage {ns}:temp _restore.items set from storage {ns}:zombies ww_inv."$(id)"
$data remove storage {ns}:zombies ww_inv."$(id)"
""")

	# Bleed out or forfeit: nothing recovered.
	write_versioned_function("zombies/whos_who/discard_snapshot", f"""
$data remove storage {ns}:zombies ww_inv."$(id)"
""")

	# Run as each ww_active owner.
	write_versioned_function("zombies/whos_who/tick", f"""
execute as @a[tag={ns}.ww_active,scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/whos_who/owner_tick
""")

	# The revive flow is the shared core; only the outcomes differ.
	write_versioned_function("zombies/whos_who/owner_tick", f"""
# zb.ww.id, not zb.downed_id, which a later normal down overwrites.
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.ww.id

{revive_body_detect()}

{revive_body_progress(f"{ns}:v{version}/zombies/whos_who/revive_complete")}

# The doppelganger fights on with the pistol; perks stay lost.
execute if score @s {ns}.zb.bleed matches ..0 run function {ns}:v{version}/zombies/whos_who/bleed_out
""")

	# Restores perks (minus Who's Who), the inventory and health.
	write_versioned_function("zombies/whos_who/revive_complete", f"""
{ww_restore}
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40

# Players cannot be data-modified, so the inventory goes back through inventory/restore_inventory.
execute store result storage {ns}:temp _ww_id.id int 1 run scoreboard players get @s {ns}.zb.ww.id
function {ns}:v{version}/zombies/whos_who/load_snapshot with storage {ns}:temp _ww_id
function {ns}:v{version}/zombies/inventory/restore_inventory
function {ns}:v{version}/zombies/inventory/refresh_perk_items
effect give @s minecraft:instant_health 1 255 true

scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.ww.id
function {ns}:v{version}/zombies/revive/hide_body
{ww_clear}
tag @s remove {ns}.ww_active
scoreboard players set @s {ns}.zb.ww.id 0
scoreboard players set @s {ns}.zb.bleed 0
scoreboard players set @s {ns}.zb.revive_p 0

{TitleTimes.EVENT.cmd()}
title @s title ["❤"]
title @s subtitle [{{"text":"Body revived: you are whole again!","color":"green"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="green")},{{"text":"'s body was revived: they are whole again!","color":"gray"}}]
{ZombiesFeedback.zb_sound('success')}
""")

	# Run as the owner: keep the pistol, perks stay lost.
	write_versioned_function("zombies/whos_who/bleed_out", f"""
function {ns}:v{version}/zombies/whos_who/forfeit
{TitleTimes.BAD_NEWS.cmd()}
title @s title ["☠"]
title @s subtitle [{{"text":"Your body bled out. Fight on with your pistol.","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="dark_aqua")},{{"text":"'s body bled out.","color":"gray"}}]
""")

	# Silently drop the body and snapshot. Runs on bleed out, and on a new down while a body is unrevived.
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

	write_versioned_function("zombies/game_tick", f"""
execute if data storage {ns}:zombies game{{state:"active"}} run function {ns}:v{version}/zombies/whos_who/tick
""")

	# Bodies carry the downed_mannequin tags, so the revive start and stop hooks already kill them.
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

