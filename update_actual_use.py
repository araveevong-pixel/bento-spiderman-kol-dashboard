#!/usr/bin/env python3
import re, sys
amount = float(sys.argv[1]); html_file = sys.argv[2] if len(sys.argv) > 2 else 'index.html'
html = open(html_file, encoding='utf-8').read()
html = re.sub(r'const\s+CAMPAIGN_ACTUAL_USE_DEFAULT\s*=\s*[\d.]+',
              f'const CAMPAIGN_ACTUAL_USE_DEFAULT = {amount}', html)
open(html_file,'w',encoding='utf-8').write(html)
print(f"Actual Use -> {amount:,.0f}")
