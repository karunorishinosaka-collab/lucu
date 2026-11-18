# ルチュ商品ページ用データを作る（ウェブショップから読んだ raw.json → data.json）
import json, re, sys, datetime
raw = json.load(open(sys.argv[1], encoding='utf-8'))
cats = json.load(open('tools/cats.json', encoding='utf-8'))
FALLBACK = {'27108395': ['9ee013c104675304c0d6fbfb789c56c0.jpg']}
def guess(n):
    if re.search(r'スカート', n): return 'skirt'
    if re.search(r'パンツ|サルエル|サロペット|オーバーオール|ズボン', n): return 'pants'
    if re.search(r'ワンピ|ドレス', n): return 'one'
    if re.search(r'バッグ|バック|ポーチ|リュック|サコッシュ|財布|ショルダー', n): return 'bag'
    if re.search(r'ピアス|イヤリング|ブレス|ネックレス|帽子|ハット|キャップ|マット|ストール|マフラー|ソックス|靴下|お香|リング|ヘア|キーホルダー|マスク', n): return 'goods'
    return 'tops'
items = []
for x in raw['items']:
    if x.get('err') or not x.get('n'): continue
    c = cats.get(x['id']) or guess(x['n'])
    cats[x['id']] = c
    ph = x.get('ph') or FALLBACK.get(x['id'], [])
    v = [re.sub(r'[\s　]+', ' ', s).strip() for s in x.get('v') or []]
    items.append({'id': x['id'], 'n': x['n'], 'p': x['p'], 'o': (x.get('off') or ''), 'c': c, 'd': x.get('d', ''), 'ph': ph, 'v': v})
items.sort(key=lambda i: int(i['id']), reverse=True)
made = datetime.datetime.fromisoformat(raw['made'].replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=9)))
json.dump({'made': made.strftime('%Y-%m-%d %H:%M'), 'items': items}, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(cats, open('tools/cats.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('items', len(items), 'photos', sum(len(i['ph']) for i in items))
