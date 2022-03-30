import string
from xml.etree.ElementInclude import include
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import db # use this line to import the db class

# ----------------------
# Kivy Window management
# ----------------------

class SplashWindow(Screen):
    
    pass

class LoginWindow(Screen):

    def login_released(self, usnm_input, passw_input):
        usnm_input.text = ""
        passw_input.text = ""

        return

    pass

class ProfileWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

# ----------------------
# Main Kivy app
# ----------------------
class MyMainApp(App):
    def build(self):
        return kv
    pass


# ----------------------
# Main application function
# ----------------------
if __name__ == "__main__":
    # # Teo: use these lines to manipulate database
    # Database initialization and tests 
    db.init()
    db.un_exists('userNameThatDoesNotExist')
    db.profile_delete('userNameThatDoesNotExist')
    db.profile_delete('davidDelSol')
    db.profile_new(
        'davidDelSol',
        'encrypted?',
        'david',
        'aloka',
        'test@preform.io',
        'salsa,extended intelligence,marathon running in a full suit'
    )
    db.profile_new(
        'Python733t',
        'encrypted?',
        'Doroteo ',
        'Bonilla',
        'doabonilla@yahoo.com',
        'work,school,sleep,repeat'
    )
    db.un_login('davidDelSol', 'encrypted?')
    db.profile_update('davidDelSol', pw = 'definitelyNotEncripted!')
    db.un_login('davidDelSol', 'definitelyNotEncripted!')
    db.un_exists('davidDelSol')
    db.profile_print(all = True)
    db.profile_print(['Python733t'])
    db.profile_print('Python733t')

    # Run Kivy app
    MyMainApp().run()