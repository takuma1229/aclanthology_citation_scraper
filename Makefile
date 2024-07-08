# 変数の定義
CONFERENCE ?= acl
YEAR ?= 
START_YEAR ?= 
END_YEAR ?= 

# デフォルトターゲット
.PHONY: all
all: run

# Pythonスクリプトを実行するターゲット
.PHONY: run
run:
ifndef YEAR
	@echo "YEAR is not set. Use make run_all to run for a range of years."
else
	python ./src/main.py $(CONFERENCE) $(YEAR)
endif

# 指定された期間内の全ての年に対して実行するターゲット
.PHONY: run_all
run_all:
ifndef START_YEAR
	@echo "START_YEAR is not set."
	exit 1
endif
ifndef END_YEAR
	@echo "END_YEAR is not set."
	exit 1
endif
	@for year in $(shell seq $(START_YEAR) $(END_YEAR)); do \
		$(MAKE) run CONFERENCE=$(CONFERENCE) YEAR=$$year; \
	done
