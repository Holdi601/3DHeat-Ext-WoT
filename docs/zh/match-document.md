---
title: "对局文档"
nav_order: 6
lang: zh
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# 对局文档 {#the-match-document}

`<对局>.match.json` 保存了录像中所有不属于表格中某一行的内容。查看器的 **对局** 标签页会读取它。（代码中称之为摘要。）

![合成对局文档的开头部分及其键](../assets/img/match-document.svg)

## 战斗 {#the-battle}

| 键 | 内容 |
|---|---|
| `format`、`version` | `heat3d-wot-match`、`2` |
| `game`、`match`、`map`、`mapName` | `World of Tanks`；战斗的 ID；地图的 ID 及其显示名称 |
| `clientVersion`、`streamVersion` | 文件头中的游戏版本，以及数据包流所给出的版本 |
| `recorded` | 录像的录制时间，与游戏写入的格式相同 |
| `player`、`vehicle` | 录像播放者及其坦克 |
| `battleType`、`gameplay`、`server`、`region`、`hasMods` | 文件头中的战斗类型编号、游戏模式、服务器、地区，以及是否安装了模组 |
| `duration` | 战斗的时长（秒），来自结果 |
| `winnerTeam`、`finishReason` | 获胜队伍，以及游戏对战斗结束原因的编号，来自结果 |
| `complete`、`truncated` | 录像中包含结果；录制提前停止 |
| `battleStart`、`battleStartFrom`、`firstMovement` | 战斗在录制中的开始时间（秒）；`arena`（竞技场如此表明）或 `movement`（任何坦克首次移动的时刻）；该首次移动的时间 |
| `recordingSeconds` | 录像的长度（秒） |
| `positionPacket`、`hz`、`positions` | 位置数据所在的数据包编号，每秒采样数，位置行 |
| `events` | 每种事件的表格行数 |
| `units` | `metres; x east, y up, z north`（米；x 朝东，y 朝上，z 朝北） |
| `decoded` | 为每类消息找到的方法和数据包编号 |

## 玩家与事件 {#players-and-events}

| 键 | 内容 |
|---|---|
| `players` | 每辆坦克一项：名称、队伍、坦克、战队、采样数、击杀、造成的伤害、是否存活、生存时间；`seen`（录像客户端所见的射击和伤害）；文件头和结果中的完整条目，以及账号 |
| `kills` | 每一次死亡：时间（秒）、时间的来源（`arena`、`health` 或 `lifeTime`）、受害者、击杀者、原因编号和名称 |
| `periods` | 战斗的各阶段（等待、开战前、战斗中、战斗后），附带服务器给出的结束时间 |
| `basePoints` | 每个队伍、每个基地的基地占领进度 |
| `chat`、`commands` | 聊天行；战斗聊天命令及其所有参数 |
| `camera`、`clientEvents` | 录像播放者的相机模式；客户端记录的关于自身的信息（变焦、自动瞄准、目标切换、载具状态） |
| `arenaUpdates` | 每一次竞技场更新，已解码，与游戏发送时相同 |

## 结果与核对 {#results-and-checks}

| 键 | 内容 |
|---|---|
| `serverSettings` | 文件头中的服务器设置 |
| `results`、`resultVehicles`、`frags` | 结果界面：通用信息、个人信息（附带针对每个目标的详细数据）、玩家、账号；每辆坦克的结果行；每位玩家的击杀数 |
| `entities` | 数据流创建的每个实体：其类型编号和角色、进入客户端视野的时间和离开的时间 |
| `selfCheck` | 完整性计数（[完整性](completeness.md)），以及对实体和版本的核对 |

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT)。
