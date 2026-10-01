""" Revive tuning constants and the mannequin upkeep blocks Who's Who reuses. """
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
HUD_OFFSET_Y_THOUSANDTHS: int = 2000
""" HUD text height above the mannequin: 2.0 blocks * 1000, for scoreboard math. """


# Functions
def revive_body_detect() -> str:
	""" Per-tick upkeep of one revivable body, for a normal down and Who's Who.

	Emitted into the caller's tick function.
	@s holds the downed state and its `zb.bleed` and `zb.revive_p` (a downed spectator, or an alive Who's Who doppelganger), and #my_downed_id is the body's id.
	Decrements the bleed timer and counts the revivers around the id-matched mannequin into #zb_reviving.
	Revivers exclude downed and spectating players but include doppelgangers, and for a Who's Who body the owner (self-revive).
	"""
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	return f"""
# Body upkeep (revive_body_detect).
scoreboard players operation @s {ns}.zb.bleed -= #tick_delta {ns}.data

# Id-matched, since with several bodies the nearest mannequin can be someone else's.
scoreboard players set #zb_reviving {ns}.data 0
execute as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE}] run scoreboard players set #zb_reviving {ns}.data 1
""".strip()

def revive_body_progress(complete_function: str) -> str:
	""" Revive progress of one revivable body: progress and decay of `zb.revive_p`, reviver bar, HUD colour, completion thresholds.

	Emitted below revive_body_detect, with the same contract.
	On completion it does `return run complete_function`, so the caller's bleed-out checks below are skipped that tick.
	"""
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	return f"""
# Progress (revive_body_progress): +delta while someone revives (1), nothing during a solo revive (2), 2x decay otherwise (0).
execute if score #zb_reviving {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.revive_p += #tick_delta {ns}.data
scoreboard players operation #rv_decay {ns}.data = #tick_delta {ns}.data
scoreboard players operation #rv_decay {ns}.data *= #2 {ns}.data
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.revive_p matches 1.. run scoreboard players operation @s {ns}.zb.revive_p -= #rv_decay {ns}.data

# Snapshot for the reviver bar: a reviver cannot reliably select the downed player.
scoreboard players operation #rv_reviver_disp {ns}.data = @s {ns}.zb.revive_p
tag @a remove {ns}.zb_reviver
execute if score #zb_reviving {ns}.data matches 1 as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE}] run function {ns}:v{version}/zombies/revive/show_reviver_bar

execute if score #zb_reviving {ns}.data matches 1.. run function {ns}:v{version}/zombies/revive/hud_white
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.bleed matches 400.. run function {ns}:v{version}/zombies/revive/hud_yellow
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.bleed matches 200..399 run function {ns}:v{version}/zombies/revive/hud_gold
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.bleed matches ..199 run function {ns}:v{version}/zombies/revive/hud_red

# Faster when a reviver at the body owns Quick Revive. `return run`: zb.bleed is 0 on the completion tick,
# so the caller's bleed-out checks must not run.
execute if score #zb_reviving {ns}.data matches 1 run scoreboard players set #rv_qr_near {ns}.data 0
execute if score #zb_reviving {ns}.data matches 1 as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE},tag={ns}.perk.quick_revive] run scoreboard players set #rv_qr_near {ns}.data 1
execute if score #zb_reviving {ns}.data matches 1 if score #rv_qr_near {ns}.data matches 1 if score @s {ns}.zb.revive_p matches {QUICK_REVIVE_TICKS}.. run return run function {complete_function}
execute if score #zb_reviving {ns}.data matches 1 if score #rv_qr_near {ns}.data matches 0 if score @s {ns}.zb.revive_p matches {REVIVE_TICKS}.. run return run function {complete_function}
""".strip()

