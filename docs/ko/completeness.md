---
title: 완전성
nav_order: 8
lang: ko
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# 완전성 {#completeness}

리플레이에서 버려지는 것은 없어요. 변환기가 읽는 것은 테이블과 매치 문서에 들어가요. 그 밖의 항목은 모두 사이드카 `<match>.messages.parquet`에 통째로 보관돼요. 매치 문서의 `selfCheck.completeness`는 항목 종류마다 그 항목이 어떻게 되었는지 셈해요. 이것은 모든 3DHeat 변환기가 함께 따르는 규칙이에요: [변환기는 모든 것을 보관해요](https://holdi601.github.io/3DHeat/converters.html).

![합성 리플레이의 자기 점검: 본 항목, 읽은 것, 보관한 것, 잃은 것](../assets/img/completeness.svg)

## 셈 {#the-count}

항목 종류마다 `selfCheck.completeness.types`는 다음을 줘요:

| 셈 | 뜻 |
|---|---|
| `seen` | 리플레이가 가진 개수 |
| `decoded` | 통째로 읽은 것 |
| `partial` | 일부를 읽고, 사이드카에 통째로 보관한 것 |
| `raw` | 사이드카에만 통째로 보관하고 읽지 않은 것 |
| `lost` | 잃은 것: 항상 `0` |

종류는 리플레이 자신의 것이에요: `block 0`(헤더), `block 1`(결과), `container sizes`와 `deflate tail`(컨테이너 자체의 바이트), `packet <type>`, 그리고 엔티티에 대한 호출은 `method <entity type>.<number>`와 `property <entity type>.<number>`예요. 엔티티 타입은 엔티티를 만드는 패킷이 주는 번호예요. `selfCheck.entities.roles`가 어느 것이 녹화한 플레이어의 아바타이고 어느 것이 차량인지 알려 줘요. 아무도 몰랐던 종류는 개수와 함께 나와요.

## 사이드카 {#the-sidecar}

| 열 | 내용 |
|---|---|
| `time` | 리플레이의 시계, 테이블과 같아요 |
| `type`, `name` | 항목의 종류; 변환기가 그것을 무엇이라 부르는지, 어디서 읽는지 |
| `entity` | 그 항목이 속한 차량 또는 아바타, 테이블의 `entity`와 같아요 |
| `decoded` | 읽은 내용, JSON으로 |
| `payload`, `text` | 바이트 전체; JSON 블록 전체 |
| `entityType`, `packet`, `method` | 번호들 |

행은 패킷, 메서드, 엔티티, 시간 순으로 정렬돼요.

## 무엇을 읽었고, 어떻게 확인했나 {#what-is-read-and-how-it-was-checked}

- 모든 위치의 **피치와 롤**: 피치는 전차가 앞으로 가는 동안 그 전차 자신의 경로 기울기의 음수예요. 같은 자리에 같은 방위를 가진 두 전차는 같은 롤을 가지고, 방위가 반대면 롤도 반대예요.
- **엔티티**(`entities`): 각각 언제 클라이언트의 시야에 들어오고 나갔는지. 어떤 전차도 나간 뒤 다시 돌아올 때까지 위치가 없어요.
- **스트림의 버전**(`streamVersion`): 헤더의 버전과 같아요.
- **녹화한 플레이어의 조준**(패킷 38): 방향이에요. 사이드카의 `decoded`(`forward`)에 있어요. 플레이어의 사격에서는 포탄이 날아간 방향과 몇 도의 몇 분의 일 이내로 맞아요.

읽은 다른 모든 것(체력, 명중, 사격, 예광탄, 폭발, 포의 각도, 전장 업데이트, 채팅, 카메라 모드, 클라이언트 이벤트, 위치)은 `partial`이에요. 테이블이나 매치 문서에 있고, 사이드카에 통째로 보관돼요.

**보관했지만 읽지 않은 것**(`raw`)이 가장 큰 종류예요. 테이블에 없는 위치 업데이트(아바타의 것, 전차가 죽은 뒤의 것, 명단에 없는 엔티티), 패킷 26, 28, 29, 31, 36, 50, 54, 57, 자주 오는 차량과 아바타의 일부 속성, 읽는 코드가 없는 모든 메서드와 속성(모듈 피해, 승무원, 소모품 등), 그리고 엔티티 생성의 속성이에요.

## 알 수 없는 것 {#not-available}

- 서버가 녹화한 클라이언트에게 보내지 않은 것: 다른 플레이어의 조준, 카메라와 입력, 발견되지 않은 적. 리플레이는 한 클라이언트가 들은 것이에요.
- 엔티티 타입, 메서드, 속성의 이름: 게임의 정의 파일에 있고, 리플레이에는 없어요. 번호는 보관해요.
- 포신의 고각(도)과, 게임 파일의 전차 자신의 데이터가 필요한 그 밖의 것.

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
