# Makefile

# 変数の定義
CONFERENCE ?= acl
YEAR ?= 2023

# デフォルトターゲット
.PHONY: all
all: run

# Pythonスクリプトを実行するターゲット
.PHONY: run
run:
	python ./src/main.py $(CONFERENCE) $(YEAR)
