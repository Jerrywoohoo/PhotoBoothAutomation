"""
printer_service.py
Handles detection, configuration, queue management, and lossless printing to
Canon SELPHY CP1500 via CUPS (lp).
"""

import subprocess
import shutil
import os
import sys
from PIL import Image

PRINTER_NAME = "Canon_SELPHY_CP1500"
POSTCARD_RATIO = 148.0 / 100.0  # 1.48 (Hagaki / 100x148 mm)


def check_printer_status(printer_name=PRINTER_NAME):
    """
    Returns (status_code, status_message) for the given printer.
    status_code: 'ready', 'offline', 'printing', 'not_found'
    """
    try:
        res = subprocess.run(
            ["lpstat", "-p", printer_name],
            capture_output=True,
            text=True,
            timeout=3
        )
        if res.returncode != 0:
            return "not_found", f"Printer '{printer_name}' not found in CUPS."
        
        output = res.stdout.strip()
        if "idle" in output.lower():
            # Check if it has offline reports
            opt_res = subprocess.run(
                ["lpoptions", "-p", printer_name],
                capture_output=True,
                text=True,
                timeout=3
            )
            if "offline-report" in opt_res.stdout:
                return "offline", "Canon SELPHY is currently powered off or disconnected."
            return "ready", "Canon SELPHY CP1500 is ready and idle."
        elif "printing" in output.lower():
            return "printing", "Canon SELPHY is currently printing."
        else:
            return "ready", output
    except Exception as e:
        return "error", str(e)


def get_print_queue_status(printer_name=PRINTER_NAME):
    """Returns the text output of the current print queue for printer."""
    try:
        res = subprocess.run(["lpq", "-P", printer_name], capture_output=True, text=True, timeout=3)
        return res.stdout.strip() or "Queue is empty."
    except Exception as e:
        return f"Error querying queue: {e}"


def open_mac_print_queue():
    """Opens macOS native Print Center or printer settings."""
    try:
        subprocess.run(["open", "-b", "com.apple.printcenter"], timeout=3)
        return True
    except Exception:
        try:
            subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.printfax"], timeout=3)
            return True
        except Exception:
            return False


def clear_print_queue(printer_name=PRINTER_NAME):
    """Cancels all pending jobs in the printer queue."""
    try:
        res = subprocess.run(["cancel", "-a", printer_name], capture_output=True, text=True, timeout=5)
        return True, "Print queue cleared."
    except Exception as e:
        return False, str(e)


def prepare_lossless_rotated_image(image_path, output_dir=None, rotation=0):
    """
    If rotation is needed, prepares a 100% LOSSLESS temporary PNG print file.
    Does NOT use lossy JPEG re-compression. Preserves exact pixel data.
    """
    with Image.open(image_path) as img:
        try:
            import PIL.ImageOps
            img = PIL.ImageOps.exif_transpose(img)
        except Exception:
            pass

        if rotation != 0:
            img = img.rotate(-rotation, expand=True)

        if output_dir is None:
            output_dir = os.path.dirname(image_path)

        base_name = os.path.basename(image_path)
        name, _ = os.path.splitext(base_name)
        out_path = os.path.join(output_dir, f".spool_lossless_{name}.png")

        # Save as 100% LOSSLESS PNG with 300 DPI metadata
        img.convert("RGB").save(out_path, "PNG", dpi=(300, 300))
        return out_path


def print_photo(image_path, copies=1, printer_name=PRINTER_NAME, dry_run=False, rotation=0):
    """
    Sends photo to Canon SELPHY CP1500 using CUPS 'lp'.
    
    LOSSLESS GUARANTEE:
    1. If rotation == 0: Sends original untouched JPEG directly to CUPS.
       CoreGraphics renders the JPEG pixels directly into the 300 DPI print raster
       without any intermediate compression loss. The original file is NEVER modified.
    2. If rotation != 0: Generates a temporary 100% LOSSLESS PNG (zero lossy re-encoding).
    
    Options used:
      - PageSize=Postcard.Fullbleed (Borderless Hagaki 100x148 mm)
      - print-scaling=fill (scales & bleeds to fill 100% of postcard without white margins)
      - ColorModel=RGB
    """
    if not os.path.isfile(image_path):
        return False, f"File not found: {image_path}"

    temp_file = None
    if rotation % 360 != 0:
        # Generate lossless PNG for rotation
        try:
            temp_file = prepare_lossless_rotated_image(image_path, rotation=rotation)
            target_print_file = temp_file
        except Exception:
            target_print_file = image_path
    else:
        # Print original file directly (100% pristine, zero intermediate re-encoding)
        target_print_file = image_path

    fname = os.path.basename(image_path)
    job_ids = []
    errors = []

    for copy_idx in range(1, copies + 1):
        if copies > 1:
            title = f"{fname} (Copy {copy_idx} of {copies})"
        else:
            title = f"{fname} (1 copy)"

        cmd = [
            "lp",
            "-d", printer_name,
            "-t", title,
            "-o", "PageSize=Postcard.Fullbleed",
            "-o", "print-scaling=fill",
            "-o", "ColorModel=RGB",
            target_print_file
        ]

        cmd_str = " ".join(cmd)

        if dry_run:
            job_ids.append(f"Simulated-{copy_idx}/{copies}: {title}")
            continue

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                # Output format: "request id is Canon_SELPHY_CP1500-XX (1 file(s))"
                out = res.stdout.strip()
                parts = out.split()
                jid = parts[3] if len(parts) >= 4 else out
                job_ids.append(f"{jid} [{title}]")
            else:
                err = res.stderr.strip() or res.stdout.strip()
                errors.append(f"Copy {copy_idx}: {err}")
        except Exception as e:
            errors.append(f"Copy {copy_idx} failed: {e}")

    # Clean up temporary lossless file if one was created
    if temp_file and os.path.exists(temp_file):
        try:
            os.remove(temp_file)
        except Exception:
            pass

    if dry_run:
        return True, f"[DRY RUN - Simulated {copies} copies] " + ", ".join(job_ids)

    if errors:
        return False, "; ".join(errors)

    return True, f"Queued {copies} copy/copies: " + ", ".join(job_ids)
