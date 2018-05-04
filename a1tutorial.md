## 1st Amendment
**Problem:** At the Court of Appeals for the Fourth Circuit, what cases are related to the first amendment?
**Solution:** Search opinions for the first amendment.

#### Version 1
Sends out a tweet when the program runs to a Twitter account.
* Create a gmail account for bot
  - firstamendmentcns@gmail.com
* Create a Twitter account using gmail account
  - @1st_amendment_4
* Get keys for Twitter account at apps.twitter.com
* Create GitHub repo with 4 files: sctutorial.md, sckey.json, readme.md, GitIgnore, & sccode.py
* Write the following code in pskey.json:
  - consumer key, consumer key secret, access token, & access token secret
* Write the following code in pscode.py:
  - Import Json & Tweepy
  - Call in authentication information from pskey.json
  - Store them so they can be passed into Twitter
  - Create keyword to tweet out
  - Tweet out keyword with authentication to test
```