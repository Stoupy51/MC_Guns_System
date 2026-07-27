""" Revive tuning constants and the mannequin upkeep blocks Who's Who reuses. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem

# Constants
BLEED_OUT_TICKS: int = 1200
""" 60 seconds to be revived before bleed out. """
REVIVE_TICKS: int = 60
""" 3 seconds of proximity to revive. """
REVIVE_RANGE: float = 2.5
""" Blocks range for revive interaction. """
QUICK_REVIVE_TICKS: int = 30
""" 1.5 seconds with Quick Revive perk. """
SOLO_QR_TICKS: int = 200
""" 10 seconds for solo Quick Revive auto-revive. """
SOLO_QR_MAX: int = 3
""" Total solo self-revives allowed per game; each use requires rebuying QR. """
CRAWL_SPEED: float = 0.06
""" Blocks per tick for downed crawl movement. """
ROUND_END_PICKUP_RANGE: int = 10
""" A teammate this close to a still-downed body at round end revives it for free. """
HUD_OFFSET_Y_THOUSANDTHS: int = 2000
""" HUD text height above the mannequin: 2.0 blocks * 1000, for scoreboard math. """


# Functions
def revive_body_detect() -> str:
	""" Shared per-tick upkeep for one revivable body (normal down AND Who's Who).

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

