import os
import requests
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- KİMLİK BİLGİLERİ ---
TOKEN = "7549980125:AAFxvyz5jVm6SKMapJI9A3BlO6fX--kaxSM"
CHAT_ID = "1958158640"

def veri_analizi(ticker):
    try:
        # Veriyi çek ve MultiIndex hatasını temizle
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if df.empty or len(df) < 200: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            
        fiyatlar = df['Close'].dropna()
        fiyat = float(fiyatlar.iloc[-1])
        dun = float(fiyatlar.iloc[-2])
        degisim = ((fiyat - dun) / dun) * 100
        ma200 = float(fiyatlar.rolling(window=200).mean().iloc[-1])
        dist_ma = ((fiyat - ma200) / ma200) * 100
        
        # RSI Hesapla
        delta = fiyatlar.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 1e-9))))
        
        return {"fiyat": fiyat, "dun": dun, "degisim": degisim, "rsi": rsi, "ma200": dist_ma}
    except: return None

def kategori_yaz(baslik, semboller):
    section = f"=== {baslik} ===\n"
    sonuclar = []
    
    for sym, isim in semboller.items():
        d = veri_analizi(sym)
        if d:
            emoji = "📈" if d['degisim'] >= 0 else "📉"
            line = f"{isim}: {d['fiyat']:,.2f} {emoji} {d['degisim']:+.2f}% (dün: {d['dun']:,.2f})\n"
            line += f"   RSI: {d['rsi']:.1f} | MA200: %{d['ma200']:+.1f}\n"
            section += line
            sonuclar.append({"isim": isim, "degisim": d['degisim'], "rsi": d['rsi'], "ma200": d['ma200']})
    
    if sonuclar:
        avg = sum(x['degisim'] for x in sonuclar) / len(sonuclar)
        en_guclu = max(sonuclar, key=lambda x: x['degisim'])
        en_zayif = min(sonuclar, key=lambda x: x['degisim'])
        section += f"--- Özet ---\nKategori Ort: {avg:+.2f}%\nEn Güçlü: {en_guclu['isim']}\nEn Zayıf: {en_zayif['isim']}\n\n"
        return section, sonuclar
    return "", []

def ana_rapor():
    # Görsellerdeki yapıya göre tam sıralı liste
    pazarlar = {
        "🪙 KRİPTO": {"BTC-USD": "Bitcoin", "ETH-USD": "Ethereum"},
        "🚨 ÖZEL TAKİP (Zarar Durumu)": {"BA": "Boeing (BA)", "VOW3.DE": "Volkswagen (VOW3)"},
        "🏛 ENDEKSLER": {"^GSPC": "S&P 500", "NQ=F": "Nasdaq", "YM=F": "Dow Jones"},
        "🧭 RİSK PUSULASI": {"DX-Y.NYB": "DXY", "^VIX": "VIX"},
        "🇺🇸 ABD ETF": {"VOO": "VOO", "QQQ": "QQQ", "SCHD": "SCHD", "IWM": "IWM", "XLK": "XLK", "XLF": "XLF"},
        "🌍 DÜNYA": {"VT": "VT", "VXUS": "VXUS"},
        "🏗 SEKTÖR/EMTİA": {"SOXX": "SOXX", "SMH": "SMH", "GC=F": "Altın", "SI=F": "Gümüş", "USO": "Petrol"}
    }
    
    final_msg = f"🏛 **STRATEJİK MİMARİ PANEL**\n📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
    toplam_sonuc = []
    
    for baslik, liste in pazarlar.items():
        metin, veriler = kategori_yaz(baslik, liste)
        final_msg += metin
        toplam_sonuc.extend(veriler)
    
    # --- STRATEJİK FIRSATLAR VE UYARILAR ---
    alarmlar = []
    for s in toplam_sonuc:
        # RSI 33 Altı = Çok Ucuz, 70 Üstü = Çok Şişkin
        if s['rsi'] < 33: alarmlar.append(f"🔥 {s['isim']} AŞIRI SATIM (RSI: {s['rsi']:.1f})")
        if s['rsi'] > 70: alarmlar.append(f"⚠️ {s['isim']} AŞIRI ŞİŞKİN (RSI: {s['rsi']:.1f})")
        # MA200 Altı = Uzun vadeli toplama bölgesi
        if s['ma200'] < 0: alarmlar.append(f"📍 {s['isim']} MA200 ALTI (İndirimli!)")

    if alarmlar:
        final_msg += "⚠️ **STRATEJİK ANALİZ NOTLARI:**\n" + "\n".join(list(set(alarmlar)))
        
    return final_msg

if __name__ == "__main__":
    print("Mimar verileri topluyor, raporun son hali hazırlanıyor...")
    rapor = ana_rapor()
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, data={"chat_id": CHAT_ID, "text": rapor, "parse_mode": "Markdown"})
    
    if res.status_code == 200:
        print("✅ Başyapıt Telegram'a başarıyla ulaştırıldı!")
    else:
        print(f"❌ Telegram Hatası: {res.text}")