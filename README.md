# MyDisplays

Configuración visual de monitores para **Hyprland** con interfaz GTK4 / Libadwaita.
Arrastra tus monitores en un canvas, ajusta resolución, escala, rotación y mirror,
aplica la configuración con un clic y guarda perfiles.

Visual monitor layout configuration for **Hyprland** with a GTK4 / Libadwaita UI.
Drag your monitors on a canvas, adjust resolution, scale, rotation and mirroring,
apply the layout with one click and save profiles.

![hyprland](https://img.shields.io/badge/Hyprland-0.56-blue) ![gtk4](https://img.shields.io/badge/GTK4-4.22-green) ![license](https://img.shields.io/badge/license-GPLv3-orange) ![python](https://img.shields.io/badge/Python-3.14-blue)

---

## Características / Features

- **Canvas visual** arrastra los monitores como en wdisplays, con zoom y desplazamiento.
- **Anti-superposición**: los monitores nunca se superponen al arrastrarlos (funciona con cualquier número de monitores).
- **Resolución / refresh / escala / rotación / mirror** por monitor, con detección de modos reales vía `hyprctl`.
- **Perfiles**: guarda y restaura disposiciones completas con un clic.
- **Identify**: resalta cada monitor con su nombre durante unos segundos.
- **Auto-revert**: si la configuración aplicada deja la pantalla en negro, se revierte en 10 segundos.
- **i18n**: interfaz en español e inglés (gettext).
- **Easy Pointer** *(daemon opcional)*: salto de cursor entre monitores con gaps.

### Easy Pointer (daemon opcional)

Un daemon en systemd que salta el cursor al monitor vecino cuando llegas al borde
(con cooldown y detección de movimiento real). Se activa/desactiva desde la app.

---

## Requisitos / Requirements

- Linux con **Hyprland** (`hyprctl` disponible)
- Python 3.10+
- GTK 4.0+ con `python3-gi`
- Libadwaita (`python3-gi` + `libadwaita`) y Gtk4LayerShell
- `systemd` (opcional, solo para el daemon Easy Pointer)

### Arch Linux

```bash
sudo pacman -S python-gobject gtk4 libadwaita gtk4-layer-shell
```

---

## Instalación / Installation

```bash
git clone https://github.com/unobbb-bit/mydisplays.git
cd mydisplays
./install.sh
```

El instalador copia los binarios a `~/.local/bin/` y crea el servicio
`easy-pointer.service` en `~/.config/systemd/user/`.

Activa el daemon de cursor (opcional):

```bash
systemctl --user enable --now easy-pointer.service
```

Ejecuta la app:

```bash
mydisplays
```

---

## Estructura del proyecto / Project layout

```
mydisplays/          # app principal (GTK4)
mydisplays-warp      # daemon de salto de cursor
mydisplays_geom.py   # geometría pura anti-superposición (sin GTK, testeable)
install.sh           # instalador
tests/               # tests unitarios (TDD) de la geometría
share/locale/        # traducciones gettext
LICENSE              # GNU GPL v3
```

---

## Tests

La lógica de superposición vive en un módulo puro (`mydisplays_geom.py`) sin
dependencias de GTK, lo que permite probarla en CI:

```bash
cd tests && python3 -m unittest discover -s . -t ..
```

---

## Contribuir / Contributing

¿Te gusta la app y quieres sumarte? Todo aporte es bienvenido, sobre todo ayuda
técnica, porque el autor no es programador (ver Disclaimer).

- **Bugs e ideas**: abre un issue con la plantilla de
  [bug report](https://github.com/unobbb-bit/mydisplays/issues/new?template=bug_report.yml)
  o de [feature request](https://github.com/unobbb-bit/mydisplays/issues/new?template=feature_request.yml).
- **Tareas para empezar**: issues etiquetados
  [`good first issue`](https://github.com/unobbb-bit/mydisplays/labels/good%20first%20issue)
  y [`help wanted`](https://github.com/unobbb-bit/mydisplays/labels/help%20wanted).
- **Buscamos mantenedores**: si sabes Python/GTK4 y la idea te gusta, este
  proyecto necesita a alguien que lo mantenga a largo plazo. Escríbenos en
  [Discussions](https://github.com/unobbb-bit/mydisplays/discussions).

---

## Historia / Background

Este proyecto **no es un fork** de `wdisplays` / `displays`: está escrito desde
cero específicamente para Hyprland, usando `hyprctl` como fuente de verdad y un
único archivo Python con GTK4. Nació como una herramienta personal para este
entorno (Omarchy) y se comparte con la esperanza de que sea útil a otros.

---

## ⚠️ Descargo de responsabilidad / Disclaimer

**El autor no es programador.** MyDisplays fue creado con ayuda de herramientas
de IA (Omarchy + opencode) y con mucho ensayo y error. El código puede contener
errores, decisiones cuestionables y reinvenciones de la rueda.

- El proyecto se distribuye **SIN NINGUNA GARANTÍA** (ver LICENSE, sección 15).
- Úsalo bajo tu propio riesgo: verifica siempre que la configuración aplicada
  sea la que esperas (la app revierte automáticamente si la pantalla se apaga).
- Aportes, *issues* y correcciones son más que bienvenidos.

---

## Licencia / License

GPLv3 — ver [LICENSE](LICENSE).

Copyright © 2026 unobbb-bit

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.
