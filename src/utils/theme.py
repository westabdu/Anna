# theme.py - JARVIS Temalı Renkler
class MobileTheme:
    themes = {
        # 🌑 **JARVIS DARK** - Iron Man'in orijinal teması
        "jarvis_dark": {
            "bg_primary": "#0A0F1F",      # Koyu lacivert - ana zemin
            "bg_secondary": "#141B2B",     # Biraz daha açık lacivert
            "primary": "#00A6FF",           # JARVIS mavisi (parlak)
            "primary_light": "#4DC3FF",     # Açık mavi
            "secondary": "#7B4DFF",         # Morumsu mavi (HUD efekti)
            "accent": "#FF3B3B",             # Iron Man kırmızısı (vurgu)
            "accent_light": "#FF6B6B",       # Açık kırmızı
            "text": "#FFFFFF",                # Beyaz
            "text_secondary": "#E0E7FF",      # Mavimsi beyaz
            "text_muted": "#8A9BB5",          # Soluk mavi-gri
            "glass": "#1A2538CC",              # Yarı saydam cam efekti
            "glass_dark": "#0F172ACC",         # Daha koyu cam
            "success": "#00D4B8",               # Turkuaz (başarı)
            "warning": "#FFB347",                # Amber (uyarı)
            "error": "#FF4D4D",                   # Parlak kırmızı (hata)
            "info": "#00A6FF",                     # JARVIS mavisi (bilgi)
            "hud_glow": "#00A6FF40",                # HUD parlaması (yarı saydam)
        },
        
        # 🔴 **JARVIS RED** - Iron Man'in zırhındaki kırmızı ağırlıklı
        "jarvis_red": {
            "bg_primary": "#1A0F0F",          # Koyu kırmızımsı siyah
            "bg_secondary": "#2A1A1A",         # Biraz daha açık
            "primary": "#FF4D4D",               # Iron Man kırmızısı
            "primary_light": "#FF7373",          # Açık kırmızı
            "secondary": "#FFB347",               # Altın sarısı (ark reaktörü)
            "accent": "#4DC3FF",                   # Kontrast mavi
            "accent_light": "#7FD4FF",              # Açık mavi
            "text": "#FFFFFF",                       # Beyaz
            "text_secondary": "#FFE0E0",              # Krem beyaz
            "text_muted": "#B58A8A",                   # Soluk kırmızımsı gri
            "glass": "#2A1A1ACC",                       # Yarı saydam kırmızımsı
            "glass_dark": "#1F1212CC",                  # Daha koyu cam
            "success": "#4CAF50",                        # Yeşil
            "warning": "#FFB347",                         # Amber
            "error": "#FF6B6B",                            # Parlak kırmızı
            "info": "#4DC3FF",                              # Mavi
            "hud_glow": "#FF4D4D40",                         # Kırmızı HUD parlaması
        },
        
        # 🔵 **JARVIS BLUE** - Daha modern, teknolojik görünüm
        "jarvis_blue": {
            "bg_primary": "#0A1428",          # Derin lacivert
            "bg_secondary": "#121E36",         # Lacivert
            "primary": "#2B7FFF",               # Elektrik mavisi
            "primary_light": "#5C9EFF",          # Açık mavi
            "secondary": "#9D4DFF",               # Mor
            "accent": "#FFD700",                    # Altın sarısı (vurgu)
            "accent_light": "#FFE55C",               # Açık altın
            "text": "#FFFFFF",                        # Beyaz
            "text_secondary": "#E0F0FF",               # Buz mavisi
            "text_muted": "#7E95B8",                    # Soluk mavi
            "glass": "#1A2740CC",                        # Cam mavisi
            "glass_dark": "#0F1A2ECC",                   # Koyu cam
            "success": "#00E5B8",                         # Turkuaz
            "warning": "#FFB347",                          # Amber
            "error": "#FF5E5E",                             # Kırmızı
            "info": "#2B7FFF",                               # Mavi
            "hud_glow": "#2B7FFF40",                          # Mavi HUD parlaması
        },
        
        # ⚪ **JARVIS WHITE** - Temiz, minimalist tema
        "jarvis_white": {
            "bg_primary": "#F5F8FF",          # Çok açık mavi-beyaz
            "bg_secondary": "#FFFFFF",         # Saf beyaz
            "primary": "#0055FF",               # Koyu mavi
            "primary_light": "#4D85FF",          # Mavi
            "secondary": "#7B4DFF",               # Mor
            "accent": "#FF3B3B",                    # Kırmızı vurgu
            "accent_light": "#FF6B6B",               # Açık kırmızı
            "text": "#0A1428",                        # Koyu lacivert (yazı)
            "text_secondary": "#2A3650",               # Lacivert
            "text_muted": "#6B7A99",                    # Gri-mavi
            "glass": "#E5ECFFCC",                        # Beyaz cam
            "glass_dark": "#D1DCFFCC",                   # Daha koyu cam
            "success": "#00A86B",                         # Koyu yeşil
            "warning": "#E68A00",                          # Koyu amber
            "error": "#E53E3E",                             # Koyu kırmızı
            "info": "#0055FF",                               # Mavi
            "hud_glow": "#0055FF20",                          # Açık mavi HUD
        }
    }
    
    # Varsayılan tema JARVIS DARK
    current = themes["jarvis_dark"]
    
    @classmethod
    def set_theme(cls, theme_name):
        if theme_name in cls.themes:
            cls.current = cls.themes[theme_name]
        return cls.current