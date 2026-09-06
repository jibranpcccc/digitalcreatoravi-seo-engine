import os

beacon = """
    <!-- Fleet Master Analytics Beacon -->
    <script is:inline>
      (function() {
        try {
          var payload = JSON.stringify({
            site: window.location.hostname,
            path: window.location.pathname,
            ref: document.referrer || "direct",
            screen: window.innerWidth + "x" + window.innerHeight,
            ts: Date.now()
          });
          var endpoint = "https://webhookwatch.vercel.app/api/track/";
          if (navigator.sendBeacon) {
            navigator.sendBeacon(endpoint, payload);
          } else {
            fetch(endpoint, { method: "POST", body: payload, keepalive: true, headers: { "Content-Type": "application/json" } }).catch(function(){});
          }
        } catch(e) {}
      })();
    </script>
"""

sites = ['site-1', 'site-2', 'site-3', 'site-4', 'site-5', 'site-6', 'site-7', 'site-8']
for s in sites:
    layout_path = f'sites/{s}/src/layouts/Layout.astro'
    if os.path.exists(layout_path):
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'https://webhookwatch.vercel.app/api/track"' in content:
            content = content.replace('https://webhookwatch.vercel.app/api/track"', 'https://webhookwatch.vercel.app/api/track/"')
            with open(layout_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated slash in {layout_path}')
        elif 'Fleet Master Analytics Beacon' not in content:
            if '</head>' in content:
                content = content.replace('</head>', beacon + '\n  </head>')
                with open(layout_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'Injected beacon into {layout_path}')

print("Completed tracker verification across all 8 sites!")

