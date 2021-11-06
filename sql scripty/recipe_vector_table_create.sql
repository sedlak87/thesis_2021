create table Recipe_IngredientVector
(
	RecipeID INTEGER
		constraint PK_ID
			primary key autoincrement,
	IngredientVector VARCHAR(10000) not null,
	Valid INTEGER not null default 1
);

CREATE INDEX RecipeID ON Recipe_IngredientVector (RecipeID);

;

SELECT * FROM Recipe_IngredientVector
