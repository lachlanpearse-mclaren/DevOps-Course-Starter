#!/bin/bash
echo "$(terraform output -raw cd_webhook)"
#curl -dH -X POST $(terraform output -raw cd_webhook)