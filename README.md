# Olivia DeJonge

Olivia DeJonge is a program written in Python with functionality of doing live stream of tweets based on particular filters.

# Dependencies
- **Twitter for Developer Account**
	Twitter for Developer account is required to get the **Consumer Key**, **Consumer Secret**, **Access Token**, & **Access Token Secret** which are used to access the Twitter APIs.
	You can request your Twitter for Developer account here: [https://developer.twitter.com/](https://developer.twitter.com/)

- **Credentials File**
	Create a python file named **credentials.py** on the same directory of cloned repository. Write those following codes on the file:
	```python
	CONSUMER_KEY = '[Your Twitter Consumer Key]' # without bracket
	CONSUMER_SECRET = '[Your Twitter Consumer Secret]' # without bracket
	ACCESS_TOKEN = '[Your Twitter Access Token]' # without bracket
	ACCESS_TOKEN_SECRET = '[Your Twitter Access Token Secret]' # without bracket
	```
	
	Replace the inside '[]' contents with your Twitter for Developer account credentials.
- **Python Packages**
Those following packages are required for the program. You can use **pip** or other package management tools to get the required packages. Here are list of the packages required and the installation commands in pip.
	1. **Tweepy**
	`$ pip install tweepy` 
	2. **NumPy**
	`$ pip install numpy` 
	3. **Pandas**
	`$ pip install pandas` 

# Basic Usage
You can use this program by executing the **apps.py**.
`$ python apps.py`

The program will request some information regarding to the tweet you want to stream.

# Files

Olivia DeJonge will save the streaming results in `.csv` file, and these files will all be stored in `target/` folder.
Table below explains all the attribute of the data stored.

Column | Description
-|-
`date` | Date of tweet posted.
`name` | Name of user who sent the tweet.
`screen_name` | Username of user who sent the tweet. `@someone` without the `@`
`verified` | Boolean representation of whether the account that sent the tweet is verified or not. `0 = not verified, 1= verified`
`location` | Location of user who sent the tweet.
`text` | The tweet itself
`user_mentions` | List of username of users mentioned in the tweet.
`hashtags` | List of hashtag used in the tweet

# Developer Message
> Go follow [https://instagram.com/olivia_dejonge](instagram.com/olivia_dejonge) <3 <3 <3 