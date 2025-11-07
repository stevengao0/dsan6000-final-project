"""
project_starter_script.py

DSAN 6000 Final Project
Topic: Reddit & the Cost of Living Crisis (Jan 2022–Mar 2023)

This script:
- Initializes a local Spark session
- Loads Reddit data (JSON)
- Prints schema and basic stats
- Produces a small CSV summary for Milestone 1 verification

"""

import os
from pathlib import Path
from pyspark.sql import SparkSession, functions as F

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = REPO_ROOT / "data" / "raw"
DATA_PROCESSED = REPO_ROOT / "data" / "processed"
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# Local data
SUBMISSIONS_PATH = DATA_RAW / "submissions-sample.json"
COMMENTS_PATH = DATA_RAW / "comments-sample.json"


def get_spark_session(app_name="dsan6000-local-eda"):
    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .getOrCreate()
    )
    return spark


def load_sample_json(spark, path, n=10000):
    if not path.exists():
        raise FileNotFoundError(f"Cannot find file: {path}")
    df = spark.read.json(str(path))
    return df.limit(n)


def main():
    spark = get_spark_session()

    print("\n=== Loading submissions sample ===")
    submissions_df = load_sample_json(spark, SUBMISSIONS_PATH)
    submissions_df.printSchema()
    print(f"Submissions sample rows: {submissions_df.count()}")

    print("\n=== Loading comments sample ===")
    comments_df = load_sample_json(spark, COMMENTS_PATH)
    comments_df.printSchema()
    print(f"Comments sample rows: {comments_df.count()}")

    # Basic summary: top subreddits in submissions
    if "subreddit" in submissions_df.columns:
        top_subs = (
            submissions_df.groupBy("subreddit")
            .count()
            .orderBy(F.desc("count"))
            .limit(20)
        )
        out_path = DATA_PROCESSED / "submissions_top20_subreddits.csv"
        top_subs.toPandas().to_csv(out_path, index=False)
        print(f"\n✅ Wrote top 20 subreddits summary to: {out_path}")

    print("\nStarter script ran successfully.")
    spark.stop()

if __name__ == "__main__":
    main()
