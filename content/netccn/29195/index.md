
---
title: "NETCCN deployment information for Saline County (fips:29195)"
description: "NETCCN deployment"
weight: 100
toc: false
plotly: true
---

For this county, population demographic data is compared to state and national values.

| | Saline County | Missouri | U.S. |
| ----------- | ----------- | ----------- | -------- |
| Population | 23,102 | 6,090,062 | 322,903,030 |
| Percentage of Population below poverty | 15% | 14% | 14% |
| Percentage of Unemployed Population | 2% | 3% | 3% |
| Percentage of Uninsured Population | 9% | 10% | 9% |
| Percentage of Population with Disability | 17% | 14% | 12% |
| Percentage of Population Aged 65 and older | 18% | 16% | 15% |
| Percentage of Population Aged 17 and younger | 23% | 23% | 23% |

  

For this county, COVID-19 community transmission levels are depicted as part of understanding demand for critical care requirements in the region.

{{<plotly json="netccn/29195/covid_transmission.plotly.json" height="400px">}}


TODO - describe covid cases plot below

  {{<plotly json="netccn/29195/covid_cases.plotly.json" height="400px">}}


For the following hospitals, average number of COVID-19 patients at a start date, with weekly changes shown in a waterfall chart, with increases depicted in green and decreases in red.  Total COVID-19 patients at the end of the selected period range is depicted in blue.  The following NETCCN deployment dates are noted as available, "week of the request", "week of the start of the deployment".  Purpose of graph is understanding the critical care conditions at the point in time when hospitals requested support and the length of time before the deployment started, including the change in conditions over the period.

{{<plotly json="netccn/29195/hospital.260142.plotly.json" height="400px">}}
