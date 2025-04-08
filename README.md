# КАТ България - HACS интеграция за Home Assistant

For English description scroll to the bottom!

![Last release](https://img.shields.io/github/release-date/nedevski/hacs_kat_bulgaria?style=flat-square)
![Code size](https://img.shields.io/github/languages/code-size/nedevski/hacs_kat_bulgaria?style=flat-square)

---

Тази интеграция позволява да се следи дали човек има нови глоби към КАТ България. Интеграцията взима информацията директно от официалния сайт на КАТ ([e-uslugi.mvr.bg](https://e-uslugi.mvr.bg/services/kat-obligations)) без да логва абсолютно нищо. Единственото място на което се пазят данните е локално, като конфигурация на интеграцията.

---

Ако харесвате работата ми, почерпете ме с 1 бира в Ko-Fi:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/nedevski/tip)

## Инсталация

Тъй като това е неофициална интеграция е необходимо първо да се [инсталира HACS](https://hacs.xyz/docs/setup/download) - официалния туул за сваляне на неофициални интеграции към Home Assistant.

След инсталация, в основното меню ще се появи линк към HACS. В неговата страница има търсачка, която филтрира всички неофициални интеграции - там може да се потърси "KAT Bulgaria" и след отваряне на интеграцията да се свали чрез Download бутона.

**След сваляне е задължително да се рестартира Home Assistant!**

След рестарт се добавя като нормална интеграция: Настройки => Устройства и услуги => Добавяне на интеграция => KAT Bulgaria.

## Как работи

За да настроите интеграцията, трябва да дадете име на човек, неговото ЕГН, както и номера на шофьорската му книжка.

![Config flow](https://raw.githubusercontent.com/Nedevski/hass_kat_bulgaria/main/docs/config-flow-bg.jpg)
![Config flow](https://raw.githubusercontent.com/Nedevski/hass_kat_bulgaria/main/docs/sensors-bg.jpg)

За всеки конфигуриран човек се създават няколко entities, които се обновяват на всеки 1 час.

- Брой глоби ([сензор, int](https://www.home-assistant.io/integrations/binary_sensor/))
- Брой невръчени глоби ([сензор, int](https://www.home-assistant.io/integrations/binary_sensor/))
- Налични глоби? ([бинарен сензор](https://www.home-assistant.io/integrations/binary_sensor/))
- Невръчени глоби? ([бинарен сензор](https://www.home-assistant.io/integrations/binary_sensor/))
- Обща дължима сума ([сензор, int](https://www.home-assistant.io/integrations/binary_sensor/)) - взима предвид активните отстъпки

## Превод на Български език

За да работят преводите правилно, трябва и езика на системата, и езика на потребителя да са зададени на Български.

## Python библиотека

Тази интеграция използва моята Python библиотека - [py_kat_bulgaria](https://github.com/Nedevski/py_kat_bulgaria).

Библиотеката е изцяло независима от тази интеграция и може да се използва самостоятелно. Повече информация има в нейното `readme.md`.

---

---

## KAT Bulgaria - a HACS integration for Home Assistant

The KAT Bulgaria custom integration allows users to check if they have any new fines from the Bulgarian Traffic Police (KAT). The integration is a wrapper around the official government website ([e-uslugi.mvr.bg](https://e-uslugi.mvr.bg/services/kat-obligations)).

---

If you like my work - consider supporting me:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/nedevski/tip)

## Installation

Since this is an unofficial integration, you have to download the [HACS (Home Assistant Community Store)](https://hacs.xyz/docs/setup/download).

After installing it you will have a link to HASS on the left menu. There you can search for "KAT Bulgaria", open the integration and click Download.

**You have to restart Home Assistant in order to be able to see the integration!**

After restarting you add the integration as usual: Settings => Devices and services => Add integration => KAT Bulgaria.

## How it works

In order to set up the integration, you need to provide a name, the person's EGN and the person's Driver License Number.

![Config flow](https://raw.githubusercontent.com/Nedevski/hass_kat_bulgaria/main/docs/config-flow-en.jpg)
![Config flow](https://raw.githubusercontent.com/Nedevski/hass_kat_bulgaria/main/docs/sensors-en.jpg)

For each configured instance, a couple of entities are created and updated every 1 hour:

- Count Non-Served ([sensor, int](https://www.home-assistant.io/integrations/binary_sensor/)) - total count of non-served fines
- Count Total ([sensor, int](https://www.home-assistant.io/integrations/binary_sensor/)) - total count of existing fines
- Has Non-Served Tickets ([binary_sensor](https://www.home-assistant.io/integrations/binary_sensor/))
- Has Tickets ([binary_sensor](https://www.home-assistant.io/integrations/binary_sensor/))
- Total BGN Owed ([sensor, int](https://www.home-assistant.io/integrations/binary_sensor/)) - the total sum that needs to be paid, which takes into account the active discounts for early payment

## Standalone Python library

The integration uses my [py_kat_bulgaria](https://github.com/Nedevski/py_kat_bulgaria) library.

It's entirely separate from this integration and can be used on its own. Check out its description for more information.
