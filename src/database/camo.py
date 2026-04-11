
# Imports
import os
from collections.abc import Callable
from copy import deepcopy
from typing import cast

import numpy as np
import stouputils as stp
from numpy.typing import NDArray
from PIL import Image
from stewbeet import Item, JsonDict, Mem

from ..config.stats import MODELS

# ---------------------------------------------------------------------------
# HSL Color blend (GIMP "HSL Color" mode)
# H + S come from the blend (material) layer, L comes from the base (weapon).
# Alpha is preserved from the base layer throughout.
# Fully vectorised with numpy — no per-pixel Python loops.
# ---------------------------------------------------------------------------

def rgb_to_hls(arr: NDArray[np.floating]) -> NDArray[np.floating]:
    """ (N, 3) floating RGB → (N, 3) floating HLS  (colorsys channel order: H, L, S). """
    r, g, b = arr[:, 0], arr[:, 1], arr[:, 2]
    maxc: NDArray[np.floating] = arr.max(axis=1)
    minc: NDArray[np.floating] = arr.min(axis=1)
    delta: NDArray[np.floating] = maxc - minc
    l_channel: NDArray[np.floating] = (maxc + minc) * 0.5

    denom_s = np.where(l_channel < 0.5, maxc + minc, 2.0 - maxc - minc)
    s_channel: NDArray[np.floating] = np.where(delta == 0, 0.0, delta / np.where(denom_s == 0, 1.0, denom_s))

    rc = np.where(delta == 0, 0.0, (maxc - r) / np.where(delta == 0, 1.0, delta))
    gc = np.where(delta == 0, 0.0, (maxc - g) / np.where(delta == 0, 1.0, delta))
    bc = np.where(delta == 0, 0.0, (maxc - b) / np.where(delta == 0, 1.0, delta))
    h_channel = np.where(
        delta == 0, 0.0,
        np.where(maxc == r, bc - gc,
        np.where(maxc == g, 2.0 + rc - bc, 4.0 + gc - rc))
    )
    h_channel = (h_channel / 6.0) % 1.0

    return np.stack([h_channel, l_channel, s_channel], axis=1)


def hls_to_rgb(hls: NDArray[np.floating]) -> NDArray[np.floating]:
    """(N, 3) floating HLS → (N, 3) floating RGB."""
    h_channel, l_channel, s_channel = hls[:, 0], hls[:, 1], hls[:, 2]
    m2: NDArray[np.floating] = np.where(l_channel <= 0.5, l_channel * (1.0 + s_channel), l_channel + s_channel - l_channel * s_channel)
    m1: NDArray[np.floating] = 2.0 * l_channel - m2

    def channel(hue: NDArray[np.floating]) -> NDArray[np.floating]:
        hue = hue % 1.0
        return np.where(
            hue < 1.0 / 6.0, m1 + (m2 - m1) * hue * 6.0,
            np.where(hue < 0.5, m2,
            np.where(hue < 2.0 / 3.0, m1 + (m2 - m1) * (2.0 / 3.0 - hue) * 6.0, m1))
        )

    r = np.where(s_channel == 0, l_channel, channel(h_channel + 1.0 / 3.0))
    g = np.where(s_channel == 0, l_channel, channel(h_channel))
    b = np.where(s_channel == 0, l_channel, channel(h_channel - 1.0 / 3.0))
    return np.stack([r, g, b], axis=1)


def hsl_color_blend(
    base_path: str, blend_path: str, out_path: str,
    gamma: float = 1.0, contrast: float = 1.0,
    l_blend: float = 0.0
) -> None:
    """ Write a blended PNG to *out_path* using GIMP's HSL Color mode:
      H + S → from blend (material texture)
      L     → from base  (weapon texture), with optional gamma & contrast
      Alpha → from base  (weapon texture), unchanged

    - gamma < 1.0  → brightens midtones → more metallic
    - gamma > 1.0  → darkens midtones   → more plastic/matte
    - contrast > 1 → increases contrast → sharper metallic highlights
    - contrast < 1 → flattens contrast  → softer, more plastic look
    - l_blend = 0.0 → L unchanged from base
    - l_blend > 0.0 → blend some L from material (e.g. for a brighter, more reflective metal)
    """
    base_img: Image.Image = Image.open(base_path).convert("RGBA")
    blend_img: Image.Image = Image.open(blend_path).convert("RGBA").resize(base_img.size, Image.Resampling.NEAREST)

    base_arr: NDArray[np.floating] = np.array(base_img,  dtype=np.float32) / 255.0   # (H, W, 4)
    blend_arr: NDArray[np.floating] = np.array(blend_img, dtype=np.float32) / 255.0

    height, width = base_arr.shape[:2]
    hls_base: NDArray[np.floating] = rgb_to_hls(base_arr[:, :, :3].reshape(-1, 3))   # 0=H 1=L 2=S
    hls_blend: NDArray[np.floating] = rgb_to_hls(blend_arr[:, :, :3].reshape(-1, 3))

    hls_out: NDArray[np.floating] = hls_base.copy()
    hls_out[:, 0] = hls_blend[:, 0]   # H ← material
    hls_out[:, 2] = hls_blend[:, 2]   # S ← material
    hls_out[:, 1] = (1.0 - l_blend) * hls_base[:, 1] + l_blend * hls_blend[:, 1]   # L ← blend of weapon & material

    # --- Gamma + contrast applied to L channel (weapon luminance) ---
    l_channel: NDArray[np.floating] = hls_out[:, 1]
    l_channel = np.power(np.clip(l_channel, 1e-6, 1.0), gamma)
    l_channel = np.clip((l_channel - 0.5) * contrast + 0.5, 0.0, 1.0)
    hls_out[:, 1] = l_channel

    out_arr: NDArray[np.floating] = base_arr.copy()
    out_arr[:, :, :3] = hls_to_rgb(hls_out).reshape(height, width, 3)   # alpha untouched

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    Image.fromarray((out_arr * 255.0).clip(0, 255).astype(np.uint8)).save(out_path)

def overlay_blend(
    base_path: str, blend_path: str, out_path: str,
    gamma: float = 0.75, contrast: float = 1.4
) -> None:
    """
    GIMP Overlay blend with optional pre-blend contrast & gamma correction.

    - gamma < 1.0  → brightens midtones → more metallic
    - gamma > 1.0  → darkens midtones  → more plastic/matte
    - contrast > 1 → increases contrast → sharper metallic highlights
    - contrast < 1 → flattens contrast  → softer, more plastic look
    """
    base_img: Image.Image = Image.open(base_path).convert("RGBA")
    blend_img: Image.Image = Image.open(blend_path).convert("RGBA").resize(base_img.size, Image.Resampling.NEAREST)

    base_arr: NDArray[np.floating] = np.array(base_img,  dtype=np.float32) / 255.0
    blend_arr: NDArray[np.floating] = np.array(blend_img, dtype=np.float32) / 255.0

    b: NDArray[np.floating]  = base_arr[:, :, :3]
    bl: NDArray[np.floating] = blend_arr[:, :, :3]

    # --- Pre-blend: gamma + contrast on base RGB (alpha untouched) ---
    b_adjusted: NDArray[np.floating] = np.power(np.clip(b, 1e-6, 1.0), gamma)          # gamma
    b_adjusted = np.clip((b_adjusted - 0.5) * contrast + 0.5, 0.0, 1.0)               # contrast

    # --- Overlay (conditioned on adjusted base) ---
    overlay: NDArray[np.floating] = np.where(
        b_adjusted <= 0.5,
        2.0 * b_adjusted * bl,
        1.0 - 2.0 * (1.0 - b_adjusted) * (1.0 - bl)
    )

    out_arr: NDArray[np.floating] = base_arr.copy()
    out_arr[:, :, :3] = np.clip(overlay, 0.0, 1.0)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    Image.fromarray((out_arr * 255.0).clip(0, 255).astype(np.uint8)).save(out_path)

BlendFunc = Callable[[str, str, str], None]

# Maps each material name to its blend function.
# To add a new material, just add an entry here — no other changes needed.
MATERIALS: dict[str, BlendFunc] = {
    "gold":                 lambda b, bl, o: hsl_color_blend(b, bl, o, l_blend=1.0),
    "autumn":               overlay_blend,
    "galaxy":               hsl_color_blend,
    "red_polymer_stripes":  hsl_color_blend,
}
COMMON_IGNORE: tuple[str, ...] = ("acogdetails", "holodetails", "kobradetails", "reticles", "reticles_1024")
GOLD_DEFAULT_IGNORE_TEXTURE: tuple[str, ...] = (
    *COMMON_IGNORE,
    "metal", "metal_bright", "metal_brighter", "metal_dark",
    "akdetails", "glock18details", "augdetails", "m82details"
)

# Allow to override functions and ignored textures on a per-weapon basis
OVERRIDES: dict[str, dict[str, list[str] | BlendFunc | tuple[str, ...]]] = {
    "m249": {"apply_to": ["gold"], "ignore_textures": ("brass", "copper", "metal", "metal_bright", "metal_dark", *COMMON_IGNORE)},
    "m4a1": {"apply_to": ["gold"], "ignore_textures": ("m4details", "ardetails2", *COMMON_IGNORE)},
    "m16a4": {"apply_to": ["gold"], "ignore_textures": ("ardetails2", *COMMON_IGNORE)},
    "m24": {"apply_to": ["gold"], "ignore_textures": ("metal_dark", "m24details", *COMMON_IGNORE)},
    "mac10": {"apply_to": ["gold"], "ignore_textures": COMMON_IGNORE},
    "mp5": {"apply_to": ["gold"], "ignore_textures": ("rubber_cross", *COMMON_IGNORE)},
    "mp7": {"apply_to": ["gold"], "ignore_textures": ("metal", "mp7details", *COMMON_IGNORE)},
    "ppsh41": {"apply_to": ["gold"], "ignore_textures": ("ppshdetails", "ppshwood", *COMMON_IGNORE)},
    "spas12": {"apply_to": ["gold"], "ignore_textures": ("metal", "spas12details", *COMMON_IGNORE)},
    "sten": {"apply_to": ["gold"], "ignore_textures": COMMON_IGNORE},
    "m1911": {"apply_to": ["gold"], "ignore_textures": COMMON_IGNORE},
    "m9": {"apply_to": ["gold"], "ignore_textures": COMMON_IGNORE},
    "deagle": {"apply_to": ["gold"], "ignore_textures": ("rubber", "deagledetails", *COMMON_IGNORE)},
    "makarov": {"apply_to": ["gold"], "ignore_textures": COMMON_IGNORE},
    "glock17": {"apply_to": ["gold"], "ignore_textures": ("glock17_polymer_dots", *COMMON_IGNORE)},
    "vz61": {"apply_to": ["gold"], "ignore_textures": ("vz61grip", "vz61wood", *COMMON_IGNORE)},
    "ray_gun": {"apply_to": ["gold"], "func": lambda b, bl, o: hsl_color_blend(b, bl, o, l_blend=0.0)},
}

def blend_texture(weapon_texture_path: str, material_texture_path: str, out_path: str, base_weapon: str, material: str) -> None:
    """ Blend with cache — skips redundant work when variants share a base texture. """
    if os.path.exists(out_path):
        return
    override_info = OVERRIDES.get(base_weapon, {})
    if override_info.get("apply_to") and material not in cast(list[str], override_info["apply_to"]):
        override_info = {}  # Ignore this override if it's not meant to be applied to the current material
    func = cast(BlendFunc, override_info.get("func", MATERIALS[material]))
    func(weapon_texture_path, material_texture_path, out_path)


# Main function
@stp.measure_time(message="Generated camouflage variants")
def main() -> None:
    ns: str = Mem.ctx.project_id
    textures_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")
    queue: list[tuple[str, str, str, str, str]] = []  # (weapon_texture_path, material_texture_path, out_path, base_weapon, material)

    # For each weapon, make variants with only one material (e.g. wood, metal, gold, etc.)
    weapons: list[Item] = [
        Item.from_id(item)
        for item in Mem.definitions.keys()
        if Item.from_id(item).components.get("custom_data", {}).get(ns, {}).get("gun")
    ]
    for material in MATERIALS:
        material_texture_path: str = f"{textures_folder}/{material}.png"

        for weapon in weapons:
            base_id: str = weapon.id.replace("_zoom", "")
            item_id: str = (
                f"{base_id}_{material}"
                if not weapon.id.endswith("_zoom")
                else f"{base_id}_{material}_zoom"
            )
            item: Item = Item(
                id=item_id, base_item=weapon.base_item, components=deepcopy(weapon.components), override_model=weapon.override_model
            )

            # Define normal and zoom models
            gun_stats: JsonDict = item.components["custom_data"].get(ns, {}).get("stats", {})
            normal_model: str = f"{ns}:{base_id}"
            zoom_model: str = normal_model + "_zoom"
            gun_stats[MODELS] = {"normal": normal_model, "zoom": zoom_model}
            base_weapon: str = gun_stats.get("base_weapon", base_id)

            # Merge textures in override model using HSL Color mode
            if item.override_model:
                item.override_model = item.override_model.copy()
                item.override_model["textures"] = item.override_model.get("textures", {}).copy()
                for key, texture in item.override_model["textures"].items():
                    override_info = OVERRIDES.get(base_weapon, {})
                    if override_info.get("apply_to") and material not in cast(list[str], override_info["apply_to"]):
                        override_info = {}  # Ignore this override if it's not meant to be applied to the current material
                    ignore_textures = cast(tuple[str, ...], override_info.get("ignore_textures", GOLD_DEFAULT_IGNORE_TEXTURE if material == "gold" else COMMON_IGNORE))
                    if any(texture.endswith(f"/{x}") for x in ignore_textures):
                        continue

                    # Resolve weapon texture PNG from its namespaced path (e.g. "mgs:item/ak47")
                    texture_file: str = texture.split("/")[-1]
                    if texture_file == material:
                        continue  # Some models reuse the material texture directly as their override texture — skip blending in this case
                    weapon_texture_path: str = f"{textures_folder}/{texture_file}.png"

                    blended_name: str = f"{texture_file}_{material}"
                    blended_out_path: str = f"{textures_folder}/blended_camo/{blended_name}.png"

                    queue.append((weapon_texture_path, material_texture_path, blended_out_path, base_weapon, material))

                    item.override_model["textures"][key] = f"{ns}:item/{blended_name}"

    # Blend textures in parallel with multiprocessing
    stp.multiprocessing(blend_texture, stp.unique_list(queue), use_starmap=True, desc="Blending camo textures", max_workers=1)

