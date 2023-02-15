# Week 0 — Billing and Architecture
## Technical Tasks
In the class and during the week, we laid out the foundation for the entire bootcamp by:
1. Prerequisites
2. Discussing the format of the bootcamp
3. Going over the business use-case of our project
4. Looking at an architectural diagram of what we plan to build
5. Showcase how to use Lucid Charts to build architectures
6. Talk about C4 Models
7. Running through the cloud services we will utilize
8. Testing that we can access our AWS accounts
9. Settings up AWS free-tier and understand how to track spend in AWS eg . AWS Budgets, AWS Cost Explorer, Billing Alarms
10. Understanding how to look at monthly billing reports
11. Launching AWS CloudShell and looking at AWS CLI
12. Generating AWS credentials
## Business Scenario
Your company has asked to put together a technical presentation on the proposed architecture that will be implemented so it can be reviewed by the fractional CTO.

Your presentation must include a technical architectural diagram and breakdown of possible services used along with their justification.

The company also wants to generally know what spend we expect to encounter and how we will ensure we keep our spending low.
## Weekly Outcome
* Gain confidence when working meter-billing with a Cloud Service Provider (CSP)
* To understand how to build useful architecture diagrams
* To gain a general idea of the cost of common cloud services
* To ensure we have a working AWS account
## Prerequisites
* Create an account in: Github, Gitpod (or configure your local VSC), Github CodeSpaces, AWS, Momento, Lucid Chards, HoneyComb.io, Rollback.
* Purchase a new public domain.
* Once Github account is created create a new repository by using Andrew's template [here](https://github.com/ExamProCo/aws-bootcamp-cruddur-2023).

Notes: 
* To create the AWS account you will need a credit card.
* Once you have completed these actions you can start with topic and tasks for week 0.
## Bussines use case of the project
At the end of the course we will have implemented a new social media called Cruddur, which is an ephemral social network where the users can post, share temporal messages and at the same time bring the user th posibility of monetize the content that has been creted. During this time, we will be using all concepts learned during the lenssons to carry on the works by using AWS services, Github and Gitpod mainly. 

This platform will be using the architecture of microservices which helps to reuse services and code scalling. Where JavaScript + React ill be used for frontend and Python + React will be used for backend, regarding databses it might be using SQL or NOSQL DB, the system will have its own NFDN and security polcies will be implemented to protect the pplatform and users.

Application layer:
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
The Iron triangle should be taken in account to manage the project correctly:
<p align="center">
  <img src="https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/iron_triangle.png" width="350" alt="accessibility text">
</p>

### C4 model
Pending

## Cloud architecture
* A good architecture of a cloud should have:
    * Clear vocabulary --> Understand customer needs.
    * The requirements should be measurable.
    * The objective should be verfible.
    * The requirements should be monitoreable.
    * Clear undertanding about what can be truncable or feastable.
    * Address risk, assumptions and constrains.
* Dising phases:
    * Conceptual desing --> first idea.
    * Logical desing --> General information.
    * Physical desing  --> Actual desing with real inforamtion.
* Tips from RRACs:
    * Ask dummy questions --> This is to have the clearest view as possible.
    * Play be the packet --> Recreating the possible scenarios will allow the designer reduce the range of failures in the future.
    * Document everything --> Don't miss anything.
* TOGAF:
    * Framework for cloud architecture.
    * It maches within AWS services.
    * It brings the vocabulary to work as cloud achitector.
    * The most populat framework for EA.



