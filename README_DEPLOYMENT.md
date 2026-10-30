## 🌱 Pure Free Study Mode Now — Enable Monetization Later Anytime!
By default, your portal and daily Python bot now run in **100% Pure Free Study Mode (`monetizationEnabled: false`)**:
- All Amazon affiliate links, book store tabs, and sponsored banners are **hidden by default** so students get a 100% clean, distraction-free study portal while your traffic grows.
- **How to Add Monetization Later (Zero Coding Required):**
  1. On your live website, open the **🤖 Auto-Bot & Admin Panel** tab (or click **🎛️ Monetization: OFF (Add Later)** in the top bar) and click **🔓 Enable Monetization Features**.
  2. Or in your GitHub repository, go to **Settings → Secrets and variables → Actions** and set `ENABLE_MONETIZATION` to `true` along with your `AMAZON_AFFILIATE_TAG`.

# RankVerse AI — 100% Automated JEE / NEET / CUET / NDA Study Portal & Money-Making Bundle (v2.0)

## Does It Auto-Fill All Formula Sheets, Find Every Note/PDF & Upload Daily By Itself?
**YES — 100% Automatically:**
1. **Daily Syllabus Formula Sheet Generator (`auto_fetch_resources.py`):**
   - Contains a built-in JEE/NEET/CUET/NDA syllabus queue with deterministic Physics, Chemistry, Mathematics, and Biology formula banks (plus optional **free Google Gemini API** enrichment if you add a free `GEMINI_API_KEY` secret).
   - Every morning at **06:00 AM IST**, GitHub Actions runs `auto_fetch_resources.py`, generates the next chapter's complete formula sheet, creates a standalone printable HTML/PDF study sheet in `generated_notes/`, and adds it to `resources_data.json`.
2. **Automatic Official NCERT PDF & Open Educational Resource Finder:**
   - Queries the **Internet Archive Open Educational API** (`archive.org/advancedsearch.php`) and links directly to official **NCERT Textbook PDFs** (`https://ncert.nic.in/textbook/pdf/...`) — 100% legal and copyright-safe.
3. **Automatic Daily YouTube One-Shot Lecture Discovery:**
   - Reads official public YouTube RSS feeds (`youtube.com/feeds/videos.xml`) to embed the newest One-Shot revision marathons legally via YouTube's official player.
4. **Automatic Monetization Injection (₹100–₹420 per Converting Visitor):**
   - Every auto-generated formula sheet, PDF card, and video modal automatically attaches your **Amazon India Associate Tag** (`?tag=yourtag-21`) and **EdTech Scholarship CPL Referral Banner**.

---

## 3-Minute Zero-Cost Setup on GitHub Pages

1. Create a free public repository on [GitHub](https://github.com/new) (e.g., `rankverse-study-hub`).
2. Extract this ZIP bundle and upload all files (`index.html`, `auto_fetch_resources.py`, `resources_data.json`, `.github/workflows/daily_sync.yml`, and `generated_notes/`) to your repository.
3. Go to **Settings → Pages** in your GitHub repository and select **Deploy from a branch → `main` / `(root)`**. Your live website will be online in 60 seconds at `https://<your-username>.github.io/rankverse-study-hub/`.
4. Go to **Settings → Secrets and variables → Actions** and add your optional secrets:
   - `AMAZON_AFFILIATE_TAG`: Your Amazon India Associate ID (e.g., `myjeesite-21` from [affiliate-program.amazon.in](https://affiliate-program.amazon.in/)).
   - `CPL_SCHOLARSHIP_URL`: Your affiliate tracking link for Unacademy / PW / Allen / Testbook scholarship tests.
   - `GEMINI_API_KEY` *(Optional, 100% Free Tier)*: Get a free API key from [Google AI Studio](https://aistudio.google.com/) to unlock unlimited AI-synthesized chapter notes.
