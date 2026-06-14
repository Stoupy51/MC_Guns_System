#!/usr/bin/env python3
"""
Pack-a-Punch (PaP) Fire Sound Generator for StoupGun
=====================================================
Generates PaP versions of weapon fire sounds by layering
a synthesized descending sine sweep ("pew") over the gun shot.

Usage:
  python generate_pap_sounds.py [path/to/assets/sounds] [--dry-run]
  Defaults to "assets/sounds" next to this script.

Output:
  Each weapon folder gets a  pap/  subfolder with processed fire*.ogg files.

Requirements:
  pip install pydub numpy scipy
  ffmpeg must be installed and on your PATH
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import stouputils as stp
from pydub import AudioSegment
from scipy.io import wavfile

# -----------------------------------------------------------------
#  TUNING  -- adjust to taste
# -----------------------------------------------------------------
PITCH_SEMITONES    = +2       # slight pitch up on the gun itself
SWEEP_START_FREQ   = 3000     # Hz -- how high the "pew" starts
SWEEP_END_FREQ     = 300      # Hz -- how low it bottoms out
SWEEP_DURATION_MS  = 350      # ms -- length of the laser sweep
SWEEP_VOLUME_DB    = -6       # dB -- how loud the pew is vs the gun
TARGET_PEAK_DBFS   = -10      # final normalisation target
# -----------------------------------------------------------------

SAMPLE_RATE   = 44100
FIRE_PATTERNS = ("fire.ogg", "fire0.ogg", "fire1.ogg", "fire_alt.ogg")
PAP_FOLDER    = "pap"


def generate_pew_sweep():
    """Synthesize a descending sine sweep -- the classic laser 'pew'."""
    n = int(SAMPLE_RATE * SWEEP_DURATION_MS / 1000)
    t = np.linspace(0, SWEEP_DURATION_MS / 1000, n)

    # Exponential frequency descent (sounds more natural than linear)
    freqs = np.exp(np.linspace(np.log(SWEEP_START_FREQ), np.log(SWEEP_END_FREQ), n))
    phase = 2 * np.pi * np.cumsum(freqs) / SAMPLE_RATE
    sine  = np.sin(phase)

    # Fast attack (5ms), exponential decay
    attack = int(0.005 * SAMPLE_RATE)
    envelope = np.exp(-t * 7)
    envelope[:attack] = np.linspace(0, 1, attack)
    sine *= envelope

    amplitude = 10 ** (SWEEP_VOLUME_DB / 20)
    samples   = (sine * amplitude * 32767).astype(np.int16)

    tmp = tempfile.mktemp(suffix=".wav")
    wavfile.write(tmp, SAMPLE_RATE, samples)
    seg = AudioSegment.from_wav(tmp)
    os.unlink(tmp)
    return seg


def pitch_shift(audio: AudioSegment, semitones: float) -> AudioSegment:
    factor   = 2 ** (semitones / 12)
    new_rate = int(audio.frame_rate * factor)
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
        src = f.name
    dst = src.replace(".ogg", "_p.ogg")
    try:
        audio.export(src, format="ogg")
        subprocess.run(
            ["ffmpeg", "-y", "-i", src, "-af",
             f"asetrate={new_rate},aresample={SAMPLE_RATE}", dst],
            capture_output=True
        )
        return AudioSegment.from_ogg(dst)
    finally:
        for p in (src, dst):
            try: os.unlink(p)
            except FileNotFoundError: pass


def apply_pap_processing(audio: AudioSegment) -> AudioSegment:
    # Pad short audio so the pew sweep is never cut off (pitch-shift shortens audio slightly)
    if len(audio) < SWEEP_DURATION_MS:
        audio = audio + AudioSegment.silent(SWEEP_DURATION_MS - len(audio))

    # 1 -- Slight pitch up so the gun itself sits higher
    gun = pitch_shift(audio, PITCH_SEMITONES)
    gun = gun - 8   # Reduce gun volume by 8dB so the pew is louder

    # 2 -- Synthesize the "pew" laser sweep
    pew = generate_pew_sweep()

    # 3 -- Layer pew on top of gun
    total = max(len(gun), len(pew))
    if len(gun) < total: gun = gun + AudioSegment.silent(total - len(gun))
    if len(pew) < total: pew = pew + AudioSegment.silent(total - len(pew))
    result = gun.overlay(pew)

    # 4 -- Normalize
    if result.dBFS > -80:
        result = result + (TARGET_PEAK_DBFS - result.dBFS)

    return result


def process_weapon_folder(weapon_dir: Path, dry_run: bool = False) -> int:
    found = [weapon_dir / p for p in FIRE_PATTERNS if (weapon_dir / p).exists()]
    if not found:
        return 0

    count = 0
    for src_path in found:
        dst_path = weapon_dir / f"{PAP_FOLDER}_{src_path.name}"
        if dry_run:
            print(f"  [dry-run] would create: {dst_path}")
            count += 1
            continue

        print(f"  Processing {src_path.name} -> {PAP_FOLDER}_{src_path.name}")
        try:
            audio  = AudioSegment.from_ogg(str(src_path))
            result = apply_pap_processing(audio)
            result.export(str(dst_path), format="ogg")
            count += 1
        except Exception as exc:
            print(f"    ERROR: {exc}")

    return count


def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        sounds_root = Path(sys.argv[1])
    else:
        sounds_root = Path(stp.get_root_path(__file__)) / "sounds"

    dry_run = "--dry-run" in sys.argv

    if not sounds_root.exists():
        print(f"ERROR: sounds root not found: {sounds_root}")
        print("Usage: python generate_pap_sounds.py [path/to/assets/sounds] [--dry-run]")
        sys.exit(1)

    if shutil.which("ffmpeg") is None:
        print("ERROR: ffmpeg not found on PATH. Please install ffmpeg.")
        sys.exit(1)

    print(f"\n{'DRY RUN -- ' if dry_run else ''}Pack-a-Punch Sound Generator")
    print(f"Root: {sounds_root.resolve()}\n")

    total_weapons = total_sounds = 0

    for weapon_dir in sorted(d for d in sounds_root.iterdir() if d.is_dir() and d.name != PAP_FOLDER):
        count = process_weapon_folder(weapon_dir, dry_run=dry_run)
        if count:
            total_weapons += 1
            total_sounds  += count
            print(f"  + {weapon_dir.name}: {count} file(s)\n")
        else:
            print(f"  - {weapon_dir.name}: no fire sounds found, skipped\n")

    print("-" * 50)
    print(f"Done! Processed {total_sounds} sound(s) across {total_weapons} weapon(s).")
    if not dry_run:
        print(f"PaP files are saved as '{PAP_FOLDER}_{{filename}}.ogg' in each weapon folder.")


if __name__ == "__main__":
    main()

