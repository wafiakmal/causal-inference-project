# Analyzing the Impact of Reporting Periods on Law Enforcement Officer Behavior

*Andrew Kroening, Chloe (Ke) Liu, Wafiakmal Miftah, Jenny (Yiran) Shen*

*Spring 2023*

## Documents

The project proposal can [be found here.](https://github.com/MIDS-at-Duke/unifying-data-science-2023-project-team7/blob/main/40_docs/ISD701%20Proposal.pdf)

The final project report can [be found here.](https://github.com/MIDS-at-Duke/unifying-data-science-2023-project-team7/blob/main/40_docs/IDS701_Final_Report.pdf) 

## Project Outline

This report examines whether local law enforcement officers increase ticketing activity in response to financial incentives or pressures as a reporting deadline approaches. Using data from the Stanford Open Policing Project for 15 US cities spanning 20 years, the analysis finds little to no evidence that officers change their ticketing behavior, regardless of the legal status of quotas in the state. However, two cities, Cincinnati, Ohio, and Aurora, Colorado, showed significant upward trends at the end of reporting periods, indicating the probable existence of policing quotas. San Francisco, California, displayed a puzzling trend with a decrease in citations as the fiscal year drew close. The report highlights limitations of the analysis and the need for further investigation into the impact of budgetary practices on policing behavior.

## Data

The data for this analysis was obtained from the [Stanford Open Policing Project at this link](https://openpolicing.stanford.edu/data/), a comprehensive source of information on policing in the United States. We selected data from cities that provided detailed information on police incidents and outcomes, with a time span ranging from 2000 to 2019. We focused on the city level to obtain the most detailed data possible, and excluded the month of December due to observed changes in law enforcement activity likely related to the holiday season. The final dataset was processed and prepared for analysis, and any transformation will be saved to [the cleaned data directory](https://github.com/MIDS-at-Duke/unifying-data-science-2023-project-team7/tree/main/05_clean_data)

<img src="/40_docs/city_timeline.png" width="800"/>

## Summary of Analysis Findings
<p align="center">
  <img src="/40_docs/city_table.png" width="500"/>
</p>

In our analysis of fifteen cities with the best available data, we employed various analytical techniques such as Exploratory Analysis, Fixed Effects Regression, and LOESS to detect evidence of explicit or implicit policing for profit. Our findings revealed that Cincinnati, OH and Aurora, CO exhibited significant positive movement in the number of citations issued as reporting cut-offs approached, indicating a potential influence on officers' behavior. However, these trends were not widespread enough to be generalized across multiple jurisdictions, and practical significance varied. Surprisingly, nearly half of the cities showed a negative movement in citations, with most deemed practically insignificant except for San Francisco. Detailed results can be found above.


