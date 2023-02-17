# Week 0 — Billing and Architecture

## Required Homework/Tasks
### Watched Week 0 - Live Streamed Video
:white_check_mark: I was present during the live trasmisstion [Link to video](https://www.youtube.com/watch?v=SG8blanhAOg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=12)

Please find below some notes that I have taken from the video:
#### Bussines use case of the project
At the end of the course we will have implemented a new social media called Cruddur, which is an ephemral social network where the users can post, share temporal messages and at the same time bring the user th posibility of monetize the content that has been creted. During this time, we will be using all concepts learned during the lenssons to carry on the works by using AWS services, Github and Gitpod mainly. 

This platform will be using the architecture of microservices which helps to reuse services and code scalling. Where JavaScript + React will be used for frontend and Python + React will be used for backend, regarding databses it might be using SQL or NOSQL DB, the system will have its own NFQDN and security polcies will be implemented to protect the pplatform and users.

There are 2 types of application archtecture:
* Monolitic: In this the archtecture there is only one application that centralices all the works and the system relays only in it. There is no separated services for each function.
* Microservices: It realys on a series of services deployable which acomplish specific functions or goals and the can be updated, tested, deployed and scaled. it reduces the complexity of the solution. It rellays on the stack below: 
<table>
    <tr>
        <td>User Unit</td>
    </tr>
    <tr>
        <td>Bussines logistics</td>
    </tr>
    <tr>
        <td>Data access</td>
    </tr>
</table>
The Iron triangle is a model that should be taken in account to manage the project correctly, it helps to keep the balance and carry on the proyect by undrestanding the strengs and willness of the project. The triagle is based on 3 pilars: scope, cost and time.
<p align="center"><img src="assets/week0/iron_triangle.png" width="350" alt="accessibility text"></p>

* Scope: Comprehence the features and funtionality (example.new service).
* Cost: Comprehence the budget and resource. (example. how much does it cost? and there is the enough resources?).
* Time: Comprehence the Schdule. (example: how long it will take based on complxity of the tasks, budget and resources?).

With the help of this diagram, we can unserstand the efect will have any action taken during the project and how it can be mitigated.

#### C4 Model
It's a model used to create set of architecture diagramas at work by using the 4C's: System context diagrams, Container diagrams,  Component diagrams and Code. Each of them is a different draw that brings different description levels of the achitecture to buid.
* System context diagrams :arrow_right: It provides the overal system context where there are reactangles and others types of shapes which represents each element of the architecture and their interaction (without going into the detail because the goal to achieve is non technical people can understand your idea)
* Container diagram :arrow_right: It contains the individual service or application by providing high level of tecnology information based on the diagrams (example: protocols, databases, API, micro services, etc). The target in this diagram are developers and software architecters withing or out the team.
* Component diagram :arrow_right: This diagram describes with more detail the information placed in container diagram, it will show the components that made the container up. The target udience are developers and software architects.
* Code :arrow_right: The detailed information of each component and how implement it, its the information that will be find here. Usually UML diagrams are builded here do describe the information.

#### Cloud architecture
* A good architecture of a cloud should have:
    * Clear vocabulary :arrow_right: Understand customer needs.
    * The requirements should be measurable.
    * The objective should be verfible.
    * The requirements should be monitoreable.
    * Clear undertanding about what can be truncable or feastable.
    * Address risk, assumptions and constrains.
* Dising phases:
    * Conceptual desing :arrow_right: first idea.
    * Logical desing :arrow_right: General information.
    * Physical desing  :arrow_right: Actual desing with real inforamtion.
* Tips from RRACs:
    * Ask dummy questions :arrow_right: This is to have the clearest view as possible.
    * Play be the packet :arrow_right: Recreating the possible scenarios will allow the designer reduce the range of failures in the future.
    * Document everything :arrow_right: Don't miss anything.
* TOGAF:
    * Framework for cloud architecture.
    * It maches within AWS services.
    * It brings the vocabulary to work as cloud achitector.
    * The most populat framework for EA.
* [Course diagram](https://lucid.app/lucidchart/6f80cd2d-7d18-4731-aadc-bdda9773c092/edit?invitationId=inv_c648fee2-f691-443d-8602-7e959b41a18d&page=u~1sbYNXU9q3#)

### Watched Chirag's Week 0 - Spend Considerations	
:white_check_mark: DONE, I watched the video, executed the works address by the instructor and summited the quiz without any issue. [Link to video](https://www.youtube.com/watch?v=OVw3RrlP-sI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=13)

### Watched Ashish's Week 0 - Security Considerations
:white_check_mark: DONE, I watched the video, executed the works address by the instructor and summited the quiz without any issue. [Link to video](https://www.youtube.com/watch?v=4EMWBYVggQI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=15)

### Recreate Conceptual Diagram in Lucid Charts or on a Napkin
:white_check_mark: DONE, I didn't have problems to recreate the chart. 

Find the link to chart file :point_right: [Link to Lucid charts file](https://lucid.app/lucidchart/aea4dfd7-f680-4c1a-99b9-1abad176d570/edit?viewport_loc=-311%2C-84%2C3840%2C1554%2C0_0&invitationId=inv_5bded0c2-5dd1-4840-b55c-264de7306582)

Here it is my napking desing:
<p align="center"><img src="assets/week0/napking.jpeg" alt="accessibility text"></p>

### Recreate Logical Architectual Diagram in Lucid Charts
:white_check_mark: DONE, I didn't have problems to recreate the diagram. 

Find the link to chart file :point_right: [Link to Lucid charts file](https://lucid.app/lucidchart/aea4dfd7-f680-4c1a-99b9-1abad176d570/edit?viewport_loc=-104%2C-36%2C3840%2C1554%2CjF0wpWsibGvK&invitationId=inv_5bded0c2-5dd1-4840-b55c-264de7306582)

<p align="center"><img src="assets/week0/Cruddur - Conceptual Diagram - Logical App.png" alt="accessibility text"></p>

### Create an Admin User
:white_check_mark: DONE, I didn't have problems to create my admin user.

Here there is the prove to the created user called "cristianramos"
<p align="center"><img src="assets/week0/admin user creation.png" alt="accessibility text"></p>

This user was created on Feb 13th and it has assigned the policy "Administratoraccess" as is stated in the picture below:

<p align="center"><img src="assets/week0/IAM Management Console.png" alt="accessibility text"></p>

### Use CloudShell
:white_check_mark: DONE, I didn't have problems launch and use the cloudshell from root and admin user account.  

In the picture below I was able to execute the commands from CloudShell: "aws sts get-caller-identity" and "aws account get-contact-information": 

<p align="center"><img src="assets/week0/AWS_CloudShell_my_admin_info.png" alt="accessibility text"></p>

### Generate AWS Credentials
:white_check_mark: DONE, I did almost all without any problem. However my blocking point was the problems at moment to make the push to Github, because I didn't set correctly the permissions between Gitpod and Github. When I realized about it, I fixed it and the push started to work.

The access key generated:
<p align="center"><img src="assets/week0/last_access_keys.png" alt="accessibility text"></p>

The access keys exported to env in linux:
<p align="center"><img src="assets/week0/generated_keys_loaded2.png" alt="accessibility text"></p>

Showing the status of the keys:
<p align="center"><img src="assets/week0/prove_linux_connection2.png" alt="accessibility text"></p>

Access keys stored on Gitpod:
<p align="center"><img src="assets/week0/keys_stored_in_gitpod.png" alt="accessibility text"></p>

### Installed AWS CLI
:white_check_mark: DONE, I didn't have problems to install and launch and use AWS CLI from Windows or Linux.

Here you can find the proves that I installed the AWS CLI for windows from .msi file:
<p align="center"><img src="assets/week0/aws_cli_win_install.png" alt="accessibility text"></p>

Then I configured my access key:
<p align="center"><img src="assets/week0/win_aws_cli_config.png" alt="accessibility text"></p>

And here there is the results:
<p align="center"><img src="assets/week0/win_aws_cli_review.png" alt="accessibility text"></p>

### Create a Billing Alarm
:white_check_mark: DONE, I didn't have problems to create the Billing alarm.

Enbaling billing alerts:
<p align="center"><img src="assets/week0/billing_alert_2.png" alt="accessibility text"></p>

SNS configuration:
<p align="center"><img src="assets/week0/sns.png" alt="accessibility text"></p>

Created billing alarm:
<p align="center"><img src="assets/week0/Billing alert.png" alt="accessibility text"></p>

### Create a Budget	
:white_check_mark: DONE, I didn't have problems to create the Budget of 10 USD.

Budget configuration:
<p align="center"><img src="assets/week0/Budget_creation.png" alt="accessibility text"></p>

## Homework chanllenges
### 1. Destroy your root account credentials, Set MFA, IAM role
:white_check_mark: DONE,  I didn't have problems to set the MFA, IAM role.

#### NFA set for root and admin user account:
<p align="center"><img src="assets/week0/mfa.png" alt="accessibility text"></p>

#### New IAM role set called "AdminRole_bootcamp":
Role summary:
<p align="center"><img src="assets/week0/role.png" alt="accessibility text"></p>

Role configuration:
<p align="center"><img src="assets/week0/role_config.png" alt="accessibility text"></p>

2. Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.
3. Review all the questions of each pillars in the Well Architected Tool (No specialized lens)
4. Create an architectural diagram (to the best of your ability) the CI/CD logical pipeline in Lucid Charts
5. Research the technical and service limits of specific services and how they could impact the technical path for technical flexibility. 
6. Open a support ticket and request a service limit







