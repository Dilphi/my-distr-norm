setfont cyr-sun 16
sudo chmod +x customize.sh
sudo ./customize.sh
sudo pacman -S plasma sddm
sudo pacman -S konsole kate firefox pipewire dolphin pipewire-pulse pipewire-jack -y
systemctl --user enable pipewire.service
systemctl --user enable pipewire.socket
systemctl --user start pipewire.service
sudo systemctl enable --now sddm
