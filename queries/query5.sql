WITH sellers AS (
    SELECT DISTINCT(Users.User_ID), Users.Rating FROM Items LEFT OUTER JOIN Users on Items.User_ID = Users.User_ID
)
SELECT COUNT(*) FROM sellers WHERE sellers.Rating > 1000;