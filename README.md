# FoodBot-DiscordBot
Tento Discord bot automaticky zverejňuje denné menu z reštaurácií **Eat&Meet**, **Družba Cantina** a **FiitFood** každý deň. Menu sú odosielané ako správy do kanálov, ktoré si nakonfigurujete v config súbore.\
Bot tiež umožňuje nastaviť rolu, ktorá bude pinguje pri zverejnení denného menu, ako aj upravovať farbu správy pre lepšiu prispôsobiteľnosť.
## 🚀 Funkcie
* 📌 Automatické posielanie denného menu z 3 webov
* ⚙️ Konfigurácia kanálov, rolí a farby správ
* 🔄 Možnosť spustiť manuálne refresh
* ⏰ Plánované spúšťanie každý deň
## ⚙️ Setup
### 1. Vytvorenie Discord aplikácie
Aby bot fungoval, je potrebné najprv vytvoriť aplikáciu a bota na [Discord Developer Portal](https://discord.com/developers/applications):
1. Prihlás sa na [discord.dev](https://discord.com/developers/applications)
2. Klikni **New Application** → pomenuj svoju aplikáciu
3. V sekcii **Bot** vytvor nového bota
4. Skopíruj si **Bot Token**, ten sa vloží do svojho projektu ako environment premennú
5. Vygeneruj **OAuth2 Invite Link** s oprávneniami:
    * `Send Messages`
    * `Manage Messages`
    * `Mention Everyone`
    * prípadne `Administrator` pre testovanie
### 2. Lokálne spustenie
1. Naklonuj repozitár:
```
git clone https://github.com/tvoj-username/FoodBot-DiscordBot.git
cd FoodBot-DiscordBot
```
2. Nainštaluj závislosti:
```
pip install -r requirements.txt
```
3. Vytvor si súbor `config.json` podľa [Konfigurácie](#-konfigurácia)
4. Nastav si env premennú s tokenom (Linux/macOS):
```
export TOKEN=discord_token
```
alebo vo Windows PowerShell:
```
setx TOKEN "discord_token"
```
5. Spusti bota:
```
python main.py
```
### 3. Hosting (odporúčané)
Bot musí byť neustále online, preto sa odporúča nasadiť ho na hosting.
**Docker build a run**
1. Urob image:
```
docker build -t foodbot-image .
```
2. Spusti kontajner s env premennou:
```
docker run -d --name foodbot -e TOKEN=discord_token foodbot-image
```
## 🔧 Konfigurácia
Súbor config.json obsahuje nastavenia pre jednotlivé servery, kde bot pôsobí. Kľúčom v JSON je ID serveru.
### Príklad
```
{
    "1382109119347167350": {
        "channel_id": 1391047537514778690,
        "role_id": 1397325138198007880,
        "embed_color": 15110684
    }
}
```
### 🔑 Vysvetlenie parametrov
+ **Guild ID** - unikátne ID servera, bot podľa toho vie, kde má posielať správy, napr "1382109119347167352".
+ **"channel_id"** - ID textového kanála, do ktorého sa pošle denné menu.
+ **"role_id"** - ID role, ktorá bude pri správe mentionnutá (ping).
+ **"embed_color"** - farba embed správy v **hexadecimálnej RGB forme**, zapísana ako **integer**
> [!TIP]
> Pre pridanie ďalšieho servera staćí pridať novú položku s jeho Guild ID.
## 📂 Štruktúra projektu
### FoodBot-DiscordBot/
- **core/**
    - **commands/**
      - `commands.py`
      - `daily.py`
      - `embeds.py`
    - `events.py`
- **scrapers/**
    - `druzba.py` - Družba Cantina scraper
    - `enm.py` - Eat&Meet scraper
    - `fiitfood.py` - FiitFood scraper
- **utils/**
    - `access_control` - kontrola prístupu
    - `config_handler.py` - načítanie configu
    - `emoji_map.py` - mapovanie emoji ku kategóriam jedál
    - `exceptions.py` - custom výnimky
- `config.json` - konfigurácia
- `Dockerfile` - Docker build súbor
- `main.py` - hlavný entrypoint pre spustenie bota
- `README.md` - dokumentácia projektu
- `requirements.txt` - zoznam Python závislostí
## 💎 Kredity
* Autori: @jfridrich1, @ElGansoConLaRinonera, @trubkazNY
* Projekt vytvorený ako open-source Discord bot pre zverejňovanie denných menu z Eat&Meet, Družba Cantina a FiitFood.
