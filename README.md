# FoodBot-DiscordBot
Discord bot, ktorý každý deň zverejňuje denné menu z Eat&Meet, Družba Cantina a FiitFood. Menu sú poslané správou do kanálov, ktoré sú nakonfiguované v config súbore. Taktiež sa dá nakonfigurovať aj rola, ktorá sa pingne pri poslaní denného menu, ako aj farba správy
## Ukážka

## Features
* Automatické posielanie denného menu z 3 webov
* Konfigurácia kanálov, rolí a farby správ
* Možnosť spustiť manuálne refresh
* Plánované spúšťanie každý deň

## Konfigurácia
Súbor config.json obsahuje nastavenia pre jednotlivé servery, kde bot pôsobí. Kľúčom v JSON je ID serveru.
### Príklad
```
{
    "1382109119347167352": {
        "channel_id": 1391047537514778696,
        "role_id": 1397325138198007888,
        "embed_color": 15110684
    }
}
```
### Vysvetlenie
+ **Guild ID** - unikátne ID servera, bot podľa toho vie, kde má posielať správy, napr "1382109119347167352".
+ **"channel_id"** - ID textového kanála, do ktorého sa pošle denné menu.
+ **"role_id"** - ID role, ktorá bude pri správe mentionnutá (ping).
+ **"embed_color"** - farba embed správy v **hexadecimálnej RGB forme**, zapísana ako **integer**
> [!TIP]
> Pre pridanie ďalšieho servera staćí pridať novú položku s jeho Guild ID.
## Štruktúra
- **core/**
    - `commands.py`
    - `events.py`
