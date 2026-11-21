#!/usr/bin/env python3
"""Сборка страницы тура «Исландия лето 2027».
Запуск: python3 src/build.py [--public]
Без --public страница помечена для поисковиков «не индексировать» (пилот)."""
import json, sys, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
BASE = 'https://iceland2027.klotstravel.com/'


def figs(prefix, n, alt):
    return ''.join(f'<figure><img src="img/{prefix}{i:02d}.jpg" alt="{alt}" loading="lazy"></figure>' for i in range(1, n + 1))


def reviews():
    out = []
    for i, r in enumerate(json.loads((SRC / 'reviews.json').read_text(encoding='utf-8')), 1):
        out.append(
            f'<article class="rev"><div class="who"><img src="img/avatars{i:02d}.jpg" alt="" loading="lazy">'
            f'<div><b>{html.escape(r["name"])}</b><span>{html.escape(r["year"])}</span></div></div>'
            f'<div class="body">{r["text"]}</div><button class="more" type="button">Читать полностью</button></article>')
    return ''.join(out)


def program():
    days = json.loads((SRC / 'program.json').read_text(encoding='utf-8'))
    return ''.join(f'<div class="day"><b>День {i}:</b>{t}</div>' for i, t in enumerate(days, 1))


def main():
    public = '--public' in sys.argv
    t = (SRC / 'template.html').read_text(encoding='utf-8')
    rep = {
        '{{ROBOTS}}': 'index, follow' if public else 'noindex, nofollow',
        '{{BASE}}': BASE,
        '{{STRIP1}}': figs('strip1', 4, 'Исландия'),
        '{{STRIP2}}': figs('strip2', 4, 'Исландия'),
        '{{FUN}}': figs('fun', 8, 'Наши поездки в Исландию'),
        '{{HOUSE}}': figs('house', 8, 'Дом, где мы живем'),
        '{{FINAL}}': figs('final', 4, 'Исландия'),
        '{{REVIEWS}}': reviews(),
        '{{PROGRAM}}': program(),
    }
    for k, v in rep.items():
        t = t.replace(k, v)
    assert '{{' not in t, 'остались незаполненные места'
    (ROOT / 'index.html').write_text(t, encoding='utf-8')
    (ROOT / 'CNAME').write_text('iceland2027.klotstravel.com', encoding='utf-8')
    (ROOT / '.nojekyll').write_text('', encoding='utf-8')
    if not public:
        (ROOT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
    elif (ROOT / 'robots.txt').exists():
        (ROOT / 'robots.txt').unlink()
    print('ok', 'public' if public else 'pilot (noindex)', round(len(t.encode()) / 1024), 'KB')


if __name__ == '__main__':
    main()
