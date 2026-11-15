---
title: "Tamlık"
nav_order: 8
lang: tr
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Tamlık {#completeness}

Tekrarda hiçbir şey atılmaz. Dönüştürücünün okuduğu şeyler tabloya ve maç belgesine girer; geri kalan her öge
`<match>.messages.parquet` yan dosyasında bütün olarak tutulur; maç belgesinin `selfCheck.completeness` alanı ise
her öge türüne ne olduğunu sayar. Bu, tüm 3DHeat dönüştürücülerinin ortak kuralıdır:
[Dönüştürücüler her şeyi tutar](https://holdi601.github.io/3DHeat/converters.html).

![Sentetik bir tekrarın öz denetimi: görülen, okunan, tutulan ya da kaybedilen her öge](../assets/img/completeness.svg)

## Sayım {#the-count}

Her öge türü için `selfCheck.completeness.types` şunları verir:

| Sayı | Anlamı |
|---|---|
| `seen` | tekrarın kaç tane tuttuğu |
| `decoded` | bütün olarak okunan |
| `partial` | kısmen okunan ve yan dosyada bütün olarak tutulan |
| `raw` | yalnızca yan dosyada bütün olarak tutulan, okunmayan |
| `lost` | kaybedilen: her zaman `0` |

Türler tekrarın kendi türleridir: `block 0` (başlık), `block 1` (sonuçlar), `container sizes` ve `deflate tail`
(kapsayıcının kendi baytları), `packet <type>`, ve varlıklara yapılan çağrılar için `method <entity type>.<number>`
ile `property <entity type>.<number>`. Varlık türleri, oluşturan paketlerin verdiği numaralardır;
`selfCheck.entities.roles` hangisinin kayıt oyuncusunun avatarı, hangilerinin araçlar olduğunu söyler.
Kimsenin bilmediği bir tür, sayısıyla birlikte görünür.

## Yan dosya {#the-sidecar}

| Sütun | Ne |
|---|---|
| `time` | tekrarın saati, tabloda olduğu gibi |
| `type`, `name` | ögenin türü; dönüştürücünün ona ne ad verdiği, nerede okuduğu |
| `entity` | ait olduğu araç ya da avatar, tablonun `entity` sütunu gibi |
| `decoded` | okunan kısmı, JSON olarak |
| `payload`, `text` | baytları bütün olarak; JSON blokları bütün olarak |
| `entityType`, `packet`, `method` | numaralar |

Satırlar paket, yöntem, varlık ve zamana göre sıralanır.

## Ne okunur ve nasıl denetlendi {#what-is-read-and-how-it-was-checked}

- Her konumun **eğimi ve yalpası**: eğim, tankın kendi yolunun ileri sürerken eğiminin eksisidir; aynı yönelimde
  aynı noktadaki iki tankın yalpası aynıdır, ters yönelimlerde ters yalpa.
- **Varlıklar** (`entities`): her biri istemcinin görüşüne ne zaman girdi ve ne zaman çıktı. Hiçbir tankın,
  çıkışı ile geri dönüşü arasında bir konumu yoktur.
- **Akıştaki sürüm** (`streamVersion`): başlıktakiyle aynı.
- **Kayıt oyuncusunun nişanı** (paket 38): bir yön, yan dosyanın `decoded` alanında (`forward`); oyuncunun
  atışlarında mermisinin uçtuğu yönden bir derecenin kesri kadar uzaktadır.

Okunan diğer her şey (can, isabetler, atışlar, izleyiciler, patlamalar, top açıları, arena güncellemeleri, sohbet,
kamera modları, istemci olayları, konumlar) `partial`dır: tabloda ya da maç belgesinde, ve yan dosyada bütün olarak tutulur.

**Tutulan ama okunmayan** (`raw`), en büyük türler: tabloda olmayan konum güncellemeleri (avatarın, bir tankın
ölümünden sonra, kadroda olmayan varlıklar), 26, 28, 29, 31, 36, 50, 54 ve 57 numaralı paketler, sık geçen bazı
araç ve avatar özellikleri, okuyucusu olmayan her yöntem ve özellik (modül hasarı, mürettebat ve tüketilebilirler
dahil) ve varlık oluşturmalarının özellikleri.

## Mevcut olmayanlar {#not-available}

- Sunucunun kayıt yapan istemciye hiç göndermediği şeyler: diğer oyuncuların nişanı, kamerası ve girdileri, fark
  edilmemiş düşmanlar. Bir tekrar, bir istemcinin kendisine anlatılanıdır.
- Varlık türlerinin, yöntemlerin ve özelliklerin adları: bunlar oyunun tanım dosyalarındadır, tekrarda değil.
  Numaralar tutulur.
- Topun derece cinsinden yükselmesi ve oyunun dosyalarından tankların kendi verisini gerektiren her şey.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
