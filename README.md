\# Automated Order Report Generation Using AWS S3 \& Lambda



\## Project Overview



This project implements an event-driven data processing pipeline using Amazon S3, AWS Lambda, Python, and Pandas.



Whenever a daily orders CSV file is uploaded to an S3 bucket, an AWS Lambda function automatically processes the file, calculates total revenue by city, and saves a summarized CSV report back to S3.



The solution eliminates manual report preparation and demonstrates serverless data processing on AWS.



\## Architecture



```text

Daily Orders CSV

&#x20;      |

&#x20;      v

Amazon S3 (incoming/)

&#x20;      |

&#x20;      | ObjectCreated Event

&#x20;      v

AWS Lambda (Python 3.12)

&#x20;      |

&#x20;      | Pandas Lambda Layer

&#x20;      | Revenue = Quantity × Price

&#x20;      | Group By City

&#x20;      | Sort By Revenue DESC

&#x20;      v

Amazon S3 (reports/)

&#x20;      |

&#x20;      v

City Revenue Summary CSV



AWS CloudWatch → Execution Logs

```



\## Technologies Used



\- \*\*Amazon S3:\*\* Storage for input CSV files and generated reports.

\- \*\*AWS Lambda:\*\* Serverless processing triggered by S3 uploads.

\- \*\*AWS IAM:\*\* Role-based permissions for secure S3 access and logging.

\- \*\*Amazon CloudWatch:\*\* Monitoring and execution logs.

\- \*\*Python 3.12:\*\* Data processing logic.

\- \*\*Pandas:\*\* Revenue calculations and city-wise aggregation.

\- \*\*Boto3:\*\* AWS SDK for accessing S3.

\- \*\*AWS CLI:\*\* Uploading files and verifying AWS resources through PowerShell.



\## Project Configuration



| Component | Configuration |

|---|---|

| AWS Region | ap-south-2 (Hyderabad) |

| S3 Bucket | ecommerce-order-report-project1 |

| Input Prefix | incoming/ |

| Output Prefix | reports/ |

| Lambda Function | OrderRevenueReportLambda |

| Runtime | Python 3.12 |

| Architecture | x86\_64 |

| Lambda Layer | pandas-order-report-layer |

| Execution Role | OrderReportLambdaRole |



\## Input Dataset



The input file, `orders.csv`, contains 30 e-commerce orders with the following columns:



`order\_id, customer\_name, product, category, quantity, price, city, order\_date`



Revenue is calculated for each order using:



\*\*Revenue = Quantity × Price\*\*



The resulting revenue values are aggregated by city.



\## Implementation Steps



\### 1. Create S3 Bucket



Create an S3 bucket with two prefixes:



\- `incoming/` for raw order files.

\- `reports/` for generated revenue reports.



\### 2. Configure IAM Permissions



Create a Lambda execution role with:



\- `s3:GetObject` for reading objects from `incoming/`.

\- `s3:PutObject` for writing objects to `reports/`.

\- `AWSLambdaBasicExecutionRole` for CloudWatch logging.



\### 3. Create Lambda Function



Create `OrderRevenueReportLambda` with the Python 3.12 runtime.



The function:



1\. Receives an S3 ObjectCreated event.

2\. Extracts the bucket name and object key.

3\. Reads the uploaded CSV using Boto3 and Pandas.

4\. Calculates revenue for each order.

5\. Aggregates total revenue by city.

6\. Sorts cities by revenue in descending order.

7\. Saves the generated summary to the S3 reports prefix.



\### 4. Create Pandas Lambda Layer



On Windows PowerShell, create a `python` directory and install Linux-compatible Pandas dependencies:



```powershell

python -m pip install pandas --platform manylinux\_2\_28\_x86\_64 --target .\\python --implementation cp --python-version 3.12 --only-binary=:all: --upgrade

```



Package the dependencies:



```powershell

Compress-Archive -Path .\\python -DestinationPath .\\pandas-layer.zip

```



Create a custom Lambda Layer using this ZIP and attach it to the Lambda function.



Ensure the layer matches the Lambda runtime and architecture. If the ZIP exceeds the direct-upload limit, upload it through S3.



\### 5. Configure S3 Trigger



Configure an S3 event notification with:



\- \*\*Event type:\*\* All object create events

\- \*\*Prefix:\*\* `incoming/`

\- \*\*Suffix:\*\* `.csv`



This ensures Lambda processes only CSV uploads in the incoming prefix.



\### 6. Upload Input Data



Using AWS CLI:



```powershell

aws s3 cp .\\orders.csv s3://ecommerce-order-report-project1/incoming/orders.csv --region ap-south-2

```



\### 7. Verify the Output



List the generated reports:



```powershell

aws s3 ls s3://ecommerce-order-report-project1/reports/ --region ap-south-2

```



Example report filename:



`city\_revenue\_summary\_2026-11-16.csv`



The report contains:



```csv

city,total\_revenue

Bangalore,8698.00

Mumbai,7864.00

Hyderabad,4850.00

Delhi,4603.00

Chennai,2528.00

```



\### 8. Monitor Execution



Check CloudWatch logs:



```powershell

aws logs tail /aws/lambda/OrderRevenueReportLambda --since 30m --region ap-south-2

```



Verify the processing message, report-generation message, and successful execution.



\## Project Structure



```text

order-report-project/

├── lambda\_function.py

├── orders.csv

├── README.md

├── summary-output/

│   └── city\_revenue\_summary\_2026-11-16.csv

├── screenshots/

│   ├── s3-bucket.png

│   ├── lambda-trigger.png

│   ├── generated-report.png

│   └── cloudwatch-logs.png

└── .gitignore

```



The Pandas layer binaries are excluded from the repository to keep it lightweight.



\## Results



\- Successfully implemented an event-driven serverless reporting pipeline.

\- Automated the calculation of city-wise revenue.

\- Generated a summary CSV in Amazon S3.

\- Verified Lambda execution using CloudWatch logs.

\- Used a reusable Lambda Layer for Pandas dependencies.



\## Limitations and Future Improvements



\- Uploading multiple files on the same UTC date overwrites the existing daily summary.

\- Input validation and malformed-record handling can be enhanced.

\- S3 events may occasionally be delivered more than once, so production implementations should consider idempotency.

\- Amazon SNS or SQS could be integrated to notify the sales team when a report is ready.

\- AWS EventBridge could support scheduled reporting and additional automation.



\## Conclusion



This project demonstrates how AWS serverless services can automate a practical e-commerce reporting workflow. It provides hands-on experience with S3 event notifications, Lambda functions, IAM permissions, Lambda Layers, Python data transformations, and CloudWatch monitoring.



