---
title: "Maç belgesi"
nav_order: 6
lang: "tr"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Maç belgesi {#the-match-document}

`<match>.match.json` tekrarın, tablonun bir satırı olmayan her şeyini tutar. Görüntüleyicinin Maç sekmesi
onu okur. (Kod buna özet der.)

![Sentetik bir maç belgesinin başı ve anahtarları](../assets/img/match-document.svg)

## Savaş {#the-battle}

| Anahtar | Ne |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; savaşın kimliği; haritanın kimliği ve görünen adı |
| `clientVersion`, `streamVersion` | başlıktan oyun sürümü ve paket akışının söylediği biçimde |
| `recorded` | tekrarın ne zaman kaydedildiği, oyunun yazdığı gibi |
| `player`, `vehicle` | kayıt oyuncusu ve tankı |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | başlıktaki savaş türü numarası, oyun modu, sunucu, bölge ve modların kurulu olup olmadığı |
| `duration` | savaşın saniye cinsinden süresi, sonuçlardan |
| `winnerTeam`, `finishReason` | kazanan takım ve savaşın nasıl bittiğinin oyundaki numarası, sonuçlardan |
| `complete`, `truncated` | sonuçlar tekrarda var; kayıt erken durdu |
| `battleStart`, `battleStartFrom`, `firstMovement` | savaşın başlangıcı, kaydın saniyesi cinsinden; `arena` (arenanın bildirdiği an) ya da `movement` (herhangi bir tankın ilk hareket ettiği an); o ilk hareket |
| `recordingSeconds` | kaydın saniye cinsinden uzunluğu |
| `positionPacket`, `hz`, `positions` | konumların geldiği paket numarası, saniyedeki örnek, konum satırları |
| `events` | her olay türünün tablo satırı sayısı |
| `units` | `metres; x east, y up, z north` |
| `decoded` | her ileti türü için bulunan yöntem ve paket numaraları |

## Oyuncular ve olaylar {#players-and-events}

| Anahtar | Ne |
|---|---|
| `players` | bir tank başına bir giriş: ad, takım, tank, klan, örnekler, öldürmeler, verilen hasar, hayatta kalma, yaşam süresi; `seen` (kayıt istemcisinin gördüğü atışlar ve hasar); başlığın ve sonuçların bütün girişi ve hesabın |
| `kills` | her ölüm: zaman (saniye), zamanın nereden geldiği (`arena`, `health` ya da `lifeTime`), kurban, öldüren, neden numarası ve adı |
| `periods` | savaşın dönemleri (bekleme, savaş öncesi, savaş, savaş sonrası) sunucunun bitiş zamanlarıyla |
| `basePoints` | takım ve üs başına üs ele geçirme ilerlemesi |
| `chat`, `commands` | sohbet satırları; tüm argümanlarıyla savaş sohbeti komutları |
| `camera`, `clientEvents` | kayıt oyuncusunun kamera modları; istemcinin kendisi hakkında kaydettikleri (yakınlaştırma, otomatik nişan, hedef değişiklikleri, araç durumu) |
| `arenaUpdates` | her arena güncellemesi, çözülmüş, oyunun gönderdiği gibi |

## Sonuçlar ve denetimler {#results-and-checks}

| Anahtar | Ne |
|---|---|
| `serverSettings` | başlıktaki sunucu ayarları |
| `results`, `resultVehicles`, `frags` | sonuç ekranı: ortak, kişisel (hedef başına ayrıntılarla), oyuncular, hesaplar; her tankın sonuç satırı; oyuncu başına öldürmeler |
| `entities` | akışın oluşturduğu her varlık: tür numarası ve rolü, istemcinin görüşüne ne zaman girdiği ve ne zaman çıktığı |
| `selfCheck` | tamlık sayımı ([Tamlık](completeness.md)) ve varlıkların ve sürümün denetimleri |

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
