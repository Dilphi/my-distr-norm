#!/bin/bash
set -euo pipefail

# Проверка root прав
if [ "$(id -u)" -ne 0 ]; then
  echo "✖ Скрипт должен быть запущен от имени root!" >&2
  exit 1
fi

# Проверка интернет-соединения
if ! ping -c 1 archlinux.org &>/dev/null; then
  echo "✖ Нет интернет-соединения!" >&2
  exit 1
fi

# Выбор диска
echo "Доступные диски:"
lsblk -d -e 7,11 -o NAME,SIZE,MODEL
echo ""
read -p "Введите диск для установки (например: sda или nvme0n1): " DISK

if [ ! -b "/dev/$DISK" ]; then
  echo "Указанный диск /dev/$DISK не найден!" >&2
  exit 1
fi

# Подтверждение выбора диска
read -p "⚠ ВСЕ ДАННЫЕ НА ДИСКЕ /dev/$DISK БУДУТ УДАЛЕНЫ! Продолжить? (y/N): " confirm
if [[ "${confirm,,}" != "y" ]]; then
  echo "Отмена установки."
  exit 0
fi

# Определение разделов
if [[ "$DISK" =~ ^sd[a-z]$ ]]; then
  BOOT="/dev/${DISK}1"
  SWAP="/dev/${DISK}2"
  ROOT="/dev/${DISK}3"
else
  BOOT="/dev/${DISK}p1"
  SWAP="/dev/${DISK}p2"
  ROOT="/dev/${DISK}p3"
fi

# Ручная разметка через cfdisk
echo "⌛ Запуск cfdisk для ручной разметки..."
setfont cyr-sun16
cfdisk "/dev/$DISK"

# Форматирование разделов
echo "⌛ Форматирование разделов..."
mkfs.fat -F32 "$BOOT"
mkswap "$SWAP"
mkfs.ext4 "$ROOT"

# Монтирование
echo "⌛ Монтирование разделов..."
mount "$ROOT" /mnt
mkdir -p /mnt/boot/efi
mount "$BOOT" /mnt/boot/efi
swapon "$SWAP"

echo "⌛ Обновление зеркал через reflector..."
reflector --country Kazakhstan,Russia --latest 10 --sort rate --save /etc/pacman.d/mirrorlist

# Установка базовой системы
echo "⌛ Установка базовой системы..."
pacstrap /mnt base linux linux-firmware sof-firmware base-devel grub efibootmgr \
  nano networkmanager git cmake sassc reflector

# Генерация fstab
echo "⌛ Генерация fstab..."
genfstab -U /mnt > /mnt/etc/fstab

# Копирование пользовательских файлов
echo "⌛ Копирование пользовательских файлов..."
mkdir -p /mnt/root/setup
cp -r hypr /mnt/root/setup/ 2>/dev/null || true
cp -r fish /mnt/root/setup/ 2>/dev/null || true
cp -r waybar /mnt/root/setup/ 2>/dev/null || true
cp -r wofi /mnt/root/setup/ 2>/dev/null || true
cp -r yay /mnt/root/setup/ 2>/dev/null || true
cp -r customize.service /mnt/root/setup/ 2>/dev/null || true
cp -r CyberGRUB-2077-base /mnt/root/setup/ 2>/dev/null || true
cp -r sddm-astronaut-theme /mnt/root/setup/ 2>/dev/null || true
cp -r Graphite-gtk-theme /mnt/root/setup/ 2>/dev/null || true
cp wallpaper.jpg /mnt/root/setup/ 2>/dev/null || true

# Ввод пользовательских данных
while [[ -z "${USERNAME:-}" ]]; do
  read -p "Введите имя пользователя (латинские буквы, без пробелов): " USERNAME
  if [[ ! "$USERNAME" =~ ^[a-zA-Z0-9]+$ ]]; then
    echo "✖ Имя пользователя содержит недопустимые символы!" >&2
    unset USERNAME
  fi
done

while true; do
  read -s -p "Введите пароль для пользователя $USERNAME: " USERPASS
  echo
  if [[ -z "$USERPASS" ]]; then
    echo "✖ Пароль не может быть пустым!" >&2
  else
    break
  fi
done

while true; do
  read -s -p "Введите пароль для root: " ROOTPASS
  echo
  if [[ -z "$ROOTPASS" ]]; then
    echo "✖ Пароль не может быть пустым!" >&2
  else
    break
  fi
done

read -p "Введите часовой пояс (например: Almaty или Tomsk): " TIMEZONE_INPUT

# Сохранение данных
echo "$USERNAME" > /mnt/root/setup/username
echo "$USERPASS" > /mnt/root/setup/userpass
echo "$ROOTPASS" > /mnt/root/setup/rootpass
echo "$TIMEZONE_INPUT" > /mnt/root/setup/timezone


# Выбор окружения
echo "Выберите DE:"
echo "1) KDE Plasma"
echo "2) Hyprland"
while true; do
  read -p "Введите 1 или 2: " SETUP
  if [[ "$SETUP" == "1" ]]; then
    echo "kde" > /mnt/root/setup/.de-choice
    break
  elif [[ "$SETUP" == "2" ]]; then
    echo "hyprland" > /mnt/root/setup/.de-choice
    break
  else
    echo "✖ Неверный выбор окружения!" >&2
  fi
done

# Монтирование системных директорий
mount --bind /dev /mnt/dev
mount --bind /dev/pts /mnt/dev/pts
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys

# Настройка внутри chroot
echo "⌛ Настройка системы в chroot..."
arch-chroot /mnt /bin/bash <<EOF
set -eu

# Чтение сохраненных данных
USERNAME=\$(cat /root/setup/username)
USERPASS=\$(cat /root/setup/userpass)
ROOTPASS=\$(cat /root/setup/rootpass)
TIMEZONE_INPUT=\$(cat /root/setup/timezone)

# Настройка часового пояса
case "\$TIMEZONE_INPUT" in
  [Aa]lmaty) TIMEZONE="Asia/Almaty" ;;
  [Tt]omsk) TIMEZONE="Asia/Tomsk" ;;
  *) TIMEZONE="Asia/Almaty" ;;
esac

ln -sf "/usr/share/zoneinfo/\$TIMEZONE" /etc/localtime
hwclock --systohc

# Локализация
sed -i 's/^#\(ru_RU\.UTF-8\)/\1/' /etc/locale.gen
sed -i 's/^#\(en_US\.UTF-8\)/\1/' /etc/locale.gen
locale-gen
reflector --country Kazakhstan --latest 5 --sort rate --save /etc/pacman.d/mirrorlist

echo "LANG=ru_RU.UTF-8" > /etc/locale.conf
echo "KEYMAP=ru" > /etc/vconsole.conf
echo "FONT=cyr-sun16" >> /etc/vconsole.conf
echo "Arch" > /etc/hostname

# Пользователи и пароли
printf "root:%s\n" "$ROOTPASS" | chpasswd
useradd -m -G wheel -s /bin/bash "\$USERNAME"
printf "%s:%s\n" "$USERNAME" "$USERPASS" | chpasswd
echo "%wheel ALL=(ALL:ALL) ALL" >> /etc/sudoers

# Службы
systemctl enable NetworkManager
loginctl enable-linger "\$USERNAME"

# Установка окружения
DE_CHOICE=\$(cat /root/setup/.de-choice)

if [[ "\$DE_CHOICE" == "kde" ]]; then
  echo "⌛ Установка KDE Plasma..."
  pacman -Syu --noconfirm
  pacman -Sy --noconfirm plasma sddm konsole kate firefox pipewire dolphin \
    pipewire-pulse pipewire-jack fish ark gwenview spectacle

  # Настройка обоев по умолчанию
  mkdir -p /usr/share/wallpapers/MyWallpaper/contents/images/
  cp /root/setup/wallpaper.jpg /usr/share/wallpapers/MyWallpaper/contents/images/
  chmod 644 /usr/share/wallpapers/MyWallpaper/contents/images/wallpaper.jpg

mkdir -p /etc/skel/.config
cat > /etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc <<EOL
[Containments][1][Wallpaper][org.kde.image][General]
Image=file:///usr/share/wallpapers/MyWallpaper/contents/images/wallpaper.jpg
EOL

  mkdir -p /home/"\$USERNAME"/.config
  cp /etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc /home/"\$USERNAME"/.config/
  chown -R "\$USERNAME:\$USERNAME" /home/"\$USERNAME"/.config

systemctl enable sddm
chsh -s /bin/fish "\$USERNAME"

elif [[ "\$DE_CHOICE" == "hyprland" ]]; then
  echo "⌛ Установка Hyprland..."
  pacman -Syu --noconfirm
  pacman -Sy --noconfirm meson git wofi fastfetch fish pkgfile ttf-dejavu \
    powerline-fonts inetutils ttf-font-awesome otf-font-awesome \
    ttf-jetbrains-mono hyprpaper hyprlock sddm kitty kate firefox pipewire \
    thunar pipewire-pulse pipewire-jack waybar nwg-look papirus-icon-theme dbus

  systemctl enable sddm
  systemctl enable dbus
  chsh -s /bin/fish "\$USERNAME"

  # Копирование конфигураций
  mkdir -p "/home/\$USERNAME/.config"
  cp -r /root/setup/{hypr,fish,waybar,wofi} "/home/\$USERNAME/.config/"
  chown -R "\$USERNAME:\$USERNAME" "/home/\$USERNAME"

  # Установка yay
  if [ ! -d "/home/\$USERNAME/yay" ]; then
    sudo -u "\$USERNAME" git clone https://aur.archlinux.org/yay.git "/home/\$USERNAME/yay"
    cd "/home/\$USERNAME/yay" && sudo -u "\$USERNAME" makepkg -si --noconfirm
  fi

fi

# Установка тем
if [ -f "/root/setup/sddm-astronaut-theme/install.sh" ]; then
  chmod +x /root/setup/sddm-astronaut-theme/install.sh
  cd /root/setup/sddm-astronaut-theme
  ./install.sh
fi

if [ -f "/root/setup/Graphite-gtk-theme/install.sh" ]; then
  chmod +x /root/setup/Graphite-gtk-theme/install.sh
  cd /root/setup/Graphite-gtk-theme
  ./install.sh
fi

# Настройка темы SDDM
mkdir -p /etc/sddm.conf.d
echo '[Theme]' > /etc/sddm.conf.d/theme.conf
echo 'Current=astronaut' >> /etc/sddm.conf.d/theme.conf

if [ ! -d /sys/firmware/efi ]; then
  echo "✖ Не найден /sys/firmware/efi — установка возможна только в UEFI!" >&2
  exit 1
fi

# Загрузчик
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB --recheck

# Установка темы GRUB вручную
echo "⌛ Установка темы GRUB CyberGRUB-2077..."
cd /root/setup/CyberGRUB-2077-base
./install.sh

# Настройка GRUB
grub-mkconfig -o /boot/grub/grub.cfg

# Очистка
shred -u /root/setup/username /root/setup/userpass /root/setup/rootpass /root/setup/timezone
EOF

# Завершение
echo "⌛ Завершение установки..."
umount -R /mnt/dev/pts
umount -R /mnt/dev
umount -R /mnt/proc
umount -R /mnt/sys
umount -R /mnt
swapoff "$SWAP"

echo "✅ Установка завершена! Перезагрузка через 5 секунд..."
sleep 5
reboot
