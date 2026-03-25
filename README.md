# 🔍 PROJECT ZERO — WEEK 4

# Tech0 Search v1.0 — アプリ実行ガイド

---

## 📁 このフォルダに含まれるファイル

```
v1.0/
├── app.py           # Streamlit アプリ本体（完成版）
├── database.py      # SQLite DB 操作モジュール
├── ranking.py       # TF-IDF 検索エンジン（SearchEngine クラス）
├── crawler.py       # Web クローラー
├── schema.sql       # DB テーブル定義
├── requirements.txt # 依存ライブラリ一覧
└── README.md        # このファイル
```

> ⚠️ **重要**：初回起動時は DB が空の状態です。
> クローラータブからURLをクロールしてデータを登録してください。

---

## 🚀 セットアップ手順

### 1. ライブラリをインストールする

```bash
pip install -r requirements.txt
```

### 2. アプリを起動する

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` が開けば成功です。

### 3. データを登録する

初回起動時は DB にデータがありません。以下の手順でデータを登録してください。

1. 「🤖 クローラー」タブを開く
2. クロールしたいURLを入力して「クロール実行」
3. 「💾 全てインデックスに登録」ボタンで保存

または、`w4_tech0_search_v1.0.ipynb` の Step 4 を実行すると
`data/tech0_search.db` が生成されます。生成後にこのフォルダで
`streamlit run app.py` を起動してください。

---

## 🏗️ アーキテクチャ

```
app.py
 ├── database.py    ← SQLite CRUD（init_db / insert_page / get_all_pages / log_search）
 ├── ranking.py     ← TF-IDF 検索エンジン（SearchEngine クラス）
 └── crawler.py     ← Web クローラー（crawl_url 関数）
```

**データの流れ：**

```
URL → crawler.py → database.py → data/tech0_search.db
                                        ↓
                               ranking.py（TF-IDF インデックス構築）
                                        ↓
                               app.py（検索 → 結果表示）
```

---

## 📖 タブ構成

| タブ          | 機能                                                                      |
| ------------- | ------------------------------------------------------------------------- |
| 🔍 検索       | キーワードで TF-IDF 検索。メダル表示＋スコア2種（relevance / base）を表示 |
| 🤖 クローラー | URL を指定してページをクロールし DB に登録する                            |
| 📋 一覧       | DB に登録されている全ページを折りたたみ表示                               |

> 💡 統計機能（検索ログの可視化）は **Step 7 発展課題** でチャレンジ可能です。

---

## ⚠️ よくあるエラーと対処法

### `ModuleNotFoundError: No module named 'sklearn'`

```bash
pip install scikit-learn
```

### `FileNotFoundError: schema.sql`

`schema.sql` が `app.py` と同じフォルダにあるか確認してください。

### 検索結果が表示されない

DB にデータが登録されていません。クローラータブからURLをクロールして登録してください。

### インデックスが再構築されない（新しく登録したページが検索に出ない）

サイドバーの「🔄 インデックスを更新」ボタンを押してください。
または Streamlit の「⋮」メニューから「Clear cache」を選択して再起動してください。

---

## 📚 参考リンク

| リソース                     | URL                                                                                                    |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| Streamlit API リファレンス   | https://docs.streamlit.io/develop/api-reference                                                        |
| scikit-learn TfidfVectorizer | https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html |
| SQLite ドキュメント          | https://www.sqlite.org/lang.html                                                                       |

---

_Tech0 BootCamp 12期 | WEEK 4 — PROJECT ZERO 指令：Tech0 Search v1.3_
