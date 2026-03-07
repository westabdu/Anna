# src/api/translator.py - ÇEVİRİ API'Sİ
"""
A.N.N.A Mobile Çeviri Motoru
- Google Translate ile çok dilli çeviri
- Dil algılama
- 100+ dil desteği
"""

import asyncio
import os
import sys

# Android tespiti
IS_ANDROID = 'android' in sys.platform or 'ANDROID_ARGUMENT' in os.environ

# Google Translate
try:
    from googletrans import Translator
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False
    print("⚠️ googletrans yüklü değil! 'pip install googletrans==4.0.2' ile kurun.")

# DeepL (opsiyonel, API anahtarı gerektirir)
try:
    import deepl
    DEEPL_AVAILABLE = True
except:
    DEEPL_AVAILABLE = False


class TranslationAPI:
    """
    A.N.N.A için çeviri motoru
    - Google Translate (ücretsiz, 100+ dil)
    - DeepL (opsiyonel, daha kaliteli)
    """
    
    def __init__(self, use_deepl: bool = False, deepl_api_key: str = None):
        self.use_deepl = use_deepl and DEEPL_AVAILABLE and deepl_api_key
        
        # Google Translate
        if GOOGLETRANS_AVAILABLE:
            try:
                self.google_translator = Translator()
                print("✅ Google Translate hazır")
            except Exception as e:
                print(f"⚠️ Google Translate başlatılamadı: {e}")
                self.google_translator = None
        else:
            self.google_translator = None
        
        # DeepL (opsiyonel)
        if self.use_deepl:
            try:
                self.deepl_translator = deepl.Translator(deepl_api_key)
                print("✅ DeepL hazır (yüksek kalite)")
            except Exception as e:
                print(f"⚠️ DeepL başlatılamadı: {e}")
                self.use_deepl = False
        
        # Dil kodları ve isimleri
        self.language_names = {
            'tr': 'Türkçe',
            'en': 'İngilizce',
            'de': 'Almanca',
            'fr': 'Fransızca',
            'es': 'İspanyolca',
            'it': 'İtalyanca',
            'ru': 'Rusça',
            'ja': 'Japonca',
            'ko': 'Korece',
            'zh-cn': 'Çince (Basitleştirilmiş)',
            'zh-tw': 'Çince (Geleneksel)',
            'ar': 'Arapça',
            'hi': 'Hintçe',
            'pt': 'Portekizce',
            'nl': 'Hollandaca',
            'pl': 'Lehçe',
            'uk': 'Ukraynaca',
            'el': 'Yunanca',
            'he': 'İbranice',
            'th': 'Tayca',
            'vi': 'Vietnamca',
            'id': 'Endonezce',
            'ms': 'Malayca',
            'fa': 'Farsça',
            'ur': 'Urduca',
            'sw': 'Svahili',
            'da': 'Danca',
            'sv': 'İsveççe',
            'no': 'Norveççe',
            'fi': 'Fince',
            'hu': 'Macarca',
            'cs': 'Çekçe',
            'sk': 'Slovakça',
            'ro': 'Rumence',
            'bg': 'Bulgarca',
            'sr': 'Sırpça',
            'hr': 'Hırvatça',
            'sl': 'Slovence',
            'lt': 'Litvanca',
            'lv': 'Letonca',
            'et': 'Estonca',
            'sq': 'Arnavutça',
            'mk': 'Makedonca',
            'bs': 'Boşnakça',
            'az': 'Azerice',
            'ka': 'Gürcüce',
            'hy': 'Ermenice',
            'kk': 'Kazakça',
            'uz': 'Özbekçe',
            'mn': 'Moğolca',
            'ne': 'Nepalce',
            'si': 'Sinhala',
            'km': 'Khmer',
            'lo': 'Laoca',
            'my': 'Burmaca',
            'am': 'Amharca',
            'ti': 'Tigrinya',
            'om': 'Oromo',
            'ig': 'İgbo',
            'yo': 'Yoruba',
            'ha': 'Hausa',
            'so': 'Somalice',
            'rw': 'Kinyarwanda',
            'rn': 'Kirundi',
            'mg': 'Malgaşça',
            'ny': 'Chichewa',
            'sn': 'Shona',
            'st': 'Sesotho',
            'tn': 'Tsvana',
            'ts': 'Tsonga',
            've': 'Venda',
            'xh': 'Xhosa',
            'zu': 'Zulu',
        }
        
        print(f"📱 Android: {'✅' if IS_ANDROID else '❌'}")
        print(f"🌍 Çeviri Motoru: {'✅ Google Translate' if GOOGLETRANS_AVAILABLE else '❌'}")
    
    async def translate(self, text: str, dest: str = 'tr', src: str = 'auto') -> dict:
        """
        Metni çevir
        
        Args:
            text: Çevrilecek metin
            dest: Hedef dil (varsayılan: 'tr' - Türkçe)
            src: Kaynak dil ('auto' = otomatik algıla)
        
        Returns:
            {
                'success': bool,
                'original': str,
                'translated': str,
                'src_lang': str,
                'src_lang_name': str,
                'dest_lang': str,
                'dest_lang_name': str,
                'method': str,
                'error': str (opsiyonel)
            }
        """
        result = {
            'success': False,
            'original': text,
            'translated': '',
            'src_lang': src if src != 'auto' else 'unknown',
            'src_lang_name': 'Bilinmiyor',
            'dest_lang': dest,
            'dest_lang_name': self.get_language_name(dest),
            'method': 'none',
            'error': None
        }
        
        if not text or not text.strip():
            result['error'] = 'Boş metin'
            return result
        
        # Google Translate ile çevir
        if GOOGLETRANS_AVAILABLE and self.google_translator:
            try:
                # Asenkron çeviri
                translation = await self.google_translator.translate(text, dest=dest, src=src)
                
                result['success'] = True
                result['translated'] = translation.text
                result['src_lang'] = translation.src
                result['src_lang_name'] = self.get_language_name(translation.src)
                result['method'] = 'google'
                
                return result
                
            except Exception as e:
                result['error'] = str(e)
                # Senkron olarak dene (yedek)
                try:
                    translation = self.google_translator.translate(text, dest=dest, src=src)
                    result['success'] = True
                    result['translated'] = translation.text
                    result['src_lang'] = translation.src
                    result['src_lang_name'] = self.get_language_name(translation.src)
                    result['method'] = 'google_sync'
                    return result
                except:
                    pass
        
        # DeepL ile dene (opsiyonel)
        if self.use_deepl and not result['success']:
            try:
                # DeepL asenkron
                translation = await self.deepl_translator.translate_text_async(
                    text, 
                    target_lang=dest.upper()
                )
                
                result['success'] = True
                result['translated'] = translation.text
                result['src_lang'] = translation.detected_source_lang.lower()
                result['src_lang_name'] = self.get_language_name(translation.detected_source_lang.lower())
                result['method'] = 'deepl'
                
                return result
                
            except Exception as e:
                result['error'] = str(e)
        
        if not result['success']:
            result['error'] = result.get('error', 'Çeviri yapılamadı')
        
        return result
    
    def translate_sync(self, text: str, dest: str = 'tr', src: str = 'auto') -> dict:
        """Senkron çeviri (asenkron kullanamıyorsanız)"""
        if not GOOGLETRANS_AVAILABLE or not self.google_translator:
            return {
                'success': False,
                'original': text,
                'translated': '',
                'error': 'Google Translate kullanılamıyor'
            }
        
        try:
            translation = self.google_translator.translate(text, dest=dest, src=src)
            return {
                'success': True,
                'original': text,
                'translated': translation.text,
                'src_lang': translation.src,
                'src_lang_name': self.get_language_name(translation.src),
                'dest_lang': dest,
                'dest_lang_name': self.get_language_name(dest),
                'method': 'google_sync'
            }
        except Exception as e:
            return {
                'success': False,
                'original': text,
                'translated': '',
                'error': str(e)
            }
    
    async def detect_language(self, text: str) -> dict:
        """Metnin dilini algıla"""
        result = {
            'success': False,
            'lang': 'unknown',
            'lang_name': 'Bilinmiyor',
            'confidence': 0.0
        }
        
        if not text or not self.google_translator:
            return result
        
        try:
            detection = await self.google_translator.detect(text)
            result['success'] = True
            result['lang'] = detection.lang
            result['lang_name'] = self.get_language_name(detection.lang)
            result['confidence'] = detection.confidence
            return result
        except:
            return result
    
    def get_language_name(self, lang_code: str) -> str:
        """Dil kodunu isme çevir"""
        return self.language_names.get(lang_code, lang_code.upper())
    
    def get_supported_languages(self) -> list:
        """Desteklenen dilleri listele"""
        return sorted([(code, name) for code, name in self.language_names.items()])
    
    def is_supported(self, lang_code: str) -> bool:
        """Dil destekleniyor mu?"""
        return lang_code in self.language_names or lang_code == 'auto'


# ============================================
# TEST KODU
# ============================================
async def test_translator():
    """Çeviri testi"""
    print("\n" + "="*50)
    print("🌍 ÇEVİRİ MOTORU TESTİ")
    print("="*50)
    
    translator = TranslationAPI()
    
    test_texts = [
        "Merhaba dünya!",
        "Hello world!",
        "こんにちは世界",
        "Bonjour le monde",
        "Hallo Welt",
    ]
    
    for text in test_texts:
        print(f"\n📝 Orijinal: {text}")
        result = await translator.translate(text, dest='tr')
        
        if result['success']:
            print(f"   🔤 Dil: {result['src_lang_name']}")
            print(f"   🇹🇷 Çeviri: {result['translated']}")
            print(f"   ⚙️ Yöntem: {result['method']}")
        else:
            print(f"   ❌ Hata: {result['error']}")
        
        await asyncio.sleep(0.5)
    
    print("\n✅ Çeviri testi tamamlandı")

if __name__ == "__main__":
    asyncio.run(test_translator())