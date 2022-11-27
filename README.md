# Listmonk API
*Version: 0.1.1*

Listmonk API Python Wrapper

This repository is actively maintained and will continue adding more API calls

### API Calls:
- Subscribers
- Lists
- Import
- Campaigns
- Media
- Templates
- Transactional

### Usage:

```python
#!/usr/bin/python
# coding: utf-8
import listmonk_api

username = "<LISTMONK USERNAME>"
password = "<LISTMONK_PASSWORD>"
listmonk_api_url = "<LISTMONK_URL>"
client = listmonk_api.Api(url=listmonk_api_url, username=username, password=password)

lists = client.get_lists()
print(f"Lists: {lists}")

created_list = client.create_list(name="EXAMPLE TEMPLATE", type="<public/private>", optin="<single/double>", tags=['<LIST TAG>'])
print(f"Created List: {created_list}")

created_campaign = client.create_campaign(name="EXAMPLE TEMPLATE", type="<public/private>", optin="<single/double>", tags=['<LIST TAG>'])
print(f"Created Campaign: {created_campaign}")

print(f"Subscribers: {client.get_subscribers()}")

print(f"Campaigns: {client.get_campaigns()}")
```

#### Install Instructions
Install Python Package

```bash
python -m pip install listmonk-api
```

#### Build Instructions
Build Python Package

```bash
sudo chmod +x ./*.py
pip install .
python setup.py bdist_wheel --universal
# Test Pypi
twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose -u "Username" -p "Password"
# Prod Pypi
twine upload dist/* --verbose -u "Username" -p "Password"
```
