""" Aim-down-sights magnification, scope barrel distortion, and the reticle of the sight.

Iron sights and each sight ship an id ramping the effect in and one ramping it out.
A removed chain stops rendering on the frame the packet lands, so it can never animate its own exit.

The zoomed models carry no reticle: a lens that magnifies the frame would magnify a reticle drawn on the model too, and its bobbing with it.
Their reticle faces sample `sight_marker` instead, transparent but for a blue texel and a green one on a diagonal of the marker quad,
inside the opening, where the lens covers them, yet out of the small centre the lens magnifies.
Lighting only scales a colour, so both keep two channels at exactly 0 on screen: two passes reduce each to its centroid,
and the shader draws the reticle, from `textures/effect/reticle/<sight>.png`, in the square they span, with the lens centred on it.
A shader pack (Iris) lights and grades the markers past recognition, so until they are seen the square is the one the aimed model has at rest.
"""
# Imports
from dataclasses import dataclass

from beet import FragmentShader, Texture
from PIL import Image
from stewbeet import JsonDict, Mem, write_load_file, write_versioned_function

from .common import HEADER, SCREENQUAD, timed_effect, uniform

# Constants
IN_TICKS: float = 7.0
""" Ramp into the scope, matching the feel of a 0.12-per-frame lerp at 60 fps. """

OUT_TICKS: float = 4.0
""" Ramp out. Kept short: re-aiming inside this window restarts from zero and visibly snaps. """

DISTORTION: float = 0.55
""" Barrel strength of the lens, unitless. """

LENS_IN_TICKS: list[float] = [5.0, 6.0]
""" The lens appears between these ticks, once the scope model has finished swinging to the centre. """

LENS_OUT_TICKS: list[float] = [0.0, 1.0]
""" Leaving the scope, the lens goes at once, before the model starts swinging away. """


@dataclass(frozen=True)
class ScopeLevel:
	""" How much a sight magnifies. """
	level: int
	magnify: float
	""" How far the UV is pulled toward the centre at full zoom, 0.45 being roughly 1.82x. """
	lens_radius: float
	""" Screen-space radius of the barrel distortion, 0 for sights with no lens.
	Sized to the scope opening once magnified: the held model is in the image and gets pulled too. """


SCOPE_LEVELS: dict[int, ScopeLevel] = {
	2: ScopeLevel(level=2, magnify=0.20, lens_radius=0.00),
	3: ScopeLevel(level=3, magnify=0.20, lens_radius=0.10),
	4: ScopeLevel(level=4, magnify=0.30, lens_radius=0.25),
}
""" Level 2 is the centre-only pull of iron sights and red dots, so it has no lens. """


@dataclass(frozen=True)
class Sight:
	""" A sight whose reticle the zoom draws, recognised by the region of `assets/textures/<source>.png` its models sample. """
	name: str
	source: str
	column: int
	""" Which 4-unit UV region of the top row holds the reticle. """
	level: int
	rest_side: float
	""" Side of the marker quad over the screen height once aimed and still, the median over the guns carrying the sight.
	The aimed models centre it on screen, and the hand camera has a fixed 70 degree FOV, so it holds at any window size. """
	marker_row: int = 0
	""" UV row of the region whose quad carries the markers, 1 when the reticle quad is too small to keep them out of the lens. """
	reticle_scale: float = 1.0
	""" Side of the reticle quad over the side of the marker quad, both quads sharing a centre. """


SIGHTS: list[Sight] = [
	Sight(name="kobra", source="reticles",      column=0, level=2, rest_side=0.0270),
	Sight(name="holo",  source="reticles",      column=1, level=2, rest_side=0.0354),
	Sight(name="acog",  source="reticles",      column=2, level=3, rest_side=0.1599, marker_row=1, reticle_scale=0.2269),
	Sight(name="aug",   source="reticles",      column=3, level=2, rest_side=0.0255),
	Sight(name="mk4",   source="reticles_1024", column=0, level=4, rest_side=0.2789),
	Sight(name="pu",    source="reticles_1024", column=1, level=2, rest_side=0.2457),
	Sight(name="pso",   source="reticles_1024", column=2, level=4, rest_side=0.2611, marker_row=1),
]
""" The PSO marks its second quad, the same square as its reticle's, since its reticle region is the ACOG dot's in the other texture. """

MARKER_TEXELS: int = 16
""" Side of a UV region in the marker texture, a marker being one texel of it. """

MARKER_INSET: int = 3
""" Texels between a corner of the region and its marker: the corners are behind the scope tube. """

CUTOUT_ALPHA: int = 26
""" The item pipeline discards a texel under this alpha, so the reticle textures drop them too. """

LENS_GRID: int = 32
""" Side of the block grid each marker search is reduced through, before its single centroid pixel. """

LENS_CENTRE_CLEAR: int = 0x7F7F7F7F
""" Both markers at the screen centre, as the centroid pass packs them: an empty square, read as markers not seen yet. """

LENS_SEARCH_GLSL: str = f"""
#define GRID {LENS_GRID}

// The markers are looked for in a centred square three quarters of the screen high, cut into GRID x GRID blocks.
int lens_block(ivec2 inSize) {{
    return (inSize.y * 3 / 4 + GRID - 1) / GRID;
}}

ivec2 lens_origin(ivec2 inSize) {{
    return inSize / 2 - GRID / 2 * lens_block(inSize);
}}
"""
""" Shared by the two passes that locate the markers, so they agree on where each block lies. """

LENS_BLOCKS_FSH: str = HEADER + LENS_SEARCH_GLSL + """
uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

// The left GRID columns look for the blue marker, the right ones for the green one.
// rg = mean marker position inside the block, a = share of the block it covers.
void main() {
    ivec2 cell = ivec2(gl_FragCoord.xy);
    int channel = cell.x < GRID ? 2 : 1;
    ivec2 inSize = textureSize(InSampler, 0);
    int block = lens_block(inSize);
    ivec2 start = lens_origin(inSize) + ivec2(cell.x % GRID, cell.y) * block;

    vec2 sum = vec2(0.0);
    float count = 0.0;
    for (int y = 0; y < block; y++) {
        for (int x = 0; x < block; x++) {
            vec3 color = texelFetch(InSampler, start + ivec2(x, y), 0).rgb;
            // The floor keeps the scope's own near-black shading from passing for a marker.
            if (color.r == 0.0 && color[3 - channel] == 0.0 && color[channel] >= 4.0 / 255.0) {
                sum += vec2(x, y) + 0.5;
                count += 1.0;
            }
        }
    }
    fragColor = count > 0.0 ? vec4(sum / (count * float(block)), 0.0, max(count / float(block * block), 1.0 / 255.0)) : vec4(0.0);
}
"""

LENS_CENTRE_FSH: str = HEADER + LENS_SEARCH_GLSL + """
uniform sampler2D BlocksSampler;
uniform sampler2D PreviousSampler;
uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

// Pixel 0 holds the blue marker and pixel 1 the green one, in screen UV, x in rg and y in ba, 16 bits each.
// A frame without the marker (a muzzle flash over it, a dark cave) keeps the last position.
void main() {
    int marker = int(gl_FragCoord.x);
    vec2 sum = vec2(0.0);
    float weight = 0.0;
    for (int y = 0; y < GRID; y++) {
        for (int x = 0; x < GRID; x++) {
            vec4 cell = texelFetch(BlocksSampler, ivec2(x + marker * GRID, y), 0);
            sum += (vec2(x, y) + cell.rg) * cell.a;
            weight += cell.a;
        }
    }
    if (weight == 0.0) {
        fragColor = texelFetch(PreviousSampler, ivec2(marker, 0), 0);
        return;
    }

    ivec2 inSize = textureSize(InSampler, 0);
    vec2 uv = (vec2(lens_origin(inSize)) + sum / weight * float(lens_block(inSize))) / vec2(inSize);
    vec2 high = floor(uv * 255.0) / 255.0;
    vec2 low = fract(uv * 255.0);
    fragColor = vec4(high.x, low.x, high.y, low.y);
}
"""

IRON_FSH: str = HEADER + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform IronConfig {
    vec2 Magnify;    // UV pull toward the centre, at the start and at the end of the ramp
    float Duration;  // ramp length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() {
    float magnify = mix(Magnify.x, Magnify.y, mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration));
    fragColor = texture(InSampler, mix(texCoord, vec2(0.5), magnify));
}
"""
""" Iron sights: the centre-only pull, with no marker to look for. """

SIGHT_FSH: str = HEADER + f"""
#define MARKER_SPAN {(MARKER_TEXELS - 1 - 2 * MARKER_INSET) / MARKER_TEXELS}
#define MARKER_TEXELS {MARKER_TEXELS}.0
""" + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;
uniform sampler2D LensSampler;
uniform sampler2D ReticleSampler;
uniform sampler2D DepthSampler;

layout(std140) uniform SightConfig {
    vec2 Magnify;        // UV pull toward the centre, at the start and at the end of the ramp
    vec2 LensAlpha;      // lens opacity, at the start and at the end of its own window
    vec4 Lens;           // x = scope magnification divisor, y = lens radius (0 disables), z = barrel strength
    vec2 LensTicks;      // the lens cross-fades between these two ticks, apart from the magnification
    float Duration;      // ramp length in ticks
    float ReticleScale;  // side of the reticle over the side of the marker square
    float ReticleAlpha;  // 0 on the way out, where the held model draws its own reticle again
    float RestSide;      // side of the marker square over the screen height, aimed and still
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

vec4 cubic(float v) {
    vec4 n = vec4(1.0, 2.0, 3.0, 4.0) - v;
    vec4 s = n * n * n;
    float x = s.x;
    float y = s.y - 4.0 * s.x;
    float z = s.z - 4.0 * s.y + 6.0 * s.x;
    return vec4(x, y, z, 6.0 - x - y - z) * (1.0 / 6.0);
}

vec4 textureBicubic(sampler2D samp, vec2 texCoords, vec2 texSize) {
    vec2 oneTexel = 1.0 / texSize;
    texCoords = texCoords * texSize - 0.5;
    vec2 fxy = fract(texCoords);
    texCoords -= fxy;

    vec4 xcubic = cubic(fxy.x);
    vec4 ycubic = cubic(fxy.y);

    vec4 c = texCoords.xxyy + vec2(-0.5, 1.5).xyxy;
    vec4 s = vec4(xcubic.xz + xcubic.yw, ycubic.xz + ycubic.yw);
    vec4 offsetbc = (c + vec4(xcubic.yw, ycubic.yw) / s) * oneTexel.xxyy;

    vec4 sample0 = texture(samp, offsetbc.xz);
    vec4 sample1 = texture(samp, offsetbc.yz);
    vec4 sample2 = texture(samp, offsetbc.xw);
    vec4 sample3 = texture(samp, offsetbc.yw);

    float sx = s.x / (s.x + s.y);
    float sy = s.z / (s.z + s.w);
    return mix(mix(sample3, sample2, sx), mix(sample1, sample0, sx), sy);
}

bool is_marker(vec3 color) {
    return color.r == 0.0 && (color.g == 0.0) != (color.b == 0.0) && max(color.g, color.b) >= 4.0 / 255.0;
}

vec2 unpack_marker(int marker) {
    vec4 packed = texelFetch(LensSampler, ivec2(marker, 0), 0);
    return packed.rb + packed.ga / 255.0;
}

// Premultiplied 3 x 3 average over the footprint of one screen pixel: the reticle is drawn several times smaller than its texture.
vec4 reticle_at(vec2 uv, vec2 footprint) {
    vec4 sum = vec4(0.0);
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            vec4 texel = texture(ReticleSampler, uv + vec2(x, y) * footprint / 3.0);
            sum += vec4(texel.rgb * texel.a, texel.a);
        }
    }
    return sum.a > 0.0 ? vec4(sum.rgb / sum.a, sum.a / 9.0) : vec4(0.0);
}

void main() {
    vec4 clock = texture(ClockSampler, vec2(0.5));
    float magnify = mix(Magnify.x, Magnify.y, mgs_ramp(clock, GameTime, Duration));
    float lensAlpha = mix(LensAlpha.x, LensAlpha.y, smoothstep(LensTicks.x, LensTicks.y, mgs_elapsed(clock, GameTime)));

    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec2 source = mix(texCoord, vec2(0.5), magnify);

    // The marker square in pixels of the unmagnified frame, signed to run from the blue texel to the green one.
    vec2 blue = unpack_marker(0) * inSize;
    vec2 green = unpack_marker(1) * inSize;
    vec2 square = (green - blue) / MARKER_SPAN;
    bool unseen = abs(square.x) < 2.0 || abs(square.y) < 2.0;
    if (unseen) {
        // The blue texel is the top-left one, and screen y runs upwards.
        square = vec2(1.0, -1.0) * RestSide * inSize.y;
        blue = (inSize - square * MARKER_SPAN) * 0.5;
        green = inSize - blue;
    }
    vec2 centre = (blue + green) * 0.5;

    // A marker shows wherever no lens covers it, so the pixels beside it stand in.
    fragColor = texture(InSampler, source);
    vec2 directions[4] = vec2[](vec2(1.0, 0.0), vec2(-1.0, 0.0), vec2(0.0, 1.0), vec2(0.0, -1.0));
    for (int i = 0; i < 4 && is_marker(fragColor.rgb); i++) {
        fragColor = texture(InSampler, source + directions[i] * 8.0 / inSize);
    }
    // Unseen markers cannot be told by colour, so the pixels toward the centre stand in around where they should be.
    vec2 marker = distance(source * inSize, blue) < distance(source * inSize, green) ? blue : green;
    vec2 gap = abs(source * inSize - marker);
    float reach = abs(square.y) / MARKER_TEXELS + 2.0;
    if (unseen && lensAlpha * ReticleAlpha > 0.0 && max(gap.x, gap.y) < reach) {
        fragColor = texture(InSampler, source + vec2(sign(centre.x - marker.x) * 2.0 * reach, 0.0) / inSize);
    }

    float aspectRatio = inSize.x / inSize.y;
    // The markers were found in the unmagnified frame: this is where the pull above puts their centre on screen.
    vec2 lensCentre = (centre / inSize - 0.5 * magnify) / (1.0 - magnify);
    vec2 screenCoord = (texCoord - lensCentre) * vec2(aspectRatio, 1.0);
    bool inLens = Lens.y > 0.0 && lensAlpha > 0.0 && length(screenCoord) < Lens.y;
    if (inLens) {
        // Always at full strength and faded as a whole: a weak barrel would squash the lens into one pixel.
        float d = length(screenCoord * Lens.z / Lens.y);
        float r = atan(d, sqrt(1.0 - d * d)) / 3.1415926535;
        float theta = atan(screenCoord.y, screenCoord.x);
        vec2 lensCoord = vec2(cos(theta), sin(theta)) * r / Lens.x;
        vec2 pixCoord = mix(lensCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5), vec2(0.5), magnify);
        fragColor = mix(fragColor, textureBicubic(InSampler, pixCoord, inSize), lensAlpha);
    }

    // Outside the lens the sight's body hides the reticle as it hid the reticle quad: the held item is the only depth at exactly 1.0.
    vec2 reticleSize = square * ReticleScale;
    vec2 uv = (source * inSize - centre) / reticleSize + 0.5;
    bool hidden = !inLens && texelFetch(DepthSampler, ivec2(source * inSize), 0).r == 1.0;
    if (hidden || any(lessThan(uv, vec2(0.0))) || any(greaterThan(uv, vec2(1.0)))) return;
    vec4 reticle = reticle_at(uv, (1.0 - magnify) / reticleSize);
    // The rest square is only right once the model has swung in, which is when the lens appears.
    fragColor.rgb = mix(fragColor.rgb, reticle.rgb, reticle.a * ReticleAlpha * (unseen ? lensAlpha : 1.0));
}
"""


# Functions
def main() -> None:
	""" Register the zoom ids of iron sights and of every sight, their shaders and textures, and the aim-down-sights wiring. """
	ns: str = Mem.ctx.project_id
	Mem.ctx.assets[ns].fragment_shaders["post/zoom"] = FragmentShader(IRON_FSH)
	Mem.ctx.assets[ns].fragment_shaders["post/sight"] = FragmentShader(SIGHT_FSH)
	Mem.ctx.assets[ns].fragment_shaders["post/lens_blocks"] = FragmentShader(LENS_BLOCKS_FSH)
	Mem.ctx.assets[ns].fragment_shaders["post/lens_centre"] = FragmentShader(LENS_CENTRE_FSH)
	Mem.ctx.assets[ns].textures["item/sight_marker"] = Texture(marker_texture())

	for fading_out in (False, True):
		register_iron(ns, fading_out)
		for sight in SIGHTS:
			register_sight(ns, sight, fading_out)
	write_functions(ns, mark_zoomed_models(ns))


def marker_texture() -> Image.Image:
	""" A blue texel toward the top-left corner and a green one toward the bottom-right corner of every region a sight marks. """
	image: Image.Image = Image.new("RGBA", (4 * MARKER_TEXELS, 4 * MARKER_TEXELS))
	for sight in SIGHTS:
		left, top = sight.column * MARKER_TEXELS + MARKER_INSET, sight.marker_row * MARKER_TEXELS + MARKER_INSET
		far: int = MARKER_TEXELS - 1 - 2 * MARKER_INSET
		image.putpixel((left, top), (0, 0, 48, 255))
		image.putpixel((left + far, top + far), (0, 48, 0, 255))
	return image


def mark_zoomed_models(ns: str) -> dict[str, int]:
	""" Point the reticle faces of every zoomed model at the marker texture.

	Returns:
		The 1-based index in `SIGHTS` of the sight each zoomed model shows, by item model id.
	"""
	sight_of: dict[str, int] = {}
	for path, model in Mem.ctx.assets[ns].models.items():
		if not path.endswith("_zoom"):
			continue

		index, reticle_keys = find_sight(ns, model.data)
		if not index:
			continue

		model.data["textures"] = {**(model.data.get("textures") or {}), **dict.fromkeys(sorted(reticle_keys),f"{ns}:item/sight_marker")}
		sight_of[f"{ns}:{path.removeprefix('item/')}"] = index
	return sight_of


def find_sight(ns: str, data: JsonDict) -> tuple[int, set[str]]:
	""" The 1-based index in `SIGHTS` of the sight a model shows, 0 for none, and the texture variables its reticle faces read. """
	textures, elements = resolve_model(ns, data)
	reticle_keys: set[str] = {key for key, value in textures.items() if key != "particle" and value.removeprefix(f"{ns}:item/") in ("reticles", "reticles_1024")}
	regions: set[tuple[str, int, int]] = {
		(textures[face["texture"][1:]].removeprefix(f"{ns}:item/"), int(face["uv"][0]) // 4, int(face["uv"][1]) // 4)
		for element in elements for face in element["faces"].values() if face["texture"][1:] in reticle_keys
	}
	return next((i for i, sight in enumerate(SIGHTS, start=1) if (sight.source, sight.column, 0) in regions), 0), reticle_keys


def resolve_model(ns: str, data: JsonDict) -> tuple[dict[str, str], list[JsonDict]]:
	""" The textures a model ends up with once its parents in this namespace are merged, and the elements it inherits. """
	chain: list[JsonDict] = [data]
	while (parent := str(chain[-1].get("parent", ""))).startswith(f"{ns}:item/"):
		chain.append(Mem.ctx.assets[ns].models[parent.removeprefix(f"{ns}:")].data)
	layers: list[dict[str, str]] = [link.get("textures") or {} for link in reversed(chain)]
	return {key: value for layer in layers for key, value in layer.items()}, next(link["elements"] for link in chain if "elements" in link)


def register_iron(ns: str, fading_out: bool) -> None:
	""" Register one direction of the iron sights zoom, the ramp running forwards or in reverse. """
	magnify: float = SCOPE_LEVELS[2].magnify
	timed_effect(
		ns,
		f"zoom_iron{'_out' if fading_out else ''}",
		f"{ns}:post/zoom",
		{"IronConfig": [
			uniform("Magnify", "vec2", [magnify, 0.0] if fading_out else [0.0, magnify]),
			uniform("Duration", "float", OUT_TICKS if fading_out else IN_TICKS),
		]},
	)


def register_sight(ns: str, sight: Sight, fading_out: bool) -> None:
	""" Register one direction of one sight's zoom, with the passes locating its markers and the texture of its reticle. """
	scope: ScopeLevel = SCOPE_LEVELS[sight.level]
	textures_folder: str = Mem.ctx.meta["stewbeet"]["textures_folder"]
	reticle: Image.Image = Image.open(f"{textures_folder}/{sight.source}.png").convert("RGBA")
	side: int = reticle.width // 4
	reticle = reticle.crop((sight.column * side, 0, (sight.column + 1) * side, side))
	reticle.putalpha(reticle.getchannel("A").point([alpha if alpha >= CUTOUT_ALPHA else 0 for alpha in range(256)]))
	Mem.ctx.assets[ns].textures[f"effect/reticle/{sight.name}"] = Texture(reticle)

	timed_effect(
		ns,
		f"zoom_{sight.name}{'_out' if fading_out else ''}",
		f"{ns}:post/sight",
		{"SightConfig": [
			uniform("Magnify", "vec2", [scope.magnify, 0.0] if fading_out else [0.0, scope.magnify]),
			uniform("LensAlpha", "vec2", [1.0, 0.0] if fading_out else [0.0, 1.0]),
			uniform("Lens", "vec4", [float(scope.level), scope.lens_radius, DISTORTION, 0.0]),
			uniform("LensTicks", "vec2", LENS_OUT_TICKS if fading_out else LENS_IN_TICKS),
			uniform("Duration", "float", OUT_TICKS if fading_out else IN_TICKS),
			uniform("ReticleScale", "float", sight.reticle_scale),
			uniform("ReticleAlpha", "float", 0.0 if fading_out else 1.0),
			uniform("RestSide", "float", sight.rest_side),
		]},
		inputs=[
			{"sampler_name": "Lens", "target": "lens_next"},
			{"sampler_name": "Reticle", "location": f"{ns}:reticle/{sight.name}", "width": side, "height": side, "bilinear": True},
			{"sampler_name": "Depth", "target": "minecraft:main", "use_depth_buffer": True},
		],
		pre_passes=[
			{
				"vertex_shader": SCREENQUAD,
				"fragment_shader": f"{ns}:post/lens_blocks",
				"inputs": [{"sampler_name": "In", "target": "minecraft:main"}],
				"output": "lens_blocks",
			},
			{
				"vertex_shader": SCREENQUAD,
				"fragment_shader": f"{ns}:post/lens_centre",
				"inputs": [
					{"sampler_name": "Blocks", "target": "lens_blocks"},
					{"sampler_name": "Previous", "target": "lens"},
					{"sampler_name": "In", "target": "minecraft:main"},
				],
				"output": "lens_next",
			},
			{
				"vertex_shader": SCREENQUAD,
				"fragment_shader": f"{ns}:post/copy",
				"inputs": [{"sampler_name": "In", "target": "lens_next"}],
				"output": "lens",
			},
		],
		targets={
			"lens_blocks": {"width": 2 * LENS_GRID, "height": LENS_GRID},
			"lens":        {"width": 2, "height": 1, "persistent": True, "clear_color": LENS_CENTRE_CLEAR},
			"lens_next":   {"width": 2, "height": 1},
		},
	)


def write_functions(ns: str, sight_of: dict[str, int]) -> None:
	""" Swap ids on the aim-down-sights edges and retire the fade-out once it has played.

	The `zoom_fx` score names the applied id, 1 for iron sights and 1 + the 1-based index in `SIGHTS` for a sight, negated while it fades out.
	"""
	version: str = Mem.ctx.project_version
	ids: dict[int, str] = {1: "zoom_iron", **{score: f"zoom_{sight.name}" for score, sight in enumerate(SIGHTS, start=2)}}

	sights: str = ",".join(f'"{model}":{index}' for model, index in sight_of.items())
	write_load_file(f"data modify storage {ns}:data zoom_sights set value {{{sights}}}\n")

	# The sight is read off the zoomed model, which every gun already carries, camo included.
	swap_in: str = "\n".join(
		f"execute if score #zoom_sight {ns}.data matches {score - 1} run function {ns}:v{version}/zoom/fx_enter_{effect_id}"
		for score, effect_id in ids.items()
	)
	write_versioned_function("zoom/fx_enter", f"""
# @s = a player who just entered aim-down-sights
scoreboard players set #zoom_sight {ns}.data 0
function {ns}:v{version}/zoom/fx_sight with storage {ns}:gun all.stats.models
function {ns}:v{version}/zoom/fx_clear
{swap_in}
""")
	write_versioned_function("zoom/fx_sight", f"""
$execute store result score #zoom_sight {ns}.data run data get storage {ns}:data zoom_sights."$(zoom)"
""")

	# Aiming again mid-fade removes the fade-out instead of handing it a successor, so the two directions never stack.
	# The new ramp restarts from zero, which shows if you tap fast.
	clear: str = "\n".join(
		f"""execute if score @s {ns}.zoom_fx matches {score} run posteffect remove @s {ns}:{effect_id}
execute if score @s {ns}.zoom_fx matches -{score} run posteffect remove @s {ns}:{effect_id}_out"""
		for score, effect_id in ids.items()
	)
	write_versioned_function("zoom/fx_clear", f"""
{clear}
scoreboard players set @s {ns}.zoom_fx 0
scoreboard players reset @s {ns}.zoom_fx_off
""")

	for score, effect_id in ids.items():
		write_versioned_function(f"zoom/fx_enter_{effect_id}", f"""
posteffect add @s {ns}:{effect_id}
scoreboard players set @s {ns}.zoom_fx {score}
scoreboard players reset @s {ns}.zoom_fx_off
""")

	leave: str = "\n".join(
		f"""execute if score @s {ns}.zoom_fx matches {score} run posteffect remove @s {ns}:{effect_id}
execute if score @s {ns}.zoom_fx matches {score} run posteffect add @s {ns}:{effect_id}_out
execute if score @s {ns}.zoom_fx matches {score} run scoreboard players set @s {ns}.zoom_fx -{score}"""
		for score, effect_id in ids.items()
	)
	write_versioned_function("zoom/fx_leave", f"""
# Hand the ramp over to the matching fade-out id, which plays itself out and is retired by fx_tick
execute unless score @s {ns}.zoom_fx matches 1.. run return 0
{leave}
scoreboard players set @s {ns}.zoom_fx_off {int(OUT_TICKS) + 1}
""")

	# Same id removed and re-added in one tick: the client keeps the chain and its clock, only the order changes.
	to_back: str = "\n".join(
		f"""execute if score @s {ns}.zoom_fx matches {sign}{score} run posteffect remove @s {ns}:{effect_id}{suffix}
execute if score @s {ns}.zoom_fx matches {sign}{score} run posteffect add @s {ns}:{effect_id}{suffix}"""
		for score, effect_id in ids.items() for sign, suffix in (("", ""), ("-", "_out"))
	)
	write_versioned_function("zoom/fx_to_back", f"""
# Post effects run in list order. The flash lights the scene from the unmagnified depth buffer,
# so it has to run before the zoom, or its lighting lands on the wrong blocks once magnified.
{to_back}
""")

	expire: str = "\n".join(
		f"execute if score @s {ns}.zoom_fx matches -{score} run posteffect remove @s {ns}:{effect_id}_out"
		for score, effect_id in ids.items()
	)
	write_versioned_function("zoom/fx_tick", f"""
# @s = a player whose fade-out is still applied
scoreboard players remove @s {ns}.zoom_fx_off 1
execute if score @s {ns}.zoom_fx_off matches 1.. run return 0
{expire}
scoreboard players set @s {ns}.zoom_fx 0
scoreboard players reset @s {ns}.zoom_fx_off
""")

