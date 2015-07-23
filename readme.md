## Jenkins CI HUD

There are other dashboards out there but none that I found met my needs.

I wanted a dashboard that had a history of the merge request tests, and big status boxes for the deployment jobs.

This is setup for the [gitlab plugin](https://wiki.jenkins-ci.org/display/JENKINS/GitLab+Plugin) & [jenkins notification.](https://wiki.jenkins-ci.org/display/JENKINS/Notification+Plugin) It will parse the $gitlabSourceBranch & $gitlabTargetBranch and go from there. 


### Screenshots
![jenkins ci hud](screenshots/hud.png?raw=true)

### Install
```
pip install -r requirements
python manage.py createdb
python manage.py runserver
```
You can take out the sample data in manage.py.

### Jenkins setup
Install [gitlab plugin](https://wiki.jenkins-ci.org/display/JENKINS/GitLab+Plugin) & [jenkins notification.](https://wiki.jenkins-ci.org/display/JENKINS/Notification+Plugin).

Parameterize your deployment jobs so the source branch is $gitlabSourceBranch. I have the app look for this parameter in the json from jenkins. See the screenshots for help.

The ContinuousBuilds table is only populated if it has gitlabTargetBranch (because then it is a merge request)

![notification](screenshots/notification.png?raw=true)
![parameters](screenshots/parameters.png?raw=true)
![branches](screenshots/branches.png?raw=true)


