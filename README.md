# HKU Moodle Auth

A Python script that gets the necessary cookies from the email and password for HKU Moodle to authenticate.

# Usage

```bash
# 1. Clone this repository
git clone https://github.com/nohackjustnoobb/HKU-Moodle-Auth.git && cd HKU-Moodle-Auth

# 2. Install the requirements.txt
pip3 install -r requirements.txt

# 3. Create config.json (optional)
touch config.json
cat  cat <<EOF >config.json
{
    "email": "example@connect.hku.hk",
    "password": "example"
}
EOF

# 4. Run the script
python3 main.py

# 5. Test the cookies (optional)
python3 test.py

```
