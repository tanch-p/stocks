# Configuration
DB_NAME = stocktracker
DB_USER = $(USER)   # macOS default Postgres user is your system username
SQL_DIR = sql

# Create database (only needed once)
createdb:
	createdb $(DB_NAME) || true

# Drop database (careful!)
dropdb:
	dropdb $(DB_NAME) || true

# Reset schema + seed data
reset: createdb
	psql -d $(DB_NAME) -f $(SQL_DIR)/reset.sql

# Run example queries
queries:
	psql -d $(DB_NAME) -f $(SQL_DIR)/queries.sql

# Open interactive psql shell
psql:
	psql -d $(DB_NAME)
