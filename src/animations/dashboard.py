# src/animations/dashboard.py
"""
A.N.N.A Mobile - Dinamik Durum Paneli
- Batarya yüzdesi
- Canlı saat
- Çevrimiçi durumu
- Sistem metrikleri
"""

import os
import sys

import flet as ft
import threading
import time
from datetime import datetime
from src.utils.theme import MobileTheme

from numpy import random

# Android tespiti
IS_ANDROID = 'android' in sys.platform or 'ANDROID_ARGUMENT' in os.environ


class DynamicPanel:
    """Dinamik durum paneli yöneticisi"""
    
    def __init__(self, colors, phone_info):
        self.colors = colors
        self.phone = phone_info
        self.is_online = True
        self.battery_percent = 100
        self.battery_charging = False
        
        # Panel bileşenleri
        self.time_text = ft.Text(
            datetime.now().strftime("%H:%M:%S"),
            size=16,
            weight=ft.FontWeight.BOLD,
            color=colors["text"],
        )
        
        self.battery_text = ft.Text(
            "%100",
            size=14,
            color=colors["success"],
        )
        
        self.battery_icon = ft.Icon(
            ft.icons.BATTERY_FULL,
            color=colors["success"],
            size=20,
        )
        
        self.status_dot = ft.Container(
            width=10,
            height=10,
            border_radius=5,
            bgcolor=colors["success"],
        )
        
        self.status_text = ft.Text(
            "Çevrimiçi",
            size=12,
            color=colors["text"],
        )
    
    def build(self):
        """Panel UI'sini oluştur"""
        return ft.Container(
            content=ft.Column([
                # Üst satır - Saat
                ft.Row([
                    ft.Icon(ft.icons.HOURGLASS_TOP, color=self.colors["accent"], size=18),
                    ft.Text("Canlı Saat:", color=self.colors["text_muted"], size=12),
                    self.time_text,
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Divider(height=1, color=self.colors["glass"]),
                ft.Container(height=5),
                
                # Alt satır - Batarya ve durum
                ft.Row([
                    # Batarya
                    ft.Row([
                        self.battery_icon,
                        self.battery_text,
                    ]),
                    
                    ft.Container(width=20),
                    
                    # Çevrimiçi durumu
                    ft.Row([
                        self.status_dot,
                        ft.Container(width=5),
                        self.status_text,
                    ]),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]),
            bgcolor=self.colors["glass"],
            border_radius=15,
            padding=15,
            animate=ft.animation.Animation(300),
            on_hover=self._on_hover,
        )
    
    def _on_hover(self, e):
        """Hover efekti"""
        if e.data == "true":
            e.control.scale = 1.02
            e.control.bgcolor = self.colors["glass_dark"]
        else:
            e.control.scale = 1.0
            e.control.bgcolor = self.colors["glass"]
        e.control.update()
    
    def start_updates(self, page):
        """Panel güncellemelerini başlat"""
        def update_loop():
            while True:
                try:
                    # Saati güncelle
                    self.time_text.value = datetime.now().strftime("%H:%M:%S")
                    
                    # Batarya bilgisini güncelle (Android'de)
                    if IS_ANDROID:
                        battery_info = self.phone.get_battery_info()
                        # Batarya yüzdesini parse et
                        if "%" in battery_info:
                            percent = battery_info.split("%")[0].split()[-1]
                            self.battery_text.value = f"%{percent}"
                            
                            # Şarj durumuna göre icon
                            if "Şarj" in battery_info:
                                self.battery_icon.name = ft.icons.BATTERY_CHARGING_FULL
                                self.battery_icon.color = self.colors["warning"]
                            else:
                                self.battery_icon.name = ft.icons.BATTERY_FULL
                                self.battery_icon.color = self.colors["success"]
                    
                    # Rastgele çevrimiçi durumu (her 30 saniyede bir)
                    if random.randint(1, 30) == 1:
                        self.is_online = not self.is_online
                        self.status_dot.bgcolor = (
                            self.colors["success"] if self.is_online 
                            else self.colors["error"]
                        )
                        self.status_text.value = (
                            "Çevrimiçi" if self.is_online 
                            else "Çevrimdışı"
                        )
                    
                    page.update()
                    time.sleep(1)  # Her saniye güncelle
                    
                except:
                    break
        
        threading.Thread(target=update_loop, daemon=True).start()
    
    def get_quick_stats(self):
        """Hızlı istatistik kartı"""
        return ft.Container(
            content=ft.Column([
                ft.Text("⚡ ANLIK DURUM", size=12, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Icon(ft.icons.MEMORY, size=14, color=self.colors["accent"]),
                    ft.Text("CPU: %45", size=11, color=self.colors["text"]),
                ]),
                ft.Row([
                    ft.Icon(ft.icons.STORAGE, size=14, color=self.colors["secondary"]),
                    ft.Text("RAM: 2.4/8GB", size=11, color=self.colors["text"]),
                ]),
            ]),
            bgcolor=self.colors["glass"],
            border_radius=10,
            padding=10,
            visible=False,  # İsteğe bağlı göster/gizle
        )