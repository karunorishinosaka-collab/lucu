# 毎日の更新：リポジトリの一番上のフォルダで  python3 tools/update.py live_ids.txt [new_items.json]
#  live_ids.txt  = 今売っている商品のID（カンマ区切り。list.js の結果）
#  new_items.json = 新しく出た商品のくわしい情報（detail.js の結果）
import json, sys, re, datetime
def guess(n):
    if re.search(r'スカート', n): return 'skirt'
    if re.search(r'パンツ|サルエル|サロペット|オーバーオール|ズボン', n): return 'pants'
    if re.search(r'ワンピ|ドレス', n): return 'one'
    if re.search(r'バッグ|バック|ポーチ|リュック|サコッシュ|財布|ショルダー', n): return 'bag'
    if re.search(r'ピアス|イヤリング|ブレス|ネックレス|帽子|ハット|キャップ|マット|ストール|マフラー|ソックス|靴下|お香|リング|ヘア|キーホルダー|マスク', n): return 'goods'
    return 'tops'
data = json.load(open('data.json', encoding='utf-8'))
cats = json.load(open('tools/cats.json', encoding='utf-8'))
live = [x for x in open(sys.argv[1], encoding='utf-8').read().strip().split(',') if x.strip()]
if len(live) < 50:
    sys.exit('売っている商品が少なすぎます（%d件）。読み込みに失敗した可能性があるので更新しません' % len(live))
new = json.load(open(sys.argv[2], encoding='utf-8')) if len(sys.argv) > 2 else []
have = {i['id']: i for i in data['items']}
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
today = now.strftime('%Y-%m-%d')
added = []
for x in new:
    if not x.get('n'): continue
    c = cats.get(x['id']) or guess(x['n']); cats[x['id']] = c
    have[x['id']] = {'id': x['id'], 'n': x['n'], 'p': x['p'], 'o': x.get('off', ''), 'c': c, 'd': x.get('d', ''),
                     'ph': x.get('ph', []), 'v': [re.sub(r'[\s　]+', ' ', s).strip() for s in x.get('v', [])]}
    if x['id'] not in {i['id'] for i in data['items']}:
        have[x['id']]['a'] = today   # 載せた日（7日間「NEW」の印が出る）
        added.append(x['id'])
missing = [i for i in live if i not in have]
items = [have[i] for i in live if i in have]
items.sort(key=lambda i: int(i['id']), reverse=True)
removed = len(data['items']) - len([i for i in data['items'] if i['id'] in set(live)])
data = {'made': now.strftime('%Y-%m-%d %H:%M'), 'items': items}
json.dump(data, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(cats, open('tools/cats.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
# 新着のお知らせ用：まだお客様に知らせていない新着をためておく（tools/news.json）
try: news = json.load(open('tools/news.json', encoding='utf-8'))
except FileNotFoundError: news = {'last_notice': None, 'pending': []}
liveset = set(live)
news['pending'] = [i for i in news['pending'] if i in liveset] + [i for i in added if i not in news['pending']]
json.dump(news, open('tools/news.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# お母さんの希望（20261119）：2週間に1回・新商品が入った時だけ・月曜のお昼12時に送る
# → 前回のお知らせの週の月曜から2週間後の月曜から送れる
d = now.date()
if news['last_notice']:
    last = datetime.date.fromisoformat(news['last_notice'])
    next_ok = last - datetime.timedelta(days=last.weekday()) + datetime.timedelta(days=14)
else:
    next_ok = d - datetime.timedelta(days=d.weekday())
due = bool(news['pending']) and d.weekday() == 0 and d >= next_ok
print('掲載', len(items), '件 / 売り切れで外した', removed, '件 / 新しく追加', len(added), '件 / 情報が足りないID', ','.join(missing) or 'なし')
print('まだ知らせていない新着', len(news['pending']), '件 / 前回のお知らせ', news['last_notice'] or 'まだなし',
      '/ お知らせの下書きを作る日', 'はい' if due else 'いいえ（次に送れる月曜 %s）' % max(next_ok, d + datetime.timedelta(days=(7 - d.weekday()) % 7)))
