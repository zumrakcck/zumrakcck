# Pet Care Assistant - Use Case Documentation

## Sistem Kapsami

Pet Care Assistant; pet sahibi kullanicilarin evcil hayvanlarini, bakim hatirlaticilarini,
gunluk aktivitelerini ve premium aboneliklerini yonetmesini saglayan; admin kullanicilarin
ise kullanici, premium durum ve rapor sureclerini izlemesini saglayan bir web uygulamasidir.

## Aktorler

- **Pet Owner:** Sisteme kayit olan, pet ekleyen, hatirlatici olusturan, AI asistan ile
  konusan ve premium abonelik satin alan son kullanici.
- **Admin:** Kullanici hesaplarini, premium durumlarini ve sistem raporlarini yoneten yetkili.
- **Payment Gateway:** Premium aktivasyonunda odeme sonucunu donduren harici sistem.
- **AI Assistant:** Pet Owner mesajlarini degerlendirip bakim onerisi ve veteriner yonlendirmesi
  uretebilen servis.

## Genel Senaryo: Pet Bakim Planini Yonetme

| Alan | Aciklama |
| --- | --- |
| Use Case Adi | Pet bakim planini yonetme |
| Birincil Aktor | Pet Owner |
| Destekleyici Aktorler | AI Assistant |
| On Kosullar | Kullanici uygulamaya erisebilir durumdadir. Kayit/giris islemi tamamlanmistir. |
| Tetikleyici | Pet Owner evcil hayvan bakim bilgilerini guncellemek ister. |
| Son Durum | Pet, hatirlatici ve aktivite bilgileri sistemde guncel olarak saklanir. |

### Genel Akis

1. Pet Owner uygulamayi acar ve Register / Login islemi ile dogrulanir.
2. Sistem kullanicinin ana panelini, pet listesini ve ozet istatistikleri gosterir.
3. Pet Owner yeni pet bilgilerini girer ve **Add Pet** islemini calistirir.
4. Sistem pet kaydini olusturur ve **View Pets** listesini gunceller.
5. Pet Owner pet icin yeni bir hatirlatici ekler.
6. Sistem hatirlaticiyi kaydeder ve yaklasan bakim planini gunceller.
7. Pet Owner gunluk aktivite bilgisini girer.
8. Sistem aktiviteyi saklar ve rapor/ozet alanlarina yansitir.
9. Pet Owner gerekirse AI asistana mesaj gonderir.
10. Sistem istegi dogrular ve uygun bakim onerisi veya veteriner yonlendirmesi uretir.

### Alternatif Akislar

- **A1 - Eksik pet bilgisi:** Pet adi, turu veya yas bilgisi eksikse sistem kaydi reddeder ve
  kullanicidan gerekli alanlari tamamlamasini ister.
- **A2 - Hatirlatici tarihi gecersiz:** Hatirlatici tarihi bos veya gecersizse sistem kaydetmez
  ve uyari mesaji gosterir.
- **A3 - AI istegi dogrulanamaz:** Mesaj bos ise veya kullanici girisi yoksa sistem istegi
  dogrulamaz ve sohbet akisini baslatmaz.

## Sub Senaryo 1: Pet Bilgisini Duzenleme veya Silme

| Alan | Aciklama |
| --- | --- |
| Use Case Adi | Pet bilgisini duzenleme / silme |
| Birincil Aktor | Pet Owner |
| On Kosullar | Kullanici giris yapmistir ve sistemde en az bir pet kaydi vardir. |
| Tetikleyici | Pet Owner mevcut pet bilgisini degistirmek veya kaydi silmek ister. |
| Son Durum | Pet bilgisi guncellenir veya pet kaydi sistemden kaldirilir. |

### Genel Akis

1. Pet Owner **View Pets** listesini acar.
2. Sistem kullaniciya ait petleri listeler.
3. Pet Owner bir pet icin **Edit Pet Information** islemini secer.
4. Sistem mevcut pet bilgilerini forma getirir.
5. Pet Owner alanlari gunceller ve kaydeder.
6. Sistem pet bilgisini dogrular, gunceller ve listeyi yeniler.

### Alternatif Akislar

- **A1 - Pet silme:** Pet Owner **Delete Pet** islemini secerse sistem onay alir ve pet kaydini
  listeden kaldirir.
- **A2 - Gecersiz veri:** Yas veya kilo sayisal degilse sistem guncellemeyi durdurur ve hata
  mesaji verir.
- **A3 - Iliskili hatirlatici bulunmasi:** Pet silindiginde sisteme bagli hatirlaticilar listede
  korunur ancak pet secimi genel hale getirilir; kullanici hatirlaticiyi ayrica silebilir.

## Sub Senaryo 2: Premium Uyelik Aktifleştirme

| Alan | Aciklama |
| --- | --- |
| Use Case Adi | Premium uyelik aktifleştirme |
| Birincil Aktor | Pet Owner |
| Destekleyici Aktorler | Payment Gateway, Admin |
| On Kosullar | Kullanici sisteme giris yapmistir ve premium degildir. |
| Tetikleyici | Pet Owner gelismis AI onerileri ve raporlar icin premium almak ister. |
| Son Durum | Odeme basariliysa kullanicinin premium durumu aktif olur; aksi halde hata mesaji gosterilir. |

### Genel Akis

1. Pet Owner premium kartindaki **Activate Premium** islemini baslatir.
2. Sistem odeme detaylarini hazirlar ve **Process Payment** islemini cagirir.
3. Payment Gateway odemeyi basarili olarak dondurur.
4. Sistem kullanici premium durumunu aktif yapar.
5. Admin panelindeki premium kullanici sayisi ve rapor bilgileri guncellenir.

### Alternatif Akislar

- **A1 - Odeme reddedildi:** Payment Gateway basarisiz yanit dondururse sistem **Show Payment Error**
  akisini calistirir ve premium durumu degistirmez.
- **A2 - Zaten premium kullanici:** Kullanici zaten premium ise sistem yeni odeme baslatmadan mevcut
  durum bilgisini gosterir.
- **A3 - Admin incelemesi:** Admin **Manage Premium Status** ekranindan kullanicinin premium durumunu
  izler ve raporlarda abonelik sayisini kontrol eder.
