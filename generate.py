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
current_timestamp = int(time.time())

print("📡 Kanal linkleri anonim istemci ile toplanıyor...\n")

for slug, isim, url in kanallar:
    try:
        # DEĞİŞİKLİK BURADA: Şifre/Token yok.
        # YouTube engellerini aşmak için botun kendisini "Android Client" olarak tanıtmasını sağladık.
        cmd = [
            "yt-dlp",
            "--extractor-args", "youtube:player-client=android", 
            "-f", "b", 
            "-g", url
        ]
            
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        link = result.stdout.strip()
        
        if link and link.startswith("http"):
            # Master Playlist formatı
            kanal_m3u_icerik = (
                "#EXTM3U\n"
                "#EXT-X-VERSION:3\n"
                "#EXT-X-STREAM-INF:BANDWIDTH=1280000,RESOLUTION=1280x720\n"
                f"{link}\n"
            )
            with open(f"{streams_dir}/{slug}.m3u8", "w", encoding="utf-8") as f:
                f.write(kanal_m3u_icerik)
                
            github_raw_url = f"https://raw.githubusercontent.com/seyfettinaskar7-sudo/yt-streams/main/streams/{slug}.m3u8?t={current_timestamp}"
            ana_m3u += f'#EXTINF:-1,{isim}\n{github_raw_url}\n'
            
            print(f"✅ {isim} - Başarıyla güncellendi.")
        else:
            print(f"❌ {isim} - Link çözülemedi (YouTube IP engeli atmış olabilir).")
    except Exception as e:
        print(f"❌ {isim} - Hata: {e}")

# Playlist kaydet
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(ana_m3u)

print("\n💾 İşlem tamam. GitHub'a pushlanıyor...")
