---
title: "Infrastructure in a Disaster"
description: "Blogpost #1 by August Reed"
lead: "Hurricane Maria Exposed a Need for Reducing Cascading Failures in Critical Infrastructure"
date: 2021-03-01T12:00:00.000Z
lastmod: 2021-03-01T12:00:00.000Z
draft: false
contributors: ["August Reed"]
menu:
  bplp:
    parent: "insights"
weight: 140
toc: true
---
 
*This article was originally posted at [https://sciencenode.org/feature/Infrastructure%20in%20a%20disaster.php](https://sciencenode.org/feature/Infrastructure%20in%20a%20disaster.php)*

&nbsp;  

From [2017’s Hurricane Maria](https://www.washingtonpost.com/graphics/2017/national/puerto-rico-life-without-power/) to a recent [swarm of severe earthquakes](https://eos.org/articles/rare-earthquake-swarm-strikes-puerto-rico), Puerto Rico has experienced catastrophe after catastrophe in recent years.

Resulting damages to the island’s utility infrastructures triggered [days-](https://eos.org/articles/rare-earthquake-swarm-strikes-puerto-rico) to [months-long](https://www.washingtonpost.com/graphics/2017/national/puerto-rico-life-without-power/) black outs. Following Hurricane Maria, electricity-dependent services — like water sanitation and some medical treatments — [failed](https://www.vox.com/science-and-health/2017/10/18/16489180/water-crisis-puerto-rico-hurricane-maria), causing an island-wide humanitarian crisis and [thousands of deaths](https://law.lclark.edu/live/blogs/132-the-effects-of-natural-disasters-on-energy).

As high winds and floods damaged various utility structures, a cascade of utility failures rippled throughout Puerto Rico’s communities, crippling the island and [impairing recovery efforts](https://www.vox.com/science-and-health/2017/9/26/16365994/hurricane-maria-2017-puerto-rico-san-juan-humanitarian-disaster-electricty-fuel-flights-facts) — a pattern common after large natural disasters.

Based on lessons learned while providing emergency response and recovery support over nearly two years in Puerto Rico, researchers at the [Argonne National Laboratory](https://www.anl.gov/) have developed an [AI model](https://www.anl.gov/article/advanced-tools-reveal-critical-infrastructure-connections-and-help-mitigate-disasters) that uses artificial intelligence and game theory to optimize infrastructures for resilience.

The model assesses which structures in a network cause the greatest cascades of utility failures when damaged, in order to facilitate better infrastructure design and recovery practices.

### How Utility Systems Fail and Cripple Communities

The AI project is informed by earlier work in Puerto Rico. Joining the island’s recovery efforts in 2017, researcher [Joshua Bergerson](https://www.anl.gov/profile/joshua-david-bergerson) and his colleagues manually collected data on hundreds of the island’s utility interdependencies by meeting with infrastructure owners and operators.

However, these manual data collection activities proved prohibitively time-consuming. So, the research team developed a tool to estimate dependency connections between utilities and assess how failures could cascade across these connections by turning assets on and off and observing the cascading impacts in their model.

Their principal goal was to assess how cascading failures occur. For example, take the island’s electricity-dependent water treatment plants.

The electricity flows out of large power plants, across transmission lines, and into neighborhood substations, where it then passes into nearby water treatment plants. If a substation fails, so too would the connected plants.

But by introducing redundancies — for example, by connecting key plants to two substations — utility equipment can remain operable even after partial network disruptions.

“Redundancy means essentially having more than one critical path, in order to decrease the potential to lose [power]” to critical buildings, like hospitals and water treatment plants, says Bergerson.

Planning creates resilient systems. This is an important feature for utility infrastructures in natural disaster-prone areas, like Puerto Rico, Japan, and China; but it is also becoming [increasingly important](https://law.lclark.edu/live/blogs/132-the-effects-of-natural-disasters-on-energy) globally, as changes in climate increase the [severity and frequency](https://www.phi.org/press/climate-change-is-making-natural-disasters-worse-and-more-likely-how-do-we-protect-the-most-vulnerable/) of hurricanes and floods.

### Reducing Crisis Timelines 

Uncovering system dependencies can also better inform immediate restoration decisions after failures.

In the urgent days to months after disaster strikes, decisions about which infrastructure repairs deserve priority can have immediate and long-term effects on citizens’ economic, physical, and [mental](https://www.theguardian.com/world/2019/apr/26/hurricane-maria-puerto-rico-youth-mental-health-study-report#:~:text=Hurricane%20Maria's%20lasting%20impact%20on%20Puerto%20Rico's%20children%20revealed%20in%20report,-This%20article%20is&text=47.5%25%20of%20children's%20family's%20homes,youth%20were%20forced%20to%20evacuate) well-being. These timely decisions require knowledge of utility dependencies: Which equipment, if restored, will have the greatest overall net effect? And how can the greatest number of services be restored in the fastest way possible? 

Unfortunately, data on these dependencies is not available in public data sets, nor is it routinely collected.

“In terms of an individual system, there are a lot of data sources that talk about electric power systems, right? They’ll show you where substations are located, where power plants are located, and where different power lines are,” says Bergerson. “So understanding a single system isn't much of an issue… It's really how those systems are connected across different types of systems — that's the information that's generally not publicly available.”

“We have many projects assessing critical infrastructure that require us to go essentially knock on doors in order to talk to people who do know that information. But, unfortunately, the information is really spread out and requires us to talk to a lot of people in order to get a handful of pieces of information — as opposed to some bigger national data sets that document overall infrastructure systems.” 

It’s slow work. And the arduous data collection process limits the studies in size. But their AI model is increasing that efficiency: “It's allowing us to look at significantly larger overall networks. Instead of being able to look at maybe the size of a city, we can now look at the size of a state,” says Bergerson.

It maps optimal connections, designing intentional systems that keep the most critical infrastructure running. Right now, it’s useful in infrastructure planning and development. And in the future, the team hopes to expand the model’s utility to restoration and recovery efforts:

“So, I personally am very excited about getting to a point where we can potentially inform, in the future, emergency response — so moving from months or years of analysis to days or even potentially hours of analysis.”

Puerto Rico’s lingering crisis, [still visible three years later](https://www.nbcnews.com/news/latino/puerto-rico-sees-more-pain-little-progress-three-years-after-n1240513), exemplifies the vulnerability and cruciality of utility infrastructures — and the dangers of slow repair rates which draw out temporarily poor living conditions.

It is these aftereffects, and the island’s [infrastructure failures](https://www.nejm.org/doi/full/10.1056/NEJMsa1803972?query=featured_home), which are widely cited as the cause for much of the hurricane’s impact on mortality. This statistic aligns with the common finding that, [with many natural disasters](https://www.nature.com/articles/d41586-019-00442-0), a large portion of the deaths have [“indirect” causes](https://www.cambridge.org/core/journals/disaster-medicine-and-public-health-preparedness/article/measuring-the-true-human-cost-of-natural-disasters/5FEDB8D5C4EACCB41433DDB1B961C565) — many power related.

A tool which informs recovery efforts based on the impact of electrical infrastructures could minimize lingering crises and the painful costs of natural disasters.
