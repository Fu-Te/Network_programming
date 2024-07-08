#!/bin/bash

# ホストPCのIPアドレス、サブネット、ゲートウェイアドレスを取得
HOST_IP=$(ip route get 8.8.8.8 | head -1 | cut -d' ' -f8)
HOST_SUBNET_CIDR=$(ip addr show | grep inet | grep -v inet6 | grep -vE '127\.|172\.17\.|10\.|192\.168\.' | cut -d' ' -f6 | cut -d'/' -f1 | head -1)
HOST_GATEWAY=$(ip route | grep default | cut -d' ' -f3)

# 環境変数を設定
export HOST_IP
export HOST_SUBNET_CIDR
export HOST_GATEWAY

# Docker Composeファイルを実行
docker-compose up -d
