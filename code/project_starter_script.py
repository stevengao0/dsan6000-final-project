"""
project_starter_script.py

DSAN 6000 Final Project
Topic: Reddit & the Cost of Living Crisis
Authors: Jiachen Gao, Zihao Huang, Chaowei Wang
This script:
- Initializes a Spark session
- Loads Reddit sample data (JSON) from data/raw
- Prints schema and basic stats
- Produces a small CSV summary for Milestone 1 verification
- Exposes helper functions for use in project_eda.ipynb
"""

from pathlib import Path
from pyspark.sql import SparkSession, functions as F

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = REPO_ROOT / "data" / "raw"
DATA_PROCESSED = REPO_ROOT / "data" / "processed"
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

SUBMISSIONS_PATH = DATA_RAW / "submissions-sample.json"
COMMENTS_PATH = DATA_RAW / "comments-sample.json"


def get_spark_session(app_name: str = "dsan6000-local-eda") -> SparkSession:
    """Create or get a SparkSession."""
    builder = SparkSession.builder.appName(app_name)
    # Uncomment for local-only testing:
    # builder = builder.master("local[*]")
    spark = builder.getOrCreate()
    return spark


def load_sample_json(spark: SparkSession, path: Path, n: int = 10000):
    """Load a JSON sample file from data/raw."""
    if not path.exists():
        raise FileNotFoundError(f"Cannot find file: {path}")
    return spark.read.json(str(path)).limit(n)


def load_submissions_sample(spark: SparkSession, n: int = 10000):
    return load_sample_json(spark, SUBMISSIONS_PATH, n=n)


def load_comments_sample(spark: SparkSession, n: int = 10000):
    return load_sample_json(spark, COMMENTS_PATH, n=n)


def load_sample_data(spark: SparkSession, n: int = 10000):
    """Load both submissions and comments sample DataFrames."""
    return load_submissions_sample(spark, n), load_comments_sample(spark, n)


def main():
    """Run a quick sanity check for Milestone 1."""
    spark = get_spark_session()

    print("\n=== Loading submissions sample ===")
    submissions_df = load_submissions_sample(spark)
    submissions_df.printSchema()
    print(f"Submissions sample rows: {submissions_df.count()}")

    print("\n=== Loading comments sample ===")
    comments_df = load_comments_sample(spark)
    comments_df.printSchema()
    print(f"Comments sample rows: {comments_df.count()}")

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
