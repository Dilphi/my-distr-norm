# 🌀 Arch Linux Auto Installer

Полностью автоматизированный bash-скрипт установки Arch Linux с выбором окружения: **KDE Plasma** или **Hyprland**, полной пользовательской настройкой, темами, шрифтами, SDDM и PipeWire.

## 📦 Возможности

- ✅ Автоматическая разметка диска через `cfdisk`
- ✅ Установка базовой системы (`base`, `linux`, `networkmanager` и т.д.)
- ✅ Выбор DE: **KDE Plasma** или **Hyprland**
- ✅ Автоматическая установка `yay` и AUR-пакетов
- ✅ Поддержка **PipeWire** и его socket-сервисов
- ✅ Темизация:
  - SDDM: `astronaut theme`
  - GTK: `Graphite-Dark`
- ✅ Автоматическая настройка shell `fish`
- ✅ Службы: `NetworkManager`, `sddm`, `pipewire`, `dbus`, `lingering`
- ✅ Локализация: `ru_RU.UTF-8`
- ✅ Настройка часового пояса (например, `Asia/Almaty`, `Asia/Tomsk`)

## 🛠 Структура


├── install.sh                 # Главный установочный скрипт
├── hypr/                     # Конфигурации Hyprland
├── fish/                     # Конфигурации fish
├── waybar/                   # Конфигурации панели
├── wofi/                     # Конфигурации меню
├── yay/                      # Сборка yay из AUR
├── customize.service         # systemd user service
├── sddm-astronaut-theme/     # Тема входа
├── Graphite-gtk-theme/       # GTK тема оформления

🚀 Установка

    ⚠️ Внимание: Удаляются все данные на выбранном диске!

    Запустите install.sh от имени root:

    chmod +x install.sh && sudo ./install.sh

    Следуйте шагам:

        Выбор диска (например: sda, nvme0n1)

        Ввод имени пользователя и паролей

        Указание часового пояса (Almaty или Tomsk)

        Выбор окружения: 1 — KDE, 2 — Hyprland

    Дождитесь завершения и перезагрузки системы.

📷 Скриншоты
Hyprland	KDE Plasma

🧠 Требования

    UEFI BIOS

    Подключение к интернету

    Минимум 10 ГБ свободного места

    Желательно использовать Arch ISO или кастомный live-образ с этим скриптом

🔒 Безопасность

Все переменные (имя пользователя, пароли, часовой пояс) временно сохраняются в /mnt/root/setup и удаляются в конце установки.
📜 Лицензия

Этот проект распространяется под MIT License. Используйте на свой страх и риск.


Если хотите сделать что-то своё или вовсе изменить то:
    клонируйте репозитории
    git clone https://github.com/Dilphi/my-distr-norm

    установитье archiso
    sudo pacman -S archiso

    откройте каталог
    cd my-distr-norm

    чтобы собрать iso образ вспользуйтесь командой
    sudo mkarchiso -v .
