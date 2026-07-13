# BENTO × SPIDER-MAN 2026 — KOL Dashboard

Live: https://araveevong-pixel.github.io/bento-spiderman-kol-dashboard/

## ทำงานยังไง
- **TikTok** (45 ราย): ดึงยอดอัตโนมัติทุก 30 นาที ผ่าน GitHub Actions + yt-dlp
- **Facebook** (9 เพจ) + **Reach ทุกกลุ่ม**: กรอกมือ → กดปุ่ม "กรอกยอด Facebook / Reach" บนแดชบอร์ด → คัดลอก JSON → วางทับ `manual_stats.json`

## เพิ่ม/แก้ลิงก์โพสต์
แก้ `kol_meta.json` → ฟิลด์ `link` ของแต่ละ KOL → commit → CI รอบถัดไปดึงยอดให้เอง

## KPI
View 72M · Reach 13M (อิงแผน Media Kickoff · 4 กลุ่ม KOL)
