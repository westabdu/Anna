# main.py - A.N.N.A Mobile Ultimate (JARVIS THEME + Navigation Drawer)
"""
A.N.N.A Mobile Ultimate - Iron Man'in JARVIS'inden ilham alan asistan
- 🔐 Gelişmiş giriş sistemi (şifre + biyometrik)
- 🤖 Yapay zeka (Gemini, Groq)
- 🌤️ Hava durumu
- 📱 Telefon bilgileri
- 👤 Rehber yönetimi
- 📸 Gelişmiş OCR + AR + CANLI ÇEVİRİ
- ⏰ Hatırlatıcılar
- 📰 Haberler
- 🎤 Sesli komut + wake word ("Jarvis")
- 🕶️ Artırılmış Gerçeklik (AR)
- 🦾 JARVIS Teması (Iron Man)
- ℹ️ Hakkında sekmesi
- 📊 Sistem Monitörü
"""

import flet as ft
import threading
import time
import random
import sys
import os
from datetime import datetime
from pathlib import Path

# Android tespiti
IS_ANDROID = 'android' in sys.platform or 'ANDROID_ARGUMENT' in os.environ

# ============================================
# MOBİL MODÜLLER (Android uyumlu)
# ============================================
from src.auth.login import MobileAuth
from src.mobile_voice_enhanced import VoiceEngineEnhanced
from src.utils.theme import MobileTheme

# API modülleri (Android uyumlu)
from src.api.gemini import GeminiAI
from src.api.groq import GroqAI
from src.api.weather import WeatherAPI
from src.api.news import NewsAPI

# Mobil özel modüller (models klasöründen)
from src.models.phone import PhoneInfo
from src.models.reminders import ReminderManager
from src.models.contacts import ContactsManager
from src.models.ocr import OCRManager
from src.models.ar_vision import ARVision
from src.models.about import AboutManager
from src.models.system_monitor import SystemMonitor

# Animasyon ve efektler için ek modüller
from src.animations.splash_screen import SplashScreen
from src.animations.dashboard import DynamicPanel
from src.animations.wave_animation import WaveAnimation

# ============================================
# TEMA AYARLARI - JARVIS DARK (Iron Man)
# ============================================
colors = MobileTheme.current

# ============================================
# GİRİŞ EKRANI
# ============================================
class LoginScreen(ft.Container):
    def __init__(self, page, on_success):
        super().__init__()
        self.page = page
        self.on_success = on_success
        self.auth = MobileAuth()
        
        self.expand = True
        self.bgcolor = colors["bg_primary"]
        self.alignment = ft.alignment.center
        self.padding = 20
        
        # Ana kart - JARVIS HUD efekti
        login_card = ft.Container(
            width=350,
            padding=30,
            bgcolor=colors["glass"],
            border_radius=30,
            border=ft.border.all(2, colors["primary"] + "80"),
            shadow=ft.BoxShadow(
                spread_radius=10,
                blur_radius=20,
                color=colors["hud_glow"],
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        # Logo - JARVIS tarama efekti
        logo = ft.Container(
            content=ft.Stack([
                ft.Container(
                    width=100,
                    height=100,
                    border_radius=50,
                    gradient=ft.RadialGradient(
                        colors=[colors["primary"] + "40", "transparent"],
                    ),
                ),
                ft.Container(
                    content=ft.Icon(ft.icons.AUTO_AWESOME, color=colors["primary"], size=60),
                    width=100,
                    height=100,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    width=100,
                    height=100,
                    border_radius=50,
                    border=ft.border.all(2, colors["primary"] + "60"),
                    content=ft.Container(),
                ),
            ]),
            margin=ft.margin.only(bottom=10),
        )
        
        # Başlık - JARVIS stili
        title = ft.Text(
            "J.A.R.V.I.S",
            size=42,
            weight=ft.FontWeight.BOLD,
            color=colors["primary"],
            text_align=ft.TextAlign.CENTER,
            font_family="Monospace",
            spans=[
                ft.TextSpan(
                    " A.N.N.A",
                    style=ft.TextStyle(
                        color=colors["text"],
                        size=24,
                        weight=ft.FontWeight.NORMAL,
                    ),
                ),
            ],
        )
        
        subtitle = ft.Text(
            "Iron Man Mobil Asistanı",
            size=14,
            color=colors["text_muted"],
            italic=True,
        )
        
        # Giriş metodu seçici
        self.method_dropdown = ft.Dropdown(
            width=280,
            options=[
                ft.dropdown.Option("password", "🔑 Şifre"),
                ft.dropdown.Option("pin", "🔢 PIN Kodu"),
                ft.dropdown.Option("pattern", "🎨 Desen Kilidi"),
                ft.dropdown.Option("biometric", "👆 Parmak İzi"),
            ],
            value="password",
            border_color=colors["primary"] + "80",
            bgcolor=colors["bg_secondary"],
            text_style=ft.TextStyle(color=colors["text"]),
        )
        
        # Şifre/PIN alanı
        self.password_field = ft.TextField(
            hint_text="Şifrenizi girin",
            password=True,
            can_reveal_password=True,
            border_color=colors["primary"] + "80",
            focused_border_color=colors["accent"],
            text_style=ft.TextStyle(color=colors["text"]),
            bgcolor=colors["bg_secondary"],
            border_radius=30,
            content_padding=15,
            width=280,
            cursor_color=colors["accent"],
            cursor_width=2,
            visible=True,
        )
        
        # Desen alanı
        self.pattern_field = ft.TextField(
            hint_text="Deseni girin (örn: 123456789)",
            border_color=colors["primary"] + "80",
            focused_border_color=colors["accent"],
            text_style=ft.TextStyle(color=colors["text"]),
            bgcolor=colors["bg_secondary"],
            border_radius=30,
            content_padding=15,
            width=280,
            cursor_color=colors["accent"],
            cursor_width=2,
            visible=False,
        )
        
        # Giriş butonu - JARVIS stili
        login_btn = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.LOGIN, color=colors["text"], size=18),
                ft.Text("GİRİŞ YAP", color=colors["text"], weight=ft.FontWeight.BOLD, size=14),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            width=280,
            padding=12,
            gradient=ft.LinearGradient(
                colors=[colors["primary"], colors["secondary"]],
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            ),
            border_radius=30,
            animate=ft.animation.Animation(200),
            on_click=self.check_login,
        )
        
        # Biyometrik butonu
        self.bio_btn = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.FINGERPRINT, color=colors["primary"], size=18),
                ft.Text("Parmak İzi ile Giriş", color=colors["primary"], weight=ft.FontWeight.BOLD, size=14),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            width=280,
            padding=12,
            bgcolor="transparent",
            border=ft.border.all(2, colors["primary"] + "80"),
            border_radius=30,
            animate=ft.animation.Animation(200),
            on_click=self.check_biometric,
        )
        
        # Durum mesajı
        self.status_text = ft.Text("", color=colors["error"], size=12)
        
        # Loading - JARVIS döner HUD
        self.loading = ft.ProgressRing(
            width=40,
            height=40,
            color=colors["primary"],
            stroke_width=4,
            visible=False,
        )
        
        # Metod değiştirme
        def on_method_change(e):
            method = self.method_dropdown.value
            self.password_field.visible = (method in ["password", "pin"])
            self.pattern_field.visible = (method == "pattern")
            self.bio_btn.visible = (method == "biometric")
            self.update()
        
        self.method_dropdown.on_change = on_method_change
        
        # Layout
        login_card.content = ft.Column([
            logo,
            title,
            subtitle,
            ft.Container(height=20),
            self.method_dropdown,
            ft.Container(height=10),
            self.password_field,
            self.pattern_field,
            ft.Container(height=5),
            login_btn,
            ft.Container(height=5),
            self.bio_btn,
            ft.Container(height=15),
            self.status_text,
            ft.Container(height=5),
            self.loading,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
        
        self.content = ft.Container(content=login_card, alignment=ft.alignment.center)
    
    def check_login(self, e):
        method = self.method_dropdown.value
        
        if method == "password":
            if not self.password_field.value:
                self.status_text.value = "❌ Şifre girin!"
                self.status_text.update()
                return
            success, message = self.auth.check_password(self.password_field.value)
        
        elif method == "pin":
            if not self.password_field.value:
                self.status_text.value = "❌ PIN girin!"
                self.status_text.update()
                return
            success, message = self.auth.check_pin(self.password_field.value)
        
        elif method == "pattern":
            if not self.pattern_field.value:
                self.status_text.value = "❌ Desen girin!"
                self.status_text.update()
                return
            success, message = self.auth.check_pattern(self.pattern_field.value)
        
        elif method == "biometric":
            self.check_biometric(e)
            return
        
        else:
            success, message = False, "❌ Geçersiz metod"
        
        self.status_text.value = message
        self.status_text.color = colors["success"] if success else colors["error"]
        self.status_text.update()
        
        if success:
            self.loading.visible = True
            self.update()
            threading.Thread(target=lambda: (time.sleep(1), self.page.clean(), self.on_success()), daemon=True).start()
    
    def check_biometric(self, e):
        self.status_text.value = "🖐️ Parmak izi okutuluyor..."
        self.status_text.color = colors["info"]
        self.status_text.update()
        self.loading.visible = True
        self.update()
        
        def check():
            time.sleep(2)
            if self.auth.check_biometric():
                self.status_text.value = "✅ Giriş başarılı"
                self.status_text.update()
                time.sleep(0.5)
                self.page.clean()
                self.on_success()
            else:
                self.status_text.value = "❌ Parmak izi okunamadı"
                self.status_text.color = colors["error"]
                self.loading.visible = False
                self.update()
        
        threading.Thread(target=check, daemon=True).start()


# ============================================
# ANA UYGULAMA - NAVIGATION DRAWER İLE
# ============================================
def main(page: ft.Page):
    # Sayfa ayarları (Android için optimize)
    page.title = "J.A.R.V.I.S - A.N.N.A Mobile"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = colors["bg_primary"]
    page.padding = 0
    
    # Android ekran boyutları
    if IS_ANDROID:
        page.window_width = None
        page.window_height = None
    else:
        page.window_width = 400
        page.window_height = 800
    
    # ============================================
    # DURUM DEĞİŞKENLERİ
    # ============================================
    is_listening = False
    wake_active = False
    wave_active = False
    current_tab = "sohbet"
    current_theme = "jarvis_dark"
    
    # ============================================
    # GİRİŞ EKRANINI GÖSTER
    # ============================================
    def show_login():
        splash = SplashScreen(page, lambda: show_login_screen())
        splash.show()

    def show_login_screen():
        page.clean()
        page.add(LoginScreen(page, lambda: show_main_app()))
        page.update()
    
    # ============================================
    # ANA UYGULAMAYI BAŞLAT
    # ============================================
    def show_main_app():
        nonlocal is_listening, wake_active, wave_active, current_tab, current_theme
        
        # Core modülleri başlat
        voice = VoiceEngineEnhanced()
        if hasattr(voice, 'microphone') and voice.microphone:
            print("🎤 Mikrofon hazır")
        else:
            print("⚠️ Mikrofon bulunamadı, sesli komutlar çalışmayabilir.")
        
        voice.set_volume(0.8)
        voice.set_speed(1.2)
        voice.set_voice('tr-TR-DenizNeural')
        
        phone = PhoneInfo()
        system_monitor = SystemMonitor(colors, phone)
        reminders = ReminderManager()
        contacts = ContactsManager()
        ocr = OCRManager()
        weather_api = WeatherAPI()
        news_api = NewsAPI()
        ar_vision = ARVision()
        about = AboutManager()

        # Animasyon modülleri
        dashboard_panel = DynamicPanel(colors, phone)
        status_panel = dashboard_panel.build()
        dashboard_panel.start_updates(page)
        
        wave_anim = WaveAnimation(colors)
        wave_container = wave_anim.build(height=80)
        
        # AI seçimi
        groq = GroqAI()
        gemini = GeminiAI()
        
        if groq.available:
            ai = groq
            ai_name = "Groq AI (Çok Hızlı!)"
        elif gemini.available:
            ai = gemini
            ai_name = "Gemini AI"
        else:
            ai = None
            ai_name = "Yerel Mod (Sınırlı)"
        
        # UI bileşenleri
        chat_list = ft.ListView(spacing=10, auto_scroll=True, expand=True)
        
        # ============================================
        # FONKSİYONLAR
        # ============================================
        def add_message(sender: str, text: str, is_user: bool = True):
            color = colors["secondary"] if is_user else colors["primary"]
            icon = "👤" if is_user else "🤖"
            
            msg = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text(icon, size=18),
                        width=36, height=36,
                        alignment=ft.alignment.center,
                        bgcolor=colors["glass"],
                        border=ft.border.all(1, colors["primary"] + "40"),
                        border_radius=18,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text(sender, size=11, color=color, weight=ft.FontWeight.BOLD),
                            ft.Text(text, color=colors["text"], size=12, selectable=True),
                        ]),
                        bgcolor=colors["glass"],
                        border=ft.border.all(1, colors["primary"] + "20"),
                        border_radius=15,
                        padding=10,
                        expand=True,
                    ),
                ], alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START),
                margin=ft.margin.only(bottom=5),
            )
            
            chat_list.controls.append(msg)
            page.update()
        
        # Wake word callback
        def on_wake_word(word: str):
            add_message("JARVIS", f"🔊 '{word}' algılandı, dinliyorum...", is_user=False)
            voice.speak("Buyurun, dinliyorum.")
            wave_anim.start_listening()

            def listen_thread():
                komut = voice.listen(timeout=5)
                if komut:
                    wave_anim.start_speaking()
                    add_message("Sen", komut, is_user=True)
                    process_command(komut)
                else:
                    add_message("JARVIS", "⏰ Dinleme süresi doldu.", is_user=False)
                    voice.speak("Dinleme süresi doldu, tekrar deneyin.")
                    wave_anim.stop()

            threading.Thread(target=listen_thread, daemon=True).start()
        
        # Wake word toggle
        def toggle_wake(e):
            nonlocal wake_active
            if not wake_active:
                if voice.start_wake_word(on_wake_word):
                    wake_active = True
                    wake_btn.content.controls[0].name = ft.icons.MIC
                    wake_btn.content.controls[1].value = "Wake Açık"
                    wake_btn.border = ft.border.all(2, colors["success"])
                    wake_btn.bgcolor = colors["success"] + "20"
                    add_message("JARVIS", "Wake word aktif: 'Jarvis', 'Anna' veya 'Bilgisayar' deyin", is_user=False)
                    wave_anim.start_processing()
            else:
                voice.stop_wake_word()
                wake_active = False
                wake_btn.content.controls[0].name = ft.icons.MIC_OFF
                wake_btn.content.controls[1].value = "Wake Kapalı"
                wake_btn.border = ft.border.all(1, colors["error"] + "80")
                wake_btn.bgcolor = "transparent"
                add_message("JARVIS", "Wake word pasif", is_user=False)
                wave_anim.stop()
            
            page.update()
        
        # Sesli komut butonu
        def start_listening(e):
            nonlocal is_listening
            
            if is_listening:
                is_listening = False
                wave_anim.stop()
                listen_btn.content.controls[0].name = ft.icons.MIC_NONE
                listen_btn.content.controls[1].value = "Sesli Komut"
                listen_btn.bgcolor = "transparent"
                page.update()
                return
            
            is_listening = True
            listen_btn.content.controls[0].name = ft.icons.MIC
            listen_btn.content.controls[1].value = "Dinliyor..."
            listen_btn.bgcolor = colors["primary"] + "40"
            
            wave_anim.start_listening()
            page.update()
            
            def listen_thread():
                komut = voice.listen(timeout=5)
                
                def update_ui():
                    nonlocal is_listening
                    is_listening = False
                    listen_btn.content.controls[0].name = ft.icons.MIC_NONE
                    listen_btn.content.controls[1].value = "Sesli Komut"
                    listen_btn.bgcolor = "transparent"
                    
                    if komut:
                        wave_anim.start_speaking()
                        add_message("Sen", komut, is_user=True)
                        process_command(komut)
                    else:
                        wave_anim.stop()
                        add_message("JARVIS", "⏰ Dinleme süresi doldu.", is_user=False)
                    
                    page.update()
                
                page.run_thread(update_ui)
            
            threading.Thread(target=listen_thread, daemon=True).start()

        def change_tab(tab_name):
            nonlocal current_tab
            current_tab = tab_name
            update_content_area()
        
        # Komut işleme
        def process_command(text: str):
            text_lower = text.lower()
            
            if "ar başlat" in text_lower or "kamera aç" in text_lower:
                result = ar_vision.start_camera()
                add_message("JARVIS", result, is_user=False)
                voice.speak(result)
                change_tab("ar")
            
            elif "ar durdur" in text_lower or "kamera kapat" in text_lower:
                result = ar_vision.stop_camera()
                add_message("JARVIS", result, is_user=False)
                voice.speak(result)
            
            elif "fotoğraf çek" in text_lower:
                result = ar_vision.take_photo()
                if isinstance(result, dict):
                    if result.get('scan', {}).get('text'):
                        add_message("JARVIS", f"📝 Okunan: {result['scan']['text'][:100]}", is_user=False)
                    elif result.get('scan', {}).get('qr_codes'):
                        qr_text = result['scan']['qr_codes'][0]['data']
                        add_message("JARVIS", f"📱 QR: {qr_text}", is_user=False)
                    else:
                        add_message("JARVIS", "📸 Fotoğraf çekildi", is_user=False)
            
            elif "hava" in text_lower:
                result = weather_api.get_weather()
                add_message("JARVIS", result, is_user=False)
                voice.speak(result)
            
            elif "haber" in text_lower:
                categories = {
                    'teknoloji': 'technology',
                    'spor': 'sports',
                    'ekonomi': 'business',
                    'sağlık': 'health',
                    'bilim': 'science',
                    'eğlence': 'entertainment'
                }
                
                kategori_bulundu = False
                for tr_kelime, en_kategori in categories.items():
                    if tr_kelime in text_lower:
                        result = news_api.get_headlines(category=en_kategori)
                        add_message("JARVIS", result, is_user=False)
                        voice.speak(f"{tr_kelime} haberleri getiriliyor...")
                        kategori_bulundu = True
                        break
                
                if not kategori_bulundu:
                    result = news_api.get_headlines()
                    add_message("JARVIS", result, is_user=False)
                    voice.speak("Güncel haberler getiriliyor...")
            
            elif "batarya" in text_lower:
                result = phone.get_battery_info()
                add_message("JARVIS", result, is_user=False)
                voice.speak("Batarya bilgileri getiriliyor...")
            
            elif "depolama" in text_lower:
                result = phone.get_storage_info()
                add_message("JARVIS", result, is_user=False)
                voice.speak("Depolama bilgileri getiriliyor...")
            
            elif "rehber" in text_lower:
                result = contacts.format_contact_list()
                add_message("JARVIS", result, is_user=False)
                voice.speak("Rehber listeleniyor...")
            
            elif "fotoğraf oku" in text_lower or "resim oku" in text_lower:
                add_message("JARVIS", "📸 Kameradan fotoğraf çekiliyor...", is_user=False)
                voice.speak("Kameradan fotoğraf çekiyorum, lütfen bekleyin.")
                
                def ocr_thread():
                    result = ocr.camera_to_text()
                    if result.get('success'):
                        add_message("JARVIS", f"📝 {result['text'][:200]}", is_user=False)
                    else:
                        add_message("JARVIS", "❌ Yazı okunamadı", is_user=False)
                
                threading.Thread(target=ocr_thread, daemon=True).start()
            
            elif "hatırlat" in text_lower:
                import re
                minutes = 5
                match = re.search(r'(\d+)\s*dakika', text_lower)
                if match:
                    minutes = int(match.group(1))
                
                message = text.replace("hatırlat", "").strip()
                if message:
                    result = reminders.add_reminder("Hatırlatıcı", message, minutes)
                    add_message("JARVIS", result, is_user=False)
                    voice.speak(result)
            
            elif "yardım" in text_lower:
                help_text = """🤖 **JARVIS Komutları**

🕶️ AR: 'kamera aç', 'fotoğraf çek'
🌤️ Hava durumu
📰 Haberler
📱 Telefon bilgisi
👤 Rehber
📸 OCR: 'fotoğraf oku'
⏰ Hatırlatıcı
💬 Sohbet"""
                add_message("JARVIS", help_text, is_user=False)
                voice.speak("Size nasıl yardımcı olabilirim?")
            
            else:
                if ai:
                    try:
                        response = ai.ask(text)
                        add_message("JARVIS", response, is_user=False)
                        voice.speak(response)
                    except Exception as e:
                        error_msg = f"❌ AI hatası: {e}"
                        add_message("JARVIS", error_msg, is_user=False)
                        voice.speak("Üzgünüm, şu anda cevap veremiyorum.")
                else:
                    response = "Merhaba! API anahtarlarınızı kontrol edin veya 'yardım' yazın."
                    add_message("JARVIS", response, is_user=False)
                    voice.speak(response)
        
        # Mesaj gönderme
        def send_message(e):
            if not message_input.value:
                return
            
            msg = message_input.value
            message_input.value = ""
            page.update()
            
            add_message("Sen", msg, is_user=True)
            process_command(msg)
        
        # Tema değiştirici
        def change_theme(theme_name):
            nonlocal current_theme
            current_theme = theme_name
            MobileTheme.set_theme(theme_name)
            
            globals()["colors"] = MobileTheme.current
            
            page.clean()
            show_main_app()
        
        # ============================================
        # NAVIGATION DRAWER
        # ============================================
        def close_drawer(e):
            drawer.open = False
            page.update()
        
        def on_drawer_item_click(tab_name):
            nonlocal current_tab
            current_tab = tab_name
            close_drawer(None)
            update_content_area()
        
        def update_content_area():
            if current_tab == "sohbet":
                content_area.content = build_chat_tab()
            elif current_tab == "telefon":
                content_area.content = build_phone_tab()
            elif current_tab == "hava":
                content_area.content = build_weather_tab()
            elif current_tab == "rehber":
                content_area.content = build_contacts_tab()
            elif current_tab == "ar":
                content_area.content = build_ar_tab()
            elif current_tab == "monitor":
                content_area.content = build_monitor_tab()
            elif current_tab == "ayarlar":
                content_area.content = build_settings_tab()
            elif current_tab == "hakkimda":
                content_area.content = build_about_tab()
            page.update()
        
        # Drawer menü öğeleri
        drawer_items = [
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.CHAT, color=colors["primary"] if current_tab == "sohbet" else colors["text_muted"], size=24),
                        width=40,
                    ),
                    ft.Text("Sohbet", color=colors["primary"] if current_tab == "sohbet" else colors["text"], size=16, weight=ft.FontWeight.BOLD if current_tab == "sohbet" else ft.FontWeight.NORMAL),
                    ft.Container(expand=True),
                    ft.Container(
                        width=4,
                        height=24,
                        bgcolor=colors["primary"] if current_tab == "sohbet" else "transparent",
                        border_radius=2,
                    ),
                ]),
                padding=10,
                border_radius=10,
                on_click=lambda _: on_drawer_item_click("sohbet"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.PHONE_ANDROID, color=colors["primary"] if current_tab == "telefon" else colors["text_muted"], size=24),
                        width=40,
                    ),
                    ft.Text("Telefon", color=colors["primary"] if current_tab == "telefon" else colors["text"], size=16, weight=ft.FontWeight.BOLD if current_tab == "telefon" else ft.FontWeight.NORMAL),
                    ft.Container(expand=True),
                    ft.Container(
                        width=4,
                        height=24,
                        bgcolor=colors["primary"] if current_tab == "telefon" else "transparent",
                        border_radius=2,
                    ),
                ]),
                padding=10,
                border_radius=10,
                on_click=lambda _: on_drawer_item_click("telefon"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.WB_SUNNY, color=colors["primary"] if current_tab == "hava" else colors["text_muted"], size=24),
                        width=40,
                    ),
                    ft.Text("Hava Durumu", color=colors["primary"] if current_tab == "hava" else colors["text"], size=16, weight=ft.FontWeight.BOLD if current_tab == "hava" else ft.FontWeight.NORMAL),
                    ft.Container(expand=True),
                    ft.Container(
                        width=4,
                        height=24,
                        bgcolor=colors["primary"] if current_tab == "hava" else "transparent",
                        border_radius=2,
                    ),
                ]),
                padding=10,
                border_radius=10,
                on_click=lambda _: on_drawer_item_click("hava"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.CONTACTS, color=colors["primary"] if current_tab == "rehber" else colors["text_muted"], size=24),
                        width=40,
                    ),
                    ft.Text("Rehber", color=colors["primary"] if current_tab == "rehber" else colors["text"], size=16, weight=ft.FontWeight.BOLD if current_tab == "rehber" else ft.FontWeight.NORMAL),
                    ft.Container(expand=True),
                    ft.Container(
                        width=4,
                        height=24,
                        bgcolor=colors["primary"] if current_tab == "rehber" else "transparent",
                        border_radius=2,
                    ),
                ]),
                padding=10,
                border_radius=10,
                on_click=lambda _: on_drawer_item_click("rehber"),
            ),
            ft.Divider(height=1, color=colors["primary"] + "40"),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.VIEW_IN_AR, color=colors["primary"] if current_tab == "ar" else colors["text_muted"], size=24),
                        width=40,
                    ),
                    ft.Text("AR Vision", color=colors["primary"] if current_tab == "ar" else colors["text"], size=16, weight=ft.FontWeight.BOLD if current_tab == "ar" else ft.FontWeight.NORMAL),
                    ft.Container(expand=True),
                    ft.Container(
                        width=4,
                        height=24,
                        bgcolor=colors["primary"] if current_tab == "ar" else "transparent",
                        border_radius=2,
                    ),
                ]),
                padding=10,
                border_radius=10,
                on_click=lambda _: on_drawer_item_click("ar"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.ANALYTICS, color=colors["primary"] if current_tab == "monitor" else colors["text_muted"], size=24),
                        width=40,
                    ),
                    ft.Text("Sistem Monitörü", color=colors["primary"] if current_tab == "monitor" else colors["text"], size=16, weight=ft.FontWeight.BOLD if current_tab == "monitor" else ft.FontWeight.NORMAL),
                    ft.Container(expand=True),
                    ft.Container(
                        width=4,
                        height=24,
                        bgcolor=colors["primary"] if current_tab == "monitor" else "transparent",
                        border_radius=2,
                    ),
                ]),
                padding=10,
                border_radius=10,
                on_click=lambda _: on_drawer_item_click("monitor"),
            ),
            ft.Divider(height=1, color=colors["primary"] + "40"),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.SETTINGS, color=colors["primary"] if current_tab == "ayarlar" else colors["text_muted"], size=24),
                        width=40,
                    ),
                    ft.Text("Ayarlar", color=colors["primary"] if current_tab == "ayarlar" else colors["text"], size=16, weight=ft.FontWeight.BOLD if current_tab == "ayarlar" else ft.FontWeight.NORMAL),
                    ft.Container(expand=True),
                    ft.Container(
                        width=4,
                        height=24,
                        bgcolor=colors["primary"] if current_tab == "ayarlar" else "transparent",
                        border_radius=2,
                    ),
                ]),
                padding=10,
                border_radius=10,
                on_click=lambda _: on_drawer_item_click("ayarlar"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.INFO, color=colors["primary"] if current_tab == "hakkimda" else colors["text_muted"], size=24),
                        width=40,
                    ),
                    ft.Text("Hakkında", color=colors["primary"] if current_tab == "hakkimda" else colors["text"], size=16, weight=ft.FontWeight.BOLD if current_tab == "hakkimda" else ft.FontWeight.NORMAL),
                    ft.Container(expand=True),
                    ft.Container(
                        width=4,
                        height=24,
                        bgcolor=colors["primary"] if current_tab == "hakkimda" else "transparent",
                        border_radius=2,
                    ),
                ]),
                padding=10,
                border_radius=10,
                on_click=lambda _: on_drawer_item_click("hakkimda"),
            ),
        ]
        
        # Drawer başlığı
        drawer_header = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Stack([
                        ft.Container(
                            width=70,
                            height=70,
                            border_radius=35,
                            gradient=ft.RadialGradient(
                                colors=[colors["primary"] + "60", "transparent"],
                            ),
                        ),
                        ft.Container(
                            content=ft.Icon(ft.icons.AUTO_AWESOME, color=colors["primary"], size=50),
                            width=70,
                            height=70,
                            alignment=ft.alignment.center,
                        ),
                    ]),
                    alignment=ft.alignment.center,
                ),
                ft.Text("J.A.R.V.I.S", size=24, weight=ft.FontWeight.BOLD, color=colors["primary"]),
                ft.Text("A.N.N.A Mobile", size=14, color=colors["text_muted"]),
                ft.Text(f"v{about.version}", size=12, color=colors["text_muted"]),
                ft.Container(height=10),
                ft.Divider(height=1, color=colors["primary"] + "40"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=colors["glass"],
        )
        
        # Drawer oluştur
        drawer = ft.NavigationDrawer(
            controls=[
                drawer_header,
                ft.Container(
                    content=ft.Column(drawer_items, spacing=2),
                    padding=10,
                ),
            ],
            bgcolor=colors["bg_secondary"],
            elevation=20,
        )
        
        page.drawer = drawer
        
        def open_drawer(e):
            page.show_drawer(drawer)
        
        # ============================================
        # TAB İÇERİKLERİ
        # ============================================
        def build_monitor_tab():
            monitor_card = system_monitor.build()
            system_monitor.start_monitoring(page)

            def show_details(e):
                details = system_monitor.get_detailed_info()
                show_detail_dialog("📊 Detaylı Sistem Bilgisi", details)

            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.ANALYTICS, color=colors["primary"], size=24),
                            ft.Text("SİSTEM MONİTÖRÜ", size=18, weight=ft.FontWeight.BOLD, color=colors["text"]),
                        ]),
                        ft.Text("Canlı grafikler ve anlık takip", size=11, color=colors["text_muted"]),
                        ft.Divider(height=1, color=colors["primary"] + "40"),
                        ft.Container(height=10),
                        monitor_card,
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "📈 Detaylı İstatistikler",
                            icon=ft.icons.ANALYTICS,
                            on_click=show_details,
                            style=ft.ButtonStyle(
                                bgcolor=colors["primary"],
                                color=colors["text"],
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                        ft.Container(height=5),
                        ft.Text(
                            "🔄 Veriler her saniye güncellenir",
                            color=colors["text_muted"],
                            size=10,
                            italic=True,
                        ),
                    ]),
                    padding=15,
                )
            ], scroll=ft.ScrollMode.AUTO)
        
        def build_chat_tab():
            return ft.Column([
                ft.Container(content=chat_list, expand=True),
            ], expand=True)
        
        def build_phone_tab():
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.PHONE_ANDROID, color=colors["primary"], size=24),
                            ft.Text("TELEFON BİLGİLERİ", size=16, weight=ft.FontWeight.BOLD, color=colors["text"]),
                        ]),
                        ft.Divider(height=1, color=colors["primary"] + "40"),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([ft.Icon(ft.icons.BATTERY_FULL, color=colors["success"]), ft.Text("Batarya", color=colors["text"], size=14)]),
                                ft.Text(phone.get_battery_info().replace("**", ""), color=colors["text_secondary"], size=12),
                            ]),
                            bgcolor=colors["glass"],
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=15,
                            padding=15,
                            margin=ft.margin.only(bottom=10),
                            on_click=lambda _: show_detail_dialog("Batarya", phone.get_battery_info()),
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([ft.Icon(ft.icons.STORAGE, color=colors["primary"]), ft.Text("Depolama", color=colors["text"], size=14)]),
                                ft.Text(phone.get_storage_info().replace("**", ""), color=colors["text_secondary"], size=12),
                            ]),
                            bgcolor=colors["glass"],
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=15,
                            padding=15,
                            margin=ft.margin.only(bottom=10),
                            on_click=lambda _: show_detail_dialog("Depolama", phone.get_storage_info()),
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([ft.Icon(ft.icons.MEMORY, color=colors["accent"]), ft.Text("RAM", color=colors["text"], size=14)]),
                                ft.Text(phone.get_ram_info().replace("**", ""), color=colors["text_secondary"], size=12),
                            ]),
                            bgcolor=colors["glass"],
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=15,
                            padding=15,
                            margin=ft.margin.only(bottom=10),
                            on_click=lambda _: show_detail_dialog("RAM", phone.get_ram_info()),
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([ft.Icon(ft.icons.SPEED, color=colors["warning"]), ft.Text("İşlemci", color=colors["text"], size=14)]),
                                ft.Text(phone.get_cpu_info().replace("**", ""), color=colors["text_secondary"], size=12),
                            ]),
                            bgcolor=colors["glass"],
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=15,
                            padding=15,
                            on_click=lambda _: show_detail_dialog("İşlemci", phone.get_cpu_info()),
                        ),
                    ]),
                    padding=10,
                )
            ], scroll=ft.ScrollMode.AUTO)
        
        def build_weather_tab():
            city_input = ft.TextField(
                hint_text="Şehir adı",
                border_color=colors["primary"] + "80",
                focused_border_color=colors["accent"],
                text_style=ft.TextStyle(color=colors["text"]),
                bgcolor=colors["bg_secondary"],
                border_radius=30,
                content_padding=15,
                expand=True,
                cursor_color=colors["primary"],
            )
            
            weather_result = ft.Container(
                content=ft.Text("Hava durumu bilgisi burada görünecek", color=colors["text_muted"]),
                bgcolor=colors["glass"],
                border=ft.border.all(1, colors["primary"] + "20"),
                border_radius=15,
                padding=15,
            )
            
            def get_weather(e):
                if city_input.value:
                    result = weather_api.get_weather(city_input.value)
                    weather_result.content = ft.Text(result, color=colors["text"])
                    page.update()
            
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.WB_SUNNY, color=colors["primary"], size=24),
                            ft.Text("HAVA DURUMU", size=16, weight=ft.FontWeight.BOLD, color=colors["text"]),
                        ]),
                        ft.Divider(height=1, color=colors["primary"] + "40"),
                        ft.Container(height=10),
                        ft.Row([
                            city_input,
                            ft.IconButton(
                                icon=ft.icons.SEARCH,
                                icon_color=colors["primary"],
                                on_click=get_weather,
                            ),
                        ]),
                        ft.Container(height=10),
                        weather_result,
                    ]),
                    padding=10,
                )
            ], scroll=ft.ScrollMode.AUTO)
        
        def build_contacts_tab():
            search_input = ft.TextField(
                hint_text="Kişi ara...",
                border_color=colors["primary"] + "80",
                focused_border_color=colors["accent"],
                text_style=ft.TextStyle(color=colors["text"]),
                bgcolor=colors["bg_secondary"],
                border_radius=30,
                content_padding=15,
                expand=True,
                cursor_color=colors["primary"],
            )
            
            contacts_list = ft.ListView(spacing=5, expand=True)
            
            def refresh_contacts():
                contacts_list.controls.clear()
                for c in contacts.get_all_contacts()[:10]:
                    fav = "⭐ " if c.get('favorite') else ""
                    contacts_list.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Text(fav + c['name'][0].upper(), size=16, color=colors["text"]),
                                    width=40, height=40,
                                    alignment=ft.alignment.center,
                                    bgcolor=colors["primary"] + "40",
                                    border=ft.border.all(1, colors["primary"] + "40"),
                                    border_radius=20,
                                ),
                                ft.Column([
                                    ft.Text(fav + c['name'], size=14, weight=ft.FontWeight.BOLD, color=colors["text"]),
                                    ft.Text(c['phone'], size=11, color=colors["text_muted"]),
                                ], spacing=2, expand=True),
                                ft.IconButton(
                                    icon=ft.icons.CALL,
                                    icon_color=colors["success"],
                                    on_click=lambda _, cid=c['id']: show_contact_dialog(cid),
                                ),
                            ]),
                            bgcolor=colors["glass"],
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=10,
                            padding=10,
                            margin=ft.margin.only(bottom=5),
                        )
                    )
                page.update()
            
            def search_contacts(e):
                if search_input.value:
                    results = contacts.search_contacts(search_input.value)
                    contacts_list.controls.clear()
                    for c in results:
                        fav = "⭐ " if c.get('favorite') else ""
                        contacts_list.controls.append(
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(
                                        content=ft.Text(fav + c['name'][0].upper(), size=16),
                                        width=40, height=40,
                                        alignment=ft.alignment.center,
                                        bgcolor=colors["primary"] + "40",
                                        border=ft.border.all(1, colors["primary"] + "40"),
                                        border_radius=20,
                                    ),
                                    ft.Column([
                                        ft.Text(fav + c['name'], size=14, weight=ft.FontWeight.BOLD),
                                        ft.Text(c['phone'], size=11, color=colors["text_muted"]),
                                    ], spacing=2, expand=True),
                                ]),
                                bgcolor=colors["glass"],
                                border=ft.border.all(1, colors["primary"] + "20"),
                                border_radius=10,
                                padding=10,
                                margin=ft.margin.only(bottom=5),
                            )
                        )
                    page.update()
            
            refresh_contacts()
            
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.CONTACTS, color=colors["primary"], size=24),
                            ft.Text("REHBER", size=16, weight=ft.FontWeight.BOLD, color=colors["text"]),
                        ]),
                        ft.Divider(height=1, color=colors["primary"] + "40"),
                        ft.Container(height=10),
                        ft.Row([
                            search_input,
                            ft.IconButton(icon=ft.icons.SEARCH, icon_color=colors["primary"], on_click=search_contacts),
                        ]),
                        ft.Container(height=10),
                        ft.Row([
                            ft.Container(
                                content=ft.Text("📋 Tümü", color=colors["text"]),
                                bgcolor=colors["glass"], 
                                border=ft.border.all(1, colors["primary"] + "40"),
                                border_radius=15, 
                                padding=5,
                                on_click=lambda _: refresh_contacts(),
                            ),
                            ft.Container(width=5),
                            ft.Container(
                                content=ft.Text("⭐ Favoriler", color=colors["text"]),
                                bgcolor=colors["glass"], 
                                border=ft.border.all(1, colors["primary"] + "40"),
                                border_radius=15, 
                                padding=5,
                                on_click=lambda _: show_favorites(),
                            ),
                        ]),
                        ft.Container(height=10),
                        contacts_list,
                    ]),
                    padding=10, expand=True,
                )
            ], expand=True)
        
        def build_settings_tab():
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.SETTINGS, color=colors["primary"], size=24),
                            ft.Text("AYARLAR", size=16, weight=ft.FontWeight.BOLD, color=colors["text"]),
                        ]),
                        ft.Divider(height=1, color=colors["primary"] + "40"),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([ft.Icon(ft.icons.COLOR_LENS, color=colors["accent"]), ft.Text("Tema", color=colors["text"], size=14)]),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Text("🌙 JARVIS Dark", color=colors["text"], size=12), 
                                        bgcolor=colors["glass"], 
                                        border=ft.border.all(1, colors["primary"] + "40"),
                                        border_radius=10, 
                                        padding=5, 
                                        on_click=lambda _: change_theme("jarvis_dark")
                                    ),
                                    ft.Container(width=5),
                                    ft.Container(
                                        content=ft.Text("🔴 JARVIS Red", color=colors["text"], size=12), 
                                        bgcolor=colors["glass"], 
                                        border=ft.border.all(1, colors["primary"] + "40"),
                                        border_radius=10, 
                                        padding=5, 
                                        on_click=lambda _: change_theme("jarvis_red")
                                    ),
                                    ft.Container(width=5),
                                    ft.Container(
                                        content=ft.Text("🔵 JARVIS Blue", color=colors["text"], size=12), 
                                        bgcolor=colors["glass"], 
                                        border=ft.border.all(1, colors["primary"] + "40"),
                                        border_radius=10, 
                                        padding=5, 
                                        on_click=lambda _: change_theme("jarvis_blue")
                                    ),
                                ]),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Text("⚪ JARVIS White", color=colors["text"], size=12), 
                                        bgcolor=colors["glass"], 
                                        border=ft.border.all(1, colors["primary"] + "40"),
                                        border_radius=10, 
                                        padding=5, 
                                        on_click=lambda _: change_theme("jarvis_white")
                                    ),
                                ]),
                            ]),
                            bgcolor=colors["glass"], 
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=15, 
                            padding=15, 
                            margin=ft.margin.only(bottom=10),
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([ft.Icon(ft.icons.INFO, color=colors["primary"]), ft.Text("AI Modeli", color=colors["text"], size=14)]),
                                ft.Text(f"Kullanılan: {ai_name}", color=colors["text_secondary"], size=12),
                            ]),
                            bgcolor=colors["glass"], 
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=15, 
                            padding=15, 
                            margin=ft.margin.only(bottom=10),
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([ft.Icon(ft.icons.NOTIFICATIONS, color=colors["warning"]), ft.Text("Hatırlatıcılar", color=colors["text"], size=14)]),
                                ft.Text(reminders.list_reminders().replace("**", ""), color=colors["text_secondary"], size=12),
                            ]),
                            bgcolor=colors["glass"], 
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=15, 
                            padding=15, 
                            margin=ft.margin.only(bottom=10),
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([ft.Icon(ft.icons.DOCUMENT_SCANNER, color=colors["success"]), ft.Text("OCR", color=colors["text"], size=14)]),
                                ft.Text("Gelişmiş OCR ile fotoğraftan yazı oku", color=colors["text_secondary"], size=12),
                            ]),
                            bgcolor=colors["glass"], 
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=15, 
                            padding=15,
                        ),
                    ]),
                    padding=10,
                )
            ], scroll=ft.ScrollMode.AUTO)
        
        def build_ar_tab():
            camera_view = ft.Container(
                content=ft.Text("📷 Kamera görüntüsü burada olacak\n(AR aktif değil)", 
                               color=colors["text_muted"], size=12, text_align=ft.TextAlign.CENTER),
                bgcolor=colors["bg_secondary"],
                border=ft.border.all(1, colors["primary"] + "20"),
                border_radius=15,
                height=250,
                alignment=ft.alignment.center,
            )
            
            result_text = ft.Container(
                content=ft.Text("Sonuçlar burada görünecek", color=colors["text_muted"]),
                bgcolor=colors["glass"],
                border=ft.border.all(1, colors["primary"] + "20"),
                border_radius=15,
                padding=15,
                height=120,
            )
            
            translation_result = ft.Container(
                content=ft.Text("Çeviri burada görünecek", color=colors["text_muted"]),
                bgcolor=colors["glass"],
                border=ft.border.all(1, colors["success"] + "40"),
                border_radius=15,
                padding=15,
                height=80,
                visible=False,
            )
            
            mode_dropdown = ft.Dropdown(
                options=[
                    ft.dropdown.Option("ocr", "📝 OCR (Yazı Tanıma)"),
                    ft.dropdown.Option("qr", "📱 QR/Barkod"),
                    ft.dropdown.Option("face", "👤 Yüz Tanıma"),
                    ft.dropdown.Option("color", "🎨 Renk Analizi"),
                    ft.dropdown.Option("translate", "🌍 CANLI ÇEVİRİ"),
                ],
                value="ocr",
                border_color=colors["primary"] + "80",
                bgcolor=colors["bg_secondary"],
                text_style=ft.TextStyle(color=colors["text"]),
                width=200,
            )
            
            def start_ar(e):
                result = ar_vision.start_camera()
                camera_view.content = ft.Text("📷 Kamera aktif - AR çalışıyor", 
                                             color=colors["success"], weight=ft.FontWeight.BOLD)
                page.update()
                show_notification(result, "info")
            
            def stop_ar(e):
                result = ar_vision.stop_camera()
                camera_view.content = ft.Text("📷 Kamera görüntüsü burada olacak\n(AR aktif değil)", 
                                             color=colors["text_muted"], text_align=ft.TextAlign.CENTER)
                translation_result.visible = False
                page.update()
                show_notification(result, "info")
            
            def capture_and_scan(e):
                if not ar_vision.camera_active:
                    show_notification("❌ Önce kamerayı başlatın", "error")
                    return
                
                result = ar_vision.take_photo()
                if isinstance(result, dict) and result.get('success'):
                    scan = result.get('scan', {})
                    
                    if scan.get('text'):
                        result_text.content = ft.Column([
                            ft.Text(f"📝 {scan['text'][:200]}", color=colors["text"], size=12),
                        ])
                        
                        if scan.get('translation') and scan['translation'].get('success'):
                            trans = scan['translation']
                            translation_result.content = ft.Column([
                                ft.Row([
                                    ft.Text(f"🔤 {trans.get('src_lang_name', 'Bilinmiyor')}:", 
                                           color=colors["text_muted"], size=10),
                                    ft.Text(trans['original'][:50], color=colors["text"], size=11),
                                ]),
                                ft.Row([
                                    ft.Text("🇹🇷 Çeviri:", color=colors["success"], size=11, weight=ft.FontWeight.BOLD),
                                    ft.Text(trans['translated'][:100], color=colors["text"], size=12),
                                ]),
                            ])
                            translation_result.visible = True
                            voice.speak(f"Çeviri: {trans['translated'][:100]}")
                        else:
                            translation_result.visible = False
                    elif scan.get('qr_codes'):
                        qr = scan['qr_codes'][0]['data']
                        result_text.content = ft.Text(f"📱 QR: {qr[:200]}", color=colors["text"])
                        translation_result.visible = False
                    else:
                        result_text.content = ft.Text("📸 Fotoğraf çekildi, içerik bulunamadı", 
                                                    color=colors["text_muted"])
                        translation_result.visible = False
                    
                    show_notification("Fotoğraf çekildi", "success")
                else:
                    show_notification("❌ Fotoğraf çekilemedi", "error")
                
                page.update()
            
            def capture_and_translate(e):
                if not ar_vision.camera_active:
                    show_notification("❌ Önce kamerayı başlatın", "error")
                    return
                
                show_notification("🌍 Fotoğraf çekiliyor ve çevriliyor...", "info")
                result = ar_vision.take_photo()
                
                if isinstance(result, dict) and result.get('success'):
                    scan = result.get('scan', {})
                    
                    if scan.get('text'):
                        result_text.content = ft.Text(f"📝 {scan['text'][:200]}", color=colors["text"])
                        
                        if scan.get('translation') and scan['translation'].get('success'):
                            trans = scan['translation']
                            translation_result.content = ft.Column([
                                ft.Row([
                                    ft.Text(f"🔤 {trans.get('src_lang_name', 'Bilinmiyor')}:", 
                                           color=colors["text_muted"], size=10),
                                    ft.Text(trans['original'][:50], color=colors["text"], size=11),
                                ]),
                                ft.Row([
                                    ft.Icon(ft.icons.TRANSLATE, color=colors["success"], size=14),
                                    ft.Text(trans['translated'][:150], color=colors["success"], 
                                           size=14, weight=ft.FontWeight.BOLD),
                                ]),
                            ])
                            translation_result.visible = True
                            voice.speak(f"Çeviri: {trans['translated'][:100]}")
                        else:
                            translation_result.content = ft.Text("❌ Çeviri yapılamadı", 
                                                                color=colors["error"])
                            translation_result.visible = True
                    else:
                        result_text.content = ft.Text("📭 Resimde yazı bulunamadı", 
                                                    color=colors["text_muted"])
                        translation_result.visible = False
                    
                    show_notification("🌍 Çeviri tamamlandı", "success")
                else:
                    show_notification("❌ Fotoğraf çekilemedi", "error")
                
                page.update()
            
            def change_mode(e):
                mode = mode_dropdown.value
                result = ar_vision.set_mode(mode)
                show_notification(result, "info")
                
                if mode == "translate":
                    capture_btn.text = "🌍 Çek & Çevir"
                    capture_btn.icon = ft.icons.TRANSLATE
                    capture_btn.on_click = capture_and_translate
                    capture_btn.style.bgcolor = colors["success"]
                else:
                    capture_btn.text = "📸 Çek & Tara"
                    capture_btn.icon = ft.icons.CAMERA_ALT
                    capture_btn.on_click = capture_and_scan
                    capture_btn.style.bgcolor = colors["primary"]
                
                translation_result.visible = False
                page.update()
            
            def quick_scan(e):
                if not ar_vision.camera_active:
                    show_notification("❌ Önce kamerayı başlatın", "error")
                    return
                
                show_notification("📸 Fotoğraf çekiliyor...", "info")
                result = ar_vision.take_photo()
                if isinstance(result, dict) and result.get('success') and result.get('scan', {}).get('text'):
                    text = result['scan']['text'][:200]
                    result_text.content = ft.Text(f"📝 {text}", color=colors["text"])
                    voice.speak(f"Okunan metin: {text[:50]}")
                page.update()
            
            start_btn = ft.ElevatedButton(
                "▶️ Başlat",
                icon=ft.icons.PLAY_ARROW,
                on_click=start_ar,
                style=ft.ButtonStyle(
                    bgcolor=colors["success"],
                    color=colors["text"],
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                expand=True,
            )
            
            stop_btn = ft.ElevatedButton(
                "⏹️ Durdur",
                icon=ft.icons.STOP,
                on_click=stop_ar,
                style=ft.ButtonStyle(
                    bgcolor=colors["error"],
                    color=colors["text"],
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                expand=True,
            )
            
            capture_btn = ft.ElevatedButton(
                "📸 Çek & Tara",
                icon=ft.icons.CAMERA_ALT,
                on_click=capture_and_scan,
                style=ft.ButtonStyle(
                    bgcolor=colors["primary"],
                    color=colors["text"],
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                expand=True,
            )
            
            quick_scan_btn = ft.ElevatedButton(
                "⚡ Hızlı OCR",
                icon=ft.icons.DOCUMENT_SCANNER,
                on_click=quick_scan,
                style=ft.ButtonStyle(
                    bgcolor=colors["accent"],
                    color=colors["text"],
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                expand=True,
            )
            
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.VIEW_IN_AR, color=colors["primary"], size=24),
                            ft.Text("AR VİZYON", size=18, weight=ft.FontWeight.BOLD, color=colors["text"]),
                        ]),
                        ft.Text("Gelişmiş OCR ve Artırılmış Gerçeklik", size=11, color=colors["text_muted"]),
                        ft.Divider(height=1, color=colors["primary"] + "40"),
                        ft.Container(height=10),
                        camera_view,
                        ft.Container(height=10),
                        ft.Row([start_btn, stop_btn]),
                        ft.Container(height=10),
                        ft.Row([capture_btn, quick_scan_btn]),
                        ft.Container(height=10),
                        ft.Row([
                            ft.Text("Mod:", color=colors["text"], size=12),
                            mode_dropdown,
                            ft.IconButton(
                                icon=ft.icons.CHECK,
                                icon_color=colors["success"],
                                on_click=change_mode,
                                tooltip="Modu uygula",
                            ),
                        ]),
                        ft.Container(height=10),
                        ft.Text("📊 TARAMA SONUCU", size=14, weight=ft.FontWeight.BOLD, color=colors["text"]),
                        result_text,
                        ft.Container(height=5),
                        translation_result,
                        ft.Container(height=5),
                        ft.Text(
                            "💡 QR kod, barkod, yazı ve renkleri otomatik algılar. Çeviri modunda Japonca tabelaları Türkçe'ye çevirir.",
                            color=colors["text_muted"],
                            size=10,
                            italic=True,
                        ),
                    ]),
                    padding=15,
                )
            ], scroll=ft.ScrollMode.AUTO)
        
        def build_about_tab():
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.INFO, color=colors["primary"], size=24),
                            ft.Text("HAKKINDA", size=18, weight=ft.FontWeight.BOLD, color=colors["text"]),
                        ]),
                        ft.Divider(height=1, color=colors["primary"] + "40"),
                        ft.Container(height=20),
                        ft.Container(
                            content=ft.Stack([
                                ft.Container(
                                    width=100,
                                    height=100,
                                    border_radius=50,
                                    gradient=ft.RadialGradient(
                                        colors=[colors["primary"] + "80", "transparent"],
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Icon(ft.icons.AUTO_AWESOME, color=colors["primary"], size=60),
                                    width=100,
                                    height=100,
                                    alignment=ft.alignment.center,
                                ),
                                ft.Container(
                                    width=100,
                                    height=100,
                                    border_radius=50,
                                    border=ft.border.all(2, colors["primary"] + "60"),
                                ),
                            ]),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(height=20),
                        ft.Text("J.A.R.V.I.S", size=28, weight=ft.FontWeight.BOLD, color=colors["primary"]),
                        ft.Text("A.N.N.A Mobile", size=16, color=colors["text"]),
                        ft.Text(f"Versiyon {about.version}", size=14, color=colors["text_muted"], italic=True),
                        ft.Container(height=30),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.icons.INFO, color=colors["primary"], size=20),
                                    ft.Text("Geliştirici: ", size=14, color=colors["text"], weight=ft.FontWeight.BOLD),
                                    ft.Text(about.developer, color=colors["text_secondary"], size=12),
                                ]),
                                ft.Divider(height=1, color=colors["glass"] + "40"),
                                ft.Row([
                                    ft.Icon(ft.icons.CALENDAR_MONTH, color=colors["primary"], size=20),
                                    ft.Text("Tarih: ", size=14, color=colors["text"], weight=ft.FontWeight.BOLD),
                                    ft.Text(about.last_updated, color=colors["text_secondary"], size=12),
                                ]),
                                ft.Divider(height=1, color=colors["glass"] + "40"),
                                ft.Row([
                                    ft.Icon(ft.icons.PHONE_ANDROID, color=colors["success"], size=20),
                                    ft.Text("Uyumluluk: ", size=14, color=colors["text"], weight=ft.FontWeight.BOLD),
                                    ft.Text(about.platform, color=colors["text_secondary"], size=12),
                                ]),
                            ]),
                            bgcolor=colors["glass"],
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=15,
                            padding=15,
                        ),
                        ft.Container(height=20),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("📋 ÖZELLİKLER", size=14, weight=ft.FontWeight.BOLD, color=colors["text"]),
                                ft.Divider(height=1, color=colors["primary"] + "40"),
                                ft.Container(height=5),
                                ft.Text("• 🔐 Gelişmiş giriş sistemi", color=colors["text_secondary"], size=12),
                                ft.Text("• 🤖 Yapay Zeka (Gemini/Groq)", color=colors["text_secondary"], size=12),
                                ft.Text("• 🌤️ Hava durumu", color=colors["text_secondary"], size=12),
                                ft.Text("• 📱 Telefon bilgileri", color=colors["text_secondary"], size=12),
                                ft.Text("• 👤 Rehber yönetimi", color=colors["text_secondary"], size=12),
                                ft.Text("• 📸 OCR ve AR", color=colors["text_secondary"], size=12),
                                ft.Text("• ⏰ Hatırlatıcılar", color=colors["text_secondary"], size=12),
                                ft.Text("• 📰 Haberler", color=colors["text_secondary"], size=12),
                                ft.Text("• 🎤 Sesli komut", color=colors["text_secondary"], size=12),
                            ]),
                            bgcolor=colors["glass"],
                            border=ft.border.all(1, colors["primary"] + "20"),
                            border_radius=15,
                            padding=15,
                        ),
                        ft.Container(height=20),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.EMAIL,
                                icon_color=colors["primary"],
                                tooltip="E-posta ile iletişim",
                                on_click=lambda _: show_notification("İletişim: github.com/westabdu", "info"),
                            ),
                            ft.IconButton(
                                icon=ft.icons.CODE,
                                icon_color=colors["secondary"],
                                tooltip="GitHub sayfası",
                                on_click=lambda _: show_notification("GitHub: @westabdu", "info"),
                            ),
                            ft.IconButton(
                                icon=ft.icons.SHARE,
                                icon_color=colors["accent"],
                                tooltip="Paylaş",
                                on_click=lambda _: show_notification("J.A.R.V.I.S - A.N.N.A Mobile", "info"),
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=15,
                )
            ], scroll=ft.ScrollMode.AUTO)
        
        # Dialog fonksiyonları
        def show_detail_dialog(title: str, content: str):
            def close_dlg(e):
                dlg.open = False
                page.update()

            dlg = ft.AlertDialog(
                title=ft.Text(title, color=colors["primary"]),
                content=ft.Text(content, color=colors["text"]),
                actions=[
                    ft.TextButton("Kapat", on_click=close_dlg)
                ],
            )
            
            page.dialog = dlg
            dlg.open = True
            page.update()

        def show_contact_dialog(contact_id: int):
            contact_info = contacts.get_contact_card(contact_id)
            dlg = ft.AlertDialog(
                title=ft.Text("Kişi Detayı", color=colors["primary"]),
                content=ft.Text(contact_info, color=colors["text"]),
                actions=[
                    ft.TextButton("Ara", on_click=lambda _: call_contact(contact_id)),
                    ft.TextButton("Mesaj", on_click=lambda _: message_contact(contact_id)),
                    ft.TextButton("Kapat", on_click=lambda _: page.close(dlg)),
                ],
            )
            page.open(dlg)
        
        def call_contact(contact_id: int):
            result = contacts.call_contact(contact_id)
            add_message("JARVIS", result, is_user=False)
        
        def message_contact(contact_id: int):
            msg_input = ft.TextField(hint_text="Mesajınız", multiline=True)
            dlg = ft.AlertDialog(
                title=ft.Text("Mesaj Gönder", color=colors["primary"]),
                content=msg_input,
                actions=[
                    ft.TextButton("Gönder", on_click=lambda _: send_contact_message(contact_id, msg_input.value)),
                    ft.TextButton("İptal", on_click=lambda _: page.close(dlg)),
                ],
            )
            page.open(dlg)
        
        def send_contact_message(contact_id: int, message: str):
            if message:
                result = contacts.message_contact(contact_id, message)
                add_message("JARVIS", result, is_user=False)
        
        def show_favorites():
            favorites = contacts.get_favorites()
            fav_text = contacts.format_contact_list(favorites)
            dlg = ft.AlertDialog(
                title=ft.Text("⭐ Favoriler", color=colors["primary"]),
                content=ft.Text(fav_text, color=colors["text"]),
                actions=[ft.TextButton("Kapat", on_click=lambda _: page.close(dlg))],
            )
            page.open(dlg)
        
        def show_notification(message, type="info"):
            color_map = {
                "info": colors["info"],
                "success": colors["success"],
                "warning": colors["warning"],
                "error": colors["error"]
            }
            page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.icons.INFO, color=color_map[type]),
                    ft.Text(message, color=colors["text"]),
                ]),
                bgcolor=colors["glass_dark"],
                duration=2000,
            )
            page.snack_bar.open = True
            page.update()
        
        # ============================================
        # UI BİLEŞENLERİ
        # ============================================
        header = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.MENU,
                        icon_color=colors["primary"],
                        on_click=open_drawer,
                    ),
                    ft.Icon(ft.icons.AUTO_AWESOME, color=colors["primary"], size=24),
                    ft.Text("J.A.R.V.I.S", color=colors["text"], size=18, weight=ft.FontWeight.BOLD),
                ]),
                ft.Container(expand=True),
                status_panel,
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.BATTERY_FULL, color=colors["text_muted"], size=14),
                        ft.Text(datetime.now().strftime("%H:%M"), color=colors["text"], size=12),
                    ]),
                    bgcolor=colors["glass"], 
                    border=ft.border.all(1, colors["primary"] + "40"),
                    border_radius=15, 
                    padding=5,
                ),
            ]),
            bgcolor=colors["glass"], 
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(1, colors["primary"] + "40")),
        )
        
        wake_btn = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.MIC_OFF, color=colors["text"], size=16),
                ft.Text("Wake Kapalı", color=colors["text"], size=12, weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=8, 
            border=ft.border.all(1, colors["error"] + "80"), 
            border_radius=20,
            on_click=toggle_wake,
        )
        
        wave_area = ft.Container(content=wave_container, height=80, alignment=ft.alignment.center)
        
        message_input = ft.TextField(
            hint_text="Mesaj yazın...",
            border_color=colors["primary"] + "80", 
            focused_border_color=colors["accent"],
            text_style=ft.TextStyle(color=colors["text"]), 
            bgcolor=colors["bg_secondary"],
            border_radius=30, 
            content_padding=15, 
            expand=True, 
            on_submit=send_message,
            cursor_color=colors["primary"],
            cursor_width=2,
        )
        
        listen_btn = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.MIC_NONE, color=colors["primary"], size=16),
                ft.Text("Sesli Komut", color=colors["primary"], size=12, weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=8, 
            border=ft.border.all(1, colors["primary"] + "80"), 
            border_radius=20,
            on_click=start_listening,
        )
        
        send_btn = ft.Container(
            content=ft.Icon(ft.icons.SEND, color=colors["primary"], size=20),
            padding=10, 
            on_click=send_message,
        )
        
        content_area = ft.Container(content=build_chat_tab(), expand=True, padding=10)
        
        page.add(
            ft.Column([
                header,
                wave_area,
                content_area,
                ft.Container(
                    content=ft.Row([
                        wake_btn, ft.Container(width=5),
                        message_input, listen_btn, send_btn,
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=colors["glass"], 
                    padding=10,
                    border=ft.border.only(top=ft.BorderSide(1, colors["primary"] + "40")),
                ),
            ], expand=True)
        )
        
        add_message("JARVIS", f"Merhaba! Ben J.A.R.V.I.S, Iron Man'in asistanı. {ai_name} ile çalışıyorum.", is_user=False)
        add_message("JARVIS", "Sesli komut için 🎤 butonuna basın veya 'Jarvis' deyin", is_user=False)
        add_message("JARVIS", "Menüyü açmak için ☰ butonuna tıklayın.", is_user=False)
        add_message("JARVIS", "🌍 Yeni özellik: AR'de CANLI ÇEVİRİ ile Japonca tabelaları Türkçe'ye çevirin!", is_user=False)
    
    show_login()


if __name__ == "__main__":
    ft.app(target=main)