import subprocess

apps = dict()
apps["com.facebook.katana"] = "facebook_reviews.json"
apps["com.instagram.android"] = "instagram_reviews.json"
apps["com.zhiliaoapp.musically"] = "tiktok_reviews.json"
apps["com.linkedin.android"] = "linkedin_reviews.json"
apps["com.twitter.android"] = "twitter_reviews.json"
apps["org.joinmastodon.android"] = "mastodon_reviews.json"
apps["co.vero.app"] = "vero_reviews.json"
apps["org.thoughtcrime.securesms"] = "signal_reviews.json"
apps["com.mewe"] = "mewe_reviews.json"
apps["co.triller.droid"] = "triller_reviews.json"

app_names = ["facebook", "instagram", "tiktok", "linkedin", "twitter", "mastodon", "vero"
, "signal", "mewe", "triller"]
json_str = "_reviews.json"
txt_str = "sentiment_score_%s.txt"
html_str = "output_%s.html"


for appid, filename in apps.items():
    file = open(filename, "w")
    subprocess.run(["python3", "get_reviews.py", appid], stdout=file)


for name in app_names:
    json_name = name + json_str
    txt_name = txt_str % name
    html_name = html_str % name
    subprocess.run(["python3", "sentiment_analysis.py", json_name, txt_name, html_name])