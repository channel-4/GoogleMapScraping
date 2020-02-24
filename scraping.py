from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class Scraping:

    def __init__(self, search_word, tries = 0):
        self.search_word = search_word
        self.shop_info = [['店名', '住所', '電話番号']]
        self.driver = webdriver.Chrome()

    def getShopPanels(self, tries=0):
        # 2ページ目以降の場合はページ内読み込みになるのでsleepで読み込み時間を確保
        sleep(1)

        try:
            panels = self.driver.find_elements_by_class_name('dbg0pd')
        except NoSuchElementException as e:
            # もし取得できずにエラーになった場合は、3回までやり直しする
            if tries < 3 :
                tries += 1
                return self.getShopPanels(self, tries)
            else :
                print(e)
        else:
            # うまく取得できた場合
            return panels

    def getTextContent(self, class_name, tries=0):
        # モーダルが開くまでラグがあるので1秒待つ
        sleep(1)

        text = ''
        try:
            title_list = self.driver.find_elements_by_class_name(class_name)
            # class取得なので配列の頭を取得
            if len(title_list) > 0:
                text = title_list[0].text
        except StaleElementReferenceException as e:
            # 読み込み不足の可能性があるので最大3回までやり直す
            if tries < 3:
                tries += 1
                return self.getShopPanels(self, tries)
            else:
                print(e)

        # 空もしくはNoneの場合は存在無し
        if text == '' or text is None:
            return 'データ無し'
        else:
            return text

    def getShopInfo(self):
        # search_wordでGoogle検索
        self.driver.get('https://www.google.com/search?q=' + self.search_word)

        # 「さらに表示」が出たらクリック
        # TODO さらに表示が出ない時のエラー処理
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'i0vbXd')))
        self.driver.find_element_by_link_text('さらに表示').click()

        # MAPページが完全に出るまで待つ
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located)

        # 最後のページになるまでループを回す
        middle_page = True
        while middle_page:
            # MAP左袖の各店舗のdiv要素(= ここではパネルとする)を取得
            shop_panels = self.getShopPanels()

            # 各店舗のパネルをクリック => 出てきたモーダルから情報取得
            for each_shop in shop_panels:
                each_shop.click()

                name    = self.getTextContent('kno-ecr-pt')
                address = self.getTextContent('LrzXr')
                tel_num = self.getTextContent('zdqRlf')

                self.shop_info.append([name, address, tel_num])

            # 閉じるボタンクリック
            self.driver.find_element_by_class_name('QU77pf').click()

            try:
                # 「次へ」ボタン
                next_link = self.driver.find_element_by_id('pnnext')
            except NoSuchElementException:
                # 次へのボタンがない場合は最終ページと判断し、エラーを握り潰してwhileから抜ける
                middle_page = False
            else:
                # 「次へ」ボタンをクリックしてマップ更新
                next_link.click()

        # ブラウザ閉じる
        self.driver.close()
        self.driver.quit()

        # 配列に情報が溜まったので返す
        return self.shop_info