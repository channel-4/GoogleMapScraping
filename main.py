import scraping
import write_csv

# 検索ワード取得
print('-- 検索キーワードを入力してください --')
search_word = input()

# 取得作業
scr = scraping.Scraping(search_word)
obtained_info = scr.getShopInfo()

# SCVに吐き出す
# "{検索ワード}.csv" として出力
write_csv.WriteCsv(search_word, obtained_info)


