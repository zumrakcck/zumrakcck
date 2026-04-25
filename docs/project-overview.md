# Pet Care Assistant - Proje Özeti

Pet Care Assistant, evcil hayvan sahiplerinin bakım kayıtlarını, hatırlatıcılarını, günlük aktivitelerini, AI destekli veteriner önerilerini ve premium üyelik sürecini tek panelden yönetmesini sağlayan bir web uygulamasıdır. Proje, verilen use case diyagramındaki Pet Owner ve Admin aktörleriyle uyumlu olacak şekilde tasarlanmıştır.

## Teslim İçeriği

1. **Sunum Dosyası:** `presentation/Zumra_Cicek_Pet_Care_Assistant.pptx`
2. **Proje Kodları:** `src/`
3. **Use Case Diyagramı:** `diagrams/use-case/use-case-diagram.vpd`, `diagrams/use-case/use-case-diagram.jpeg`
4. **Use Case Dokümantasyonu:** `docs/use-case-documentation.md`
5. **Class Diyagramı:** `diagrams/class/class-diagram.vpd`, `diagrams/class/class-diagram.jpeg`
6. **Activity Diyagramı:** `diagrams/activity/activity-diagram.vpd`, `diagrams/activity/activity-diagram.jpeg`
7. **Sekans Diyagramı:** `diagrams/sequence/sequence-diagram.vpd`, `diagrams/sequence/sequence-diagram.jpeg`
8. **Database Diyagramı:** `diagrams/database/database-diagram.vpd`, `diagrams/database/database-diagram.jpeg`

## Teknoloji

- HTML5
- CSS3
- JavaScript
- LocalStorage tabanlı örnek veri saklama

## Çalıştırma

`src/index.html` dosyasını tarayıcıda açmanız yeterlidir. Alternatif olarak:

```bash
python3 -m http.server 8000 -d src
```

komutunu çalıştırıp `http://localhost:8000` adresine gidebilirsiniz.

## Ana Modüller

- Kullanıcı doğrulama ve oturum simülasyonu
- Pet ekleme, düzenleme ve silme
- Hatırlatıcı ekleme, düzenleme ve silme
- Günlük aktivite takibi
- AI sohbet ve veteriner önerisi
- Premium ödeme işlemi ve ödeme hata durumu
- Admin kullanıcı ve rapor paneli
