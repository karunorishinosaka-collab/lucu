# 毎日の自動更新の手順（クロード用）
1. 新大阪のChromeで https://ajianlucu.thebase.in/ を開き、tools/list.js の中身を実行 → 少し待って window.__L（売っている商品IDのカンマ区切り）を読む（長いので slice で分けて読む）
2. data.json に無いIDがあれば、window.__IDS にそのIDを入れて tools/detail.js を実行 → window.__X を読む（多いときは数件ずつ）
3. live_ids.txt と new_items.json に保存して `python3 tools/update.py live_ids.txt new_items.json`
4. 変わっていれば commit して push（GitHub Pages に自動で反映）
