---
title: "Koşullar ve lisans"
nav_order: 9
lang: tr
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Koşullar ve lisans {#terms-and-licence}

## Wargaming'in koşulları {#wargamings-terms}

2026-11-07 tarihinde okundu, Wargaming EULA sürüm 14 (10 Nisan 2024 tarihinden geçerli, güncel olarak listeli):

- 5.3 (b): yazılı izin olmadan "... decompile, disassemble, reverse engineer or otherwise make unauthorized use of the
  Content" yapmamalısınız.
- 12.1 (k): yasak olan "Creating, using, making available, or distributing any unauthorized software or tools,
  including hacks, cheats, exploits, scripts, bots, trainers, automation programs, or other software that interacts
  with a Product in any way and for any purpose, including intercepts, emulates, or redirects any communication
  between such software and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user experience ("mods") unless expressly
  permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures implemented by Wargaming".

World of Tanks'in yasaklı modlar listesi savaşın kendisiyle ilgilidir: "reveal the position of enemies in a way not
included in the client" yapan modlar, nişan botları, yeniden yükleme zamanlayıcıları ve benzerleri. Ne EULA ne de
bu liste tekrarlardan söz eder.

Bu dönüştürücü ne yapar: oyunun yazdığı bir dosyayı, savaştan sonra, oyunun dışında okur. Oyunda hiçbir şeyi
değiştirmez, hiçbir sunucuyla konuşmaz ve savaş sırasında hiçbir şey göstermez. Akışı oyunun anahtarıyla
deşifre eder; bunun 5.3 (b) ve 12.1 (p) kapsamında okunabileceği düşünülebilir. Kullanmak kullanıcının kararıdır;
bu yüzden ayrı bir paket olarak tutulur.

## Lisans ve kaynaklar {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). numpy (BSD-3-Clause) ve pyarrow
(Apache-2.0) gerektirir. Bu proje için yazılmıştır: buradaki Blowfish şifresi kendi şifresidir, tabloları şifrenin
tanımladığı gibi pi'nin basamaklarından hesaplanmıştır. Biçim hakkında bilinenler (kapsayıcı, şifre, konum paketi)
replay araçları arasında yaygın bilgidir; evido/wotreplay-parser (BSD-3-Clause) bunları belgeler; ondan ya da başka
bir projeden hiçbir kod alınmamıştır.

`bigworld.py` ve `table.py`, World of Warships dönüştürücüsündeki
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)) aynı dosyalardır; ikisini birlikte değiştirin.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
