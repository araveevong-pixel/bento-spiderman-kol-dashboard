#!/usr/bin/env python3
"""Set CAMPAIGN_ACTUAL_USE_DEFAULT in index.html. Tolerant of commas, ฿, spaces."""
import re, sys

def parse_amount(raw):
    s = str(raw).strip().replace(',', '').replace('฿', '').replace('THB', '').replace(' ', '')
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        print(f"skip: cannot parse Actual Use value {raw!r}")
        return None

def main():
    if len(sys.argv) < 2:
        print("skip: no Actual Use value given"); return 0
    amount = parse_amount(sys.argv[1])
    if amount is None:
        return 0                      # ไม่ทำให้ workflow ล้ม
    html_file = sys.argv[2] if len(sys.argv) > 2 else 'index.html'
    html = open(html_file, encoding='utf-8').read()
    html, n = re.subn(r'const\s+CAMPAIGN_ACTUAL_USE_DEFAULT\s*=\s*[\d.]+',
                      f'const CAMPAIGN_ACTUAL_USE_DEFAULT = {amount}', html)
    if n == 0:
        print("warn: CAMPAIGN_ACTUAL_USE_DEFAULT not found in html"); return 0
    open(html_file, 'w', encoding='utf-8').write(html)
    print(f"Actual Use -> {amount:,.2f}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
