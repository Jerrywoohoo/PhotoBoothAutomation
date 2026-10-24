# 📸 Photo Booth Print Automation for Canon SELPHY CP1500

Automated, lossless, borderless photo printing workflow with multi-template `.png` frame overlays for Sony Imaging Edge + Canon SELPHY CP1500 on macOS.

---

## 🚀 How to Use (Quick Start)

### 1. Clone the Repository & Enter the Folder
```bash
git clone https://github.com/Jerrywoohoo/PhotoBoothAutomation.git
cd PhotoBoothAutomation
```

### 2. Grant Script Execution Permissions (macOS)
On macOS, newly cloned or downloaded repositories may block shell scripts with `Permission denied` or Gatekeeper quarantine flags. Run this once inside the folder to allow running the scripts:
```bash
chmod +x run.sh
xattr -cr .
```

### 3. Install Dependency (`Pillow`)
```bash
pip3 install Pillow
```

### 4. Run the App

#### Option A: Live Photo Booth Station (or Toggle Test Mode in UI)
```bash
./run.sh
# Or run directly with Python and specify a custom camera folder:
python3 photobooth.py --folder "<image source>"
```
- Monitors your Sony Imaging Edge save folder (`<image source>`, defaults to `~/Pictures`).
- Incoming camera photos appear side-by-side automatically.
- Click **"🖨️ Print Selected Photos"** (or press `Enter`) to print.
- Click **"✅ Next Group / Clear Feed"** (or press `c`) to archive the session and clear the screen for the next guest.

#### Option B: Interactive Test Mode (Pre-loads 3 Simulated Shots)
```bash
python3 interactive_test.py
```
- Generates 3 clean **3:2 (`3000×2000 px`)** gradient test photos with a centered shot number circle and a thin **`1.48` printable area boundary line** (`2960×2000 px`) so you can verify exact center-cropping.
- Launches the UI in **Test Mode** so you can test frame templates, selection, and copies safely without using paper.

---

## 🎯 The Problem This Solves

When printing manually from macOS Preview, System Dialogs, or Canva:
1. **Aspect Ratio Mismatch:** Sony Alpha cameras shoot at **3:2 (1.50)**. Canon SELPHY paper is Japanese Postcard (Hagaki / KP-108IN) at **100 x 148 mm (1.48)**.
2. **Preview Scaling Reset:** Preview defaults to ~29% scale to fit inside default printable margins, leaving white borders.
3. **Lost Presets:** macOS presets **never save scale percentage** between documents. You had to manually crank the slider from 29% to 31% on every single photo.
4. **Manual Canva Frame Overlays:** Manually importing camera shots into Canva, overlaying transparent `.png` frames, exporting PDFs, and printing takes too long during live events.

### How This Script Solves It Automatically:
- **CUPS Direct Printing:** Uses the exact hardware profile: `-o PageSize=Postcard.Fullbleed` and `-o print-scaling=fill`.
- **Multi-Template Photo Frame Overlays:** Point the app to any folder of transparent `.png` frames (`1.48` ratio). The app center-crops `3:2` camera shots to `1.48`, composites the chosen frame losslessly at 300 DPI, and previews it live on every card and in the full-screen lightbox.
- **Zero Lossy Re-encoding:** Sends the high-resolution image directly into macOS CoreGraphics print rasterizer without intermediate JPEG compression. Original camera files remain 100% untouched.
- **Side-by-Side Batch Display:** If guests take 3 photos in a session, all 3 are displayed on screen simultaneously for quick visual comparison, individual frame choice, and printing.
- **One-Click Session Reset:** A single **"Next Group / Clear Feed"** button archives the session and clears the screen ready for the next guest.

---

## ⌨️ Shortcuts & Controls

- **Click Photo Card:** Toggle selection for printing (`✓ SELECTED` vs `✕ SKIPPED`).
- **`🔍 Preview` Button (or Double-Click Photo):** Open the **Google Drive-style Full-Display Lightbox** (`1128×752 px`) with up to **400% zoom**, click-and-drag panning, `◀ Prev` / `Next ▶` arrows, live frame selector, and `Esc` to close.
- **Grid Zoom (`⌘ + Scroll` or Top Bar `[−] 🔍 100% [+]`, or `⌘ +` / `⌘ -`):** Dynamically scales photo cards and automatically snaps between **3 per row**, **2 per row**, and **1 per row** (`⌘ 0` or click the zoom label to reset to `100%`).
- **Individual Photo Frame Selection (`[ ◀ ] [ 🖼️ Template Name ] [ ▶ ]`):** Each photo card has its own dedicated frame row with left (`◀`) and right (`▶`) circular arrow buttons (`1 -> 2 -> 3 -> 1`) and an adaptive template name button that expands to display the full filename without clipping. Click the template name button for a dropdown menu to pick any template or turn the frame OFF (`🚫 No Frame`) for that specific shot.
- **Top Bar Session Default & Multi-Template Folder (`[ ◀ ] [ 🖼️ Default Template ] [ ▶ ]` or `f` key):** Point the app to any folder containing transparent `.png` frames. Sets the session default template for incoming photos, or applies a template to all current photos via the dropdown menu.
- **`[−] Copies [+]`:** Set number of copies per photo (live copy counts appear directly on the print buttons).
- **`🔄 Rotate`:** Rotates the photo 90° clockwise losslessly.
- **`Enter`:** Print all selected photos.
- **`c`:** Finish session & clear feed for next group.
- **`🧪 Test Mode: ON` / `🖨️ Live Print: ON`:** Toggle in the top bar between safe simulation and live printing.
- **`📸 +3 Shots` (Test Mode only):** Generates 3 simulated 3:2 camera photos in the watched folder during `🧪 Test Mode: ON`. Automatically hidden when switched to `🖨️ Live Print: ON` to prevent accidental clicks during live events.
- **`📋 Print Queue`:** Opens macOS Print Center to inspect pending print jobs.

---

## 📁 File Structure

- `photobooth.py`: Main CLI & launcher.
- `ui_booth.py`: Multi-photo batch kiosk UI with custom auto-sizing buttons and per-photo frame controls.
- `printer_service.py`: Lossless CUPS (`lp`) communication, `1.48` center-crop + `.png` frame compositing, and print queue management.
- `watcher.py`: Background thread monitoring Sony Imaging Edge save folder.
- `simulate_shots.py`: Generates clean 3:2 gradient test photos with centered shot numbers and `1.48` printable boundary lines.
- `interactive_test.py`: End-to-end interactive test script.
- `sample_frames/`: Folder containing ready-to-use transparent `.png` frame templates (`1.48` postcard ratio).
- `run.sh`: macOS shell launcher.
- `config.json`: Stores your chosen watch folder and frame folder settings.
