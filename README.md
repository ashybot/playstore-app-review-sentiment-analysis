# playstore-app-review-sentiment-analysis

1. Edit the `get_reviews.py` file so that you use the ID of the app you need to collect reviews for.
2. Run something like: `python3 get_reviews.py > appname_reviews.json` to get 1000 reviews for your app in JSON format.
3. Update the `sentiment_analysis.py` file to open a file of name `appname_reviews.json` in line 20 and to open a file named `sentiment_score_appname.txt` in line 104.
4. Run `python3 sentiment_analysis.py` to perform the analysis. A file called `output.html` will be produced which shows various characteristics about the data, as well as the `sentiment_score_appname.txt` file which contains all of the actual sentiment score data.
