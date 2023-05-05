from dotenv import load_dotenv, find_dotenv


def config():
    load_dotenv(find_dotenv())
