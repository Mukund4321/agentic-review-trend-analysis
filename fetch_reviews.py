from google_play_scraper import reviews, Sort
import pandas as pd

result, _ = reviews(
    'in.swiggy.android',
    lang='en',
    country='in',
    sort=Sort.NEWEST,
    count=120
)

df = pd.DataFrame(result)
df['date'] = pd.to_datetime(df['at']).dt.date

df[['content', 'date']].to_csv("reviews.csv", index=False)
print("Saved reviews.csv")
