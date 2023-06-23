# KAT Bulgaria - HACS Integration

The KAT Bulgaria custom integration allows users to check if they have any new fines from the Bulgarian Traffic Police (KAT).
The integration is a wrapper around the official government website.
([e-uslugi.mvr.bg](https://e-uslugi.mvr.bg/services/kat-obligations)).

For each configured user this integration will create a single [binary_sensor](/integrations/binary_sensor) indicating if you have a fine or not. You can add as many entries as you need. Entries are updated once every 20 minutes.

In order to set it up, you need to provide a name, the person's EGN and the person's Driver License Number.

For each integration instance a single entity is created, named `globi_{name}`.

It might not show up under the integration itself, search for it in the entities list.
