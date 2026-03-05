
# Imports
from stewbeet import (
    DamageType,
    Font,
    LootTable,
    Mem,
    set_json_encoder,
    texture_mcmeta,
    write_function,
    write_load_file,
    write_tag,
    write_tick_file,
    write_versioned_function,
)

from ..config.blocks import main as write_block_tags
from ..config.stats import REMAINING_BULLETS


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Write to load file
    write_load_file(
f"""
## Define objectives
scoreboard objectives add {ns}.previous_selected dummy

# Tracks right clicks to enable continuous right-click detection
scoreboard objectives add {ns}.pending_clicks dummy

# Tracks if the player is holding right-click (vs single tap)
scoreboard objectives add {ns}.held_click dummy

# Tracks current burst fire count (resets after BURST shots)
scoreboard objectives add {ns}.burst_count dummy

# Tracks weapon drops to enable fire mode switching
scoreboard objectives add {ns}.dropped minecraft.custom:minecraft.drop

# Cooldown in ticks before being able to shot
scoreboard objectives add {ns}.cooldown dummy

# Tracks weapon-switch-only cooldown (not set when shooting) for zoom shader guard
scoreboard objectives add {ns}.switch_cooldown dummy

# Indicates if the player was zooming (used to remove slowness)
scoreboard objectives add {ns}.zoom dummy

# Tracks continuous zoom duration for delayed scope effect (10-tick delay)
scoreboard objectives add {ns}.zoom_timer dummy

# Tracks the most recently selected weapon ID for weapon switching mechanics
scoreboard objectives add {ns}.last_selected dummy

# Tracks the current amount of bullets in the selected weapon
scoreboard objectives add {ns}.{REMAINING_BULLETS} dummy

# Tracks the total reserve ammo (sum of all magazine bullets in inventory)
# Updated on reload and when player is idle (not shooting for ~60 ticks)
scoreboard objectives add {ns}.reserve_ammo dummy

# Tracks the room acoustics level for crack sound effects
scoreboard objectives add {ns}.acoustics_level dummy

## Global configuration scoreboards (admin/server-level)
# RPG explosion power (0 = no block destruction, higher = more destruction)
scoreboard objectives add {ns}.config dummy

## Per-player special scoreboards (for zombies bonuses, testing, etc.)
# Instant kill: duration in ticks (kills entities in one hit, except {ns}.no_instant_kill tagged)
scoreboard objectives add {ns}.special.instant_kill dummy
# Infinite ammo: duration in ticks (don't consume ammo, set ammo to max capacity)
scoreboard objectives add {ns}.special.infinite_ammo dummy
# Quick reload: percentage faster reload (20 = 20% faster, 50 = 50% faster)
scoreboard objectives add {ns}.special.quick_reload dummy
# Quick swap: percentage faster weapon switch (20 = 20% faster, 50 = 50% faster)
scoreboard objectives add {ns}.special.quick_swap dummy
# DPS tracking: accumulates damage dealt per second, snapshot stored for actionbar
scoreboard objectives add {ns}.dps dummy
scoreboard objectives add {ns}.previous_dps dummy
scoreboard objectives add {ns}.dps_timer dummy


# Define some constants
scoreboard players set #2 {ns}.data 2
scoreboard players set #10 {ns}.data 10
scoreboard players set #100 {ns}.data 100
scoreboard players set #1000 {ns}.data 1000
scoreboard players set #1000000 {ns}.data 1000000

# Initialize slow bullet (projectile) counter
scoreboard players add #slow_bullet_count {ns}.data 0

# Semtex entity pairing: unique ID objective + global counter
scoreboard objectives add {ns}.grenade_launch dummy
scoreboard objectives add {ns}.stuck_id dummy
scoreboard players set #semtex_id {ns}.data 0

# Initialize global config defaults (only if not already set)
execute unless score #projectile_explosion_power {ns}.config matches -2147483648.. run scoreboard players set #projectile_explosion_power {ns}.config 0
execute unless score #grenade_explosion_power {ns}.config matches -2147483648.. run scoreboard players set #grenade_explosion_power {ns}.config 0
execute unless score #max_ammo_reload_weapons {ns}.config matches -2147483648.. run scoreboard players set #max_ammo_reload_weapons {ns}.config 0
execute unless score #damage_debug {ns}.config matches -2147483648.. run scoreboard players set #damage_debug {ns}.config 0
""", prepend=True)

    # Write to tick file
    write_tick_file(
f"""
# Player loop
execute as @e[type=player,sort=random] at @s run function {ns}:v{version}/player/tick
""")

    # Add block tags
    write_block_tags()

    # Loot table for getting username
    Mem.ctx.data[ns].loot_tables["get_username"] = set_json_encoder(LootTable({
        "type": "minecraft:block",
        "pools": [
            {
                "rolls": 1,
                "bonus_rolls": 0,
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": "minecraft:player_head",
                        "functions": [
                            {
                                "function": "minecraft:fill_player_head",
                                "entity": "this"
                            }
                        ]
                    }
                ]
            }
        ]
    }))

    ## Register signal function tags (empty by default, other datapacks can add listeners)
    # These are called at various events in the system, with relevant data stored in mgs:signals storage
    signal_events: list[str] = [
        "on_shoot",             # @s = shooter player, weapon data in mgs:signals
        "on_hit_block",         # @s = raycast marker, block/position/weapon in mgs:signals
        "on_reload",            # @s = reloading player, weapon data in mgs:signals
        "on_zoom",              # @s = zooming player, weapon data in mgs:signals
        "on_unzoom",            # @s = unzooming player, weapon data in mgs:signals
        "on_switch",            # @s = player, weapon data in mgs:signals
        "on_kill",              # @s = killer player, victim/weapon data in mgs:signals
        "damage",           # @s = damaged entity, damage/weapon/attacker in mgs:input with
        "on_explosion",         # @s = projectile entity, explosion data in mgs:signals
        "on_headshot",          # @s = hit entity, damage/weapon in mgs:signals
        "on_fire_mode_change",  # @s = player, weapon/new fire mode in mgs:signals
    ]
    for event in signal_events:
        write_tag(f"signals/{event}", Mem.ctx.data[ns].function_tags, [])

    ## Setup special damage type
    Mem.ctx.data[ns].damage_type["bullet"] = set_json_encoder(DamageType({"exhaustion": 0, "message_id": "player", "scaling": "when_caused_by_living_non_player"}))
    for tag in ["bypasses_cooldown", "no_knockback"]:
        write_tag(tag, Mem.ctx.data["minecraft"].damage_type_tags, [f"{ns}:bullet"])
    write_versioned_function("utils/damage", f"$damage $(target) $(amount) {ns}:bullet by $(attacker)")
    write_versioned_function("utils/signal_and_damage", f"""
function {ns}:v{version}/utils/damage with storage {ns}:input with
function #{ns}:signals/damage with storage {ns}:input with
""")

    # Add bullet font (for actionbar)
    textures_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")
    font: Font = Mem.ctx.assets.fonts.setdefault(f"{ns}:icons", Font({"providers": []}))
    font.data["providers"].extend([
        {"type": "bitmap","file": f"{ns}:font/bullet_full.png","ascent": 7,"height": 9,"chars": ["A"]},
        {"type": "bitmap","file": f"{ns}:font/bullet_outline.png","ascent": 7,"height": 9,"chars": ["B"]},
    ])
    for icon_name in ["bullet_outline", "bullet_full"]:
        Mem.ctx.assets[ns].textures[f"font/{icon_name}"] = texture_mcmeta(f"{textures_folder}/{icon_name}.png")

    # Random weapon function
    write_versioned_function("utils/random_weapon", f"""
execute store result score #random {ns}.data run random value 1..31
$execute if score #random {ns}.data matches 1 run loot replace entity @s $(slot) loot {ns}:i/m16a4
$execute if score #random {ns}.data matches 2 run loot replace entity @s $(slot) loot {ns}:i/m16a4
$execute if score #random {ns}.data matches 3 run loot replace entity @s $(slot) loot {ns}:i/ak47
$execute if score #random {ns}.data matches 4 run loot replace entity @s $(slot) loot {ns}:i/fnfal
$execute if score #random {ns}.data matches 5 run loot replace entity @s $(slot) loot {ns}:i/aug
$execute if score #random {ns}.data matches 6 run loot replace entity @s $(slot) loot {ns}:i/m4a1
$execute if score #random {ns}.data matches 7 run loot replace entity @s $(slot) loot {ns}:i/g3a3
$execute if score #random {ns}.data matches 8 run loot replace entity @s $(slot) loot {ns}:i/famas
$execute if score #random {ns}.data matches 9 run loot replace entity @s $(slot) loot {ns}:i/scar17
$execute if score #random {ns}.data matches 10 run loot replace entity @s $(slot) loot {ns}:i/m1911
$execute if score #random {ns}.data matches 11 run loot replace entity @s $(slot) loot {ns}:i/m9
$execute if score #random {ns}.data matches 12 run loot replace entity @s $(slot) loot {ns}:i/deagle
$execute if score #random {ns}.data matches 13 run loot replace entity @s $(slot) loot {ns}:i/makarov
$execute if score #random {ns}.data matches 14 run loot replace entity @s $(slot) loot {ns}:i/glock17
$execute if score #random {ns}.data matches 15 run loot replace entity @s $(slot) loot {ns}:i/glock18
$execute if score #random {ns}.data matches 16 run loot replace entity @s $(slot) loot {ns}:i/vz61
$execute if score #random {ns}.data matches 17 run loot replace entity @s $(slot) loot {ns}:i/mp5
$execute if score #random {ns}.data matches 18 run loot replace entity @s $(slot) loot {ns}:i/mac10
$execute if score #random {ns}.data matches 19 run loot replace entity @s $(slot) loot {ns}:i/mp7
$execute if score #random {ns}.data matches 20 run loot replace entity @s $(slot) loot {ns}:i/ppsh41
$execute if score #random {ns}.data matches 21 run loot replace entity @s $(slot) loot {ns}:i/sten
$execute if score #random {ns}.data matches 22 run loot replace entity @s $(slot) loot {ns}:i/spas12
$execute if score #random {ns}.data matches 23 run loot replace entity @s $(slot) loot {ns}:i/m500
$execute if score #random {ns}.data matches 24 run loot replace entity @s $(slot) loot {ns}:i/m590
$execute if score #random {ns}.data matches 25 run loot replace entity @s $(slot) loot {ns}:i/svd
$execute if score #random {ns}.data matches 26 run loot replace entity @s $(slot) loot {ns}:i/m82
$execute if score #random {ns}.data matches 27 run loot replace entity @s $(slot) loot {ns}:i/mosin
$execute if score #random {ns}.data matches 28 run loot replace entity @s $(slot) loot {ns}:i/m24
$execute if score #random {ns}.data matches 29 run loot replace entity @s $(slot) loot {ns}:i/rpg7
$execute if score #random {ns}.data matches 30 run loot replace entity @s $(slot) loot {ns}:i/rpk
$execute if score #random {ns}.data matches 31 run loot replace entity @s $(slot) loot {ns}:i/m249
""")

    # Config menu: /function mgs:config
    # Build clickable chat menu for server configuration
    from .helpers import btn as _btn
    def btn(label: str, command: str, color: str = "yellow", hover: str = "") -> str:
        return _btn(label, command, color, hover, action="suggest_command")

    # Separator line
    sep = r'{"text":"============================================","color":"dark_gray"}'

    # Title
    title = '["  ",[{"text":"","color":"gold","bold":true},"     ☣ ",{"text":"MGS Configuration Menu"}," ☣"]]'

    # --- Global Settings ---
    global_header = '["",[{"text":"","color":"aqua","bold":true},"⚙ ",{"text":"Global Settings"}],[{"text":"","color":"gray","italic":true}," (",{"text":"server-wide"},")"]]'

    # RPG Explosion Power
    rpg_btns = ",".join([
        btn(str(i), f"/scoreboard players set #projectile_explosion_power {ns}.config {i}",
            "green" if i == 0 else "yellow",
            f"Set Projectile Explosion Power to {i}" + (" (disabled)" if i == 0 else ""))
        for i in range(6)
    ])
    rpg_line = f'["  ",["",{{"text":"RPG Explosion Power"}},": "],{rpg_btns}]'

    # Grenade Explosion Power
    gren_btns = ",".join([
        btn(str(i), f"/scoreboard players set #grenade_explosion_power {ns}.config {i}",
            "green" if i == 0 else "yellow",
            f"Set Grenade Explosion Power to {i}" + (" (disabled)" if i == 0 else ""))
        for i in range(6)
    ])
    gren_line = f'["  ",["",{{"text":"Grenade Explosion Power"}},": "],{gren_btns}]'

    # Max Ammo Mode: OG (magazines only) or Recent (also reload weapons)
    ma_btns = ",".join([
        btn("OG", f"/scoreboard players set #max_ammo_reload_weapons {ns}.config 0",
            "yellow", "Only refill magazines in inventory (OG zombies)"),
        btn("Recent", f"/scoreboard players set #max_ammo_reload_weapons {ns}.config 1",
            "green", "Also reload current weapon (recent zombies)"),
    ])
    ma_line = f'["  ",["",{{"text":"Max Ammo Mode"}},": "],{ma_btns}]'

    # Damage Debug (global): OFF or ON (tellraw @a all damage)
    dd_btns = ",".join([
        btn("OFF", f"/scoreboard players set #damage_debug {ns}.config 0",
            "red", "Disable global damage debug"),
        btn("ON", f"/scoreboard players set #damage_debug {ns}.config 1",
            "green", "Enable global damage debug (tellraw @a every hit)"),
    ])
    dd_line = f'["  ",["",{{"text":"Damage Debug"}},": "],{dd_btns}]'

    # --- Player Specials ---
    special_header = '["",[{"text":"","color":"aqua","bold":true},"⚡ ",{"text":"Player Specials"}],[{"text":"","color":"gray","italic":true}," (",{"text":"self only"},")"]]'

    # Instant Kill durations: OFF, 10s, 30s, 60s, ∞
    ik_options = [("OFF", 0, "red"), ("10s", 200, "yellow"), ("30s", 600, "yellow"), ("60s", 1200, "yellow"), ("∞", 72000, "light_purple")]
    ik_btns = ",".join([
        btn(label, f"/scoreboard players set @s {ns}.special.instant_kill {ticks}",
            color, f"Set instant kill {'off' if ticks == 0 else f'for {label}'}")
        for label, ticks, color in ik_options
    ])
    ik_line = f'["  ",["",{{"text":"Instant Kill"}},": "],{ik_btns}]'

    # Infinite Ammo durations: OFF, 10s, 30s, 60s, ∞
    ia_options = [("OFF", 0, "red"), ("10s", 200, "yellow"), ("30s", 600, "yellow"), ("60s", 1200, "yellow"), ("∞", 72000, "light_purple")]
    ia_btns = ",".join([
        btn(label, f"/scoreboard players set @s {ns}.special.infinite_ammo {ticks}",
            color, f"Set infinite ammo {'off' if ticks == 0 else f'for {label}'}")
        for label, ticks, color in ia_options
    ])
    ia_line = f'["  ",["",{{"text":"Infinite Ammo"}},": "],{ia_btns}]'

    # Quick Reload: 0%, 20%, 50%, 80%
    qr_options = [("0%", 0, "red"), ("20%", 20, "yellow"), ("50%", 50, "yellow"), ("80%", 80, "green")]
    qr_btns = ",".join([
        btn(label, f"/scoreboard players set @s {ns}.special.quick_reload {val}",
            color, f"Set quick reload to {label}")
        for label, val, color in qr_options
    ])
    qr_line = f'["  ",["",{{"text":"Quick Reload"}},": "],{qr_btns}]'

    # Quick Swap: 0%, 20%, 50%, 80%
    qs_options = [("0%", 0, "red"), ("20%", 20, "yellow"), ("50%", 50, "yellow"), ("80%", 80, "green")]
    qs_btns = ",".join([
        btn(label, f"/scoreboard players set @s {ns}.special.quick_swap {val}",
            color, f"Set quick swap to {label}")
        for label, val, color in qs_options
    ])
    qs_line = f'["  ",["",{{"text":"Quick Swap"}},": "],{qs_btns}]'

    # --- Map Editor ---
    map_header = '[{"text":"","color":"aqua","bold":true},"🗺 ",{"text":"Map Editor"}]'
    map_editor_btn = btn("Open Map Editor", f"/function {ns}:v{version}/maps/editor/menu", "green", "Open the multiplayer map editor")
    map_line = f'["  ",{map_editor_btn}]'

    # --- Multiplayer ---
    mp_header = '[{"text":"","color":"aqua","bold":true},"⚔ ",{"text":"Multiplayer"}]'
    mp_setup_btn = btn("Game Setup", f"/function {ns}:v{version}/multiplayer/setup", "green", "Open the multiplayer game setup menu")
    mp_line = f'["  ",{mp_setup_btn}]'

    write_function(f"{ns}:config",
f"""tellraw @s {sep}
tellraw @s {title}
tellraw @s {sep}
tellraw @s {global_header}
tellraw @s {rpg_line}
tellraw @s {gren_line}
tellraw @s {ma_line}
tellraw @s {dd_line}
tellraw @s ""
tellraw @s {special_header}
tellraw @s {ik_line}
tellraw @s {ia_line}
tellraw @s {qr_line}
tellraw @s {qs_line}
tellraw @s ""
tellraw @s {map_header}
tellraw @s {map_line}
tellraw @s ""
tellraw @s {mp_header}
tellraw @s {mp_line}
tellraw @s {sep}
""")

