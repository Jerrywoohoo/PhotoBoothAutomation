"""
ui_macos.py
Built-in macOS interface using AppleScript dialogs and Quick Look preview.
Zero GUI frameworks required; 100% native macOS dialogs.
"""

import subprocess
import os
import time

def prompt_photo_print_native(image_path, printer_name="Canon_SELPHY_CP1500"):
    """
    1. Opens Quick Look preview of the photo in background.
    2. Displays an AppleScript alert asking whether to print and how many copies.
    3. Returns (should_print, copies, rotation)
    """
    filename = os.path.basename(image_path)
    
    # 1. Open Quick Look preview in background
    ql_proc = None
    try:
        ql_proc = subprocess.Popen(["qlmanage", "-p", image_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.4)
    except Exception:
        pass

    # 2. AppleScript Dialog
    applescript = f'''
    set dialogResult to display alert "Photo Booth: New Photo Captured" message "File: {filename}\nDo you want to print to {printer_name}?" as informational buttons {{"Skip", "Print 2", "Print 1"}} default button "Print 1" cancel button "Skip"
    return button returned of dialogResult
    '''

    btn = "Skip"
    try:
        res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
        btn = res.stdout.strip()
    except Exception:
        pass
    finally:
        # Close Quick Look preview
        if ql_proc:
            try:
                ql_proc.terminate()
            except Exception:
                pass

    if btn == "Print 1":
        return True, 1, 0
    elif btn == "Print 2":
        return True, 2, 0
    else:
        return False, 0, 0

