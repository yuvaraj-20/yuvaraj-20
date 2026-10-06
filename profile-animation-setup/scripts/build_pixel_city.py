"""Build an animated contribution city without third-party Python dependencies."""
import argparse
import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.request

QUERY = '''query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date weekday contributionCount contributionLevel}}}}}}'''
LEVELS = {'NONE': 0, 'FIRST_QUARTILE': 1, 'SECOND_QUARTILE': 2, 'THIRD_QUARTILE': 3, 'FOURTH_QUARTILE': 4}


def fetch_calendar(login):
    token = os.environ.get('GH_TOKEN')
    if not token:
        raise RuntimeError('GH_TOKEN is required. Use the workflow or set it locally.')
    req = urllib.request.Request('https://api.github.com/graphql',
        data=json.dumps({'query': QUERY, 'variables': {'login': login}}).encode(),
        headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json', 'User-Agent': 'pixel-city-profile'})
    with urllib.request.urlopen(req, timeout=45) as response:
        result = json.load(response)
    if result.get('errors'):
        raise RuntimeError('GitHub GraphQL returned errors; check token permissions and username.')
    user = result.get('data', {}).get('user')
    if not user:
        raise RuntimeError('GitHub user not found.')
    return user['contributionsCollection']['contributionCalendar']


def demo_calendar():
    start = dt.date(2025, 10, 5)
    weeks = []
    for week in range(53):
        days = []
        for weekday in range(7):
            seed = (week * 31 + weekday * 47 + week * weekday * 13) % 97
            level = 0 if seed < 47 else 1 + seed % 4
            days.append({'date': str(start + dt.timedelta(days=week * 7 + weekday)),
                'weekday': weekday, 'contributionCount': level * 3, 'contributionLevel': list(LEVELS)[level]})
        weeks.append({'contributionDays': days})
    return {'totalContributions': sum(d['contributionCount'] for w in weeks for d in w['contributionDays']), 'weeks': weeks}


def polygon(points, color):
    return '<polygon points="' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in points) + f'" fill="{color}"/>'


def render(calendar, login, demo=False):
    weeks = calendar['weeks']
    if not weeks or len(weeks) > 54:
        raise ValueError('Expected 1–54 contribution weeks.')
    scale = 1000 / (len(weeks) + 7)
    sy = scale * .36
    def project(x, y):
        return 150 + (x - y) * scale, 150 + (x + y) * sy
    title = 'DEMO DATA — run the workflow to load your contributions' if demo else f'{login} · {calendar["totalContributions"]:,} contributions · rolling year'
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="570" viewBox="0 0 1180 570" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">Animated isometric contribution city. Each tile represents a day; tower height reflects GitHub contribution intensity. Decorative traffic and crane do not represent data.</desc>
<style>
.tower{{transform-box:fill-box;transform-origin:center bottom;animation:rise 2s cubic-bezier(.2,.8,.2,1) both}}
.lamp{{animation:light 5s ease-in-out infinite alternate}}
.hook{{animation:hoist 6s ease-in-out infinite alternate}}
.traffic{{animation:drive 14s linear infinite}}
@keyframes rise{{from{{transform:scaleY(.02)}}to{{transform:scaleY(1)}}}}
@keyframes light{{from{{opacity:.35}}to{{opacity:1}}}}
@keyframes hoist{{from{{transform:translate(0,0)}}to{{transform:translate(45px,22px)}}}}
@keyframes drive{{from{{transform:translate(0,0)}}to{{transform:translate(820px,295px)}}}}
@media(prefers-reduced-motion:reduce){{.tower,.lamp,.hook,.traffic{{animation:none}}}}
</style>
<rect width="1180" height="570" rx="18" fill="#0d1117"/>
<text x="38" y="45" fill="#e6edf3" font-family="sans-serif" font-size="24">PIXEL CITY / NIGHT SHIFT</text>
<text x="38" y="75" fill="#a9b5c1" font-family="sans-serif" font-size="15">{html.escape(title)}</text>''']
    tiles = [(x, day) for x, week in enumerate(weeks) for day in week['contributionDays']]
    tiles.sort(key=lambda item: item[0] + item[1]['weekday'])
    for x, day in tiles:
        y = day['weekday']
        level = LEVELS[day['contributionLevel']]
        px, py = project(x, y)
        a, b = scale * .84, sy * .84
        tooltip = html.escape(f'{day["date"]}: {day["contributionCount"]} contributions')
        out.append(f'<g><title>{tooltip}</title>')
        out.append(polygon([(px, py-b), (px+a, py), (px, py+b), (px-a, py)], ['#172029', '#0e4429', '#006d32', '#26a641', '#39d353'][level]))
        if level:
            bh, bw, bd = 10 + level * 13, scale * .62, sy * .62
            delay = ((x + y) % 12) * .055
            out.append(f'<g class="tower" style="animation-delay:{delay:.3f}s">')
            out.append(polygon([(px-bw, py), (px, py+bd), (px, py+bd-bh), (px-bw, py-bh)], '#29423e'))
            out.append(polygon([(px, py+bd), (px+bw, py), (px+bw, py-bh), (px, py+bd-bh)], '#192f33'))
            out.append(polygon([(px-bw, py-bh), (px, py-bd-bh), (px+bw, py-bh), (px, py+bd-bh)], '#7ee787' if level == 4 else '#51ad75'))
            for floor in range(8, bh-3, 9):
                for side in (-1, 1):
                    out.append(f'<rect class="lamp" x="{px+side*bw*.5:.2f}" y="{py+bd*.4-floor:.2f}" width="2.5" height="3.5" fill="#f0d77b" style="animation-delay:-{(x+y+floor)%5}s"/>')
            out.append('</g>')
        out.append('</g>')
    out.append('''<g stroke="#c59652" fill="none" stroke-width="2"><path d="M805 290V115M813 290V115M775 115H890"/><path d="M805 290l8-15-8-15 8-15-8-15 8-15-8-15 8-15-8-15 8-15-8-15" stroke-width="1"/></g>
<g class="hook"><path d="M843 115v38" stroke="#a9b5c1"/><rect x="837" y="152" width="12" height="12" fill="#7ee787"/></g>
<g class="traffic"><rect x="64" y="230" width="8" height="4" rx="1" fill="#f0d77b"/><rect x="72" y="230" width="2" height="2" fill="#fff3c4"/></g>
<text x="38" y="525" fill="#a9b5c1" font-family="sans-serif" font-size="14">One tile per day · Taller buildings mean higher contribution intensity</text>
<text x="38" y="550" fill="#a9b5c1" font-family="sans-serif" font-size="12">Generated from the GitHub contribution calendar. Native GitHub graph stays unchanged.</text></svg>''')
    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', default='yuvaraj-20')
    parser.add_argument('--output', default='assets/pixel-city.svg')
    parser.add_argument('--demo', action='store_true')
    args = parser.parse_args()
    calendar = demo_calendar() if args.demo else fetch_calendar(args.username)
    svg = render(calendar, args.username, args.demo)
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix('.tmp')
    temporary.write_text(svg, encoding='utf-8')
    temporary.replace(destination)
    print(f'Wrote {destination} ({"DEMO" if args.demo else "GitHub calendar"})')


if __name__ == '__main__':
    main()
