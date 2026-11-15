---
title: "Tekrarları çevirme"
nav_order: 4
lang: "tr"
source: converting.md
source_hash: "489c52c182ae"
nav_exclude: true
search_exclude: true
---
# Tekrarları çevirme {#converting-replays}

## Adım adım {#step-by-step}

1. **Oyunda kaydı açın:** Ayarlar > Genel > Savaşları kaydet. Bundan sonra oyun her savaşı
   World of Tanks kurulumunuzun `replays` klasörüne kaydeder, örneğin
   `C:\Games\World_of_Tanks_EU\replays`.
2. **Bir terminal açın.** Sonuçların yazılabileceği bir klasörde olun
   ([Başlamadan önce](before-you-start.md)).
3. **Dönüştürücüyü çalıştırın.** Tekrar dosyalarında ya da bunları tutan klasörlerde:

   ```bash
   heat3d-wot-replay "C:\Games\World_of_Tanks_EU\replays" -o out
   heat3d-wot-replay a.wotreplay b.wotreplay -o out
   ```

   `out`, terminalinizin bulunduğu klasörde oluşturulur.
4. **Ne dediğini okuyun.** Her tekrar için bir satır görmelisiniz; sonunda yazdığı tablo yer alır.
5. **Sonucu açın:** 3DHeat görüntüleyicisinde `out/<map>/<match>.parquet` dosyasını Isı haritası
   sekmesinde, `<match>.match.json` dosyasını Maç sekmesinde. Ya da bunları herhangi bir Parquet
   ya da JSON okuyucusuyla okuyun.

![Sentetik bir tekrar üzerinde çalıştırma: çevirme, yeniden çalıştırma, bozuk bir dosya, boş bir klasör](../assets/img/convert.svg)

Resim, testlerin kodda ürettiği bir tekrar üzerinde yapılan çalıştırmadır (gerçek tekrar yok):

- bir tekrar çevrildi: `<file>: <n> positions of <n> vehicles at <rate> Hz, <n> deaths, <map> (<client version>) -> <table>`;
- yeniden çalıştırıldığında, zaten yazılmış maç atlanır: `<file>: already written, <table>`;
- bir tekrar olmayan dosya: `<file>: not converted: <why>` (hata çıktısında; çıkış durumu 1, diğer tekrarlar yine çevrilir);
- hiç tekrar bulunamadı: `no .wotreplay files in <folders>` (çıkış durumu 2).

## Seçenekler {#options}

| Seçenek | Varsayılan | Ne yapar |
|---|---|---|
| `replays` (bir ya da daha fazla) | - | `.wotreplay` dosyaları ya da içlerinde aranacak klasörler (alt klasörler de) |
| `-o`, `--out` | zorunlu | yazılacak klasör: içinde her harita için bir klasör |
| `--force` | kapalı | zaten yazılmış olanları yeniden çevirir |
| `--version` | - | `heat3d-wot-replay <version>` yazar ve durur |
| `-h`, `--help` | - | seçenekleri yazar ve durur |

Program seçenekleri nasıl yazdırıyorsa: [Komut başvurusu](../cli-reference.md).

## Ne yazılır {#what-is-written}

Yalnızca ayrı dosyalar: bu dönüştürücü `.3dheat` dosyası yazmaz (görüntüleyici onları tek bir dosyaya
paketleyebilir: [Bir maç tek dosyada](https://holdi601.github.io/3DHeat/container.html)).
Her tekrar için, `out/<map>/` içine:

| Dosya | Ne |
|---|---|
| `<match>.parquet` | tablo: her tankın zamana göre konumu ve olduğu her olay ([Tablo](table.md)) |
| `<match>.match.json` | maç belgesi: harita, istemci sürümü, oyuncular, öldürmeler, sonuçlar ve diğer her şey ([Maç belgesi](match-document.md)) |
| `<match>.messages.parquet` | yan dosya: yukarıdaki iki dosyanın bütün olarak tutmadığı tekrarın her ögesi ([Tamlık](completeness.md)) |

`<match>`, savaşın kendi kimliğidir; kayıt sonuçlardan önce durduysa dosyanın adıdır.

## Çıkış durumu {#exit-status}

Her tekrar çevrildi ya da atlandıysa `0`, herhangi biri başarısız olduysa `1` (diğerleri yine çevrilir),
hiç tekrar dosyası bulunamadıysa `2`.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
