
---
title: "NETCCN deployment information for Washington County (fips:27163)"
description: "NETCCN deployment"
weight: 100
toc: false
plotly: true
---

For this county, population demographic data is compared to state and national values.

| | Washington County | Minnesota | U.S. |
| ----------- | ----------- | ----------- | -------- |
| Population | 253,317 | 5,527,358 | 322,903,030 |
| Percentage of Population below poverty | 5% | 10% | 14% |
| Percentage of Unemployed Population | 2% | 2% | 3% |
| Percentage of Uninsured Population | 3% | 5% | 9% |
| Percentage of Population with Disability | 9% | 11% | 12% |
| Percentage of Population Aged 65 and older | 14% | 15% | 15% |
| Percentage of Population Aged 17 and younger | 25% | 23% | 23% |

  

For this county, COVID-19 community transmission levels are depicted as part of understanding demand for critical care requirements in the region.

{{<plotly json="netccn/27163/covid_transmission.plotly.json" height="400px">}}


TODO - describe covid cases plot below

  {{<plotly json="netccn/27163/covid_cases.plotly.json" height="400px">}}


For the following hospitals, average number of COVID-19 patients at a start date, with weekly changes shown in a waterfall chart, with increases depicted in green and decreases in red.  Total COVID-19 patients at the end of the selected period range is depicted in blue.  The following NETCCN deployment dates are noted as available, "week of the request", "week of the start of the deployment".  Purpose of graph is understanding the critical care conditions at the point in time when hospitals requested support and the length of time before the deployment started, including the change in conditions over the period.

{{<plotly json="netccn/27163/hospital.240066.plotly.json" height="400px">}}
