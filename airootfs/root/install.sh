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

# Проверяем, что диск существует
if [ ! -b "/dev/$DISK" ]; then
  echo "Указанный диск /dev/$DISK не найден!"
  exit 1
fi

# Объявляем переменные для разделов
BOOT="/dev/${DISK}p1"
SWAP="/dev/${DISK}p2"
ROOT="/dev/${DISK}p3"

# Если диск не NVMe, то разделы без `p`
if [[ "$DISK" =~ ^sd[a-z]$ ]]; then
  BOOT="/dev/${DISK}1"
  SWAP="/dev/${DISK}2"
  ROOT="/dev/${DISK}3"
fi

# Настройка шрифта
setfont cyr-sun16

# Разметка вручную
cfdisk "/dev/$DISK"

# Форматирование
mkfs.fat -F 32 "$BOOT"
mkswap "$SWAP"
mkfs.ext4 "$ROOT"

# Монтирование
mount "$ROOT" /mnt
mkdir -p /mnt/boot/efi
mount "$BOOT" /mnt/boot/efi
swapon "$SWAP"

# Базавая установка сиситемы
pacstrap /mnt base linux linux-firmware sof-firmware base-devel grub efibootmgr nano networkmanager
# Автоматическое монтирование после входа в систему
genfstab /mnt > /mnt/etc/fstab
# Копирования файла с установкой пакетов
cp install-pkg.sh /mnt
cp -r hyrp /mnt
cp -r fish /mnt
cp -r waybar /mnt
cp -r wofi /mnt
cp -r yay /mnt
cp install-hyprland.sh /mnt
cp customize.sh /mnt

# Выполняем chroot
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
grub-install /dev/$DISK
grub-mkconfig -o /boot/grub/grub.cfg
EOF


umount -a
# Завершающие шаги
echo "Установка завершена! Перезагрузка системы."
reboot
