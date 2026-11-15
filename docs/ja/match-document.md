---
title: マッチドキュメント
nav_order: 6
lang: ja
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# マッチドキュメント {#the-match-document}

`<match>.match.json` には、テーブルの行にはならない、リプレイが伝えるすべてのことが入っています。ビューアの Match タブがこれを読みます。（コードではこれを要約（summary）と呼んでいます。）

![合成したマッチドキュメントの冒頭と、そのキー](../assets/img/match-document.svg)

## 戦闘 {#the-battle}

| キー | 内容 |
|---|---|
| `format`、`version` | `heat3d-wot-match`、`2` |
| `game`、`match`、`map`、`mapName` | `World of Tanks`。戦闘の ID。マップの ID とその表示名 |
| `clientVersion`、`streamVersion` | ヘッダーにあるゲームのバージョン。パケットの流れが示すバージョン |
| `recorded` | リプレイが録画された時刻。ゲームが書いたとおり |
| `player`、`vehicle` | 録画しているプレイヤーと、その戦車 |
| `battleType`、`gameplay`、`server`、`region`、`hasMods` | ヘッダーの戦闘タイプの番号、ゲームモード、サーバー、地域、そして MOD が入っていたかどうか |
| `duration` | 戦闘の長さ（秒）。結果から |
| `winnerTeam`、`finishReason` | 勝ったチーム、およびゲームが戦闘の終わり方に付けた番号。結果から |
| `complete`、`truncated` | 結果がリプレイに入っている。録画が早く止まった |
| `battleStart`、`battleStartFrom`、`firstMovement` | 録画の中での戦闘の開始（秒）。`arena`（アリーナがそう示した）または `movement`（どの戦車かが最初に動いた瞬間）。その最初の動き |
| `recordingSeconds` | 録画の長さ（秒） |
| `positionPacket`、`hz`、`positions` | 位置が届いたパケットの番号、1 秒あたりのサンプル数、位置の行の数 |
| `events` | 各イベントのテーブルの行の数 |
| `units` | `metres; x east, y up, z north`（メートル。x は東、y は上、z は北） |
| `decoded` | メッセージの種類ごとに見つかったメソッドとパケットの番号 |

## プレイヤーとイベント {#players-and-events}

| キー | 内容 |
|---|---|
| `players` | 戦車 1 台につき 1 つの項目: 名前、チーム、戦車、クラン、サンプル数、キル、与えたダメージ、生存、生存時間。`seen`（録画したクライアントが見た射撃とダメージ）。ヘッダーと結果の項目の全体、そしてアカウントのもの |
| `kills` | すべての死亡: 時刻（秒）、時刻の出どころ（`arena`、`health`、`lifeTime`）、犠牲者、キラー、理由の番号と名前 |
| `periods` | 戦闘の期間（待機、戦闘前、戦闘、戦闘後）と、サーバーの終了時刻 |
| `basePoints` | チームと基地ごとの、基地の占領の進み具合 |
| `chat`、`commands` | チャットの行。バトルチャットのコマンドとそのすべての引数 |
| `camera`、`clientEvents` | 録画しているプレイヤーのカメラのモード。クライアントが自分について記録したこと（ズーム、自動照準、目標の変更、車両の状態） |
| `arenaUpdates` | アリーナの更新のすべて。読まれたもの。ゲームが送ったとおり |

## 結果と確認 {#results-and-checks}

| キー | 内容 |
|---|---|
| `serverSettings` | ヘッダーにあるサーバーの設定 |
| `results`、`resultVehicles`、`frags` | 結果の画面: 共通、個人（目標ごとの詳細つき）、プレイヤー、アカウント。すべての戦車の結果の行。プレイヤーごとのキル |
| `entities` | ストリームが作るすべてのエンティティ: その型の番号と役割、クライアントの視界に入った時刻と出た時刻 |
| `selfCheck` | 完全性の数（[完全性](completeness.md)）と、エンティティとバージョンの確認 |

---

[3DHeat](https://github.com/Holdi601/3DHeat)（[ドキュメント](https://holdi601.github.io/3DHeat/)）の一部です。ソース: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT)。
