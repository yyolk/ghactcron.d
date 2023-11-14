import json
import os
import urllib.request
from datetime import datetime


github_event_url = "https://api.github.com/users/yyolk/events"
headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
taskade_reoccurring_push_to_github_task_id = os.environ[
    "taskade_reoccurring_push_to_github_task_id"
]
taskade_reoccurring_project_id = os.environ["taskade_reoccurring_project_id"]
taskade_api_pat = os.environ["taskade_api_pat"]
request = urllib.request.Request(github_event_url, headers=headers)
with urllib.request.urlopen(request) as response:
    data = json.load(response)
events_interested_in_leetcode_dailies_only = list(
    filter(
        lambda x: x["type"] == "PushEvent"
        and "repo" in x
        and x["repo"]["name"] == "yyolk/leetcode_dailies",
        data,
    )
)
push_events = list(filter(lambda x: x["type"] == "PushEvent", data))
for event in push_events:
    if (
        dtelta := (
            datetime.now()
            - datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        )
    ).days == 0:
        print(True)
        url_task_complete = f"https://www.taskade.com/api/v1/projects/{taskade_reoccurring_project_id}/tasks/{taskade_reoccurring_push_to_github_task_id}/complete"
        request = urllib.request.Request(url_task_complete, method="POST", headers={"Authorization": f"Bearer {taskade_api_pat}"})
        with urllib.request.urlopen(request) as response:
            print(response.code)
        break
    print(datetime.now() - datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ"))

else:
    print(False, "no push events today")
