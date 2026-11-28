""" Built-in zombies maps and their per-map scripts (Kino der Toten). """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from .common import ZombiesCommon
from .enemies.escort.shared import PAP_ROOM_TAG


# Functions
def generate_zombies_maps() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	# Run as the interaction entity; `on target` reaches the player.
	deny_recharging: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"The teleporter is recharging...","color":"yellow"}')

	# Kino der Toten (base_coordinates and spawn arrays are placeholders).
	kino_der_toten_map: str = r"""{base_coordinates: [208, 115, 194], shared: {barricade: {block_enabled: {id: "minecraft:oak_fence_gate", properties: {open: "false"}}, block_disabled: {id: "minecraft:oak_fence_gate", properties: {open: "true"}}}}, wallbuys: [{refill_price_pap: 250, pos: [-21, 7, 3], price: 250, refill_price: 250, magazine_id: "", name: "Grenades", yaw: 180, weapon_id: "frag_grenade"}, {pos: [-41, -1, -47], magazine_id: "sten_mag", weapon_id: "sten"}, {pos: [-23, 8, -21], magazine_id: "vz61_mag", yaw: 270, weapon_id: "vz61"}, {pos: [-60, -1, 13], price: 1200, refill_price: 600, magazine_id: "m16a4_mag", yaw: 90, weapon_id: "m16a4"}, {pos: [-68, -1, -24], price: 1200, refill_price: 600, magazine_id: "mp5_mag", yaw: 270, weapon_id: "mp5"}, {pos: [-40, -1, 26], price: 1200, refill_price: 600, magazine_id: "ak47_mag", weapon_id: "ak47"}, {pos: [-23, 1, 20], magazine_id: "mac10_mag", yaw: 270, weapon_id: "mac10"}, {refill_price_pap: 3000, pos: [-23, -2, 4], price: 3000, refill_price: 3000, magazine_id: "", name: "Bowie Knife", weapon_id: "bowie_knife"}, {pos: [-33, 4, -17], price: 1200, refill_price: 600, magazine_id: "spas12_shell", yaw: 180, weapon_id: "spas12"}, {pos: [-19, 6, -9], price: 500, refill_price: 250, magazine_id: "mosin_bullet", yaw: 270, weapon_id: "mosin"}], spawning_points: {special: [{group_id: 6, pos: [-45, -2, 38], yaw: 135}, {group_id: 6, pos: [-37, -2, 32], yaw: 180}, {group_id: 6, pos: [-41, -2, 28]}, {group_id: 6, pos: [-27, -2, 29], yaw: 90}, {group_id: 6, pos: [-31, -2, 29], yaw: 90}, {group_id: 6, pos: [-21, -2, 38], yaw: 90}, {group_id: 6, pos: [-26, -2, 37], yaw: 180}, {group_id: 7, pos: [-7, 0, 22], yaw: 90}, {group_id: 7, pos: [-21, 0, 22]}, {pos: [-3, 0, -8], yaw: 315}, {group_id: 7, pos: [-10, 0, 17]}, {pos: [-3, 0, 8], yaw: 225}, {pos: [-13, 0, 0], yaw: 270}, {group_id: 1, pos: [-12, 7, -19], yaw: 45}, {group_id: 1, pos: [-20, 7, -18], yaw: 315}, {group_id: 2, pos: [-39, -2, -40], yaw: 135}, {group_id: 2, pos: [-33, 3, -33], yaw: 270}, {group_id: 2, pos: [-46, -2, -32], yaw: 270}, {group_id: 2, pos: [-38, -2, -33], yaw: 180}, {group_id: 3, pos: [-55, -2, -35], yaw: 270}, {group_id: 2, pos: [-37, 3, -19], yaw: 180}, {group_id: 3, pos: [-60, -2, -29], yaw: 270}, {group_id: 3, pos: [-55, -2, -27], yaw: 225}, {group_id: 4, pos: [-68, -2, -16], yaw: 180}, {group_id: 3, pos: [-66, -2, -27], yaw: 180}, {group_id: 4, pos: [-72, -2, 0], yaw: 180}, {group_id: 4, pos: [-70, -2, -8], yaw: 180}, {group_id: 4, pos: [-60, -2, 3], yaw: 90}, {group_id: 4, pos: [-69, -2, 6], yaw: 135}, {group_id: 4, pos: [-59, -2, -10], yaw: 45}, {group_id: 4, pos: [-60, -2, -4], yaw: 45}, {group_id: 4, pos: [-49, -4, -5], yaw: 180}, {group_id: 4, pos: [-49, -4, -15], yaw: 45}, {group_id: 4, pos: [-48, -4, 8], yaw: 180}, {group_id: 4, pos: [-48, -4, 1], yaw: 180}, {group_id: 4, pos: [-42, -4, 0], yaw: 90}, {group_id: 4, pos: [-49, -4, 15], yaw: 180}, {group_id: 5, pos: [-59, 4, 34], yaw: 135}, {group_id: 4, pos: [-29, -3, 0], yaw: 90}, {group_id: 5, pos: [-66, 4, 30]}, {group_id: 5, pos: [-66, 4, 38], yaw: 225}, {group_id: 5, pos: [-53, -2, 35], yaw: 315}, {group_id: 5, pos: [-53, -2, 39], yaw: 45}, {group_id: 6, pos: [-47, -2, 34], yaw: 315}], players: [{pos: [2, 0, 2], yaw: 208}, {pos: [-2, 0, -2], yaw: 244}, {pos: [2, 0, -2], yaw: 339}, {pos: [-2, 0, 2], yaw: 288}], zombies: [{group_id: 4, pos: [-84, -2, -14]}, {group_id: 4, pos: [-42, -4, -22], activation_box: [-34, 0, 1, 51, 14, 39]}, {group_id: 4, pos: [-34, -2, -11], yaw: 90}, {group_id: 4, pos: [-76, -2, 10]}, {group_id: 4, pos: [-43, -4, 22], activation_box: [-33, 0, -43, 51, 14, 39], yaw: 90}, {group_id: 5, pos: [-53, 4, 24], activation_box: [-16, -8, -5, 27, 16, 29], yaw: 90}, {group_id: 4, pos: [-36, -2, 13], yaw: 90}, {group_id: 5, pos: [-63, -2, 28]}, {group_id: 5, pos: [-47, 4, 43], yaw: 90}, {group_id: 6, pos: [-16, -2, 33], yaw: 270}, {group_id: 6, pos: [-48, -2, 43], yaw: 270}, {group_id: 7, pos: [-30, 0, 21]}, {group_id: 7, pos: [-3, 0, 16]}, {pos: [-2, 0, 14], yaw: 270}, {pos: [13, 0, 4], yaw: 90, walk_to: [-8, 1, -11]}, {pos: [-18, 0, -15], yaw: 270}, {pos: [-13, 7, 16], yaw: 90}, {group_id: 1, pos: [-28, 7, -23]}, {group_id: 1, pos: [-2, 7, -19]}, {group_id: 1, pos: [-17, 12, -25], yaw: 180}, {group_id: 1, pos: [-8, 4, -47], yaw: 90}, {group_id: 2, pos: [-28, -2, -36]}, {group_id: 2, pos: [-48, 2, -21], activation_box: [0, -4, -26, 17, 12, 31], yaw: 270}, {group_id: 3, pos: [-65, -2, -43], yaw: 270}, {group_id: 2, pos: [-39, -2, -55], yaw: 90}, {group_id: 3, pos: [-60, 5, -29], yaw: 90}, {group_id: 3, pos: [-45, -2, -25]}]}, out_of_bounds: [], description: "from: Black Ops I", wunderfizz: [], start_commands: [], barricades: [{pos: [-69, -1, 14], yaw: 270}, {pos: [-8, 2, 16], yaw: 90}, {pos: [-17, 9, 14], yaw: 180}, {pos: [-24, 1, 22], yaw: 270}, {pos: [-26, 9, -18], yaw: 270}, {pos: [-16, 8, -40]}, {pos: [-4, 9, -16], yaw: 90}, {pos: [-41, 4, -18], yaw: 270}, {pos: [-76, 0, -15], yaw: 270}, {pos: [-45, -1, -48]}, {pos: [-17, 0, 37], yaw: 90}, {pos: [4, 1, -7], yaw: 90}, {pos: [1, 2, 11], yaw: 180}, {pos: [-60, 0, -38]}, {pos: [-57, 5, 26]}, {pos: [-35, -1, -33], yaw: 90}, {pos: [-69, 0, 14], yaw: 270}, {pos: [-41, 4, -19], yaw: 270}, {pos: [-15, 2, -6]}, {pos: [-45, 0, 41], yaw: 180}, {pos: [-44, -1, 41], yaw: 180}, {pos: [-8, 1, 17], yaw: 90}, {pos: [-44, -1, -48]}, {pos: [-15, 1, -6]}, {pos: [-53, 5, 41], yaw: 180}, {pos: [1, 1, 11], yaw: 180}, {pos: [-49, -2, -19]}, {pos: [-17, 9, -40]}, {pos: [-52, 0, -24], yaw: 90}, {pos: [-49, -3, 19], yaw: 180}, {pos: [-50, -3, -19]}, {pos: [-35, 0, -33], yaw: 90}, {pos: [-60, -1, -38]}, {pos: [-49, -2, 19], yaw: 180}, {pos: [-57, 6, 26]}, {pos: [-24, 2, 21], yaw: 270}, {pos: [2, 2, 11], yaw: 180}, {pos: [-14, 2, -6]}, {pos: [-16, 9, -40]}, {pos: [4, 2, -7], yaw: 90}, {pos: [-56, 6, 26]}, {pos: [-26, 8, -19], yaw: 270}, {pos: [-76, -1, -15], yaw: 270}, {pos: [-41, 5, -18], yaw: 270}, {pos: [-69, -1, 15], yaw: 270}, {pos: [-52, -1, -24], yaw: 90}, {pos: [-56, 5, 26]}, {pos: [-24, 1, 21], yaw: 270}, {pos: [-17, 0, 38], yaw: 90}, {pos: [-50, -2, -19]}, {pos: [-52, 0, -25], yaw: 90}, {pos: [-8, 2, 17], yaw: 90}, {pos: [2, 1, 11], yaw: 180}, {pos: [-49, -3, -19]}, {pos: [-45, 0, -48]}, {pos: [-53, 6, 41], yaw: 180}, {pos: [-4, 8, -17], yaw: 90}, {pos: [-17, -1, 37], yaw: 90}, {pos: [-76, 0, -14], yaw: 270}, {pos: [-50, -3, 19], yaw: 180}, {pos: [-52, 6, 41], yaw: 180}, {pos: [-45, -1, 41], yaw: 180}, {pos: [-26, 8, -18], yaw: 270}, {pos: [-35, -1, -34], yaw: 90}, {pos: [-4, 8, -16], yaw: 90}, {pos: [-52, 5, 41], yaw: 180}, {pos: [-44, 0, 41], yaw: 180}, {pos: [-76, -1, -14], yaw: 270}, {pos: [-52, -1, -25], yaw: 90}, {pos: [-17, -1, 38], yaw: 90}, {pos: [-69, 0, 15], yaw: 270}, {pos: [-17, 8, -40]}, {pos: [-50, -2, 19], yaw: 180}, {pos: [4, 1, -8], yaw: 90}, {pos: [-16, 8, 14], yaw: 180}, {pos: [-24, 2, 22], yaw: 270}, {pos: [4, 2, -8], yaw: 90}, {pos: [-8, 1, 16], yaw: 90}, {pos: [-17, 8, 14], yaw: 180}, {pos: [-35, 0, -34], yaw: 90}, {pos: [-44, 0, -48]}, {pos: [-59, -1, -38]}, {pos: [-4, 9, -17], yaw: 90}, {pos: [-59, 0, -38]}, {pos: [-41, 5, -19], yaw: 270}, {pos: [-14, 1, -6]}, {pos: [-16, 9, 14], yaw: 180}, {pos: [-26, 9, -19], yaw: 270}], doors: [{back_name: "Lower Hall", price: 750, blocks: [{pos: [-16, 0, 14]}, {pos: [-17, 0, 14]}, {pos: [-15, 0, 14]}, {pos: [-16, 2, 14]}, {pos: [-17, 2, 14]}, {pos: [-17, 1, 14]}, {pos: [-15, 2, 14]}, {pos: [-15, 1, 14]}, {pos: [-16, 1, 14]}], name: "Lobby", block: "minecraft:spruce_planks", back_group_id: 7, link_id: 8}, {back_name: "Lobby", price: 750, blocks: [{pos: [-17, 9, -14]}, {pos: [-17, 8, -14]}, {pos: [-16, 9, -14]}, {pos: [-17, 7, -14]}, {pos: [-16, 8, -14]}, {pos: [-16, 7, -14]}], name: "Upper Hall", block: "minecraft:spruce_planks", link_id: 1}, {back_name: "Upper Hall", blocks: [{pos: [-24, 9, -32]}, {pos: [-24, 9, -34]}, {pos: [-24, 9, -33]}, {pos: [-24, 8, -33]}, {pos: [-24, 8, -32]}, {pos: [-24, 7, -32]}, {pos: [-24, 8, -34]}, {pos: [-24, 7, -34]}, {pos: [-24, 7, -33]}], name: "Foyer", block: "minecraft:spruce_planks", back_group_id: 1, link_id: 2, yaw: 270}, {back_name: "Foyer", price: 1250, blocks: [{pos: [-52, -1, -35]}, {pos: [-52, 0, -35]}, {pos: [-52, 0, -34], block: "minecraft:oak_stairs[facing=south]"}, {pos: [-52, -2, -35]}, {pos: [-52, -2, -34], block: "minecraft:oak_stairs[facing=south]"}, {pos: [-52, -1, -34], block: "minecraft:oak_stairs[facing=south]"}, {pos: [-52, -1, -36], block: "minecraft:oak_stairs[facing=north]"}, {pos: [-52, 0, -36], block: "minecraft:oak_stairs[facing=north]"}, {pos: [-52, -2, -36], block: "minecraft:oak_stairs[facing=north]"}], name: "Dressing Room", block: "minecraft:oak_slab[type=top]", back_group_id: 2, link_id: 3, yaw: 270}, {back_name: "Dressing Room", price: 1250, blocks: [{pos: [-65, 0, -21]}, {pos: [-67, 0, -21]}, {pos: [-66, 0, -21]}, {pos: [-66, -1, -21]}, {pos: [-67, -1, -21]}, {pos: [-67, -2, -21]}, {pos: [-65, -1, -21]}, {pos: [-65, -2, -21]}, {pos: [-66, -2, -21]}], name: "Theater", block: "minecraft:oak_slab[type=top]", back_group_id: 3, link_id: 4, yaw: 180}, {back_name: "Theater", price: 1250, blocks: [{pos: [-61, -1, 17]}, {pos: [-62, -1, 17]}, {pos: [-61, -2, 17]}, {pos: [-62, -2, 17]}, {pos: [-63, 5, 25]}, {pos: [-64, 5, 25]}, {pos: [-63, 4, 25]}, {pos: [-64, 4, 25]}], name: "Storage Room", block: "minecraft:cyan_terracotta", back_group_id: 4, link_id: 5, yaw: 180}, {back_name: "Storage Room", price: 1250, blocks: [{pos: [-50, -2, 35]}, {pos: [-50, -1, 34]}, {pos: [-50, -1, 35]}, {pos: [-50, -2, 34]}], name: "Alley", block: "minecraft:cobblestone_wall", back_group_id: 5, link_id: 6, yaw: 90}, {back_name: "Alley", blocks: [{pos: [-23, 1, 31]}, {pos: [-22, 1, 31]}, {pos: [-23, 0, 31]}, {pos: [-22, 0, 31]}], name: "Lower Hall", block: "minecraft:spruce_planks", back_group_id: 6, link_id: 7}], traps: [{duration: 1800, pos: [-52, 1, 0], price: 1500, cooldown: 2400, type: 2, yaw: 90, effect_radius: [15.0f, 15.0f, 15.0f]}, {duration: 1800, pos: [-43, 0, -37], price: 1500, cooldown: 2400, type: 2, yaw: 90, effect_radius: [8.0f, 8.0f, 8.0f]}, {duration: 600, offset_pos: [1, -1, -4], pos: [-63, 5, 38], cooldown: 1800, type: 1, yaw: 90, effect_radius: [0.5f, 2.0f, 3.0f]}, {duration: 600, offset_pos: [1, 0, -2], pos: [-26, -3, 2], cooldown: 1800, type: 1, yaw: 90, effect_radius: [1.0f, 2.0f, 2.0f]}, {duration: 600, offset_pos: [0, 0, -2], pos: [-16, 0, 24], cooldown: 1800, yaw: 180, effect_radius: [1.5f, 2.0f, 1.5f]}, {duration: 600, offset_pos: [1, -1, 1], pos: [-14, 8, -25], cooldown: 1800, type: 1, yaw: 270, effect_radius: [1.0f, 2.0f, 1.0f]}], pap_machines: [{pos: [-19, 6, 0], yaw: 90}], name: "Kino der Toten", power_switch: [{pos: [-60, -1, 9], yaw: 90}], boundaries: [[-106, -14, -92], [103, 52, 87]], id: "kino_der_toten", mystery_box: {positions: [{location_name: "Theater Auditorium", pos: [-36, -3, -2]}, {location_name: "Lower Hall", pos: [-16, 0, 30], yaw: 180}, {location_name: "Alley", pos: [-36, -2, 35], yaw: 180}, {location_name: "Upper Hall", pos: [-17, 7, -22]}, {can_start_on: 0b, location_name: "Lobby", pos: [-13, 5, 0], yaw: 90}, {location_name: "Dressing Room", pos: [-61, -2, -33], yaw: 180}, {location_name: "Foyer", pos: [-48, -2, -41], yaw: 270}, {location_name: "Theater Stage", pos: [-75, -2, -5], yaw: 270}, {location_name: "Storage Room", pos: [-54, 4, 32]}]}, perks: [{pos: [-36, -2, -30], price: 3000, perk_id: "speed_cola", name: "Speed Cola", yaw: 90}, {pos: [-22, -2, 40], price: 2000, perk_id: "double_tap", name: "Double Tap", yaw: 180}, {pos: [-23, 7, -27], price: 4000, perk_id: "mule_kick", name: "Mule Kick", yaw: 180}, {pos: [-1, 0, -14], price: 1500, perk_id: "quick_revive", name: "Quick Revive"}, {pos: [-20, -3, 5], price: 2500, name: "Juggernog", yaw: 90}], respawn_commands: [], dimension: "mgs:zombies"}"""
	beyounds_map: str = r"""{base_coordinates: [191, 130, 1058], shared: {barricade: {block_enabled: {id: "minecraft:spruce_slab", properties: {type: "top"}}, block_disabled: {id: "minecraft:air", properties: {}}}}, wallbuys: [{pos: [9, -8, 35], magazine_id: "ak47_mag", yaw: 270, weapon_id: "ak47"}, {pos: [3, -20, 61], price: 1250, refill_price: 625, magazine_id: "famas_mag", yaw: 180, weapon_id: "famas"}, {pos: [-10, -10, -13], price: 500, refill_price: 250, magazine_id: "mosin_bullet", yaw: 270, weapon_id: "mosin"}, {pos: [-23, -20, 1], magazine_id: "m16a4_mag", weapon_id: "m16a4"}, {pos: [-41, -20, -9], magazine_id: "", weapon_id: "semtex"}, {pos: [-55, -8, 20], price: 750, refill_price: 375, magazine_id: "m500_shell", yaw: 270, weapon_id: "m500"}, {pos: [-11, -8, 18], magazine_id: "vz61_mag", yaw: 270, weapon_id: "vz61"}, {pos: [39, -20, 38], magazine_id: "ppsh_mag", yaw: 90, weapon_id: "ppsh41"}, {pos: [8, -8, 9], price: 750, refill_price: 375, magazine_id: "spas12_shell", weapon_id: "spas12"}, {pos: [-31, -17, -29], price: 750, refill_price: 375, magazine_id: "makarov_mag", yaw: 270, weapon_id: "makarov"}], out_of_bounds: [], spawning_points: {special: [{group_id: 8, pos: [28, -16, 50], yaw: 45}, {group_id: 7, pos: [-4, -21, 29], yaw: 135}, {group_id: 2, pos: [-27, -9, -4], yaw: 270}, {group_id: 5, pos: [-24, -21, 23], yaw: 180}, {group_id: 3, pos: [-51, -9, -3], yaw: 45}, {group_id: 5, pos: [-24, -21, 5], yaw: 45}, {group_id: 7, pos: [-8, -21, 42], yaw: 225}, {group_id: 6, pos: [-40, -21, -5], yaw: 90}, {group_id: 3, pos: [-51, -9, 17], yaw: 180}, {pos: [-24, -19, -20], yaw: 180}, {group_id: 4, pos: [-41, -15, 37], yaw: 90}, {group_id: 3, pos: [-42, -9, 5], yaw: 180}, {group_id: 1, pos: [-7, -12, -10], yaw: 180}, {pos: [-29, -18, -32]}, {group_id: 7, pos: [-3, -21, 18], yaw: 135}, {group_id: 8, pos: [34, -16, 64], yaw: 135}, {group_id: 10, pos: [24, -9, 20], yaw: 270}, {group_id: 9, pos: [16, -9, 26]}, {group_id: 10, pos: [5, -9, 19], yaw: 225}, {group_id: 6, pos: [-56, -21, -12], yaw: 270}, {group_id: 8, pos: [35, -21, 26]}, {group_id: 10, pos: [12, -9, 12], yaw: 270}, {group_id: 7, pos: [-2, -21, 56], yaw: 135}, {group_id: 4, pos: [-51, -9, 28]}, {group_id: 2, pos: [-33, -9, 18], yaw: 180}, {group_id: 9, pos: [11, -9, 35], yaw: 270}, {group_id: 1, pos: [-7, -15, -25], yaw: 180}, {group_id: 8, pos: [20, -16, 64], yaw: 225}, {group_id: 2, pos: [-1, -9, 6], yaw: 315}, {group_id: 2, pos: [-2, -9, 19], yaw: 225}, {group_id: 9, pos: [23, -16, 35], yaw: 225}, {group_id: 8, pos: [14, -16, 51]}, {group_id: 5, pos: [-50, -21, 19], yaw: 270}, {group_id: 4, pos: [-45, -9, 37], yaw: 90}, {pos: [-19, -18, -25], yaw: 90}], players: [{group_id: 5, pos: [-41, -21, 18]}, {pos: [-29, -18, -36], yaw: 315}, {group_id: 8, pos: [29, -21, 68], yaw: 90}, {group_id: 5, pos: [-23, -21, 9], yaw: 180}, {group_id: 10, pos: [15, -9, 18], yaw: 90}, {group_id: 2, pos: [-14, -10, 16]}, {group_id: 3, pos: [-46, -9, -3], yaw: 90}, {pos: [-19, -18, -22], yaw: 135}, {pos: [-29, -18, -22], yaw: 270}, {pos: [-19, -18, -36], yaw: 90}, {pos: [-24, -19, -16], yaw: 180}, {group_id: 2, pos: [-22, -10, 3], yaw: 90}, {group_id: 8, pos: [31, -21, 45]}], zombies: [{group_id: 1, pos: [0, -12, -13], yaw: 90}, {group_id: 5, pos: [-15, -21, 2]}, {group_id: 10, pos: [14, -9, 5], yaw: 270}, {group_id: 6, pos: [-66, -21, -17]}, {group_id: 6, pos: [-66, -21, -11], yaw: 180}, {group_id: 9, pos: [14, -9, 43], yaw: 270}, {group_id: 7, pos: [-3, -21, 64], yaw: 90}, {group_id: 5, pos: [-32, -21, -5]}, {group_id: 4, pos: [-40, -9, 37], yaw: 270}, {group_id: 2, pos: [-32, -9, 26], yaw: 180}, {group_id: 8, pos: [43, -21, 18]}, {group_id: 8, pos: [43, -21, 66], yaw: 90}, {group_id: 5, pos: [-38, -21, 7], yaw: 90}, {group_id: 3, pos: [-54, -9, -10], yaw: 270}, {group_id: 7, pos: [-23, -21, 39], yaw: 270}, {pos: [-34, -18, -42], yaw: 270}, {group_id: 2, pos: [-31, -9, -10], yaw: 90}, {group_id: 8, pos: [43, -21, 39], yaw: 180}, {group_id: 1, pos: [0, -15, -29], yaw: 90}, {pos: [-34, -18, -18]}, {group_id: 9, pos: [5, -9, 23]}, {group_id: 7, pos: [12, -21, 23], yaw: 90}, {group_id: 3, pos: [-43, -9, 20], yaw: 270}, {group_id: 10, pos: [33, -9, 26], yaw: 90}, {group_id: 2, pos: [-5, -9, 26], yaw: 180}, {group_id: 10, pos: [33, -9, 12], yaw: 90}, {group_id: 8, pos: [27, -21, 74], yaw: 90}, {group_id: 5, pos: [-57, -21, 8], yaw: 180}, {group_id: 9, pos: [24, -9, 44], yaw: 180}, {pos: [-14, -18, -41], yaw: 90}, {group_id: 9, pos: [6, -9, 29], yaw: 180}, {group_id: 2, pos: [-19, -9, -10], yaw: 270}, {group_id: 5, pos: [-44, -21, 7], yaw: 270}, {group_id: 5, pos: [-26, -21, 31], yaw: 270}, {group_id: 8, pos: [24, -21, 25], yaw: 270}, {group_id: 7, pos: [-14, -21, 23], yaw: 270}, {group_id: 3, pos: [-58, -9, 15], yaw: 180}, {group_id: 3, pos: [-58, -9, 7], yaw: 180}, {group_id: 7, pos: [3, -21, 6]}, {group_id: 4, pos: [-40, -9, 28], yaw: 90}, {group_id: 8, pos: [43, -21, 48], yaw: 90}, {pos: [-14, -18, -18]}]}, description: "Le grand maitre canard suprême", wunderfizz: [{pos: [-41, -21, -1], yaw: 180}], barricades: [{pos: [-6, -19, 62], yaw: 180}, {pos: [-31, -19, 0]}, {pos: [-18, -20, 38], yaw: 270}, {pos: [28, -19, 25], yaw: 270}, {pos: [8, -7, 26], yaw: 270}, {pos: [40, -20, 67], yaw: 90}, {pos: [-20, -16, -18], yaw: 180}, {pos: [-43, -8, 29], yaw: 90}, {pos: [17, -7, 40], yaw: 180}, {pos: [-40, -19, 9]}, {pos: [-28, -16, -40]}, {pos: [-19, -17, -18], yaw: 180}, {pos: [40, -20, 49], yaw: 90}, {pos: [-56, -7, 11], yaw: 270}, {pos: [-40, -20, 9]}, {pos: [-18, -17, -40]}, {pos: [28, -19, 24], yaw: 270}, {pos: [28, -7, 12], yaw: 90}, {pos: [-50, -8, -7]}, {pos: [25, -19, 71], yaw: 180}, {pos: [-3, -10, -12], yaw: 90}, {pos: [-18, -19, 6], yaw: 90}, {pos: [-18, -8, -7]}, {pos: [-34, -7, -7]}, {pos: [-29, -17, -40]}, {pos: [-43, -7, 28], yaw: 90}, {pos: [18, -7, 7]}, {pos: [-6, -7, 23], yaw: 180}, {pos: [-28, -17, -18], yaw: 180}, {pos: [-19, -17, -40]}, {pos: [-18, -19, 5], yaw: 90}, {pos: [28, -8, 25], yaw: 90}, {pos: [40, -20, 47], yaw: 90}, {pos: [-30, -17, -40]}, {pos: [44, -19, 21]}, {pos: [2, -20, 9]}, {pos: [-29, -17, -18], yaw: 180}, {pos: [-18, -16, -18], yaw: 180}, {pos: [-31, -20, 0]}, {pos: [16, -7, 7]}, {pos: [-33, -20, 0]}, {pos: [-36, -19, -5], yaw: 90}, {pos: [8, -19, 22], yaw: 90}, {pos: [-20, -17, -40]}, {pos: [-11, -20, 23], yaw: 270}, {pos: [-33, -7, 23], yaw: 180}, {pos: [-24, -19, 28], yaw: 180}, {pos: [16, -8, 40], yaw: 180}, {pos: [43, -20, 21]}, {pos: [28, -8, 26], yaw: 90}, {pos: [28, -20, 26], yaw: 270}, {pos: [-5, -7, 23], yaw: 180}, {pos: [-46, -8, 19], yaw: 90}, {pos: [-64, -20, -13], yaw: 270}, {pos: [8, -19, 24], yaw: 90}, {pos: [-29, -16, -18], yaw: 180}, {pos: [-31, -8, 23], yaw: 180}, {pos: [18, -7, 40], yaw: 180}, {pos: [-11, -19, 22], yaw: 270}, {pos: [28, -8, 11], yaw: 90}, {pos: [42, -19, 21]}, {pos: [18, -8, 40], yaw: 180}, {pos: [-56, -7, 4], yaw: 270}, {pos: [-32, -19, 0]}, {pos: [17, -7, 7]}, {pos: [-55, -20, 4], yaw: 270}, {pos: [-28, -16, -18], yaw: 180}, {pos: [-64, -19, -13], yaw: 270}, {pos: [-6, -20, 62], yaw: 180}, {pos: [-5, -8, 23], yaw: 180}, {pos: [-51, -7, -7]}, {pos: [28, -8, 27], yaw: 90}, {pos: [-23, -20, 28], yaw: 180}, {pos: [-3, -11, -14], yaw: 90}, {pos: [-50, -7, -7]}, {pos: [-18, -20, 39], yaw: 270}, {pos: [28, -7, 11], yaw: 90}, {pos: [40, -20, 65], yaw: 90}, {pos: [8, -8, 25], yaw: 270}, {pos: [-28, -17, -40]}, {pos: [2, -19, 9]}, {pos: [8, -8, 27], yaw: 270}, {pos: [-19, -16, -18], yaw: 180}, {pos: [-64, -19, -14], yaw: 270}, {pos: [-30, -17, -18], yaw: 180}, {pos: [-56, -8, 3], yaw: 270}, {pos: [-56, -7, 3], yaw: 270}, {pos: [8, -7, 25], yaw: 270}, {pos: [28, -20, 25], yaw: 270}, {pos: [-43, -8, 27], yaw: 90}, {pos: [-23, -19, 28], yaw: 180}, {pos: [-18, -17, -18], yaw: 180}, {pos: [28, -7, 13], yaw: 90}, {pos: [-3, -14, -29], yaw: 90}, {pos: [-18, -20, 6], yaw: 90}, {pos: [8, -20, 23], yaw: 90}, {pos: [44, -19, 36], yaw: 180}, {pos: [-32, -20, 0]}, {pos: [16, -8, 7]}, {pos: [-11, -19, 23], yaw: 270}, {pos: [-20, -17, -18], yaw: 180}, {pos: [-55, -20, 5], yaw: 270}, {pos: [-18, -19, 40], yaw: 270}, {pos: [-43, -7, 17], yaw: 180}, {pos: [-43, -8, 17], yaw: 180}, {pos: [25, -20, 71], yaw: 180}, {pos: [-11, -20, 22], yaw: 270}, {pos: [28, -8, 13], yaw: 90}, {pos: [-56, -8, 5], yaw: 270}, {pos: [-36, -20, -6], yaw: 90}, {pos: [42, -20, 21]}, {pos: [28, -8, 12], yaw: 90}, {pos: [-3, -10, -13], yaw: 90}, {pos: [-30, -16, -40]}, {pos: [-5, -20, 62], yaw: 180}, {pos: [44, -20, 36], yaw: 180}, {pos: [18, -8, 7]}, {pos: [8, -7, 27], yaw: 270}, {pos: [-32, -8, 23], yaw: 180}, {pos: [-18, -7, -7]}, {pos: [40, -20, 66], yaw: 90}, {pos: [-6, -8, 23], yaw: 180}, {pos: [17, -8, 40], yaw: 180}, {pos: [-56, -8, 13], yaw: 270}, {pos: [4, -20, 9]}, {pos: [-42, -7, 17], yaw: 180}, {pos: [4, -19, 9]}, {pos: [28, -7, 27], yaw: 90}, {pos: [-43, -8, 28], yaw: 90}, {pos: [-22, -19, 28], yaw: 180}, {pos: [-17, -8, -7]}, {pos: [-64, -20, -14], yaw: 270}, {pos: [-31, -7, 23], yaw: 180}, {pos: [-55, -20, 6], yaw: 270}, {pos: [3, -19, 9]}, {pos: [-18, -19, 39], yaw: 270}, {pos: [-36, -19, -4], yaw: 90}, {pos: [-3, -14, -28], yaw: 90}, {pos: [8, -19, 23], yaw: 90}, {pos: [-33, -8, 23], yaw: 180}, {pos: [24, -19, 71], yaw: 180}, {pos: [3, -20, 9]}, {pos: [-3, -13, -30], yaw: 90}, {pos: [43, -20, 36], yaw: 180}, {pos: [-22, -20, 28], yaw: 180}, {pos: [43, -19, 21]}, {pos: [-16, -7, -7]}, {pos: [-46, -8, 20], yaw: 90}, {pos: [-51, -8, -7]}, {pos: [40, -19, 47], yaw: 90}, {pos: [-30, -16, -18], yaw: 180}, {pos: [-56, -7, 5], yaw: 270}, {pos: [-18, -20, 4], yaw: 90}, {pos: [-18, -16, -40]}, {pos: [-36, -19, -6], yaw: 90}, {pos: [-52, -8, -7]}, {pos: [-55, -19, 5], yaw: 270}, {pos: [-42, -19, 9]}, {pos: [-56, -7, 13], yaw: 270}, {pos: [-17, -7, -7]}, {pos: [28, -7, 25], yaw: 90}, {pos: [28, -7, 26], yaw: 90}, {pos: [24, -20, 71], yaw: 180}, {pos: [42, -20, 36], yaw: 180}, {pos: [-19, -16, -40]}, {pos: [-55, -19, 6], yaw: 270}, {pos: [-4, -7, 23], yaw: 180}, {pos: [-56, -8, 12], yaw: 270}, {pos: [-20, -16, -40]}, {pos: [23, -19, 71], yaw: 180}, {pos: [28, -20, 24], yaw: 270}, {pos: [-56, -8, 11], yaw: 270}, {pos: [-33, -7, -7]}, {pos: [-52, -7, -7]}, {pos: [40, -19, 48], yaw: 90}, {pos: [-33, -19, 0]}, {pos: [-56, -8, 4], yaw: 270}, {pos: [40, -19, 49], yaw: 90}, {pos: [-7, -20, 62], yaw: 180}, {pos: [-24, -20, 28], yaw: 180}, {pos: [28, -19, 26], yaw: 270}, {pos: [-29, -16, -40]}, {pos: [-3, -11, -12], yaw: 90}, {pos: [-11, -20, 24], yaw: 270}, {pos: [-3, -14, -30], yaw: 90}, {pos: [40, -19, 65], yaw: 90}, {pos: [-42, -20, 9]}, {pos: [-3, -11, -13], yaw: 90}, {pos: [8, -20, 22], yaw: 90}, {pos: [-36, -20, -5], yaw: 90}, {pos: [-3, -10, -14], yaw: 90}, {pos: [-36, -20, -4], yaw: 90}, {pos: [-3, -13, -29], yaw: 90}, {pos: [-32, -8, -7]}, {pos: [42, -19, 36], yaw: 180}, {pos: [-7, -19, 62], yaw: 180}, {pos: [-33, -8, -7]}, {pos: [-42, -8, 17], yaw: 180}, {pos: [-41, -20, 9]}, {pos: [-18, -20, 40], yaw: 270}, {pos: [-43, -7, 27], yaw: 90}, {pos: [-46, -7, 19], yaw: 90}, {pos: [23, -20, 71], yaw: 180}, {pos: [-64, -19, -15], yaw: 270}, {pos: [40, -20, 48], yaw: 90}, {pos: [-56, -7, 12], yaw: 270}, {pos: [-41, -19, 9]}, {pos: [-18, -19, 38], yaw: 270}, {pos: [-11, -19, 24], yaw: 270}, {pos: [-16, -8, -7]}, {pos: [-18, -20, 5], yaw: 90}, {pos: [40, -19, 66], yaw: 90}, {pos: [43, -19, 36], yaw: 180}, {pos: [-64, -20, -15], yaw: 270}, {pos: [-3, -13, -28], yaw: 90}, {pos: [-18, -19, 4], yaw: 90}, {pos: [-34, -8, -7]}, {pos: [-5, -19, 62], yaw: 180}, {pos: [16, -7, 40], yaw: 180}, {pos: [44, -20, 21]}, {pos: [8, -20, 24], yaw: 90}, {pos: [-32, -7, 23], yaw: 180}, {pos: [-55, -19, 4], yaw: 270}, {pos: [17, -8, 7]}, {pos: [-32, -7, -7]}, {pos: [-46, -7, 20], yaw: 90}, {pos: [-43, -7, 29], yaw: 90}, {pos: [40, -19, 67], yaw: 90}, {pos: [8, -8, 26], yaw: 270}, {pos: [-4, -8, 23], yaw: 180}], start_commands: [], doors: [{back_name: "Accueil", price: 1250, blocks: [{pos: [-52, -6, 24]}, {pos: [-49, -8, 24]}, {pos: [-50, -7, 24]}, {pos: [-51, -8, 24]}, {pos: [-51, -9, 24]}, {pos: [-52, -8, 24]}, {pos: [-50, -8, 24]}, {pos: [-53, -7, 24]}, {pos: [-49, -9, 24]}, {pos: [-51, -7, 24]}, {pos: [-51, -5, 24]}, {pos: [-52, -7, 24]}, {pos: [-50, -5, 24]}, {pos: [-53, -6, 24]}, {pos: [-52, -9, 24]}, {pos: [-50, -9, 24]}, {pos: [-53, -8, 24]}, {pos: [-49, -7, 24]}, {pos: [-51, -6, 24]}, {pos: [-49, -6, 24]}, {pos: [-50, -6, 24]}, {pos: [-52, -5, 24]}, {pos: [-53, -9, 24]}], name: "Escalier", block: "minecraft:waxed_oxidized_copper_bars", back_group_id: 3, link_id: 4, yaw: 180}, {back_name: "Experimentation", price: 1750, blocks: [{pos: [8, -17, 58]}, {pos: [8, -18, 55], block: "minecraft:waxed_copper_bars"}, {pos: [8, -18, 57], block: "minecraft:waxed_copper_bars"}, {pos: [8, -21, 59], block: "minecraft:waxed_copper_bars"}, {pos: [8, -20, 55], block: "minecraft:waxed_copper_bars"}, {pos: [8, -20, 57], block: "minecraft:waxed_copper_bars"}, {pos: [8, -20, 56], block: "minecraft:waxed_copper_bars"}, {pos: [8, -18, 58], block: "minecraft:waxed_copper_bars"}, {pos: [8, -18, 56], block: "minecraft:waxed_copper_bars"}, {pos: [8, -18, 59], block: "minecraft:waxed_copper_bars"}, {pos: [8, -21, 57], block: "minecraft:waxed_copper_bars"}, {pos: [8, -20, 59], block: "minecraft:waxed_copper_bars"}, {pos: [8, -19, 58], block: "minecraft:waxed_copper_bars"}, {pos: [8, -19, 56], block: "minecraft:waxed_copper_bars"}, {pos: [8, -20, 58], block: "minecraft:waxed_copper_bars"}, {pos: [8, -19, 59], block: "minecraft:waxed_copper_bars"}, {pos: [8, -17, 57]}, {pos: [8, -17, 56]}, {pos: [8, -21, 55], block: "minecraft:waxed_copper_bars"}, {pos: [8, -19, 57], block: "minecraft:waxed_copper_bars"}, {pos: [8, -19, 55], block: "minecraft:waxed_copper_bars"}, {pos: [8, -21, 56], block: "minecraft:waxed_copper_bars"}, {pos: [8, -21, 58], block: "minecraft:waxed_copper_bars"}], name: "Archive", block: "minecraft:waxed_oxidized_copper_bars", back_group_id: 7, link_id: 8, yaw: 90}, {price: 2000, blocks: [{pos: [-49, -17, 0]}, {pos: [-49, -20, 0]}, {pos: [-50, -20, 0]}, {pos: [-52, -21, 0]}, {pos: [-49, -18, 0]}, {pos: [-49, -21, 0]}, {pos: [-51, -17, 0]}, {pos: [-51, -18, 0]}, {pos: [-48, -21, 0]}, {pos: [-48, -20, 0]}, {pos: [-49, -19, 0]}, {pos: [-51, -20, 0]}, {pos: [-48, -18, 0]}, {pos: [-52, -20, 0]}, {pos: [-50, -19, 0]}, {pos: [-48, -19, 0]}, {pos: [-51, -19, 0]}, {pos: [-52, -18, 0]}, {pos: [-50, -18, 0]}, {pos: [-50, -17, 0]}, {pos: [-52, -19, 0]}, {pos: [-51, -21, 0]}, {pos: [-50, -21, 0]}], name: "Atelier", block: "minecraft:waxed_copper_bars", link_id: 6}, {back_name: "Laboratoire", price: 1750, blocks: [{pos: [-18, -17, 13]}, {pos: [-18, -18, 12]}, {pos: [-18, -19, 12]}, {pos: [-18, -21, 16]}, {pos: [-18, -19, 13]}, {pos: [-18, -21, 14]}, {pos: [-18, -19, 15]}, {pos: [-18, -21, 15]}, {pos: [-18, -20, 12]}, {pos: [-18, -21, 12]}, {pos: [-18, -17, 15]}, {pos: [-18, -19, 16]}, {pos: [-18, -18, 16]}, {pos: [-18, -20, 14]}, {pos: [-18, -17, 14], block: "minecraft:waxed_oxidized_copper_bars"}, {pos: [-18, -20, 13]}, {pos: [-18, -18, 14]}, {pos: [-18, -21, 13]}, {pos: [-18, -20, 15]}, {pos: [-18, -18, 13]}, {pos: [-18, -18, 15]}, {pos: [-18, -20, 16]}, {pos: [-18, -19, 14]}], name: "Experimentation", block: "minecraft:waxed_copper_bars", back_group_id: 5, link_id: 7, yaw: 90}, {back_name: "Parking", blocks: [{pos: [-38, -6, 11]}, {pos: [-38, -6, 12]}, {pos: [-38, -5, 13]}, {pos: [-38, -7, 13]}, {pos: [-38, -7, 14]}, {pos: [-38, -5, 12]}, {pos: [-38, -9, 12]}, {pos: [-38, -8, 12]}, {pos: [-38, -5, 11]}, {pos: [-38, -8, 14]}, {pos: [-38, -8, 10]}, {pos: [-38, -6, 13]}, {pos: [-38, -7, 10]}, {pos: [-38, -7, 12]}, {pos: [-38, -9, 14]}, {pos: [-38, -9, 10]}, {pos: [-38, -7, 11]}, {pos: [-38, -9, 13]}, {pos: [-38, -8, 11]}, {pos: [-38, -9, 11]}, {pos: [-38, -6, 10]}, {pos: [-38, -6, 14]}, {pos: [-38, -8, 13]}], name: "Accueil", block: "minecraft:waxed_oxidized_copper_bars", link_id: 3, yaw: 270}, {back_name: "Cafétéria", blocks: [{pos: [3, -8, 14]}, {pos: [3, -6, 12]}, {pos: [3, -9, 11]}, {pos: [3, -7, 10]}, {pos: [3, -7, 13]}, {pos: [3, -6, 14]}, {pos: [3, -5, 11]}, {pos: [3, -8, 11]}, {pos: [3, -7, 12]}, {pos: [3, -7, 14]}, {pos: [3, -5, 13]}, {pos: [3, -9, 10]}, {pos: [3, -5, 12]}, {pos: [3, -6, 10]}, {pos: [3, -6, 13]}, {pos: [3, -8, 12]}, {pos: [3, -7, 11]}, {pos: [3, -9, 12]}, {pos: [3, -8, 13]}, {pos: [3, -9, 14]}, {pos: [3, -8, 10]}, {pos: [3, -9, 13]}, {pos: [3, -6, 11]}], name: "Parking", block: "minecraft:waxed_oxidized_copper_bars", back_group_id: 10, link_id: 11, yaw: 270}, {back_name: "Archive", price: 1500, blocks: [{pos: [22, -21, 44]}, {pos: [23, -18, 44]}, {pos: [22, -19, 44]}, {pos: [26, -19, 44]}, {pos: [23, -17, 44]}, {pos: [26, -18, 44]}, {pos: [24, -21, 44]}, {pos: [26, -20, 44]}, {pos: [24, -19, 44]}, {pos: [22, -18, 44]}, {pos: [26, -21, 44]}, {pos: [25, -20, 44]}, {pos: [23, -20, 44]}, {pos: [24, -18, 44]}, {pos: [25, -21, 44]}, {pos: [24, -17, 44]}, {pos: [23, -21, 44]}, {pos: [24, -20, 44]}, {pos: [25, -18, 44]}, {pos: [25, -19, 44]}, {pos: [23, -19, 44]}, {pos: [25, -17, 44]}, {pos: [22, -20, 44]}], name: "Escalier", block: "minecraft:waxed_copper_bars", back_group_id: 8, link_id: 9}, {blocks: [{pos: [-6, -5, 2]}, {pos: [-7, -5, 2]}, {pos: [-8, -5, 2]}, {pos: [-7, -9, 2]}, {pos: [-9, -6, 2]}, {pos: [-9, -8, 2]}, {pos: [-5, -9, 2]}, {pos: [-6, -6, 2]}, {pos: [-5, -6, 2]}, {pos: [-7, -8, 2]}, {pos: [-9, -9, 2]}, {pos: [-6, -7, 2]}, {pos: [-8, -8, 2]}, {pos: [-7, -7, 2]}, {pos: [-6, -9, 2]}, {pos: [-5, -7, 2]}, {pos: [-8, -9, 2]}, {pos: [-5, -8, 2]}, {pos: [-8, -7, 2]}, {pos: [-8, -6, 2]}, {pos: [-9, -7, 2]}, {pos: [-7, -6, 2]}, {pos: [-6, -8, 2]}], name: "Parking", block: "minecraft:waxed_oxidized_copper_bars", link_id: 2, yaw: 180}, {back_name: "Escalier", price: 1500, blocks: [{pos: [-43, -21, 27]}, {pos: [-43, -19, 27]}, {pos: [-40, -19, 27]}, {pos: [-42, -20, 27]}, {pos: [-42, -19, 27]}, {pos: [-40, -18, 27]}, {pos: [-42, -17, 27]}, {pos: [-40, -21, 27]}, {pos: [-41, -21, 27]}, {pos: [-43, -20, 27]}, {pos: [-39, -18, 27]}, {pos: [-39, -21, 27]}, {pos: [-39, -19, 27]}, {pos: [-40, -17, 27]}, {pos: [-40, -20, 27]}, {pos: [-42, -18, 27]}, {pos: [-41, -19, 27]}, {pos: [-42, -21, 27]}, {pos: [-41, -20, 27]}, {pos: [-41, -17, 27]}, {pos: [-41, -18, 27]}, {pos: [-43, -18, 27]}, {pos: [-39, -20, 27]}], name: "Laboratoire", block: "minecraft:waxed_copper_bars", back_group_id: 4, link_id: 5}, {back_name: "Escalier", price: 1250, blocks: [{pos: [20, -6, 28]}, {pos: [20, -6, 25]}, {pos: [21, -7, 26]}, {pos: [20, -5, 27]}, {pos: [20, -5, 26]}, {pos: [20, -6, 27]}, {pos: [20, -6, 24]}, {pos: [20, -5, 25]}, {pos: [20, -8, 26]}, {pos: [20, -9, 24]}, {pos: [20, -7, 25]}, {pos: [20, -9, 27]}, {pos: [20, -7, 27]}, {pos: [20, -7, 24]}, {pos: [20, -9, 26]}, {pos: [20, -7, 26]}, {pos: [20, -9, 28]}, {pos: [20, -9, 25]}, {pos: [20, -7, 28]}, {pos: [20, -8, 27]}, {pos: [20, -8, 25]}, {pos: [20, -8, 24]}, {pos: [20, -8, 28]}], name: "Cafétéria", block: "minecraft:waxed_oxidized_copper_bars", back_group_id: 9, link_id: 10, yaw: 270}, {blocks: [{pos: [-16, -16, -28]}, {pos: [-16, -16, -30]}, {pos: [-16, -16, -29]}, {pos: [-16, -15, -30]}, {pos: [-16, -18, -28]}, {pos: [-16, -17, -30]}, {pos: [-16, -16, -31]}, {pos: [-16, -14, -28]}, {pos: [-16, -15, -27]}, {pos: [-16, -14, -30]}, {pos: [-16, -17, -31]}, {pos: [-16, -18, -30]}, {pos: [-16, -16, -27]}, {pos: [-16, -18, -31]}, {pos: [-16, -15, -28]}, {pos: [-16, -18, -29]}, {pos: [-16, -17, -28]}, {pos: [-16, -18, -27]}, {pos: [-16, -17, -29]}, {pos: [-16, -14, -29]}, {pos: [-16, -15, -31]}, {pos: [-16, -17, -27]}, {pos: [-16, -15, -29]}], name: "Corridor", block: "minecraft:waxed_oxidized_copper_bars", link_id: 1, yaw: 90}], traps: [], pap_machines: [{pos: [46, -21, 32], yaw: 90}], name: "Beyonds", power_switch: [{pos: [-57, -20, -17]}], boundaries: [[-89, -28, -57], [61, 14, 95]], id: "beyounds", mystery_box: {positions: [{location_name: "Experimentation", pos: [-6, -21, 10]}, {location_name: "Parking", pos: [-13, -9, -3], yaw: 90}, {location_name: "Escalier", pos: [-38, -15, 37], yaw: 90}, {location_name: "Escalier", pos: [16, -9, 23]}]}, perks: [{pos: [1, -9, 56], perk_id: "tombstone", yaw: 180}, {pos: [-17, -21, 48], perk_id: "speed_cola", yaw: 270}, {pos: [-24, -17, -42], perk_id: "quick_revive"}, {pos: [46, -21, 25], perk_id: "deadshot", yaw: 90}, {pos: [-28, -9, 25], yaw: 180}, {pos: [9, -9, 18], perk_id: "electric_cherry", yaw: 270}, {pos: [-46, -21, 5], perk_id: "stamin_up", yaw: 90}, {pos: [-21, -9, 55], perk_id: "double_tap", yaw: 180}], dimension: "mgs:zombies", respawn_commands: []}"""
	write_versioned_function("maps/zombies/kino_der_toten/register", f"""
execute unless data storage {ns}:maps zombies[{{id:"kino_der_toten"}}] run data modify storage {ns}:maps zombies append value {kino_der_toten_map}
""", tags=[f"{ns}:zombies/register_maps"])

	write_load_file(f"""
execute unless data storage {ns}:maps zombies run data modify storage {ns}:maps zombies set value []
function #{ns}:zombies/register_maps
""")

	write_versioned_function("maps/zombies/beyounds/register", f"""
execute unless data storage {ns}:maps zombies[{{id:"beyounds"}}] run data modify storage {ns}:maps zombies append value {beyounds_map}
""", tags=[f"{ns}:zombies/register_maps"])

	# "leave" runs from zombies/stop, after the state left "active", so only map_id gates it.
	guard = (
		f'execute if data storage {ns}:temp _base{{mode:"zombies"}}'
		f' if data storage {ns}:zombies game{{state:"active"}}'
		f' if data storage {ns}:zombies game{{map_id:"kino_der_toten"}}'
	)
	leave_guard = f'execute if data storage {ns}:temp _base{{mode:"zombies"}} if data storage {ns}:zombies game{{map_id:"kino_der_toten"}}'
	for script in ["start", "tick", "join", "leave", "respawn", "power"]:
		script_guard = leave_guard if script == "leave" else guard
		write_versioned_function(f"maps/zombies/kino_der_toten/calls/{script}",
			f"{script_guard} run return run function {ns}:v{version}/maps/zombies/kino_der_toten/{script}",
			tags=[f"{ns}:maps/{script}_script"]
		)

	write_versioned_function("maps/zombies/kino_der_toten/start", f"""
scoreboard players set #kino_tp_state {ns}.data 0
scoreboard players set #kino_tp_timer {ns}.data 0
scoreboard players set #kino_tp_cd {ns}.data 0
scoreboard players set #kino_met_count {ns}.data 0

# Lobby to theater door starts closed.
execute positioned ~-19 ~0 ~-1 run fill ~ ~ ~ ~ ~2 ~2 cobblestone

## Teleporter
execute positioned ~-57 ~-1 ~9 run summon interaction ~ ~ ~ {{Tags:["{ns}.kino","{ns}.zombies_entity","{ns}.kino.teleporter","{ns}.kino.teleporter_theater"],width:1.0f,height:2.0f}}
execute positioned ~ ~ ~ run summon interaction ~ ~ ~ {{Tags:["{ns}.kino","{ns}.zombies_entity","{ns}.kino.teleporter","{ns}.kino.teleporter_lobby"],width:1.0f,height:1.0f}}

## Meteorites
execute positioned ~-12 ~0 ~-5 run summon interaction ~ ~ ~ {{Tags:["{ns}.kino","{ns}.zombies_entity","{ns}.kino.meteorite_1"],width:1.1f,height:2.1f}}
execute positioned ~-58 ~-2 ~-22 run summon interaction ~ ~ ~ {{Tags:["{ns}.kino","{ns}.zombies_entity","{ns}.kino.meteorite_2"],width:1.1f,height:2.1f}}
execute positioned ~-54 ~4 ~39 run summon interaction ~ ~ ~ {{Tags:["{ns}.kino","{ns}.zombies_entity","{ns}.kino.meteorite_3"],width:1.1f,height:2.1f}}

execute as @e[tag={ns}.kino] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/maps/zombies/kino_der_toten/on_right_click",executor:"target"}}
execute as @e[tag={ns}.kino.teleporter] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/on_hover",executor:"source"}}
""")

	# tick
	write_versioned_function("maps/zombies/kino_der_toten/tick", f"""
function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/tick
""")

	# join
	write_versioned_function("maps/zombies/kino_der_toten/join", """
""")

	# leave
	write_versioned_function("maps/zombies/kino_der_toten/leave", f"""
kill @e[tag={ns}.kino]

tag @a remove {ns}.kino.in_tp

scoreboard players set #kino_tp_state {ns}.data 0
scoreboard players set #kino_tp_timer {ns}.data 0
scoreboard players set #kino_tp_cd {ns}.data 0
scoreboard players set #kino_met_count {ns}.data 0
""")

	# respawn
	write_versioned_function("maps/zombies/kino_der_toten/respawn", """
""")

	# on_right_click
	write_versioned_function("maps/zombies/kino_der_toten/on_right_click", f"""
# Run as the clicked interaction; `on target` reaches the player.
execute if entity @s[tag={ns}.kino.teleporter_theater] run return run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/on_theater_click
execute if entity @s[tag={ns}.kino.teleporter_lobby] run return run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/on_lobby_click
execute if entity @s[tag={ns}.kino.meteorite_1] run return run function {ns}:v{version}/maps/zombies/kino_der_toten/meteorite/on_click
execute if entity @s[tag={ns}.kino.meteorite_2] run return run function {ns}:v{version}/maps/zombies/kino_der_toten/meteorite/on_click
execute if entity @s[tag={ns}.kino.meteorite_3] run return run function {ns}:v{version}/maps/zombies/kino_der_toten/meteorite/on_click
""")

	# teleporter/on_theater_click
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/on_theater_click", f"""
# State 0 (idle): start linking, the player must now click the lobby pad.
execute if score #kino_tp_state {ns}.data matches 0 run return run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/start_link
# State 2 (armed): teleport.
execute if score #kino_tp_state {ns}.data matches 2 at @s run return run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/activate
# States 1 and 3 to 6 (linking, active, returning, cooldown): deny.
execute on target at @s run {deny_recharging}
""")

	# teleporter/on_hover
	def hover_line(states: str, text: str, color: str, pad: str = "", suffix: str = "") -> str:
		pad_check: str = f" if entity @n[tag=bs.interaction.target,tag={ns}.kino.teleporter_{pad}]" if pad else ""
		return (
			f'execute if score #kino_tp_state {ns}.data matches {states}{pad_check} run data modify storage smithed.actionbar:input message set value '
			f'{{json:[{{"text":"⚡ ","color":"white"}},{{"text":"Teleporter","color":"yellow"}},{{"text":" - {text}","color":"{color}"}}{suffix}],priority:"conditional",freeze:5}}'
		)
	seconds_left: str = f',{{"score":{{"name":"#kino_tp_sec","objective":"{ns}.data"}},"color":"white"}},{{"text":"s","color":"gray"}}'
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/on_hover", f"""
# Run as the player looking at a pad. Whole seconds left of the timer of the current state, rounded up.
scoreboard players operation #kino_tp_sec {ns}.data = #kino_tp_timer {ns}.data
execute if score #kino_tp_state {ns}.data matches 6 run scoreboard players operation #kino_tp_sec {ns}.data = #kino_tp_cd {ns}.data
scoreboard players add #kino_tp_sec {ns}.data 19
scoreboard players operation #kino_tp_sec {ns}.data /= #20 {ns}.data

{hover_line("0", "Click to start the link", "gray", "theater")}
{hover_line("0", "Start the link at the theater pad", "gray", "lobby")}
{hover_line("1", "Waiting for the lobby pad", "gold", "theater")}
{hover_line("1", "Click to complete the link", "green", "lobby")}
{hover_line("2", "Linked, click to teleport", "green", "theater")}
{hover_line("2", "Linked, use the theater pad", "green", "lobby")}
{hover_line("3", "Teleporting...", "aqua")}
{hover_line("4", "In use: ", "aqua", suffix=seconds_left)}
{hover_line("5", "Returning: ", "aqua", suffix=seconds_left)}
{hover_line("6", "Recharging: ", "red", suffix=seconds_left)}
function #smithed.actionbar:message
""")

	# teleporter/start_link
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/start_link", f"""
scoreboard players set #kino_tp_state {ns}.data 1
playsound minecraft:block.beacon.power_select block @a[distance=..50] ~ ~ ~ 1 1
tellraw @a[distance=..50] [{MGS_TAG},{{"text":"Teleporter link started.","color":"green"}}]
""")

	# teleporter/on_lobby_click
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/on_lobby_click", f"""
execute unless score #kino_tp_state {ns}.data matches 1 run return fail

# State 2 (armed): the next theater click teleports.
scoreboard players set #kino_tp_state {ns}.data 2
playsound minecraft:block.beacon.activate block @a[distance=..50] ~ ~ ~ 1 1
tellraw @a[distance=..50] [{MGS_TAG},{{"text":"Teleporter linked! Click the theater pad again to teleport.","color":"green"}}]
""")

	# teleporter/activate
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/activate", f"""
# Run as the theater interaction.
playsound minecraft:entity.lightning_bolt.thunder block @a[distance=..50] ~ ~ ~ 0.25 1
playsound minecraft:block.portal.trigger block @a[distance=..50] ~ ~ ~ 1 2

# State 3: 50-tick build-up.
scoreboard players set #kino_tp_state {ns}.data 3
scoreboard players set #kino_tp_timer {ns}.data 50
""")

	# teleporter/activating_tick
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/activating_tick", f"""

scoreboard players remove #kino_tp_timer {ns}.data 1

kill @e[tag={ns}.zombie_round,distance=..4]

particle electric_spark ~ ~1 ~ 0.6 0.6 0.6 0.1 30 normal

# Firework cue at ticks 40, 25 and 10.
execute if score #kino_tp_timer {ns}.data matches 40 run playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..30] ~ ~ ~ 1 1
execute if score #kino_tp_timer {ns}.data matches 25 run playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..30] ~ ~ ~ 1 1
execute if score #kino_tp_timer {ns}.data matches 10 run playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..30] ~ ~ ~ 1 1

execute if score #kino_tp_timer {ns}.data matches ..0 run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/do_teleport
""")

	# teleporter/do_teleport
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/do_teleport", f"""
# In-game players within 3 blocks go to the projection room.
tag @a[distance=..3,scores={{{ns}.zb.in_game=1}},gamemode=!spectator] add {ns}.kino.in_tp
tag @a[tag={ns}.kino.in_tp] add {ns}.{PAP_ROOM_TAG}
execute positioned ~57 ~1 ~-9 run tp @a[tag={ns}.kino.in_tp] ~-22 ~6 ~0
execute as @a[tag={ns}.kino.in_tp] at @s run playsound minecraft:entity.enderman.teleport block @s ~ ~ ~ 1 1

# State 4: 30 s in the projection room.
scoreboard players set #kino_tp_state {ns}.data 4
scoreboard players set #kino_tp_timer {ns}.data 600
""")

	# teleporter/tick
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/tick", f"""
# State 3: build-up, then teleport.
execute if score #kino_tp_state {ns}.data matches 3 at @e[tag={ns}.kino.teleporter_theater] run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/activating_tick

# States 4 to 6 count down in real time (#tick_delta), so one-shot cues fire when the timer crosses a threshold,
# not on an exact value a delta of 2+ could skip. State 4: projection room, then scatter to random lobby spots.
execute if score #kino_tp_state {ns}.data matches 4 run scoreboard players operation #kino_prev_t {ns}.data = #kino_tp_timer {ns}.data
execute if score #kino_tp_state {ns}.data matches 4 run scoreboard players operation #kino_tp_timer {ns}.data -= #tick_delta {ns}.data
execute if score #kino_tp_state {ns}.data matches 4 if score #kino_prev_t {ns}.data matches 31.. if score #kino_tp_timer {ns}.data matches ..30 as @a[tag={ns}.kino.in_tp] at @s run playsound minecraft:block.portal.trigger block @a[distance=..50] ~ ~ ~ 1 2
execute if score #kino_tp_state {ns}.data matches 4 if score #kino_tp_timer {ns}.data matches ..0 run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/return_players

# State 5: 5 s at the random spots, then everyone to the lobby pad.
execute if score #kino_tp_state {ns}.data matches 5 run scoreboard players operation #kino_prev_t {ns}.data = #kino_tp_timer {ns}.data
execute if score #kino_tp_state {ns}.data matches 5 run scoreboard players operation #kino_tp_timer {ns}.data -= #tick_delta {ns}.data
execute if score #kino_tp_state {ns}.data matches 5 if score #kino_prev_t {ns}.data matches 31.. if score #kino_tp_timer {ns}.data matches ..30 as @a[tag={ns}.kino.in_tp] at @s run playsound minecraft:block.portal.trigger block @a[distance=..50] ~ ~ ~ 1 2
execute if score #kino_tp_state {ns}.data matches 5 if score #kino_tp_timer {ns}.data matches ..0 run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/return_to_lobby

# State 6: cooldown, then idle.
execute if score #kino_tp_state {ns}.data matches 6 run scoreboard players operation #kino_prev_t {ns}.data = #kino_tp_cd {ns}.data
execute if score #kino_tp_state {ns}.data matches 6 run scoreboard players operation #kino_tp_cd {ns}.data -= #tick_delta {ns}.data
execute if score #kino_tp_state {ns}.data matches 6 if score #kino_prev_t {ns}.data matches 2.. if score #kino_tp_cd {ns}.data matches ..1 run tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The teleporter is ready to use again.","color":"green"}}]
execute if score #kino_tp_state {ns}.data matches 6 if score #kino_tp_cd {ns}.data matches ..0 run scoreboard players set #kino_tp_state {ns}.data 0
""")

	# teleporter/return_players
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/return_players", f"""
execute as @a[tag={ns}.kino.in_tp] run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/return_one
tag @a remove {ns}.{PAP_ROOM_TAG}
# kino.in_tp stays: return_to_lobby needs it 5 s later.

scoreboard players set #kino_tp_state {ns}.data 5
scoreboard players set #kino_tp_timer {ns}.data 100
""")

	# teleporter/return_to_lobby
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/return_to_lobby", f"""
execute as @a[tag={ns}.kino.in_tp] at @e[tag={ns}.kino.teleporter_lobby] run tp @s ~ ~ ~
execute at @n[tag={ns}.kino.in_tp] run playsound minecraft:entity.enderman.teleport block @a[distance=..50] ~ ~ ~ 1 1
execute at @n[tag={ns}.kino.in_tp] run kill @e[tag={ns}.zombie_round,distance=..4]

tag @a remove {ns}.kino.in_tp

# State 6: 1 min 30 s cooldown.
scoreboard players set #kino_tp_state {ns}.data 6
scoreboard players set #kino_tp_cd {ns}.data 1800
""")

	# teleporter/return_one
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/return_one", f"""
# Run as a returning player: pick one of 5 lobby spots.
execute store result score #tp_random {ns}.data run random value 1..5
execute if score #tp_random {ns}.data matches 1 run tp @s ~9 ~-4 ~-40
execute if score #tp_random {ns}.data matches 2 run tp @s ~-34 ~4 ~54
execute if score #tp_random {ns}.data matches 3 run tp @s ~-27 ~4 ~-82
execute if score #tp_random {ns}.data matches 4 run tp @s ~-97 ~7 ~13
execute if score #tp_random {ns}.data matches 5 run tp @s ~40 ~4 ~39
execute at @s run playsound minecraft:entity.enderman.teleport block @s ~ ~ ~ 1 1
""")

	# meteorite/on_click
	write_versioned_function("maps/zombies/kino_der_toten/meteorite/on_click", f"""
# Run as the meteorite interaction.
execute if entity @s[tag={ns}.kino.met_active] run return fail

tag @s add {ns}.kino.met_active
scoreboard players add #kino_met_count {ns}.data 1
execute at @s run playsound minecraft:block.beacon.activate block @a[distance=..50] ~ ~ ~ 1 1

# Third meteorite: play 115.
execute if score #kino_met_count {ns}.data matches 3 run function {ns}:v{version}/maps/zombies/kino_der_toten/meteorite/play_song
""")

	# meteorite/play_song
	write_versioned_function("maps/zombies/kino_der_toten/meteorite/play_song", f"""
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/music/115_song record @s ~ ~ ~ 0.2 1

# Reset so the song can be replayed.
tag @e[tag={ns}.kino.met_active] remove {ns}.kino.met_active
scoreboard players set #kino_met_count {ns}.data 0
""")

	# setup_lure: when every player hides in the PaP room, the horde gathers at the theater centre instead of the PaP door (see escort).
	# Runs from #{ns}:zombies/setup_lure positioned at the map base, so the marker sits at base + (~-49 ~-3 ~0).
	write_versioned_function("maps/zombies/kino_der_toten/setup_lure",
		f'execute if data storage {ns}:zombies game{{map_id:"kino_der_toten"}} positioned ~-49 ~-3 ~0 run summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.lure_center","{ns}.zombies_entity"]}}',
		tags=[f"{ns}:zombies/setup_lure"]
	)

	# power
	write_versioned_function("maps/zombies/kino_der_toten/power", """
execute positioned ~-19 ~0 ~-1 run fill ~ ~ ~ ~ ~2 ~2 air
""")

