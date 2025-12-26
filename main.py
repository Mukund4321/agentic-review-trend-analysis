import pandas as pd
import openai
import json
import re



df = pd.read_csv("reviews.csv")
df["date"] = pd.to_datetime(df["date"])

daily_groups = df.groupby(df["date"].dt.date)

final_records = []

def extract_json_fallback(text):
    """
    Extracts JSON array from text using regex fallback
    """
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return []

for date, group in daily_groups:
    reviews_text = "\n".join(group["content"].tolist()[:20])

    messages = [
        {
            "role": "system",
            "content": "You are a strict JSON API. Respond ONLY with valid JSON."
        },
        {
            "role": "user",
            "content": f"""
Analyze the following app reviews.

Return a JSON array ONLY.
Each element must have:
- topic (string)
- count (integer)

Example:
[
  {{"topic":"Delivery issue","count":3}},
  {{"topic":"Food quality issue","count":2}}
]

Reviews:
{reviews_text}
"""
        }
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0
        )

        text = response.choices[0].message.content.strip()

        try:
            data = json.loads(text)
        except:
            data = extract_json_fallback(text)

        for item in data:
            final_records.append({
                "date": date,
                "topic": item["topic"],
                "count": item["count"]
            })

    except Exception as e:
        print(f"Skipped date {date}")

# 🚨 FINAL SAFETY CHECK
if not final_records:
    raise Exception("Still no data generated. Reduce review count to 10 and retry.")

result_df = pd.DataFrame(final_records)

pivot = result_df.pivot_table(
    index="topic",
    columns="date",
    values="count",
    aggfunc="sum",
    fill_value=0
)

pivot.to_excel("output_trend_report_final.xlsx", sheet_name="Trend Report")

print("Trend report saved successfully")



