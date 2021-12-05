CREATE TABLE PP_RECIPES
(
	id INTEGER,
	i INTEGER,
	name_tokens TEXT,
	ingredient_tokens TEXT,
	steps_tokens TEXT,
	techniques TEXT,
	calorie_level INTEGER,
	ingredient_ids TEXT
);

create table RAW_RECIPES
(
	name TEXT,
	id INTEGER,
	minutes INTEGER,
	contributor_id INTEGER,
	submitted TEXT,
	tags TEXT,
	nutrition TEXT,
	n_steps INTEGER,
	steps TEXT,
	description TEXT,
	ingredients TEXT,
	n_ingredients INTEGER
);

CREATE TABLE RECIPE_INGREDIENTS
(
    id             uniqueidentifier
        constraint PK_ID
            primary key,
    ingredient_ids int IDENTITY(1, 1) not null,
    valid          INTEGER default 1 not null
);

CREATE INDEX IX_RECIPE_INGREDIENTS
    on RECIPE_INGREDIENTS (id);

CREATE TABLE RECIPE_INGREDIENTS_NF
(
	id INTEGER
		constraint PK_ID
			primary key autoincrement,
	recipe_id INTEGER not null,
	ingredient_id INTEGER not null
);

CREATE INDEX IX_RECIPE_ID
	      ON RECIPE_INGREDIENTS_NF (recipe_id);

CREATE TABLE INGREDIENTS_NF
(
	id INTEGER
		constraint PK_ID
			primary key autoincrement,
	ingredient_id INTEGER UNIQUE not null,
	valid INTEGER not null default 1
);
--UPDATE INGREDIENTS_NF SET ID=ID-1

CREATE TABLE RECIPE_INGREDIENT_VECTOR
(
	recipe_id INTEGER
		constraint PK_ID
			primary key autoincrement,
	ingredient_vector VARCHAR(10000) not null,
	valid INTEGER not null default 1
);
CREATE INDEX IX_RECIPE_ID ON RECIPE_INGREDIENT_VECTOR (recipe_id);

CREATE TABLE USER_RECIPES
(
    id INTEGER
        constraint PK_ID
            primary key autoincrement,
    user_id INTEGER not null,
    recipe_id INTEGER UNIQUE not null
);

CREATE TABLE METRIC_DATA
(
    metric_name TEXT    not null,
    recipe_id   INTEGER not null,
    rank        INTEGER not null,
    primary key (metric_name, recipe_id)
);

CREATE TABLE INGREDIENTS_VECTOR_I
(
	vector_i INTEGER
		constraint PK_ID
			primary key autoincrement,
	ingredient_id INTEGER UNIQUE not null,
	valid INTEGER not null default 1
);

CREATE UNIQUE INDEX index_recipes_id
	             ON RAW_RECIPES (id);

create table sqlite_master
(
	type text,
	name text,
	tbl_name text,
	rootpage int,
	sql text
);

create table sqlite_sequence
(
	name,
	seq
);