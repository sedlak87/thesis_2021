SELECT * FROM RECIPE_INGREDIENTS_NF;

-- Now add the clustered index
CREATE INDEX IX_RecipeID ON RECIPE_INGREDIENTS_NF (recipe_id);

SELECT * FROM Ingredients_NF
WHERE ingredient_id IN (SELECT ingredient_id FROM RECIPE_INGREDIENTS_NF where recipe_id=38);

SELECT * FROM RECIPE_INGREDIENTS_NF;

SELECT count(DISTINCT recipe_id) FROM RECIPE_INGREDIENTS_NF where valid=0;

SELECT * FROM PP_RECIPES WHERE id=488260;
-- total 7993
-- 1760 rare , less than 3 recipes
-- 6 very popular
-- Total ingredients = 6227
-- Total recipes 178263
SELECT count(distinct ingredient_id) FROM RECIPE_INGREDIENTS_NF where valid=1;

SELECT * FROM INGREDIENTS_VECTOR_I

--DROP TABLE RECIPE_INGREDIENTS_NF;

SELECT id, name, ingredients FROM RAW_RECIPES where n_ingredients < 5

SELECT id, ingredient_ids FROM PP_RECIPES