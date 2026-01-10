
import os
import re
import sqlite3
from typing import List, Tuple

import numpy as np
from osgeo import gdal

from db.db import insert_chart_with_points


# -------------------------
# File / header parsing
# -------------------------
def read_kap_header_lines(path: str) -> List[str]:
    """
    Read the header lines from a .kap file.

    Strategy:
    - Read file in binary mode line-by-line.
    - Try to decode each line with latin-1 (preserves bytes).
    - Stop when we detect a binary/EOF marker (0x1A), or when a decode fails,
      or when a line contains a NUL byte.
    - Return decoded, stripped lines (no trailing newline).
    """
    header_lines = []
    with open(path, "rb") as f:
        for raw in f:
            # If file contains DOS EOF marker 0x1A, stop
            if b"\x1A" in raw:
                # include portion before 0x1A if any printable characters exist
                try:
                    part = raw.split(b"\x1A", 1)[0].decode("latin-1").rstrip("\r\n")
                except Exception:
                    part = ""
                if part:
                    header_lines.append(part)
                break

            # stop if raw contains embedded NUL which indicates binary data
            if b"\x00" in raw:
                break

            try:
                line = raw.decode("latin-1").rstrip("\r\n")
            except UnicodeDecodeError:
                break

            # Some files may include blank lines within header; keep them.
            # Stop if we encounter a line of mostly-control characters
            if not line:
                # Accept a single blank line, but if it's repeated or followed by binary it's ok to stop.
                # We'll append blank lines (safe).
                header_lines.append(line)
                continue

            # If the line contains many low-codepoint characters, treat as end
            low_control = sum(1 for c in line if ord(c) < 9)
            if low_control > 0:
                break

            header_lines.append(line)

    # Strip common leading/trailing whitespace from lines
    return [ln.strip() for ln in header_lines if ln is not None]


# -------------------------
# Parsers for REF and PLY
# -------------------------
def parse_ref_points(header_lines: List[str]) -> List[Tuple[int, float, float, float, float]]:
    """
    Parse REF lines.

    Returns list of tuples:
      (ref_index, pixel_x, pixel_y, latitude, longitude)

    Accepts line forms like:
      REF/1,0,0,57.392429795,18.154330972
      or with leading '!' (e.g. '!REF/1,...')
    """
    ret = []
    for ln in header_lines:
        l = ln.lstrip("!").strip()
        if not l.upper().startswith("REF/"):
            continue
        # Remove initial 'REF/' then split by comma
        try:
            body = l.split("/", 1)[1]
        except IndexError:
            continue
        parts = [p.strip() for p in body.split(",")]
        # expected at least 5 parts: index, pixel_x, pixel_y, lat, lon
        if len(parts) >= 5:
            try:
                idx = int(parts[0])
                px = float(parts[1])
                py = float(parts[2])
                lat = float(parts[3])
                lon = float(parts[4])
                ret.append((idx, px, py, lat, lon))
            except ValueError:
                # skip malformed REF
                continue
    return ret


def parse_ply_points(header_lines: List[str]) -> List[Tuple[int, float, float]]:
    """
    Parse PLY lines.

    Returns list of tuples:
      (ply_index, latitude, longitude)

    Accepts lines like:
      PLY/1,57.391627540,18.155924546
      or '!PLY/1,...'
    """
    ret = []
    for ln in header_lines:
        l = ln.lstrip("!").strip()
        if not l.upper().startswith("PLY/"):
            continue
        try:
            body = l.split("/", 1)[1]
        except IndexError:
            continue
        parts = [p.strip() for p in body.split(",")]
        if len(parts) >= 3:
            try:
                idx = int(parts[0])
                lat = float(parts[1])
                lon = float(parts[2])
                ret.append((idx, lat, lon))
            except ValueError:
                continue
    return ret


# -------------------------
# Metadata extraction
# -------------------------
def parse_metadata(header_lines: List[str]) -> dict:
    """
    Extract common metadata from header lines:
    - RA=<width>,<height>  (image pixel size)
    - DX=<dx>,DY=<dy> or DX=<dx> , DY=<dy> sometimes as 'DX=1.06,DY=1.06'
    Returns dict with possible keys: width, height, dx, dy
    """
    text = "\n".join(header_lines)
    meta = {}

    # RA=2544,1541  or RA= 2544,1541
    m = re.search(r"\bRA\s*=\s*([0-9]+)\s*,\s*([0-9]+)\b", text, flags=re.IGNORECASE)
    if m:
        meta["width"] = int(m.group(1))
        meta["height"] = int(m.group(2))
    else:
        # some files use RA=<w>,<h> without spaces and on same line with NU= etc
        m2 = re.search(r"\bRA=([0-9]+),([0-9]+)\b", text, flags=re.IGNORECASE)
        if m2:
            meta["width"] = int(m2.group(1))
            meta["height"] = int(m2.group(2))

    # DX and DY
    m3 = re.search(r"\bDX\s*=\s*([0-9.+-eE]+)\b", text, flags=re.IGNORECASE)
    if m3:
        try:
            meta["dx"] = float(m3.group(1))
        except ValueError:
            pass
    m4 = re.search(r"\bDY\s*=\s*([0-9.+-eE]+)\b", text, flags=re.IGNORECASE)
    if m4:
        try:
            meta["dy"] = float(m4.group(1))
        except ValueError:
            pass

    # Some headers pack 'DX=1.06,DY=1.06' next to each other
    m5 = re.search(r"\bDX=([0-9.+-eE]+)\s*,\s*DY=([0-9.+-eE]+)\b", text, flags=re.IGNORECASE)
    if m5:
        try:
            meta["dx"] = float(m5.group(1))
            meta["dy"] = float(m5.group(2))
        except ValueError:
            pass

    return meta


# -------------------------
# Utilities
# -------------------------
def bounds_from_refs(ref_points: List[Tuple[int, float, float, float, float]]):
    if not ref_points:
        return None, None, None, None
    lats = [r[3] for r in ref_points]
    lons = [r[4] for r in ref_points]
    return min(lats), max(lats), min(lons), max(lons)


# -------------------------
# Main CLI
# -------------------------
def parse_kap_file(kap_path: str):
    if not os.path.isfile(kap_path):
        print(f"File not found: {kap_path}")
        return 2

    filename = os.path.basename(kap_path)

    print(f"Reading KAP file: {kap_path}")
    header_lines = read_kap_header_lines(kap_path)
    print(f"  -> Header lines read: {len(header_lines)}")

    ref_points = parse_ref_points(header_lines)
    ply_points = parse_ply_points(header_lines)
    meta = parse_metadata(header_lines)

    print("Parsed metadata:", meta)
    print(f"Found {len(ref_points)} REF points and {len(ply_points)} PLY points.")

    lat_min, lat_max, lon_min, lon_max = bounds_from_refs(ref_points)
    if lat_min is not None:
        print("REF bounds from control points:")
        print(f"  lat_min: {lat_min}")
        print(f"  lat_max: {lat_max}")
        print(f"  lon_min: {lon_min}")
        print(f"  lon_max: {lon_max}")
    else:
        print("No REF points found to compute bounds.")

    dataset = gdal.Open(kap_path)
    band = dataset.GetRasterBand(1)

    # --- Check if there's a color table (palette) ---
    color_table = band.GetColorTable()

    if color_table:
        # Convert indexed values to RGB
        arr = band.ReadAsArray()
        lut = np.array([color_table.GetColorEntry(i) for i in range(color_table.GetCount())])
        lut = lut[:, :3].astype(np.uint8)
        rgb = lut[arr]
    else:
        # Fallback: raw RGB or grayscale
        arr = dataset.ReadAsArray()
        if arr.ndim == 3:
            rgb = arr.transpose((1, 2, 0))
        else:
            rgb = np.stack([arr] * 3, axis=-1)

    chart_id = insert_chart_with_points( filename, rgb, meta, ref_points, ply_points)


    print(f"Inserted chart '{filename}' as chart_id={chart_id}")


