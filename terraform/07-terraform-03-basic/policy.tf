//Импортирал сюда политики, Включает политики:
//AmazonEC2FullAccess
//AmazonS3FullAccess
//AmazonDynamoDBFullAccess
//AmazonRDSFullAccess
//CloudWatchFullAccess
//IAMFullAccess



//Добавлено для работы с S3 Bucket
//https://www.terraform.io/docs/backends/types/s3.html
//        {
//      "Effect": "Allow",
//      "Action": "s3:ListBucket",
//      "Resource": "arn:aws:s3:::mybucket"
//       },
//       {
//          "Effect": "Allow",
//          "Action": ["s3:GetObject", "s3:PutObject"],
//         "Resource": "arn:aws:s3:::mybucket/path/to/my/key"
//        },
//#Добавлено для работы с DynamoDB Table
//       {
//          "Effect": "Allow",
//          "Action": [
//          "dynamodb:GetItem",
//          "dynamodb:PutItem",
//          "dynamodb:DeleteItem"
//      ],
//          "Resource": "arn:aws:dynamodb:*:*:table/mytable"
//    }
//


resource "aws_iam_policy" "terraform__user_policy" {
  name = "terraform__user_policy"
  path = "/"
  description = "Policy for work with Terraform"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:GetInsightRuleReport",
                "pi:*"
            ],
            "Resource": [
                "arn:aws:cloudwatch:*:*:insight-rule/DynamoDBContributorInsights*",
                "arn:aws:pi:*:*:metrics/rds/*"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "iam:GetPolicyVersion",
                "organizations:ListRoots",
                "rds:*",
                "cloudwatch:DeleteAlarms",
                "logs:*",
                "organizations:DescribeAccount",
                "dynamodb:*",
                "sns:Unsubscribe",
                "lambda:GetFunctionConfiguration",
                "autoscaling:*",
                "organizations:ListChildren",
                "datapipeline:CreatePipeline",
                "ec2:DescribeInternetGateways",
                "organizations:DescribeOrganization",
                "resource-groups:GetGroup",
                "cloudwatch:DescribeAlarmsForMetric",
                "logs:GetLogEvents",
                "ec2:DescribeAccountAttributes",
                "lambda:DeleteFunction",
                "sns:Subscribe",
                "sns:*",
                "iam:GetRole",
                "datapipeline:ListPipelines",
                "application-autoscaling:RegisterScalableTarget",
                "sns:ListSubscriptionsByTopic",
                "lambda:ListFunctions",
                "dax:*",
                "iam:GetPolicy",
                "outposts:GetOutpostInstanceTypes",
                "sns:CreateTopic",
                "application-autoscaling:DeleteScalingPolicy",
                "cloudwatch:GetMetricStatistics",
                "iam:*",
                "resource-groups:CreateGroup",
                "cloudwatch:*",
                "application-autoscaling:DescribeScalingPolicies",
                "lambda:ListEventSourceMappings",
                "cloudwatch:DescribeAlarms",
                "application-autoscaling:PutScalingPolicy",
                "ec2:*",
                "resource-groups:ListGroupResources",
                "lambda:DeleteEventSourceMapping",
                "datapipeline:ActivatePipeline",
                "ec2:DescribeSubnets",
                "resource-groups:GetGroupQuery",
                "autoscaling:Describe*",
                "tag:GetResources",
                "sns:DeleteTopic",
                "logs:DescribeLogStreams",
                "sns:ListTopics",
                "sns:SetTopicAttributes",
                "lambda:CreateEventSourceMapping",
                "datapipeline:DescribePipelines",
                "ec2:DescribeVpcAttribute",
                "cloudwatch:ListMetrics",
                "organizations:DescribePolicy",
                "sns:Publish",
                "cloudwatch:DescribeAlarmHistory",
                "ec2:DescribeAvailabilityZones",
                "application-autoscaling:DescribeScalingActivities",
                "organizations:DescribeOrganizationalUnit",
                "kms:DescribeKey",
                "organizations:ListPoliciesForTarget",
                "datapipeline:PutPipelineDefinition",
                "organizations:ListTargetsForPolicy",
                "s3:*",
                "application-autoscaling:DescribeScalableTargets",
                "datapipeline:QueryObjects",
                "datapipeline:DescribeObjects",
                "iam:ListRoles",
                "elasticloadbalancing:*",
                "sns:ListSubscriptions",
                "datapipeline:GetPipelineDefinition",
                "resource-groups:ListGroups",
                "ec2:DescribeSecurityGroups",
                "organizations:ListPolicies",
                "cloudwatch:PutMetricAlarm",
                "resource-groups:DeleteGroup",
                "ec2:DescribeVpcs",
                "kms:ListAliases",
                "organizations:ListParents",
                "datapipeline:DeletePipeline",
                "application-autoscaling:DeregisterScalableTarget"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": [
                        "autoscaling.amazonaws.com",
                        "ec2scheduled.amazonaws.com",
                        "elasticloadbalancing.amazonaws.com",
                        "spot.amazonaws.com",
                        "spotfleet.amazonaws.com",
                        "transitgateway.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "iam:PassedToService": [
                        "application-autoscaling.amazonaws.com",
                        "dax.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "VisualEditor4",
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": [
                        "replication.dynamodb.amazonaws.com",
                        "dax.amazonaws.com",
                        "dynamodb.application-autoscaling.amazonaws.com",
                        "contributorinsights.dynamodb.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "VisualEditor5",
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "iam:AWSServiceName": [
                        "rds.amazonaws.com",
                        "rds.application-autoscaling.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "VisualEditor6",
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "arn:aws:iam::*:role/aws-service-role/events.amazonaws.com/AWSServiceRoleForCloudWatchEvents*",
            "Condition": {
                "StringLike": {
                    "iam:AWSServiceName": "events.amazonaws.com"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::mybucket"
       },
       {
          "Effect": "Allow",
          "Action": ["s3:GetObject", "s3:PutObject"],
          "Resource": "arn:aws:s3:::mybucket/path/to/my/key"
       },
       {
          "Effect": "Allow",
          "Action": [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem"
      ],
          "Resource": "arn:aws:dynamodb:*:*:table/mytable"
    }
    ]
}
EOF
}



