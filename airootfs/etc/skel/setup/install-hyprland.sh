cp -r hyrp ~/.config
cp -r fish ~/.config
cp -r waybar ~/.config
cp -r wofi ~/.config
cd yay && makepkg -si
sudo pacman -S meson git wofi fastfetch fish pkgfile ttf-dejavu powerline-fonts inetutils ttf-font-awesome otf-font-awesome ttf-jetbrains-mono hyprpaper hyprlock sddm kitty kate firefox pipewire thunar pipewire-pulse pipewire-jack waybar nwg-look papirus-icon-theme -y
systemctl --user enable pipewire.service
systemctl --user enable pipewire.socket
systemctl --user start pipewire.service
echo "/bin/fish"
#chsh

sudo systemctl enable sddm
# для моментального включения --now после enable
