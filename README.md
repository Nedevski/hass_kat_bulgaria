# КАТ България - HACS интеграция за Home Assistant

English description is at the bottom!

![Last release](https://img.shields.io/github/release-date/nedevski/hacs_kat_bulgaria?style=flat-square)
![Code size](https://img.shields.io/github/languages/code-size/nedevski/hacs_kat_bulgaria?style=flat-square)

---

Тази интеграция позволява да се следи дали човек има нови глоби към КАТ България. Интеграцията взима информацията директно от официалния сайт на КАТ ([e-uslugi.mvr.bg](https://e-uslugi.mvr.bg/services/kat-obligations)) без да логва абсолютно нищо. Единственото място на което се пазят данните е локално, като конфигурация на интеграцията.

## Инсталиране

Тъй като това е неофициална интеграция е необходимо първо да се [инсталира HACS](https://hacs.xyz/docs/setup/download) - официалния туул за сваляне на неофициални интеграции и добавки към Home Assistant.

След инсталация, в основното меню ще се появи линк към HACS. В неговата страница има търсачка, която филтрира всички неофициални интеграции - там може да се потърси "KAT Bulgaria" и след отваряне на интеграцията да се свали чрез Download бутона.

**След сваляне е задължително да се рестартира Home Assistant!**

След рестарт се добавя като нормална интеграция: Настройки => Устройства и услуги => Добавяне на интеграция => KAT Bulgaria.

## Как работи

За всеки конфигуриран потребител, тази интеграция ще създаде единичен [бинарен сензор](/integrations/binary_sensor), който показва дали има чакаща глоба или не. Можете да добавяте колкото инстанции желаете - за всеки нов човек просто добавете нова интеграция. Записите се обновяват на всеки 30 минути.

За да настроите интеграцията, трябва да дадете име на човек, неговото ЕГН, както и номера на шофьорската му книжка.

![Config flow](https://raw.githubusercontent.com/Nedevski/hass_kat_bulgaria/main/docs/config-flow-en.jpg)

За всяка конфигурирана инстанция се създават няколко entities:

- Има ли глоби (binary_sensor)
- Има ли невръчени глоби (binary_sensor)
- Общ брой глоби (sensor, int)
- Брой невръчени глоби (sensor, int)
- Обща дължима сума (sensor, int) - взима предвид активните отстъпки

## Python библиотека

Тази интеграция използва моята Python библиотека - [py_kat_bulgaria](https://github.com/Nedevski/py_kat_bulgaria).

Библиотеката е изцяло независима от тази интеграция и може да се използва самостоятелно. Повече информация има в нейното `readme.md`.

---

---

## KAT Bulgaria - a HACS integration for Home Assistant

The KAT Bulgaria custom integration allows users to check if they have any new fines from the Bulgarian Traffic Police (KAT). The integration is a wrapper around the official government website ([e-uslugi.mvr.bg](https://e-uslugi.mvr.bg/services/kat-obligations)).

## Installation

Since this is an unofficial integration, you have to download the [HACS (Home Assistant Community Store)](https://hacs.xyz/docs/setup/download).

After installing it you will have a link to HASS on the left menu. There you can search for "KAT Bulgaria", open the integration and click Download.

**You have to restart Home Assistant in order to be able to see the integration!**

After restarting you add the integration as usual: Settings => Devices and services => Add integration => KAT Bulgaria.

## How it works

For each configured user this integration will create a single [binary_sensor](/integrations/binary_sensor) indicating if you have a fine or not. You can add as many entries as you need. Entries are updated once every 30 minutes.

In order to set up the integration, you need to provide a name, the person's EGN and the person's Driver License Number.

![Config flow](https://raw.githubusercontent.com/Nedevski/hass_kat_bulgaria/main/docs/config-flow-en.jpg)

For each configured instance, a couple of entities are created:

- Has Tickets (binary_sensor)
- Has Non-Served Tickets (binary_sensor)
- Count Total (sensor, int) - total count of existing fines
- Count Non-Served (sensor, int) - total count of non-served fines
- Total BGN Owed (sensor, int) - the total sum that needs to be paid, which takes into account the active discounts for early payment

## Standalone Python library

The integration uses my [py_kat_bulgaria](https://github.com/Nedevski/py_kat_bulgaria) library.

It's entirely separate from this integration and can be used on its own. Check out its description for more information.
