#!/usr/bin/env python3

import argparse
import datetime
import boto3
import sys

client = boto3.client('s3')
s3 = boto3.resource('s3')


def cli_args():
    parser = argparse.ArgumentParser(
        description="""
            AWS S3 bucket explorer open beta v1
            """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-l",
        "--list-buckets",
        help=("List available buckets from all regions"),
        action="store_true",
    ),
    parser.add_argument(
        "-a",
        "--list-contents",
        action="store_true",
        help=("List contents from all buckets ")
    )
    args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    return args


def all_buckets():
    all_bck = [bucket.name for bucket in s3.buckets.all()]
    bucket_name = all_bck
    return bucket_name


def get_contents():
    for buck in all_buckets():
        for key in client.list_objects(Bucket=buck)['Contents']:
            # return {"Bucket Name": key["Key"], "LastModified": key["LastModified"]}
            print("Name: "+key["Key"]+"\nLastModified: " +
                  str(key["LastModified"])+"\nStorageClass: "+key["StorageClass"]+"\nSize: "+str(round(float(key["Size"]/1024/1024), 3))+"MB\n")


def main():
    args = cli_args()
    if args.list_buckets:
        print("\n".join(all_buckets()))
    if args.list_contents:
        get_contents()
    # print(get_contents())


if __name__ == "__main__":
    main()
