#!/usr/bin/env bash

set -Eeuo pipefail

AGENT_DIR=/opt/watcher-agent
SERVICE_PATH=/etc/systemd/system/watcher-agent.service
SERVICE_NAME=watcher-agent.service

function uninstall {
    printf '%b\n' "Uninstalling..."
    if [ -d "$AGENT_DIR" ]
    then
        rm -rf "$AGENT_DIR"
        printf '%b\n' "Agent deleted"
    fi
    if [ -f "$SERVICE_PATH" ]
    then
        systemctl stop "$SERVICE_NAME"
        rm "$SERVICE_PATH"
        systemctl daemon-reload
        printf '%b\n' "Systemd service deleted"
    fi
    printf '%b\n' "Uninstalled"
}

function exit_way {
    printf '%b\n' "INSTALLATION ERROR!"
    uninstall
}
trap exit_way SIGINT SIGTERM ERR


if [ ! $# -eq 0 ]
then
    if [ $1 = '--uninstall' ]
    then
        uninstall
        exit
    fi
fi

if [ -f "$AGENT_DIR"/INSTALLED ]
then
    printf '%b\n' "Watcher Agent installed yet!"
    printf '%b\n' "If you need to uninstall it, use --uninstall argument"
    exit
fi

mkdir "$AGENT_DIR"
touch "$AGENT_DIR"/out_log.log

cp watcher_agent.py "$AGENT_DIR"/
cp watcher_agent.json "$AGENT_DIR"/

chown -R root:root "$AGENT_DIR"
chmod -R 740 "$AGENT_DIR"
printf '%b\n' "Watcher Agent: agent copied to "$AGENT_DIR""

cd "$AGENT_DIR"
python3 -m venv watcher-pyenv
source watcher-pyenv/bin/activate
python3 -m pip install psutil
python3 -m pip install asyncio
printf '%b\n' "Watcher Agent: python requirenments installed"

cat > "$SERVICE_PATH" << EOF
[Unit]
Description=Watcher Agent Service

[Service]
WorkingDirectory=$AGENT_DIR
ExecStart=/usr/bin/python3 watcher_agent.py

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
printf '%b\n' "Watcher Agent: systemd service installed"

touch INSTALLED

printf '%b\n' "Watcher Agent: INSTALLATION DONE. To start monitoring you need:"
printf '%b\n' "1. edit configuration file: "$AGENT_DIR"/watcher_agent.json"
printf '%b\n' "2. run systemd service: systemctl start "$SERVICE_NAME""