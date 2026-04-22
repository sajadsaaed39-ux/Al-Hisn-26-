import random, sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (0.01, 0.02, 0.08, 1)

class GameDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("alhisn26.db")
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT, rating INTEGER, price INTEGER);
            CREATE TABLE IF NOT EXISTS user_stats (id INTEGER PRIMARY KEY, coins INTEGER, wins INTEGER);
        ''')
        self.cursor.execute("SELECT COUNT(*) FROM players")
        if self.cursor.fetchone()[0] == 0:
            players = [("يونس محمود", 99, 99999), ("Lionel Messi", 97, 50000), ("C. Ronaldo", 96, 48000)]
            self.cursor.executemany("INSERT INTO players (name, rating, price) VALUES (?,?,?)", players)
            self.cursor.execute("INSERT OR IGNORE INTO user_stats (id, coins, wins) VALUES (1, 10000, 0)")
        self.conn.commit()

class MainMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        layout.add_widget(Label(text="AL-HISN 26", font_size='40sp', pos_hint={'center_y':0.8}, bold=True, color=(1, 0.8, 0, 1)))
        btn_box = BoxLayout(orientation='vertical', size_hint=(0.6, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.4}, spacing=15)
        for txt, target in [("🎮 ابدأ", 'match'), ("🏪 المتجر", 'market')]:
            btn = Button(text=txt, background_color=(0.1, 0.4, 0.8, 1), font_size='20sp')
            btn.bind(on_release=lambda x, t=target: setattr(self.manager, 'current', t))
            btn_box.add_widget(btn)
        layout.add_widget(btn_box)
        self.add_widget(layout)

class MatchScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation='vertical', padding=20)
        self.lbl = Label(text="اضغط للعب", font_size='25sp')
        self.layout.add_widget(self.lbl)
        btn = Button(text="عودة", size_hint_y=0.2); btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(btn)
        self.add_widget(self.layout)

class MarketScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=10)
        scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        layout.add_widget(scroll)
        btn = Button(text="رجوع", size_hint_y=0.1); btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(btn)
        self.add_widget(layout)

class AlHisnApp(App):
    def build(self):
        self.db = GameDatabase()
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(MatchScreen(name='match'))
        sm.add_widget(MarketScreen(name='market'))
        return sm

if __name__ == "__main__":
    AlHisnApp().run()
    
