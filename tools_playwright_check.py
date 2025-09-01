import json
from playwright.sync_api import sync_playwright
url='http://127.0.0.1:8000'
logs=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={'width':1280,'height':800})
    page=context.new_page()
    page.on('console', lambda m: logs.append({'type': m.type, 'text': m.text}))
    page.goto(url, wait_until='networkidle', timeout=20000)
    page.wait_for_timeout(1000)
    html=page.content()
    page.screenshot(path='playwright_screenshot.png', full_page=True)
    result={'health': ('HEALTHCHECK_BUYPEER' in html) or ('Blade OK' in html), 'has_app_div': ('id="app"' in html) or ('id="admin-app"' in html) or ('id="site-app"' in html), 'console': logs[-10:]}
    print('RESULT_JSON:'+json.dumps(result))
