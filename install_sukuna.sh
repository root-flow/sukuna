#!/bin/bash
# SUKUNA v11.0 - Otomatik Kurulum + Alias
# Author: canmitm | Instagram: @canmitm

set -e

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}SUKUNA v11.0 - OTOMATİK KURULUM${NC}"
echo -e "${YELLOW}Author: canmitm | @canmitm${NC}\n"

# Root kontrol
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}[!] ROOT GEREKLİ! sudo bash $0${NC}"
   exit 1
fi

# Gerekli paketler
echo -e "${GREEN}[1] Gerekli araçlar kuruluyor...${NC}"
apt update -qq
apt install -y nmap sqlmap xsser commix nikto nuclei python3 python3-tk gcc nasm git curl -qq

# sukuna.py indir
echo -e "${GREEN}[2] sukuna.py indiriliyor...${NC}"
curl -sL https://raw.githubusercontent.com/canmitm/sukuna/main/sukuna.py -o /usr/bin/sukuna
chmod +x /usr/bin/sukuna

# Klasörler
mkdir -p /var/lib/sukuna/{reports,evidence}

# Alias ekle (.bashrc ve .zshrc)
echo -e "${GREEN}[3] Alias ekleniyor: 'sukuna' → python3 /usr/bin/sukuna${NC}"

# .bashrc
if ! grep -q "alias sukuna=" /root/.bashrc 2>/dev/null; then
    echo "alias sukuna='python3 /usr/bin/sukuna'" >> /root/.bashrc
    echo -e "    ${GREEN}→ /root/.bashrc${NC}"
fi

# .zshrc (eğer varsa)
if [ -f /root/.zshrc ]; then
    if ! grep -q "alias sukuna=" /root/.zshrc 2>/dev/null; then
        echo "alias sukuna='python3 /usr/bin/sukuna'" >> /root/.zshrc
        echo -e "    ${GREEN}→ /root/.zshrc${NC}"
    fi
fi

# Normal kullanıcılar için (isteğe bağlı)
for user_home in /home/*; do
    user=$(basename "$user_home")
    bashrc="$user_home/.bashrc"
    zshrc="$user_home/.zshrc"

    if [ -f "$bashrc" ] && ! grep -q "alias sukuna=" "$bashrc" 2>/dev/null; then
        echo "alias sukuna='python3 /usr/bin/sukuna'" >> "$bashrc"
        chown "$user:$user" "$bashrc"
        echo -e "    ${GREEN}→ $bashrc${NC}"
    fi

    if [ -f "$zshrc" ] && ! grep -q "alias sukuna=" "$zshrc" 2>/dev/null; then
        echo "alias sukuna='python3 /usr/bin/sukuna'" >> "$zshrc"
        chown "$user:$user" "$zshrc"
        echo -e "    ${GREEN}→ $zshrc${NC}"
    fi
done

echo -e "${CYAN}
KURULUM TAMAM!
${NC}"
echo -e "${YELLOW}ŞİMDİ YAZ →${NC} sukuna"
echo -e "${GREEN}GUI için →${NC} sukuna (2 seç)"
echo -e "${GREEN}GitHub →${NC} https://github.com/canmitm/sukuna"
