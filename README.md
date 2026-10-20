# 📸 Photo Booth Print Automation for Canon SELPHY CP1500

Automated, lossless, borderless photo printing workflow for Sony Imaging Edge + Canon SELPHY CP1500 on macOS.

---

## 🎯 The Problem This Solves

When printing manually from macOS Preview or System Dialogs:
1. **Aspect Ratio Mismatch:** Sony Alpha cameras shoot at **3:2 (1.50)**. Canon SELPHY paper is Japanese Postcard (Hagaki / KP-108IN) at **100 x 148 mm (1.48)**.
2. **Preview Scaling Reset:** Preview defaults to ~29% scale to fit inside default printable margins, leaving white borders.
3. **Lost Presets:** macOS presets **never save scale percentage** between documents. You had to manually crank the slider from 29% to 31% on every single photo.

### How This Script Solves It Automatically:
- **CUPS Direct Printing:** Uses the exact hardware profile: `-o PageSize=Postcard.Fullbleed` and `-o print-scaling=fill`.
- **Zero Lossy Re-encoding:** Sends the original image directly into macOS CoreGraphics print rasterizer in memory without intermediate JPEG compression. The original camera files remain 100% untouched.
- **Side-by-Side Batch Display:** If guests take 3 photos in a session, all 3 are displayed on screen simultaneously for quick visual comparison, selection, and printing.
- **One-Click Session Reset:** A single **"Next Group / Clear Feed"** button archives the session and clears the screen ready for the next guest.

---

## 🎬 Demo Video

Check out [`howtouse.mov`](howtouse.mov) for a quick walkthrough showing live camera tethering, side-by-side selection, Google Drive-style zoom preview, and printing.

---

## 🚀 How to Run

Navigate to the directory:
```bash
cd "/Volumes/Jerry_SSD 1/Work/ie/PhotoBoothAutomation"
```

### 1. Interactive Test Mode (Simulate 3 Camera Shots)
```bash
python3 interactive_test.py
```
- Creates 3 synthetic camera photos with colors, numbers, and timestamps.
- Launches the UI with all 3 photos displayed side-by-side.
- Lets you click to select, choose copies, and queue test jobs to macOS Print Center (`Canon_SELPHY_CP1500`).
- You can click **"📋 Mac Print Queue"** in the top bar to inspect the pending jobs in macOS native Print Center.

### 2. Live Photo Booth Station (Normal Usage)
```bash
./run.sh
```
- Listens to your Sony Imaging Edge save folder.
- When photos arrive, they immediately show up side-by-side.
- Click **"🖨️ Print Selected Photos"** (or press `Enter`) to print.
- Click **"✅ Next Group / Clear Feed"** (or press `c`) when that group is done to reset the feed for the next guest.

---

## ⌨️ Shortcuts & Controls

- **Click Photo Card:** Toggle selection for printing (`✓ SELECTED` vs `✕ SKIPPED`).
- **`🔍 Preview` Button (or Double-Click Photo):** Open the **Google Drive-style Full-Display Lightbox** (`1128×752 px`) with up to **400% zoom**, click-and-drag panning, `◀ Prev` / `Next ▶` arrows, and `Esc` to close.
- **Grid Zoom (`⌘ + Scroll` or Top Bar `[−] 🔍 100% [+]`, or `⌘ +` / `⌘ -`):** Dynamically scales photo cards and automatically snaps between **3 per row**, **2 per row**, and **1 per row** (`⌘ 0` or click the zoom label to reset to `100%`).
- **`[−] Copies [+]`:** Set number of copies per photo (live copy counts appear directly on the print buttons).
- **`Enter`:** Print all selected photos.
- **`c`:** Finish session & clear feed for next group.
- **`📸 +3 Shots`:** Generates 3 simulated HD camera photos in the watched folder anytime to test tethering.
- **`📋 Print Queue`:** Opens macOS Print Center to see pending print jobs.
- **`🧪 Test Mode: ON` / `🖨️ Live Print: ON`:** Toggle in the top bar between safe simulation and live printing.

---

## 📁 File Structure

- `photobooth.py`: Main CLI & launcher.
- `ui_booth.py`: Multi-photo batch kiosk UI with high-contrast custom buttons.
- `printer_service.py`: Lossless CUPS (`lp`) communication and print queue management.
- `watcher.py`: Background thread monitoring Sony Imaging Edge save folder.
- `simulate_shots.py`: Generates 3:2 synthetic camera photos for testing.
- `interactive_test.py`: End-to-end interactive test script.
- `config.json`: Stores your chosen watch folder and settings.
