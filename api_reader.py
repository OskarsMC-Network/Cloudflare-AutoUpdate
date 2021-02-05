def get_api_key(announce: bool) -> str:
    file = open("api_key.txt", "r+")
    lines = file.readlines()
    if lines == []:
        print("[Local] Please Insert API key to api_key.txt (file created)")
        quit()
        return None
    else:
        if announce:
            print(f"[Local] Found Key: {lines[0]}")
        return lines[0]
