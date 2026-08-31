from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import sqlite3

# --- Data Dictionaries ---
CROP_DATA = {
    "Rice (1.2)": (
        "Rice is one of the major food crops of the world. Hot and wet tropical and subtropical regions are best suited for rice cultivation.\n\n"
        "• Temperature: High temperature\n"
        "• Humidity/Rainfall: High humidity and high rainfall\n"
        "• Soil: Grows best in alluvial and clayey soil, which can hold water for a long time.\n"
        "• In India: Mainly grown in West Bengal, Andhra Pradesh, Tamil Nadu, Bihar, Odisha, and Assam."
    ),
    "Wheat (2.2)": (
        "Wheat is the staple crop in mid-latitude and dry subtropical regions.\n\n"
        "• Temperature: Moderate temperature\n"
        "• Conditions: Requires a cool and moist growing season and bright sunshine at harvest.\n"
        "• Soil: Well-drained loamy or black soil.\n"
        "• In India: Grown in winter in Punjab, Haryana, and Uttar Pradesh."
    ),
    "Maize (3.2)": (
        "Maize (corn) is grown both as a food and fodder crop.\n\n"
        "• Temperature: Moderate temperature\n"
        "• Soil: Fertile and well-drained.\n"
        "• In India: Grown in UP, MP, Bihar, and Karnataka."
    ),
    "Millets (4.2)": (
        "Millets refer to coarse grains like jowar, bajra, and ragi.\n\n"
        "• Temperature: Moderate\n"
        "• Rainfall: Low rainfall\n"
        "• Soil: Sandy and less fertile soil.\n"
        "• In India: Grown in Karnataka, Maharashtra, Rajasthan, and UP."
    )
}

PRACTICE_DATA = {
    "Steps to Increase Yield (1.8)": (
        "Steps to Increase Crop Production:\n"
        "1. Soil Management – Maintain proper pH and nutrients\n"
        "2. High Yielding Varieties (HYV)\n"
        "3. Modern Irrigation\n"
        "4. Nutrient Management\n"
        "5. Plant Protection\n"
        "6. Mechanization"
    ),
    "Kharif Crops (2.8)": (
        "Kharif Crops Details:\n"
        "• Sowing Period: June – July\n"
        "• Harvesting Period: September – October\n"
        "• Water Needs: High quantity of water\n"
        "• Examples: Rice, maize, soya bean, cotton, groundnut"
    ),
    "Rabi Crops (3.8)": (
        "Rabi Crops Details:\n"
        "• Sowing Period: October – November\n"
        "• Harvesting Period: March – April\n"
        "• Water Needs: Lesser quantity of water\n"
        "• Examples: Wheat, pea, mustard, barley, gram"
    )
}

SCHEMES_DATA = {
    "PM-KISAN": "Income support to eligible farmer families to support cultivation expenses.",
    "PM Fasal Bima Yojana": "Financial support and insurance coverage in case of crop loss.",
    "Kisan Credit Card": "Affordable institutional credit for crop cultivation and allied activities."
}


class AgriApp(App):
    def build(self):
        self.title = "Agronomic & Farmer Advisor"
        
        # Initialize SQLite database
        self.init_db()

        # Layout Setup
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header Label
        header = Label(
            text="Agri-Advisor Mobile Portal",
            size_hint_y=None,
            height=40,
            bold=True,
            font_size='18sp'
        )
        main_layout.add_widget(header)

        # Main Category Spinner
        self.category_spinner = Spinner(
            text="Select Section",
            values=("Crop Info", "Farming Practices", "Government Schemes", "Farm Database Check"),
            size_hint_y=None,
            height=45
        )
        self.category_spinner.bind(text=self.on_category_change)
        main_layout.add_widget(self.category_spinner)

        # Sub-Category Spinner
        self.subcategory_spinner = Spinner(
            text="Select Topic",
            values=(),
            size_hint_y=None,
            height=45
        )
        main_layout.add_widget(self.subcategory_spinner)

        # Submit Action Button
        submit_btn = Button(
            text="Get Information",
            size_hint_y=None,
            height=50,
            background_color=(0.18, 0.49, 0.20, 1)
        )
        submit_btn.bind(on_press=self.display_information)
        main_layout.add_widget(submit_btn)

        # Scrollable Output Text Area
        scroll = ScrollView(size_hint=(1, 1))
        self.output_label = Label(
            text="Select options above and click 'Get Information'.",
            size_hint_y=None,
            text_size=(None, None),
            valign='top',
            halign='left',
            padding=(10, 10)
        )
        self.output_label.bind(texture_size=self._update_label_height)
        scroll.add_widget(self.output_label)
        main_layout.add_widget(scroll)

        return main_layout

    def _update_label_height(self, instance, value):
        instance.height = value[1]
        instance.text_size = (instance.width - 20, None)

    def init_db(self):
        self.conn = sqlite3.connect("farm_app.db")
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS farmer(name TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS crops(name TEXT, area REAL)")
        self.conn.commit()

    def on_category_change(self, spinner, text):
        if text == "Crop Info":
            self.subcategory_spinner.values = tuple(CROP_DATA.keys())
        elif text == "Farming Practices":
            self.subcategory_spinner.values = tuple(PRACTICE_DATA.keys())
        elif text == "Government Schemes":
            self.subcategory_spinner.values = tuple(SCHEMES_DATA.keys())
        elif text == "Farm Database Check":
            self.subcategory_spinner.values = ("View Records",)
        
        if self.subcategory_spinner.values:
            self.subcategory_spinner.text = self.subcategory_spinner.values[0]

    def display_information(self, instance):
        cat = self.category_spinner.text
        sub = self.subcategory_spinner.text

        if cat == "Crop Info" and sub in CROP_DATA:
            self.output_label.text = CROP_DATA[sub]
        elif cat == "Farming Practices" and sub in PRACTICE_DATA:
            self.output_label.text = PRACTICE_DATA[sub]
        elif cat == "Government Schemes" and sub in SCHEMES_DATA:
            self.output_label.text = f"{sub}:\n\n{SCHEMES_DATA[sub]}"
        elif cat == "Farm Database Check":
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM crops")
            count = cur.fetchone()[0]
            self.output_label.text = f"Local Database Status:\nTotal crops saved: {count}"
        else:
            self.output_label.text = "Please select a valid section and topic."

if __name__ == "__main__":
    AgriApp().run()
