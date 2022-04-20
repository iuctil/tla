
---
title: "NETCCN deployment information for Scurry County (fips:48415)"
description: "NETCCN deployment"
weight: 100
toc: false
plotly: true
---

For this county, population demographic data is compared to state and national values.

| | Scurry County | Texas | U.S. |
| ----------- | ----------- | ----------- | -------- |
| Population | 17,239 | 27,885,195 | 322,903,030 |
| Percentage of Population below poverty | 12% | 15% | 14% |
| Percentage of Unemployed Population | 2% | 3% | 3% |
| Percentage of Uninsured Population | 14% | 17% | 9% |
| Percentage of Population with Disability | 13% | 11% | 12% |
| Percentage of Population Aged 65 and older | 15% | 12% | 15% |
| Percentage of Population Aged 17 and younger | 25% | 26% | 23% |

  

For this county, COVID-19 community transmission levels are depicted as part of understanding demand for critical care requirements in the region.

{{<plotly json="netccn/48415/covid_transmission.plotly.json" height="400px">}}


TODO - describe covid cases plot below

  {{<plotly json="netccn/48415/covid_cases.plotly.json" height="400px">}}


For the following hospitals, average number of COVID-19 patients at a start date, with weekly changes shown in a waterfall chart, with increases depicted in green and decreases in red.  Total COVID-19 patients at the end of the selected period range is depicted in blue.  The following NETCCN deployment dates are noted as available, "week of the request", "week of the start of the deployment".  Purpose of graph is understanding the critical care conditions at the point in time when hospitals requested support and the length of time before the deployment started, including the change in conditions over the period.

{{<plotly json="netccn/48415/hospital.451384.plotly.json" height="400px">}}
