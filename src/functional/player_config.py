
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from .helpers import MGS_TAG
from .multiplayer.classes import CLASS_IDS, CLASSES
from .multiplayer.loadouts import (
    GRENADE_TYPES,
    PERKS,
    PRIMARY_WEAPONS,
    TRIG_BACK_EQUIPMENT,
    TRIG_BACK_PERKS,
    TRIG_BACK_SECONDARY,
    TRIG_DELETE_BASE,
    TRIG_EDITOR_START,
    TRIG_EQUIP_SLOT1_BASE,
    TRIG_EQUIP_SLOT2_BASE,
    TRIG_FAVORITE_BASE,
    TRIG_LIKE_BASE,
    TRIG_MARKETPLACE,
    TRIG_MARKETPLACE_ALL,
    TRIG_MARKETPLACE_FAV_ONLY,
    TRIG_MARKETPLACE_LIKES,
    TRIG_MY_LOADOUTS,
    TRIG_MY_LOADOUTS_FAV_ONLY,
    TRIG_PERK_BASE,
    TRIG_PERKS_DONE,
    TRIG_PRIMARY_BASE,
    TRIG_PRIMARY_MAGS_BASE,
    TRIG_PRIMARY_SCOPE_BASE,
    TRIG_SAVE_PRIVATE,
    TRIG_SAVE_PUBLIC,
    TRIG_SECONDARY_BASE,
    TRIG_SECONDARY_MAGS_BASE,
    TRIG_SECONDARY_NONE,
    TRIG_SECONDARY_SCOPE_BASE,
    TRIG_SELECT_BASE,
    TRIG_SET_DEFAULT_BASE,
    TRIG_TOGGLE_VIS_BASE,
    TRIG_UNSET_DEFAULT,
)


def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    ## Setup scoreboards
    # Per-player config trigger (players use /trigger mgs.player.config set <value>)
    # Per-player toggle scoreboards (0 = disabled, 1 = enabled)
    write_versioned_function("load/confirm_load", f"""
# Player config: trigger objective for /trigger command
scoreboard objectives add {ns}.player.config trigger

# Per-player toggles (default 0 = disabled)
scoreboard objectives add {ns}.player.hitmarker dummy
scoreboard objectives add {ns}.player.damage_debug dummy
""", prepend=True)

    ## In player tick: enable trigger and process if set
    write_versioned_function("player/tick", f"""
# Enable /trigger for this player
scoreboard players enable @s {ns}.player.config
execute if score @s {ns}.player.config matches 1.. run function {ns}:v{version}/player/config/process

# Map editor tick (particles + actionbar) for players in editor mode
execute if score @s {ns}.mp.map_edit matches 1 run function {ns}:v{version}/maps/editor/tick
""")

    ## Process trigger values
    # Pre-compute trigger ranges for custom loadout editor
    primary_max = TRIG_PRIMARY_BASE + len(PRIMARY_WEAPONS) - 1
    primary_mags_max = TRIG_PRIMARY_MAGS_BASE + 5
    secondary_mags_max = TRIG_SECONDARY_MAGS_BASE + 5
    perk_max = TRIG_PERK_BASE + len(PERKS) - 1
    equip1_max = TRIG_EQUIP_SLOT1_BASE + len(GRENADE_TYPES) - 1
    equip2_max = TRIG_EQUIP_SLOT2_BASE + len(GRENADE_TYPES) - 1
    select_max = TRIG_SELECT_BASE + 99  # Max 99 custom loadouts
    favorite_max = TRIG_FAVORITE_BASE + 99
    like_max = TRIG_LIKE_BASE + 99
    delete_max = TRIG_DELETE_BASE + 99
    toggle_vis_max = TRIG_TOGGLE_VIS_BASE + 99
    set_default_max = TRIG_SET_DEFAULT_BASE + 99

    write_versioned_function("player/config/process", f"""
# 1 = Show config menu
# 2 = Toggle hitmarker Sound
# 3 = Toggle damage debug in chat
# 4 = Open multiplayer class selection menu
# 6-9 = Zombies perk selection (passive/ability via trigger from dialog)
# 11-20 = Select class 1-10 (via trigger from class menu)
execute if score @s {ns}.player.config matches 1 run function {ns}:v{version}/player/config/menu
execute if score @s {ns}.player.config matches 2 run function {ns}:v{version}/player/config/toggle_hitmarker
execute if score @s {ns}.player.config matches 3 run function {ns}:v{version}/player/config/toggle_damage_debug
execute if score @s {ns}.player.config matches 4 run function {ns}:v{version}/multiplayer/select_class
execute if score @s {ns}.player.config matches 5 run function {ns}:v{version}/zombies/passive_ability_menu
execute if score @s {ns}.player.config matches 6 run function {ns}:v{version}/zombies/perks/set_passive_1
execute if score @s {ns}.player.config matches 7 run function {ns}:v{version}/zombies/perks/set_passive_2
execute if score @s {ns}.player.config matches 8 run function {ns}:v{version}/zombies/perks/set_ability_1
execute if score @s {ns}.player.config matches 9 run function {ns}:v{version}/zombies/perks/set_ability_2
{"".join(f'execute if score @s {ns}.player.config matches {10 + class_num} run function {ns}:v{version}/multiplayer/set_class {{class_num:{class_num},class_name:"{CLASSES[class_id]["name"]}"}}{chr(10)}' for class_id, class_num in CLASS_IDS.items())}
# === Custom Loadout Editor ===
# 100 = Open loadout editor (create new)
execute if score @s {ns}.player.config matches {TRIG_EDITOR_START} run function {ns}:v{version}/multiplayer/editor/start
# 101 = Open marketplace browser
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE} run function {ns}:v{version}/multiplayer/marketplace/browse
# 102 = Open my loadouts manager
execute if score @s {ns}.player.config matches {TRIG_MY_LOADOUTS} run function {ns}:v{version}/multiplayer/my_loadouts/browse
# 200-{primary_max} = Editor: pick primary weapon
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_BASE}..{primary_max} run function {ns}:v{version}/multiplayer/editor/pick_primary
# 230-234 = Editor: pick primary scope
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_SCOPE_BASE}..{TRIG_PRIMARY_SCOPE_BASE + 4} run function {ns}:v{version}/multiplayer/editor/pick_primary_scope
# 250-{TRIG_SECONDARY_NONE} = Editor: pick secondary weapon (258 = none)
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_BASE}..{TRIG_SECONDARY_NONE} run function {ns}:v{version}/multiplayer/editor/pick_secondary
# 260-264 = Editor: pick secondary scope
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_SCOPE_BASE}..{TRIG_SECONDARY_SCOPE_BASE + 4} run function {ns}:v{version}/multiplayer/editor/pick_secondary_scope
# 350-351 = Editor: save loadout (350=public, 351=private)
execute if score @s {ns}.player.config matches {TRIG_SAVE_PUBLIC}..{TRIG_SAVE_PRIVATE} run function {ns}:v{version}/multiplayer/editor/save
# 360 = Back to secondary weapon dialog (refunds secondary weapon + scope costs)
execute if score @s {ns}.player.config matches {TRIG_BACK_SECONDARY} run function {ns}:v{version}/multiplayer/editor/back_to_secondary
# 370 = Back from equipment area: if in perks step (9) refund equip_slot2+perks, else refund equip_slot1 and go to slot1 dialog
execute if score @s {ns}.player.config matches {TRIG_BACK_EQUIPMENT} if score @s {ns}.mp.edit_step matches 9 run function {ns}:v{version}/multiplayer/editor/back_from_perks
execute if score @s {ns}.player.config matches {TRIG_BACK_EQUIPMENT} unless score @s {ns}.mp.edit_step matches 9 run function {ns}:v{version}/multiplayer/editor/back_to_equip1
# 380 = Back to perks dialog
execute if score @s {ns}.player.config matches {TRIG_BACK_PERKS} run function {ns}:v{version}/multiplayer/editor/show_perks_dialog
# {TRIG_PRIMARY_MAGS_BASE+1}-{primary_mags_max} = Editor: pick primary mag count (1-5)
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_MAGS_BASE + 1}..{primary_mags_max} run function {ns}:v{version}/multiplayer/editor/pick_primary_mags
# {TRIG_SECONDARY_MAGS_BASE}-{secondary_mags_max} = Editor: pick secondary mag count (0-5)
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_MAGS_BASE}..{secondary_mags_max} run function {ns}:v{version}/multiplayer/editor/pick_secondary_mags
# {TRIG_PERK_BASE}-{perk_max} = Editor: toggle perk
execute if score @s {ns}.player.config matches {TRIG_PERK_BASE}..{perk_max} run function {ns}:v{version}/multiplayer/editor/pick_perk
# {TRIG_PERKS_DONE} = Editor: done selecting perks → show confirm
execute if score @s {ns}.player.config matches {TRIG_PERKS_DONE} run function {ns}:v{version}/multiplayer/editor/perks_done
# {TRIG_EQUIP_SLOT1_BASE}-{equip1_max} = Editor: pick equipment slot 1 grenade
execute if score @s {ns}.player.config matches {TRIG_EQUIP_SLOT1_BASE}..{equip1_max} run function {ns}:v{version}/multiplayer/editor/pick_equip_slot1
# {TRIG_EQUIP_SLOT2_BASE}-{equip2_max} = Editor: pick equipment slot 2 grenade
execute if score @s {ns}.player.config matches {TRIG_EQUIP_SLOT2_BASE}..{equip2_max} run function {ns}:v{version}/multiplayer/editor/pick_equip_slot2
# === Custom Loadout Actions ===
# 1000-1099 = Select/use a custom loadout
execute if score @s {ns}.player.config matches {TRIG_SELECT_BASE}..{select_max} run function {ns}:v{version}/multiplayer/custom/select
# 1100-1199 = Toggle favorite on a loadout
execute if score @s {ns}.player.config matches {TRIG_FAVORITE_BASE}..{favorite_max} run function {ns}:v{version}/multiplayer/custom/toggle_favorite
# 1200-1299 = Like a loadout
execute if score @s {ns}.player.config matches {TRIG_LIKE_BASE}..{like_max} run function {ns}:v{version}/multiplayer/custom/like
# 1300-1399 = Delete own loadout
execute if score @s {ns}.player.config matches {TRIG_DELETE_BASE}..{delete_max} run function {ns}:v{version}/multiplayer/custom/delete
# 1400-1499 = Toggle public/private on own loadout
execute if score @s {ns}.player.config matches {TRIG_TOGGLE_VIS_BASE}..{toggle_vis_max} run function {ns}:v{version}/multiplayer/custom/toggle_visibility
# 1500-1598 = Set default custom loadout
execute if score @s {ns}.player.config matches {TRIG_SET_DEFAULT_BASE}..{set_default_max} run function {ns}:v{version}/multiplayer/custom/set_default
# 1599 = Unset default loadout
execute if score @s {ns}.player.config matches {TRIG_UNSET_DEFAULT} run function {ns}:v{version}/multiplayer/custom/unset_default
# === Marketplace / My Loadouts Filter & Sort ===
# {TRIG_MARKETPLACE_ALL} = Marketplace: all public (favorites first)
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE_ALL} run function {ns}:v{version}/multiplayer/marketplace/browse
# {TRIG_MARKETPLACE_FAV_ONLY} = Marketplace: only favorited loadouts
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE_FAV_ONLY} run function {ns}:v{version}/multiplayer/marketplace/browse_fav_only
# {TRIG_MARKETPLACE_LIKES} = Marketplace: sorted by most likes
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE_LIKES} run function {ns}:v{version}/multiplayer/marketplace/browse_likes
# {TRIG_MY_LOADOUTS_FAV_ONLY} = My Loadouts: favorites only
execute if score @s {ns}.player.config matches {TRIG_MY_LOADOUTS_FAV_ONLY} run function {ns}:v{version}/multiplayer/my_loadouts/browse_fav_only

# Reset score
scoreboard players set @s {ns}.player.config 0
""")

    ## Toggle functions (hitmarker, damage_debug)
    for score_name, display_name in [("hitmarker", "Hitmarker Sound"), ("damage_debug", "Damage Debug")]:
        write_versioned_function(f"player/config/toggle_{score_name}", f"""
# If currently OFF (0), turn ON (1)
execute store success score #toggle {ns}.data unless score @s {ns}.player.{score_name} matches 1
execute if score #toggle {ns}.data matches 1 run scoreboard players set @s {ns}.player.{score_name} 1
execute if score #toggle {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},["",{{"text":"{display_name}"}},": "],{{"text":"ON","color":"green"}},{{"text":" ✔","color":"green"}}]

# Otherwise it was ON, turn OFF
scoreboard players set @s {ns}.player.{score_name} 0
tellraw @s [{MGS_TAG},["",{{"text":"{display_name}"}},": "],{{"text":"OFF","color":"red"}},{{"text":" ✘","color":"red"}}]
""")

    ## Player config menu (clickable chat buttons)
    from .helpers import btn

    sep = '{"text":"=======================================","color":"dark_gray"}'
    title = '["",[{"text":"","color":"gold","bold":true},"       🎮 ",{"text":"Player Settings"}," 🎮"]]'

    # Hitmarker toggle button
    hm_btn = btn("Toggle", f"/trigger {ns}.player.config set 2", "yellow", "Toggle hitmarker Sound on entity hit")
    hm_on  = f'["  ",["",{{"text":"Hitmarker Sound"}},": "],{{"text":"ON","color":"green"}},{{"text":" ✔ ","color":"green"}},{hm_btn}]'
    hm_off = f'["  ",["",{{"text":"Hitmarker Sound"}},": "],{{"text":"OFF","color":"red"}},{{"text":" ✘","color":"red"}},{hm_btn}]'

    # Damage Debug toggle button
    dd_btn = btn("Toggle", f"/trigger {ns}.player.config set 3", "yellow", "Toggle damage numbers in chat")
    dd_on  = f'["  ",["",{{"text":"Damage Debug"}},": "],{{"text":"ON","color":"green"}},{{"text":" ✔ ","color":"green"}},{dd_btn}]'
    dd_off = f'["  ",["",{{"text":"Damage Debug"}},": "],{{"text":"OFF","color":"red"}},{{"text":" ✘","color":"red"}},{dd_btn}]'

    # Multiplayer class selection button
    mp_btn = btn("Select Class", f"/trigger {ns}.player.config set 4", "aqua", "Open multiplayer class selection menu")
    mp_line = f'["  ",["",{{"text":"Multiplayer"}},": "],{mp_btn}]'

    # Info line
    info_line = f'["  ",{{"text":"Use ","color":"gray","italic":true}},{{"text":"/trigger {ns}.player.config","color":"aqua","italic":true}},{{"text":" to reopen","color":"gray","italic":true}}]'

    write_versioned_function("player/config/menu", f"""tellraw @s {sep}
tellraw @s {title}
tellraw @s {sep}
execute if score @s {ns}.player.hitmarker matches 1 run tellraw @s {hm_on}
execute unless score @s {ns}.player.hitmarker matches 1 run tellraw @s {hm_off}
execute if score @s {ns}.player.damage_debug matches 1 run tellraw @s {dd_on}
execute unless score @s {ns}.player.damage_debug matches 1 run tellraw @s {dd_off}
tellraw @s {mp_line}
tellraw @s {sep}
tellraw @s {info_line}
""")

    write_versioned_function("player/config/damage_debug", f"""
# Round amount to 1 decimal: store (amount * 10) as int score, then split into whole + decimal parts
$data modify storage {ns}:temp amount set value $(amount)
execute store result score #dmg_x10 {ns}.data run data get storage {ns}:temp amount 10
scoreboard players operation #dmg_whole {ns}.data = #dmg_x10 {ns}.data
scoreboard players operation #dmg_whole {ns}.data /= #10 {ns}.data
scoreboard players operation #dmg_dec {ns}.data = #dmg_x10 {ns}.data
scoreboard players operation #dmg_dec {ns}.data %= #10 {ns}.data

# Damage Debug: global config overrides (tellraw @a), otherwise per-player (tellraw to shooter only)
$execute if score #damage_debug {ns}.config matches 1 run tellraw @a ["",[{{"text":"","color":"red"}},"[",{{"text":"DMG"}},"] "],[{{"score":{{"name":"#dmg_whole","objective":"{ns}.data"}},"color":"gold"}},".",{{"score":{{"name":"#dmg_dec","objective":"{ns}.data"}}}}],{{"text":" HP to ","color":"gray"}},{{"selector":"$(target)"}},{{"text":" by ","color":"gray"}},{{"selector":"$(attacker)"}}]
$execute unless score #damage_debug {ns}.config matches 1 at @s as $(attacker) if score @s {ns}.player.damage_debug matches 1 run tellraw @s ["",[{{"text":"","color":"red"}},"[",{{"text":"DMG"}},"] "],[{{"score":{{"name":"#dmg_whole","objective":"{ns}.data"}},"color":"gold"}},".",{{"score":{{"name":"#dmg_dec","objective":"{ns}.data"}}}}],{{"text":" HP to ","color":"gray"}},{{"selector":"@n"}}]
""", tags=[f"{ns}:signals/damage"])

    ## Hitmarker Sound on entity hit (added to damage signal)
    # Plays for both hitscan (@p[tag=ticking]) and explosion (@p[tag=temp_shooter]) hits
    write_versioned_function("player/config/hitmarker_sound", f"""
# Play hitmarker Sound to the shooter if their personal config has it enabled
# For hitscan: shooter has tag {ns}.ticking
execute as @a[tag={ns}.ticking] if score @s {ns}.player.hitmarker matches 1 at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1.0 2.0
# For explosions: shooter has tag {ns}.temp_shooter (skip if already played via ticking)
execute as @a[tag={ns}.temp_shooter,tag=!{ns}.ticking] if score @s {ns}.player.hitmarker matches 1 at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1.0 2.0
""", tags=[f"{ns}:signals/damage"])

