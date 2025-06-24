#!/bin/bash

# Проверка root прав
if [ "$(id -u)" -ne 0 ]; then
  echo "Скрипт должен быть запущен от имени root!" 1>&2
  exit 1
fi
# Делаем нормальный шрифт для кириллицы
setfont cyr-sun16
# Разметка расчитанная на установку HDD если у вас он то измените на sdaX (вместо х номер), если его нет то не трогать
cfdisk /dev/nvme0n1
# Фарматируем для загрузчика
mkfs.fat -F 32 /dev/nvme0n1p1
# Подкачка для надёжности
mkswap /dev/nvme0n1p2
# Форматирование основнова раздела системы
mkfs.ext4 /dev/nvme0n1p3
# Подключаем
mount /dev/nvme0n1p3 /mnt
mkdir -p /mnt/boot/efi
mount /dev/nvme0n1p1 /mnt/boot/efi
swapon /dev/nvme0n1p2
# Базавая установка сиситемы
pacstrap /mnt base linux linux-firmware sof-firmware base-devel grub efibootmgr nano networkmanager
# Автоматическое монтирование после входа в систему
genfstab /mnt > /mnt/etc/fstab
# Копирования файла с установкой пакетов
cp install-pkg.sh /mnt/home/user
cp -r hyrp /mnt/home/user
cp -r fish /mnt/home/user
cp -r waybar /mnt/home/user
cp -r wofi /mnt/home/user
cp -r yay /mnt/home/user

# Выполняем chroot
arch-chroot /mnt /bin/bash <<EOF
ln -sf /usr/share/zoneinfo/Asia/Almaty /etc/localtime
hwclock --systohc

# Автоматическое раскомментирование строки в /etc/locale.gen
sed -i 's/^#\(ru_RU.UTF-8 UTF-8\)/\1/' /etc/locale.gen

# Генерация локалей
locale-gen

# Завершающие действия
echo "LANG=ru_RU.UTF-8" > /etc/locale.conf

echo "Arch" > /etc/hostname

# Установка пароля root
echo "root:1234" | chpasswd

# Создание пользователя и настройка sudo с тем же паролем
useradd -m -G wheel -s /bin/bash user
echo "user:1234" | chpasswd

sed -i 's/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers

systemctl enable NetworkManager
grub-install /dev/nvme0n1
grub-mkconfig -o /boot/grub/grub.cfg

EOF

umount -a
# Завершающие шаги
echo "Установка завершена! Перезагрузка системы."
reboot
