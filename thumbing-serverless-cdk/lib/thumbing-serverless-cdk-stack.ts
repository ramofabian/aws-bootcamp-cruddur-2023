import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import * as dotenv from 'dotenv';

// Load env variables
dotenv.config();

export class ThumbingServerlessCdkStack extends cdk.Stack {
  // main method
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    // The code in tyscript that defines your stack goes here
    
    //Define our bucket name env var
    const bucketName: string = process.env.THUMBING_BUCKET_NAME as string;
    // Define function path env var
    const functionPath: string = process.env.THUMBING_FUNCTION_PATH as string;
    const folderInput: string = process.env.THUMBING_S3_FOLDER_INPUT as string;
    const folderOutput: string = process.env.THUMBING_S3_FOLDER_OUTPUT as string;
    // Create the bucket
    const bucket = this.createBucket(bucketName);
    const lambda = this.createLambda(functionPath, bucketName, folderInput, folderOutput);
  }

  createBucket(bucketName: string): s3.IBucket {
    //This function creates a bucket
    // id = 'ThumbingBucket'
    // bucket Name = bucketName,
    const bucket = new s3.Bucket(this, 'ThumbingBucket', {
      bucketName: bucketName,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
    return bucket;
  }

  createLambda(functionPath: string, bucketName: string, folderInput: string, folderOutput: string): lambda.IFunction {
    //This function 
    // id = 'ThumbLambda'
    // lambda pthat file = functionPath,
    // lambda code lenguage = lambda.Runtime.NODEJS_18_X
    // code = lambda path
    const lambdaFunction = new lambda.Function(this, 'ThumbLambda', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(functionPath),
      environment: {
        DEST_BUCKET_NAME: bucketName,
        FOLDER_INPUT: folderInput,
        FOLDER_OUTPUT: folderOutput,
        PROCESS_WIDTH: '512',
        PROCESS_HEIGTH: '512'
      }
    });
    return lambdaFunction;
  }
}
