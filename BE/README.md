# HelpServiceBE

## Testing
`pytest` to run the tests

### This is backend of our volunteer help service

Local setup:

- Python 3.9
- Configure .env file with `.env-example`. Minimum change `MONGODB_URL` to your own (local of in cluster, i.e. with free tier). 
  - ensure you have `HelpService` database
- Run `pip install -r requirements.txt` from root
- Run `uvicorn main:app --host 0.0.0.0 --port 5000` from root

To fulfill data in mongo you can:

- Use dump from `deploy` folder (can be deprecated)
- Install bot locally and then make some order and get same result 