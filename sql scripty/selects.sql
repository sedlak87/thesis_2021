SELECT * FROM RECIPE_INGREDIENTS_NF
;

SELECT count(DISTINCT IngredientId) FROM RECIPE_INGREDIENTS_NF;
-- 7993 total ingredients

-- ingredients that appear in less than 250 recipes
SELECT DISTINCT IngredientId FROM RECIPE_INGREDIENTS_NF
group by IngredientId
having COUNT(RecipeId) < 250;

-- create INGREDIENTS_NF table

-- remove Ingredients that appear less than 250 times
UPDATE Ingredients_NF
SET Valid=0
WHERE IngredientValue IN (SELECT DISTINCT IngredientId
    FROM RECIPE_INGREDIENTS_NF
    GROUP BY IngredientId
    HAVING COUNT(RecipeId) < 250
);

SELECT RI.RecipeID FROM RECIPE_INGREDIENTS_NF RI
JOIN Ingredients_NF I on RI.IngredientID= I.IngredientValue
GROUP BY RI.RecipeId
HAVING GROUP_CONCAT(I.Valid, ' ') LIKE '%0%';

UPDATE RECIPE_INGREDIENTS SET Valid=0
WHERE ID IN (
   SELECT RI.RecipeID FROM RECIPE_INGREDIENTS_NF RI
          JOIN Ingredients_NF I on RI.IngredientID= I.IngredientValue
 GROUP BY RI.RecipeId
   HAVING GROUP_CONCAT(I.Valid, ' ') LIKE '%0%'
);



-- -- (most common - salt, butter, egg, onion, sugar, olive_oil, water, milk, pepper, baking_soda, black_pepper)
-- --               6270 , 840   ,2499, 5010 , 6906 , 5006     , 7655 , 4717, 5319  , 335        , 590
-- ignore most popular ingredients in recipes (does not set 1 for them vector)
UPDATE INGREDIENTS_NF SET Valid = 0
WHERE IngredientValue IN (6270, 840, 2499, 5010, 6906, 5006, 7655, 4717, 5319, 335, 590);
-- 729 ingredients left, 11 ingredients are ignored in vector representation
SELECT count(*) FROM Ingredients_NF where valid=1;

-- consider recipes with at least 3 ingredients recipes
  SELECT RecipeId
    FROM RECIPE_INGREDIENTS_NF
GROUP BY RecipeId
  HAVING count(IngredientId) < 5
;
-- consider recipes with at least 5 ingredients recipes
UPDATE RECIPE_INGREDIENTS
SET Valid=0
WHERE ID IN (
    SELECT RecipeId
    FROM RECIPE_INGREDIENTS_NF
GROUP BY RecipeId
  HAVING count(IngredientId) < 5
);
-- 55,990 recipes left
SELECT count(*) FROM RECIPE_INGREDIENTS WHERE Valid=1;
;

-- Before creating table with RecipeId, Ingredient bool vector we need
-- helper table to store vector indeces from 0 to |ingredients|
--  INSERT INTO Ingredients_VectorI(IngredientValue)
--  SELECT IngredientValue FROM Ingredients_NF WHERE Valid=1;
-- FIX ID's
--  UPDATE Ingredients_NF SET ID=ID-1 -- (we work with first index 0 in array)


SELECT RI.RecipeID, RI.IngredientID, I.Valid FROM RECIPE_INGREDIENTS_NF RI
JOIN Ingredients_NF I on RI.IngredientID= I.IngredientValue
WHERE RI.RecipeID=393219
;

SELECT count(*) from Recipe_IngredientVector where valid=0;

UPDATE Recipe_IngredientVector SET Valid=0
WHERE RecipeID IN (
    SELECT ID from RECIPE_INGREDIENTS WHERE Valid=0
    );

SELECT * FROM Ingredients_NF where valid=1
