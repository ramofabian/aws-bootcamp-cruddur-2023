# Week 3 — Decentralized Authentication
## Mandatory tasks
### Watched Ashish's Week 3 - Decenteralized Authentication	
:white_check_mark: DONE.
### Watch Chirag Week 3 - Spending Considerations	
### Setup Cognito User Pool	
:white_check_mark: DONE. I had some issues with the user pool and I had to recreated it a couple times, becuase I had missed some features to make it work properly.

The following parameters were used create the user pool correctly via web from AWS Cognito for ours Cruddur application:
```
* User pool name: cruddur-user-pool
* provider option: Cognito user pool (default)
* Cognito user pool sign-in: email
* Multi-factor autenticator: No MFA
* User account recovery: Enable self-service account recovery and email only
* Required attributes: name and preferred_username
* Email: Send email with Cognito
* Integrate your app (User pool name): cruddur-user-pool
* Initial app client: Public client
* App client name: cruddur
```

- Please find below the user pool created:

<p align="center"><img src="assets/week3/user_pool_created.png" alt="accessibility text"></p>

- Created users:
 
<p align="center"><img src="assets/week3/user_pool_users.png" alt="accessibility text"></p>

- With the command `aws cognito-idp list-user-pools --max-results 20`

<p align="center"><img src="assets/week3/user_pool_info_via_aws_cli.png" alt="accessibility text"></p>

- With the command `aws cognito-idp describe-user-pool --user-pool-id <<user_pool_id>>` the user pool configuration can be seen from AWS CLI

- With the command `aws cognito-idp list-user-pool-clients --user-pool-id <<user_pool_id>>` the app client are listed:

<p align="center"><img src="assets/week3/user_pool_client.png" alt="accessibility text"></p>

- With this command the created users under `cruddur-user-pool` administration `aws cognito-idp list-users --user-pool-id <<user_pool_id>>`

<p align="center"><img src="assets/week3/user_pool_created_users.png" alt="accessibility text"></p>

<b>References:</b> [AWS CLI Reference](https://docs.aws.amazon.com/cli/latest/index.html) and [AWS web tutotial](https://docs.aws.amazon.com/cognito/latest/developerguide/tutorial-create-user-pool.html)

### Implement Custom Signin Page
### Implement Custom Signup Page
### Implement Custom Confirmation Page
### Implement Custom Recovery Page
### Watch about different approaches to verifying JWTs
