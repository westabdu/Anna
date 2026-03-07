# src/animations/wave_animation.py
"""
A.N.N.A Mobile - JARVIS SES DALGASI ANİMASYONLARI
- Iron Man HUD tarzı ses dalgaları
- Canlı frekans göstergesi
- Dinleme/konuşma modları
- Renk geçişleri ve parlamalar
"""

import flet as ft
import threading
import time
import random
import math


class WaveAnimation:
    """JARVIS tarzı ses dalgası animasyonu"""
    
    def __init__(self, colors):
        self.colors = colors
        self.is_active = False
        self.mode = "idle"  # idle, listening, speaking
        self.wave_bars = []
        self.bar_count = 40  # Daha fazla bar = daha akıcı
        self.base_heights = []
        
        # JARVIS renk paleti
        self.wave_colors = [
            colors["primary"],      # JARVIS mavisi
            colors["secondary"],    # Mor
            colors["accent"],       # Kırmızı (vurgu)
            colors["primary_light"],
            colors["accent_light"],
        ]
        
        # HUD parlaması
        self.hud_glow = colors.get("hud_glow", colors["primary"] + "40")
        
        # Dalga konteynırı
        self.container = None
        self.animation_thread = None
        
    def build(self, height=80):
        """JARVIS dalga animasyonu container'ını oluştur"""
        
        # Rastgele başlangıç yükseklikleri (daha çeşitli)
        for i in range(self.bar_count):
            self.base_heights.append(random.randint(5, 30))
        
        # Bar'ları oluştur (JARVIS HUD tarzı)
        self.wave_bars = []
        for i in range(self.bar_count):
            # Gradient efekti için renk seçimi
            if i < self.bar_count // 3:
                color = self.colors["primary"]  # Mavi
            elif i < 2 * self.bar_count // 3:
                color = self.colors["secondary"]  # Mor
            else:
                color = self.colors["accent"]  # Kırmızı
            
            bar = ft.Container(
                width=3,
                height=self.base_heights[i],
                bgcolor=color,
                border_radius=2,
                animate=ft.animation.Animation(100, ft.AnimationCurve.EASE_IN_OUT),
                opacity=0.6,
                shadow=ft.BoxShadow(
                    blur_radius=5,
                    color=self.hud_glow,
                    spread_radius=1,
                ),
                tooltip=f"Frekans {i}",
            )
            self.wave_bars.append(bar)
        
        # JARVIS tarzı alt çizgi
        bottom_line = ft.Container(
            width=400,
            height=1,
            gradient=ft.LinearGradient(
                colors=[self.colors["primary"], self.colors["secondary"], self.colors["accent"]],
            ),
            border_radius=1,
            margin=ft.margin.only(top=5),
        )
        
        # Ana konteynır
        self.container = ft.Container(
            content=ft.Column([
                ft.Row(
                    self.wave_bars,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2,
                ),
                bottom_line,
            ]),
            height=height,
            visible=False,
            animate=ft.animation.Animation(300),
            padding=5,
        )
        
        return self.container
    
    def start_listening(self):
        """Dinleme modu - JARVIS tarama efekti"""
        self.mode = "listening"
        self.container.visible = True
        self.is_active = True
        
        def animate():
            phase = 0
            while self.is_active and self.mode == "listening":
                for i, bar in enumerate(self.wave_bars):
                    # Karmaşık dalga formülü (JARVIS tarama efekti)
                    t = time.time() * 4
                    
                    # Ana dalga
                    wave1 = math.sin(t + i * 0.3) * 0.7
                    
                    # İkincil dalga (frekans modülasyonu)
                    wave2 = math.sin(t * 1.5 + i * 0.5) * 0.3
                    
                    # Rastgele varyasyon
                    noise = random.uniform(-0.1, 0.1)
                    
                    # Birleştir
                    height_factor = wave1 + wave2 + noise + 1.0
                    
                    # Bar yüksekliği
                    bar.height = max(4, int(25 * height_factor))
                    
                    # Soldan sağa renk geçişi
                    color_index = (i + int(t * 10)) % len(self.wave_colors)
                    bar.bgcolor = self.wave_colors[color_index]
                    
                    # Hareket eden parlaklık
                    bar.opacity = 0.5 + 0.5 * math.sin(t * 2 + i)
                    
                    # Parlama efekti
                    bar.shadow = ft.BoxShadow(
                        blur_radius=5 + 5 * math.sin(t + i),
                        color=self.hud_glow,
                        spread_radius=1,
                    )
                
                phase += 0.1
                time.sleep(0.02)  # Daha akıcı
        
        # Eski thread'i durdur
        if self.animation_thread and self.animation_thread.is_alive():
            self.is_active = False
            time.sleep(0.1)
        
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
    
    def start_speaking(self):
        """Konuşma modu - JARVIS konuşma efekti (daha enerjik)"""
        self.mode = "speaking"
        self.container.visible = True
        self.is_active = True
        
        def animate():
            while self.is_active and self.mode == "speaking":
                for i, bar in enumerate(self.wave_bars):
                    # Daha agresif, patlamalı dalga
                    t = time.time() * 8
                    
                    # Çoklu frekans
                    freq1 = abs(math.sin(t + i)) * 2
                    freq2 = abs(math.sin(t * 2 + i * 2)) * 1.5
                    freq3 = random.uniform(0, 1) * 0.5  # Rastgele patlama
                    
                    height_factor = freq1 + freq2 + freq3
                    
                    # Daha yüksek dalgalar
                    bar.height = max(8, int(30 * height_factor))
                    
                    # Parlak renkler
                    color_index = (i + int(t * 15)) % len(self.wave_colors)
                    bar.bgcolor = self.wave_colors[color_index]
                    bar.opacity = 0.8 + 0.2 * math.sin(t * 3)
                    
                    # Güçlü parlama
                    bar.shadow = ft.BoxShadow(
                        blur_radius=10 + 10 * math.sin(t * 2),
                        color=self.colors["accent"] + "80",
                        spread_radius=2,
                    )
                
                time.sleep(0.015)
        
        # Eski thread'i durdur
        if self.animation_thread and self.animation_thread.is_alive():
            self.is_active = False
            time.sleep(0.1)
        
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
    
    def start_processing(self):
        """İşlem modu - veri akışı efekti"""
        self.mode = "processing"
        self.container.visible = True
        self.is_active = True
        
        def animate():
            direction = 1
            pos = 0
            while self.is_active and self.mode == "processing":
                for i, bar in enumerate(self.wave_bars):
                    # Soldan sağa hareket eden dalga
                    distance = abs(i - pos)
                    intensity = math.exp(-distance / 5)
                    
                    bar.height = max(5, int(20 * intensity))
                    bar.bgcolor = self.colors["primary"]
                    bar.opacity = intensity
                
                pos += direction * 0.5
                if pos >= self.bar_count:
                    direction = -1
                    pos = self.bar_count - 1
                elif pos < 0:
                    direction = 1
                    pos = 0
                
                time.sleep(0.03)
        
        # Eski thread'i durdur
        if self.animation_thread and self.animation_thread.is_alive():
            self.is_active = False
            time.sleep(0.1)
        
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
    
    def stop(self):
        """Animasyonu durdur ve gizle"""
        self.is_active = False
        self.mode = "idle"
        
        if self.container:
            self.container.visible = False
        
        # Bar'ları sıfırla
        for i, bar in enumerate(self.wave_bars):
            bar.height = self.base_heights[i]
            bar.bgcolor = self.wave_colors[i % len(self.wave_colors)]
            bar.opacity = 0.6
    
    def pause(self):
        """Animasyonu duraklat"""
        self.is_active = False
        self.mode = "idle"