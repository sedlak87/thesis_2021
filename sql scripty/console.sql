create table RECIPE_INGREDIENTS_NF
(
	ID INTEGER
		constraint PK_ID
			primary key autoincrement,
	RecipeID INTEGER not null,
	IngredientID INTEGER not null
);

SELECT * FROM RECIPE_INGREDIENTS_NF;

-- Now add the clustered index
CREATE INDEX IX_RecipeID ON RECIPE_INGREDIENTS_NF (RecipeID);

SELECT * FROM Ingredients_NF
WHERE IngredientValue IN (SELECT IngredientID FROM RECIPE_INGREDIENTS_NF where RecipeID=38);

SELECT * FROM RECIPE_INGREDIENTS_NF;

SELECT count(DISTINCT RecipeID) FROM RECIPE_INGREDIENTS_NF where Valid=0;

SELECT * FROM PP_RECIPES WHERE id=488260;
-- total 7993
-- 1760 rare , less than 3 recipes
-- 6 very popular
-- Total ingredients = 6227
-- Total recipes 178263
SELECT count(distinct IngredientID) FROM RECIPE_INGREDIENTS_NF where valid=1;

SELECT * FROM RECIPE_INGREDIENTS;

--DROP TABLE RECIPE_INGREDIENTS_NF;

SELECT * FROM Recipe_IngredientVector


