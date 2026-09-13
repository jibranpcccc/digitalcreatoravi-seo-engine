# Fleet Masterclass Typography Injector
from pathlib import Path

PALETTES = {
    5: ('VectorBench', '#06b6d4', '#22d3ee', 'rgba(6, 182, 212, 0.25)', 'rgba(8, 51, 68, 0.7)'),
    6: ('NomadTreaty', '#10b981', '#34d399', 'rgba(16, 185, 129, 0.25)', 'rgba(6, 78, 59, 0.7)'),
    7: ('WebhookWatch', '#f59e0b', '#fbbf24', 'rgba(245, 158, 11, 0.25)', 'rgba(120, 53, 15, 0.7)'),
    8: ('LocalDocPrivacy', '#6366f1', '#818cf8', 'rgba(99, 102, 241, 0.25)', 'rgba(49, 46, 129, 0.7)'),
    9: ('FounderRunway', '#10b981', '#34d399', 'rgba(16, 185, 129, 0.25)', 'rgba(6, 78, 59, 0.7)'),
    10: ('RAGInspect', '#0284c7', '#38bdf8', 'rgba(2, 132, 199, 0.25)', 'rgba(8, 47, 73, 0.7)'),
    11: ('NomadPassportIndex', '#3b82f6', '#60a5fa', 'rgba(59, 130, 246, 0.25)', 'rgba(30, 58, 138, 0.7)'),
    12: ('SaaSUnitMath', '#a855f7', '#c084fc', 'rgba(168, 85, 247, 0.25)', 'rgba(88, 28, 135, 0.7)'),
    13: ('GrokLogTester', '#f97316', '#fb923c', 'rgba(249, 115, 22, 0.25)', 'rgba(124, 45, 18, 0.7)'),
    14: ('SOC2Ready', '#10b981', '#34d399', 'rgba(16, 185, 129, 0.25)', 'rgba(6, 78, 59, 0.7)'),
    15: ('EORCalculator', '#2563eb', '#60a5fa', 'rgba(37, 99, 235, 0.25)', 'rgba(30, 58, 138, 0.7)'),
    16: ('DevConfigHub', '#0284c7', '#38bdf8', 'rgba(2, 132, 199, 0.25)', 'rgba(8, 47, 73, 0.7)'),
    17: ('OpenCRMStack', '#7c3aed', '#a78bfa', 'rgba(124, 58, 237, 0.25)', 'rgba(76, 29, 149, 0.7)'),
    18: ('CIPipelineGraph', '#e11d48', '#fb7185', 'rgba(225, 29, 72, 0.25)', 'rgba(136, 19, 55, 0.7)'),
    19: ('GreekVisualizer', '#f59e0b', '#fbbf24', 'rgba(245, 158, 11, 0.25)', 'rgba(120, 53, 15, 0.7)'),
    20: ('EdgeRuntimeHQ', '#06b6d4', '#22d3ee', 'rgba(6, 182, 212, 0.25)', 'rgba(8, 51, 68, 0.7)'),
}

def generate_style(name, accent, light_accent, grad_start, grad_end):
    return f"""    <style is:global>
      /* Masterclass Editorial & Technical Typography for {name} */
      .prose {{
        color: #cbd5e1;
        font-size: 1.0625rem;
        line-height: 1.85;
        max-width: 100%;
      }}

      .prose h1, .prose h2, .prose h3, .prose h4 {{
        color: #f8fafc;
        font-weight: 800;
        letter-spacing: -0.025em;
      }}

      .prose h2 {{
        font-size: 1.75rem;
        margin-top: 3.5rem;
        margin-bottom: 1.25rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.18);
        display: flex;
        align-items: center;
        gap: 0.5rem;
      }}

      .prose h3 {{
        font-size: 1.35rem;
        margin-top: 2.5rem;
        margin-bottom: 1rem;
        color: #e2e8f0;
      }}

      .prose h4 {{
        font-size: 1.125rem;
        margin-top: 2rem;
        margin-bottom: 0.75rem;
        color: {light_accent};
      }}

      .prose p {{
        margin-top: 1.25rem;
        margin-bottom: 1.25rem;
        color: #cbd5e1;
        line-height: 1.85;
      }}

      .prose strong {{
        color: #ffffff;
        font-weight: 700;
      }}

      .prose a {{
        color: {light_accent};
        text-decoration: underline;
        text-underline-offset: 4px;
        font-weight: 500;
        transition: color 0.15s ease;
      }}
      .prose a:hover {{
        color: #ffffff;
      }}

      .prose ul {{
        list-style-type: disc !important;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        padding-left: 1.75rem !important;
      }}

      .prose ol {{
        list-style-type: decimal !important;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        padding-left: 1.75rem !important;
      }}

      .prose li {{
        margin-top: 0.625rem;
        margin-bottom: 0.625rem;
        line-height: 1.8;
        color: #cbd5e1;
        display: list-item !important;
      }}

      .prose li::marker {{
        color: {accent};
      }}

      .prose blockquote {{
        margin: 2.25rem 0;
        padding: 1.5rem 1.75rem;
        background: linear-gradient(135deg, {grad_start} 0%, {grad_end} 100%);
        border-left: 4px solid {accent};
        border-top: 1px solid rgba(148, 163, 184, 0.15);
        border-right: 1px solid rgba(148, 163, 184, 0.15);
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 0 1rem 1rem 0;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.4);
      }}

      .prose blockquote p {{
        color: #e2e8f0;
        margin: 0.5rem 0;
        line-height: 1.8;
      }}

      .prose blockquote strong {{
        color: #ffffff;
      }}

      /* Modern Data Tables */
      .prose table {{
        width: 100%;
        border-collapse: separate !important;
        border-spacing: 0;
        margin: 2.5rem 0;
        border-radius: 0.875rem;
        overflow: hidden;
        border: 1px solid #334155;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.4);
        font-size: 0.9375rem;
      }}

      .prose thead {{
        background: #0f172a;
      }}

      .prose th {{
        padding: 1.125rem 1.25rem;
        font-size: 0.8125rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #f1f5f9;
        text-align: left;
        border-bottom: 2px solid #334155;
        background: #0f172a;
      }}

      .prose td {{
        padding: 1rem 1.25rem;
        color: #cbd5e1;
        border-bottom: 1px solid #1e293b;
        vertical-align: middle;
      }}

      .prose tr:last-child td {{
        border-bottom: none;
      }}

      .prose tbody tr {{
        background: rgba(15, 23, 42, 0.5);
        transition: background 0.15s ease;
      }}

      .prose tbody tr:nth-child(even) {{
        background: rgba(30, 41, 59, 0.4);
      }}

      .prose tbody tr:hover {{
        background: rgba(255, 255, 255, 0.05);
      }}

      /* Code and Syntax */
      .prose code:not(pre code) {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.875em;
        font-weight: 600;
        color: {light_accent};
        background: rgba(15, 23, 42, 0.8);
        padding: 0.2em 0.45em;
        border-radius: 0.375rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
      }}

      .prose pre {{
        margin: 2.25rem 0;
        padding: 1.35rem 1.5rem;
        background: #090d16 !important;
        border: 1px solid #1e293b;
        border-radius: 0.875rem;
        overflow-x: auto;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
      }}

      .prose pre code {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.875rem;
        line-height: 1.7;
        color: #e2e8f0;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
      }}

      .prose hr {{
        margin: 3.5rem 0;
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.25), transparent);
      }}
    </style>"""

sites_dir = Path(r'c:\Users\jibra\Desktop\1\digitalcreatoravi\sites')
updated = 0
for site_id, (name, accent, light_accent, grad_start, grad_end) in PALETTES.items():
    layout_file = sites_dir / f'site-{site_id}' / 'src' / 'layouts' / 'Layout.astro'
    if not layout_file.exists():
        continue
    content = layout_file.read_text(encoding='utf-8')
    if '.prose' in content:
        print(f'Site {site_id} already has .prose, skipping')
        continue
    if '</head>' in content:
        style_block = generate_style(name, accent, light_accent, grad_start, grad_end)
        content = content.replace('</head>', f'{style_block}\n  </head>')
        layout_file.write_text(content, encoding='utf-8')
        print(f'Successfully injected typography for Site {site_id} ({name})')
        updated += 1
    else:
        print(f'Site {site_id}: </head> not found!')

print(f'Total sites updated: {updated}')

