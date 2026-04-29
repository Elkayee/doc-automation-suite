.PHONY: setup format lint build clean

setup:
	uv sync
	npm install
	uv run pre-commit install

format:
	uv run ruff check --fix .
	uv run ruff format .
	npm run format

lint:
	uv run ruff check .
	npm run lint

build:
	uv run python make.py

clean:
	rm -f Bao_Cao_Tieu_Luan_NMCNPM.docx
	rm -f Bao_Cao_Tieu_Luan_NMCNPM.md
	rm -rf diagram_cache/
	rm -rf extracted_media/
