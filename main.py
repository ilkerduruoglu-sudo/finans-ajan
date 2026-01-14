import os
import requests
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- KİMLİK BİLGİLERİ ---
TOKEN = "7549980125:AAFxvyz5jVm6SKMapJI9A3BlO6fX--kaxSM"
CHAT_ID = "1958158640"

# --- HATTORI HANZO S&P 500 TAM PUSU LİSTESİ ---
pusu_hisseleri = [
    'AAPL', 'MSFT', 'NVDA', 'AMZN', 'META', 'GOOGL', 'GOOG', 'BRK-B', 'LLY', 'AVGO',
    'JPM', 'TSLA', 'UNH', 'V', 'XOM', 'MA', 'JNJ', 'PG', 'COST', 'HD',
    'ABBV', 'ORCL', 'NFLX', 'WMT', 'KO', 'BAC', 'AMD', 'CVX', 'PEP', 'CRM',
    'ADBE', 'LIN', 'PM', 'ACN', 'TMO', 'WFC', 'IBM', 'DIS', 'ABT', 'CSCO',
    'INTU', 'QCOM', 'AXP', 'CAT', 'GE', 'TXN', 'DHR', 'VZ', 'AMAT', 'MS',
    'AMGN', 'ISRG', 'PFE', 'GS', 'NEE', 'LOW', 'RTX', 'UNP', 'HON', 'SYK',
    'BKNG', 'SPGI', 'T', 'TJX', 'ETN', 'PGR', 'VRTX', 'LRCX', 'BSX', 'REGN',
    'BLK', 'MU', 'C', 'MMC', 'ADP', 'SCHW', 'PLTR', 'ADI', 'MDLZ',
    'GILD', 'BA', 'LMT', 'FIS', 'WM', 'DE', 'BMY', 'CB', 'HCA', 'UBER',
    'KLAC', 'CDNS', 'ANET', 'SNPS', 'MDT', 'SHW', 'MO', 'INTC', 'ZTS', 'EOG',
    'PH', 'APH', 'ORLY', 'CTAS', 'TGT', 'CRWD', 'MCK', 'MAR', 'USB', 'ITW',
    'CL', 'WELL', 'CSX', 'EMR', 'CMG', 'BDX', 'ADSK', 'AON', 'MCO', 'ECL',
    'PNC', 'ICE', 'FDX', 'D', 'NEM', 'HUM', 'NSC', 'F', 'GD', 'EL', 
    'AIG', 'KDP', 'KVUE', 'ROP', 'O', 'COR', 'MPC', 'EW', 'PSA', 'TEL', 
    'DXCM', 'STZ', 'AJG', 'MCHP', 'NOC', 'TRV', 'TFC', 'MET', 'PCAR', 'MSI', 
    'SRE', 'NXPI', 'MNST', 'TT', 'PYPL', 'DASH', 'CPRT', 'VLO', 'IQV', 
    'PAYX', 'AZO', 'IDXX', 'AEP', 'GWW', 'ODFL', 'CHTR', 'FSLR', 'BKR', 'DLTR', 
    'DVN', 'GEHC', 'HLT', 'OKE', 'PCG', 'PSX', 'ROST', 'SBAC', 'STT', 'WBD',
    'MCD', 'MGM', 'MTCH', 'NRG', 'PEG', 'QRVO', 'BXP', 'CME', 'EXC', 'FAST', 'GEN',
    'A', 'ADM', 'AKAM', 'ALB', 'ALGN', 'ALLE', 'AMCR', 'AME', 'AMP', 'AMT',
    'AOS', 'APA', 'APD', 'ARE', 'ATO', 'AVB', 'AWK', 'AXON', 'BALL', 'BBWI',
    'BEN', 'BG', 'BIIB', 'BIO', 'BK', 'BRO', 'BWA', 'CARR', 'CBRE', 'CCI',
    'CCL', 'CDW', 'CE', 'CEG', 'CF', 'CFG', 'CHD', 'CHRW', 'CI', 'CINF',
    'CLX', 'CMA', 'CMCSA', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COO', 'CPB',
    'CPT', 'CRL', 'CSGP', 'CTRA', 'CTSH', 'CTVA', 'CVS', 'DTE', 'DUK', 'DVA',
    'EFX', 'EG', 'EIX', 'ENPH', 'EPAM', 'EQIX', 'EQR', 'ES', 'ESS', 'EVRG',
    'EXC', 'EXPD', 'EXPE', 'EXR', 'FANG', 'FCX', 'FDS', 'FE', 'FFIV', 'FITB',
    'FMC', 'FOXA', 'FRT', 'FTNT', 'FTV', 'GDDY', 'GNRC', 'GRMN', 'HAS', 'HBAN',
    'HIG', 'HII', 'HOLX', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUBB', 'IEX',
    'IFF', 'ILMN', 'INCY', 'INVH', 'IP', 'IPG', 'IRM', 'IT', 'IVZ', 'JBHT',
    'JKHY', 'K', 'KEY', 'KEYS', 'KIM', 'KMB', 'KMI', 'KMX', 'KR', 'L',
    'LDOS', 'LEN', 'LH', 'LHX', 'LNC', 'LNT', 'LULU', 'LUV', 'LVS', 'LW',
    'LYB', 'LYV', 'MAA', 'MAS', 'MHK', 'MKC', 'MLM', 'MOH', 'MOS', 'MPWR',
    'MRK', 'MRNA', 'MSCI', 'MTB', 'MTD', 'NCLH', 'NDAQ', 'NDSN', 'NFE', 'NI',
    'NKE', 'NTRS', 'NUE', 'NVCR', 'NVR', 'NWL', 'NWSA', 'NWS', 'OMC', 'ON',
    'OTIS', 'OXY', 'PAYC', 'PBI', 'PENN', 'PFG', 'PHM', 'PKG', 'PLD', 'PNR',
    'PNW', 'POOL', 'PPG', 'PRU', 'PTC', 'PWR', 'RCL', 'RF', 'RHI', 'RJF',
    'RL', 'RMD', 'ROK', 'ROL', 'RSG', 'RVTY', 'RYAAY', 'SBUX', 'SEE', 'SJM',
    'SLB', 'SNA', 'SO', 'SPG', 'STX', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'TAP',
    'TDG', 'TDY', 'TECH', 'TER', 'TFX', 'TMUS', 'TPR', 'TRMB', 'TROW', 'TSCO',
    'TSN', 'TTWO', 'TYL', 'UAL', 'UDR', 'UHS', 'ULTA', 'VFC', 'VICI', 'VMC',
    'VNO', 'VRSK', 'VRSN', 'VTR', 'VTRS', 'WAB', 'WAT', 'WDC', 'WEC', 'WHR',
    'WMB', 'WRB', 'WST', 'WTW', 'WY', 'WYNN', 'XEL', 'XYL', 'YUM', 'ZBH',
    'ZBRA', 'ZION'

def mavilim_w(df):
    m1 = df['Close'].rolling(window=3).mean()
    m2 = m1.rolling(window=5).mean()
    return m2

def veri_analizi(ticker):
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if df.empty or len(df) < 200: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            
        fiyatlar = df['Close'].dropna()
        fiyat = float(fiyatlar.iloc[-1])
        dun = float(fiyatlar.iloc[-2])
        degisim = ((fiyat - dun) / dun) * 100
        ma200_serisi = fiyatlar.rolling(window=200).mean()
        ma200 = float(ma200_serisi.iloc[-1])
        dist_ma = ((fiyat - ma200) / ma200) * 100
        
        # RSI Hesapla
        delta = fiyatlar.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 1e-9))))
        
        # MavilimW Hesapla (Hattori Hanzo için)
        mav_deger = float(mavilim_w(df).iloc[-1])
        
        return {
            "fiyat": fiyat, "dun": dun, "degisim": degisim, 
            "rsi": rsi, "ma200": dist_ma, "mavilim": mav_deger
        }
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

def hattori_hanzo_taramasi():
    print("⚔️ Hattori Hanzo pusuya yatmış balıkları arıyor...")
    pusu_raporu = "\n⚓ **HATTORI HANZO PUSU LİSTESİ**\n"
    bulunan_sayisi = 0
    
    # Listenin adının pusu_hisseleri olduğundan emin ol
    for ticker in pusu_hisseleri:
        d = veri_analizi(ticker)
        if d and "ma200" in d and "rsi" in d: # Veri tam mı kontrol et
            # Pusu Kriteri: MA200'e %5 yakınlık VE RSI < 45
            if abs(d['ma200']) < 5 and d['rsi'] < 45:
                # d['mavilim'] değerinin hesaplandığından emin olalım
                mav_fiyat = d.get('mavilim', d['fiyat']) 
                durum = "🚀 GÜÇLÜ PUSU" if d['fiyat'] > mav_fiyat else "🚩 PUSU"
                pusu_raporu += f"{durum}: {ticker}\n💰 Fiyat: {d['fiyat']:.2f} | RSI: {d['rsi']:.1f}\n📏 MA200 Uzaklık: %{d['ma200']:.1f}\n\n"
                bulunan_sayisi += 1
                
    if bulunan_sayisi == 0:
        return "\n⚓ **HATTORI HANZO:** Okyanus sakin, pusuya uygun balık yok.\n"
    return pusu_raporu

def ana_rapor():
    pazarlar = {
        "🪙 KRİPTO": {"BTC-USD": "Bitcoin", "ETH-USD": "Ethereum"},
        "🚨 ÖZEL TAKİP": {"BA": "Boeing (BA)", "VOW3.DE": "Volkswagen (VOW3)"},
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
    
    # --- Hattori Hanzo Bölümünü Ekle ---
    final_msg += hattori_hanzo_taramasi()
    
    # --- STRATEJİK FIRSATLAR VE UYARILAR ---
    alarmlar = []
    for s in toplam_sonuc:
        if s['rsi'] < 33: alarmlar.append(f"🔥 {s['isim']} AŞIRI SATIM (RSI: {s['rsi']:.1f})")
        if s['rsi'] > 70: alarmlar.append(f"⚠️ {s['isim']} AŞIRI ŞİŞKİN (RSI: {s['rsi']:.1f})")
        if s['ma200'] < 0: alarmlar.append(f"📍 {s['isim']} MA200 ALTI (İndirimli!)")

    if alarmlar:
        final_msg += "\n⚠️ **STRATEJİK ANALİZ NOTLARI:**\n" + "\n".join(list(set(alarmlar)))
        
    return final_msg

if __name__ == "__main__":
    print("Mimar ve Hattori Hanzo iş birliğiyle rapor hazırlanıyor...")
    rapor = ana_rapor()
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, data={"chat_id": CHAT_ID, "text": rapor, "parse_mode": "Markdown"})
    
    if res.status_code == 200:
        print("✅ Rapor Telegram'a başarıyla ulaştırıldı!")
    else:
        print(f"❌ Telegram Hatası: {res.text}")
