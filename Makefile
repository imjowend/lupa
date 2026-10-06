.PHONY: help progress

help: ## Muestra los targets disponibles
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

progress: ## Avance de las tareas según specs/ROADMAP.md
	python3 scripts/progress.py
