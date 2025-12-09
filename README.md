## End-to-End Data Pipeline

Bu proje, Apache Kafka, Apache Spark ve Apache Airflow kullanılarak uçtan uca (end-to-end) veri üretimi, işlenmesi ve otomasyonu örneklemek için hazırlanmıştır.

## Proje Amacı
Gerçek zamanlı vliği araçlarıyla (Kafka, Spark, Airflow) Docker üzerinde dee toplu veri işleme süreçlerini, modern veri mühendisneyimlemek ve öğrenmek.

## Mimarideki Bileşenler
- **Kafka:** Gerçek zamanlı veri akışı ve saklama (sipariş verileri).
- **Spark:** Kafka'dan verileri okuyup toplu (batch) olarak analiz ve raporlama.
- **Airflow:** Spark işlerini otomatik ve zamanlanmış şekilde tetikleme.
- **Postgres:** (İsteğe bağlı) Kalıcı veri saklama.Bu projede kullanılmıyor.
- **Producer (Python):** Kafka'ya rastgele sipariş verisi üreten Python scripti.

## Nasıl Çalışır?
1. **Producer**, Kafka'ya rastgele sipariş verileri gönderir.
2. **Kafka**, bu verileri saklar ve Spark ile paylaşır.
3. **Airflow**, her gün otomatik olarak bir Spark job'u tetikler.
4. **Spark**, Kafka'daki verileri okur, ürün bazında toplam satış ve ciroyu hesaplar.
5. Sonuçlar loglarda tablo olarak görüntülenir.

## Kurulum ve Çalıştırma
1. `.env.example` dosyasını kopyalayıp `.env` olarak adlandırın ve gerekli bilgileri doldurun.
2. Tüm servisleri başlatmak için:
   ```
   docker-compose up -d
   ```
3. Kafka producer'ı başlatmak için:
   ```
   python kafka_producer/producer.py
   ```
4. Airflow arayüzüne erişin.
5. `daily_report_dag` isimli DAG'ı elle veya otomatik olarak tetikleyin.


## Kullanılan Teknolojiler
- Apache Kafka
- Apache Spark
- Apache Airflow
- Docker & Docker Compose
- Python (kafka-python, pyspark)

---
## UYARI
Bu proje, veri mühendisliği süreçlerini öğrenmek ve denemek isteyenler için hazırlanmış bir örnektir.Ticari bir amaç için kullanılamaz.
