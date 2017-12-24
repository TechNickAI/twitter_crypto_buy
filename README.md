# Twitter Crypto Buy

Listen to a twitter account for a mention of a crypto currency and buy it. 

Originally built for the @officialmcaffee account after watching that whatever crypto he mentioned for his "Coin of the day" rose signifigantly.

## Requirements

* A suitable environment to run the bot. [screen](https://www.gnu.org/software/screen/) on *nix should do.
* Knowledge of Python
* A [Bittrex](https://bittrex.com/) account with BTC available, and an [API key](https://support.bitfinex.com/hc/en-us/articles/115002349625-API-Key-Setup-Login) with trade access.
* Tolerance for risk (**this might fail miserably and lose money)
* Twitter streaming API access. This is the hardest part, it's a PITA to set up.

## Setup

1. Clone the repo
2. Create a virtualenv with python3
3. Install the requirements (`pip install -r requirements.txt`)

## Running 

1. Run `python bot.py` with the appropriate environment variables set
2. Profit (or loss)

## TODO

[ ] Sentiment analysis on the tweet to make sure that it is a positive mention

[ ] Sanity checks to make sure we don't do stupid stuff like buy more than once
