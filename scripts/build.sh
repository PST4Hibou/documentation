#!/usr/bin/env bash


rm -rf ./docs

./scripts/clone.py
./scripts/doc_gen.py

rm -rf ./tmp/*
