""" Camo variants: blends each weapon texture into its cosmetic colour schemes. """
# Imports
import os
from collections.abc import Callable
from copy import deepcopy
from dataclasses import astuple, dataclass

import numpy as np
import stouputils as stp
from numpy.typing import NDArray
from PIL import Image
from stewbeet import Item, JsonDict, Mem

from ..config.stats.keys import MODELS
from ..config.stats.weapons.melee import MELEE_WEAPONS

# HSL Color blend (GIMP "HSL Color" mode): H and S from the blend (material) layer, L from the base (weapon); alpha from the base.
# Vectorised with numpy, no per-pixel Python loop.

# Functions
def rgb_to_hls(arr: NDArray[np.floating]) -> NDArray[np.floating]:
	""" (N, 3) floating RGB to (N, 3) floating HLS, in colorsys channel order (H, L, S). """
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
	""" (N, 3) floating HLS to (N, 3) floating RGB. """
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
	hue and saturation from the blend (material texture), lightness and alpha from the base (weapon texture).

	- gamma below 1 brightens midtones (more metallic), above 1 darkens them (more matte).
	- contrast above 1 sharpens metallic highlights, below 1 gives a softer, more plastic look.
	- l_blend above 0 mixes some lightness from the material, for a brighter, more reflective metal.
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

	# Gamma and contrast on the L channel (weapon luminance).
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
	""" GIMP Overlay blend with optional pre-blend contrast and gamma correction.

	- gamma below 1 brightens midtones (more metallic), above 1 darkens them (more matte).
	- contrast above 1 sharpens metallic highlights, below 1 gives a softer, more plastic look.
	"""
	base_img: Image.Image = Image.open(base_path).convert("RGBA")
	blend_img: Image.Image = Image.open(blend_path).convert("RGBA").resize(base_img.size, Image.Resampling.NEAREST)

	base_arr: NDArray[np.floating] = np.array(base_img,  dtype=np.float32) / 255.0
	blend_arr: NDArray[np.floating] = np.array(blend_img, dtype=np.float32) / 255.0

	b: NDArray[np.floating]  = base_arr[:, :, :3]
	bl: NDArray[np.floating] = blend_arr[:, :, :3]

	# Pre-blend: gamma and contrast on the base RGB, alpha untouched.
	b_adjusted: NDArray[np.floating] = np.power(np.clip(b, 1e-6, 1.0), gamma)          # gamma
	b_adjusted = np.clip((b_adjusted - 0.5) * contrast + 0.5, 0.0, 1.0)               # contrast

	# Overlay, conditioned on the adjusted base.
	overlay: NDArray[np.floating] = np.where(
		b_adjusted <= 0.5,
		2.0 * b_adjusted * bl,
		1.0 - 2.0 * (1.0 - b_adjusted) * (1.0 - bl)
	)

	out_arr: NDArray[np.floating] = base_arr.copy()
	out_arr[:, :, :3] = np.clip(overlay, 0.0, 1.0)

	os.makedirs(os.path.dirname(out_path), exist_ok=True)
	Image.fromarray((out_arr * 255.0).clip(0, 255).astype(np.uint8)).save(out_path)

# Constants
BlendFunc = Callable[[str, str, str], None]

# A new material only needs an entry here.
MATERIALS: dict[str, BlendFunc] = {
	"gold":                 lambda b, bl, o: hsl_color_blend(b, bl, o, l_blend=1.0),
	"autumn":               overlay_blend,
	"galaxy":               hsl_color_blend,
	"red_polymer_stripes":  hsl_color_blend,
}
COMMON_IGNORE: tuple[str, ...] = ("acogdetails", "holodetails", "kobradetails", "reticles", "reticles_1024", "element_115")
""" element_115 is an animated strip (8 frames + .mcmeta); blending it would drop the .mcmeta and
render the whole strip squashed onto one face. """

CAMO_MELEE: frozenset[str] = frozenset(melee.item_id for melee in MELEE_WEAPONS if melee.camo_eligible)
""" Melee weapons that get camo variants, on top of every non-tactical gun. """
GOLD_DEFAULT_IGNORE_TEXTURE: tuple[str, ...] = (
	*COMMON_IGNORE,
	"metal", "metal_bright", "metal_brighter", "metal_dark",
	"akdetails", "glock18details", "augdetails", "m82details"
)

@dataclass(frozen=True)
class CamoOverride:
	""" Per-weapon exception to how its camo textures are blended. """
	ignore_textures: tuple[str, ...] | None = None
	""" Texture names left untouched, instead of the material's default list. """
	func: BlendFunc | None = None
	""" Blend function used instead of the material's. """
	apply_to: tuple[str, ...] = ("gold",)
	""" Materials this override applies to. """


OVERRIDES: dict[str, CamoOverride] = {
	"m249": CamoOverride(ignore_textures=("brass", "copper", "metal", "metal_bright", "metal_dark", *COMMON_IGNORE)),
	"m4a1": CamoOverride(ignore_textures=("m4details", "ardetails2", *COMMON_IGNORE)),
	"m16a4": CamoOverride(ignore_textures=("ardetails2", *COMMON_IGNORE)),
	"m24": CamoOverride(ignore_textures=("metal_dark", "m24details", *COMMON_IGNORE)),
	"mac10": CamoOverride(ignore_textures=COMMON_IGNORE),
	"mp5": CamoOverride(ignore_textures=("rubber_cross", *COMMON_IGNORE)),
	"mp7": CamoOverride(ignore_textures=("metal", "mp7details", *COMMON_IGNORE)),
	"ppsh41": CamoOverride(ignore_textures=("ppshdetails", "ppshwood", *COMMON_IGNORE)),
	"spas12": CamoOverride(ignore_textures=("metal", "spas12details", *COMMON_IGNORE)),
	"sten": CamoOverride(ignore_textures=COMMON_IGNORE),
	"m1911": CamoOverride(ignore_textures=COMMON_IGNORE),
	"m9": CamoOverride(ignore_textures=COMMON_IGNORE),
	"deagle": CamoOverride(ignore_textures=("rubber", "deagledetails", *COMMON_IGNORE)),
	"makarov": CamoOverride(ignore_textures=COMMON_IGNORE),
	"glock17": CamoOverride(ignore_textures=("glock17_polymer_dots", *COMMON_IGNORE)),
	"vz61": CamoOverride(ignore_textures=("vz61grip", "vz61wood", *COMMON_IGNORE)),
	"ray_gun": CamoOverride(func=lambda b, bl, o: hsl_color_blend(b, bl, o, l_blend=0.0)),
}

# Gold spares a gun's metal sheets so the receiver stays black, but a melee weapon is its blade: sparing them would leave a gold knife with only a gold grip.
# Driven by CAMO_MELEE, so toggling `camo_eligible` needs no second edit here.
OVERRIDES.update({melee_id: CamoOverride(ignore_textures=COMMON_IGNORE) for melee_id in CAMO_MELEE})

@dataclass(frozen=True)
class BlendJob:
	""" Arguments of one `blend_texture` call. """
	weapon_texture: str
	material_texture: str
	out_path: str
	base_weapon: str
	material: str


def active_override(base_weapon: str, material: str) -> CamoOverride:
	""" The weapon's `OVERRIDES` entry, or an empty one when it has none for this material. """
	override: CamoOverride | None = OVERRIDES.get(base_weapon)
	return override if override and material in override.apply_to else CamoOverride()

def blend_texture(weapon_texture_path: str, material_texture_path: str, out_path: str, base_weapon: str, material: str) -> None:
	""" Blend with cache: skips redundant work when variants share a base texture. """
	if os.path.exists(out_path):
		return
	func: BlendFunc = active_override(base_weapon, material).func or MATERIALS[material]
	func(weapon_texture_path, material_texture_path, out_path)

@stp.measure_time(message="Generated camouflage variants")
def main() -> None:
	ns: str = Mem.ctx.project_id
	textures_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")

	# One variant per weapon and material.
	weapons: list[Item] = [item for item in map(Item.from_id, Mem.definitions) if is_camo_eligible(ns, item)]
	queue: list[BlendJob] = [
		job
		for material in MATERIALS
		for weapon in weapons
		for job in add_camo_variant(ns, textures_folder, weapon, material)
	]

	stp.multiprocessing(blend_texture, [astuple(job) for job in stp.unique_list(queue)], use_starmap=True, desc="Blending camo textures", max_workers=1)

def is_camo_eligible(ns: str, item: Item) -> bool:
	""" Every non-tactical gun, plus the melee weapons flagged `camo_eligible` in MELEE_WEAPONS.

	Tacticals such as monkey_bomb get no camos, and their models use vanilla block textures absent from the folder the blender reads.
	"""
	if item.id in CAMO_MELEE:
		return True
	custom: JsonDict = item.components.get("custom_data", {}).get(ns, {})
	return bool(custom.get("gun")) and not custom.get("tactical")

def add_camo_variant(ns: str, textures_folder: str, weapon: Item, material: str) -> list[BlendJob]:
	""" Register the `material` variant of a weapon, and return the texture blends its model needs. """
	base_id: str = weapon.id.replace("_zoom", "")
	item_id: str = f"{base_id}_{material}_zoom" if weapon.id.endswith("_zoom") else f"{base_id}_{material}"
	item: Item = Item(
		id=item_id, base_item=weapon.base_item, components=deepcopy(weapon.components), override_model=weapon.override_model
	)
	gun_stats: JsonDict = item.components["custom_data"].get(ns, {}).get("stats", {})
	gun_stats[MODELS] = {"normal": f"{ns}:{base_id}_{material}", "zoom": f"{ns}:{base_id}_{material}_zoom"}
	if not item.override_model:
		return []
	item.override_model = item.override_model.copy()

	# Zoom models are `parent:` children of their base with no textures of their own, so the camo points at the camo'd parent.
	parent: str = str(item.override_model.get("parent", ""))
	if parent.startswith(f"{ns}:item/"):
		item.override_model["parent"] = f"{parent}_{material}"
		return []
	jobs: list[BlendJob] = retexture(ns, textures_folder, item.override_model, gun_stats.get("base_weapon", base_id), material)
	item.override_model = {"parent": f"{ns}:item/{weapon.id}", "textures": item.override_model["textures"]}
	return jobs

def retexture(ns: str, textures_folder: str, model: JsonDict, base_weapon: str, material: str) -> list[BlendJob]:
	""" Point a model's textures at their HSL-blended camo versions, and return the blends to produce.

	Args:
		model: The variant's own override model, whose `textures` is replaced by an edited copy.
	"""
	default_ignore: tuple[str, ...] = GOLD_DEFAULT_IGNORE_TEXTURE if material == "gold" else COMMON_IGNORE
	override_ignore: tuple[str, ...] | None = active_override(base_weapon, material).ignore_textures
	ignore_textures: tuple[str, ...] = default_ignore if override_ignore is None else override_ignore
	textures: JsonDict = model.get("textures", {}).copy()
	model["textures"] = textures

	jobs: list[BlendJob] = []
	for key, texture in textures.items():
		# Some models use the material texture directly, which needs no blending.
		texture_file: str = texture.split("/")[-1]
		if texture_file == material or any(texture.endswith(f"/{x}") for x in ignore_textures):
			continue
		blended_name: str = f"{texture_file}_{material}"
		jobs.append(BlendJob(
			weapon_texture=f"{textures_folder}/{texture_file}.png",
			material_texture=f"{textures_folder}/{material}.png",
			out_path=f"{textures_folder}/blended_camo/{blended_name}.png",
			base_weapon=base_weapon,
			material=material,
		))
		textures[key] = f"{ns}:item/{blended_name}"
	return jobs

