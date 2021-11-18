#!/bin/bash
curl -dH -X POST "$(terraform output -raw cd_webhook)"