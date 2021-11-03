create table RECIPE_INGREDIENTS_NF
(
	ID INTEGER
		constraint PK_ID
			primary key autoincrement,
	RecipeID INTEGER not null,
	IngredientID INTEGER not null,
	Valid INTEGER not null default 1
);

-- Now add the clustered index
CREATE INDEX IX_RecipeID ON RECIPE_INGREDIENTS_NF (RecipeID);

SELECT count(DISTINCT RecipeID) FROM RECIPE_INGREDIENTS_NF

SELECT count(DISTINCT RecipeID) FROM RECIPE_INGREDIENTS_NF ;

SELECT * FROM PP_RECIPES WHERE id=488260;

SELECT * FROM RECIPE_INGREDIENTS_NF WHERE IngredientID=6028;

SELECT count(*) FROM RECIPE_INGREDIENTS_NF WHERE Valid=0;

SELECT * FROM RAW_RECIPES where ingredients like '%shredded three cheese%'

--DELETE FROM RECIPE_INGREDIENTS_NF;

