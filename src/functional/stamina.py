
# Stamina system (Call of Duty: Black Ops style) — reference: src/functional/zombies/stamina.md
#
# Shared across all three modes (multiplayer, missions, zombies). The hunger bar IS the visible
# stamina meter: 20 = full stamina, 6 = empty (vanilla already blocks sprinting at foodLevel <= 6,
# so the bar doubles as the sprint gate). A scoreboard (mgs.stam) stays the source of truth for
# deterministic timing; every tick the bar is nudged toward the mapped target with short
# saturation/hunger pulses, so the player SEES stamina drain while sprinting and refill while
# resting. No sound and no "out of breath" message — the draining bar is the feedback.
#
# Saturation discipline (stamina.md): the saturation effect restores +1 food but ALSO +2 invisible
# saturation per tick. Left unchecked that invisible buffer absorbs hunger pulses and freezes the
# bar for seconds. So refill pulses are only given while the bar is below target, and leftover
# invisible saturation is burned off with hunger pulses whenever the bar sits at target, keeping
# the bar responsive the moment the player sprints again.
#
# Stamin-Up (zombies perk, stamina.md): double sprint endurance = +STAM_MAX on mgs.stam_bonus
# (sprintEnergyMax * 2); the +7% movement speed is an attribute modifier applied by the perk.

from stewbeet import Mem, write_load_file, write_versioned_function

# Tuning constants (all in ticks / stamina points). Stamina runs 0..stam_max.
STAM_MAX: int = 200      # base full stamina (perks add mgs.stam_bonus on top)
STAM_DRAIN: int = 2      # stamina lost per tick while sprinting  -> 200/2 = 100t (5s); 10s with Stamin-Up
STAM_REGEN: int = 2      # stamina gained per tick while resting  -> 200/2 = 100t (5s) to refill
REST_DELAY: int = 20     # ticks after the last sprint before regen starts (1s)
RECOVER_AT: int = 80     # winded players can sprint again once stamina regenerates back to this (hysteresis)

# Hunger-bar mapping: target foodLevel = FOOD_MIN + FOOD_SPAN * stam / stam_max
FOOD_MIN: int = 6        # vanilla no-sprint threshold = empty stamina
FOOD_MAX: int = 20       # full bar = full stamina
FOOD_SPAN: int = FOOD_MAX - FOOD_MIN


def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    ## Objectives
    write_load_file(f"""
# Stamina system (Black Ops style) — per-player stamina state
scoreboard objectives add {ns}.stam dummy
scoreboard objectives add {ns}.stam_max dummy
scoreboard objectives add {ns}.stam_bonus dummy
scoreboard objectives add {ns}.stam_rest dummy
scoreboard objectives add {ns}.stam_out dummy
scoreboard objectives add {ns}.stam_seen dummy

# Set while refill pulses may have left invisible saturation; only then does the at-target
# branch pay the foodSaturationLevel NBT read to burn it off (see stamina_bar)
scoreboard objectives add {ns}.stam_dirty dummy
""")

    ## Hook into the global player tick. player/tick runs `as @e[type=player] at @s`, so @s is each
    ## player. Only run for players currently in a game mode and not spectating (downed/dead players
    ## spectate). One in_game flag is set at a time, so at most one branch fires.
    gate: str = f"execute if score #any_game_active {ns}.data matches 1 unless entity @s[gamemode=spectator]"
    write_versioned_function("player/tick", f"""
# Stamina (Black Ops style): drain while sprinting, block sprint when winded, regen while resting
{gate} if score @s {ns}.mp.in_game matches 1 run function {ns}:v{version}/player/stamina_tick
{gate} if score @s {ns}.mi.in_game matches 1 run function {ns}:v{version}/player/stamina_tick
{gate} if score @s {ns}.zb.in_game matches 1 run function {ns}:v{version}/player/stamina_tick
""")

    ## Per-player stamina tick (@s = in-game, non-spectating player, at @s)
    write_versioned_function("player/stamina_tick", f"""
# First tick in this game (or a fresh late-joiner / respawn): start at full stamina. stam_seen is
# reset to 0 at game start (see regen_enable_lines) and on respawn/revive, so this re-inits then.
execute if score @s {ns}.stam_seen matches 0 run function {ns}:v{version}/player/stamina_init

# Max stamina = base + perk bonus (Stamin-Up doubles the endurance budget); clamp current to it
scoreboard players set @s {ns}.stam_max {STAM_MAX}
scoreboard players operation @s {ns}.stam_max += @s {ns}.stam_bonus
scoreboard players operation @s {ns}.stam < @s {ns}.stam_max

# Detect sprinting via the is_sprinting entity flag: unlike the sprint_one_cm stat (which only
# increments on the ground), the flag stays set through the whole jump arc, so jump-sprinting
# drains exactly like ground sprinting
scoreboard players set #stam_sprinting {ns}.data 0
execute if predicate {ns}:v{version}/is_sprinting run scoreboard players set #stam_sprinting {ns}.data 1

# Sprinting → drain stamina and (re)arm the rest delay before regen can start
execute if score #stam_sprinting {ns}.data matches 1 run scoreboard players remove @s {ns}.stam {STAM_DRAIN}
execute if score #stam_sprinting {ns}.data matches 1 run scoreboard players set @s {ns}.stam_rest {REST_DELAY}

# Resting → count down the delay, then regen stamina
execute if score #stam_sprinting {ns}.data matches 0 if score @s {ns}.stam_rest matches 1.. run scoreboard players remove @s {ns}.stam_rest 1
execute if score #stam_sprinting {ns}.data matches 0 if score @s {ns}.stam_rest matches 0 run scoreboard players add @s {ns}.stam {STAM_REGEN}

# Clamp 0..max
execute if score @s {ns}.stam matches ..-1 run scoreboard players set @s {ns}.stam 0
scoreboard players operation @s {ns}.stam < @s {ns}.stam_max

# Become winded when stamina hits 0; silently recover once it regenerates past the hysteresis
# threshold. No sound, no "out of breath" message — the empty bar is the feedback (stamina.md).
execute if score @s {ns}.stam_out matches 0 if score @s {ns}.stam matches 0 run scoreboard players set @s {ns}.stam_out 1
execute if score @s {ns}.stam_out matches 1 if score @s {ns}.stam matches {RECOVER_AT}.. run scoreboard players set @s {ns}.stam_out 0

# Map stamina to the hunger-bar target ({FOOD_MIN}..{FOOD_MAX}); winded → held at the no-sprint level
scoreboard players operation #stam_t {ns}.data = @s {ns}.stam
scoreboard players operation #stam_t {ns}.data *= #{FOOD_SPAN} {ns}.data
scoreboard players operation #stam_t {ns}.data /= @s {ns}.stam_max
scoreboard players add #stam_t {ns}.data {FOOD_MIN}
execute if score @s {ns}.stam_out matches 1 run scoreboard players set #stam_t {ns}.data {FOOD_MIN}

# Nudge the visible bar toward the target
function {ns}:v{version}/player/stamina_bar
""")

    write_versioned_function("player/stamina_init", f"""
scoreboard players set @s {ns}.stam_max {STAM_MAX}
scoreboard players operation @s {ns}.stam_max += @s {ns}.stam_bonus
scoreboard players operation @s {ns}.stam = @s {ns}.stam_max
scoreboard players set @s {ns}.stam_out 0
scoreboard players set @s {ns}.stam_rest 0
scoreboard players set @s {ns}.stam_seen 1

# Assume leftover invisible saturation from before the game (e.g. the game-stop refill pin),
# so the first at-target ticks verify and burn it off
scoreboard players set @s {ns}.stam_dirty 1
""")

    ## Drive the hunger bar toward #stam_t with 1-tick effect pulses (@s = in-game player).
    ## Clearing both effects first kills last tick's pulses AND any infinite saturation pin left
    ## by other systems, so this function fully owns the bar while a game is running.
    write_versioned_function("player/stamina_bar", f"""
effect clear @s minecraft:saturation
effect clear @s minecraft:hunger

# The bar is read from the auto-updated 'food' criterion — no player-NBT read on this path.
# Below target → refill pulse (+1 food this tick). Never given at/above target so the invisible
# saturation side effect (+2/tick) can't stack past what's visible (stamina.md). The pulse may
# leave invisible saturation behind, so flag it for the at-target burn-off below.
execute if score @s {ns}.food < #stam_t {ns}.data run scoreboard players set @s {ns}.stam_dirty 1
execute if score @s {ns}.food < #stam_t {ns}.data run return run effect give @s minecraft:saturation 1 0 true

# Above target → hunger pulse slowly drains the bar, showing the player they sprint too much
execute if score @s {ns}.food > #stam_t {ns}.data run return run effect give @s minecraft:hunger 1 255 true

# At target: only while flagged dirty, pay the saturation NBT read and burn leftovers off with
# hunger pulses so the next drain shows immediately; once it reads 0 the flag clears and the
# steady state costs no NBT read at all
execute unless score @s {ns}.stam_dirty matches 1 run return 0
execute store result score #stam_sat {ns}.data run data get entity @s foodSaturationLevel
execute if score #stam_sat {ns}.data matches 1.. run return run effect give @s minecraft:hunger 1 255 true
scoreboard players set @s {ns}.stam_dirty 0
""")

