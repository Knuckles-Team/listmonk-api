# Listmonk API
*Version: 0.0.1*

Listmonk API Python Wrapper

This repository is actively maintained and will continue adding more API calls

### API Calls:
- Campaigns
- Lists
- Import

### Usage:

```python
#!/usr/bin/python
# coding: utf-8
import listmonk_api

token = "<GITLAB_TOKEN/PERSONAL_TOKEN>"
gitlab_url = "<GITLAB_URL>"
client = listmonk_api.Api(url=gitlab_url, token=token)

users = client.get_users()
print(users)

created_merge_request = client.create_merge_request(project_id=123, source_branch="development",
                                                    target_branch="production", title="Merge Request Title")
print(created_merge_request)

print(f"Users: {client.get_users()}")

print(f"Projects: {client.get_projects()}")

response = client.get_runners(runner_type='instance_type', all_runners=True)
print(f"Runners: {response}")
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