#!/usr/bin/env python3
"""Re-port upstream pstack (cursor/plugins) to Claude Code.
Usage: python3 -I tools/port.py <upstream-pstack-dir> <output-dir>
"""
import pathlib, shutil, sys, json, subprocess
HERE=pathlib.Path(__file__).resolve().parent
def main(src, dst):
    src=pathlib.Path(src).resolve(); dst=pathlib.Path(dst).resolve()
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src, dst)
    for junk in ['.cursor-plugin','automations','plugin.json','.gitignore']:
        p=dst/junk
        if p.is_dir(): shutil.rmtree(p)
        elif p.exists(): p.unlink()
    version=json.loads((src/'plugin.json').read_text()).get('version','0.0.0')
    (dst/'.claude-plugin').mkdir(exist_ok=True)
    (dst/'.claude-plugin/plugin.json').write_text(json.dumps({
      "name":"pstack","version":version,
      "description":"if you want to go fast, go deep first. pstack helps you write less, but higher quality code. rigorous agent workflows you can parallelize with confidence.",
      "author":{"name":"Lauren Tan"},
      "homepage":"https://github.com/cursor/plugins/tree/main/pstack",
      "repository":"https://github.com/cursor/plugins","license":"MIT",
      "keywords":["pstack","poteto-mode","workflow","principles","subagents","unslop"]},indent=2)+"\n")
    for step in ['sweep1.py','sweep2.py','sweep3.py','rewrite.py','final.py']:
        subprocess.run([sys.executable,'-I',str(HERE/step),str(dst)],check=True,stdout=subprocess.DEVNULL)
    print(f"ported {src} -> {dst} (upstream version {version})")
if __name__=='__main__':
    main(sys.argv[1], sys.argv[2])
