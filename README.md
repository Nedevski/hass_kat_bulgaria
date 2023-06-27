# КАТ България - HACS интеграция за Home Assistant

English description is at the bottom!

![Last release](https://img.shields.io/github/release-date/nedevski/hacs_kat_bulgaria?style=flat-square)
![Code size](https://img.shields.io/github/languages/code-size/nedevski/hacs_kat_bulgaria?style=flat-square)

___

Тази интеграция позволява да се следи дали човек има нови глоби към КАТ България. Интеграцията взима информацията директно от официалния сайт на КАТ ([e-uslugi.mvr.bg](https://e-uslugi.mvr.bg/services/kat-obligations)) без да логва абсолютно нищо. Единственото място на което се пазят данните е локално, като конфигурация на интеграцията.

## Как работи

За всеки конфигуриран потребител, тази интеграция ще създаде единичен [бинарен сензор](/integrations/binary_sensor), който показва дали има чакаща глоба или не. Можете да добавяте колкото инстанции желаете - за всеки нов човек просто добавете нова интеграция. Записите се обновяват на всеки 20 минути.

За да настроите интеграцията, трябва да дадете име на човек, неговото ЕГН, както и номера на шофьорската му книжка.

За всяка конфигурирана инстанция се създава единично entity във формат `globi_{име на човека}`.

За момента генерираното entity не излиза към прилежащата му инстанция на интеграцията, за да го намерите трябва да влезете в списъка с ентитита и да го намерите там.

![Config flow](https://raw.githubusercontent.com/Nedevski/hass_kat_bulgaria/main/docs/config-flow-en.jpg)

## Python библиотека

Тази интеграция използва моята Python библиотека - [py_kat_bulgaria](https://github.com/Nedevski/py_kat_bulgaria).

Библиотеката е изцяло независима от тази интеграция и може да се използва самостоятелно. Повече информация има в нейното `readme.md`.

___
___

## KAT Bulgaria - a HACS integration for Home Assistant

The KAT Bulgaria custom integration allows users to check if they have any new fines from the Bulgarian Traffic Police (KAT). The integration is a wrapper around the official government website ([e-uslugi.mvr.bg](https://e-uslugi.mvr.bg/services/kat-obligations)).

## How it works

For each configured user this integration will create a single [binary_sensor](/integrations/binary_sensor) indicating if you have a fine or not. You can add as many entries as you need. Entries are updated once every 20 minutes.

In order to set up the integration, you need to provide a name, the person's EGN and the person's Driver License Number.

For every configured instance, a single entity is created in the format of `globi_{name}`.

Please note that the integration will not show any entities that belong to its instance, you need to go in the entity list screen in order to find your entity.

![Config flow](https://raw.githubusercontent.com/Nedevski/hass_kat_bulgaria/main/docs/config-flow-en.jpg)

## Standalone Python library

The integration uses my [py_kat_bulgaria](https://github.com/Nedevski/py_kat_bulgaria) library.

It's entirely separate from this integration and can be used on its own. Check out its description for more information.
