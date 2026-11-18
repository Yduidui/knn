# -*- coding: utf-8 -*-
"""一道题一条命令：打包 starter、生成二维码、输出清单。

用法
----
    python scripts/build.py            # 处理全部题目
    python scripts/build.py 4-5        # 只处理指定题号

生成物
------
    p/<id>/starter.zip          学生下载包
    assets/qr/<id>.svg          矢量二维码（出书用）
    assets/qr/<id>.png          高分辨率位图（Word 排版用）
    manifest.csv                全量清单（题号 / URL / 校验结果）
"""
import csv
import json
import shutil
import sys
import zipfile
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

import segno

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))

IGNORE = {"__pycache__", ".pytest_cache", ".ipynb_checkpoints", ".git"}
IGNORE_SUFFIX = {".pyc", ".pyo"}


def sync_starter(prob_dir, meta):
    """把 starter 源目录同步到站点路径，让学生 clone 后可直接运行。"""
    src = prob_dir / "starter"
    dst = ROOT / meta["path"].strip("/") / "starter"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src, dst,
        ignore=shutil.ignore_patterns(*IGNORE, *IGNORE_SUFFIX, ".DS_Store", "Thumbs.db"),
    )
    n = sum(1 for _ in dst.rglob("*") if _.is_file())
    print(f"  starter/    已同步 {n} 个文件")


def find_problems(only=None):
    out = []
    for meta_path in sorted(ROOT.glob("exercises/*/*/meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if only and meta["id"] != only:
            continue
        out.append((meta_path.parent, meta))
    return out


def make_zip(prob_dir, meta):
    starter = prob_dir / "starter"
    target = ROOT / meta["assets"]["starter"]
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(starter.rglob("*")):
            if not f.is_file():
                continue
            if IGNORE & set(f.parts) or f.suffix in IGNORE_SUFFIX:
                continue
            if f.name in {".DS_Store", "Thumbs.db"}:
                continue
            z.write(f, f.relative_to(starter))
    size = target.stat().st_size
    print(f"  starter.zip  {size/1024:.1f} KB")
    return size


def make_qr(meta):
    url = f"{CFG['base_url'].rstrip('/')}/{meta['path'].strip('/')}/"
    qcfg = CFG["qr"]
    qr = segno.make(url, error=qcfg["error_level"])
    out = ROOT / "assets/qr"
    out.mkdir(parents=True, exist_ok=True)

    svg = out / f"{meta['id']}.svg"
    qr.save(svg, kind="svg", border=qcfg["border_modules"], dark="#000000", light=None)

    png = out / f"{meta['id']}.png"
    modules = qr.symbol_size(border=qcfg["border_modules"])[0]
    scale = max(4, round(qcfg["png_target_px"] / modules))
    qr.save(png, kind="png", border=qcfg["border_modules"], scale=scale)

    print(f"  QR 版本 {qr.version}  模块 {modules}x{modules}  "
          f"PNG {png.stat().st_size//1024} KB")
    print(f"  URL: {url}")
    if "YOURNAME" in url:
        print("  [警告] config.json 里的 base_url 还是占位符，拿到真实地址后改一行重跑")
    return url, svg, png


def check(url):
    try:
        req = Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=8) as r:
            return r.status
    except URLError as e:
        return f"不可达({e.reason})"
    except Exception as e:  # noqa: BLE001
        return f"异常({e})"


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    rows = []
    for prob_dir, meta in find_problems(only):
        print(f"\n[{meta['id']}] {meta['title']}")
        sync_starter(prob_dir, meta)
        size = make_zip(prob_dir, meta)
        url, svg, png = make_qr(meta)
        status = check(url)
        print(f"  链接状态: {status}")
        rows.append({
            "题号": meta["id"],
            "题型": meta["type"],
            "标题": meta["title"],
            "URL": url,
            "二维码SVG": str(svg.relative_to(ROOT)).replace("\\", "/"),
            "二维码PNG": str(png.relative_to(ROOT)).replace("\\", "/"),
            "starter大小KB": round(size / 1024, 1),
            "链接状态": status,
        })

    if rows:
        out = ROOT / "manifest.csv"
        with out.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"\n清单已写入 {out.name}（{len(rows)} 道题）")


if __name__ == "__main__":
    main()
