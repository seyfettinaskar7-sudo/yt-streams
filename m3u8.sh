#!/bin/bash

# --- AYARLAR ---
PROJE_DIR="/root/github-actions[bot]"
cd $PROJE_DIR || { echo "Dizin bulunamadı!"; exit 1; }

# Sistem yollarını tanımla (Cron çalışırken hata almamak için)
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Git Güvenlik Ayarı: Ana dalda olduğumuzdan emin olalım
git checkout main || git checkout -b main

# Playlist Klasörünü Hazırla (Her seferinde temiz bir liste için)
mkdir -p playlist
rm -f playlist/*.m3u8

# --- KANALLARI İŞLE ---
echo ">>> Kanallar taranıyor ve YouTube canlı yayın linkleri alınıyor..."

cat link.json | jq -c '.[]' | while read -r i; do
    name=$(echo "$i" | jq -r '.name')
    target_url=$(echo "$i" | jq -r '.url')
    
    echo ">>> $name güncelleniyor..."

    # --- BURAYA EKLEDİK ---
    # Eğer link.json içindeki url bir YouTube linkiyse, direkt yt-dlp ile canlı çekiyoruz.
    # Eğer değilse, senin eski curl yönteminle sunucudan çekmeye devam ediyor.
    if [[ "$target_url" == *""youtube.com""* ]] || [[ "$target_url" == *""youtu.be""* ]]; then
        echo "    [YouTube] yt-dlp ve cookies.txt kullanılarak link çıkarılıyor..."
        raw_manifest=$(yt-dlp --cookies cookies.txt -g -f b "$target_url" 2>/dev/null)
    else
        echo "    [API] Sunucudan curl ile link aranıyor..."
        raw_manifest=$(curl -i -s --max-time 30 "$target_url" | grep -o "https://manifest.googlevideo.com[^[:space:]\"']*" | head -n 1 | tr -d '\r\n')
    fi
    # ----------------------

    if [ ! -z "$raw_manifest" ] && [[ "$raw_manifest" == http* ]]; then
        # Dosyayı HLS 'Master Playlist' standartlarına uygun oluştur
        cat <<EOF > "streams/${name}.m3u8"
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=1280000,RESOLUTION=1280x720
$raw_manifest
EOF
        echo "   [OK] $name başarıyla dosyaya yazıldı."
    else
        echo "   [!] HATA: $name için link bulunamadı. Yayın kapalı veya yt-dlp engellendi."
    fi
    
    # İstekler arasında 1 saniye bekle
    sleep 1
done

# --- ANA PLAYLIST (M3U) OLUŞTURMA ---
echo ">>> Ana playlist (m3u) birleştiriliyor..."
echo "#EXTM3U" > lists/playlist.m3u

for file in playlist/*.m3u8; do
    [ -s "$file" ] || continue
    fname=$(basename "$file" .m3u8)
    
    # Sadece Google linkini başarıyla çekmiş dosyaları ana listeye ekle
    if grep -q "googlevideo" "$file"; then
        echo "#EXTINF:-1,$fname" >> lists/playlist.m3u
        # GitHub Raw Linkinin sonuna timestamp ekleyerek cache sorununu önlüyoruz
        echo "https://raw.githubusercontent.com/seyfettinaskar7-sudo/yt-streams/main/streams/${fname}.m3u8?t=$(date +%s)" >> lists/playlist.m3u
    fi
done

# --- GITHUB PUSH ---
echo ">>> GitHub'a gönderiliyor..."
git add .
# Eğer bir değişiklik varsa (linkler yenilendiyse) commit ve push yap
if ! git diff-index --quiet HEAD --; then
    git commit -m "Manifest Refresh: $(date +'%d-%m-%Y %H:%M')"
    git push origin HEAD:main --force
    echo ">>> İşlem Başarılı: GitHub güncellendi."
else
    echo ">>> Değişiklik yok, push atlandı."
fi
