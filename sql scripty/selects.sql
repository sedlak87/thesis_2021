SELECT * FROM RECIPE_INGREDIENTS_NF where RecipeId=38
;

SELECT * FROM Ingredients_NF WHERE IngredientValue IN (648, 3355, 7501, 4253) order by ID
;

UPDATE RECIPE_INGREDIENTS_NF
SET Valid=0
where IngredientId IN (SELECT DISTINCT IngredientId FROM RECIPE_INGREDIENTS_NF
group by IngredientId
having COUNT(RecipeId) < 20
order by Count(RecipeId))
;

SELECT DISTINCT IngredientId FROM RECIPE_INGREDIENTS_NF
group by IngredientId
having COUNT(RecipeId) < 20
order by Count(RecipeId); -- 3868 invalidated

-- 7993 total
-- remove Ingredients that appear less than 20 times
-- remove recipes that contain at least 1 invalid ingredient
-- -- (most common - salt, butter, egg, onion, sugar, olive_oil, water, milk, pepper, baking_soda, black_pepper)
-- --               6270 , 840   ,2499, 5010 , 6906 , 5006     , 7655 , 4717, 5319  , 335        , 590
-- ignore most popular ingredients in recipes (does not set 1 for them vector)



SELECT COUNT(distinct IngredientId) FROM RECIPE_INGREDIENTS_NF where valid=1
;

SELECT count(distinct RecipeId) FROM RECIPE_INGREDIENTS_NF where IngredientId=5319
;

SELECT count(RecipeId) FROM RECIPE_INGREDIENTS_NF where Valid=0
; -- has at least one invalid ingredient

SELECT count(distinct RecipeId) FROM RECIPE_INGREDIENTS_NF where valid=1
; -- where RecipeId=95491


select * from RAW_RECIPES raw
JOIN PP_RECIPES pp ON raw.id=pp.id
--WHERE raw.ingredients like '%black pepper%'
where ingredient_ids like '%590%'