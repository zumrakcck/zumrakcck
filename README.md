# Pet Care Assistant

Bu depo, Pet Care Assistant proje teslimi icin hazirlanmistir. Uygulama; pet sahibi
kullanicilarin evcil hayvan, hatirlatici, aktivite, AI destekli oneriler ve premium
abonelik islemlerini yonetmesini saglar. Admin rolu ise kullanici, premium durum ve
rapor ekranlarini izler.

## Teslim Dosyalari

- `presentation/Zumra_Cicek_Pet_Care_Assistant.pptx` - Sunum dosyasi
- `src/` - Proje kodlari
- `docs/use-case-documentation.md` - Use case dokumantasyonu
- `diagrams/use-case/` - Use Case diyagrami (`.vpd` ve `.jpeg`)
- `diagrams/class/` - Class diyagrami (`.vpd` ve `.jpeg`)
- `diagrams/activity/` - Activity diyagrami (`.vpd` ve `.jpeg`)
- `diagrams/sequence/` - Sekans diyagrami (`.vpd` ve `.jpeg`)
- `diagrams/database/` - Database diyagrami (`.vpd` ve `.jpeg`)

## Calistirma

Tarayicida dogrudan `src/index.html` dosyasini acabilirsiniz.

Alternatif olarak yerel sunucu ile calistirmak icin:

```bash
python3 -m http.server 8000 -d src
```

Sonra `http://localhost:8000` adresini acin.

## Diyagram ve Sunum Uretimi

Diyagram JPEG dosyalari, Visual Paradigm kaynak dosyasi yerine teslim klasorune eklenen
`.vpd` adli metinsel model taslaklari ve sunum dosyasi su komutla tekrar uretilebilir:

```bash
python3 tools/generate_assets.py
```
