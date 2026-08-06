#!/usr/bin/env bash
#
# MyDisplays — instalador
# Copyright (C) 2026 unobbb-bit <unobbb@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
set -euo pipefail

SCRIPTS_DIR="${BASH_SOURCE[0]%/*}"
: "${DEST_DIR:="$HOME/.local/bin"}"
: "${SERVICE_DIR:="$HOME/.config/systemd/user"}"

MISSING=()

if ! command -v python3 &>/dev/null; then
    MISSING+=("python3")
fi

if ! python3 -c "import gi; gi.require_version('Gtk', '4.0'); gi.require_version('Adw', '1'); from gi.repository import Gtk, Adw" 2>/dev/null; then
    MISSING+=("GTK4 + Adwaita (python3-gi + libadwaita)")
fi

if ! command -v hyprctl &>/dev/null; then
    MISSING+=("Hyprland (hyprctl)")
fi

if ! command -v systemctl &>/dev/null; then
    MISSING+=("systemd")
fi

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "Faltan dependencias:"
    for dep in "${MISSING[@]}"; do
        echo "  - $dep"
    done
    echo "Instálalas e intenta de nuevo."
    exit 1
fi

mkdir -p "$DEST_DIR/share/locale/es/LC_MESSAGES"
mkdir -p "$SERVICE_DIR"

cp "$SCRIPTS_DIR/mydisplays" "$DEST_DIR/mydisplays"
chmod +x "$DEST_DIR/mydisplays"
echo "Copiado: $DEST_DIR/mydisplays"

cp "$SCRIPTS_DIR/mydisplays_geom.py" "$DEST_DIR/mydisplays_geom.py"
chmod +x "$DEST_DIR/mydisplays_geom.py"
echo "Copiado: $DEST_DIR/mydisplays_geom.py"

cp "$SCRIPTS_DIR/mydisplays-warp" "$DEST_DIR/mydisplays-warp"
chmod +x "$DEST_DIR/mydisplays-warp"
echo "Copiado: $DEST_DIR/mydisplays-warp"

cp -r "$SCRIPTS_DIR/share/locale"/* "$DEST_DIR/share/locale/"
echo "Copiados: archivos de idioma"

cat > "$SERVICE_DIR/easy-pointer.service" << 'EOF'
[Unit]
Description=Easy Pointer - salto de cursor entre monitores Hyprland

[Service]
ExecStart=%h/.local/bin/mydisplays-warp
Restart=on-failure
RestartSec=2

[Install]
WantedBy=default.target
EOF

echo "Creado: $SERVICE_DIR/easy-pointer.service"

systemctl --user daemon-reload 2>/dev/null || true

echo ""
echo "Instalación completada."
echo ""
echo "Para iniciar Easy Pointer ahora:"
echo "  systemctl --user enable --now easy-pointer.service"
echo ""
echo "Para ejecutar MyDisplays:"
echo "  mydisplays"
