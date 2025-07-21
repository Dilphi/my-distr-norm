#!/bin/bash

echo "[*] Начинаем кастомизацию системы..."

WALLPAPER="/usr/share/wallpapers/wallpaper.jpg"
USER_NAME="user"

# Проверка наличия обоев
if [ ! -f "$WALLPAPER" ]; then
  echo "[!] Обои не найдены в $WALLPAPER"
else
  echo "[✓] Обои найдены: $WALLPAPER"
fi

# Заменяем фон SDDM (если используется breeze)
SDDM_QML="/usr/share/sddm/themes/breeze/Background.qml"
if [ -f "$SDDM_QML" ]; then
  sed -i "s|source: .*|source: \"$WALLPAPER\"|" "$SDDM_QML"
  echo "[✓] Обои SDDM обновлены"
else
  echo "[!] SDDM тема breeze не найдена: $SDDM_QML"
fi

# Настройка Plasma обоев для новых пользователей
SKEL_CONF="/etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc"
mkdir -p "$(dirname "$SKEL_CONF")"
cat > "$SKEL_CONF" <<EOF
[Containments][1][Wallpaper][org.kde.image][General]
Image=file://$WALLPAPER
EOF
echo "[✓] Обои Plasma заданы для новых пользователей"

# Настройка Plasma обоев для пользователя user (если он уже создан)
if id "$USER_NAME" &>/dev/null; then
  USER_CONF="/home/$USER_NAME/.config/plasma-org.kde.plasma.desktop-appletsrc"
  mkdir -p "$(dirname "$USER_CONF")"
  cp "$SKEL_CONF" "$USER_CONF"
  chown -R "$USER_NAME:$USER_NAME" "/home/$USER_NAME/.config"
  echo "[✓] Обои Plasma заданы для пользователя $USER_NAME"
else
  echo "[!] Пользователь '$USER_NAME' ещё не создан. Обои будут применены через /etc/skel"
fi

echo "[✓] Кастомизация завершена."
