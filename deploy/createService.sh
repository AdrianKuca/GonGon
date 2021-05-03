#!/bin/bash
set -e
set -x

echo "[Unit] 
Description=GonGon Discord bot

[Service]
Type=forking
ExecStart=/home/pi/GonGon/deploy/run-prod.sh
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/gongon.service

systemctl daemon-reload
systemctl enable gongon