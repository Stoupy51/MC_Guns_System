
# Imports
import json

from stewbeet import JsonDict, Mem, write_versioned_function


def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    ## Setup scoreboards
    # Per-player config trigger (players use /trigger mgs.player.config set <value>)
    # Per-player toggle scoreboards (0 = disabled, 1 = enabled)
    write_versioned_function("load/confirm_load",
f"""
# Player config: trigger objective for /trigger command
scoreboard objectives add {ns}.player.config trigger

# Per-player toggles (default 0 = disabled)
scoreboard objectives add {ns}.player.hitmarker dummy
scoreboard objectives add {ns}.player.damage_debug dummy
""", prepend=True)

    ## In player tick: enable trigger and process if set
    write_versioned_function("player/tick",
f"""
# Enable /trigger for this player
scoreboard players enable @s {ns}.player.config
execute if score @s {ns}.player.config matches 1.. run function {ns}:v{version}/player/config/process
""")

    ## Process trigger values
    write_versioned_function("player/config/process",
f"""
# 1 = Show config menu
# 2 = Toggle hitmarker sound
# 3 = Toggle damage debug in chat
execute if score @s {ns}.player.config matches 1 run function {ns}:v{version}/player/config/menu
execute if score @s {ns}.player.config matches 2 run function {ns}:v{version}/player/config/toggle_hitmarker
execute if score @s {ns}.player.config matches 3 run function {ns}:v{version}/player/config/toggle_damage_debug

# Reset score
scoreboard players set @s {ns}.player.config 0
""")

    ## Toggle hitmarker
    write_versioned_function("player/config/toggle_hitmarker",
f"""
# If currently OFF (0), turn ON (1)
execute store success score #toggle {ns}.data unless score @s {ns}.player.hitmarker matches 1
execute if score #toggle {ns}.data matches 1 run scoreboard players set @s {ns}.player.hitmarker 1
execute if score #toggle {ns}.data matches 1 run return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Hitmarker sound: ","color":"white"}},{{"text":"ON ✔","color":"green"}}]

# Otherwise it was ON, turn OFF
scoreboard players set @s {ns}.player.hitmarker 0
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Hitmarker sound: ","color":"white"}},{{"text":"OFF ✘","color":"red"}}]
""")

    ## Toggle damage debug
    write_versioned_function("player/config/toggle_damage_debug",
f"""
# If currently OFF (0), turn ON (1)
execute store success score #toggle {ns}.data unless score @s {ns}.player.damage_debug matches 1
execute if score #toggle {ns}.data matches 1 run scoreboard players set @s {ns}.player.damage_debug 1
execute if score #toggle {ns}.data matches 1 run return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Damage debug: ","color":"white"}},{{"text":"ON ✔","color":"green"}}]

# Otherwise it was ON, turn OFF
scoreboard players set @s {ns}.player.damage_debug 0
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Damage debug: ","color":"white"}},{{"text":"OFF ✘","color":"red"}}]
""")

    ## Player config menu (clickable chat buttons)
    def btn(label: str, command: str, color: str = "yellow", hover: str = "") -> str:
        obj: JsonDict = {"text": f"[{label}]", "color": color, "click_event": {"action": "run_command", "command": command}}
        if hover:
            obj["hover_event"] = {"action": "show_text", "value": hover}
        return json.dumps(obj)

    sep = '{"text":"=======================================","color":"dark_gray"}'
    blank = '""'
    title = f'[{blank},{{"text":"       🎮 Player Settings 🎮","color":"gold","bold":true}}]'

    # Hitmarker toggle button
    hm_btn = btn("Toggle", f"/trigger {ns}.player.config set 2", "yellow", "Toggle hitmarker sound on entity hit")
    hm_on  = f'[{blank},{{"text":"  Hitmarker Sound: ","color":"white"}},{{"text":"ON ✔ ","color":"green"}},{hm_btn}]'
    hm_off = f'[{blank},{{"text":"  Hitmarker Sound: ","color":"white"}},{{"text":"OFF ✘ ","color":"red"}},{hm_btn}]'

    # Damage debug toggle button
    dd_btn = btn("Toggle", f"/trigger {ns}.player.config set 3", "yellow", "Toggle damage numbers in chat")
    dd_on  = f'[{blank},{{"text":"  Damage Debug: ","color":"white"}},{{"text":"ON ✔ ","color":"green"}},{dd_btn}]'
    dd_off = f'[{blank},{{"text":"  Damage Debug: ","color":"white"}},{{"text":"OFF ✘ ","color":"red"}},{dd_btn}]'

    # Info line
    info_line = f'[{blank},{{"text":"  Use ","color":"gray","italic":true}},{{"text":"/trigger {ns}.player.config","color":"aqua","italic":true}},{{"text":" to reopen","color":"gray","italic":true}}]'

    write_versioned_function("player/config/menu",
f"""tellraw @s {sep}
tellraw @s {title}
tellraw @s {sep}
execute if score @s {ns}.player.hitmarker matches 1 run tellraw @s {hm_on}
execute unless score @s {ns}.player.hitmarker matches 1 run tellraw @s {hm_off}
execute if score @s {ns}.player.damage_debug matches 1 run tellraw @s {dd_on}
execute unless score @s {ns}.player.damage_debug matches 1 run tellraw @s {dd_off}
tellraw @s {sep}
tellraw @s {info_line}
""")

    write_versioned_function("player/config/damage_debug", f"""
# Damage debug: global config overrides (tellraw @a), otherwise per-player (tellraw to shooter only)
$execute if score #damage_debug {ns}.config matches 1 run tellraw @a [{{"text":"[DMG] ","color":"red"}},{{"text":"$(amount)","color":"gold"}},{{"text":" HP to ","color":"gray"}},{{"selector":"$(target)"}},{{"text":" by ","color":"gray"}},{{"selector":"$(attacker)"}}]
$execute unless score #damage_debug {ns}.config matches 1 if score $(attacker) {ns}.player.damage_debug matches 1 run tellraw $(attacker) [{{"text":"[DMG] ","color":"red"}},{{"text":"$(amount)","color":"gold"}},{{"text":" HP to ","color":"gray"}},{{"selector":"$(target)"}}]
""", tags=[f"{ns}:signals/damage"])  # noqa: E501

    ## Hitmarker sound on entity hit (added to damage signal)
    # Plays for both hitscan (@p[tag=ticking]) and explosion (@p[tag=temp_shooter]) hits
    write_versioned_function("player/config/hitmarker_sound",
f"""
# Play hitmarker sound to the shooter if their personal config has it enabled
# For hitscan: shooter has tag {ns}.ticking
execute as @a[tag={ns}.ticking] if score @s {ns}.player.hitmarker matches 1 at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.5 2.0
# For explosions: shooter has tag {ns}.temp_shooter (skip if already played via ticking)
execute as @a[tag={ns}.temp_shooter,tag=!{ns}.ticking] if score @s {ns}.player.hitmarker matches 1 at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.5 2.0
""", tags=[f"{ns}:signals/damage"])

