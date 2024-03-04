sudo apt update
sudo apt install -y --reinstall libc6 build-essentials
sudo apt install -y python3 python3-pyqt5 python3-requests qt5ct onboard xfce4-panel-profiles xfpanel-switch qt5-gtk-platformtheme qt5-gtk2-platformtheme git touchegg
sudo apt install -y nautilus gnome-calculator musescore geogebra firefox libreoffice

mkdir -p ~/scripts/smart_launcher
cp -r ./* ~/scripts/smart_launcher/
cd ~/scripts/smart_launcher
cp ./install/config.json ./config/

chmod +x ./install.sh
chmod +x ./smart_launcher.py

mkdir tmp
cd tmp
sudo apt install -y libimlib2-dev, libfontconfig1-dev, libfreetype6-dev, libx11-dev, libxext-dev, libxft-dev, libxrender-dev, zlib1g-dev, libxinerama-dev, libxcomposite-dev, libxdamage-dev, libxfixes-dev, libxmu-dev
git clone https://github.com/richardgv/skippy-xd
cd skippy-xd
sudo make install
cd ../../

mkdir -p ~/.config/autostart
cp ./install/autostart/* ~/.config/autostart/
echo Exec=$HOME/scripts/smart_launcher/smart_launcher.py >> ~/.config/autostart/smart_launcher.desktop
echo Icon=$HOME/scripts/smart_launcher/appicon.png >> ~/.config/autostart/smart_launcher.desktop
chmod +x ~/.config/autostart/*

mkdir -p ~/.config/skippy-xd
cp ./install/skippy-xd.rc ~/.config/skippy-xd/

mkdir -p ~/.config/touchegg
cp ./install/touchegg.conf ~/.config/touchegg/

mkdir -p ~/.xournal
cp ./install/config ~/.xournal/

firefox -setDefaultPref dom.w3c_touch_events.enabled 1
echo export MOZ_USE_XINPUT2=1 >> ~/.profile

xfce4-panel-profiles load ./install/smart_launcher.tar.bz2
mkdir ~/.icons/
mkdir ~/.themes/
unzip -qo ./install/icons/smart_launcher.zip -d ~/.icons/
unzip -qo ./install/themes/smart_launcher.zip -d ~/.themes/

onboard
qt5ct
xfwm4-settings
xfce4-appearance-settings
xfce4-display-settings
xfce4-settings-manager
