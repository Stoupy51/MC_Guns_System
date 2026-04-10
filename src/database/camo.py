
# Imports
import os
from collections.abc import Callable
from copy import deepcopy

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


def hsl_color_blend(base_path: str, blend_path: str, out_path: str) -> None:
    """ Write a blended PNG to *out_path* using GIMP's HSL Color mode:
      H + S → from blend (material texture)
      L     → from base  (weapon texture)
      Alpha → from base  (weapon texture), unchanged

    Args:
        base_path  (str): File path to the base weapon texture PNG.
        blend_path (str): File path to the material texture PNG.
        out_path   (str): File path to save the blended PNG output.
    """
    base_img: Image.Image = Image.open(base_path).convert("RGBA")
    blend_img: Image.Image = Image.open(blend_path).convert("RGBA").resize(base_img.size, Image.Resampling.NEAREST)

    base_arr: NDArray[np.floating] = np.array(base_img,  dtype=np.float32) / 255.0   # (H, W, 4)
    blend_arr: NDArray[np.floating] = np.array(blend_img, dtype=np.float32) / 255.0

    h, w = base_arr.shape[:2]
    hls_base: NDArray[np.floating] = rgb_to_hls(base_arr[:, :, :3].reshape(-1, 3))   # 0=H 1=L 2=S
    hls_blend: NDArray[np.floating] = rgb_to_hls(blend_arr[:, :, :3].reshape(-1, 3))

    hls_out: NDArray[np.floating] = hls_base.copy()
    hls_out[:, 0] = hls_blend[:, 0]   # H ← material
    hls_out[:, 2] = hls_blend[:, 2]   # S ← material
    # hls_out[:, 1] unchanged          # L ← weapon

    out_arr: NDArray[np.floating] = base_arr.copy()
    out_arr[:, :, :3] = hls_to_rgb(hls_out).reshape(h, w, 3)   # alpha untouched

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    Image.fromarray((out_arr * 255.0).clip(0, 255).astype(np.uint8)).save(out_path)


def overlay_blend(base_path: str, blend_path: str, out_path: str) -> None:
    """ Write a blended PNG to *out_path* using GIMP's Overlay mode:
      Dark base areas  → Multiply (warm gold tint in shadows)
      Bright base areas → Screen  (gold highlights on bright spots)
      Alpha             → from base (weapon texture), unchanged

    Args:
        base_path  (str): File path to the base weapon texture PNG.
        blend_path (str): File path to the material texture PNG.
        out_path   (str): File path to save the blended PNG output.
    """
    base_img: Image.Image = Image.open(base_path).convert("RGBA")
    blend_img: Image.Image = Image.open(blend_path).convert("RGBA").resize(base_img.size, Image.Resampling.NEAREST)

    base_arr: NDArray[np.floating] = np.array(base_img,  dtype=np.float32) / 255.0   # (H, W, 4)
    blend_arr: NDArray[np.floating] = np.array(blend_img, dtype=np.float32) / 255.0

    b: NDArray[np.floating] = base_arr[:, :, :3]
    bl: NDArray[np.floating] = blend_arr[:, :, :3]

    # Overlay: conditioned on base (b), not blend (bl) — this matches GIMP's Overlay
    overlay: NDArray[np.floating] = np.where(
        b <= 0.5,
        2.0 * b * bl,                           # multiply: dark base areas get gold tint
        1.0 - 2.0 * (1.0 - b) * (1.0 - bl)     # screen: bright base areas get gold highlights
    )

    out_arr: NDArray[np.floating] = base_arr.copy()
    out_arr[:, :, :3] = np.clip(overlay, 0.0, 1.0)   # alpha untouched

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    Image.fromarray((out_arr * 255.0).clip(0, 255).astype(np.uint8)).save(out_path)


def hard_light_blend(base_path: str, blend_path: str, out_path: str) -> None:
    """ Write a blended PNG to *out_path* using GIMP's Hard Light mode:
      Hard contrast effects — ideal for metallic textures like black metal.
      Alpha → from base (weapon texture), unchanged

    Args:
        base_path  (str): File path to the base weapon texture PNG.
        blend_path (str): File path to the material texture PNG.
        out_path   (str): File path to save the blended PNG output.
    """
    blend_img: Image.Image = Image.open(blend_path).convert("RGBA")#.resize(base_img.size, Image.Resampling.NEAREST)
    base_img: Image.Image = Image.open(base_path).convert("RGBA").resize(blend_img.size, Image.Resampling.NEAREST)

    base_arr: NDArray[np.floating] = np.array(base_img,  dtype=np.float32) / 255.0   # (H, W, 4)
    blend_arr: NDArray[np.floating] = np.array(blend_img, dtype=np.float32) / 255.0

    b: NDArray[np.floating] = base_arr[:, :, :3]
    bl: NDArray[np.floating] = blend_arr[:, :, :3]

    # Hard Light (GIMP formula)
    hard_light: NDArray[np.floating] = np.where(
        bl <= 0.5,
        b - (1.0 - 2.0 * bl) * b * (1.0 - b),
        b + (2.0 * bl - 1.0) * (np.where(b <= 0.25, ((16.0 * b - 12.0) * b + 4.0) * b, np.sqrt(b)) - b)
    )

    out_arr: NDArray[np.floating] = base_arr.copy()
    out_arr[:, :, :3] = np.clip(hard_light, 0.0, 1.0)   # alpha untouched

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    Image.fromarray((out_arr * 255.0).clip(0, 255).astype(np.uint8)).save(out_path)


BlendFunc = Callable[[str, str, str], None]

# Maps each material name to its blend function.
# To add a new material, just add an entry here — no other changes needed.
MATERIALS: dict[str, BlendFunc] = {
    "gold":                 overlay_blend,
    "autumn":               overlay_blend,
    "galaxy":               hsl_color_blend,
    "red_polymer_stripes":  hsl_color_blend,
}
SCOPE_OVERLAYS: tuple[str, ...] = ("acogdetails", "holodetails", "kobradetails", "reticles")


def blend_texture(weapon_texture_path: str, material_texture_path: str, out_path: str, material: str) -> None:
    """ Blend with cache — skips redundant work when variants share a base texture. """
    if os.path.exists(out_path):
        return
    MATERIALS[material](weapon_texture_path, material_texture_path, out_path)


# Main function
@stp.measure_time(message="Generated camo variants")
def main() -> None:
    ns: str = Mem.ctx.project_id
    textures_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")

    # For each weapon, make variants with only one material (e.g. wood, metal, gold, etc.)
    weapons: list[Item] = [
        Item.from_id(item)
        for item in Mem.definitions.keys()
        if Item.from_id(item).components.get("custom_data", {}).get(ns, {}).get("gun")
    ]
    for material in MATERIALS:
        material_texture_path: str = f"{textures_folder}/{material}.png"

        for weapon in weapons:
            item_id: str = (
                f"{weapon.id}_{material}"
                if not weapon.id.endswith("_zoom")
                else f"{weapon.id[:-5]}_{material}_zoom"
            )
            item: Item = Item(
                id=item_id, base_item=weapon.base_item, components=deepcopy(weapon.components), override_model=weapon.override_model
            )

            # Define normal and zoom models
            gun_stats: JsonDict = item.components["custom_data"].get(ns, {}).get("stats", {})
            normal_model: str = f"{ns}:{item_id.replace('_zoom', '')}"
            zoom_model: str = normal_model + "_zoom"
            gun_stats[MODELS] = {"normal": normal_model, "zoom": zoom_model}

            # Merge textures in override model using HSL Color mode
            if item.override_model:
                item.override_model = item.override_model.copy()
                item.override_model["textures"] = item.override_model.get("textures", {}).copy()
                for key, texture in item.override_model["textures"].items():
                    if any(x in texture for x in SCOPE_OVERLAYS):
                        continue

                    # Resolve weapon texture PNG from its namespaced path (e.g. "mgs:item/ak47")
                    texture_file: str = texture.split("/")[-1]
                    if texture_file == material:
                        continue  # Some models reuse the material texture directly as their override texture — skip blending in this case
                    weapon_texture_path: str = f"{textures_folder}/{texture_file}.png"

                    blended_name: str = f"{texture_file}_{material}"
                    blended_out_path: str = f"{textures_folder}/blended_camo/{blended_name}.png"

                    blend_texture(weapon_texture_path, material_texture_path, blended_out_path, material)

                    item.override_model["textures"][key] = f"{ns}:item/{blended_name}"

