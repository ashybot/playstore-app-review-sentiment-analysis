from google_play_scraper import Sort, reviews

result, continuation_token = reviews(
    'co.triller.droid',
    lang='en', # defaults to 'en'
    country='us', # defaults to 'us'
    sort=Sort.MOST_RELEVANT, # defaults to Sort.NEWEST
    count=1000, # defaults to 100
    filter_score_with=5 # defaults to None(means all score)
)

# If you pass "continuation_token" as an argument to the reviews function at this point,
# it will crawl the items after 3 review items.

result, _ = reviews(
    'co.triller.droid',
    continuation_token=continuation_token # defaults to None(load from the beginning)
)

print(result)