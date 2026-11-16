
import boto3
import pandas as pd
import io
from urllib.parse import unquote_plus

s3 = boto3.client("s3")


def lambda_handler(event, context):

    # Get S3 bucket and uploaded file name
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = unquote_plus(record["s3"]["object"]["key"])

    print(f"Processing file: s3://{bucket}/{key}")

    # Read orders CSV from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(response["Body"].read()))

    # Calculate revenue for each order
    df["revenue"] = df["quantity"] * df["price"]

    # Calculate total revenue per city
    summary = (
        df.groupby("city", as_index=False)["revenue"]
        .sum()
        .rename(columns={"revenue": "total_revenue"})
        .sort_values("total_revenue", ascending=False)
    )

    
    # Convert order_date to datetime (YYYY-MM-DD)
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        format="%Y-%m-%d"
    )

    # Get the latest order date
    latest_order_date = df["order_date"].max()

    # Generate report filename
    date_str = latest_order_date.strftime("%Y-%m-%d")
    output_key = f"reports/city_revenue_summary_{date_str}.csv"

    # Convert DataFrame to CSV
    csv_buffer = io.StringIO()
    summary.to_csv(
        csv_buffer,
        index=False,
        float_format="%.2f"
    )

    # Save summary to S3
    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=csv_buffer.getvalue().encode("utf-8"),
        ContentType="text/csv"
    )

    print(f"Report generated: s3://{bucket}/{output_key}")
    print(summary.to_string(index=False))

    return {
        "statusCode": 200,
        "body": f"Report successfully saved to {output_key}"
    }
