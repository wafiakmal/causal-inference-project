"""File for data visualization tools."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


def plot_time_period(city, period, data, metric="citation_issued"):
    """
    Visualize the aggregated data for a given city and time period.

    Parameters
    ----------
    city: str
        The city name to visualize

    period: str
        The time period to visualize. Can be one of month, quarter, or year.

    data: pd.DataFrame
        The dataframe to visualize. Must have a column named "city."

    metric: str
        The metric to visualize. Must be a column in the dataframe.
            Default is "citation_issued." Can be set to "citation_rate."

    Returns
    -------
    None
    """
    # Filter the data by city
    city_data = data[data["city"] == city]

    if period == "month":
        i = 1

        # make a plot object
        plt.figure(figsize=((10, 25)))
        plt.subplots_adjust(hspace=0.75)

        # unique years
        years = city_data["year"].unique()

        # make a subplot for each year
        for year in years:
            # Filter the data by year
            year_data = city_data[city_data["year"] == year]

            # make a subplot
            ax = plt.subplot(8, 2, i)

            # plot a line for each month
            for month in year_data["month"].unique():
                # Filter the data by month
                month_data = year_data[year_data["month"] == month]

                # Plot the data
                ax.plot(
                    month_data["days_end_month"],
                    month_data[metric],
                    alpha=0.2,
                    color="grey",
                )

            # Plot the mean
            ax.plot(
                year_data.groupby("days_end_month")[metric].mean(),
                label="Mean",
                color="red",
            )

            # invert the x axis
            ax.invert_xaxis()

            # Set the title
            ax.set_title(f"{city.upper()} Citations for {year}")

            # Set the x axis label
            ax.set_xlabel("Days to end of month")

            # Set the y axis label
            ax.set_ylabel("Citations Issued")

            # Set the legend
            ax.legend()

            i += 1

        # Show the plot
        plt.show()

    if period == "quarter":
        i = 1

        # make a plot object
        plt.figure(figsize=((10, 25)))
        plt.subplots_adjust(hspace=0.75)

        # unique years
        years = city_data["year"].unique()

        # subplot sizes
        nrows = 2

        # make a subplot for each year
        for year in years:
            # Filter the data by year
            year_data = city_data[city_data["year"] == year]

            # make a subplot
            ax = plt.subplot(8, 2, i)

            # plot a line for each month
            for quarter in year_data["quarter"].unique():
                # Filter the data by month
                quarter_data = year_data[year_data["quarter"] == quarter]

                # Plot the data
                ax.plot(
                    quarter_data["days_end_quarter"],
                    quarter_data[metric],
                    alpha=0.2,
                    color="grey",
                )

            # Plot the mean
            ax.plot(
                year_data.groupby("days_end_quarter")[metric].mean(),
                label="Mean",
                color="red",
            )

            # invert the x axis
            ax.invert_xaxis()

            # Set the title
            ax.set_title(f"{city.upper()} Citations for {year}")

            # Set the x axis label
            ax.set_xlabel("Days to end of quarter")

            # Set the y axis label
            ax.set_ylabel("Citations Issued")

            # Set the legend
            ax.legend()

            i += 1

        # Show the plot
        plt.show()

    if period == "year":
        # make a plot object
        plt.figure(figsize=((8, 8)))

        # Plot the data
        plt.plot(
            city_data["days_end_year"],
            city_data[metric],
            alpha=0.2,
            color="grey",
            label="year",
        )

        # Plot the mean
        plt.plot(
            city_data.groupby("days_end_year")[metric].mean(),
            label="Mean",
            color="red",
        )

        # invert the x axis
        plt.gca().invert_xaxis()

        # Set the title
        plt.title(f"{city.upper()} Citations by year")

        # Set the x axis label
        plt.xlabel("Days to end of year")

        # Set the y axis label
        plt.ylabel("Citations Issued")

        # Set the legend
        plt.legend()

        # Show the plot
        plt.show()


def target_days(city_name, df):
    """
    Initialize a dictionary to store the number of days in each month of year.

    Parameters
    ----------
    city_name : str
        The name of the city to be analyzed.
    df : pandas.DataFrame
        The dataframe containing the data to be analyzed.

    Returns
    -------
    days_dict : dict
        A dictionary containing the number of days in each month for each year.
    """
    # get the unique years of this_city
    city_df = df[df["city"] == city_name]
    years = city_df["year"].unique()
    years.sort()

    temp_dict = dict()
    # make a for loop to get the unique months of each year
    for year in years:
        months = np.arange(1, 13)
        temp_dict[year] = months

    days_dict = dict()
    # based on temp_dict, get the number of days for each month in each year
    for year in temp_dict.keys():
        temp_dict2 = dict()
        # get the number of days for each year
        days_year = (dt.date(year + 1, 1, 1) - dt.date(year, 1, 1)).days
        for month in temp_dict[year]:
            if month == 12:
                day_month = (dt.date(year + 1, 1, 1) - dt.date(year, 12, 1)).days
            else:
                day_month = (dt.date(year, month + 1, 1) - dt.date(year, month, 1)).days
            temp_dict2[month] = day_month
        days_dict[year] = days_year, temp_dict2
    return days_dict


def actual_days(city_name, df):
    """
    Initialize a dictionary to store the number of days in each month of year.

    Parameters
    ----------
    city_name : str
        The name of the city to be analyzed.
    df : pandas.DataFrame
        The dataframe containing the data to be analyzed.

    Returns
    -------
    days_dict : dict
        A dictionary containing the number of days in each month for each year.
    """
    city_df = df[(df["city"] == city_name) & (df["citation_issued"] != 0)]
    years = np.sort(city_df["year"].unique())

    temp_dict = dict()
    # make a for loop to get the unique months of each year
    for year in years:
        # get the unique months of this_city
        df_city_year = city_df[city_df["year"] == year]
        months = np.sort(df_city_year["month"].unique())
        temp_dict[year] = months

    actual_daysz = dict()
    # based on temp_dict, get the number of days for each month in each year
    for year in temp_dict.keys():
        temp_dict2 = dict()
        # groupby the data by year and get the unique counts of date column
        days_year = (
            city_df[city_df["year"] == year].groupby("year")["date"].nunique()
        ).to_dict()[year]
        for month in range(1, 13):
            # groupby year and month and get the unique counts of date column
            month_dict = (
                city_df[(city_df["year"] == year) & (city_df["month"] == month)]
                .groupby("month")["date"]
                .nunique()
            ).to_dict()
            temp_dict2[month] = month_dict.get(month, 0)
        actual_daysz[year] = days_year, temp_dict2
    return actual_daysz


def missing_days(city_name, df, option):
    """
    Get the missing days.

    Parameters
    ----------
    city_name : str
        The name of the city.
    df : pandas.DataFrame
        The data frame of the city.
    option : str
        The option of the missing days. It can be "year" or "month".

    Returns
    -------
    missing_days_dict : dict
        The dictionary of the missing days either based on year or month.
    """
    # get the target days
    target_days_dict = target_days(city_name, df)
    # get the actual days
    actual_days_dict = actual_days(city_name, df)
    # get the years of the city
    years = np.sort(df[df["city"] == city_name]["year"].unique())
    # initialize a dictionary to store the results
    missing_days_dict = dict()
    # loop through the years
    if option == "year":
        for year in years:
            # get the target days of the year
            target_days_year = target_days_dict[year][0]
            # get the actual days of the year
            actual_days_year = actual_days_dict[year][0]
            # check if the target days and actual days match
            if target_days_year != actual_days_year:
                missing_days_dict[year] = target_days_year - actual_days_year
    elif option == "month":
        for year in years:
            missing_days = dict()
            for month in actual_days_dict[year][1].keys():
                # get the target days of the year
                target_days_month = target_days_dict[year][1][month]
                # get the actual days of the year
                actual_days_month = actual_days_dict[year][1][month]
                # check if the target days and actual days match
                if target_days_month != actual_days_month:
                    missing_days[month] = target_days_month - actual_days_month
            missing_days_dict[year] = missing_days
        missing_days_dict = {k: v for k, v in missing_days_dict.items() if v}
    return missing_days_dict


def print_statement(city, year_miss_data, month_miss_data):
    """
    Print the missing data of the city.

    Parameters
    ----------
    city : str
        The name of the city.
    year_miss_data : dict
        The dictionary of the missing days based on year.
    month_miss_data : dict
        The dictionary of the missing days based on month.

    Returns
    -------
    str
        The print statement of the missing data.
    """
    print(f"Grouped by the year, the missing data of {city} are:")
    for year in year_miss_data.keys():
        print(f"Year-{year}: {year_miss_data[year]}")

    # loop through the missing_days_month and get the missing days
    print(f"\nGrouped by the month, the missing data of {city} are:")
    for year in month_miss_data.keys():
        print(f"\nYear-{year}:")
        for month in month_miss_data[year].keys():
            # use datetime to get the month name
            monthz = dt.date(1900, month, 1).strftime("%B")
            print(f"{monthz}: {month_miss_data[year][month]}")


def plot_missing(city_name, df, year_miss_data, month_miss_data, option):
    """
    Plot the missing days.

    Parameters
    ----------
    city_name : str
        The name of the city.
    df : pandas.DataFrame
        The data frame of the city.
    option : str
        The option of the missing days. It can be "year" or "month".

    Returns
    -------
    plot : matplotlib.pyplot
        The plot of the missing days.

    """
    if option == "year":
        target_days_dict = target_days(city_name, df)
        # make a plot of the missing_days_year, but keep all the years
        plt.figure(figsize=(10, 5))
        plt.bar(
            year_miss_data.keys(),
            year_miss_data.values(),
            color="gold",
            edgecolor="black",
            linewidth=1.2,
        )
        plt.title(f"Missing Days of {city_name.capitalize()} by year", fontsize=16)
        plt.xlabel("Year", fontsize=14)
        plt.ylabel("Missing Days", fontsize=14)
        plt.xticks(
            np.arange(
                min(target_days_dict.keys()),
                max(target_days_dict.keys()) + 1,
                1,
            )
        )
        plt.show()
    elif option == "month":
        # loop through the missing_days_month and get the missing days
        for year in month_miss_data.keys():
            plt.figure(figsize=(10, 5))
            plt.bar(
                month_miss_data[year].keys(),
                month_miss_data[year].values(),
                color="gold",
                edgecolor="black",
                linewidth=1.2,
            )
            plt.title(
                f"Missing days of {city_name.capitalize()} in {year} per " "Month",
                fontsize=16,
            )
            plt.xlabel("Month", fontsize=14)
            plt.ylabel("Missing Days", fontsize=14)
            plt.xticks(
                np.arange(
                    1,
                    12 + 1,
                    1,
                )
            )
            plt.yticks(
                np.arange(
                    0,
                    max(month_miss_data[year].values()) + 1,
                    1,
                )
            )
            plt.show()


def percent_missing(city, df, year_miss_data, month_miss_data):
    """
    Calculate the percentage of the missing data.

    Parameters
    ----------
    city : str
        The name of the city.
    df : pandas.DataFrame
        The data frame of the city.
    year_miss_data : dict
        The dictionary of the missing days based on year.
    month_miss_data : dict
        The dictionary of the missing days based on month.

    Returns
    -------
    str
        The print statement of the percentage of the missing data.
    """
    # calculate the total missing days and compare it with the total days
    total_missing_days = 0
    for year in year_miss_data.keys():
        total_missing_days += year_miss_data[year]
    total_days = 0
    for year in target_days(city, df).keys():
        total_days += target_days(city, df)[year][0]
    print(
        f"The total missing days of {city} are {total_missing_days} out of "
        f"{total_days} days, or "
        f"{round(total_missing_days/total_days*100, 2)}%."
    )
    # calculate the highest month with missing data
    highest_month = 0
    year = 0
    month = 0
    for year in month_miss_data.keys():
        for month in month_miss_data[year].keys():
            if month_miss_data[year][month] > highest_month:
                highest_month = month_miss_data[year][month]
                month = month
                year = year
    print(
        f"The highest month with missing data is {highest_month} days that "
        f"happen on the month {month} in {year}."
    )
