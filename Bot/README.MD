# HelpServiceBot

### This is bot of our volunteer help service

Local setup:

- Configure .env file with `.env-example`
  - setup your mongo URI (local or in cluster)
  - ensure you have `HelpService` database
  - setup your bot token [click](https://core.telegram.org/bots)
  - cities are default for now
- Run `pip install -r requirements.txt` from root
- Run `python main.py` from root

Then you can make an order and it will apper in your mongo