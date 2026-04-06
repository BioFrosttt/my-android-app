from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.snackbar import Snackbar

store = JsonStore("user.json")

KV = '''
ScreenManager:
    LoginScreen:
    DashboardScreen:

<LoginScreen>:
    name: "login"

    MDScreen:
        MDTopAppBar:
            title: "Login"

        MDBoxLayout:
            orientation: "vertical"
            padding: 30
            spacing: 20
            pos_hint: {"center_y": 0.5}

            MDTextField:
                id: username
                hint_text: "Enter your name"
                mode: "outlined"

            MDRaisedButton:
                text: "Login"
                pos_hint: {"center_x": 0.5}
                on_release: app.login()

<DashboardScreen>:
    name: "dashboard"

    MDScreen:
        MDTopAppBar:
            title: "Dashboard"
            left_action_items: [["arrow-left", lambda x: app.logout()]]
            right_action_items: [["theme-light-dark", lambda x: app.toggle_theme()]]

        MDBoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 20

            MDLabel:
                id: welcome_label
                text: "Welcome!"
                halign: "center"
                font_style: "H5"

            MDCard:
                padding: 20
                radius: [15]
                elevation: 4

                MDLabel:
                    text: "📊 Your Dashboard Card"
                    halign: "center"

            MDCard:
                padding: 20
                radius: [15]
                elevation: 4

                MDLabel:
                    text: "🔥 Another Feature Card"
                    halign: "center"
'''

class LoginScreen(Screen):
    pass

class DashboardScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def on_start(self):
        # Auto login if saved
        if store.exists("user"):
            username = store.get("user")["name"]
            self.go_to_dashboard(username)

    def login(self):
        username = self.root.get_screen("login").ids.username.text

        if username.strip() == "":
            Snackbar(text="Please enter your name").open()
            return

        store.put("user", name=username)
        Snackbar(text="Login successful!").open()
        self.go_to_dashboard(username)

    def go_to_dashboard(self, username):
        dashboard = self.root.get_screen("dashboard")
        dashboard.ids.welcome_label.text = f"Welcome, {username}!"
        self.root.current = "dashboard"

    def logout(self):
        store.delete("user")
        Snackbar(text="Logged out").open()
        self.root.current = "login"

    def toggle_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

MyApp().run()
