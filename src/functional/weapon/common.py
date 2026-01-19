
# Imports
from typing import Any

from stewbeet import Advancement, ItemModifier, JsonDict, Mem, Predicate, set_json_encoder, write_versioned_function

from ...config.stats import COOLDOWN, REMAINING_BULLETS, json_dump


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Advancement detecting right click
    adv: JsonDict = {
        "criteria": {
            "requirement": {
                "trigger": "minecraft:tick",
                "conditions": {
                    "player": [
                        {"condition": "minecraft:entity_scores","entity": "this","scores": {f"{ns}.right_click": {"min": 1}}}
                    ]
                }
            }
        },
        "rewards": {
            "function": f"{ns}:v{version}/player/set_pending_clicks"
        }
    }
    adv_str: str = json_dump(adv)
    Mem.ctx.data[ns].advancements[f"v{version}/right_click"] = set_json_encoder(Advancement(adv), max_level=-1)
    Mem.ctx.data[ns].advancements[f"v{version}/alt_right_click"] = set_json_encoder(Advancement(adv_str.replace(".right_click", ".alt_right_click")), max_level=-1)

    # Function to set pending clicks
    write_versioned_function("player/set_pending_clicks",
f"""

# Revoke advancement and reset right click
advancement revoke @s only {ns}:v{version}/right_click
advancement revoke @s only {ns}:v{version}/alt_right_click
scoreboard players reset @s {ns}.right_click
scoreboard players reset @s {ns}.alt_right_click

# Set pending clicks
scoreboard players set @s {ns}.pending_clicks 4
""")

    # Copy gun data function
    write_versioned_function("utils/copy_gun_data",
f"""
# Copy gun data
data remove storage {ns}:gun all
data modify storage {ns}:gun SelectedItem set value {{id:""}}
data modify storage {ns}:gun SelectedItem set from entity @s SelectedItem
data modify storage {ns}:gun all set from storage {ns}:gun SelectedItem.components."minecraft:custom_data".{ns}
""")

    # Player tick function
    write_versioned_function("player/tick",
f"""
# Add temporary tag
tag @s add {ns}.ticking

# Compute acoustics (#TODO: Only if player moved enough, and every second not tick)
function {ns}:v{version}/sound/compute_acoustics

# Reload when moving weapon to offhand
execute if items entity @s weapon.offhand * run function {ns}:v{version}/player/reload_check

# Copy gun data
function {ns}:v{version}/utils/copy_gun_data

# Check if we need to zoom weapon or stop
function {ns}:v{version}/zoom/main

# Check if switching weapon
function {ns}:v{version}/switch/main

# Decrease cooldown by 1
execute if score @s {ns}.cooldown matches 1.. run scoreboard players remove @s {ns}.cooldown 1

# Check mid cooldown sound
execute if score @s {ns}.cooldown matches 1.. if entity @s[tag={ns}.pump_sound] if data storage {ns}:gun all.sounds.pump run function {ns}:v{version}/sound/check/pump
execute if score @s {ns}.cooldown matches 0 if entity @s[tag={ns}.pump_sound] run tag @s remove {ns}.pump_sound

# Check mid reload sound
execute if score @s {ns}.cooldown matches 1.. if entity @s[tag={ns}.reload_mid_sound] if data storage {ns}:gun all.sounds.playermid run function {ns}:v{version}/sound/check/reload_mid
execute if score @s {ns}.cooldown matches 0 if entity @s[tag={ns}.reload_mid_sound] run tag @s remove {ns}.reload_mid_sound

# Check if we need to play reload end sound
execute if score @s {ns}.cooldown matches 1.. if data storage {ns}:gun all.sounds.playerend run function {ns}:v{version}/sound/check/reload_end
execute if score @s {ns}.cooldown matches 0 if entity @s[tag={ns}.reloading] run function {ns}:v{version}/ammo/end_reload

# If pending clicks, run right click function
execute if score @s {ns}.pending_clicks matches -100.. run function {ns}:v{version}/player/right_click

# Show ammo action bar
execute if data storage {ns}:gun all.gun run function {ns}:v{version}/ammo/show_action_bar

# Remove temporary tag
tag @s remove {ns}.ticking

# Set previous selected weapon (length of string)
execute store result score @s {ns}.previous_selected run data get storage {ns}:gun SelectedItem.id
""")

    # Handle pending clicks
    write_versioned_function("player/right_click",
f"""
# Decrease pending clicks by 1
scoreboard players remove @s {ns}.pending_clicks 1

# If player stopped right clicking for 3 second, we update the item lore
execute if score @s {ns}.pending_clicks matches -60 if data storage {ns}:gun all.gun run function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}

# Stop here is weapon cooldown OR pending clicks if negative
execute if score @s {ns}.cooldown matches 1.. run return fail
execute if score @s {ns}.pending_clicks matches ..-1 run return fail

# Stop if SelectedItem is not a gun or if not enough ammo
execute unless data storage {ns}:gun all.gun run return fail
execute if score @s {ns}.{REMAINING_BULLETS} matches ..0 run return run function {ns}:v{version}/ammo/reload

# Set cooldown
execute store result score @s {ns}.cooldown run data get storage {ns}:gun all.stats.{COOLDOWN}
""")

    # Prepare predicates for movement checks
    # (Can't use flag 'is_on_ground' because /tp @s ~ ~ ~ makes it false for two ticks)
    def json_enc(x: Any) -> Any: return set_json_encoder(x, max_level=-1)
    Mem.ctx.data[ns].predicates[f"v{version}/is_on_ground"] = json_enc(Predicate({"condition":"minecraft:entity_properties","entity":"this","predicate":{"movement":{"vertical_speed":{"max":0.1}}}}))
    Mem.ctx.data[ns].predicates[f"v{version}/is_sprinting"] = json_enc(Predicate({"condition":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_sprinting":True}}}))
    Mem.ctx.data[ns].predicates[f"v{version}/is_sneaking"] = json_enc(Predicate({"condition":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_sneaking":True}}}))
    Mem.ctx.data[ns].predicates[f"v{version}/is_moving"] = json_enc(Predicate({"condition":"minecraft:entity_properties","entity":"this","predicate":{"movement":{"horizontal_speed":{"min":0.1}}}}))

    # Update weapon stats item modifier
    modifier: dict[str, Any] = {"function":"minecraft:copy_custom_data","source":{"type":"minecraft:storage","source":f"{ns}:gun"},"ops":[{"source":"all.stats","target":f"{ns}.stats","op":"replace"}]}
    Mem.ctx.data[ns].item_modifiers[f"v{version}/update_stats"] = json_enc(ItemModifier(modifier))

    # Update weapon model item modifier
    write_versioned_function("utils/update_model", """
$item modify entity @s weapon.mainhand {"function": "minecraft:set_components","components": {"minecraft:item_model": "$(item_model)"}}
""")

    # Reload check when item is moved to offhand
    write_versioned_function("player/reload_check",
f"""
# If mainhand is empty and offhand has a weapon, move it to mainhand and reload
execute unless items entity @s weapon.mainhand * if items entity @s weapon.offhand *[custom_data~{{{ns}:{{gun:true}}}}] run function {ns}:v{version}/player/swap_and_reload
""")

    # Swap offhand to mainhand and reload
    write_versioned_function("player/swap_and_reload",
f"""
# Move offhand item to mainhand
item replace entity @s weapon.mainhand from entity @s weapon.offhand
item replace entity @s weapon.offhand with air

# Copy gun data
function {ns}:v{version}/utils/copy_gun_data

# Reload the weapon
function {ns}:v{version}/ammo/reload
""")

