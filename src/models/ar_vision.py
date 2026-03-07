# src/modules/ar_vision.py - ANDROID UYUMLU
"""
A.N.N.A Mobile AR ve Gelişmiş Görüntü İşleme
- 🕶️ Artırılmış Gerçeklik (AR) özellikleri
- 📸 Gelişmiş OCR (El yazısı, çoklu dil, otomatik düzeltme)
- 🌍 CANLI ÇEVİRİ (Japonca tabelayı Türkçe'ye çevir)
- 🎯 Nesne tanıma
- 🔍 QR/Barkod okuma
- 🎨 Renk analizi
"""

import os
import sys
import cv2
import numpy as np
import time
import tempfile
from pathlib import Path
import threading
import queue
import asyncio
from datetime import datetime

# Android tespiti
IS_ANDROID = 'android' in sys.platform or 'ANDROID_ARGUMENT' in os.environ

# OCR
try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except:
    TESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except:
    EASYOCR_AVAILABLE = False

# QR/Barkod
try:
    from pyzbar.pyzbar import decode
    QR_AVAILABLE = True
except:
    QR_AVAILABLE = False

# MediaPipe (Android'de çalışır)
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except:
    MEDIAPIPE_AVAILABLE = False

# Çeviri API'si
try:
    from src.api.translator import TranslationAPI
    TRANSLATOR_AVAILABLE = True
except:
    TRANSLATOR_AVAILABLE = False
    print("⚠️ Çeviri modülü yüklenemedi! 'pip install googletrans==4.0.2' ile kurun.")


class ARVision:
    """
    A.N.N.A Mobile AR ve Gelişmiş Görüntü İşleme
    - Kameradan canlı görüntü
    - Nesne/QR/OCR tanıma
    - Gelişmiş metin işleme
    - CANLI ÇEVİRİ (yeni!)
    """
    
    def __init__(self):
        # Android'de depolama yolu farklı
        if IS_ANDROID:
            try:
                from android.storage import primary_external_storage_path
                base_path = Path(primary_external_storage_path()) / "ANNA" / "data"
                self.data_dir = base_path / "ar"
            except:
                self.data_dir = Path("/storage/emulated/0/ANNA/data/ar")
        else:
            self.data_dir = Path("data/ar")
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Kamera durumu
        self.camera_active = False
        self.cap = None
        self.frame_queue = queue.Queue(maxsize=2)
        self.result_queue = queue.Queue()
        
        # AR modları - ÇEVİRİ EKLENDİ!
        self.modes = {
            'ocr': '📝 OCR (Yazı Tanıma)',
            'qr': '📱 QR/Barkod',
            'face': '👤 Yüz Tanıma',
            'object': '🔍 Nesne Tanıma',
            'color': '🎨 Renk Analizi',
            'translate': '🌍 CANLI ÇEVİRİ'  # <-- YENİ MOD
        }
        self.current_mode = 'ocr'
        
        # Çeviri motoru
        self.translator = None
        if TRANSLATOR_AVAILABLE:
            try:
                self.translator = TranslationAPI()
                print("✅ Çeviri motoru hazır")
            except Exception as e:
                print(f"⚠️ Çeviri motoru başlatılamadı: {e}")
        
        # EasyOCR (Android'de çalışır)
        self.easyocr_reader = None
        if EASYOCR_AVAILABLE:
            try:
                # Daha fazla dil ekle! (Japonca, Çince, Korece vb.)
                self.easyocr_reader = easyocr.Reader(
                    ['tr', 'en', 'ja', 'ko', 'zh-cn', 'zh-tw', 'ru', 'ar', 'de', 'fr', 'es'], 
                    gpu=False
                )
                print("✅ EasyOCR hazır (Türkçe + İngilizce + Japonca + Çince + Korece + 7 dil daha)")
            except Exception as e:
                print(f"⚠️ EasyOCR yüklenemedi: {e}")
        
        # Tesseract (Android'de yol farklı)
        if not EASYOCR_AVAILABLE and TESSERACT_AVAILABLE:
            if IS_ANDROID:
                # Android'de Tesseract yolu
                possible_paths = [
                    '/data/data/org.anna.mobile/files/tesseract',
                    '/storage/emulated/0/ANNA/tesseract'
                ]
            else:
                possible_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
                ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
            print("✅ Tesseract OCR hazır")
        
        # MediaPipe (Android'de çalışır)
        if MEDIAPIPE_AVAILABLE:
            try:
                self.mp_face_detection = mp.solutions.face_detection
                self.mp_face_mesh = mp.solutions.face_mesh
                self.mp_hands = mp.solutions.hands
                self.mp_drawing = mp.solutions.drawing_utils
                
                self.face_detection = self.mp_face_detection.FaceDetection(
                    model_selection=0, min_detection_confidence=0.5
                )
                print("✅ MediaPipe hazır (Yüz/El tanıma)")
            except:
                pass
        
        # Nesne tanıma için basit Cascade
        self.face_cascade = None
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
        except:
            pass
        
        print(f"📸 AR Vision Modülü başlatıldı")
        print(f"   Modlar: {', '.join(self.modes.values())}")
        print(f"📱 Android: {'✅' if IS_ANDROID else '❌'}")
    
    # ============================================
    # KAMERA KONTROLÜ
    # ============================================
    
    def start_camera(self, callback=None):
        """Kamerayı başlat (Android'de farklı)"""
        if self.camera_active:
            return "Kamera zaten aktif"
        
        try:
            # Android'de kamera indeksi farklı olabilir
            if IS_ANDROID:
                # Arka kamera için 0, ön kamera için 1
                self.cap = cv2.VideoCapture(0)
            else:
                self.cap = cv2.VideoCapture(0)
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            if not self.cap.isOpened():
                return "❌ Kamera açılamadı"
            
            self.camera_active = True
            self.callback = callback
            
            # Kamera thread'ini başlat
            threading.Thread(target=self._camera_loop, daemon=True).start()
            
            return "✅ Kamera başlatıldı"
            
        except Exception as e:
            return f"❌ Kamera hatası: {e}"
    
    def stop_camera(self):
        """Kamerayı durdur"""
        self.camera_active = False
        if self.cap:
            self.cap.release()
        return "⏹️ Kamera durduruldu"
    
    def _camera_loop(self):
        """Kamera döngüsü"""
        while self.camera_active:
            ret, frame = self.cap.read()
            if ret:
                # İşleme moduna göre frame'i işle
                processed = self._process_frame(frame)
                
                # Callback varsa çağır
                if self.callback:
                    self.callback(processed)
            
            time.sleep(0.03)  # ~30 FPS
    
    def _process_frame(self, frame):
        """Frame'i işle - ÇEVİRİ MODU EKLENDİ"""
        result = {
            'frame': frame,
            'mode': self.current_mode,
            'detections': [],
            'text': None,
            'translation': None  # Çeviri sonucu
        }
        
        if self.current_mode == 'ocr':
            result['text'] = self._scan_text(frame)
            result['detections'] = self._detect_text_regions(frame)
            
        elif self.current_mode == 'qr':
            result['detections'] = self._scan_qr(frame)
            
        elif self.current_mode == 'face':
            result['detections'] = self._detect_faces(frame)
            
        elif self.current_mode == 'object':
            result['detections'] = self._detect_objects(frame)
            
        elif self.current_mode == 'color':
            result['detections'] = self._analyze_colors(frame)
            
        elif self.current_mode == 'translate':
            # Önce metni oku
            text = self._scan_text(frame)
            if text:
                result['text'] = text
                result['detections'] = self._detect_text_regions(frame)
                
                # Çeviriyi yap (ayrı thread'de)
                if self.translator:
                    # Asenkron çeviriyi senkron çalıştır
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        translation = loop.run_until_complete(
                            self.translator.translate(text, dest='tr', src='auto')
                        )
                        loop.close()
                        result['translation'] = translation
                    except Exception as e:
                        print(f"⚠️ Çeviri hatası: {e}")
                        result['translation'] = {
                            'success': False,
                            'error': str(e)
                        }
        
        return result
    
    # ============================================
    # GELİŞMİŞ OCR (Çok Dilli)
    # ============================================
    
    def _scan_text(self, frame):
        """Gelişmiş OCR - EasyOCR veya Tesseract (çok dilli)"""
        text = ""
        
        # EasyOCR dene (daha iyi, çok dilli)
        if EASYOCR_AVAILABLE and self.easyocr_reader:
            try:
                results = self.easyocr_reader.readtext(frame)
                if results:
                    texts = []
                    for (bbox, text_part, prob) in results:
                        if prob > 0.3:  # Biraz daha düşük eşik (Japonca için)
                            texts.append(text_part)
                    text = " ".join(texts)
                    if text:
                        print(f"🔍 EasyOCR algıladı: {text[:50]}...")
            except Exception as e:
                print(f"⚠️ EasyOCR hatası: {e}")
        
        # EasyOCR yoksa Tesseract dene
        elif TESSERACT_AVAILABLE:
            try:
                # Ön işleme (Japonca/Çince için farklı parametreler)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Görüntüyü büyüt (küçük karakterler için)
                gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                
                # Gürültü azaltma
                gray = cv2.medianBlur(gray, 3)
                
                # Adaptif eşikleme
                thresh = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY, 11, 2
                )
                
                # Tesseract ile çok dilli OCR
                text = pytesseract.image_to_string(
                    thresh, 
                    lang='tur+eng+jpn+chi_sim+chi_tra+kor'
                )
            except Exception as e:
                print(f"⚠️ Tesseract hatası: {e}")
        
        return text.strip()
    
    def _detect_text_regions(self, frame):
        """Metin bölgelerini tespit et"""
        regions = []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        try:
            mser = cv2.MSER_create()
            regions_m, _ = mser.detectRegions(gray)
            
            for region in regions_m:
                if len(region) > 0:
                    x, y, w, h = cv2.boundingRect(region)
                    if w > 20 and h > 10:
                        regions.append({
                            'bbox': (x, y, x+w, y+h),
                            'type': 'text'
                        })
        except:
            pass
        
        return regions[:10]
    
    def scan_image(self, image_path: str) -> dict:
        """Resim dosyasını tara (ÇEVİRİ DESTEKLİ)"""
        result = {
            'text': '',
            'translation': None,  # Çeviri sonucu
            'qr_codes': [],
            'faces': 0,
            'colors': []
        }
        
        try:
            img = cv2.imread(image_path)
            
            # OCR
            result['text'] = self._scan_text(img)
            
            # Çeviri (eğer metin varsa)
            if result['text'] and self.translator:
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    translation = loop.run_until_complete(
                        self.translator.translate(result['text'], dest='tr')
                    )
                    loop.close()
                    result['translation'] = translation
                except:
                    pass
            
            # QR
            if QR_AVAILABLE:
                qr_results = decode(img)
                for qr in qr_results:
                    result['qr_codes'].append({
                        'data': qr.data.decode('utf-8'),
                        'type': qr.type
                    })
            
            # Yüz
            faces = self._detect_faces(img)
            result['faces'] = len(faces)
            
            # Renkler
            colors = self._analyze_colors(img)
            result['colors'] = [c['name'] for c in colors if c['percent'] > 10]
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    # ============================================
    # QR/BARKOD
    # ============================================
    
    def _scan_qr(self, frame):
        """QR kod ve barkod tara"""
        detections = []
        
        if not QR_AVAILABLE:
            return detections
        
        try:
            codes = decode(frame)
            for code in codes:
                detections.append({
                    'type': 'qr' if code.type == 'QRCODE' else 'barcode',
                    'data': code.data.decode('utf-8'),
                    'bbox': code.rect
                })
        except:
            pass
        
        return detections
    
    # ============================================
    # YÜZ TANIMA
    # ============================================
    
    def _detect_faces(self, frame):
        """Yüz tespiti"""
        faces = []
        
        # MediaPipe ile dene
        if MEDIAPIPE_AVAILABLE and hasattr(self, 'face_detection'):
            try:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.face_detection.process(rgb)
                
                if results.detections:
                    h, w, _ = frame.shape
                    for detection in results.detections:
                        bbox = detection.location_data.relative_bounding_box
                        x = int(bbox.xmin * w)
                        y = int(bbox.ymin * h)
                        width = int(bbox.width * w)
                        height = int(bbox.height * h)
                        
                        faces.append({
                            'bbox': (x, y, x+width, y+height),
                            'confidence': detection.score[0],
                            'type': 'face'
                        })
            except:
                pass
        
        # Cascade ile dene (yedek)
        if not faces and self.face_cascade is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_cascade = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            for (x, y, w, h) in faces_cascade:
                faces.append({
                    'bbox': (x, y, x+w, y+h),
                    'confidence': 0.8,
                    'type': 'face'
                })
        
        return faces
    
    # ============================================
    # NESNE TANIMA
    # ============================================
    
    def _detect_objects(self, frame):
        """Basit nesne tespiti"""
        objects = []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        try:
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    
                    obj_type = 'object'
                    if 0.8 < aspect_ratio < 1.2 and area > 5000:
                        obj_type = 'square'
                    elif aspect_ratio > 2:
                        obj_type = 'rectangle'
                    elif w < 30 and h < 30:
                        obj_type = 'small'
                    
                    objects.append({
                        'bbox': (x, y, x+w, y+h),
                        'area': area,
                        'type': obj_type
                    })
        except:
            pass
        
        return objects[:5]
    
    # ============================================
    # RENK ANALİZİ
    # ============================================
    
    def _analyze_colors(self, frame):
        """Renk analizi"""
        colors = []
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width = frame.shape[:2]
        
        color_ranges = {
            'kırmızı': ([0, 50, 50], [10, 255, 255]),
            'turuncu': ([10, 50, 50], [20, 255, 255]),
            'sarı': ([20, 50, 50], [30, 255, 255]),
            'yeşil': ([40, 50, 50], [80, 255, 255]),
            'mavi': ([100, 50, 50], [130, 255, 255]),
            'mor': ([130, 50, 50], [160, 255, 255]),
            'pembe': ([160, 50, 50], [180, 255, 255]),
        }
        
        for color_name, (lower, upper) in color_ranges.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            ratio = cv2.countNonZero(mask) / (width * height) * 100
            
            if ratio > 5:
                colors.append({
                    'name': color_name,
                    'percent': round(ratio, 1)
                })
        
        return sorted(colors, key=lambda x: x['percent'], reverse=True)
    
    # ============================================
    # YARDIMCI FONKSİYONLAR
    # ============================================
    
    def set_mode(self, mode: str):
        """AR modunu değiştir"""
        if mode in self.modes:
            self.current_mode = mode
            return f"🔄 Mod değiştirildi: {self.modes[mode]}"
        return f"❌ Geçersiz mod. Seçenekler: {', '.join(self.modes.keys())}"
    
    def get_modes(self) -> dict:
        """Kullanılabilir modları getir"""
        return self.modes
    
    def take_photo(self) -> dict:
        """Fotoğraf çek ve kaydet (ÇEVİRİ DESTEKLİ)"""
        if not self.camera_active or not self.cap:
            return {"error": "❌ Kamera aktif değil"}
        
        try:
            ret, frame = self.cap.read()
            if ret:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = self.data_dir / f"photo_{timestamp}.jpg"
                cv2.imwrite(str(filename), frame)
                
                # Fotoğrafı tara (çeviri dahil)
                scan_result = self.scan_image(str(filename))
                
                return {
                    'success': True,
                    'file': str(filename),
                    'scan': scan_result
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        return {'success': False, 'error': 'Fotoğraf çekilemedi'}
    
    def save_current_frame(self):
        """Mevcut kareyi kaydet"""
        return self.take_photo()
    
    def get_status(self) -> dict:
        """AR durumunu getir"""
        return {
            'active': self.camera_active,
            'mode': self.current_mode,
            'mode_name': self.modes.get(self.current_mode, ''),
            'easyocr': EASYOCR_AVAILABLE,
            'tesseract': TESSERACT_AVAILABLE,
            'translator': self.translator is not None,
            'qr': QR_AVAILABLE,
            'mediapipe': MEDIAPIPE_AVAILABLE
        }