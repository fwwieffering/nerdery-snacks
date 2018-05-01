import os
from snacks.utils import get_next_month


# secret key for signing hashed pws
secret_key = os.environ.get("SECRET_KEY", 'oiwjefoijoiwnmenkfughyy1222')

db_name = os.environ.get('DB_NAME', 'postgres')
db_user = os.environ.get('DB_USER', 'postgres')
db_pass = os.environ.get('DB_PASS', 'postgres')
db_host = os.environ.get('DB_HOST', 'localhost')


snacks_api_url = "https://api-snacks.nerderylabs.com/v1/snacks"
snacks_api_key = os.environ.get('SNACKS_API_KEY')

# max votes per time period
max_votes = 3
# function to get vote expiration
vote_expiration = get_next_month
