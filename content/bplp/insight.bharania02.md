---
title: "Best Practices for Securing Data"
description: "Blogpost #2 by Rakesh Bharania"
lead: "Best Practices for Securing Data in Humanitarian Crisis Situations"
date: 2021-09-03T12:00:00.000Z
lastmod: 2021-09-03T12:00:00.000Z
draft: false
contributors:
  - Rakesh Bharania
  - Alex Parker
menu:
  bplp:
    parent: "insights"
weight: 109
toc: true
#extlink: https://www.salesforce.org/blog/securing-data-crisis-situations/
---

{{< alert >}}This article was originally posted at [https://www.salesforce.org/blog/securing-data-crisis-situations/](https://www.salesforce.org/blog/securing-data-crisis-situations/){{< /alert >}}

{{< float right>}}{{< quote >}}Following these best practices will help increase awareness of the security tools and features that can be used to minimize the risk to vulnerable people.{{< /quote >}}{{< /float >}}


The unfolding crisis in Afghanistan is a stark reminder that many Salesforce.org nonprofit customers often work in fragile environments. Whether involved in humanitarian response in conflict or disaster situations, development work, human rights, or peace-building, our international nonprofit customers have some of the most complex nonprofit missions on earth. In addition to the challenges inherent to any nonprofit mission, these organizations and their personnel must often work in areas with poor security and limited resources.

These fragile environments mean that those using Salesforce technologies have to take into account a whole set of additional potential threats, such as considering the theft or capture of trusted devices, or personnel may be forced to divulge login information under duress. And the potential harms resulting from the loss of data confidentiality, integrity, or availability may go beyond digital security concerns to include serious physical security risks — including targeted violence — for nonprofit staff and beneficiaries alike.

In recent years, the international humanitarian community has responded with a number of data protection guidance documents, such as those from [USAID](https://www.usaid.gov/sites/default/files/documents/15396/USAID-UsingDataResponsibly.pdf), [ICRC](https://www.icrc.org/en/data-protection-humanitarian-action-handbook), [OCHA](https://data.humdata.org/dataset/2048a947-5714-4220-905b-e662cbcd14c8/resource/c7053042-fd68-44c7-ae24-a57890a48235/download/ocha-dr-guidelines-working-draft-032019.pdf), and the [Harvard Humanitarian Initiative](https://hhi.harvard.edu/publications/signal-code-human-rights-approach-information-during-crisis). Salesforce.org welcomes these sector-developed guidelines, and we engage organizations like [UN OCHA](https://centre.humdata.org/), [ICRC](https://www.icrc.org/en/who-we-are/the-governance/icrc-and-data-protection), and [NetHope](https://nethope.org/) to improve protection guidance while remaining grounded in humanitarian principles.

Trust is the number one value for Salesforce.org and we are committed to ensuring world-class security across our products and solutions. But assuring security and data protection is a shared responsibility between Salesforce.org and our customers. We believe that technology systems intended to be used in fragile environments must be “protective by design,” and seek from the outset to minimize the risk of harm. Fragile environments can be unpredictable and dynamic, and while all possible harms cannot be foreseen, good Salesforce implementations should actively minimize the possibility of harm.

### Step One: Understanding Your Use Case’s Purpose and Threat Model

The first step is to clearly understand why the system, application, or data collection ought to exist in the first place. Organizations should critically review proposed data collection and ensure that the intended benefits and impact justify the risks of data collection in the first place.

This may be done through a formal [Data Protection Impact Assessment (DPIA)](https://gdpr.eu/data-protection-impact-assessment-template/) or other mechanism. Importantly, the digital security and data responsibility evaluations should also be placed in the context of the physical security concerns that may also exist in the field environment for which the solution is intended.

For example, if the use case needs to take into account lost or stolen devices that may be captured by an armed group, appropriate digital security capabilities, such as remote wipe of those devices, should also be incorporated. Appropriate data retention policies should be implemented, including considerations for the rapid decay of the physical security situation.

### Step Two: Incorporate Salesforce Security Features Into Your Implementation Accordingly

With a clear understanding and justification for data collection, and with an eye towards the kinds of possible threats that may need to be accounted for, consider how the following features and capabilities might reduce risks for the application, nonprofit personnel, and for beneficiaries.

#### For users in the field utilizing the Salesforce App or Salesforce Mobile SDK:

* **Remote Wipe:** All data requires authentication in order to be accessed, whether in the cloud or on the device, however, remote wiping revokes access for a user and clears a device. This is commonly done when employees are terminated and reduces on-device risks, but can be an important tool to keep in mind. [Learn more.](https://help.salesforce.com/s/articleView?id=sf.mobile_security_remote_wipe.htm&type=5)

* **Authentication Refresh:** Ensure that user authentication requires a refresh when inactive for a reasonably short amount of time. This ensures an active session isn’t easily misused to access data. [Learn more.](https://help.salesforce.com/s/articleView?id=sf.mobile_security_oauth.htm&type=5)

* **Monitor Mobile Activities:** Using real-time streaming events, monitor mobile activity of users in case of suspicious activity like screenshots, calls, or emails. [Learn more.](https://help.salesforce.com/s/articleView?id=sf.mobile_security_mam_monitor.htm&type=5) *Note: This uses “Event Monitoring”*

* **Review Mobile Application Security:** While the above are important call outs, the full [Mobile Application Security Help Document](https://help.salesforce.com/s/articleView?id=sf.mobile_security.htm&type=5) is a great resource to review.

* **Review Mobile SDK Development Guide:** Similar to the above resource, for any organization using the Salesforce Mobile SDK, there is a comprehensive guide around security and best practices available. [Learn more.](https://developer.salesforce.com/docs/atlas.en-us.mobile_sdk.meta/mobile_sdk/preface_intro.htm?icid=SFORG:blog-inline:&_ga=2.229603033.471686356.1635640708-900093857.1635640708)

#### Overall Salesforce.org admin guidance:

* **Enable Multi-Factor Authentication (MFA):** A key security feature of Salesforce intrinsic to being a cloud service is that while some tightly controlled data can be stored offline/on-device, systems are cloud based and access to all data requires authentication. Adding an additional factor to security can be key to ensure leaking of passwords or devices themselves won’t individually lead to unauthorized access. There are offline MFA options for low connectivity areas. Learn more in the [MFA Guide.](https://www.salesforce.com/content/dam/web/en_us/www/documents/guides/mfa-quick-admin-guide.pdf?icid=SFORG:blog-inline:&_ga=2.229488345.471686356.1635640708-900093857.1635640708)

* **Review Sessions:** When users access Salesforce, their “sessions” can be seen along with details of their locations, username, access type, etc. Review Sessions to monitor access and remove if needed. [Learn more.](https://help.salesforce.com/s/articleView?id=sf.security_user_session_info.htm&type=5)

* **Elevate Session Security:** For sensitive data or activities, ensure “High-Assurance Sessions” to dynamically elevate security settings or block activities entirely. Example: Forcing MFA when accessing reports. [Learn more.](https://help.salesforce.com/s/articleView?id=sf.security_auth_require_ha_session.htm&type=5)

* **Set Trusted IP Ranges:** If there are still trusted networks, or trusted VPN services, blocking access from all IP addresses except for trusted IP ranges can help. Keep in mind that this tool has broad implications and should be part of a layered approach if used. [Learn more.](https://developer.salesforce.com/docs/atlas.en-us.securityImplGuide.meta/securityImplGuide/salesforce_security_guide.htm)

* **Disable Report Exports:** While this doesn’t prevent the ability to capture data if a user has access to that data, disabling report exports can make it harder to obtain data in bulk. You can do this by going to Profile > System Preferences > disable “Export Reports”.

* **Disable Print Screen:** Similar to above, disabling the print screen option makes it harder to obtain data locally in bulk. To do this, go to Setup > User Interface > disable “Enable Printable List Views”.

* **Utilize Threat Detection:** Using Machine Learning, Salesforce allows users to see when “anomalies” have been identified across their users and data. As an admin, this helps to proactively identify suspicious use of API Activity, Report Activity, as well as Session Hijacking and Credential Stuffing. Read more about [Threat Detection Overview](https://developer.salesforce.com/docs/atlas.en-us.securityImplGuide.meta/securityImplGuide/real_time_em_threat_detection.htm?icid=SFORG:blog-inline:&_ga=2.25521656.471686356.1635640708-900093857.1635640708) in this [help document](https://developer.salesforce.com/docs/atlas.en-us.securityImplGuide.meta/securityImplGuide/salesforce_security_guide.htm) *Note: This requires Event Monitoring.*

* **Review Security Guide:** [The Salesforce Security Guide](https://developer.salesforce.com/docs/atlas.en-us.securityImplGuide.meta/securityImplGuide/salesforce_security_guide.htm?icid=SFORG:blog-inline:&_ga=2.192780271.471686356.1635640708-900093857.1635640708) is a much more comprehensive document to help assess an organization’s security posture.

Organizations impacted by the [withdrawal in Afghanistan have been asked to also secure or delete](https://apnews.com/article/afghanistan-technology-online-us-civilians-e13530f8b8d41268cd5b582fb59bbe20) any personally identifiable information related to individuals on the ground if there is a risk that the data may be captured by unauthorized personnel. Here are some tips for finding and managing that user data and content.


* **Search your Salesforce data:** Simple, but the best place to start is to search your records for anything related to “Afghanistan,” understanding that you know your data, the context of your mission best and how to search for it. This could be identified through the roles of individuals, contact addresses, names of provinces, language, or currency, as examples.

* **Control access:** For any sensitive information found above within Salesforce, there are a number of ways to further lock it down to others if this is not already being done. This is object, field or file access. This security can depend on the nature of the data you’re working with, but [this quick training](https://docs.google.com/document/d/16kNFk25itvcIFNQDuROydhI6i2gbgE-u9Q2awJ5xia4/edit?usp=sharing) covers different ways to control access.

#### Off-Salesforce tips and best practices:

* **Device Management:** If your organization has [MDM (Mobile Device Management)](https://www.gartner.com/en/information-technology/glossary/mobile-device-management-mdm) tools in place, this can ensure that data is protected at the device-level (laptop, mobile, etc), remotely wiped and monitored. If the Salesforce Mobile SDK is utilized, [it can work together](https://developer.salesforce.com/docs/atlas.en-us.mobile_sdk.meta/mobile_sdk/oauth_mdm.htm?icid=SFORG:blog-inline:&_ga=2.201897940.471686356.1635640708-900093857.1635640708) with this as well.

* **Integrated Services:** Services that integrate with Salesforce (ie: third-party tools, data warehouses, analytics, etc.) should also be considered. While Salesforce may be locked, if all data flows through a specific tool or a data warehouse for analytics, access to those systems would need to be managed.

* **Sensitive Data Footprint:** Similar to above, when systems are integrated, often elements of data interrelate where pieces of a full picture may live in different systems. For sensitive data, ensure it’s protected across systems.

* **Email Services & Messaging:** Working with your email or messaging service, ensure that all options for clearing on-device caching are explored, including monitoring for suspicious emails, and control any potential for compromised identities misusing access for phishing attempts. An example of this would be an individual’s device being accessed, and obtaining data by posing as the individual.

### Step Three: Monitor and Prepare to Respond to Incidents

Deploying the application into production does not end the process of harm minimization. Indeed, monitoring the ongoing security situation, security logs, and taking action on any incidents that may arise needs to be an ongoing activity for the lifetime of the application.

**Define roles and responsibilities** for monitoring logs and identifying suspicious activity, including when and how to activate the incident response plan.

**Develop and exercise the incident response plan** to suspected or confirmed data breaches. It should be practiced regularly to ensure the validity of the workflow and to ensure that the entire team knows how to respond prior to a real-world incident occurring. In fragile environments, these incident response plans should integrate both the digital security response as well as the physical security response on the ground in the crisis zone to ensure that vulnerable people are able to take appropriate protective action.

**Respond to incidents** and iterate processes and procedures as needed.

### In a Crisis, Reducing Risk Enhances Impact

Salesforce.org is proud to partner with our customers to help enable their impact in these vital missions all around the world. This includes ensuring that critical data remains safe and protected, even in challenging crisis circumstances. Of course, a blog article cannot address specific threats in context. The real world is simply far too complex for that! But if you have questions or concerns about your use case, or Salesforce security and privacy features in the context of fragile environments, [please reach out](https://www.salesforce.com/form/sfdo/sfdo/contact-us/?icid=SFORG:blog-inline:&_ga=2.206028758.471686356.1635640708-900093857.1635640708) to your Salesforce account executive or Salesforce partner for a more in-depth conversation.

***For more information, visit the Salesforce [Office of Ethical and Humane Use](https://www.salesforce.com/company/ethical-and-humane-use/?icid=SFORG:blog-cta:&_ga=2.239058885.471686356.1635640708-900093857.1635640708). And read more about [Protecting the Humanitarian Mission With the Cloud](https://www.salesforce.org/blog/first-do-no-digital-harm-protecting-the-humanitarian-mission-with-the-cloud/), and [Safely Delivering Connectivity as Aid](https://blogs.icrc.org/law-and-policy/2021/07/08/protective-by-design-connectivity-as-aid/).***

### About the Authors

***Rakesh Bharania** is Director of Humanitarian Impact Data at Salesforce.org. He has spent more than 25 years in the humanitarian sector, focusing on the intersection of emerging technologies and international humanitarian crisis response and development. Rakesh has also engaged across the board with policy-makers, senior government officials, academia, first responders, NGOs/IGOs, volunteer organizations and industry leaders.*

***Alex Parker** is Senior Platform Architect at Salesforce.org. He has 14 years experience implementing, solutioning, and supporting nonprofit enterprise technology with a focus on governance, compliance, and security.*