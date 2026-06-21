
# ruff: noqa: E501
# Imports

from stewbeet import Mem, write_versioned_function

from .helpers import MGS_TAG
from .multiplayer.classes import CLASS_IDS, CLASSES
from .multiplayer.loadouts import (
    CAMO_VARIANTS,
    GRENADE_TYPES,
    PERKS,
    PRIMARY_WEAPONS,
    SECONDARY_WEAPONS,
    TRIG_DELETE_BASE,
    TRIG_EDIT_BASE,
    TRIG_EDITOR_START,
    TRIG_EQUIP1_CAMO_BASE,
    TRIG_EQUIP2_CAMO_BASE,
    TRIG_EQUIP_SLOT1_BASE,
    TRIG_EQUIP_SLOT2_BASE,
    TRIG_FAVORITE_BASE,
    TRIG_HUB,
    TRIG_HUB_EQUIP1,
    TRIG_HUB_EQUIP2,
    TRIG_HUB_PERKS,
    TRIG_HUB_PRIMARY,
    TRIG_HUB_PRIMARY_MAGS,
    TRIG_HUB_SECONDARY,
    TRIG_HUB_SECONDARY_MAGS,
    TRIG_LIKE_BASE,
    TRIG_MANAGE_BASE,
    TRIG_MARKETPLACE,
    TRIG_MARKETPLACE_ALL,
    TRIG_MARKETPLACE_FAV_ONLY,
    TRIG_MARKETPLACE_LIKES,
    TRIG_MY_LOADOUTS,
    TRIG_MY_LOADOUTS_FAV_ONLY,
    TRIG_OVERKILL_SEC_BASE,
    TRIG_PERK_BASE,
    TRIG_PRIMARY_BASE,
    TRIG_PRIMARY_CAMO_BASE,
    TRIG_PRIMARY_MAGS_BASE,
    TRIG_PRIMARY_SCOPE_BASE,
    TRIG_REMOVE_PRIMARY,
    TRIG_REMOVE_SECONDARY,
    TRIG_SAVE_PRIVATE,
    TRIG_SAVE_PUBLIC,
    TRIG_SECONDARY_BASE,
    TRIG_SECONDARY_CAMO_BASE,
    TRIG_SECONDARY_MAGS_BASE,
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
# Assign unique player ID (Bookshelf SUID) if not yet assigned
execute unless score @s bs.id matches 0.. run function #bs.id:give_suid

# Enable /trigger for this player
scoreboard players enable @s {ns}.player.config
execute if score @s {ns}.player.config matches 1.. run function {ns}:v{version}/player/config/process

# Map editor tick (particles + actionbar) for players in editor mode
execute if score @s {ns}.mp.map_edit matches 1 run function {ns}:v{version}/maps/editor/tick
""")

    ## Process trigger values
    # Pre-compute trigger ranges for custom loadout editor
    primary_max = TRIG_PRIMARY_BASE + len(PRIMARY_WEAPONS) - 1
    secondary_count = len([w for w in SECONDARY_WEAPONS if w.in_loadout])
    secondary_max = TRIG_SECONDARY_BASE + secondary_count - 1
    overkill_sec_max = TRIG_OVERKILL_SEC_BASE + len(PRIMARY_WEAPONS) - 1
    primary_mags_max = TRIG_PRIMARY_MAGS_BASE + 5
    secondary_mags_max = TRIG_SECONDARY_MAGS_BASE + 5
    perk_max = TRIG_PERK_BASE + len(PERKS) - 1
    equip1_max = TRIG_EQUIP_SLOT1_BASE + len(GRENADE_TYPES) - 1
    equip2_max = TRIG_EQUIP_SLOT2_BASE + len(GRENADE_TYPES) - 1
    primary_camo_max = TRIG_PRIMARY_CAMO_BASE + len(CAMO_VARIANTS) - 1
    secondary_camo_max = TRIG_SECONDARY_CAMO_BASE + len(CAMO_VARIANTS) - 1
    equip1_camo_max = TRIG_EQUIP1_CAMO_BASE + len(CAMO_VARIANTS) - 1
    equip2_camo_max = TRIG_EQUIP2_CAMO_BASE + len(CAMO_VARIANTS) - 1
    edit_max = TRIG_EDIT_BASE + 9999
    manage_max = TRIG_MANAGE_BASE + 9999
    select_max = TRIG_SELECT_BASE + 9999  # 10000-wide range per loadout action
    favorite_max = TRIG_FAVORITE_BASE + 9999
    like_max = TRIG_LIKE_BASE + 9999
    delete_max = TRIG_DELETE_BASE + 9999
    toggle_vis_max = TRIG_TOGGLE_VIS_BASE + 9999
    set_default_max = TRIG_SET_DEFAULT_BASE + 9998  # 69999 is reserved for UNSET_DEFAULT

    write_versioned_function("player/config/process", f"""
# Load per-player editor state (isolates simultaneous editors)
execute store result storage {ns}:temp _pid int 1 run scoreboard players get @s bs.id
function {ns}:v{version}/multiplayer/editor/load_state with storage {ns}:temp

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
# === Custom Loadout Editor (CoD-style hub) ===
# 100 = Open loadout editor (create new), then show the hub
execute if score @s {ns}.player.config matches {TRIG_EDITOR_START} run function {ns}:v{version}/multiplayer/editor/start
# 101 = Open marketplace browser
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE} run function {ns}:v{version}/multiplayer/marketplace/browse
# 102 = Open my loadouts manager
execute if score @s {ns}.player.config matches {TRIG_MY_LOADOUTS} run function {ns}:v{version}/multiplayer/my_loadouts/browse
# {TRIG_HUB} = Re-open the editor hub (also the no-op target for grayed-out rows)
execute if score @s {ns}.player.config matches {TRIG_HUB} run function {ns}:v{version}/multiplayer/editor/hub
# Hub category rows → open submenus
execute if score @s {ns}.player.config matches {TRIG_HUB_PRIMARY} run function {ns}:v{version}/multiplayer/editor/show_primary_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_PRIMARY_MAGS} run function {ns}:v{version}/multiplayer/editor/show_primary_mags_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_SECONDARY} run function {ns}:v{version}/multiplayer/editor/show_secondary_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_SECONDARY_MAGS} run function {ns}:v{version}/multiplayer/editor/show_secondary_mags_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_EQUIP1} run function {ns}:v{version}/multiplayer/editor/show_equip_slot1_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_EQUIP2} run function {ns}:v{version}/multiplayer/editor/show_equip_slot2_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_PERKS} run function {ns}:v{version}/multiplayer/editor/show_perks_dialog
# Remove weapon buttons
execute if score @s {ns}.player.config matches {TRIG_REMOVE_PRIMARY} run function {ns}:v{version}/multiplayer/editor/remove_primary
execute if score @s {ns}.player.config matches {TRIG_REMOVE_SECONDARY} run function {ns}:v{version}/multiplayer/editor/remove_secondary
# 200-{primary_max} = Editor: pick primary weapon
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_BASE}..{primary_max} run function {ns}:v{version}/multiplayer/editor/pick_primary
# 230-234 = Editor: pick primary scope
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_SCOPE_BASE}..{TRIG_PRIMARY_SCOPE_BASE + 4} run function {ns}:v{version}/multiplayer/editor/pick_primary_scope
# 250-{secondary_max} = Editor: pick secondary weapon
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_BASE}..{secondary_max} run function {ns}:v{version}/multiplayer/editor/pick_secondary
# {TRIG_OVERKILL_SEC_BASE}-{overkill_sec_max} = Editor: pick a primary as the Overkill secondary
execute if score @s {ns}.player.config matches {TRIG_OVERKILL_SEC_BASE}..{overkill_sec_max} run function {ns}:v{version}/multiplayer/editor/pick_overkill_secondary
# 260-264 = Editor: pick secondary scope
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_SCOPE_BASE}..{TRIG_SECONDARY_SCOPE_BASE + 4} run function {ns}:v{version}/multiplayer/editor/pick_secondary_scope
# 350-351 = Editor: save loadout (350=public, 351=private)
execute if score @s {ns}.player.config matches {TRIG_SAVE_PUBLIC}..{TRIG_SAVE_PRIVATE} run function {ns}:v{version}/multiplayer/editor/save
# {TRIG_PRIMARY_MAGS_BASE+1}-{primary_mags_max} = Editor: pick primary mag count (1-5)
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_MAGS_BASE + 1}..{primary_mags_max} run function {ns}:v{version}/multiplayer/editor/pick_primary_mags
# {TRIG_SECONDARY_MAGS_BASE}-{secondary_mags_max} = Editor: pick secondary mag count (0-5)
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_MAGS_BASE}..{secondary_mags_max} run function {ns}:v{version}/multiplayer/editor/pick_secondary_mags
# {TRIG_PERK_BASE}-{perk_max} = Editor: toggle perk
execute if score @s {ns}.player.config matches {TRIG_PERK_BASE}..{perk_max} run function {ns}:v{version}/multiplayer/editor/pick_perk
# {TRIG_EQUIP_SLOT1_BASE}-{equip1_max} = Editor: pick equipment slot 1 grenade
execute if score @s {ns}.player.config matches {TRIG_EQUIP_SLOT1_BASE}..{equip1_max} run function {ns}:v{version}/multiplayer/editor/pick_equip_slot1
# {TRIG_EQUIP_SLOT2_BASE}-{equip2_max} = Editor: pick equipment slot 2 grenade
execute if score @s {ns}.player.config matches {TRIG_EQUIP_SLOT2_BASE}..{equip2_max} run function {ns}:v{version}/multiplayer/editor/pick_equip_slot2
# {TRIG_PRIMARY_CAMO_BASE}-{primary_camo_max} = Editor: pick primary camo (free)
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_CAMO_BASE}..{primary_camo_max} run function {ns}:v{version}/multiplayer/editor/pick_primary_camo
# {TRIG_SECONDARY_CAMO_BASE}-{secondary_camo_max} = Editor: pick secondary camo (free)
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_CAMO_BASE}..{secondary_camo_max} run function {ns}:v{version}/multiplayer/editor/pick_secondary_camo
# {TRIG_EQUIP1_CAMO_BASE}-{equip1_camo_max} = Editor: pick grenade slot 1 camo (free)
execute if score @s {ns}.player.config matches {TRIG_EQUIP1_CAMO_BASE}..{equip1_camo_max} run function {ns}:v{version}/multiplayer/editor/pick_equip1_camo
# {TRIG_EQUIP2_CAMO_BASE}-{equip2_camo_max} = Editor: pick grenade slot 2 camo (free)
execute if score @s {ns}.player.config matches {TRIG_EQUIP2_CAMO_BASE}..{equip2_camo_max} run function {ns}:v{version}/multiplayer/editor/pick_equip2_camo
# === Custom Loadout Actions ===
# {TRIG_SELECT_BASE}-{select_max} = Select/use a custom loadout
execute if score @s {ns}.player.config matches {TRIG_SELECT_BASE}..{select_max} run function {ns}:v{version}/multiplayer/custom/select
# {TRIG_FAVORITE_BASE}-{favorite_max} = Toggle favorite on a loadout
execute if score @s {ns}.player.config matches {TRIG_FAVORITE_BASE}..{favorite_max} run function {ns}:v{version}/multiplayer/custom/toggle_favorite
# {TRIG_LIKE_BASE}-{like_max} = Like a loadout
execute if score @s {ns}.player.config matches {TRIG_LIKE_BASE}..{like_max} run function {ns}:v{version}/multiplayer/custom/like
# {TRIG_DELETE_BASE}-{delete_max} = Delete own loadout
execute if score @s {ns}.player.config matches {TRIG_DELETE_BASE}..{delete_max} run function {ns}:v{version}/multiplayer/custom/delete
# {TRIG_TOGGLE_VIS_BASE}-{toggle_vis_max} = Toggle public/private on own loadout
execute if score @s {ns}.player.config matches {TRIG_TOGGLE_VIS_BASE}..{toggle_vis_max} run function {ns}:v{version}/multiplayer/custom/toggle_visibility
# {TRIG_SET_DEFAULT_BASE}-{set_default_max} = Set default custom loadout
execute if score @s {ns}.player.config matches {TRIG_SET_DEFAULT_BASE}..{set_default_max} run function {ns}:v{version}/multiplayer/custom/set_default
# {TRIG_UNSET_DEFAULT} = Unset default loadout
execute if score @s {ns}.player.config matches {TRIG_UNSET_DEFAULT} run function {ns}:v{version}/multiplayer/custom/unset_default
# {TRIG_EDIT_BASE}-{edit_max} = Edit own loadout (re-opens the hub pre-filled; saving overwrites)
execute if score @s {ns}.player.config matches {TRIG_EDIT_BASE}..{edit_max} run function {ns}:v{version}/multiplayer/custom/edit
# {TRIG_MANAGE_BASE}-{manage_max} = Open the per-loadout manage submenu (My Loadouts)
execute if score @s {ns}.player.config matches {TRIG_MANAGE_BASE}..{manage_max} run function {ns}:v{version}/multiplayer/my_loadouts/manage
# === Marketplace / My Loadouts Filter & Sort ===
# {TRIG_MARKETPLACE_ALL} = Marketplace: all public (favorites first)
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE_ALL} run function {ns}:v{version}/multiplayer/marketplace/browse
# {TRIG_MARKETPLACE_FAV_ONLY} = Marketplace: only favorited loadouts
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE_FAV_ONLY} run function {ns}:v{version}/multiplayer/marketplace/browse_fav_only
# {TRIG_MARKETPLACE_LIKES} = Marketplace: sorted by most likes
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE_LIKES} run function {ns}:v{version}/multiplayer/marketplace/browse_likes
# {TRIG_MY_LOADOUTS_FAV_ONLY} = My Loadouts: favorites only
execute if score @s {ns}.player.config matches {TRIG_MY_LOADOUTS_FAV_ONLY} run function {ns}:v{version}/multiplayer/my_loadouts/browse_fav_only

# Save per-player editor state back to isolated storage
function {ns}:v{version}/multiplayer/editor/save_state with storage {ns}:temp

# Reset score
scoreboard players set @s {ns}.player.config 0
""")

    ## Toggle functions (hitmarker, damage_debug)
    for score_name, display_name in [("hitmarker", "Hitmarker Sound"), ("damage_debug", "Damage Debug")]:
        write_versioned_function(f"player/config/toggle_{score_name}", f"""
# Flip the toggle: #toggle = 1 when it was OFF (so we turn it ON), 0 when it was already ON
execute store success score #toggle {ns}.data unless score @s {ns}.player.{score_name} matches 1
execute if score #toggle {ns}.data matches 1 run scoreboard players set @s {ns}.player.{score_name} 1
execute unless score #toggle {ns}.data matches 1 run scoreboard players set @s {ns}.player.{score_name} 0
execute if score #toggle {ns}.data matches 1 run tellraw @s [{MGS_TAG},["",{{"text":"{display_name}"}},": "],{{"text":"ON","color":"green"}},{{"text":" ✔","color":"green"}}]
execute unless score #toggle {ns}.data matches 1 run tellraw @s [{MGS_TAG},["",{{"text":"{display_name}"}},": "],{{"text":"OFF","color":"red"}},{{"text":" ✘","color":"red"}}]

# Reopen the settings dialog so the updated state is reflected immediately
function {ns}:v{version}/player/config/menu
""")

    ## Player config menu — a quick-action dialog (built per-player so toggle states show live).
    ## Replaces the old clickable-chat menu: /trigger set 1 now opens this dialog instead.
    write_versioned_function("player/config/menu", f"""
# Build the Player Settings dialog in storage, then show it via /dialog
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:{{text:"🎮 Player Settings",color:"gold",bold:true}},body:[{{type:"minecraft:plain_message",contents:{{text:"Toggle your personal settings","color":"gray"}}}}],actions:[],columns:1,after_action:"close",exit_action:{{label:{{translate:"gui.done"}}}}}}

# Hitmarker Sound toggle (label reflects the current ON/OFF state)
execute if score @s {ns}.player.hitmarker matches 1 run data modify storage {ns}:temp dialog.actions append value {{label:["",{{text:"Hitmarker Sound: "}},{{text:"ON ✔",color:"green"}}],tooltip:{{text:"Toggle hitmarker sound on entity hit"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 2"}}}}
execute unless score @s {ns}.player.hitmarker matches 1 run data modify storage {ns}:temp dialog.actions append value {{label:["",{{text:"Hitmarker Sound: "}},{{text:"OFF ✘",color:"red"}}],tooltip:{{text:"Toggle hitmarker sound on entity hit"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 2"}}}}

# Damage Debug toggle
execute if score @s {ns}.player.damage_debug matches 1 run data modify storage {ns}:temp dialog.actions append value {{label:["",{{text:"Damage Debug: "}},{{text:"ON ✔",color:"green"}}],tooltip:{{text:"Toggle damage numbers in chat"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 3"}}}}
execute unless score @s {ns}.player.damage_debug matches 1 run data modify storage {ns}:temp dialog.actions append value {{label:["",{{text:"Damage Debug: "}},{{text:"OFF ✘",color:"red"}}],tooltip:{{text:"Toggle damage numbers in chat"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 3"}}}}

# Multiplayer class selection
data modify storage {ns}:temp dialog.actions append value {{label:[{{text:"⚔ ",color:"aqua",bold:true}},{{text:"Multiplayer Class"}}],tooltip:{{text:"Open multiplayer class selection menu"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 4"}}}}

# Show the completed dialog (reuses the multiplayer show_dialog macro)
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
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
$execute if score #damage_debug {ns}.config matches 1 run tellraw @a ["",[{{"text":"","color":"red"}},"[",{{"text":"DMG"}},"] "],[{{"score":{{"name":"#dmg_whole","objective":"{ns}.data"}},"color":"gold"}},".",{{"score":{{"name":"#dmg_dec","objective":"{ns}.data"}}}}]," ",{{"text":"HP to","color":"gray"}}," ",{{"selector":"$(target)"}}," ",{{"text":"by","color":"gray"}}," ",{{"selector":"$(attacker)"}}]
$execute unless score #damage_debug {ns}.config matches 1 at @s as $(attacker) if score @s {ns}.player.damage_debug matches 1 run tellraw @s ["",[{{"text":"","color":"red"}},"[",{{"text":"DMG"}},"] "],[{{"score":{{"name":"#dmg_whole","objective":"{ns}.data"}},"color":"gold"}},".",{{"score":{{"name":"#dmg_dec","objective":"{ns}.data"}}}}]," ",{{"text":"HP to","color":"gray"}}," ",{{"selector":"@n"}}]
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
