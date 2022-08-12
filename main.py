import os
from paul import Paul
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv('data/.env')
    client = Paul()
    client.run(os.getenv('TOKEN'))
