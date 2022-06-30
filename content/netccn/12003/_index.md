
---
title: "NETCCN deployment information for Baker County (fips:12003)"
description: "NETCCN deployment"
weight: 100
toc: false
plotly: true
---

For this county, population demographic data is compared to state and national values.

| | Baker County | Florida | U.S. |
| ----------- | ----------- | ----------- | -------- |
| Population | 27,785 | 20,598,139 | 322,903,030 |
| Percentage of Population below poverty | 13% | 14% | 14% |
| Percentage of Unemployed Population | 2% | 3% | 3% |
| Percentage of Uninsured Population | 11% | 13% | 9% |
| Percentage of Population with Disability | 16% | 13% | 12% |
| Percentage of Population Aged 65 and older | 14% | 20% | 15% |
| Percentage of Population Aged 17 and younger | 24% | 20% | 23% |

  

For this county, COVID-19 community transmission levels are depicted as part of understanding demand for critical care requirements in the region.

{{<plotly json="netccn/12003/covid_transmission.plotly.json" height="400px">}}


TODO - describe covid cases plot below

  {{<plotly json="netccn/12003/covid_cases.plotly.json" height="400px">}}


For the following hospitals, average number of COVID-19 patients at a start date, with weekly changes shown in a waterfall chart, with increases depicted in green and decreases in red.  Total COVID-19 patients at the end of the selected period range is depicted in blue.  The following NETCCN deployment dates are noted as available, "week of the request", "week of the start of the deployment".  Purpose of graph is understanding the critical care conditions at the point in time when hospitals requested support and the length of time before the deployment started, including the change in conditions over the period.

{{<plotly json="netccn/12003/hospital.100134.plotly.json" height="400px">}}
