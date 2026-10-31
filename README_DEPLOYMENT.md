# RankVerse — Deployment, Security, Incident Response & Operations Guide

## 1. Zero-Cost Architecture Overview
- **Static Hosting**: [GitHub Pages](https://docs.github.com/en/pages/quickstart) (`https://tommyvercetti5700-code.github.io/RANKVERSE/`).
- **Automated Pipeline (`auto_fetch_resources.py`)**: Runs daily at 00:30 UTC (06:00 AM IST) via `.github/workflows/daily_sync.yml` using standard Python 3.11 library modules (`urllib`, `xml.etree.ElementTree`, `json`, `argparse`) with zero paid dependencies.
- **Static Defense-in-Depth**: Client-side administrator passcodes (`14071982`, `5700`) and URL query bypasses (`?owner=`, `?admin=`) are permanently disabled in public JavaScript. All configuration and publishing operations occur exclusively via authenticated GitHub commits and GitHub Actions Secrets.

## 2. Automated Content Pipeline (10-Stage Quality Gate)
Run locally or in CI:
```bash
python3 auto_fetch_resources.py
python3 auto_fetch_resources.py --validate
```
1. **DISCOVER & FETCH**: Queries official public feeds (`NCERT`, `SWAYAM IIT-PAL`).
2. **VERIFY & CLASSIFY**: Enforces HTTPS-only allowlist (`ncert.nic.in`, `nta.ac.in`, `swayam.gov.in`, `upsc.gov.in`, `ssc.gov.in`, `ibps.in`, `gpsc.gujarat.gov.in`, `icai.org`, `archive.org`, `youtube.com`) and records provenance metadata (`canonical_url`, `publisher`, `retrieval_date`, `license`, `verification_status`).
3. **DEDUPLICATE & CHECK**: Preserves existing `resources` and `notes` non-destructively and aborts publication if any required field is missing or any URL fails validation.
4. **PUBLISH**: Writes atomically via `.tmp` files and updates `sitemap.xml`.

## 3. Incident Response, Backups & Credential Rotation
- **Rollback**: Every automated commit in Git history preserves the prior state. To revert an unwanted update, run `git revert HEAD && git push` or revert via the GitHub Commits UI.
- **Credential Rotation**: Store optional future keys (`AMAZON_AFFILIATE_TAG`, `ENABLE_MONETIZATION`) only in **Settings → Secrets and variables → Actions**, never in `index.html`.
- **Optional Free-Tier Backend Upgrade**: When multi-device server-validated leaderboards or OAuth login are needed in the future, connect a free-tier Supabase or Firebase Authentication project with Row-Level Security (RLS).
