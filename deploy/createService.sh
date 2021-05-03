#!/bin/bash
set -e
set -x

echo "[Unit] 
Description=GonGon Discord bot

[Service]
User=pi
Type=forking
WorkingDirectory=/home/pi/GonGon
ExecStart=/home/pi/GonGon/deploy/run-prod.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/gongon.service

systemctl daemon-reload
systemctl enable gongon