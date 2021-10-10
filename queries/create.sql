DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
    User_ID CHAR(200) PRIMARY KEY,
    Rating INTEGER,
    Location CHAR(200),
    Country CHAR(200)
);

DROP TABLE IF EXISTS Items;
CREATE TABLE Items(
    Items_ID INTEGER PRIMARY KEY,
    Name CHAR(100),
    Num_Categories INTEGER,
    Categories CHAR(2000),
    Currently INTEGER,
    Buy_Price INTEGER,
    First_Bid INTEGER,
    Number_of_Bids INTEGER,
    Started CHAR(50),
    Ends CHAR(50),
    User_ID Char(50),
    Description CHAR(400),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
);
DROP TABLE IF EXISTS Bids;
CREATE TABLE Bids(
    Time CHAR(100),
    Amount CHAR(50),
    Bidder_ID CHAR(100),
    Item_ID INTEGER,
    FOREIGN KEY (Item_ID) REFERENCES Items(Item_ID),
    FOREIGN KEY (Bidder_ID) REFERENCES Users(User_ID)
);

DROP TABLE IF EXISTS Categories;
CREATE TABLE Categories(
    Name CHAR(100) PRIMARY KEY
)