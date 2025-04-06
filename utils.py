from dotenv import load_dotenv
import os

def load_api_key():
    """
    환경 변수를 로드합니다.
    :return: API 키
    """
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY is not set in the environment variables.")
    return api_key

if __name__ == "__main__":
    load_dotenv()
    # API 키를 로드합니다.
    try:
        api_key = load_api_key()
        print("API_KEY loaded successfully.")
    except ValueError as e:
        print(e)