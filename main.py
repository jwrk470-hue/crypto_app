import requests
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

# استخدام متغيرة بيئة أو قيمة افتراضية آمنة
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

class CryptoAgentApp(App):
    def build(self):
        self.title = "Crypto AI Agent"
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        header = Label(text="🤖 AI Trading Agent", font_size='22sp', size_hint_y=None, height=40, color=(0, 0.8, 1, 1))
        layout.add_widget(header)
        
        self.btn = Button(text="تحليل السوق واتخاذ القرار", font_size='16sp', size_hint_y=None, height=50, background_color=(0, 0.7, 0.9, 1))
        self.btn.bind(on_press=self.analyze_market)
        layout.add_widget(self.btn)
        
        scroll = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text="اضغط على الزر أعلاه لبدء التحليل...",
            font_size='14sp',
            size_hint_y=None,
            halign='right',
            valign='top'
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        return layout

    def analyze_market(self, instance):
        self.result_label.text = "جاري سحب البيانات والاتصال بـ Gemini..."
        
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
        try:
            res = requests.get(url).json()
            btc = res.get('bitcoin', {}).get('usd', 'N/A')
            eth = res.get('ethereum', {}).get('usd', 'N/A')
            sol = res.get('solana', {}).get('usd', 'N/A')
            market_prices = f"Bitcoin: ${btc} | Ethereum: ${eth} | Solana: ${sol}"
        except Exception as e:
            self.result_label.text = f"خطأ في الأسعار: {e}"
            return

        prompt = f"أنت وكيل ذكاء اصطناعي لتداول العملات الرقمية. رأس المال: $100.\nالأسعار: {market_prices}\nالمطلوب: تحليل مختصر وقرار تداول واضح."
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        try:
            response = requests.post(gemini_url, headers={'Content-Type': 'application/json'}, json={"contents": [{"parts": [{"text": prompt}]}]})
            if response.status_code == 200:
                decision = response.json()['candidates'][0]['content']['parts'][0]['text']
                self.result_label.text = f"📊 الأسعار الحالية:\n{market_prices}\n\n💡 قرار الوكيل:\n{decision}"
            else:
                self.result_label.text = f"خطأ من API: {response.status_code}"
        except Exception as e:
            self.result_label.text = f"خطأ اتصال: {e}"

if __name__ == '__main__':
    CryptoAgentApp().run()
