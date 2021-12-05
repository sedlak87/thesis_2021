SELECT * FROM RECIPE_INGREDIENTS_NF
;

SELECT count(DISTINCT IngredientId) FROM RECIPE_INGREDIENTS_NF;
-- 7993 total ingredients

-- ingredients that appear in less than 250 recipes
SELECT DISTINCT IngredientId FROM RECIPE_INGREDIENTS_NF
group by IngredientId
having COUNT(recipe_id) < 250;

-- create INGREDIENTS_NF table

-- remove Ingredients that appear less than 250 times
UPDATE Ingredients_NF
SET valid=0
WHERE ingredient_id IN (SELECT DISTINCT IngredientId
    FROM RECIPE_INGREDIENTS_NF
    GROUP BY IngredientId
    HAVING COUNT(recipe_id) < 250
);

SELECT RI.recipe_id FROM RECIPE_INGREDIENTS_NF RI
JOIN Ingredients_NF I on RI.IngredientID= I.ingredient_id
GROUP BY RI.recipe_id
HAVING GROUP_CONCAT(I.valid, ' ') LIKE '%0%';

UPDATE RECIPE_INGREDIENTS SET valid=0
WHERE id IN (
   SELECT RI.recipe_id FROM RECIPE_INGREDIENTS_NF RI
          JOIN Ingredients_NF I on RI.IngredientID= I.ingredient_id
 GROUP BY RI.recipe_id
   HAVING GROUP_CONCAT(I.valid, ' ') LIKE '%0%'
);



-- -- (most common - salt, butter, egg, onion, sugar, olive_oil, water, milk, pepper, baking_soda, black_pepper)
-- --               6270 , 840   ,2499, 5010 , 6906 , 5006     , 7655 , 4717, 5319  , 335        , 590
-- ignore most popular ingredients in recipes (does not set 1 for them vector)
UPDATE INGREDIENTS_NF SET valid = 0
WHERE ingredient_id IN (6270, 840, 2499, 5010, 6906, 5006, 7655, 4717, 5319, 335, 590);
-- 729 ingredients left, 11 ingredients are ignored in vector representation
SELECT count(*) FROM Ingredients_NF where valid=1;

-- consider recipes with at least 3 ingredients recipes
  SELECT recipe_id
    FROM RECIPE_INGREDIENTS_NF
GROUP BY recipe_id
  HAVING count(IngredientId) < 5
;
-- consider recipes with at least 5 ingredients recipes
UPDATE RECIPE_INGREDIENTS
SET valid=0
WHERE id IN (
    SELECT recipe_id
    FROM RECIPE_INGREDIENTS_NF
GROUP BY recipe_id
  HAVING count(IngredientId) < 5
);
-- 55,990 recipes left
SELECT count(*) FROM RECIPE_INGREDIENTS WHERE valid=1;
;

-- Before creating table with RecipeId, Ingredient bool vector we need
-- helper table to store vector indeces from 0 to |ingredients|
--  INSERT INTO Ingredients_VectorI(IngredientValue)
--  SELECT IngredientValue FROM Ingredients_NF WHERE Valid=1;
-- FIX ID's
--  UPDATE Ingredients_NF SET ID=ID-1 -- (we work with first index 0 in array)


SELECT RI.recipe_id, RI.IngredientID, I.valid FROM RECIPE_INGREDIENTS_NF RI
JOIN Ingredients_NF I on RI.IngredientID= I.ingredient_id
WHERE RI.recipe_id=393219
;

SELECT count(*) from Recipe_IngredientVector where valid=0;

UPDATE Recipe_IngredientVector SET Valid=0
WHERE RecipeID IN (
    SELECT id from RECIPE_INGREDIENTS WHERE valid=0
    );

SELECT recipe_id, count(IngredientID) as c FROM RECIPE_INGREDIENTS_NF
group by recipe_id
having c < 5;

select * from PP_RECIPES;

select id, ingredient_ids as ingr_id from RECIPE_INGREDIENTS;

select id from RECIPE_INGREDIENTS_NF
order by random()
LIMIT 10;


SELECT IngredientID FROM RECIPE_INGREDIENTS_NF
WHERE IngredientID IN (
    select IngredientID
    from RECIPE_INGREDIENTS_NF
    group by IngredientID
    having count(distinct recipe_id) > 10000
    order by count(distinct recipe_id) desc
)

select IngredientID
    from RECIPE_INGREDIENTS_NF
    group by IngredientID
    having count(distinct recipe_id) > 10000
    order by count(distinct recipe_id) desc;

select count(IngredientID) from RECIPE_INGREDIENTS_NF where IngredientID=6270

select * from Metric_Data order by metric_name, rank

SELECT * from INGREDIENTS_VECTOR_I