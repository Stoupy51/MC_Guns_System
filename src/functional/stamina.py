
# Stamina system (Call of Duty: Black Ops style)
#
# Shared across all three modes (multiplayer, missions, zombies). Sprinting for too long drains
# a stamina meter; when it empties the player becomes "winded" and the hunger bar is pushed down
# to the vanilla no-sprint threshold (foodLevel <= 6), so the player physically can't sprint.
# After resting for a moment, stamina slowly regenerates and a saturation burst refills the bar.
#
# A scoreboard (mgs.stam) is the source of truth so the timing is deterministic; the hunger bar is
# only used as the on/off sprint gate + visual indicator. We don't fight the modes' "infinite
# saturation" pins continuously — saturation is only cleared at the moment a player gets winded.

from stewbeet import Mem, write_load_file, write_versioned_function

# Tuning constants (all in ticks / stamina points). Stamina runs 0..MAX.
STAM_MAX: int = 100      # full stamina
STAM_DRAIN: int = 2      # stamina lost per tick while sprinting  -> MAX/DRAIN = 50t (2.5s) of sprint
STAM_REGEN: int = 1      # stamina gained per tick while resting  -> MAX/REGEN = 100t (5s) to refill
REST_DELAY: int = 20     # ticks after the last sprint before regen starts (1s)
RECOVER_AT: int = 40     # winded players can sprint again once stamina regenerates back to this (hysteresis)


def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    ## Objectives
    write_load_file(f"""
# Stamina system (Black Ops style)
# Distance-sprinted stat (cm) — increments only while the player is sprinting and moving
scoreboard objectives add {ns}.sprint minecraft.custom:minecraft.sprint_one_cm
# Per-player stamina state
scoreboard objectives add {ns}.stam dummy
scoreboard objectives add {ns}.stam_prev dummy
scoreboard objectives add {ns}.stam_rest dummy
scoreboard objectives add {ns}.stam_out dummy
scoreboard objectives add {ns}.stam_seen dummy
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
# First tick in this game (or a fresh late-joiner): start at full stamina. stam_seen is reset to 0
# for everyone at game start (see regen_enable_lines), so this re-inits every game.
execute if score @s {ns}.stam_seen matches 0 run function {ns}:v{version}/player/stamina_init

# Detect sprinting via the distance-sprinted stat delta (cm gained since last tick)
scoreboard players operation #stam_delta {ns}.data = @s {ns}.sprint
scoreboard players operation #stam_delta {ns}.data -= @s {ns}.stam_prev
scoreboard players operation @s {ns}.stam_prev = @s {ns}.sprint

# Sprinting → drain stamina and (re)arm the rest delay before regen can start
execute if score #stam_delta {ns}.data matches 1.. run scoreboard players remove @s {ns}.stam {STAM_DRAIN}
execute if score #stam_delta {ns}.data matches 1.. run scoreboard players set @s {ns}.stam_rest {REST_DELAY}

# Resting → count down the delay, then regen stamina
execute if score #stam_delta {ns}.data matches ..0 if score @s {ns}.stam_rest matches 1.. run scoreboard players remove @s {ns}.stam_rest 1
execute if score #stam_delta {ns}.data matches ..0 if score @s {ns}.stam_rest matches 0 run scoreboard players add @s {ns}.stam {STAM_REGEN}

# Clamp 0..MAX
execute if score @s {ns}.stam matches ..-1 run scoreboard players set @s {ns}.stam 0
execute if score @s {ns}.stam matches {STAM_MAX + 1}.. run scoreboard players set @s {ns}.stam {STAM_MAX}

# Become winded when stamina hits 0; recover once it regenerates back past the hysteresis threshold
execute if score @s {ns}.stam_out matches 0 if score @s {ns}.stam matches 0 run function {ns}:v{version}/player/stamina_wind
execute if score @s {ns}.stam_out matches 1 if score @s {ns}.stam matches {RECOVER_AT}.. run function {ns}:v{version}/player/stamina_recover

# Not winded → keep the hunger bar full while stamina remains. Vanilla sprint exhaustion slowly
# drains real food, which would otherwise lock sprint before OUR meter is actually empty.
execute if score @s {ns}.stam_out matches 0 store result score #stam_food {ns}.data run data get entity @s foodLevel
execute if score @s {ns}.stam_out matches 0 if score #stam_food {ns}.data matches ..19 run effect give @s minecraft:saturation 1 20 true

# While winded, hold the hunger bar at the no-sprint level (foodLevel <= 6). Push down with a short
# hunger pulse while it's still above 6, and clear it once at/below 6 so it can't drain to starvation.
execute if score @s {ns}.stam_out matches 1 run function {ns}:v{version}/player/stamina_hold
""")

    write_versioned_function("player/stamina_init", f"""
scoreboard players set @s {ns}.stam {STAM_MAX}
scoreboard players set @s {ns}.stam_out 0
scoreboard players set @s {ns}.stam_rest 0
scoreboard players operation @s {ns}.stam_prev = @s {ns}.sprint
scoreboard players set @s {ns}.stam_seen 1
""")

    ## Become winded: drop the hunger bar so vanilla disables sprint. Clear the (possibly infinite)
    ## saturation pin so the bar can actually fall, then the hold logic drives it down to ~6.
    write_versioned_function("player/stamina_wind", f"""
scoreboard players set @s {ns}.stam_out 1
effect clear @s minecraft:saturation
# Out-of-breath feedback
playsound minecraft:entity.player.breath player @s ~ ~ ~ 0.5 0.8
title @s actionbar [{{"text":"⚡ ","color":"yellow"}},{{"text":"Out of breath","color":"gray","italic":true}}]
""")

    ## Hold the bar at the no-sprint threshold without draining into starvation territory.
    write_versioned_function("player/stamina_hold", f"""
execute store result score #stam_food {ns}.data run data get entity @s foodLevel
execute if score #stam_food {ns}.data matches 7.. run effect give @s minecraft:hunger 1 255 true
execute if score #stam_food {ns}.data matches ..6 run effect clear @s minecraft:hunger
""")

    ## Recover: clear the drain and refill the hunger bar with a saturation burst so the player can sprint again.
    write_versioned_function("player/stamina_recover", f"""
scoreboard players set @s {ns}.stam_out 0
effect clear @s minecraft:hunger
effect give @s minecraft:saturation 2 20 true
""")
