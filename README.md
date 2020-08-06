# sec-lint

Please copy the custom_hooks folder to the gitlab's [Gitaly relative path](https://docs.gitlab.com/ee/administration/server_hooks.html). 

Make the pre-receive file and the linter.py file executable and ensure that the custom_hooks and it's files are owned by the Git user and in the Git group.

testCase:
```bash
python testCase.py
```

# License
MIT