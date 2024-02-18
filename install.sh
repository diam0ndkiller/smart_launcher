sudo apt install -y python3 python3-pyqt5 qt5ct onboard xfpanel-switch
sudo apt install -y nautilus gnome-calculator musescore geogebra firefox libreoffice

mkdir -p ~/scripts/smart_launcher
cp -r ./* ~/scripts/smart_launcher/
cd ~/scripts/smart_launcher
cp ./install/config.json ./config/

chmod -R +x ./install/autostart/
chmod +x ./install.sh
chmod +x ./smart_launcher.py

sudo dpkg -i skippy-xd_0.5-1.deb

mkdir -p ~/.config/autostart
cp ./install/autostart/skippy-xd.desktop ~/.config/autostart/
cp ./install/autostart/onboard.desktop ~/.config/autostart/
cp ./install/autostart/smart_launcher.desktop ~/.config/autostart/

mkdir -p ~/.config/skippy-xd
cp ./install/skippy-xd.rc ~/.config/skippy-xd/

xfce4-panel-profiles load ./smart_launcher.tar.bz2
mkdir ~/.icons/
mkdir ~/.themes/
unzip -qo ./install/icons/smart_launcher.zip -d ~/.icons/
unzip -qo ./install/themes/smart_launcher.zip -d ~/.themes/