# 毎日の自動更新の手順（クロード用）
1. 新大阪のChromeで https://ajianlucu.thebase.in/ を開き、tools/list.js の中身を実行 → 少し待って window.__L（売っている商品IDのカンマ区切り）を読む（長いので slice で分けて読む）
2. data.json に無いIDがあれば、window.__IDS にそのIDを入れて tools/detail.js を実行 → window.__X を読む（多いときは数件ずつ）
3. live_ids.txt と new_items.json に保存して `python3 tools/update.py live_ids.txt new_items.json`
4. 変わっていれば commit して push（GitHub Pages に自動で反映）
5. update.py の最後の行が「お知らせの下書きを作る日 はい」のときだけ（月曜日だけ「はい」になります）：`python3 tools/notice.py draft` で下書き（吹き出し3つ）を作る
   → ルチュのLINE公式アカウント管理画面（manager.line.biz/account/@212nahsk）の「メッセージを作成」に吹き出し3つを入れて「下書き保存」（配信はしない）
   → 今前田さんに下書きの文章を見せて、○×で送ってよいか聞く
   → ○をもらったら、その日の「お昼12:00」の予約配信にする（12時を過ぎてから○が来たら、「今すぐ送る／来週の月曜12時」を聞く）。予約できたら `python3 tools/notice.py sent` を実行して commit・push
   ※ 新着のお知らせのルール（お母さんの希望 20261119）：2週間に1回・新商品が入った時だけ・月曜日のお昼12時
   ※ 前回のお知らせの週の月曜から2週間たった月曜から送れる（例：11/18に送った → 次は11/30（月））
