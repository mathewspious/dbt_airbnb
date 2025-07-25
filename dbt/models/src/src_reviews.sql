WITH raw_reviews AS (
    SELECT
        *
    FROM
        AIRBNB.RAW.AIRBNB_REVIEWS
)
SELECT
    listing_id,
    date AS review_date,
    reviewer_name,
    comments AS review_text,
    sentiment AS review_sentiment
FROM
    raw_reviews