# Week 1 — App Containerization
## Required Homework/Tasks
### Watched Grading Homework Summaries
:white_check_mark: DONE.
### Watched Week 1 - Live Streamed Video
:white_check_mark: DONE.
### Remember to Commit Your Code
:white_check_mark: DONE.
### Watcked Chirag's Week 1 - Spending Considerations
:white_check_mark: DONE.
### Watched Ashish's Week 1 - Container Security Considerations
:white_check_mark: DONE.

I installed snyk and docker compose on my prsonal ubuntu VM and ran the docker-compose.yml as it was done from the video. Then I scanned the running docker containers to see if there is any security breaches. It was good exersice and very much stright forward procedure, I liked it becuse this is something that I had never done before.

I followed this procedure form this [link](https://docs.snyk.io/snyk-cli/install-the-snyk-cli)
```
# To download the packet
curl https://static.snyk.io/cli/latest/snyk-linux
chmod +x ./snyk
mv ./snyk /usr/local/bin/

# Check the version
snyk --version

# Login on Snyk system 
snyk auth

# Go to your to your docker directory where docker composer is placed
cd <<your docker directory>>

# Monitor de version immages
snyk monitor

# Scan your running container
snyk test 
```

Find below the evidence of the scan perfomed snyk CLI:

<p align="center"><img src="assets/week1/snyk_test.png" alt="accessibility text"></p>

The same result seen from Snyk website:

<p align="center"><img src="assets/week1/snyk_web_results.png" alt="accessibility text"></p>

### Containerize Application (Dockerfiles, Docker Compose)

