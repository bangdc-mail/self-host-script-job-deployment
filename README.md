
# Deploying python script to Raspberry pi server using GitHub as a beginner 📚

## Why this?
I used to use Google Cloud Platform (GCP) as a way to run my scripts. I would code, compile, run, test, create a CI/CD pipeline on GitLab/Github; afterwards deploying on GCP job with its cron schedule and have the script run things automatically that I would have to do manually. Now that I have a raspberry pi running around with my applications, I just want to move some of my simple scripts to the raspberry pi.
Thus, this repository will be a place to document my approach and hope this helps some beginners that have similar needs.

## Prerequisites

- A server of some kind (PC, laptop that runs constantly, raspberry pi lying around, VPS,...)
- Installed Python, git, docker...etc...
- Github
- Running electricity 😃
- ...

## Steps

### Set up Pi and Github

On your Pi:
```
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl
```
- Set up ssh key (for github)
```
ssh-keygen -t ed25519 -C "pi-deploy-key"
```
- This make (if no passphrase and default)
	- private key → `~/.ssh/id_ed25519`
	- public key → `~/.ssh/id_ed25519.pub`
- Copy the public key:
```
cat ~/.ssh/id_ed25519.pub
```
- In GitHub:
	- Go to your repo
	- Settings → **Deploy Keys**
	- Add key
	- ✅ Allow write access (if needed)
- Test connection:
`ssh -T git@github.com`

- Clone the repo with ssh to the pi
```
git clone git@....
cd [Your repo]
```

### Docker
- Install docker, docker compose on the Pi (ref: [[Docker, Docker Compose Intro]])

on the Pi's repo directory (`cd [YOUR REPO]`):
- Create a python script, something simple like
```
import requests

def get_dad_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        print(data["joke"])
    except Exception as e:
        print("Error fetching joke:", e)

if __name__ == "__main__":
    get_dad_joke()
```
This creates a simple dad joke script just for testing. `python3 main.py`
- Create Dockerfile (`nano Dockerfile`)
and have something like this in the `Dockerfile`:
```
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt || true
CMD ["python", "main.py"]
```
- create `docker-compose.yml`
just something like this (modify to suit your needs) - ref: [[Docker, Docker Compose Intro]]
(I replace context with my mounted volume)
```
version: "3.9"
services:
  my-job:
    build:
      context: .
      dockerfile: Dockerfile
    image: my-python-job:latest
    container_name: my-python-job
networks: {}
```
- Test out of everything running
```
// build and run
docker compose up --build
// test run and exit
docker compose run --rm my-job
```

### GitHub Action

Github Action is where you can build your pipeline to automate the process of deploying the code to the server without having to manually pull the code and build every time you commit the code to the repo.

#### Install a GitHub Actions Runner on your Pi
- Go to your repo → **Settings → Actions → Runners**
- Add a **self-hosted runner**
- Follow the Linux instructions

This installs a small agent that listens for jobs.
#### Create a GitHub Actions Workflow

In your repo, create:
`.github/workflows/deploy.yml`
Example:
```yaml
name: Deploy to Raspberry Pi
on:
  workflow_dispatch:   # manual button, only for private repo
  push:
    branches: [main]   # optional auto deploy
jobs:
  deploy:
    runs-on: self-hosted
    steps:
      - name: Pull latest code
        run: |
          cd /home/raspberry/git-repo/self-host-script-job-deployment
          git fetch origin
          git reset --hard origin/main
      - name: Rebuild image via Dockge
        run: |
          cd /home/raspberry/git-repo/self-host-script-job-deployment
          docker compose build --no-cache my-job
```
This makes a workflow that has a button to press and it should deploy to the server (raspberry pi in my case), then rebuild the image that Dockge is going to refer to. Please do review and make changes to the workflow to suit your needs
#### Pull image or rebuild containers
Others may differ but for my case, I manage my docker containers using **Dockge**, thus I just need to tweak my `docker-compose.yml` stacks and/or mount the git repo to Dockge as a volume. However with the automation of rebuilding the image, this may not be required.

Else if your Python scripts are inside the repo:
`docker compose up -d --build`
#### Note: “Deploy Button”

GitHub gives you this automatically via:
- **Actions tab → “Run workflow” button**
This should appear on the Actions tab if the .github/workflows/ folder is commited to the branch.

Now every changes pushed to the repo can be deployed to the server for trigger.

#### Add Scheduler-type action

Since we are already running with Github Actions, I'll just make a separate scheduler that dedicates only to running the image/Python scripts

```yaml
name: Scheduled Job Runner
on:
  schedule:
    - cron: "0 7 * * *"
jobs:
  run-job:
    runs-on: self-hosted
    concurrency:
      group: scheduled-job
      cancel-in-progress: false
    steps:
      - name: Run container
        run: docker run --rm my-job:latest
```

And this concludes the approach I have for running scripts automatically on your server with CI/CD pipeline and scheduling. There should be better ways to automate the process. However, this repository would serves as how I discover and try to solve an issue that I have on my self-hosting journey.