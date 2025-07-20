#!/bin/bash

# Меняем фон в SDDM теме breeze
sed -i 's|source: .*|source: "/usr/share/wallpapers/wallpaper.jpg"|g' \
  /usr/share/sddm/themes/breeze/Background.qml
