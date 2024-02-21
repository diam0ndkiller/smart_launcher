#!/bin/python3

import sys

import configparser
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import subprocess
import sqlite3
import requests

os.chdir(os.path.dirname(os.path.abspath(__file__)))

VERSION = "V1.3"

EXPANDING_SPACER_V = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
EXPANDING_SPACER_H = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

FACTOR = 1

FIREFOX_PROFILES_INI = configparser.ConfigParser()
FIREFOX_PROFILES_INI.read(os.path.expanduser('~/.mozilla/firefox/profiles.ini'))
FIREFOX_PROFILE = FIREFOX_PROFILES_INI['Profile0']['Path']

print(FIREFOX_PROFILE)


with open("config/config.json", "r") as file:
    CONFIG = eval(file.read())

with open("config/apps.json", "r") as file:
    APPS = eval(file.read())

with open("config/action_buttons.json", "r") as file:
    ACTION_BUTTONS = eval(file.read())

with open("config/translations.json", "r") as file:
    TRANSLATIONS = eval(file.read())



class ShadowLabel(QLabel):
    def __init__(self, text = None):
        super().__init__(text)
        self.initUI()

    def initUI(self):
        default_text_color = self.palette().color(self.foregroundRole())

        shadow_color = QColor(255 if default_text_color.red() < 128 else 0,
                              255 if default_text_color.green() < 128 else 0,
                              255 if default_text_color.blue() < 128 else 0)

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setColor(shadow_color)
        shadow_effect.setBlurRadius(int(FACTOR * 10))
        shadow_effect.setOffset(0, 0)
        self.setGraphicsEffect(shadow_effect)



class FocusDebug(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            print(f"{obj.objectName()} gained focus")
        elif event.type() == QEvent.FocusOut:
            print(f"{obj.objectName()} lost focus")
        print("test")



class LauncherWidget(QWidget):
    def __init__(self):
        global FACTOR

        screen_size = QDesktopWidget().screenGeometry()
        screen_width = screen_size.width()
        screen_height = screen_size.height()

        print(screen_height)

        FACTOR = screen_height / 1080

        print(FACTOR)

        self.background = QPixmap(CONFIG["background"])

        super().__init__()
        self.initUI()



    def paintEvent(self, event):
        painter = QPainter(self)
        widWidth = self.width()
        widHeight = self.height()
        pixmap = self.background.scaled(widWidth, widHeight, Qt.KeepAspectRatioByExpanding)
        painter.drawPixmap((self.width() - pixmap.width()) // 2, (self.height() - pixmap.height()) // 2, pixmap)
        super().paintEvent(event)



    def initUI(self):
        self.setLayout(self.main_layout())
        self.setWindowTitle(f'{get_translation("heading")} {VERSION}')
        self.setWindowIcon(QIcon("assets/appicon.png"))
        self.setWindowFlag(Qt.FramelessWindowHint)


    def main_layout(self):
        main_layout = QStackedLayout()

        layout = QVBoxLayout()

        layout.addWidget(self.heading_box_widget())
        layout.addWidget(self.content_box_widget())

        widget = QWidget()
        widget.setLayout(layout)

        main_layout.addWidget(widget)

        return main_layout



    def heading_box_widget(self):
        heading_box_layout = QHBoxLayout()

        heading_label = ShadowLabel(f'{get_translation("heading")} {VERSION}')
        heading_label.setFont(QFont("Ubuntu", int(FACTOR * 15), QFont.Bold))

        heading_box_layout.addItem(EXPANDING_SPACER_H)
        heading_box_layout.addWidget(heading_label)

        heading_box_widget = QWidget()
        heading_box_widget.setLayout(heading_box_layout)

        return heading_box_widget



    def content_box_widget(self):
        content_box_layout = QHBoxLayout()

        content_box_layout.addWidget(self.left_side_widget())
        content_box_layout.addItem(EXPANDING_SPACER_H)
        content_box_layout.addWidget(self.center_widget())
        content_box_layout.addItem(EXPANDING_SPACER_H)
        content_box_layout.addWidget(self.right_side_widget())

        content_box_widget = QWidget()
        content_box_widget.setLayout(content_box_layout)

        return content_box_widget



    def left_side_widget(self):
        left_side_layout = QVBoxLayout()

        left_side_layout.addItem(EXPANDING_SPACER_V)
        left_side_layout.addWidget(self.app_heading_box_widget())
        left_side_layout.addWidget(self.app_grid_widget())
        left_side_layout.addItem(EXPANDING_SPACER_V)
        left_side_layout.addWidget(self.action_button_widget())

        left_side_widget = QWidget()
        left_side_widget.setLayout(left_side_layout)

        return left_side_widget



    def app_heading_box_widget(self):
        app_heading_box_layout = QHBoxLayout()

        app_heading_label = ShadowLabel(get_translation("heading.apps"))
        app_heading_label.setFont(QFont("Ubuntu", int(FACTOR * 15), QFont.Bold))

        app_heading_box_layout.addItem(EXPANDING_SPACER_H)
        app_heading_box_layout.addWidget(app_heading_label)
        app_heading_box_layout.addItem(EXPANDING_SPACER_H)

        app_heading_box_widget = QWidget()
        app_heading_box_widget.setLayout(app_heading_box_layout)

        return app_heading_box_widget



    def app_grid_widget(self):
        app_grid_layout = QGridLayout()

        for i in range(4):
            for j in range(4):
                button = QPushButton()
                button.setFixedSize(int(FACTOR * 120), int(FACTOR * 120))

                app_index = i * 4 + j
                if len(APPS) > app_index:
                    command, icon, key = APPS[app_index]

                    button.setIcon(QIcon.fromTheme(icon))
                    button.setIconSize(QSize(int(FACTOR * 96), int(FACTOR * 96)))

                    button.clicked.connect(self.launch_application)
                    button.setProperty("command", command)

                    label = ShadowLabel(get_translation(key))
                    label.setFont(QFont("Ubuntu", int(FACTOR * 12), QFont.Bold))
                    app_grid_layout.addWidget(label, i*2+1, j)

                app_grid_layout.addWidget(button, i*2, j)

        app_grid_layout.setVerticalSpacing(10)
        app_grid_layout.setHorizontalSpacing(10)

        app_grid_widget = QWidget()
        app_grid_widget.setLayout(app_grid_layout)

        return app_grid_widget



    def action_button_widget(self):
        action_button_layout = QHBoxLayout()

        for command, icon, key in ACTION_BUTTONS:
            button = QPushButton()
            button.setFixedSize(int(FACTOR * 60), int(FACTOR * 60))

            button.setIcon(QIcon.fromTheme(icon))
            button.setIconSize(QSize(int(FACTOR * 48), int(FACTOR * 48)))
            button.setToolTip(get_translation(key))

            button.clicked.connect(self.launch_application)
            button.setProperty("command", command)

            action_button_layout.addWidget(button)
        action_button_layout.addWidget(self.settings_button())
        action_button_layout.addItem(EXPANDING_SPACER_H)


        action_button_layout.setSpacing(10)

        action_button_widget = QWidget()
        action_button_widget.setLayout(action_button_layout)

        return action_button_widget



    def settings_button(self):
        button = QPushButton()
        button.setFixedSize(int(FACTOR * 60), int(FACTOR * 60))

        button.setIcon(QIcon.fromTheme("preferences-system"))
        button.setIconSize(QSize(int(FACTOR * 48), int(FACTOR * 48)))
        button.setToolTip(get_translation("action_buttons.settings"))

        button.clicked.connect(self.open_settings_dialog)

        return button



    def center_widget(self):
        center_layout = QVBoxLayout()

        center_layout.addItem(EXPANDING_SPACER_V)
        center_layout.addWidget(self.clock_widget())
        center_layout.addItem(EXPANDING_SPACER_V)

        center_widget = QWidget()
        center_widget.setLayout(center_layout)

        return center_widget



    def clock_widget(self):
        self.time_label = ShadowLabel()
        self.time_label.setFont(QFont("Ubuntu", int(FACTOR * 60), QFont.Normal))

        self.update_time_timer = QTimer(self)
        self.update_time_timer.timeout.connect(self.update_time)
        self.update_time_timer.start(1000)

        self.update_time()

        return self.time_label



    def update_time(self):
        current_time = QTime.currentTime()

        time_text = current_time.toString('hh:mm:ss')

        self.time_label.setText(time_text)



    def right_side_widget(self):
        right_side_layout = QVBoxLayout()

        right_side_layout.addItem(EXPANDING_SPACER_V)
        right_side_layout.addWidget(self.samba_widget())
        right_side_layout.addItem(EXPANDING_SPACER_V)
        right_side_layout.addWidget(self.bookmark_heading_box_widget())
        right_side_layout.addWidget(self.bookmark_grid_widget())

        right_side_widget = QWidget()
        right_side_widget.setLayout(right_side_layout)

        return right_side_widget



    def samba_widget(self):
        samba_layout = QVBoxLayout()

        self.username_input = QLineEdit(focusPolicy=Qt.StrongFocus)
        self.username_input.setPlaceholderText(get_translation("samba.username"))
        self.username_input.setFont(QFont("Ubuntu", int(FACTOR * 10), QFont.Normal))
        samba_layout.addWidget(self.username_input)

        """self.password_input = QLineEdit(focusPolicy=Qt.StrongFocus)
        self.password_input.setPlaceholderText(get_translation("samba.password"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Ubuntu", int(FACTOR * 10), QFont.Normal))
        samba_layout.addWidget(self.password_input)"""

        self.samba_login_button = QPushButton(get_translation("samba.login"))
        self.samba_login_button.clicked.connect(self.login_to_samba)
        self.samba_login_button.setFont(QFont("Ubuntu", int(FACTOR * 10), QFont.Normal))
        samba_layout.addWidget(self.samba_login_button)

        samba_widget = QWidget()
        samba_widget.setLayout(samba_layout)

        return samba_widget



    def bookmark_heading_box_widget(self):
        bookmark_heading_box_layout = QHBoxLayout()

        bookmark_heading_label = ShadowLabel(get_translation("heading.bookmarks"))
        bookmark_heading_label.setFont(QFont("Ubuntu", int(FACTOR * 15), QFont.Bold))

        bookmark_heading_box_layout.addItem(EXPANDING_SPACER_H)
        bookmark_heading_box_layout.addWidget(bookmark_heading_label)
        bookmark_heading_box_layout.addItem(EXPANDING_SPACER_H)

        bookmark_heading_box_widget = QWidget()
        bookmark_heading_box_widget.setLayout(bookmark_heading_box_layout)

        return bookmark_heading_box_widget



    def bookmark_grid_widget(self):
        self.update_bookmarks()

        bookmark_grid_widget = QWidget()
        bookmark_grid_widget.setLayout(self.bookmark_grid_layout)

        return bookmark_grid_widget



    def update_bookmarks(self):
        os.system("mkdir tmp")
        os.system(f'cp "{os.path.expanduser(f"~/.mozilla/firefox/{FIREFOX_PROFILE}/places.sqlite")}" "./tmp/"')

        conn = sqlite3.connect(os.path.expanduser(f'tmp/places.sqlite'))
        cursor = conn.cursor()

        cursor.execute("select b.title, p.url from moz_bookmarks b join moz_places p on b.fk = p.id where b.parent = 3;")
        bookmarks = cursor.fetchall()

        conn.close()

        self.bookmark_grid_layout = QGridLayout()

        self.bookmark_grid_layout.setVerticalSpacing(10)
        self.bookmark_grid_layout.setHorizontalSpacing(10)

        for i in range(4):
            for j in range(4):
                button = QPushButton()
                button.setFixedSize(int(FACTOR * 100), int(FACTOR * 100))

                bookmark_index = i * 4 + j
                if len(bookmarks) > bookmark_index:
                    title, url = bookmarks[bookmark_index]

                    button.setIcon(self.get_favicon(url, int(FACTOR * 64)))
                    button.setIconSize(QSize(int(FACTOR * 64), int(FACTOR * 64)))
                    button.setToolTip(title)

                    button.clicked.connect(self.open_bookmark)
                    button.setProperty("url", url)

                    font = QFont("Ubuntu", int(FACTOR * 10), QFont.Bold)
                    label = ShadowLabel(shorten_string_to_width(title, int(FACTOR * 95), font))
                    label.setFont(font)
                    self.bookmark_grid_layout.addWidget(label, i*2+1, j)

                self.bookmark_grid_layout.addWidget(button, i*2, j)



    def get_favicon(self, url, size):
        favicons_folder = 'favicons'
        if not os.path.exists(favicons_folder):
            os.makedirs(favicons_folder)

        favicon_filename = os.path.join(favicons_folder, url.split('//')[-1].split('/')[0] + '.ico')

        if os.path.exists(favicon_filename):
            return QIcon(scale_icon(QIcon(favicon_filename), size, size))
        else:
            response = requests.get(f"https://www.google.com/s2/favicons?sz={256}&domain_url={url}")
            favicon_url = response.url
            try:
                subprocess.run(['wget', '-O', favicon_filename, favicon_url], stderr=subprocess.PIPE, check=True)
                return QIcon(scale_icon(QIcon(favicon_filename), size, size))
            except subprocess.CalledProcessError as e:
                print(f"Failed to download favicon: {e}")
                os.system('rm "' + favicon_filename + '"')
                return QIcon.fromTheme("applications-internet")



    def open_bookmark(self, item):
        sender = self.sender()
        url = sender.property("url")
        subprocess.Popen(["firefox", url])



    def launch_application(self):
        sender = self.sender()
        command = sender.property("command")
        if command == "#exit": sys.exit()
        if command == "#restart": restart()
        subprocess.Popen(command, shell=True)



    def login_to_samba(self):
        username = self.username_input.text()
        
        if not username: return

        #mount_command = ["mount", "-t", "cifs", f"//{server_address}{share_path}", mount_point, "-o", f"username={username},password={password}"]
        mount_command = ["nautilus", f"smb://{username}@{CONFIG['schulserver']}/{username}"]

        subprocess.Popen(mount_command)
        self.samba_login_button.setText(get_translation("samba.logged-in"))



    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.show()



class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()



    def initUI(self):
        self.setLayout(self.main_layout())
        self.setWindowTitle(get_translation("settings.heading"))
        self.setWindowIcon(QIcon("assets/appicon.png"))
        self.setGeometry(int(FACTOR * 800), int(FACTOR * 100), int(FACTOR * 500), int(FACTOR * 300))



    def main_layout(self):
        main_layout = QStackedLayout()

        layout = QVBoxLayout()

        layout.addWidget(self.heading_box_widget())
        layout.addWidget(self.content_box_widget())
        layout.addItem(EXPANDING_SPACER_V)

        widget = QWidget()
        widget.setLayout(layout)

        main_layout.addWidget(widget)

        return main_layout



    def heading_box_widget(self):
        heading_box_layout = QHBoxLayout()

        heading_label = QLabel(get_translation("settings.heading"))
        heading_label.setFont(QFont("Ubuntu", int(FACTOR * 15), QFont.Bold))

        heading_box_layout.addItem(EXPANDING_SPACER_H)
        heading_box_layout.addWidget(heading_label)
        heading_box_layout.addItem(EXPANDING_SPACER_H)

        heading_box_widget = QWidget()
        heading_box_widget.setLayout(heading_box_layout)

        return heading_box_widget



    def content_box_widget(self):
        content_box_layout = QHBoxLayout()

        content_box_layout.addWidget(self.language_button_widget())
        content_box_layout.addItem(EXPANDING_SPACER_H)
        content_box_layout.addWidget(self.background_button_widget())

        content_box_widget = QWidget()
        content_box_widget.setLayout(content_box_layout)

        return content_box_widget



    def language_button_widget(self):
        layout = QHBoxLayout()

        language_menu = QMenu(self)
        language_menu.addAction("EN", lambda : set_language("EN"))
        language_menu.addAction("DE", lambda : set_language("DE"))

        button = QPushButton(get_translation("settings.language"))
        button.setFont(QFont("Ubuntu", int(FACTOR * 12), QFont.Normal))

        button.setIcon(QIcon(f"assets/flag-{CONFIG['language']}.png"))
        button.setMenu(language_menu)

        layout.addWidget(button)
        layout.addItem(EXPANDING_SPACER_H)

        widget = QWidget()
        widget.setLayout(layout)

        return widget



    def background_button_widget(self):
        layout = QHBoxLayout()
        layout = QHBoxLayout()

        button = QPushButton(get_translation("settings.change-background"))
        button.setFont(QFont("Ubuntu", int(FACTOR * 12), QFont.Normal))

        button.setIcon(QIcon.fromTheme("insert-image"))
        button.clicked.connect(self.open_file_dialog)

        layout.addWidget(button)
        layout.addItem(EXPANDING_SPACER_H)

        widget = QWidget()
        widget.setLayout(layout)

        return widget



    def open_file_dialog(self):
        global CONFIG

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Image Files (*.jpg *.png *.JPG *.PNG)")
        file_dialog.setDirectory("assets/wallpapers/")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                CONFIG["background"] = selected_files[0]
                os.system(os.path.expanduser(f"sed -i 's|background = .*|background = {selected_files[0]}|' '~/.config/skippy-xd/skippy-xd.rc'"))
                save_config()
                restart()



def shorten_string_to_width(s, max_width, font):
    font_metrics = QFontMetrics(font)
    ellipsis_width = font_metrics.width('...')
    
    width = font_metrics.width(s)
    
    if width <= max_width:
        return s
    elif width + ellipsis_width <= max_width:
        return s
    else:
        # String needs to be shortened to fit within the maximum width
        for i in range(len(s)):
            if font_metrics.width(s[:i] + '...') > max_width:
                return s[:i-1] + '...'



def scale_icon(icon, width, height):
    original_width = icon.availableSizes()[0].width()
    original_height = icon.availableSizes()[0].height()

    print(original_width, width)
    pixmap = icon.pixmap(width, height)
    
    if width >= original_width:
        pixmap = pixmap.scaled(width, height, transformMode=Qt.FastTransformation)
    else:
        pixmap = pixmap.scaled(width, height, transformMode=Qt.SmoothTransformation)

    return QIcon(pixmap)



def save_config():
    with open("config/config.json", "w") as file:
        file.write(str(CONFIG))



def set_language(l):
    global CONFIG
    CONFIG["language"] = l
    save_config()
    restart()



def restart():
    subprocess.Popen([sys.executable, sys.argv[0]])
    sys.exit()



def get_translation(key):
    if CONFIG["language"] in TRANSLATIONS and key in TRANSLATIONS[CONFIG["language"]]:
        return TRANSLATIONS[CONFIG["language"]][key]
    elif key in TRANSLATIONS["EN"]:
        return TRANSLATIONS["EN"][key]
    else:
        return key



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setCursorFlashTime(50)
    launcher = LauncherWidget()
    launcher.showMaximized()
    sys.exit(app.exec_())
