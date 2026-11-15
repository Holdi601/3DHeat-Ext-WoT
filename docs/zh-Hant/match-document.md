---
title: "對應文件"
nav_order: 6
lang: zh-Hant
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# 對應文件 {#the-match-document}

`<match>.match.json` 保存了回放所記錄、但不屬於表格中任何一列的所有內容。檢視器的對戰分頁會讀取它。（程式碼稱它為摘要。）

![合成對應文件的開頭，以及它的鍵](../assets/img/match-document.svg)

## 戰鬥 {#the-battle}

| 鍵 | 內容 |
|---|---|
| `format`、`version` | `heat3d-wot-match`、`2` |
| `game`、`match`、`map`、`mapName` | `World of Tanks`；戰鬥的 id；地圖的 id 及其顯示名稱 |
| `clientVersion`、`streamVersion` | 標頭中的遊戲版本，以及封包串流所示的版本 |
| `recorded` | 回放錄製的時間，依遊戲的寫法 |
| `player`、`vehicle` | 錄製玩家及其坦克 |
| `battleType`、`gameplay`、`server`、`region`、`hasMods` | 標頭中的戰鬥類型編號、遊戲模式、伺服器、地區，以及是否安裝了模組 |
| `duration` | 戰鬥的長度（秒），取自結算 |
| `winnerTeam`、`finishReason` | 獲勝隊伍，以及遊戲對戰鬥結束方式的編號，取自結算 |
| `complete`、`truncated` | 結算在回放中；錄製提前停止 |
| `battleStart`、`battleStartFrom`、`firstMovement` | 戰鬥在錄製中的開始秒數；`arena`（戰場如此表示）或 `movement`（任何坦克第一次移動的時刻）；該次第一次移動 |
| `recordingSeconds` | 錄製的長度（秒） |
| `positionPacket`、`hz`、`positions` | 位置所在的封包編號、每秒取樣數、位置列 |
| `events` | 表格中每種事件的列數 |
| `units` | `metres; x east, y up, z north`（公尺；x 朝東、y 向上、z 朝北） |
| `decoded` | 每一類訊息所找到的方法與封包編號 |

## 玩家與事件 {#players-and-events}

| 鍵 | 內容 |
|---|---|
| `players` | 每輛坦克一筆：名稱、隊伍、坦克、戰隊、取樣數、擊殺、造成的傷害、是否存活、存活時間；`seen`（錄製客戶端看到的射擊與傷害）；標頭與結算中的完整項目，以及帳號 |
| `kills` | 每次陣亡：時間（秒）、時間的來源（`arena`、`health` 或 `lifeTime`）、受害者、擊殺者、原因編號與名稱 |
| `periods` | 戰鬥的時段（等待、戰前、戰鬥、戰後），附伺服器的結束時間 |
| `basePoints` | 每個隊伍與每個基地的基地佔領進度 |
| `chat`、`commands` | 聊天行；戰鬥聊天指令及其所有引數 |
| `camera`、`clientEvents` | 錄製玩家的攝影機模式；錄製客戶端對自身的紀錄（縮放、自動瞄準、目標變更、載具狀態） |
| `arenaUpdates` | 每一次戰場更新，已解碼，與遊戲送出的內容相同 |

## 結算與檢查 {#results-and-checks}

| 鍵 | 內容 |
|---|---|
| `serverSettings` | 標頭中的伺服器設定 |
| `results`、`resultVehicles`、`frags` | 結算畫面：共通、個人（附每個目標的詳細資料）、玩家、帳號；每輛坦克的結算行；每位玩家的擊殺數 |
| `entities` | 串流建立的每個實體：其類型編號與角色、何時進入客戶端的視野、何時離開 |
| `selfCheck` | 完整性計數（[完整性](completeness.md)），以及實體與版本的檢查 |

---

屬於 [3DHeat](https://github.com/Holdi601/3DHeat)（[說明文件](https://holdi601.github.io/3DHeat/)）的一部分。來源：[3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT)。
