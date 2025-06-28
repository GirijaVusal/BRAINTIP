import hashlib


def generate_token(text: str = "THIS_IS_SECRET##") -> str:
    # Use SHA256 hash of the text as a token
    return hashlib.sha256(text.encode()).hexdigest()


if __name__ == "__main__":
    # token = generate_token("hello world")
    token = generate_token()
    print(token)
