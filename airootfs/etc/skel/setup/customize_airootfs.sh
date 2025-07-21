#!/bin/bash

# Создаём пользователя liveuser
useradd -m -G wheel -s /bin/bash liveuser
passwd -d liveuser  # убираем пароль

# sudo без пароля
echo "liveuser ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/liveuser
chmod 0440 /etc/sudoers.d/liveuser
