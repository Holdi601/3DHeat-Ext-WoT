---
title: "完整性"
nav_order: 8
lang: zh-Hant
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# 完整性 {#completeness}

回放中沒有任何東西會被丟棄。轉換器讀取的內容會放入表格與對戰文件；其他每個項目都會完整保存在附屬檔案 `<match>.messages.parquet` 中；而對戰文件中的 `selfCheck.completeness` 會計算每一類項目的去向。這是所有 3DHeat 轉換器共同遵守的規則：[轉換器保留一切](https://holdi601.github.io/3DHeat/converters.html)。

![合成回放的自我檢查：每個看到、讀取、保留或遺失的項目](../assets/img/completeness.svg)

## 計數 {#the-count}

對於每一類項目，`selfCheck.completeness.types` 提供以下數字：

| 計數 | 意義 |
|---|---|
| `seen` | 回放中有多少個 |
| `decoded` | 完整讀取 |
| `partial` | 部分讀取，並完整保存在附屬檔案中 |
| `raw` | 只完整保存在附屬檔案中，未讀取 |
| `lost` | 遺失：永遠為 `0` |

類別來自回放本身：`block 0`（標頭）、`block 1`（結算）、`container sizes` 與 `deflate tail`（容器本身的位元組）、`packet <type>`，以及對實體的呼叫：`method <entity type>.<number>` 與 `property <entity type>.<number>`。實體類型是建立封包所給的編號；`selfCheck.entities.roles` 說明哪一個是錄製玩家的化身，哪些是載具。無人知道的類別會以其計數出現。

## 附屬檔案 {#the-sidecar}

| 欄位 | 內容 |
|---|---|
| `time` | 回放的時鐘，與表格相同 |
| `type`、`name` | 項目的類別；轉換器如何稱呼它，以及它在哪裡被讀取 |
| `entity` | 它所屬的載具或化身，與表格的 `entity` 相同 |
| `decoded` | 讀取到的內容，以 JSON 表示 |
| `payload`、`text` | 其位元組，完整保存；JSON 區塊，完整保存 |
| `entityType`、`packet`、`method` | 編號 |

列依封包、方法、實體與時間排序。

## 讀取了什麼，以及如何核對 {#what-is-read-and-how-it-was-checked}

- **每個位置的俯仰與橫滾：**俯仰是坦克自己向前行駛時路徑斜率的負值；在同一地點、航向相同的兩輛坦克有相同的橫滾，航向相反則橫滾相反。
- **實體**（`entities`）：每個實體何時進入客戶端的視野、何時離開。坦克在離開與再次出現之間，沒有任何位置。
- **串流中的版本**（`streamVersion`）：與標頭的版本相同。
- **錄製玩家的瞄準**（封包 38）：一個方向，記錄在附屬檔案的 `decoded`（`forward`）中；在玩家開火的時刻，它與砲彈飛行的方向相差不到一度的幾分之一。

其餘讀取到的內容（血量、命中、射擊、曳光彈、爆炸、砲管角度、戰場更新、聊天、攝影機模式、客戶端事件、位置）都是 `partial`：會出現在表格或對戰文件中，並完整保存在附屬檔案中。

**保留但未讀取**（`raw`）的主要類別：不在表格中的位置更新（化身的、坦克陣亡後的、不在名單中的實體）、封包 26、28、29、31、36、50、54 與 57、一些頻繁出現的載具與化身屬性，以及每個沒有讀取器的方法與屬性（其中包括模組損傷、組員與消耗品），還有實體建立的屬性。

## 無法取得的內容 {#not-available}

- 伺服器從未送給錄製客戶端的資料：其他玩家的瞄準、攝影機與操作，以及未被發現時的敵人。回放只是一個客戶端被告知的內容。
- 實體類型、方法與屬性的名稱：它們在遊戲的定義檔案中，而不在回放裡。編號會被保留。
- 以度為單位的砲管仰角，以及任何需要遊戲檔案中坦克自身資料的其他內容。

---

屬於 [3DHeat](https://github.com/Holdi601/3DHeat)（[說明文件](https://holdi601.github.io/3DHeat/)）的一部分。來源：[3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT)。
