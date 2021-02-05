# Cloudflare-AutoUpdate
This loops through all "A" records and sets the ip to the external IPv4 of the machine. Everything else, however remains the same.
## Setup & Running
```bash
git clone https://github.com/OskarsMC-Network/Cloudflare-AutoUpdate.git
cd 'Cloudflare-AutoUpdate'
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```
## Contributing
I don't see why you would want to contribute to this, but you are free to. Submit a PR and if it works, ill accept it.