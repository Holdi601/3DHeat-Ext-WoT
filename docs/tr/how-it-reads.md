---
title: "Tekrarı nasıl okur"
nav_order: 7
lang: tr
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Tekrarı nasıl okur {#how-it-reads-a-replay}

Bir tekrar, JSON bloklarından oluşan bir başlık ve oyunun paket akışıdır (biçim notları:
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Açık haldeki ilk blok: harita, istemci sürümü, kayıt oyuncusu, sunucunun ayarları ve kadro (`vehicles`: ad,
  takım, tank, aracın kimliğiyle anahtarlanmış).
- İkincisi, kayıt sonuna kadar sürdüyse: sonuç ekranı. Her aracın satırı (atışlar, isabetler, delmeler, verilen,
  alınan, engellenen ve yardım edilen hasar, keşif, xp, kredi, başarımlar...), kayıt oyuncusunun hedef başına
  ayrıntıları, hesaplar, maçın süresi, kazanan ve bitiş nedeni; bazı modlarda bu listelerin tek tam kadrosu (bu
  listelerin başlığı yalnızca kendi takımını listeler).
- Paket akışı, zlib ile sıkıştırılmış ve oyunun taşıdığı bir anahtarla Blowfish ile şifrelenmiş; bu dosyaları okuyan
  topluluk araçlarının 2013'ten beri yayımladığı.

**Konumlar**, motorun konum güncellemeleridir: bir aracın kimliği, konumu ve yönü, paket numarasına göre değil
şekline göre bulunur; bu yüzden numaraları değiştiren bir yama tabloyu boşaltmaz. Kayıt eden istemciye söylenenlerdir:
kendi takımı boyunca, bir düşman yalnızca görüldüğü sürece (ya da istemcinin menzilindeyken). Hiç görülmemiş bir
aracın satırı yoktur. Bir aracın satırları ölümünde durur.

**Akışın geri kalanı** (can, atışlar, izleyiciler, patlamalar, isabetler, top açıları, arena güncellemeleri),
araçların ve istemcinin avatarının yöntem çağrıları ve özellik değişiklikleridir; oyunun tanım dosyalarıyla
numaralanmışlardır ve yamalarla değişirler (1.12 ve 2.4 bunları farklı numaralandırır). Her biri argümanlarının
şekliyle ve birbirleriyle nasıl ilişkilendiğiyle bulunur; bkz.
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py).
Bulunan numaralar maç belgesinin `decoded` alanındadır. Sohbet, kamera modu ve istemcinin kendi olayları kendi
paketleridir. Arena güncellemeleri ve istemci olayları Python pickle'larıdır; bunları, adlandırdıkları her sınıfı
etkisiz bir vekile çeviren ve hiçbir şey çalıştırmayan bir okuyucu okur.

Kayıt eden istemciye söylenen, kendi takımı için tam, düşmanlar için kısmidir: onların atışları, isabetleri ve can
değişiklikleri, menzildeyken oradadır.

**Savaşın başlangıcı**, arena güncellemesinin savaş döneminin başladığını söylediği andır; bu olmayan bir tekrarda,
herhangi bir aracın ilk hareket ettiği andır.

**Ölümler:** zaman, arenanın öldürme iletisidir (1.x), yoksa aracı bitiren can değişikliği, yoksa savaşın
başlangıcı artı sonuçlardaki kurbanın `lifeTime`ı (tam saniye). Yer, kurbanın son görüldüğü yerdir; bu ölümünden
beş saniye içindeyse; yoksa 2.x istemcilerinde sonuçların verdiği yer (x ve z, yükseklik yok), yalnızca maç
belgesinde. Sonundan önce duran bir kayıtta ölüm yoktur.

**Okunmayanlar:**

- Görüş ve minimap: tekrarda kendi olayları olarak bir akış yoktur.
- Topun derece cinsinden yükselmesi: akışta topun sınırları arasında bir adım vardır ve sınırlar oyunun araç
  dosyalarındadır.
- Modül hasarı, mürettebat yaralanmaları, tüketilebilirler ve mühimmat: bunları taşıyan çağrılar, 1.12 ve 2.4
  arasında yalnızca şekle bakarak ayırt edilemedi.
- Varlığı ve türü dışındaki varlık oluşturma paketleri: bir aracın istemcinin görüşüne bir anda girdiğindeki her
  özelliği taşırlar, yalnızca tanım dosyalarının verdiği bir sırayla (yan dosyada bütün olarak tutulur).
- Statik çarpışmalar (ağaçlar, evler), kayıt oyuncusunun kendi nişan ve fizik paketleri.
- Savaş sohbeti komut numaraları ad olarak: numaralandırma oyunun kendisidir ve değişir; maç belgesi her komutun
  argümanlarını tutar, varsa anahtarıyla birlikte (`ATTACK_ENEMY`, ...).
- 5'in üzerindeki saldırı nedenleri: yalnızca numara olarak yazılır.

## Okumanın nasıl denetlendiği {#how-the-reading-was-checked}

Okuma, 1.12 ve 2.4 istemcilerinin herkese açık tekrarlarında denetlendi; her değer, tekrarın ona ikinci kez verdiği
bir şeyle karşılaştırıldı:

- **Konumlar:** görülen her tankın saniyede on örnekle bir izi vardır; hızlar bir tankın yapabileceklerinin içinde
  kalır; yön, hareket yönüyle yaklaşık 0,02 rad içinde uyuşur; sonuçların bir ölümün yerini verdiği yerlerde, burada
  okunan yer birkaç metre içindedir.
- **Kayıt oyuncusu:** atışlar ve verilen hasar, denetlenen her tekrarda sonuçların değerlerine eşit okunur.
- **Can:** her tankın son okunan canı sonuçlarınkine eşittir; okunan alınan hasar hiçbir zaman sonuçlardakinden fazla
  değildir. 2.4'te istemcinin görüşü dışındaki bir tankın öldüren darbesi çoğu zaman gönderilmez.
- **İsabetler:** bir isabetin hasarı, neredeyse her isabette o andaki can değişikliğine eşittir.
- **Taret:** bir atışta, gövde yönü artı taretin yaw'ı, izleyicinin uçtuğu yeri gösterir; yaklaşık 0,01 rad içinde
  (medyan).
- **Ölümler ve savaşın başlangıcı:** sonuçların ve arenanın verdiği zamanın yaklaşık bir saniye içinde.

Testler tekrarları aynı düzende üretir; bu yüzden bu depoda hiçbir gerçek tekrar tutulmaz.

**Denetlenmeyenler:** 1.12 öncesi istemciler, konsol ve Blitz tekrarları (farklı oyunlar), Lesta'nın Mir Tankov'u
(`.mtreplay`) ve rastgele savaşlar ile savaş türü 20 dışındaki modlar.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
