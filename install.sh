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
git clone https://github.com/richardgv/skippy-xd
cd skippy-xd
sudo make install
cd ../../

mkdir -p ~/.config/autostart
cp ./install/autostart/* ~/.config/autostart/
chmod +x ~/.config/autostart/*

mkdir -p ~/.config/skippy-xd
cp ./install/skippy-xd.rc ~/.config/skippy-xd/

mkdir -p ~/.config/touchegg
cp ./install/touchegg.conf ~/.config/touchegg/

mkdir -p ~/.xournal
cp ./install/config ~/.xournal/

xfce4-panel-profiles load ./install/smart_launcher.tar.bz2
mkdir ~/.icons/
mkdir ~/.themes/
unzip -qo ./install/icons/smart_launcher.zip -d ~/.icons/
unzip -qo ./install/themes/smart_launcher.zip -d ~/.themes/

qt5ct
