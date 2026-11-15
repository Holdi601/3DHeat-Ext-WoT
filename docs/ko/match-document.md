---
title: 매치 문서
nav_order: 6
lang: ko
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# 매치 문서 {#the-match-document}

`<match>.match.json`에는 리플레이가 테이블의 행이 아닌 것으로 말하는 모든 것이 들어 있어요. 뷰어의 매치 탭이 이 파일을 읽어요. (코드에서는 이것을 요약이라고 불러요.)

![합성 매치 문서의 시작 부분과 그 키들](../assets/img/match-document.svg)

## 전투 {#the-battle}

| 키 | 내용 |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; 전투의 ID; 맵의 ID와 표시 이름 |
| `clientVersion`, `streamVersion` | 헤더의 게임 버전, 그리고 패킷 스트림이 말하는 버전 |
| `recorded` | 리플레이를 녹화한 시각, 게임이 쓴 그대로 |
| `player`, `vehicle` | 녹화한 플레이어와 그 전차 |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | 헤더의 전투 유형 번호, 게임 모드, 서버, 지역, 그리고 모드가 설치되어 있었는지 |
| `duration` | 결과에서 가져온 전투의 길이(초) |
| `winnerTeam`, `finishReason` | 이긴 팀과, 전투가 어떻게 끝났는지에 대한 게임의 번호. 결과에서 가져와요 |
| `complete`, `truncated` | 결과가 리플레이에 있는지; 녹화가 일찍 멈췄는지 |
| `battleStart`, `battleStartFrom`, `firstMovement` | 녹화 중 전투의 시작(초); `arena`(전장이 그렇다고 말함) 또는 `movement`(어떤 전차라도 처음 움직인 순간); 그 처음 움직인 순간 |
| `recordingSeconds` | 녹화의 길이(초) |
| `positionPacket`, `hz`, `positions` | 위치가 온 패킷 번호, 초당 샘플 수, 위치 행 |
| `events` | 이벤트마다 테이블 행의 수 |
| `units` | `metres; x east, y up, z north` |
| `decoded` | 메시지 종류마다 찾은 메서드와 패킷 번호 |

## 플레이어와 이벤트 {#players-and-events}

| 키 | 내용 |
|---|---|
| `players` | 전차 하나당 항목 하나: 이름, 팀, 전차, 클랜, 샘플 수, 처치, 준 피해, 생존 여부, 생존 시간. `seen`(녹화한 클라이언트가 본 사격과 피해); 헤더와 결과의 항목 전체, 그리고 계정 |
| `kills` | 모든 사망: 시각(초), 시각의 출처(`arena`, `health`, `lifeTime`), 피해자, 공격자, 이유 번호와 이름 |
| `periods` | 전투의 기간들(대기, 전투 준비, 전투, 전투 후)과 서버가 준 끝나는 시각 |
| `basePoints` | 팀과 기지별 기지 점령 진행도 |
| `chat`, `commands` | 채팅 줄; 모든 인자가 있는 전투 채팅 명령 |
| `camera`, `clientEvents` | 녹화한 플레이어의 카메라 모드; 클라이언트가 자신에 대해 녹화한 것(줌, 자동 조준, 목표 변경, 차량 상태) |
| `arenaUpdates` | 게임이 보낸 그대로 해독한 모든 전장 업데이트 |

## 결과와 확인 {#results-and-checks}

| 키 | 내용 |
|---|---|
| `serverSettings` | 헤더의 서버 설정 |
| `results`, `resultVehicles`, `frags` | 결과 화면: 공통, 개인(대상별 세부 정보 포함), 플레이어, 계정; 모든 전차의 결과 줄; 플레이어별 처치 |
| `entities` | 스트림이 만드는 모든 엔티티: 타입 번호와 역할, 클라이언트 시야에 들어온 때와 나간 때 |
| `selfCheck` | 완전성 셈([완전성](completeness.md))과 엔티티 및 버전의 확인 |

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
