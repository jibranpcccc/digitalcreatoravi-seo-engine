#!/usr/bin/env python3
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def run_cmd(cmd, cwd):
    print(f'[*] Executing: {cmd} in {cwd}')
    res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f'[-] Error:
{res.stderr or res.stdout}')
        return False, res.stderr or res.stdout
    print(f'[OK] Success:
{res.stdout[:200]}')
    return True, res.stdout

def deploy_wave1():
    print('================================================================')
    print('DEPLOYING WAVE 1 SITES (SITES 9 TO 13)')
    print('================================================================')
    
    # 1. Site 9 -> Vercel
    s9_dir = os.path.join(ROOT, 'sites', 'site-9')
    if os.path.exists(os.path.join(s9_dir, 'dist')):
        print('[+] Deploying Site 9 (FounderRunway) to Vercel...')
        run_cmd('npx vercel --prod --yes', s9_dir)

    # 2. Site 10 -> Cloudflare Pages
    s10_dir = os.path.join(ROOT, 'sites', 'site-10')
    if os.path.exists(os.path.join(s10_dir, 'dist')):
        print('[+] Deploying Site 10 (RAGInspect) to Cloudflare Pages...')
        run_cmd('npx wrangler pages deploy dist --project-name=raginspect', s10_dir)

    # 3. Site 11 -> Netlify
    s11_dir = os.path.join(ROOT, 'sites', 'site-11')
    if os.path.exists(os.path.join(s11_dir, 'dist')):
        print('[+] Deploying Site 11 (NomadPassportIndex) to Netlify...')
        run_cmd('npx netlify deploy --prod --dir=dist --site=nomadpassportindex --no-build', s11_dir)

    # 4. Site 12 -> GitHub Pages
    s12_dir = os.path.join(ROOT, 'sites', 'site-12')
    if os.path.exists(os.path.join(s12_dir, 'dist')):
        print('[+] Deploying Site 12 (SaaSUnitMath)...')
        run_cmd('npx vercel --prod --yes', s12_dir)

    # 5. Site 13 -> Cloudflare Pages
    s13_dir = os.path.join(ROOT, 'sites', 'site-13')
    if os.path.exists(os.path.join(s13_dir, 'dist')):
        print('[+] Deploying Site 13 (GrokLogTester) to Cloudflare Pages...')
        run_cmd('npx wrangler pages deploy dist --project-name=groklogtester', s13_dir)

if __name__ == '__main__':
    deploy_wave1()
