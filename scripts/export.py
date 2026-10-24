#!/usr/bin/env python3
"""Export only the two implemented pages and their transitive local assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True, type=Path, help='New or empty destination directory')
args = parser.parse_args()
output = args.output.resolve()
if output == ROOT or ROOT.is_relative_to(output):
    parser.error('Choose a separate output directory, not the source or its parent')
if output.exists() and any(output.iterdir()):
    parser.error('Output must be new or empty; existing files will never be deleted')
files = set()


def add_url(url, origin):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return
    target = (origin.parent / unquote(parsed.path)).resolve()
    if target.is_dir():
        target /= 'index.html'
    if not target.is_relative_to(ROOT):
        raise ValueError(f'Local URL escapes source: {url}')
    if not target.is_file():
        raise ValueError(f'Missing dependency: {url} in {origin.relative_to(ROOT)}')
    add_file(target)


class Assets(HTMLParser):
    def __init__(self, origin):
        super().__init__()
        self.origin = origin

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        for attr in ['src', 'href', 'poster']:
            if attrs.get(attr):
                add_url(attrs[attr], self.origin)
        if attrs.get('srcset'):
            for item in attrs['srcset'].split(','):
                add_url(item.strip().split()[0], self.origin)
        if tag == 'meta' and attrs.get('property') == 'og:image':
            # With a final host configured, this absolute URL is not traversed.
            # The local social asset is explicitly included below in either case.
            add_url(attrs.get('content', ''), self.origin)


def add_file(source):
    if source in files:
        return
    files.add(source)
    if source.suffix == '.html':
        Assets(source).feed(source.read_text())
    elif source.suffix == '.css':
        for url in re.findall(r'url\([\'"]?([^\)\'\"]+)', source.read_text()):
            add_url(url, source)


for name in ['index.html', 'our-story/index.html', 'robots.txt', 'sitemap.xml',
             '.nojekyll', 'assets/images/social-preview.jpg',
             'assets/fonts/dmsans-OFL.txt', 'assets/fonts/instrumentserif-OFL.txt']:
    add_file(ROOT / name)
output.mkdir(parents=True, exist_ok=True)
for source in sorted(files):
    target = output / source.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
print(f'Exported {len(files)} files, {sum(f.stat().st_size for f in files):,} bytes to {output}')
print('Only implemented pages and required ReLeaf assets are included. No reference snapshots or QA artifacts.')
