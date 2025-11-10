# Database
.PHONY: migration
migration:
	@poetry run alembic revision \
	  --autogenerate \
	  --rev-id $(shell poetry run python migrations/_get_next_revision_id.py) \
	  --message $(message)

# Migrate
.PHONY: migrate
migrate:
	@poetry run alembic upgrade head

.PHONY: stamp
stamp:
	@poetry run alembic stamp head