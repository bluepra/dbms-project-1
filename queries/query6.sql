WITH both as (
    SELECT DISTINCT(Bids.Bidder_ID) FROM Bids
        INTERSECT
    SELECT DISTINCT(Items.User_ID) FROM Items
)
SELECT COUNT(*) from both;
