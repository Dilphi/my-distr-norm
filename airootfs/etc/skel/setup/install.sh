#!/bin/bash

# Проверка root прав
if [ "$(id -u)" -ne 0 ]; then
  echo "Скрипт должен быть запущен от имени root!" 1>&2
  exit 1
fi

# Показываем список дисков
echo "Доступные диски:"
lsblk -d -e 7,11 -o NAME,SIZE,MODEL
echo ""
read -p "Введите диск для установки (например: sda или nvme0n1): " DISK

if [ ! -b "/dev/$DISK" ]; then
  echo "Указанный диск /dev/$DISK не найден!"
  exit 1
fi

BOOT="/dev/${DISK}p1"
SWAP="/dev/${DISK}p2"
ROOT="/dev/${DISK}p3"

if [[ "$DISK" =~ ^sd[a-z]$ ]]; then
  BOOT="/dev/${DISK}1"
  SWAP="/dev/${DISK}2"
  ROOT="/dev/${DISK}3"
fi

setfont cyr-sun16
cfdisk "/dev/$DISK"

mkfs.fat -F 32 "$BOOT"
mkswap "$SWAP"
mkfs.ext4 "$ROOT"

mount "$ROOT" /mnt
mkdir -p /mnt/boot/efi
mount "$BOOT" /mnt/boot/efi
swapon "$SWAP"

pacstrap /mnt base linux linux-firmware sof-firmware base-devel grub efibootmgr nano networkmanager

genfstab /mnt > /mnt/etc/fstab

# Копируем пользовательские файлы
cp install-pkg.sh /mnt
cp -r hyrp /mnt
cp -r fish /mnt
cp -r waybar /mnt
cp -r wofi /mnt
cp -r yay /mnt
cp install-hyprland.sh /mnt
cp customize.sh /mnt
cp customize_airootfs.sh /mnt

# Выполняем настройку в chroot
arch-chroot /mnt /bin/bash <<EOF
ln -sf /usr/share/zoneinfo/Asia/Almaty /etc/localtime
hwclock --systohc
sed -i 's/^#\(ru_RU.UTF-8 UTF-8\)/\1/' /etc/locale.gen
locale-gen
echo "LANG=ru_RU.UTF-8" > /etc/locale.conf
echo "Arch" > /etc/hostname

echo "root:1234" | chpasswd
useradd -m -G wheel -s /bin/bash user
echo "user:1234" | chpasswd
sed -i 's/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers

systemctl enable NetworkManager

# ⬇️ Настройка Plasma, SDDM и PipeWire
chmod +x /customize.sh
/customize.sh

pacman -Sy --noconfirm plasma sddm konsole kate firefox pipewire dolphin pipewire-pulse pipewire-jack

systemctl enable sddm
systemctl enable pipewire.socket

# Установка загрузчика
grub-install /dev/$DISK
grub-mkconfig -o /boot/grub/grub.cfg
EOF

umount -a
echo "Установка завершена! Перезагрузка системы."
reboot
