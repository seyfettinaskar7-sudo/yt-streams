import os
import subprocess
import time

# Güncel ve doğrulanmış YouTube IPTV kanal listesi
kanallar = [
    ("TRT_Haber", "TRT Haber", "https://www.youtube.com/@trthaber/live"),
    ("Cnn_Turk", "CNN Türk", "https://www.youtube.com/@cnnturk/live"),
    ("NTV", "NTV", "https://www.youtube.com/@ntv/live"),
    ("A_haber", "A Haber", "https://www.youtube.com/@Ahaber/live"),
    ("Haber_Turk", "Haber Türk", "https://www.youtube.com/@haberturktv/live"),
    ("Halk_Tv", "Halk TV", "https://www.youtube.com/@Halktvkanali/live"),
    ("Sozcu_Tv", "Sözcü TV", "https://www.youtube.com/@sozcutelevizyonu/live"),
    ("TGRT_Haber", "TGRT Haber", "https://www.youtube.com/@tgrthaber/live"),
    ("Tgrt_Belgesel", "TGRT Belgesel", "https://www.youtube.com/@tgrtbelgeseltv/live"),
    ("Tgrt_Eu", "TGRT EU", "https://www.youtube.com/@tgrteutv/live"),
    ("Flash_Haber", "Flash Haber", "https://www.youtube.com/@FlashHaberTV/live"),
    ("Haber_Global_TV", "Haber Global", "https://www.youtube.com/@haberglobal/live"),
    ("TV_100", "TV 100", "https://www.youtube.com/@tv100/live"),
    ("Bloomberg_Ht", "Bloomberg HT", "https://www.youtube.com/@bloomberght/live"),
    ("Benguturk_Tv", "Bengü Türk", "https://www.youtube.com/@tvbenguturk/live"),
    ("Krt_Tv", "KRT TV", "https://www.youtube.com/@krtcanli/live"),
    ("Ulusal_Kanal", "Ulusal Kanal", "https://www.youtube.com/@ulusalkanalTV/live"),
    ("Ulke_Tv", "Ülke TV", "https://www.youtube.com/@ulketv/live"),
    ("Akit_Tv", "Akit TV", "https://www.youtube.com/@akittv/live"),
    ("Eko_Turk", "Eko Türk", "https://www.youtube.com/@ekoturktv/live"),
    ("24_Tv", "24 TV", "https://www.youtube.com/@YirmidortTV/live"),
    ("A_Spor", "A Spor", "https://www.youtube.com/@aspor/live"),
    ("Ht_Spor", "HT Spor", "https://www.youtube.com/@htspor/live"),
    ("Tv_Net", "TV Net", "https://www.youtube.com/@tvnet/live"),
    ("Bein_Spor_Haber", "Bein Spor Haber", "https://www.youtube.com/@beINSPORTST%C3%BCrkiye/live"),
    ("Bizim_Ev_Tv", "Bizimev TV", "https://www.youtube.com/@bizimevtv2000/live"),
    ("CNBC_E", "CNBC-e", "https://www.youtube.com/@cnbce/live"),
    ("Diyanet_Cocuk", "Diyanet Çocuk", "https://www.youtube.com/@DiyanetCocuk/live"),
    ("Kemal_Sunal_Tv", "Kemal Sunal TV", "https://www.youtube.com/@GulsahFilmOfficial/live")
]

streams_dir = "streams"
os.makedirs(streams_dir, exist_ok=True)

ana_m3u = "#EXTM3U\n"

print("📡 Kanal linkleri web_embedded istemcisi ile toplanıyor...\n")

for slug, isim, url in kanallar:
    try:
        # YouTube engellerini aşmak için en kararlı web oynatıcı taklidini yapıyoruz
        result = subprocess.run(
            ["yt-dlp", "--extractor-args", "youtube:player-client=web_embedded", "-f", "best", "-g", url],
            capture_output=True, text=True, timeout=20
        )
        link = result.stdout.strip()
        
        if link and link.startswith("http"):
            # 1. Tekil kanal dosyası üretimi
            kanal_m3u_icerik = f"#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:BANDWIDTH=1280000,RESOLUTION=1280x720\n{link}\n"
            with open(f"{streams_dir}/{slug}.m3u8", "w", encoding="utf-8") as f:
                f.write(kanal_m3u_icerik)
                
            # 2. Ana playlist.m3u dosyasına kanalın eklenmesi (M3U Standart format)
            ana_m3u += f'#EXTINF:-1,{isim}\n{streams_dir}/{slug}.m3u8\n'
            print(f"✅ {isim} linki başarıyla alındı.")
        else:
            print(f"❌ {isim} - Yayın linki boş döndü.")
            
    except Exception as e:
        print(f"❌ {isim} - Süreç sırasında hata oluştu: {e}")

# Ana listenin kaydedilmesi
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(ana_m3u)

print("\n💾 Tüm işlemler bitti. Dosyalar başarıyla güncellendi.")
