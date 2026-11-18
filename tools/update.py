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
for x in new:
    if not x.get('n'): continue
    c = cats.get(x['id']) or guess(x['n']); cats[x['id']] = c
    have[x['id']] = {'id': x['id'], 'n': x['n'], 'p': x['p'], 'o': x.get('off', ''), 'c': c, 'd': x.get('d', ''),
                     'ph': x.get('ph', []), 'v': [re.sub(r'[\s　]+', ' ', s).strip() for s in x.get('v', [])]}
missing = [i for i in live if i not in have]
items = [have[i] for i in live if i in have]
items.sort(key=lambda i: int(i['id']), reverse=True)
removed = len(data['items']) - len([i for i in data['items'] if i['id'] in set(live)])
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
data = {'made': now.strftime('%Y-%m-%d %H:%M'), 'items': items}
json.dump(data, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(cats, open('tools/cats.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('掲載', len(items), '件 / 売り切れで外した', removed, '件 / 新しく追加', len(new), '件 / 情報が足りないID', ','.join(missing) or 'なし')
