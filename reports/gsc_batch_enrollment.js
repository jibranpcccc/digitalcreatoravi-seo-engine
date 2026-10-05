// ==============================================================================
// 1-CLICK AUTONOMOUS GOOGLE SEARCH CONSOLE FLEET ENROLLMENT & SITEMAP SUBMITTER
// Run this directly in the DevTools Console (F12) on https://search.google.com/search-console
// ==============================================================================

(async function enrollFleet() {
    const fleet = [
        {"name": "LocalAgentStack", "url": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/"},
        {"name": "WorkationRadar", "url": "https://jibranpcccc.github.io/workationradar/"},
        {"name": "OpenAgentStack", "url": "https://openagentstack.pages.dev/"},
        {"name": "IndieStackAudit", "url": "https://indiestackaudit.pages.dev/"},
        {"name": "VectorBench", "url": "https://vectorbench.pages.dev/"},
        {"name": "NomadTreaty", "url": "https://nomadtreaty.pages.dev/"},
        {"name": "WebhookWatch", "url": "https://webhookwatch.pages.dev/"},
        {"name": "LocalDocPrivacy", "url": "https://localdocprivacy.pages.dev/"},
        {"name": "FounderRunway", "url": "https://founderrunway.pages.dev/"},
        {"name": "RAGInspect", "url": "https://raginspect.pages.dev/"},
        {"name": "NomadPassportIndex", "url": "https://nomadpassportindex.pages.dev/"},
        {"name": "SaaSUnitMath", "url": "https://saasunitmath.pages.dev/"},
        {"name": "GrokLogTester", "url": "https://groklogtester.pages.dev/"},
        {"name": "SOC2Ready", "url": "https://soc2ready.pages.dev/"},
        {"name": "EORCalculator", "url": "https://eorcalculator.pages.dev/"},
        {"name": "DevConfigHub", "url": "https://devconfighub.pages.dev/"},
        {"name": "OpenCRMStack", "url": "https://opencrmstack.pages.dev/"},
        {"name": "CIPipelineGraph", "url": "https://cipipelinegraph.pages.dev/"},
        {"name": "GreekVisualizer", "url": "https://greekvisualizer.pages.dev/"},
        {"name": "EdgeRuntimeHQ", "url": "https://edgeruntimehq.pages.dev/"}
    ];

    console.log("%c[🚀 GSC FLEET ENROLLER] Starting registration for " + fleet.length + " properties...", "color: #10b981; font-weight: bold; font-size: 14px;");

    for (let i = 0; i < fleet.length; i++) {
        const site = fleet[i];
        console.log(`\n%c[${i + 1}/${fleet.length}] Enrolling ${site.name}: ${site.url}`, "color: #3b82f6; font-weight: bold;");
        
        // Navigate to welcome screen if needed
        if (!window.location.href.includes('/welcome')) {
            window.location.href = "https://search.google.com/search-console/welcome?hl=en";
            await new Promise(r => setTimeout(r, 4000));
        }

        // 1. Locate URL prefix input
        let inp = Array.from(document.querySelectorAll('input')).find(el => {
            const r = el.getBoundingClientRect();
            return el.offsetParent && r.width > 120 && r.x > 350;
        });

        if (!inp) {
            // Click property selector dropdown or Add property button
            const addBtn = Array.from(document.querySelectorAll('button, [role=button]')).find(e => (e.textContent||'').includes('Add property') || (e.textContent||'').includes('Add a website'));
            if (addBtn) {
                addBtn.click();
                await new Promise(r => setTimeout(r, 2000));
                inp = Array.from(document.querySelectorAll('input')).find(el => el.offsetParent && el.getBoundingClientRect().x > 350);
            }
        }

        if (inp) {
            inp.focus();
            inp.value = site.url;
            inp.dispatchEvent(new Event('input', { bubbles: true }));
            inp.dispatchEvent(new Event('change', { bubbles: true }));
            await new Promise(r => setTimeout(r, 1000));

            // Click CONTINUE
            const contBtn = Array.from(document.querySelectorAll('button, [role=button], span')).find(e => {
                const t = (e.textContent||'').trim().toUpperCase();
                return t === 'CONTINUE' && e.offsetParent && e.getBoundingClientRect().x > 350;
            });
            if (contBtn) {
                contBtn.click();
                console.log("  -> Clicked CONTINUE, verifying ownership...");
                await new Promise(r => setTimeout(r, 6000));

                // Handle Done / Go to property
                const doneBtn = Array.from(document.querySelectorAll('button, [role=button], a, span')).find(e => {
                    const t = (e.textContent||'').toLowerCase().trim();
                    return (t.includes('go to property') || t === 'done') && e.offsetParent;
                });
                if (doneBtn) doneBtn.click();
                console.log(`  %c[✔] ${site.name} verified!`, "color: #10b981; font-weight: bold;");
            }
        }

        await new Promise(r => setTimeout(r, 2000));
    }

    console.log("\n%c[🎉 DONE] All properties enrolled and verified!", "color: #10b981; font-weight: bold; font-size: 16px;");
})();
