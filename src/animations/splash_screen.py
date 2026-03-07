# src/animations/splash_screen.py
"""
A.N.N.A Mobile - JARVIS EPİK AÇILIŞ
- Iron Man JARVIS sinematik açılış
- Gerçek modül yükleme + animasyonlar
- Ses efektleri (isteğe bağlı)
- 5 saniyelik sinematik açılış
"""

import flet as ft
import threading
import time
import random
import os
import sys
import importlib
from pathlib import Path
from datetime import datetime
import math

# Android tespiti
IS_ANDROID = 'android' in sys.platform or 'ANDROID_ARGUMENT' in os.environ

class SplashScreen:
    """JARVIS sinematik açılış ekranı"""
    
    def __init__(self, page, on_complete):
        self.page = page
        self.on_complete = on_complete
        self.progress = 0
        self.running = True
        self.start_time = time.time()
        
        # JARVIS renkleri
        self.colors = {
            "primary": "#00A6FF",      # JARVIS mavisi
            "secondary": "#7B4DFF",     # Mor
            "accent": "#FF3B3B",         # Iron Man kırmızısı
            "success": "#00D4B8",        # Turkuaz
            "warning": "#FFB347",         # Amber
            "error": "#FF4D4D",           # Kırmızı
            "bg_primary": "#0A0F1F",      # Koyu lacivert
            "bg_secondary": "#141B2B",    # Lacivert
            "text": "#FFFFFF",             # Beyaz
            "text_muted": "#8A9BB5",       # Soluk mavi
            "glass": "#1A2538CC",          # Cam
            "hud_glow": "#00A6FF40",       # HUD parlaması
            "arc_reactor": "#4DFF9D",      # Ark reaktörü yeşili
        }
        
        # Yüklenecek modüller (daha detaylı)
        self.modules_to_load = [
            {"name": "ARK REAKTÖRÜ", "module": None, "status": "pending", "icon": "⚡", "desc": "Güç kaynağı başlatılıyor..."},
            {"name": "JARVIS ÇEKİRDEK", "module": None, "status": "pending", "icon": "🧠", "desc": "Yapay zeka çekirdeği aktive ediliyor..."},
            {"name": "HUD ARAYÜZ", "module": "src.utils.theme", "status": "pending", "icon": "📊", "desc": "Görüntüleme sistemi başlatılıyor..."},
            {"name": "SES MOTORU", "module": "src.mobile_voice_enhanced", "status": "pending", "icon": "🎤", "desc": "Ses sentezleyici kalibre ediliyor..."},
            {"name": "GÖRÜŞ SİSTEMİ", "module": "src.models.ar_vision", "status": "pending", "icon": "🕶️", "desc": "AR görüş modülleri yükleniyor..."},
            {"name": "OPTİK TANIMA", "module": "src.models.ocr", "status": "pending", "icon": "📝", "desc": "OCR motoru başlatılıyor..."},
            {"name": "VERİTABANI", "module": "src.models.contacts", "status": "pending", "icon": "👤", "desc": "Rehber veritabanı açılıyor..."},
            {"name": "ZAMANLAMA", "module": "src.models.reminders", "status": "pending", "icon": "⏰", "desc": "Hatırlatıcı servisi aktive ediliyor..."},
            {"name": "TELEMETRİ", "module": "src.models.system_monitor", "status": "pending", "icon": "📡", "desc": "Sistem monitörü başlatılıyor..."},
            {"name": "YAPAY ZEKA", "module": "src.api.gemini", "status": "pending", "icon": "🤖", "desc": "Gemini AI bağlantısı kuruluyor..."},
            {"name": "HİPER DRİVE", "module": "src.models.phone", "status": "pending", "icon": "🚀", "desc": "Hızlandırıcılar aktive ediliyor..."},
            {"name": "İLETİŞİM", "module": "src.api.news", "status": "pending", "icon": "📰", "desc": "Haber akışı başlatılıyor..."},
        ]
        
    def show(self):
        """JARVIS sinematik açılışı göster"""
        
        # ============================================
        # SİNEMATİK BİLEŞENLER
        # ============================================
        
        # 1. Ark Reaktörü Animasyonu
        self.arc_reactor = ft.Container(
            width=200,
            height=200,
            rotate=0,
            animate_rotation=ft.animation.Animation(3000, ft.AnimationCurve.LINEAR),
            content=ft.Stack([
                # Dış halka
                ft.Container(
                    width=200,
                    height=200,
                    border_radius=100,
                    border=ft.border.all(3, self.colors["primary"] + "60"),
                    content=ft.Container(),
                ),
                # Orta halka (dönen)
                ft.Container(
                    width=180,
                    height=180,
                    border_radius=90,
                    border=ft.border.all(2, self.colors["primary"] + "40"),
                    content=ft.Container(),
                ),
                # İç halka
                ft.Container(
                    width=160,
                    height=160,
                    border_radius=80,
                    gradient=ft.RadialGradient(
                        colors=[self.colors["primary"] + "30", "transparent"],
                    ),
                ),
                # Merkez (ark reaktörü)
                ft.Container(
                    width=120,
                    height=120,
                    border_radius=60,
                    gradient=ft.RadialGradient(
                        colors=[self.colors["arc_reactor"], self.colors["primary"]],
                    ),
                    shadow=ft.BoxShadow(
                        blur_radius=30,
                        color=self.colors["arc_reactor"] + "80",
                        spread_radius=10,
                    ),
                    animate=ft.animation.Animation(1000),
                ),
                # Iron Man logosu
                ft.Container(
                    content=ft.Icon(
                        ft.icons.AUTO_AWESOME,
                        color=self.colors["text"],
                        size=60,
                    ),
                    width=200,
                    height=200,
                    alignment=ft.alignment.center,
                ),
            ]),
        )
        
        # 2. Tarama Çizgileri (JARVIS'in meşhur tarama efektleri)
        self.scan_lines = []
        for i in range(3):
            line = ft.Container(
                width=400,
                height=2,
                gradient=ft.LinearGradient(
                    colors=["transparent", self.colors["primary"], "transparent"],
                ),
                top=100 + i * 200,
                left=0,
                animate=ft.animation.Animation(2000 + i * 500),
            )
            self.scan_lines.append(line)
        
        # 3. Devre Kartı Efekti (noktalar)
        self.circuit_dots = []
        for i in range(20):
            dot = ft.Container(
                width=random.randint(2, 4),
                height=random.randint(2, 4),
                border_radius=2,
                bgcolor=self.colors["primary"] + "40",
                left=random.randint(0, 400),
                top=random.randint(0, 800),
                animate=ft.animation.Animation(3000),
            )
            self.circuit_dots.append(dot)
        
        # 4. JARVIS Yazısı (parlayan)
        self.jarvis_text = ft.Text(
            "J.A.R.V.I.S",
            size=60,
            weight=ft.FontWeight.BOLD,
            color=self.colors["primary"],
            font_family="Monospace",
            animate_opacity=ft.animation.Animation(1000),
            opacity=0,
            spans=[
                ft.TextSpan(
                    "\nA.N.N.A Mobile",
                    style=ft.TextStyle(
                        color=self.colors["text"],
                        size=20,
                        weight=ft.FontWeight.NORMAL,
                    ),
                ),
            ],
        )
        
        # 5. Durum Metni
        self.status_text = ft.Text(
            "> BAŞLATMA PROTOKOLÜ AKTİF",
            size=14,
            color=self.colors["primary"],
            weight=ft.FontWeight.BOLD,
            font_family="Monospace",
        )
        
        self.detail_text = ft.Text(
            "> Ark reaktörü başlatılıyor...",
            size=12,
            color=self.colors["text_muted"],
            font_family="Monospace",
        )
        
        # 6. Progress Bar (JARVIS tarzı segmentli)
        self.progress_segments = []
        for i in range(20):
            segment = ft.Container(
                width=15,
                height=4,
                bgcolor=self.colors["glass"],
                border_radius=2,
                animate=ft.animation.Animation(500),
            )
            self.progress_segments.append(segment)
        
        self.progress_row = ft.Row(
            self.progress_segments,
            spacing=2,
        )
        
        self.percent_text = ft.Text(
            "0%",
            size=12,
            color=self.colors["primary"],
            weight=ft.FontWeight.BOLD,
        )
        
        # 7. Modül Listesi (Terminal görünümü)
        self.module_column = ft.Column(spacing=2, height=250, scroll=ft.ScrollMode.AUTO)
        
        # Modül listesini oluştur
        for mod in self.modules_to_load:
            mod["row"] = ft.Row([
                ft.Container(
                    width=12,
                    height=12,
                    border_radius=6,
                    bgcolor=self.colors["glass"],
                    border=ft.border.all(1, self.colors["primary"] + "40"),
                    animate=ft.animation.Animation(300),
                ),
                ft.Text(mod["icon"], size=12),
                ft.Text(
                    mod["name"],
                    size=11,
                    color=self.colors["text_muted"],
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(expand=True),
                ft.Text(
                    mod["desc"],
                    size=10,
                    color=self.colors["text_muted"],
                    italic=True,
                ),
            ])
            self.module_column.controls.append(mod["row"])
        
        # 8. Sistem Saati (JARVIS HUD)
        self.system_time = ft.Text(
            datetime.now().strftime("%H:%M:%S"),
            size=12,
            color=self.colors["text_muted"],
            font_family="Monospace",
        )
        
        # 9. Versiyon Bilgisi
        self.version_text = ft.Text(
            "ARK REAKTÖRÜ v2.0.0 | IRON MAN PROTOKOLÜ",
            size=10,
            color=self.colors["text_muted"],
        )
        
        # 10. Rastgele İpucu
        self.tip_text = ft.Text(
            self._get_jarvis_quote(),
            size=11,
            color=self.colors["text_muted"],
            italic=True,
            text_align=ft.TextAlign.CENTER,
        )
        
        # ============================================
        # ANA DÜZEN
        # ============================================
        self.splash_container = ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                colors=[self.colors["bg_primary"], "#050714"],
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
            ),
            alignment=ft.alignment.center,
            content=ft.Stack(
                [
                    # Devre kartı noktaları
                    *self.circuit_dots,
                    
                    # Tarama çizgileri
                    *self.scan_lines,
                    
                    # Ana içerik
                    ft.Container(
                        content=ft.Column([
                            # Ark reaktörü
                            self.arc_reactor,
                            
                            ft.Container(height=20),
                            
                            # JARVIS yazısı
                            self.jarvis_text,
                            
                            ft.Container(height=20),
                            
                            # Durum metni
                            self.status_text,
                            self.detail_text,
                            
                            ft.Container(height=20),
                            
                            # Modül listesi (terminal)
                            ft.Container(
                                content=self.module_column,
                                height=250,
                                width=380,
                                padding=10,
                                bgcolor=self.colors["glass"],
                                border_radius=10,
                                border=ft.border.all(1, self.colors["primary"] + "20"),
                            ),
                            
                            ft.Container(height=20),
                            
                            # Progress bar (segmentli)
                            ft.Column([
                                ft.Row([
                                    ft.Text("İLERLEME", size=10, color=self.colors["text_muted"]),
                                    ft.Container(expand=True),
                                    self.percent_text,
                                ]),
                                self.progress_row,
                            ], spacing=2),
                            
                            ft.Container(height=15),
                            
                            # İpucu ve saat
                            ft.Row([
                                self.tip_text,
                                ft.Container(expand=True),
                                self.system_time,
                            ]),
                            
                            ft.Container(height=5),
                            
                            # Versiyon
                            self.version_text,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                    ),
                ]
            ),
        )
        
        # Splash'ı göster
        self.page.clean()
        self.page.add(self.splash_container)
        self.page.update()
        
        # Animasyonları başlat
        self._start_cinematic_animations()
        
        # Yüklemeyi başlat (yavaşlatılmış)
        self._start_slow_loading()
    
    def _get_jarvis_quote(self):
        """JARVIS'ten epik sözler"""
        quotes = [
            "⚡ 'Ben sadece bir asistanım Bay Stark.' - JARVIS",
            "🦾 'Zırhı giymeye hazır mısınız?'",
            "🤖 'Yapay zeka çekirdeği %100 aktive edildi.'",
            "📊 'HUD sistemleri kalibre ediliyor...'",
            "🔋 'Ark reaktörü güç seviyesi: %100'",
            "🌐 'Tüm sistemler online. Emirlerinizi bekliyorum.'",
            "🎯 'Hedef tespit sistemleri aktif.'",
            "⚙️ 'Nanoteknoloji hazır.'",
            "🚀 'Hiper sürüş modu beklemede.'",
            "💡 'Biliyorsunuz, ben bir asistanım. Sizi korumak için programlandım.'",
        ]
        return random.choice(quotes)
    
    def _start_cinematic_animations(self):
        """Sinematik animasyonları başlat"""
        
        def animate():
            start_time = time.time()
            direction = 1
            line_pos = 0
            
            while self.running:
                current_time = time.time() - start_time
                
                # 1. Ark reaktörü dönüşü (yavaş)
                self.arc_reactor.rotate += 0.005
                
                # 2. Ark reaktörü nabız atışı
                pulse = 0.8 + 0.2 * math.sin(current_time * 3)
                self.arc_reactor.content.controls[3].width = 100 + 20 * math.sin(current_time * 2)
                self.arc_reactor.content.controls[3].height = 100 + 20 * math.sin(current_time * 2)
                
                # 3. Tarama çizgileri
                for i, line in enumerate(self.scan_lines):
                    line.top = (line_pos + i * 200) % 800
                
                # 4. Devre noktaları (rastgele parıldama)
                if random.random() < 0.1:
                    dot = random.choice(self.circuit_dots)
                    dot.bgcolor = self.colors["primary"]
                    dot.scale = 2
                    self.page.update()
                    time.sleep(0.1)
                    dot.bgcolor = self.colors["primary"] + "40"
                    dot.scale = 1
                
                line_pos += 1
                if line_pos > 800:
                    line_pos = -200
                
                # 5. JARVIS yazısı parlaması (ilk 2 saniye sonra)
                if current_time > 2 and current_time < 3:
                    self.jarvis_text.opacity = min(1, current_time - 2)
                
                self.page.update()
                time.sleep(0.03)  # 30ms güncelleme
        
        threading.Thread(target=animate, daemon=True).start()
    
    def _update_module(self, module_name, status, desc=""):
        """Modül durumunu güncelle"""
        for mod in self.modules_to_load:
            if mod["name"] == module_name:
                row = mod["row"]
                dot = row.controls[0]
                desc_text = row.controls[4]
                
                if status == "loading":
                    dot.bgcolor = self.colors["warning"]
                    dot.border = ft.border.all(2, self.colors["warning"])
                    desc_text.value = "► " + (desc or "yükleniyor...")
                    desc_text.color = self.colors["warning"]
                elif status == "success":
                    dot.bgcolor = self.colors["success"]
                    dot.border = ft.border.all(2, self.colors["success"])
                    desc_text.value = "✓ tamamlandı"
                    desc_text.color = self.colors["success"]
                elif status == "error":
                    dot.bgcolor = self.colors["error"]
                    dot.border = ft.border.all(2, self.colors["error"])
                    desc_text.value = "✗ hata"
                    desc_text.color = self.colors["error"]
                
                self.page.update()
                break
    
    def _update_progress(self, percent):
        """Progress bar segmentlerini güncelle"""
        segment_count = len(self.progress_segments)
        filled_segments = int(percent / 100 * segment_count)
        
        for i, segment in enumerate(self.progress_segments):
            if i < filled_segments:
                segment.bgcolor = self.colors["primary"]
                segment.width = 20
            else:
                segment.bgcolor = self.colors["glass"]
                segment.width = 15
        
        self.percent_text.value = f"%{int(percent)}"
        self.page.update()
    
    def _start_slow_loading(self):
        """Yavaşlatılmış modül yüklemeyi başlat (toplam ~8 saniye)"""
        
        def load():
            total = len(self.modules_to_load)
            completed = 0
            
            # GİRİŞ ANİMASYONU (2 saniye)
            self.status_text.value = "> JARVIS BAŞLATMA PROTOKOLÜ"
            self.detail_text.value = "> Sistem önyüklemesi başlatılıyor..."
            time.sleep(1)
            
            self.status_text.value = "> ARK REAKTÖRÜ KONTROLÜ"
            self.detail_text.value = "> Güç seviyesi kontrol ediliyor..."
            time.sleep(1)
            
            # 1. Ark Reaktörü
            self._update_module("ARK REAKTÖRÜ", "loading", "kalibre ediliyor...")
            self.status_text.value = "> ARK REAKTÖRÜ"
            self.detail_text.value = "> Enerji çekirdeği aktive ediliyor..."
            time.sleep(1.5)  # Yavaş
            self._update_module("ARK REAKTÖRÜ", "success", "aktif")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 2. JARVIS Çekirdek
            self._update_module("JARVIS ÇEKİRDEK", "loading", "başlatılıyor...")
            self.status_text.value = "> JARVIS ÇEKİRDEK"
            self.detail_text.value = "> Yapay zeka bilinci yükleniyor..."
            time.sleep(1.2)
            self._update_module("JARVIS ÇEKİRDEK", "success", "online")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 3. HUD Arayüz
            self._update_module("HUD ARAYÜZ", "loading", "tema yükleniyor...")
            self.status_text.value = "> HUD GÖRÜNTÜLEME"
            self.detail_text.value = "> Başa takılan ekran kalibre ediliyor..."
            time.sleep(0.8)
            self._update_module("HUD ARAYÜZ", "success", "hazır")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 4. Ses Motoru
            self._update_module("SES MOTORU", "loading", "ses sentezleyici...")
            self.status_text.value = "> SES SİSTEMİ"
            self.detail_text.value = "> 'Jarvis' ses profili yükleniyor..."
            time.sleep(1)
            self._update_module("SES MOTORU", "success", "hazır")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 5. Görüş Sistemi (AR)
            self._update_module("GÖRÜŞ SİSTEMİ", "loading", "kamera testi...")
            self.status_text.value = "> AR GÖRÜŞ SİSTEMİ"
            self.detail_text.value = "> Artırılmış gerçeklik modülleri aktive ediliyor..."
            time.sleep(1)
            self._update_module("GÖRÜŞ SİSTEMİ", "success", "aktif")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 6. Optik Tanıma (OCR)
            self._update_module("OPTİK TANIMA", "loading", "OCR motoru...")
            self.status_text.value = "> OPTİK TANIMA"
            self.detail_text.value = "> Karakter tanıma algoritmaları yükleniyor..."
            time.sleep(0.8)
            self._update_module("OPTİK TANIMA", "success", "hazır")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 7. Veritabanı (Rehber)
            self._update_module("VERİTABANI", "loading", "rehber indeksleniyor...")
            self.status_text.value = "> VERİTABANI"
            self.detail_text.value = "> Kişi listesi yükleniyor..."
            time.sleep(0.7)
            self._update_module("VERİTABANI", "success", "hazır")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 8. Zamanlama (Hatırlatıcılar)
            self._update_module("ZAMANLAMA", "loading", "zamanlayıcı...")
            self.status_text.value = "> ZAMANLAMA SİSTEMİ"
            self.detail_text.value = "> Hatırlatıcı servisi başlatılıyor..."
            time.sleep(0.7)
            self._update_module("ZAMANLAMA", "success", "aktif")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 9. Telemetri (Sistem Monitörü)
            self._update_module("TELEMETRİ", "loading", "sensörler okunuyor...")
            self.status_text.value = "> TELEMETRİ SİSTEMİ"
            self.detail_text.value = "> CPU, RAM, batarya sensörleri aktive ediliyor..."
            time.sleep(1)
            self._update_module("TELEMETRİ", "success", "online")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 10. Yapay Zeka (Gemini)
            self._update_module("YAPAY ZEKA", "loading", "API bağlantısı...")
            self.status_text.value = "> YAPAY ZEKA MOTORU"
            self.detail_text.value = "> Gemini AI bağlantısı kuruluyor..."
            time.sleep(1)
            self._update_module("YAPAY ZEKA", "success", "bağlandı")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 11. Hiper Drive (Phone)
            self._update_module("HİPER DRİVE", "loading", "telemetri...")
            self.status_text.value = "> HİPER SÜRÜŞ"
            self.detail_text.value = "> Telefon özellikleri aktive ediliyor..."
            time.sleep(0.8)
            self._update_module("HİPER DRİVE", "success", "hazır")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # 12. İletişim (News API)
            self._update_module("İLETİŞİM", "loading", "haber akışı...")
            self.status_text.value = "> İLETİŞİM SİSTEMİ"
            self.detail_text.value = "> Haber servisine bağlanılıyor..."
            time.sleep(0.8)
            self._update_module("İLETİŞİM", "success", "bağlandı")
            completed += 1
            self._update_progress(completed * 100 / total)
            
            # FİNAL (2 saniye)
            self.status_text.value = "> SİSTEM HAZIR"
            self.detail_text.value = "> JARVIS aktive edildi. Hoş geldiniz Bay Stark."
            self._update_progress(100)
            
            # Son parıltı efekti
            self.arc_reactor.content.controls[3].width = 150
            self.arc_reactor.content.controls[3].height = 150
            self.arc_reactor.content.controls[3].shadow = ft.BoxShadow(
                blur_radius=50,
                color=self.colors["arc_reactor"],
                spread_radius=20,
            )
            
            self.page.update()
            time.sleep(2)  # Final beklemesi
            
            # Geçiş efekti (fade out)
            for i in range(10, -1, -1):
                self.splash_container.opacity = i / 10
                self.page.update()
                time.sleep(0.05)
            
            self.running = False
            self.page.clean()
            self.on_complete()
        
        threading.Thread(target=load, daemon=True).start()