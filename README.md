# Daybreak — Daily News Briefing

A personal morning news briefing covering **Leisure & Entertainment (the attractions industry), Crypto, AI, Tech, World Affairs, Politics, and Finance**, refreshed automatically every morning.

The Leisure & Entertainment section leads the page (Aahan works at Amusement Services International): 2-3 trade stories a day from sources like [Blooloop](https://blooloop.com/) and [Amusements & Attractions](https://www.amusementsandattractions.com/), prioritizing arcades, FECs, and the Middle East market. One industry story also appears in the email under "From the industry".

**Read it here (bookmark this):** https://claude.ai/code/artifact/904b7d2f-409a-41c5-bf5d-d98684779486

## How it works

```
Every morning:
  Scheduled Claude routine (cloud)
    ├── researches overnight headlines across all topics
    ├── rewrites briefing/index.html  → redeploys the artifact page (same URL)
    └── rewrites briefing/email.html → commits & pushes to this repo

  Google Apps Script (your account, ~30 min later)
    └── fetches raw.githubusercontent.com/.../briefing/email.html
        and emails it to aahanprakash123@gmail.com
```

## Files

- `briefing/index.html` — the full briefing page (source of the artifact). Design system: "Daybreak" — dawn-blue paper, navy ink, single amber accent, serif headlines. Both light and dark themes. The Crypto section opens with a **Crypto Board**: the top 10 coins by market cap (excluding stablecoins, always including BTC/ETH/XRP/ADA) with price and 24h change, refreshed daily.
- `briefing/email.html` — compact Gmail-safe nudge: markets line, top 3 stories, button to the full page. The `<title>` tag is the email subject line.
- `apps-script/Code.gs` — the Apps Script that sends the email (lives in script.google.com, kept here as the source of truth).

## One-time setup checklist

1. Create a **public** GitHub repo named `daily-briefing` and push this folder to it.
2. Go to [script.google.com](https://script.google.com) → New project → paste `apps-script/Code.gs`, set `GITHUB_USER`.
3. Run `sendDaybreak` once manually to grant Gmail permissions (it will send you today's edition).
4. Add a trigger: clock icon → Add Trigger → `sendDaybreak`, time-driven, day timer, 7am–8am.

## Changing things

- **Topics, story counts, tone**: edit the scheduled routine's prompt (`/schedule` in Claude Code).
- **Delivery time**: the routine runs at 6:15am; move the Apps Script trigger window to taste (keep it after the routine finishes, ~6:45am+).
- **Design**: edit `briefing/index.html` styles — the routine preserves the design and only replaces content.
