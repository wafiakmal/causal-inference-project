"""This file is the pre-processing of the data files in the source_data folder."""

############### Set-up and imports ###############
import pandas as pd
import numpy as np
import calendar
import datetime
import glob


############### Functions ###############
def year_calc(in_date, state):

    """Function to calculate number of days until the end of the year

    Parameters
    ----------
    in_date : datetime
        The date to calculate the days until the end of the year

    state : str
        The state to calculate the days until the end of the year

    Returns
    -------
    days_out : int
        The number of days until the end of the year
    """

    # calculate the year
    in_year = in_date.year

    # if the state is "texas" then use 31 AUG as the end of the year
    if state == "texas":

        # if the date is after 31 AUG then use 31 AUG of the next year
        if in_date > pd.Timestamp(year=in_year, month=8, day=31):

            # calculate days from 31 AUG of the next year
            days_out = (pd.Timestamp(year=in_year + 1, month=8, day=31) - in_date).days

        else:

            # calculate days from 31 AUG of the in year
            days_out = (pd.Timestamp(year=in_year, month=8, day=31) - in_date).days

    else:

        # if the in date is greater than 30 JUN then use 30 JUN of the next year
        if in_date > pd.Timestamp(year=in_year, month=6, day=30):

            # calculate days from 30 JUN of the next year
            days_out = (pd.Timestamp(year=in_year + 1, month=6, day=30) - in_date).days

        else:

            # calculate days from 30 JUN of the in year
            days_out = (pd.Timestamp(year=in_year, month=6, day=30) - in_date).days

    return days_out


def quarter_calc(in_date, state):

    """Function to calculate the number of days until the end of the quarter

    Parameters
    ----------
    in_date : datetime
        The date to calculate the days until the end of the quarter

    state : str
        The state to calculate the days until the end of the quarter

    Returns
    -------
    days_out : int
        The number of days until the end of the quarter

    qtr_out : int
        The quarter number
    """

    # get the in year
    in_year = in_date.year

    # get the in month
    in_month = in_date.month

    # get the in date
    in_day = in_date.day

    # separate logic for texas - year end is 31 AUG
    if state == "texas":

        # Get quarter one
        if in_month in [9, 10, 11]:

            # calculate days from 30 NOV of the in year
            days_out = (pd.Timestamp(year=in_year, month=11, day=30) - in_date).days

            qtr_out = 1

        # Get quarter two
        elif in_month == 12:

            # calculate days from 1 MAR of the next year minus one day
            days_out = (
                pd.Timestamp(year=in_year + 1, month=3, day=1) - in_date
            ).days - 1

            qtr_out = 2

        # Get quarter two
        elif in_month in [1, 2]:

            # calculate days from 1 MAR of the in year minus one day
            days_out = (pd.Timestamp(year=in_year, month=3, day=1) - in_date).days - 1

            qtr_out = 2

        # Get quarter three
        elif in_month in [3, 4, 5]:

            # calculate days from 31 MAY of the in year
            days_out = (pd.Timestamp(year=in_year, month=5, day=31) - in_date).days

            qtr_out = 3

        # Get quarter four
        elif in_month in [6, 7, 8]:

            # calculate days from 31 AUG of the in year
            days_out = (pd.Timestamp(year=in_year, month=8, day=31) - in_date).days

            qtr_out = 4

    # separate logic for all other states - year end is 30 JUN
    else:

        # Get quarter one
        if in_month in [7, 8, 9]:

            # calculate days from 30 SEP of the in year
            days_out = (pd.Timestamp(year=in_year, month=9, day=30) - in_date).days

            qtr_out = 1

        # Get quarter two
        elif in_month in [10, 11, 12]:

            # calculate days from 31 DEC of the in year
            days_out = (pd.Timestamp(year=in_year, month=12, day=31) - in_date).days

            qtr_out = 2

        # Get quarter three
        elif in_month in [1, 2, 3]:

            # calculate days from 31 MAR of the in year
            days_out = (pd.Timestamp(year=in_year, month=3, day=31) - in_date).days

            qtr_out = 3

        # Get quarter four
        elif in_month in [4, 5, 6]:

            # calculate days from 30 JUN of the in year
            days_out = (pd.Timestamp(year=in_year, month=6, day=30) - in_date).days

            qtr_out = 4

    return days_out, qtr_out


def data_process():

    """Function to process data

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # Set the working directory
    folder = "../00_source_data/"

    # Create a list of the files in the folder
    files = glob.glob(folder + "*.csv")

    # Make a base dataframe
    final_df = pd.DataFrame()

    # Loop through the csv files in the folder
    for file in files:

        print(f"Reading {file} ({files.index(file) + 1} of {len(files)})")

        # read the csv files
        base_df = pd.read_csv(
            file,
            usecols=[
                "date",
                "citation_issued",
            ],
        )

        # correct isues in the citation_issued column by replacing NA with 0 - fixes 3x St Paul values
        base_df["citation_issued"] = base_df["citation_issued"].fillna(0)

        # convert to boolean
        base_df["citation_issued"] = base_df["citation_issued"].astype(bool)

        # drop na rows if less than 5
        if base_df.isna().sum().sum() < 5:
            base_df.dropna(inplace=True)

        assert base_df.isna().sum().sum() == 0, "There are still missing values"

        # convert the date and time columns to datetime
        base_df["date"] = pd.to_datetime(base_df["date"])

        # create a column for the day of the week
        base_df["day_of_week"] = base_df["date"].dt.dayofweek + 1

        # make a column that we'll sum later
        base_df["total_activity"] = 1

        # groupby the date column
        group_df = (
            base_df.groupby("date")
            .agg(
                {
                    "total_activity": "sum",
                    "citation_issued": "sum",
                    "day_of_week": "first",
                }
            )
            .copy()
        )

        # assert we didn't lose anything
        assert (
            group_df["total_activity"].sum() == base_df["total_activity"].sum()
        ), "We lost some data"

        # add a city and state from the file name
        group_df["city"] = file.split("_")[3]
        group_df["state"] = file.split("_")[2].split("/")[1]

        # concat the base_df to the final_df
        final_df = pd.concat([final_df, group_df])

        # Add a column for the month
        final_df["month"] = final_df.index.month

        # Add a column to the final_df to count days until end of month
        final_df["days_end_month"] = final_df.index.days_in_month - final_df.index.day

        # Add a column for the year
        final_df["year"] = final_df.index.year

        # Add a column to the final_df to count days until end of year
        for i in range(len(final_df)):

            # call the function to get the days to the end of the year
            days_to_year = year_calc(final_df.index[i], final_df.state[i])

            # add the value to the dataframe
            final_df.loc[final_df.index[i], "days_end_year"] = days_to_year

        # Add a column for days to the end of the quarter
        for i in range(len(final_df)):

            # run the function to get the days to the end of the quarter
            days_to_qtr, qtr = quarter_calc(final_df.index[i], final_df.state[i])

            # add the value to the dataframe
            final_df.loc[final_df.index[i], "days_end_quarter"] = days_to_qtr

            # add the value to the dataframe
            final_df.loc[final_df.index[i], "quarter"] = qtr

        # calculate the citation rate
        final_df["citation_rate"] = (
            final_df["citation_issued"] / final_df["total_activity"]
        )

        # flag for end of month (5 days or less)
        final_df["end_of_month"] = final_df["days_end_month"] <= 5

        # flag for end of quarter (10 days or less)
        final_df["end_of_quarter"] = final_df["days_end_quarter"] <= 10

        # flag for end of year (20 days or less)
        final_df["end_of_year"] = final_df["days_end_year"] <= 15

        # reorder the columns
        final_df = final_df[
            [
                "total_activity",
                "citation_issued",
                "citation_rate",
                "day_of_week",
                "month",
                "days_end_month",
                "end_of_month",
                "year",
                "days_end_year",
                "end_of_year",
                "quarter",
                "days_end_quarter",
                "end_of_quarter",
                "city",
                "state",
            ]
        ]

    # save the final_df to a csv file
    final_df.to_csv("../05_clean_data/processed_data_revised.csv")

    pass


if __name__ == "__main__":
    data_process()
