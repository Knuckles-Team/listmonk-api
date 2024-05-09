# Listmonk API

![PyPI - Version](https://img.shields.io/pypi/v/listmonk-api)
![PyPI - Downloads](https://img.shields.io/pypi/dd/listmonk-api)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/listmonk-api)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/listmonk-api)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/listmonk-api)
![PyPI - License](https://img.shields.io/pypi/l/listmonk-api)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/listmonk-api)

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/listmonk-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/listmonk-api)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/listmonk-api)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/listmonk-api)

![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/listmonk-api)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/listmonk-api)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/listmonk-api)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/listmonk-api)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/listmonk-api)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/listmonk-api)

*Version: 0.3.0*

Listmonk API Python Wrapper

This repository is actively maintained - Contributions are welcome!

### API Calls:
- Subscribers
- Lists
- Import
- Campaigns
- Media
- Templates
- Transactional

<details>
  <summary><b>Usage:</b></summary>

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

</details>

<details>
  <summary><b>Installation Instructions:</b></summary>

Install Python Package

```bash
python -m pip install listmonk-api
```

</details>

<details>
  <summary><b>Repository Owners:</b></summary>


<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)
</details>
