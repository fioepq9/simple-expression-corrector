#!/bin/bash
git reset --hard origin/main
git clean -f
git pull
git checkout main