#!/bin/bash
set -euv

cd $CI_PROJECT_DIR/deploy

if [ ! -e "rancher-compose" ]; then
    wget "https://github.com/rancher/rancher-compose/releases/download/v0.8.4-rc3/rancher-compose-linux-amd64-v0.8.4-rc3.tar.gz"
    tar -xzf "rancher-compose-linux-amd64-v0.8.4-rc3.tar.gz"
    cp rancher-compose-v0.8.4-rc3/rancher-compose .
fi

./rancher-compose-v0.8.4-rc3/rancher-compose \
    --project-name "$RANCHER_STACK_NAME" \
    --file ./docker-compose.yml \
    --rancher-file ./rancher-compose.yml \
    --env-file ./env \
    --url https://rancher.iilab.org \
    --access-key "$RANCHER_ACCESS" \
    --secret-key "$RANCHER_SECRET" \
    up -d --pull --upgrade --force-upgrade --confirm-upgrade
