# src/modules/mobile_voice_enhanced.py - ANDROID UYUMLU
"""
A.N.N.A Mobile Gelişmiş Ses Motoru - JARVIS ENTEGRE
- 🎙️ Wake word (Jarvis, Bilgisayar, Alexa, ANNA)
- 🗣️ DOĞAL KADIN SESİ (Edge-TTS ile 5 farklı kadın sesi)
- 👂 Gelişmiş ses tanıma (Google Speech + offline yedek)
- 📊 Gerçek zamanlı ses seviyesi göstergesi
- 🔇 Sessiz mod
- 💬 Konuşma geçmişi ve analiz
- 🎚️ Ses tonu, hız, perde ayarları
- 📱 Android optimizasyonu
"""

import os
import sys
import asyncio
import tempfile
import threading
import queue
import time
import json
import re
from datetime import datetime
from pathlib import Path
import random

# Android tespiti
IS_ANDROID = 'android' in sys.platform or 'ANDROID_ARGUMENT' in os.environ

# Ses tanıma
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except:
    SR_AVAILABLE = False

# Ses sentezi
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except:
    GTTS_AVAILABLE = False

try:
    import edge_tts
    EDGE_AVAILABLE = True
except:
    EDGE_AVAILABLE = False

# Wake word
try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except:
    PORCUPINE_AVAILABLE = False

# Ses çalma
try:
    import pygame
    PYGAME_AVAILABLE = True
except:
    PYGAME_AVAILABLE = False

# Ses kayıt ve analiz
try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    SOUNDDEVICE_AVAILABLE = True
except:
    SOUNDDEVICE_AVAILABLE = False

# Ses efektleri
try:
    import audioop
    AUDIOOP_AVAILABLE = True
except:
    AUDIOOP_AVAILABLE = False


class VoiceEngineEnhanced:
    """
    A.N.N.A'nın Gelişmiş Ses Motoru - JARVIS'in kadın sesli asistanı
    """
    
    def __init__(self):
        # Android'de farklı depolama
        if IS_ANDROID:
            self.data_dir = Path("/storage/emulated/0/ANNA/voice")
        else:
            self.data_dir = Path("data/voice")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # ============================================
        # A.N.N.A'NIN DOĞAL KADIN SESLERİ (Edge-TTS)
        # ============================================
        self.voices = {
            # TÜRKÇE KADIN SESLERİ (En doğal olanlar)
            'tr-TR-EmelNeural': '👩 Emel (Doğal, Sıcak)',
            'tr-TR-DenizNeural': '🧑 Deniz (Samimi, Genç)',
            'tr-TR-BerrakNeural': '👩 Berrak (Profesyonel, Net)',
            'tr-TR-CemreNeural': '👧 Cemre (Enerjik, Canlı)',
            
            # YABANCI KADIN SESLERİ (Test için)
            'en-US-JennyNeural': '🇺🇸 Jenny (İngilizce)',
            'en-GB-LibbyNeural': '🇬🇧 Libby (İngiliz İngilizcesi)',
        }
        
        # A.N.N.A'nın varsayılan sesi - EN DOĞAL KADIN SESİ
        self.current_voice = 'tr-TR-EmelNeural'  # Deniz en doğal!
        
        # Yedek sesler (Edge çalışmazsa kullanılacak)
        self.fallback_voices = {
            'tr-TR-Standard-A': '🇹🇷 Standart Kadın',
            'tr-TR-Standard-B': '🇹🇷 Standart Kadın 2',
        }
        
        # ============================================
        # GELİŞMİŞ KONUŞMA AYARLARI
        # ============================================
        self.volume = 0.85  # Ses seviyesi (0.0-1.0)
        self.speed = 1.0     # Konuşma hızı (0.5-2.0)
        self.pitch = 1.0     # Ses perdesi (0.5-2.0)
        self.muted = False
        self.language = 'tr'
        
        # Duygu durumu (ses tonunu etkiler)
        self.emotion = {
            'mode': 'neutral',  # neutral, happy, sad, excited, calm
            'intensity': 1.0,
        }
        
        # Konuşma stilleri
        self.speech_styles = {
            'normal': {'speed': 1.0, 'pitch': 1.0, 'volume': 0.85},
            'hızlı': {'speed': 1.3, 'pitch': 1.1, 'volume': 0.9},
            'yavaş': {'speed': 0.8, 'pitch': 0.9, 'volume': 0.8},
            'resmi': {'speed': 0.9, 'pitch': 1.0, 'volume': 0.85},
            'samimi': {'speed': 1.1, 'pitch': 1.1, 'volume': 0.9},
            'fısıltı': {'speed': 0.7, 'pitch': 0.8, 'volume': 0.4},
        }
        
        # ============================================
        # TEMEL BİLEŞENLER
        # ============================================
        self.recognizer = sr.Recognizer() if SR_AVAILABLE else None
        self.microphone = None
        self._init_microphone()
        
        # Wake word
        self.porcupine = None
        self.wake_active = False
        self.wake_callback = None
        self.wake_keywords = ["jarvis", "computer", "alexa", "bilgisayar", "anna", "asistan"]
        self._init_wake_word()
        
        # Pygame mixer (ses çalma)
        if PYGAME_AVAILABLE:
            self._init_pygame_mixer()
        
        # Ses kuyruğu
        self.sound_queue = queue.Queue()
        self.is_playing = False
        self.sound_thread = threading.Thread(target=self._sound_worker, daemon=True)
        self.sound_thread.start()
        
        # Ön yüklenmiş ses efektleri
        self.sound_effects = {}
        self._preload_sound_effects()
        
        # Konuşma geçmişi
        self.history = []
        self.history_file = self.data_dir / "voice_history.json"
        self._load_history()
        
        # İstatistikler
        self.stats = {
            'words_spoken': 0,
            'sentences_spoken': 0,
            'listening_sessions': 0,
            'wake_word_triggers': 0,
            'total_speak_time': 0,
            'favorite_voice': self.current_voice,
        }
        
        # Ses tanıma için özel kelimeler
        self.custom_commands = {
            'merhaba': ['merhaba', 'selam', 'hey'],
            'nasılsın': ['nasılsın', 'naber', 'n\'aber'],
            'teşekkürler': ['teşekkürler', 'sağ ol', 'eyvallah'],
        }
        
        print("\n" + "="*60)
        print("🎤 A.N.N.A GELİŞMİŞ SES MOTORU - JARVIS ENTEGRE")
        print("="*60)
        print(f"🎙️ Ses Tanıma: {'✅' if SR_AVAILABLE else '❌'}")
        print(f"🔊 Edge-TTS: {'✅' if EDGE_AVAILABLE else '❌'}")
        print(f"🎵 Pygame: {'✅' if PYGAME_AVAILABLE else '❌'}")
        print(f"🎚️ Wake Word: {'✅' if PORCUPINE_AVAILABLE else '❌'}")
        print(f"📊 Ses Analizi: {'✅' if SOUNDDEVICE_AVAILABLE else '❌'}")
        print(f"📱 Android: {'✅' if IS_ANDROID else '❌'}")
        print("-"*60)
        print(f"🎙️ AKTİF SES: {self.voices[self.current_voice]}")
        print(f"🔊 Ses Seviyesi: %{int(self.volume * 100)}")
        print(f"⚡ Konuşma Hızı: {self.speed}x")
        print("="*60)
    
    def _init_pygame_mixer(self):
        """Pygame mixer'ı optimize et"""
        try:
            pygame.mixer.quit()
            if IS_ANDROID:
                # Android için optimize
                pygame.mixer.init(
                    frequency=22050,  # Daha yüksek kalite
                    size=-16,
                    channels=2,       # Stereo
                    buffer=512
                )
            else:
                pygame.mixer.init(
                    frequency=44100,  # CD kalitesi
                    size=-16,
                    channels=2,
                    buffer=1024
                )
            print("✅ Pygame mixer hazır (Yüksek kalite)")
        except Exception as e:
            print(f"⚠️ Pygame mixer hatası: {e}")
    
    def _preload_sound_effects(self):
        """Ses efektlerini ön yükle"""
        effects_dir = self.data_dir / "effects"
        effects_dir.mkdir(exist_ok=True)
        
        # Varsayılan efektler (ileride MP3 eklenebilir)
        self.sound_effects = {
            'notification': None,
            'error': None,
            'success': None,
            'wake': None,
            'sleep': None,
        }
    
    def _init_microphone(self):
        """Mikrofonu başlat (gelişmiş kalibrasyon)"""
        if not SR_AVAILABLE:
            print("❌ SpeechRecognition kütüphanesi yok! 'pip install SpeechRecognition' ile kurun.")
            return
        
        try:
            # Sistemdeki mikrofonları listele (debug için)
            if not IS_ANDROID:
                mics = sr.Microphone.list_microphone_names()
                if mics:
                    print(f"🎤 Bulunan mikrofonlar ({len(mics)}):")
                    for i, mic in enumerate(mics[:5]):  # İlk 5'i göster
                        print(f"   {i}: {mic}")
                else:
                    print("⚠️ Hiç mikrofon bulunamadı!")
            
            # Varsayılan mikrofonu al
            if IS_ANDROID:
                # Android'de genelde index 0 çalışır
                self.microphone = sr.Microphone(device_index=0)
            else:
                try:
                    self.microphone = sr.Microphone()
                except:
                    # Alternatif olarak ilk mikrofonu dene
                    self.microphone = sr.Microphone(device_index=0)
            
            # Mikrofonu test et
            with self.microphone as source:
                print("🎤 Mikrofon kalibre ediliyor...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold = 3000
                self.recognizer.dynamic_energy_threshold = True
                print(f"✅ Mikrofon hazır - Enerji eşiği: {self.recognizer.energy_threshold:.1f}")
                
        except AttributeError as e:
            print(f"❌ Mikrofon hatası: {e}")
            print("   Çözüm: pip install --upgrade SpeechRecognition PyAudio")
            self.microphone = None
        except OSError as e:
            print(f"❌ Mikrofon erişim hatası: {e}")
            print("   Android'de mikrofon izni verdiğinizden emin olun")
            self.microphone = None
        except Exception as e:
            print(f"❌ Mikrofon başlatma hatası: {e}")
            self.microphone = None
    
    def _init_wake_word(self):
        """Wake word sistemini başlat"""
        if not PORCUPINE_AVAILABLE:
            return
        
        access_key = os.getenv("PICOVOICE_ACCESS_KEY")
        if not access_key:
            print("⚠️ PICOVOICE_ACCESS_KEY yok, wake word çalışmaz")
            return
        
        try:
            self.porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=self.wake_keywords,
                sensitivities=[0.5] * len(self.wake_keywords)
            )
            print(f"✅ Wake word hazır: {', '.join(self.wake_keywords)}")
        except Exception as e:
            print(f"❌ Wake word hatası: {e}")
    
    def _sound_worker(self):
        """Ses çalma worker'ı (gelişmiş)"""
        while True:
            try:
                item = self.sound_queue.get(timeout=1)
                
                if isinstance(item, tuple) and len(item) == 4:
                    text, voice, speed, emotion = item
                elif isinstance(item, tuple) and len(item) == 3:
                    text, voice, speed = item
                    emotion = 'neutral'
                else:
                    text = str(item)
                    voice = self.current_voice
                    speed = self.speed
                    emotion = 'neutral'
                
                self.is_playing = True
                
                if not self.muted:
                    # Her konuşma için yeni event loop
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    # Duygu durumuna göre konuş
                    start_time = time.time()
                    loop.run_until_complete(
                        self._speak_async(text, voice, speed, emotion)
                    )
                    loop.close()
                    
                    # Konuşma süresini hesapla
                    speak_time = time.time() - start_time
                    self.stats['total_speak_time'] += speak_time
                    
                else:
                    print(f"🔇 [SESSİZ] A.N.N.A: {text[:100]}...")
                
                self.is_playing = False
                self.sound_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Ses worker hatası: {e}")
                self.is_playing = False
    
    async def _speak_async(self, text: str, voice: str = None, speed: float = 1.0, emotion: str = 'neutral'):
        """Asenkron konuşma (gelişmiş)"""
        voice = voice or self.current_voice
        temp_file = None
        
        try:
            # Metni temizle ve optimize et
            text = self._clean_text_for_speech(text)
            if not text:
                return
            
            # Kelime sayısını hesapla
            words = len(text.split())
            self.stats['words_spoken'] += words
            self.stats['sentences_spoken'] += 1
            
            # Konuşma geçmişine ekle
            self._add_to_history(text, voice, emotion)
            
            # Metni doğal konuşma için parçala (çok uzunsa)
            if words > 50:
                # Parçalara böl ve sırayla konuş
                parts = self._split_text_for_speech(text)
                for part in parts:
                    await self._speak_single(part, voice, speed, emotion)
                    await asyncio.sleep(0.3)  # Kısa bekleme
            else:
                # Tek parça konuş
                await self._speak_single(text, voice, speed, emotion)
            
        except Exception as e:
            print(f"❌ Ses sentezi hatası: {e}")
            print(f"🗣️ A.N.N.A: {text[:100]}...")
    
    async def _speak_single(self, text: str, voice: str, speed: float, emotion: str):
        """Tek parça konuşma"""
        temp_file = None
        
        # Önce Edge-TTS dene (en kaliteli)
        if EDGE_AVAILABLE:
            try:
                # Hız ve perde ayarı - DÜZELTİLDİ
                if speed > 1.0:
                    rate = f"+{int((speed - 1.0) * 100)}%"
                elif speed < 1.0:
                    rate = f"-{int((1.0 - speed) * 100)}%"
                else:
                    rate = "+0%"  # Normal hız
                
                # Duygu durumuna göre ses tonu
                if emotion == 'happy':
                    base_speed = speed * 1.1
                    if base_speed > 1.0:
                        rate = f"+{int((base_speed - 1.0) * 100)}%"
                elif emotion == 'calm':
                    base_speed = speed * 0.9
                    if base_speed < 1.0:
                        rate = f"-{int((1.0 - base_speed) * 100)}%"
                
                # Geçici dosya oluştur
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_file = fp.name
                
                # Edge-TTS ile sentez
                communicate = edge_tts.Communicate(text, voice, rate=rate)
                await communicate.save(temp_file)
                
                # Pygame ile çal
                if PYGAME_AVAILABLE and os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                    # Ses efektleri
                    if pygame.mixer.get_init():
                        pygame.mixer.music.load(temp_file)
                        pygame.mixer.music.set_volume(self.volume)
                        pygame.mixer.music.play()
                        
                        # Ses bitene kadar bekle
                        while pygame.mixer.music.get_busy():
                            await asyncio.sleep(0.1)
                        
                        # Geçici dosyayı sil
                        self._safe_delete(temp_file)
                        return
                    
            except Exception as e:
                print(f"⚠️ Edge-TTS hatası: {e}")
        
        # Edge yoksa veya hata verdiyse gTTS dene
        if GTTS_AVAILABLE:
            try:
                # gTTS için dil
                lang = 'tr' if voice.startswith('tr') else 'en'
                
                tts = gTTS(text=text, lang=lang, slow=(speed < 0.8))
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_file = fp.name
                
                tts.save(temp_file)
                
                if PYGAME_AVAILABLE and os.path.exists(temp_file):
                    # Hız ayarı (gTTS'de kısıtlı)
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.set_volume(self.volume)
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                        await asyncio.sleep(0.1)
                    
                    self._safe_delete(temp_file)
                    return
                    
            except Exception as e:
                print(f"⚠️ gTTS hatası: {e}")
        
        # Hiçbiri çalışmazsa konsola yaz
        print(f"🗣️ A.N.N.A: {text}")
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Konuşma için metni temizle ve optimize et"""
        if not text:
            return ""
        
        # Fazla boşlukları temizle
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Emojileri kaldır (konuşmada sorun çıkarabilir)
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        
        text = emoji_pattern.sub(r'', text)
        
        # Kısaltmaları düzelt
        replacements = {
            ':)': 'gülen yüz',
            ':(': 'üzgün yüz',
            '%': 'yüzde',
            '&': 've',
            '@': 'at',
            'www.': 'www nokta',
            '.com': 'nokta com',
        }
        
        for short, full in replacements.items():
            text = text.replace(short, full)
        
        return text
    
    def _split_text_for_speech(self, text: str, max_words: int = 30) -> list:
        """Uzun metni konuşma için parçalara böl"""
        words = text.split()
        if len(words) <= max_words:
            return [text]
        
        parts = []
        current_part = []
        
        for word in words:
            current_part.append(word)
            if len(current_part) >= max_words:
                # Cümle sonu bul
                if '.' in word or '?' in word or '!' in word:
                    parts.append(' '.join(current_part))
                    current_part = []
        
        if current_part:
            parts.append(' '.join(current_part))
        
        return parts
    
    def _safe_delete(self, file_path):
        """Güvenli dosya silme"""
        try:
            if file_path and os.path.exists(file_path):
                os.unlink(file_path)
        except:
            pass
    
    # ============================================
    # ANA KONUŞMA FONKSİYONLARI
    # ============================================
    
    def speak(self, text: str, wait: bool = False, emotion: str = 'neutral'):
        """
        A.N.N.A'nın doğal sesiyle konuş
        
        Args:
            text: Konuşulacak metin
            wait: Konuşma bitene kadar bekle
            emotion: Duygu durumu (neutral, happy, sad, excited, calm)
        """
        if not text:
            return
        
        # Kısa metinlerde direkt yazdır
        if len(text) < 100:
            print(f"🗣️ A.N.N.A: {text}")
        else:
            print(f"🗣️ A.N.N.A: {text[:100]}...")
        
        # Konuşma kuyruğuna ekle
        self.sound_queue.put((text, self.current_voice, self.speed, emotion))
        
        if wait:
            while self.is_busy():
                time.sleep(0.1)
    
    def speak_with_style(self, text: str, style: str = 'normal', wait: bool = False):
        """Belirli bir konuşma stiliyle konuş"""
        if style in self.speech_styles:
            # Stil ayarlarını geçici olarak uygula
            old_speed = self.speed
            old_volume = self.volume
            
            self.speed = self.speech_styles[style]['speed']
            self.volume = self.speech_styles[style]['volume']
            
            self.speak(text, wait)
            
            # Eski ayarlara dön
            self.speed = old_speed
            self.volume = old_volume
        else:
            self.speak(text, wait)
    
    def speak_with_voice(self, text: str, voice: str, wait: bool = False):
        """Belirli bir sesle konuş"""
        if voice in self.voices:
            old_voice = self.current_voice
            self.current_voice = voice
            self.speak(text, wait)
            self.current_voice = old_voice
    
    def say_hello(self):
        """A.N.N.A'dan samimi bir selamlama"""
        greetings = [
            "Merhaba! Ben A.N.N.A. Size nasıl yardımcı olabilirim?",
            "Hoş geldiniz! A.N.N.A olarak hizmetinizdeyim.",
            "Merhaba! Sizi duymak ne güzel. Nasıl yardımcı olabilirim?",
            "Selam! Ben A.N.N.A, JARVIS'in kadın sesli asistanıyım.",
        ]
        self.speak(random.choice(greetings), emotion='happy')
    
    def say_goodbye(self):
        """Vedalaşma"""
        goodbyes = [
            "Görüşmek üzere! İyi günler.",
            "Hoşça kalın! Yine beklerim.",
            "Kendinize iyi bakın!",
            "Güle güle! İyi eğlenceler.",
        ]
        self.speak(random.choice(goodbyes), emotion='calm')
    
    # ============================================
    # DİNLEME FONKSİYONLARI
    # ============================================
    
    def listen(self, timeout: int = 5, phrase_limit: int = 10, show_volume: bool = False) -> str:
        """
        Dinle ve metne çevir (gelişmiş)
        
        Args:
            timeout: Dinleme süresi (saniye)
            phrase_limit: Maksimum cümle süresi
            show_volume: Ses seviyesini göster
            
        Returns:
            Anlaşılan metin veya boş string
        """
        if not SR_AVAILABLE or not self.microphone:
            print("❌ Ses tanıma kullanılamıyor")
            return ""
        
        self.stats['listening_sessions'] += 1
        
        try:
            with self.microphone as source:
                # Ortam gürültüsünü tekrar kalibre et (her seferinde)
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                if show_volume and SOUNDDEVICE_AVAILABLE:
                    # Ses seviyesi göstergeli dinleme
                    return self._listen_with_volume(source, timeout, phrase_limit)
                else:
                    # Normal dinleme
                    print("🎤 Dinliyorum...")
                    audio = self.recognizer.listen(
                        source,
                        timeout=timeout,
                        phrase_time_limit=phrase_limit
                    )
            
            # Google Speech ile tanı
            try:
                text = self.recognizer.recognize_google(audio, language="tr-TR")
                print(f"📝 Anlaşılan: {text}")
                
                # Özel komutları tanı
                text_lower = text.lower()
                for cmd, keywords in self.custom_commands.items():
                    if any(keyword in text_lower for keyword in keywords):
                        print(f"🔍 Özel komut algılandı: {cmd}")
                
                return text_lower
                
            except sr.UnknownValueError:
                print("🤔 Anlaşılamadı")
                return ""
            except sr.RequestError as e:
                print(f"❌ Google Speech hatası: {e}")
                return ""
            
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            print(f"❌ Dinleme hatası: {e}")
            return ""
    
    def _listen_with_volume(self, source, timeout, phrase_limit):
        """Ses seviyesi göstergeli dinleme"""
        print("🎤 Dinliyor... (ses seviyesi gösteriliyor)")
        
        # Volume göstergesi için yardımcı
        def volume_indicator():
            bars = 0
            for i in range(timeout * 10):  # 0.1 saniye aralıklarla
                try:
                    # Ses seviyesini al
                    data = source.stream.read(source.CHUNK)
                    rms = audioop.rms(data, 2) if AUDIOOP_AVAILABLE else 0
                    
                    # Bar grafiği
                    bars = int(rms / 500) if rms > 0 else 0
                    bars = min(bars, 50)
                    
                    # Renkli gösterim
                    if bars < 10:
                        color = '⚪'  # Sessiz
                    elif bars < 25:
                        color = '🟢'  # Normal
                    elif bars < 40:
                        color = '🟡'  # Yüksek
                    else:
                        color = '🔴'  # Çok yüksek
                    
                    bar_str = '█' * bars + '░' * (50 - bars)
                    print(f"\r{color} [{bar_str}]", end='', flush=True)
                    
                except:
                    pass
                time.sleep(0.1)
            
            print()  # Yeni satır
        
        # Volume göstergesini ayrı thread'de başlat
        indicator_thread = threading.Thread(target=volume_indicator)
        indicator_thread.daemon = True
        indicator_thread.start()
        
        # Dinlemeyi başlat
        audio = self.recognizer.listen(
            source,
            timeout=timeout,
            phrase_time_limit=phrase_limit
        )
        
        return audio
    
    def listen_with_confirmation(self, prompt: str = None, timeout: int = 5) -> str:
        """Onay bekleyerek dinle"""
        if prompt:
            self.speak(prompt)
        
        text = self.listen(timeout)
        
        if text:
            self.speak(f"Anladığım: {text}. Doğru mu?", wait=True)
            confirmation = self.listen(3)
            
            if confirmation and any(word in confirmation for word in ['evet', 'doğru', 'aynen']):
                self.speak("Tamam, anlaşıldı.")
                return text
            else:
                self.speak("Peki, tekrar dener misiniz?")
                return ""
        return ""
    
    # ============================================
    # WAKE WORD FONKSİYONLARI
    # ============================================
    
    def start_wake_word(self, callback):
        """Wake word dinlemeyi başlat"""
        if not self.porcupine:
            return False
        
        self.wake_callback = callback
        self.wake_active = True
        threading.Thread(target=self._wake_loop, daemon=True).start()
        print("🔊 Wake word dinleniyor... ('Jarvis', 'Anna' veya 'Bilgisayar' deyin)")
        return True
    
    def _wake_loop(self):
        """Wake word döngüsü (optimize)"""
        if not self.porcupine or not SOUNDDEVICE_AVAILABLE:
            return
        
        frame_length = self.porcupine.frame_length
        sample_rate = self.porcupine.sample_rate
        
        try:
            with sd.InputStream(
                samplerate=sample_rate,
                channels=1,
                dtype='int16',
                blocksize=frame_length,
                latency='low'
            ) as stream:
                
                print("🔊 Wake word aktif - konuşabilirsiniz")
                
                while self.wake_active:
                    try:
                        frame, overflowed = stream.read(frame_length)
                        
                        if len(frame) == frame_length:
                            pcm = frame.flatten().astype(np.int16).tobytes()
                            result = self.porcupine.process(pcm)
                            
                            if result >= 0:
                                word = self.wake_keywords[result]
                                print(f"\n🔊 '{word.capitalize()}' algılandı!")
                                self.stats['wake_word_triggers'] += 1
                                
                                # Kısa bir onay sesi (opsiyonel)
                                if self.wake_callback:
                                    self.wake_callback(word)
                                
                                # Tekrar tetiklemeyi önlemek için bekle
                                time.sleep(1.5)
                        
                        time.sleep(0.01)
                    except Exception as e:
                        print(f"⚠️ Wake word döngü hatası: {e}")
                        time.sleep(0.1)
                    
        except Exception as e:
            print(f"❌ Wake word ses akışı hatası: {e}")
    
    def stop_wake_word(self):
        """Wake word dinlemeyi durdur"""
        self.wake_active = False
        print("⏹️ Wake word durduruldu")
    
    # ============================================
    # AYARLAR
    # ============================================
    
    def set_volume(self, volume: float):
        """Ses seviyesini ayarla (0.0 - 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        print(f"🔊 Ses seviyesi: %{int(self.volume * 100)}")
    
    def set_speed(self, speed: float):
        """Konuşma hızını ayarla (0.5 - 2.0)"""
        self.speed = max(0.5, min(2.0, speed))
        print(f"⚡ Konuşma hızı: {self.speed}x")
    
    def set_voice(self, voice: str) -> bool:
        """A.N.N.A'nın sesini değiştir"""
        if voice in self.voices:
            self.current_voice = voice
            self.stats['favorite_voice'] = voice
            print(f"🎙️ Ses değiştirildi: {self.voices[voice]}")
            
            # Kısa bir test konuşması
            if voice.startswith('tr'):
                self.speak(f"Merhaba! Ben {self.voices[voice]}. Yeni sesimi beğendiniz mi?")
            else:
                self.speak(f"Hello! I am {self.voices[voice]}. Do you like my new voice?")
            
            return True
        return False
    
    def set_emotion(self, emotion: str, intensity: float = 1.0):
        """Duygu durumunu ayarla"""
        if emotion in ['neutral', 'happy', 'sad', 'excited', 'calm']:
            self.emotion['mode'] = emotion
            self.emotion['intensity'] = intensity
            print(f"🎭 Duygu durumu: {emotion} (yoğunluk: {intensity})")
    
    def toggle_mute(self):
        """Sessiz modu aç/kapa"""
        self.muted = not self.muted
        status = "açıldı" if self.muted else "kapatıldı"
        print(f"🔇 Sessiz mod {status}")
        
        if not self.muted:
            self.speak("Ses geri açıldı.")
        
        return self.muted
    
    def get_voices(self) -> dict:
        """Kullanılabilir sesleri listele"""
        return self.voices
    
    def get_current_voice_info(self) -> str:
        """Aktif ses hakkında bilgi"""
        return f"🎙️ {self.voices[self.current_voice]} | Hız: {self.speed}x | Ses: %{int(self.volume * 100)}"
    
    def is_busy(self) -> bool:
        """Konuşuyor mu?"""
        return self.is_playing or not self.sound_queue.empty()
    
    # ============================================
    # KONUŞMA GEÇMİŞİ VE İSTATİSTİKLER
    # ============================================
    
    def _add_to_history(self, text: str, voice: str, emotion: str):
        """Konuşma geçmişine ekle"""
        self.history.append({
            'text': text,
            'voice': voice,
            'emotion': emotion,
            'timestamp': datetime.now().isoformat(),
            'words': len(text.split())
        })
        
        # Son 100 konuşmayı tut
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        self._save_history()
    
    def _save_history(self):
        """Geçmişi kaydet"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'history': self.history,
                    'stats': self.stats
                }, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def _load_history(self):
        """Geçmişi yükle"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get('history', [])
                    self.stats = data.get('stats', self.stats)
        except:
            pass
    
    def get_stats(self) -> str:
        """Detaylı istatistikleri göster"""
        
        # Ortalama konuşma süresi
        avg_speak_time = self.stats['total_speak_time'] / max(1, self.stats['sentences_spoken'])
        
        return f"""
📊 **A.N.N.A SES İSTATİSTİKLERİ**

🗣️ **Genel**
   • Konuşulan kelime: {self.stats['words_spoken']:,}
   • Konuşulan cümle: {self.stats['sentences_spoken']:,}
   • Ortalama cümle uzunluğu: {self.stats['words_spoken'] / max(1, self.stats['sentences_spoken']):.1f} kelime
   • Toplam konuşma süresi: {self.stats['total_speak_time']:.1f} saniye
   • Ortalama konuşma: {avg_speak_time:.2f} sn/cümle

👂 **Dinleme**
   • Dinleme oturumu: {self.stats['listening_sessions']:,}
   • Wake word tetikleme: {self.stats['wake_word_triggers']:,}
   • Başarı oranı: %{int(self.stats['wake_word_triggers'] / max(1, self.stats['listening_sessions']) * 100)}

🎙️ **Aktif Ses**
   • {self.voices[self.current_voice]}
   • Ses seviyesi: %{int(self.volume * 100)}
   • Konuşma hızı: {self.speed}x
   • Duygu durumu: {self.emotion['mode']}
   • Sessiz mod: {'Açık' if self.muted else 'Kapalı'}

⚡ **Anlık**
   • Kuyrukta bekleyen: {self.sound_queue.qsize()} ses
   • Konuşuyor: {'Evet' if self.is_playing else 'Hayır'}
   • Wake word: {'Aktif' if self.wake_active else 'Pasif'}
"""
    
    def get_history(self, limit: int = 5) -> str:
        """Son konuşmaları göster"""
        if not self.history:
            return "📭 Konuşma geçmişi yok"
        
        result = "📜 **SON KONUŞMALAR**\n\n"
        for h in self.history[-limit:]:
            time_str = datetime.fromisoformat(h['timestamp']).strftime('%H:%M')
            voice_name = self.voices.get(h['voice'], h['voice'])
            emotion_icon = {
                'neutral': '😐',
                'happy': '😊',
                'sad': '😔',
                'excited': '😲',
                'calm': '😌'
            }.get(h.get('emotion', 'neutral'), '😐')
            
            result += f"{emotion_icon} [{time_str}] {voice_name}: {h['text'][:60]}...\n"
        
        return result
    
    def clear_history(self):
        """Geçmişi temizle"""
        self.history = []
        self._save_history()
        print("🧹 Konuşma geçmişi temizlendi")
    
    # ============================================
    # TEST FONKSİYONLARI
    # ============================================
    
    def test_microphone(self):
        """Mikrofon testi"""
        print("\n" + "="*50)
        print("🎤 MİKROFON TESTİ")
        print("="*50)
        print("3 saniye boyunca konuşun...")
        
        text = self.listen(timeout=3)
        
        if text:
            print(f"✅ Mikrofon çalışıyor! Duyulan: {text}")
            self.speak(f"Duyduğum: {text}. Sesiniz net anlaşılıyor.")
            return True
        else:
            print("❌ Mikrofon çalışmıyor veya ses algılanamadı")
            print("\nOlası çözümler:")
            print("1. Mikrofonun bağlı olduğundan emin olun")
            print("2. Android'de mikrofon izni verdiğinizden emin olun")
            print("3. Ortam gürültüsünü azaltın")
            return False
    
    def test_speaker(self):
        """Hoparlör testi"""
        print("\n" + "="*50)
        print("🔊 HOPARLÖR TESTİ")
        print("="*50)
        
        test_messages = [
            ("normal", "Merhaba! Ben A.N.N.A. Ses testi yapıyorum."),
            ("happy", "Harika bir gün! Umarım sizin de gününüz güzeldir."),
            ("calm", "Şimdi daha sakin bir sesle konuşuyorum."),
            ("excited", "Vay canına! Bu gerçekten heyecan verici!"),
        ]
        
        for style, message in test_messages:
            print(f"\n🎭 Stil: {style}")
            self.speak_with_style(message, style, wait=True)
            time.sleep(0.5)
        
        print("\n✅ Hoparlör testi tamamlandı")
        print("Eğer tüm mesajları duyduysanız, ses sisteminiz çalışıyor!")
        return True
    
    def test_all_voices(self):
        """Tüm sesleri dene"""
        print("\n" + "="*50)
        print("🎙️ SES TESTİ - TÜM KADIN SESLERİ")
        print("="*50)
        
        for voice_id, voice_name in self.voices.items():
            print(f"\n▶️ {voice_name} deneniyor...")
            old_voice = self.current_voice
            self.current_voice = voice_id
            
            if voice_id.startswith('tr'):
                self.speak(f"Merhaba! Ben {voice_name}. Sesimi nasıl buldunuz?", wait=True)
            else:
                self.speak(f"Hello! I am {voice_name}. How do you like my voice?", wait=True)
            
            time.sleep(0.5)
            self.current_voice = old_voice
        
        print("\n✅ Tüm sesler test edildi")
        print(f"Şu anki ses: {self.voices[self.current_voice]}")
    
    def test_emotions(self):
        """Duygu durumlarını test et"""
        print("\n" + "="*50)
        print("🎭 DUYGU DURUMU TESTİ")
        print("="*50)
        
        test_text = "Bugün nasılsınız?"
        
        for emotion in ['neutral', 'happy', 'sad', 'excited', 'calm']:
            print(f"\n▶️ Duygu: {emotion}")
            self.speak(test_text, emotion=emotion, wait=True)
            time.sleep(0.3)
        
        print("\n✅ Duygu testi tamamlandı")