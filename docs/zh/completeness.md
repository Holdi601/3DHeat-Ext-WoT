---
title: "完整性"
nav_order: 8
lang: zh
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# 完整性 {#completeness}

录像中的任何内容都不会被丢弃。转换器读取的内容进入表格和对局文档；其他每一项都会完整保存在附属文件 `<对局>.messages.parquet` 中；对局文档中的 `selfCheck.completeness` 则统计每一类项目的去向。这是所有 3DHeat 转换器共同遵守的规则：[转换器保留所有内容](https://holdi601.github.io/3DHeat/converters.html)。

![一份合成录像的自我检查：每一项都已被看到、读取、保留或丢失](../assets/img/completeness.svg)

## 计数 {#the-count}

对于每一类项目，`selfCheck.completeness.types` 给出以下数值：

| 计数 | 含义 |
|---|---|
| `seen` | 录像中有多少个 |
| `decoded` | 完整读取的数量 |
| `partial` | 部分读取，并在附属文件中完整保存的数量 |
| `raw` | 仅在附属文件中完整保存、未被读取的数量 |
| `lost` | 丢失的数量：始终为 `0` |

这些类别来自录像本身：`block 0`（文件头）、`block 1`（结果）、`container sizes` 和 `deflate tail`（容器自身的字节）、`packet <类型>`；对于实体上的调用，则为 `method <实体类型>.<编号>` 和 `property <实体类型>.<编号>`。实体类型即创建数据包给出的编号；`selfCheck.entities.roles` 说明哪一个是录像播放者的化身，哪些是载具。未知的类别会以其计数显示出来。

## 附属文件 {#the-sidecar}

| 列 | 内容 |
|---|---|
| `time` | 录像的时钟，与表格中相同 |
| `type`、`name` | 项目的类别；转换器如何称呼它，以及它在何处被读取 |
| `entity` | 它所属的载具或化身，即表格中的 `entity` |
| `decoded` | 对它的读取内容，以 JSON 表示 |
| `payload`、`text` | 它的字节，完整保存；JSON 块，完整保存 |
| `entityType`、`packet`、`method` | 对应的编号 |

各行按数据包、方法、实体和时间排序。

## 读取了什么，以及如何核对 {#what-is-read-and-how-it-was-checked}

- 每个位置的**俯仰和横滚**：俯仰为负的坦克自身路径在前进时的坡度；同一位置、朝向相同的两辆坦克，横滚相同；朝向相反则横滚相反。
- **实体**（`entities`）：每个实体何时进入客户端的视野，何时离开。坦克在离开与重新出现之间没有位置。
- **流中的版本**（`streamVersion`）：与文件头中的相同。
- **录像播放者的瞄准**（数据包 38）：一个方向，位于附属文件的 `decoded` 中（`forward`）；在播放者开火时，它与炮弹飞行的方向相差不到一度。

其余所有读取的内容（生命值、命中、射击、曳光弹、爆炸、炮的角度、竞技场更新、聊天、相机模式、客户端事件、位置）都属于 `partial`：它们在表格或对局文档中，并在附属文件中完整保存。

**保留但未读取**（`raw`）的主要类别：不在表格中的位置更新（化身的、坦克阵亡之后的，以及不在名单中的实体）；数据包 26、28、29、31、36、50、54 和 57；一些频繁出现的载具和化身属性；每一个没有读取器的方法和属性（其中包括模块损伤、乘组和消耗品）；以及实体创建时的属性。

## 不可用的内容 {#not-available}

- 服务器从未发送给录像播放者客户端的内容：其他玩家的瞄准、相机和输入，未被发现的敌人。录像只反映一个客户端所被告知的内容。
- 实体类型、方法和属性的名称：它们位于游戏的定义文件中，而不在录像中。编号会被保留。
- 以度为单位的火炮仰角，以及任何需要游戏文件中坦克自身数据的其他内容。

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT)。
