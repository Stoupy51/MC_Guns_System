# Imports
from stewbeet import DamageType, Font, LootTable, Mem, set_json_encoder, texture_mcmeta, write_function, write_load_file, write_tag, write_tick_file, write_versioned_function

from ..config.blocks import main as write_block_tags
from ..config.stats import REMAINING_BULLETS

# Main function


def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Write to load file
    write_load_file(f"""
## Define objectives
# Used to tag players that should be selected by Multiplayer/Mission/Zombies functions (@a)
# We use a scoreboard instead of tag so we can reset offline players
scoreboard objectives add {ns}.player dummy

# Tracks the currently selected weapon ID for each player
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

# Tracks how much time has passed since the player last saw a muzzle flash
scoreboard objectives add {ns}.last_muzzle_flash dummy

## Global configuration scoreboards (admin/server-level)
# RPG explosion power (0 = no block destruction, higher = more destruction)
scoreboard objectives add {ns}.config dummy

## Per-player special scoreboards (for zombies bonuses, testing, etc.)
# Instant kill: duration in ticks (kills entities in one hit, except {ns}.no_instant_kill tagged)
scoreboard objectives add {ns}.special.instant_kill dummy
# Infinite ammo: duration in ticks (don't consume ammo, set ammo to max capacity)
scoreboard objectives add {ns}.special.infinite_ammo dummy
# Double points: duration in ticks (double points earned from kills/hits in zombies)
scoreboard objectives add {ns}.special.double_points dummy
# Quick reload: percentage faster reload (20 = 20% faster, 50 = 50% faster)
scoreboard objectives add {ns}.special.quick_reload dummy
# Quick swap: percentage faster weapon switch (20 = 20% faster, 50 = 50% faster)
scoreboard objectives add {ns}.special.quick_swap dummy
# Additional shots: number of extra projectiles per shot (Double Tap perk)
scoreboard objectives add {ns}.special.additional_shots dummy
# Multiplayer loadout perk flags (0/1), set on loadout apply
scoreboard objectives add {ns}.special.juggernaut dummy
scoreboard objectives add {ns}.special.scavenger dummy
scoreboard objectives add {ns}.special.flak_jacket dummy
scoreboard objectives add {ns}.special.tracker dummy
scoreboard objectives add {ns}.special.tactical_mask dummy
scoreboard objectives add {ns}.special.overkill dummy
scoreboard objectives add {ns}.special.quick_fix dummy
# DPS tracking: accumulates damage dealt per second, snapshot stored for actionbar
scoreboard objectives add {ns}.dps dummy
scoreboard objectives add {ns}.previous_dps dummy
scoreboard objectives add {ns}.dps_timer dummy

# Forces an immediate actionbar refresh (set by events its idle gate can't detect, e.g. fire-mode toggle)
scoreboard objectives add {ns}.ab_force dummy


# Initialize slow bullet (projectile) counter
scoreboard players add #slow_bullet_count {ns}.data 0

# Semtex entity pairing: unique ID objective + global counter
scoreboard objectives add {ns}.grenade_launch dummy
scoreboard objectives add {ns}.stuck_id dummy

# Per-grenade accumulated tumble angle (1e-4 rad units)
scoreboard objectives add {ns}.grenade_spin dummy
scoreboard players set #semtex_id {ns}.data 0

# Initialize global config defaults (only if not already set)
execute unless score #projectile_explosion_power {ns}.config matches -2147483648.. run scoreboard players set #projectile_explosion_power {ns}.config 0
execute unless score #grenade_explosion_power {ns}.config matches -2147483648.. run scoreboard players set #grenade_explosion_power {ns}.config 0
execute unless score #max_ammo_reload_weapons {ns}.config matches -2147483648.. run scoreboard players set #max_ammo_reload_weapons {ns}.config 0
execute unless score #damage_debug {ns}.config matches -2147483648.. run scoreboard players set #damage_debug {ns}.config 0

# Health regeneration tracking (global, shared across all game modes)
scoreboard objectives add {ns}.last_hit dummy
scoreboard objectives add {ns}.hp_prev dummy

# Read-only criteria objectives, auto-updated by the server every tick a value changes.
# Reading these replaces per-tick `data get entity @s Health/foodLevel` (full player-NBT
# serialization) with a plain score read. NOTE: {ns}.health = ceil(health + absorption);
# this pack has no absorption sources, so it tracks health exactly.
scoreboard objectives add {ns}.health health
scoreboard objectives add {ns}.food food

# Real-time clock: global stopwatch queried every tick (lag-immune wall-clock time).
# Recreated on every load — only per-tick deltas are consumed, so the reset is harmless.
stopwatch remove {ns}:clock
stopwatch create {ns}:clock
scoreboard players set #real_prev {ns}.data 0
""", prepend=True)

    # Write to tick file
    write_tick_file(
f"""
# Infinitely incrementing tick counter for general timing purposes
scoreboard players add #total_tick {ns}.data 1

# Real-time tick equivalents from the {ns}:clock stopwatch (scale 20 = seconds x20).
# #tick_delta = real ticks elapsed since the previous game tick: ~1 at 20 TPS, 2+ under lag.
# Mode timers subtract #tick_delta instead of 1 so durations stay wall-clock accurate.
# No lower clamp to 1: ms rounding jitters deltas between 0/1/2 but their SUM stays exact.
# Upper clamp 40 (2s) bounds the jump after a singleplayer pause or a world freeze.
execute store result score #real_tick {ns}.data run stopwatch query {ns}:clock 20
scoreboard players operation #tick_delta {ns}.data = #real_tick {ns}.data
scoreboard players operation #tick_delta {ns}.data -= #real_prev {ns}.data
scoreboard players operation #real_prev {ns}.data = #real_tick {ns}.data
execute unless score #tick_delta {ns}.data matches 0.. run scoreboard players set #tick_delta {ns}.data 0
execute if score #tick_delta {ns}.data matches 41.. run scoreboard players set #tick_delta {ns}.data 40

# Player loop
execute as @e[type=player,sort=random] at @s run function {ns}:v{version}/player/tick
""")

    # Health regeneration tick hook (global — only runs during an active game)
    write_versioned_function("player/tick", f"""
# Health regeneration: Black Ops style — only active during a game
execute if score #any_game_active {ns}.data matches 1 run function {ns}:v{version}/player/regen_tick
""")

    write_versioned_function("player/regen_tick", f"""
# @s = any player during an active game
# Damage detection via the auto-updated 'health' criterion (no player-NBT read)
execute if score @s {ns}.health < @s {ns}.hp_prev run scoreboard players set @s {ns}.last_hit 0
execute unless score @s {ns}.health < @s {ns}.hp_prev run scoreboard players add @s {ns}.last_hit 1
scoreboard players operation @s {ns}.hp_prev = @s {ns}.health
execute unless score @s {ns}.last_hit matches 100.. run return 0

# At full health there is nothing to refresh; a still-running 3s pulse finishes any half-heart
# (regeneration can't overheal, so letting it expire replaces the old per-tick `effect clear`)
execute store result score #hp_max {ns}.data run attribute @s minecraft:max_health get 1
execute if score @s {ns}.health >= #hp_max {ns}.data run return 0
effect give @s minecraft:regeneration 3 2 true
""")

    # Add block tags
    write_block_tags()

    # Entity tags to ignore when shooting
    write_tag(f"{ns}:ignore", Mem.ctx.data.entity_type_tags, ["#bs.hitbox:intangible", "minecraft:interaction", "minecraft:experience_orb"])

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
    # Unattributed variant: no "by <attacker>", so team friendlyFire=false can't cancel it
    # (used for self-inflicted explosion damage, where the shooter and victim share a team).
    write_versioned_function("utils/damage_plain", "$damage $(target) $(amount) minecraft:explosion")
    write_versioned_function("utils/signal_and_damage", f"""
# Check if target is a player in active MP game and damage would be lethal -> simulate death
execute store result score #incoming_dmg {ns}.data run data get storage {ns}:input with.amount 10
execute store result score #victim_hp {ns}.data run data get entity @s Health 10
execute if entity @s[type=player,scores={{{ns}.mp.in_game=1..}}] if score #incoming_dmg {ns}.data >= #victim_hp {ns}.data run return run function {ns}:v{version}/multiplayer/simulate_death

# Non-lethal or non-MP: normal damage + signals
function {ns}:v{version}/utils/damage with storage {ns}:input with
function #{ns}:signals/damage with storage {ns}:input with
""")
    # Same flow as signal_and_damage but applies plain (unattributed) damage.
    write_versioned_function("utils/signal_and_damage_plain", f"""
# Check if target is a player in active MP game and damage would be lethal -> simulate death
execute store result score #incoming_dmg {ns}.data run data get storage {ns}:input with.amount 10
execute store result score #victim_hp {ns}.data run data get entity @s Health 10
execute if entity @s[type=player,scores={{{ns}.mp.in_game=1..}}] if score #incoming_dmg {ns}.data >= #victim_hp {ns}.data run return run function {ns}:v{version}/multiplayer/simulate_death

# Non-lethal or non-MP: plain damage + signals
function {ns}:v{version}/utils/damage_plain with storage {ns}:input with
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
    # A dialog-based settings menu (replaces the old clickable-chat tellraw menu).
    # The main dialog lists every setting as a button that opens its own sub-dialog of value
    # buttons; picking a value runs the scoreboard command directly. Each value button is
    # independent (no submit step), so opening the menu never resets untouched settings — the
    # same "click the value you want" model as the old menu, just rendered as native dialogs.
    from .helpers import dialog_back_action, dialog_function, dialog_run_btn, dialog_show_btn, register_dialog, register_value_picker, split_emoji

    # --- Global Settings (server-wide fake-player scores) ---
    rpg_opts = [
        (str(i), f"/scoreboard players set #projectile_explosion_power {ns}.config {i}",
         "green" if i == 0 else "yellow",
         f"Set Projectile Explosion Power to {i}" + (" (disabled)" if i == 0 else ""))
        for i in range(6)
    ]
    gren_opts = [
        (str(i), f"/scoreboard players set #grenade_explosion_power {ns}.config {i}",
         "green" if i == 0 else "yellow",
         f"Set Grenade Explosion Power to {i}" + (" (disabled)" if i == 0 else ""))
        for i in range(6)
    ]
    ma_opts = [
        ("OG", f"/scoreboard players set #max_ammo_reload_weapons {ns}.config 0", "yellow", "Only refill magazines in inventory (OG zombies)"),
        ("Recent", f"/scoreboard players set #max_ammo_reload_weapons {ns}.config 1", "green", "Also reload current weapon (recent zombies)"),
    ]
    dd_opts = [
        ("OFF", f"/scoreboard players set #damage_debug {ns}.config 0", "red", "Disable global damage debug"),
        ("ON", f"/scoreboard players set #damage_debug {ns}.config 1", "green", "Enable global damage debug (tellraw @a every hit)"),
    ]

    # --- Player Specials (self-only scores; commands run as the clicking player) ---
    duration_opts = [("OFF", 0, "red"), ("10s", 200, "yellow"), ("30s", 600, "yellow"), ("60s", 1200, "yellow"), ("∞", 72000, "light_purple")]
    percent_opts = [("0%", 0, "red"), ("20%", 20, "yellow"), ("50%", 50, "yellow"), ("80%", 80, "green")]
    ik_opts = [(label, f"/scoreboard players set @s {ns}.special.instant_kill {v}", color,
                f"Set instant kill {'off' if v == 0 else f'for {label}'}") for label, v, color in duration_opts]
    ia_opts = [(label, f"/scoreboard players set @s {ns}.special.infinite_ammo {v}", color,
                f"Set infinite ammo {'off' if v == 0 else f'for {label}'}") for label, v, color in duration_opts]
    qr_opts = [(label, f"/scoreboard players set @s {ns}.special.quick_reload {v}", color,
                f"Set quick reload to {label}") for label, v, color in percent_opts]
    qs_opts = [(label, f"/scoreboard players set @s {ns}.special.quick_swap {v}", color,
                f"Set quick swap to {label}") for label, v, color in percent_opts]

    # Register every value sub-dialog: (sub_id, title, description, options)
    value_dialogs = [
        ("config/rpg_power", "RPG Explosion Power", "Server-wide projectile explosion power", rpg_opts),
        ("config/grenade_power", "Grenade Explosion Power", "Server-wide grenade explosion power", gren_opts),
        ("config/max_ammo", "Max Ammo Mode", "How the Max Ammo powerup refills weapons", ma_opts),
        ("config/damage_debug", "Damage Debug", "Broadcast every hit's damage to chat", dd_opts),
        ("config/instant_kill", "Instant Kill", "One-shot kills for a duration (self only)", ik_opts),
        ("config/infinite_ammo", "Infinite Ammo", "No reloads needed for a duration (self only)", ia_opts),
        ("config/quick_reload", "Quick Reload", "Reduce reload time (self only)", qr_opts),
        ("config/quick_swap", "Quick Swap", "Reduce weapon-swap time (self only)", qs_opts),
    ]
    # Each value picker's Back button returns to its parent category (global / personal).
    picker_back = {
        "config/rpg_power": "config/global", "config/grenade_power": "config/global",
        "config/max_ammo": "config/global", "config/damage_debug": "config/global",
        "config/instant_kill": "config/personal", "config/infinite_ammo": "config/personal",
        "config/quick_reload": "config/personal", "config/quick_swap": "config/personal",
    }
    for sub_id, title_text, desc, options in value_dialogs:
        register_value_picker(sub_id, title_text, desc, options, back_dialog=picker_back[sub_id])

    # --- Configuration dialog, organized into categories (by scope) ---
    # The top-level menu is a short list of categories; each opens its own sub-dialog whose Back
    # button returns to the top-level config. Leaf value pickers Back to their category (above).
    def register_category(sub_id: str, title: str, actions: list[dict[str, str]]) -> None:
        register_dialog(sub_id, {
            "type": "minecraft:multi_action",
            "title": split_emoji(title, color="gold", bold=True),
            "actions": actions,
            # Each category lists items of a single kind (settings / mode links) → one column.
            "columns": 1,
            "exit_action": dialog_back_action("config", tooltip="Return to configuration"),
        })

    register_category("config/global", "⚙ Global Settings", [
        dialog_show_btn(f"{ns}:config/rpg_power", "RPG Explosion Power", "Server-wide projectile explosion power", "red"),
        dialog_show_btn(f"{ns}:config/grenade_power", "Grenade Explosion Power", "Server-wide grenade explosion power", "gold"),
        dialog_show_btn(f"{ns}:config/max_ammo", "Max Ammo Mode", "How the Max Ammo powerup refills weapons", "aqua"),
        dialog_show_btn(f"{ns}:config/damage_debug", "Damage Debug", "Broadcast every hit's damage to chat", "yellow"),
    ])
    register_category("config/personal", "⚡ Personal Cheats", [
        dialog_show_btn(f"{ns}:config/instant_kill", "Instant Kill", "One-shot kills for a duration (self only)", "red"),
        dialog_show_btn(f"{ns}:config/infinite_ammo", "Infinite Ammo", "No reloads needed for a duration (self only)", "gold"),
        dialog_show_btn(f"{ns}:config/quick_reload", "Quick Reload", "Reduce reload time (self only)", "green"),
        dialog_show_btn(f"{ns}:config/quick_swap", "Quick Swap", "Reduce weapon-swap time (self only)", "aqua"),
    ])
    # The three game-mode setups sit directly on the first page instead of behind a "Game Modes"
    # category — opening a mode used to cost two clicks for no benefit. There is no "Players & Teams"
    # category either: team assignment only makes sense in the context of one mode, and every mode's
    # setup dialog already carries its own "Manage Players" button.
    config_actions = [
        # Row 1: the game modes, side by side (see columns=3 below)
        dialog_show_btn(f"{ns}:multiplayer/setup", "⚔ Multiplayer", "Open the multiplayer game setup menu", "red"),
        dialog_show_btn(f"{ns}:zombies/setup", "🧟 Zombies", "Open the zombies setup menu", "green"),
        dialog_show_btn(f"{ns}:missions/setup", "🎯 Missions", "Open the mission setup menu", "gold"),
        # Row 2: settings and tools
        dialog_show_btn(f"{ns}:config/global", "⚙ Global Settings", "Server-wide gameplay settings", "gold"),
        dialog_show_btn(f"{ns}:config/personal", "⚡ Personal Cheats", "Self-only powerups", "light_purple"),
        dialog_run_btn("🗺 Map Editor", f"/function {ns}:v{version}/maps/editor/menu", "Open the map editor", "yellow"),
    ]
    register_dialog("config", {
        "type": "minecraft:multi_action",
        "title": split_emoji("☣ MGS Configuration ☣", color="gold", bold=True),
        "body": [{"type": "minecraft:plain_message", "contents": {"text": "Pick a game mode, or a settings category", "color": "gray"}}],
        "actions": config_actions,
        # 3 columns lays the actions out as two rows: the game modes, then settings + tools.
        "columns": 3,
        "exit_action": {"label": {"translate": "gui.done"}},
    })

    # /function mgs:config now opens the (inline) dialog
    write_function(f"{ns}:config", f"function {dialog_function('config')}")
