create table Ingredients_NF
(
	ID INTEGER
		constraint PK_ID
			primary key autoincrement,
	IngredientValue INTEGER UNIQUE not null,
	Valid INTEGER not null default 1
);

CREATE TABLE Ingredients_VectorI
(
    Vector_I INTEGER
		constraint PK_ID
			primary key autoincrement,
	IngredientValue INTEGER UNIQUE not null
);

SELECT * FROM Ingredients_VectorI;

UPDATE Ingredients_VectorI SET Vector_I=Vector_I-1 -- (we work with first index 0 in array)

-- UPDATE Ingredients_NF SET ID=ID-1


