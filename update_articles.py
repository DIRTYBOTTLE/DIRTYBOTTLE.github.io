#!/usr/bin/env python3
import os, json, re
from datetime import datetime

ARTICLES_DIR = 'articles'
JSON_PATH = os.path.join(ARTICLES_DIR, 'articles.json')


def extract_metadata(path):
    title = None
    summary = ''
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if title is None:
                m = re.match(r"^#\s+(.*)", line)
                if m:
                    title = m.group(1).strip()
                    continue
            if line.strip():
                summary = line.strip()
                break
    if title is None:
        title = os.path.splitext(os.path.basename(path))[0]
    mtime = os.path.getmtime(path)
    date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    return {
        'title': title,
        'filename': os.path.basename(path),
        'date': date,
        'summary': summary
    }


def main():
    entries = []
    for fname in os.listdir(ARTICLES_DIR):
        if fname.lower().endswith('.md'):
            full = os.path.join(ARTICLES_DIR, fname)
            entries.append(extract_metadata(full))
    # sort by date desc
    entries.sort(key=lambda x: x['date'], reverse=True)
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f'Updated {JSON_PATH} with {len(entries)} entries.')


if __name__ == '__main__':
    main()
