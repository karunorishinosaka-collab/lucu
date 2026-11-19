# 新着のお知らせ（ルチュLINEの一斉配信）の下書きを作る道具（2週間に1回・月曜お昼12時に送る）
#   python3 tools/notice.py draft   … 下書きの文章（吹き出し3つ）を notice_draft.txt に書く
#   python3 tools/notice.py sent    … お知らせを送ったあとに実行（前回の日付を今日にして、ためた新着を空にする）
# ※ 配信そのものは、今前田さんの○をもらってから送る（自動では送らない）
import json, sys, datetime
URL = 'https://karunorishinosaka-collab.github.io/lucu/'
FREE_DAY = datetime.date(2027, 1, 1)
today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()
news = json.load(open('tools/news.json', encoding='utf-8'))
if sys.argv[1:] == ['sent']:
    news['last_notice'] = today.isoformat(); news['pending'] = []
    json.dump(news, open('tools/news.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('お知らせ済みにしました', today); sys.exit()
items = {i['id']: i for i in json.load(open('data.json', encoding='utf-8'))['items']}
new = [items[i] for i in news['pending'] if i in items]
if not new: sys.exit('まだ知らせていない新着はありません')
new.sort(key=lambda i: int(i['id']), reverse=True)
lines = '\n'.join('・%s（¥%s）' % (i['n'], i['p']) for i in new[:5])
more = '\nほか%d点' % (len(new) - 5) if len(new) > 5 else ''
free = '8,000円' if today < FREE_DAY else '1万円'
b1 = ('【新着】アジアン雑貨ルチュに、新しい服と雑貨が%d点入りました\n\n%s%s\n\n↓写真は「ルチュ かんたんLINEショップ」で見られます（「新着」のボタンを押すとすぐ出ます）\n%s'
      % (len(new), lines, more, URL))
b2 = ('ほしい物があったら、緑の「これ欲しい」を押して、LINEで「送信」するだけです。\n'
      'インスタグラムやウェブショップの登録はいりません。お取り置きもできます。\n'
      '送料は全国600円（小さい物は250円）、%s以上で送料無料です。' % free)
b3 = '柄は1枚ずつちがうので、気になる物はお早めにどうぞ。\nこれからもアジアン雑貨ルチュをよろしくお願いいたします。'
out = '\n\n'.join(['【吹き出し①】\n' + b1, '【吹き出し②】\n' + b2, '【吹き出し③】\n' + b3])
open('notice_draft.txt', 'w', encoding='utf-8').write(out)
print(out)
