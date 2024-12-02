import pandas as pd
import numpy as np
import random
import datetime
from functools import wraps

# import duckdb

# Set parameters
seed = 868823
n_ppl = 3_000_000
n_tests = 15 * n_ppl
n_ppl_t = int(0.3 * n_ppl)
n_transactions = 100 * n_ppl_t
n_shops = 50_000


def random_timestamps(start_date_str, end_date_str, num_timestamps, seed=seed):
    """
    Return a list of 'num_timestamps' random datetime objects between
    'start_date_str' and 'end_date_str' (inclusive).

    Parameters
    ----------
    start_date_str : str
        The start date in 'YYYY-MM-DD' format.

    end_date_str : str
        The end date in 'YYYY-MM-DD' format.

    num_timestamps : int
        The number of random timestamps to generate.

    seed : int, optional
        The random seed to use. If not provided, use the default random seed.

    Returns
    -------
    list of datetime
        A list of 'num_timestamps' random datetime objects between
        'start_date_str' and 'end_date_str' (inclusive).
    """
    random.seed(seed)
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    timestamps = [
        start_timestamp + random.randint(0, end_timestamp - start_timestamp)
        for _ in range(num_timestamps)
    ]
    return [datetime.datetime.fromtimestamp(ts) for ts in timestamps]


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print(
            f"Function {func.__name__} took {str(end_time - start_time)} seconds to run."
        )
        return result

    return wrapper


@timeit
def transaction_generator(
    n_transactions=n_transactions, seed=seed, n_ppl_t=n_ppl_t, n_shops=n_shops
):
    transactions = pd.DataFrame(
        random_timestamps("2022-01-01", "2022-12-31", n_transactions, seed=seed),
        columns=["transaction_time"],
    )
    np.random.seed(seed)
    transactions["id"] = np.random.randint(1, n_ppl_t, size=transactions.shape[0])
    transactions["shop"] = np.random.randint(1, n_shops, size=transactions.shape[0])
    transactions.to_parquet("data/transactions.parquet")
    transactions.to_csv("data/transactions.csv", index=False)


@timeit
def test_generator(n_tests=n_tests, seed=seed, n_ppl=n_ppl):
    tests = pd.DataFrame(
        random_timestamps("2022-01-01", "2022-12-31", n_tests, seed=seed),
        columns=["test_time"],
    )
    np.random.seed(seed)
    tests["id"] = np.random.randint(1, n_ppl, size=tests.shape[0])
    tests["positive"] = 1 * (np.random.uniform(size=tests.shape[0]) < 0.08)
    tests.to_parquet("data/tests.parquet")
    tests.to_csv("data/tests.csv", index=False)


# @timeit
# def id_chara_generator():
#     ids = duckdb.sql("Select distinct id from read_parquet('data/tests.parquet')").df()
#     ids["income"] = np.random.lognormal(5, 1, size=ids.shape[0])
#     ids["age"] = np.random.randint(18, 90, size=ids.shape[0])
#     ids.to_parquet("data/id_chara.parquet")
#     ids.to_csv("data/id_chara.csv", index=False)


if __name__ == "__main__":

    # Generate transaction dataframe
    transaction_generator()
    # Generate tests dataframe
    # test_generator()
    # Generate id_characteristics dataframe
    # id_chara_generator()