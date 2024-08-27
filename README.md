# Epidemiological stratification and subnational targeting (SNT) of malaria control interventions in Sierra Leone
![Sierra Leone Map](https://github.com/user-attachments/assets/1ce28ecc-191b-4f2d-bbfc-8944223bc993)

## Table of Contents
- [Summary](#summary)
- [Acknowledgement](#acknowledgement)
- [Introduction](#introduction)
- [Epidemiological Stratification](#epidemiological-stratification)
  - [Quality Assessment of Data Elements Used for Stratification](#quality-assessment-of-data-elements-used-for-stratification)
  - [Reporting Rate](#reporting-rate)
  - [Incidence of Malaria](#incidence-of-malaria)
  - [Prevalence of Plasmodium Falciparum](#prevalence-of-plasmodium-falciparum)
  - [All-Cause Mortality in Children Under Five](#all-cause-mortality-in-children-under-five)
  - [Median Malaria Incidence Between 2019-2023](#median-malaria-incidence-between-2019-2023)
  - [Final Malaria Epidemiological Stratification Map](#final-malaria-epidemiological-stratification-map)
- [Stratification of Malaria Transmission Determinants](#stratification-of-malaria-transmission-determinants)
  - [Case Management](#case-management)
  - [Vector Control](#vector-control)
  - [Malaria Vaccine Plans for 2024](#malaria-vaccine-plans-for-2024)
  - [Entomology](#entomology)
  - [Malaria Seasonality](#malaria-seasonality)
- [Next Steps](#next-steps)
- [Conclusion](#conclusion)
- [References](#references)
- [Appendices](#appendices)
  - [Appendix 1: WHO Incidence Adjustment Methodology](#appendix-1-who-incidence-adjustment-methodology)
  - [Appendix 2: Seasonality Per Chiefdom](#appendix-2-seasonality-per-chiefdom)

### List of Figures
- [Figure 1. SNT team members](#figure-1-snt-team-members)
- [Figure 2. Inconsistencies checking](#figure-2-inconsistencies-checking)
- [Figure 3. Strip plot of intervention variables for malaria in Sierra Leone (2015-2023)](#figure-3-strip-plot-of-intervention-variables-for-malaria-in-sierra-leone-2015-2023)
- [Figure 4. Stacked bar charts for the number of outliers for test positivity per month in Sierra Leone (2015-2023)](#figure-4-stacked-bar-charts-for-the-number-of-outliers-for-test-positivity-per-month-in-sierra-leone-2015-2023)
- [Figure 5. Overall reporting status among DHIS2 HFs in Sierra Leone (2015-2023)](#figure-5-overall-reporting-status-among-dhis2-hfs-in-sierra-leone-2015-2023)
- [Figure 6. Reporting rate of confirmed cases among DHIS2 HFs in Sierra Leone (2015-2023)](#figure-6-reporting-rate-of-confirmed-cases-among-dhis2-hfs-in-sierra-leone-2015-2023)
- [Figure 7. Crude incidence of malaria (cases per 1000 inhabitants)](#figure-7-crude-incidence-of-malaria-cases-per-1000-inhabitants)
- [Figure 8. Malaria incidence adjusted for testing](#figure-8-malaria-incidence-adjusted-for-testing)
- [Figure 9. Malaria incidence adjusted for testing and reporting rate](#figure-9-malaria-incidence-adjusted-for-testing-and-reporting-rate)
- [Figure 10. Malaria incidence adjusted for testing, reporting and care seeking rate](#figure-10-malaria-incidence-adjusted-for-testing-reporting-and-care-seeking-rate)
- [Figure 11. Summary of crude and adjusted incidence values according to WHO methodology](#figure-11-summary-of-crude-and-adjusted-incidence-values-according-to-who-methodology)
- [Figure 12. Care-seeking rate in Sierra Leone](#figure-12-care-seeking-rate-in-sierra-leone)
- [Figure 13. Prevalence of Plasmodium falciparum (SLMIS 2021)](#figure-13-prevalence-of-plasmodium-falciparum-slmis-2021)
- [Figure 14. Under-five mortality rate, all causes from SLDHS 2019](#figure-14-under-five-mortality-rate-all-causes-from-sldhs-2019)
- [Figure 15. Median Incidence 2019-2023 adjusted for testing and reporting rates](#figure-15-median-incidence-2019-2023-adjusted-for-testing-and-reporting-rates)
- [Figure 16. Final maps for risk estimation](#figure-16-final-maps-for-risk-estimation)
- [Figure 17. Map for access to care decision-making](#figure-17-map-for-access-to-care-decision-making)
- [Figure 18. CHW density](#figure-18-chw-density)
- [Figure 19. CHW and access](#figure-19-chw-and-access)
- [Figure 20. Care-seeking behavior](#figure-20-care-seeking-behavior)
- [Figure 21. Health facilities density per population](#figure-21-health-facilities-density-per-population)
- [Figure 22. Testing rate (DHS 2019)](#figure-22-testing-rate-dhs-2019)
- [Figure 23. Testing rates for uncomplicated malaria in health facilities](#figure-23-testing-rates-for-uncomplicated-malaria-in-health-facilities)
- [Figure 24. Treatment rates for uncomplicated malaria in health facilities](#figure-24-treatment-rates-for-uncomplicated-malaria-in-health-facilities)
- [Figure 25. Presumed cases](#figure-25-presumed-cases)
- [Figure 26. CHWs malaria testing rates](#figure-26-chws-malaria-testing-rates)
- [Figure 27. CHW malaria treatment rates](#figure-27-chw-malaria-treatment-rates)
- [Figure 28. Hospital malaria mortality ratios](#figure-28-hospital-malaria-mortality-ratios)
- [Figure 29. RDT stockouts per year](#figure-29-rdt-stockouts-per-year)
- [Figure 30. Antimalarial stock outs](#figure-30-antimalarial-stock-outs)
- [Figure 31. ACT stock-outs](#figure-31-act-stock-outs)
- [Figure 32. Coverage of ITN distribution through antenatal care visits](#figure-32-coverage-of-itn-distribution-through-antenatal-care-visits)
- [Figure 33. Coverage of mass ITN distribution](#figure-33-coverage-of-mass-itn-distribution)
- [Figure 34. Targeting of school-based ITN distribution (SBD)](#figure-34-targeting-of-school-based-itn-distribution-sbd)
- [Figure 35. Household ITN access (map)](#figure-35-household-itn-access-map)
- [Figure 36. Household ITN access (plot)](#figure-36-household-itn-access-plot)
- [Figure 37. Population ITN use](#figure-37-population-itn-use)
- [Figure 38. Pregnant women ITN use](#figure-38-pregnant-women-itn-use)
- [Figure 39. Population-level ITN use](#figure-39-population-level-itn-use)
- [Figure 40. Net durability](#figure-40-net-durability)
- [Figure 41. IRS implementation and coverage](#figure-41-irs-implementation-and-coverage)
- [Figure 42. IPTp operational coverage out of ANC1](#figure-42-iptp-operational-coverage-out-of-anc1)
- [Figure 43. IPTp effective coverage (DHS 2019)](#figure-43-iptp-effective-coverage-dhs-2019)
- [Figure 44. IPTi (PMC) Coverage out of target population](#figure-44-ipti-pmc-coverage-out-of-target-population)
- [Figure 45. Chiefdoms where malaria vaccination is conducted](#figure-45-chiefdoms-where-malaria-vaccination-is-conducted)
- [Figure 46. Location of entomological surveillance sites](#figure-46-location-of-entomological-surveillance-sites)
- [Figure 47. Rainfall vs cases (all ages and u5) for seasonality analysis](#figure-47-rainfall-vs-cases-all-ages-and-u5-for-seasonality-analysis)
- [Figure 48. Profiling seasonality for SMC targeting](#figure-48-profiling-seasonality-for-smc-targeting)
- [Figure 49. Seasonality map based on rainfall vs case peaks](#figure-49-seasonality-map-based-on-rainfall-vs-case-peaks)
- [Figure 50. Rainfall peak detection (example of BO)](#figure-50-rainfall-peak-detection-example-of-bo)
- [Figure 51. The onset of end and peak of the rainy season](#figure-51-the-onset-of-end-and-peak-of-the-rainy-season)
- [Figure 52. Seasonality for implementation purposes using cases](#figure-52-seasonality-for-implementation-purposes-using-cases)

- Code Repository: python version
  - [Data Managemnt](#data-management)




### Summary
---

Malaria continues to pose a significant public health challenge in Sierra Leone, with its burden varying across time and geographical regions. Given the constraints on human and financial resources, a strategic approach based on disease transmission intensity is essential. This stratification allows for targeted interventions tailored to the epidemiological profile of each chiefdom, taking into account insecticide resistance patterns, parasite sensitivity to treatments, and vector biology. The ultimate goal is to maximize cost-effectiveness in malaria control efforts.
Epidemiological stratification can be achieved through various methodologies, utilizing different data sources either independently or in combination. A spectrum of indicators, including both crude and predicted prevalence, as well as crude, WHO-adjusted, or predicted incidence rates, can be employed for this purpose. The selection of the most suitable approach is context-dependent, considering factors such as the surveillance system's capacity to capture comprehensive malaria case data, healthcare-seeking behaviors among febrile patients, and the overall quality of malaria-related data within the country.
This report presents a comprehensive analysis of routine data collected over the past nine years in Sierra Leone, complemented by the most recent malaria prevalence data from the 2021 Malaria Indicator Survey. Its primary objective is to guide the national malaria control program and other stakeholders in identifying the most relevant indicators for the local context. To facilitate informed decision-making, we present prevalence and incidence maps along with adjusted values for each indicator. Additionally, we outline the targeting of various malaria control interventions, based on WHO recommendations and stakeholder consensus. 
It's important to note that this document contains preliminary analysis results. These findings will be subject to updates as new data becomes available and will incorporate insights from ongoing stakeholder discussions and workshops.

### Acknowledgement
---

We would like to thank all our partners who have contributed to the development of this document and the revision of its various versions.
Contacts:

### NMCP: 
Mr Musa Sillah-Kanu (NMCP-M&E unit, musasillahkanu1@gmail.com)
Dr Mac-Abdul Falama (NMCP-PM, abdulmac14@yahoo.com)

### CHAI: 
Mr Victor Olayemi (volayemi@clintonhealthaccess.org)
Dr Valérian Turbé (vturbe@clintonhealthaccess.org)
Dr Celestin Danwang (cdanwang@clintonhealthaccess.org)


### WHO: 
Mr Mohamed Sillah Kanu (sillahmohamedkanu@gmail.com)
Dr Omoniwa Omowunmi Fiona (omoniwao@who.int)
Dr Beatriz Galatas (galatasb@who.int)


| Name                        | Position                                     |
|-----------------------------|----------------------------------------------|
| Dr Abdul Mac Falama         | Programme Manager                            |    
| Musa Sillah-Kanu            | Surveillance, Monitoring and Evaluation Lead |  
| Dr Omoniwa Omowunmi Fiona   | WHO Country Office                           |
| Mr Mohamed Sillah Kanu      | Local Consultant                             |
| Dr Beatriz Galatas          | WHO Global Malaria Program                   |


 <img width="479" alt="Partners" src="https://github.com/user-attachments/assets/c6630349-669f-4521-9862-23c3fca751a6"> 

 

 
 
  
### Figure 1. SNT team members


### Epidemiological stratification

The data used in this analysis come from the District Health Information System version 2 (DHIS2), the 2019 Sierra Leone Demographic and Health Survey (SLDHS),[2] 2021 Sierra Leone Malaria Indicators Survey (SLMIS 2021) and results of studies carried out by partners in Sierra Leone. All these data were consolidated into a single database available in the WHO SharePoint. Data processing and analysis were carried out using python, Stata and R analysis software, with codes available upon request.
The first step was to merge the data into a single database and shapefile in python. For this purpose, the names of the geographical units (admin1, admin2 and admin3) contained in DHIS2 were taken as the reference. The names of the geographical units contained in the various data files were modified to match those in DHIS2. Subsequently, variable names were standardized to match the data dictionary used by WHO-GMP for variable names in SNT. The dictionary employed is available in the WHO SharePoint and can be obtained upon request. The resulting data was then merged with the adm3 level Shapefile (chiefdoms/zones). Analyses were carried out at the chiefdom level in accordance with the resolutions of the initial stratification online meeting.

Sierra Leone has made steady progress in malaria control over the past decade, with malaria prevalence among children under five decreasing slightly from 40.1% in 2016 (MIS 2016) to 21.6% in 2021 (SL MIS 2021). However, the country still faces significant challenges, including high transmission rates in certain districts, insecticide resistance, and the need for improved healthcare access in rural areas. This stratification effort aims to address these challenges by tailoring interventions to the specific needs of each chiefdom/district ultimately contributing to Sierra Leone's goal of reducing malaria morbidity and mortality. By adopting a more targeted approach, the country seeks to optimize its resources and enhance the effectiveness of its malaria control strategies, paving the way for further reductions in the disease burden across the country.

### Quality assessment of data elements used for stratification

#### Checking database contents
The variables of interest for epidemiological stratification are listed in the SNT data collection template available to all on the WHO Sharepoint. This template summarizes in an excel file, the routine and intervention data collected between 2015 and 2023, disaggregated by month and by chiefdom.

#### Inconsistencies
To detect the presence of inconsistencies in the data, nested data elements were used. Figure 2 illustrates comparisons between different malaria-related indicators.


![one to one scatter plot](https://github.com/user-attachments/assets/a683cfa8-d1be-4939-8fc4-c74820699abd)




### Figure 2. Inconsistencies checking

### Some key observations:
test vs allout (top left): This graph compares the number of malaria tests performed (test) with the total number of outpatients (allout). Ideally, all points should fall below the diagonal line, as the number of tests should not exceed the total number of outpatients. However, we observed many points above the line, indicating instances where more malaria tests were reported than total outpatients. This suggests potential over-reporting of malaria tests or under-reporting of outpatient visits.
conf vs test (top right): This graph compares the number of confirmed malaria cases (conf) with the number of tests performed (test). All points should fall below the diagonal line, as confirmed cases cannot exceed the number of tests. 

The graph shows good consistency, with most points below the line, indicating that this relationship is generally well-maintained in the data.
maltreat vs conf (bottom left): This graph compares the number of malaria treatments given (maltreat) with the number of confirmed cases (conf). Ideally, these numbers should be close, with points near the diagonal line. However, we see many points below the line, suggesting that in some instances, fewer treatments were given than there were confirmed cases. This could indicate issues with treatment availability or reporting inconsistencies.
maldth vs maladm (bottom right): This graph compares malaria deaths (maldth) with malaria admissions (maladm). All points should fall below the diagonal line, as deaths cannot exceed admissions. The graph shows good consistency in this regard, with all visible points below the line. However, the clustering of points near zero suggests that either malaria mortality is very low or there might be under-reporting of malaria deaths.

These graphs highlight several data quality issues: i) Inconsistencies between malaria tests and outpatient numbers, ii) Generally good consistency between confirmed cases and tests, iii) Potential under-treatment or under-reporting of treatments for confirmed cases, iv) Consistent relationship between malaria deaths and admissions, but possible under-reporting of deaths (Figure 2).
These findings underscore the need for improved data quality assurance measures, regular monitoring of reported data, and capacity building for health workers in accurate data collection and reporting. Further investigation is needed to understand the root causes of these inconsistencies, which could include issues with data entry, misunderstanding of reporting requirements, stockout of registers and reporting tools, or systemic problems in the health information system.

### Outliers
To visualize and analyze outliers across variables and years from 2015 to 2023, strip plots were constructed for both routine epidemiological data (Figure 3) and intervention data (Figure 3) related to malaria in Sierra Leone.

This visualization (Figure 3) allows for a comparison of different malaria interventions over time in Sierra Leone, highlighting variations, potential trends, and unusual data points that may warrant further investigation.



![Stripplot plot2](https://github.com/user-attachments/assets/85d15331-c3e2-42b7-a0a2-b9d59385eef6)


### Figure 3. Strip plot of intervention variables for malaria in Sierra Leone (2015-2023)


#### Some key observations:
Outliers: There are several notable outliers, particularly for variables like "IPTi3 total", "LLIN_penta3 total", where some data points are significantly higher than the majority.
Variability: Some variables show more spread in their values across years (e.g., "Vita1 total", " Vita2 total "), while others are more tightly clustered (e.g., "Penta1 total", " Penta3 total ").
Temporal trends: For some variables, there appear to be changes over time. For example, "anc4 total" seems to have more high-value outliers in later years.
Missing data: Some variables have fewer data points than others, which could indicate missing data for certain years.
Consistency: Some interventions (like those at the bottom of the graph) seem to have more consistent values across years, while others (like those in the middle) show more variation.

The outlier checking of routine epidemiological malaria data in Sierra Leone was done (Figure 4). Outlier detection is crucial in this context because: outliers can lead to the misclassification of chiefdoms due to incorrect data. Thus, the detection process was automated for each health facility (HF), identifying records above [Q3 + 1.5*IQR] based on the data distribution for each facility. Due to Community Health Worker (CHW) outreach campaigns in 2023 that affected the data, this year was excluded from outlier detection, and its values were not corrected. Similar, 2023 was also excluded from the distribution used to compute the thresholds for each health facility.

![test_positive](https://github.com/user-attachments/assets/1109169e-b9a6-49a6-a5d4-90a00fa0cb05)


### Figure 4. stacked bar charts for the number of outliers for test positivity per month in Sierra Leone (2015-2023)

### Some key observations in figure 4:
Fluctuations: The graph shows significant fluctuations in test positivity rates over time, with some periods showing higher rates than others.
Seasonal patterns: There appear to be some recurring patterns, possibly indicating seasonal variations in malaria transmission or testing rates.
Outliers: While specific outliers are not immediately apparent in this aggregated view, there are several spikes in the data that could represent periods of unusually high-test positivity rates. These could be due to actual increases in malaria cases or potential data anomalies.
Recent trends: The right side of the graph, representing more recent years, shows some notably high spikes in test positivity rates across multiple categories.
Potential impact of interventions: Some of the variations observed could be related to malaria control interventions or changes in testing practices over time.
This visualization provides a comprehensive view of test positivity trends over time, allowing for the identification of patterns, potential outliers, and areas that may require further investigation or data validation.

### Reporting rate 
To calculate the malaria reporting rate, health facility level routine data were obtained from Sierra Leone's national DHIS2 system for the period 2015 to 2023 (Figure 5).

<img width="218" alt="image" src="https://github.com/user-attachments/assets/bf640426-e831-4864-a0d3-90dc298e6d00">


![completenes2](https://github.com/user-attachments/assets/30024607-b6ca-4e07-89f5-431d0c42efed)    


### Figure 5. Overall reporting status among DHIS2 HFs in Sierra Leone (2015-2023)


The graph above (Figure 5) presents a comprehensive visualization of health facility reporting patterns across districts in Sierra Leone from 2015 to 2023. This graph tracks the monthly reporting of key malaria indicators including all-cause outpatients, tested, confirmed, or treated malaria cases. The color-coded representation provides insights into reporting consistency: green indicates months with reports, yellow shows gaps after previous reporting, and red highlights missing data without prior reporting. This visualization was instrumental in computing monthly reporting rates, which were subsequently used to adjust malaria incidence estimates according to WHO methodology.
The graph reveals significant variations in reporting patterns across districts. While some districts demonstrate consistent reporting (predominantly green), others show more frequent gaps (more yellow and red), indicating potential challenges in data collection or submission processes.
This analysis of reporting patterns is crucial for several reasons: It helps identify districts that may require additional support to improve their reporting practices (like Western area urban districts); it provides context for interpreting malaria incidence data, as areas with lower reporting rates may underestimate the true disease burden; it informs the adjustment of incidence rates, ensuring more accurate estimates of malaria burden across Sierra Leone.
After discussion, it was agreed that only health facilities which had previously reported data (all-cause outpatients, tested, confirmed, or treated) at least once would be considered active and included in the denominator when calculating the reporting rate. 
Figure 6 illustrates the monthly reporting rate by health facility and district of confirmed cases, which is the main variable used to calculate crude incidence.


![RR Confirmed cases](https://github.com/user-attachments/assets/49409b17-2b8e-4f6c-ad62-f9750895343c)


### Figure 6. Reporting rate of confirmed cases among DHIS2 HFs in Sierra Leone (2015-2023)


The heatmap in **Figure 6** reveals significant variations in confirmed malaria case reporting rates across districts and over time, with most districts showing improved consistency in recent years, though some continue to exhibit periodic gaps or fluctuations in reporting, underscoring the importance of ongoing efforts to strengthen the health information system and ensure comprehensive malaria surveillance across Sierra Leone.


### Incidence of malaria 
To calculate malaria incidence, routine data aggregated by chiefdom were obtained from Sierra Leone's national DHIS2 system for the period from 2015 to 2023. The reporting rate obtained as explained in the previous section was used for incidence adjustment.
The total number of confirmed malaria cases was calculated by summing confirmed cases at community, health center, and hospital levels. Crude incidence per month (or year) was obtained by dividing the number of confirmed cases by the Chiefdom's population.
The incidence was adjusted using WHO methodology:[3]
1. First-level adjustment: Accounting for presumed cases not tested.
2. Second-level adjustment: Accounting for variable reporting rates across Chiefdoms.
3. Third-level adjustment: Incorporating care-seeking behavior estimates from community surveys (DHS/MICS) to account for cases outside the public health sector.
   
Crude and adjusted incidence rates were categorized based on the maximum value of adjusted annual incidence observed in each chiefdom between 2015 and 2023, using the categories: 0-<50, 50-<100, 100-<250, 250-<450, 450-<700, 700-<1000 and >=1000 per 1000 inhabitants at risk.

### Crude incidence of malaria (cases per 1000 population at risk)
Crude incidence was obtained by dividing the number of confirmed cases by the population of the chiefdoms. The crude incidence maps for Sierra Leone from 2015 to 2023 reveal a significant and encouraging trend in malaria control efforts across the country. Over this period, there has been a notable decrease in malaria incidence rates, with a marked shift from predominantly high-incidence areas in the earlier years to a more varied landscape with many low to moderate incidence regions by 2023 (Figure 7). 


![Incidence map](https://github.com/user-attachments/assets/22f38a48-b3c0-4162-8c28-dc955fb00085)


### Figure 7. Crude incidence of malaria (cases per 1000 inhabitants)

The geographical distribution of malaria incidence shows considerable variation across Sierra Leone's chiefdoms. Throughout the years, the southern and eastern regions of the country have consistently exhibited higher incidence rates, while the western and some northern areas have generally maintained lower rates. This pattern suggests that local factors, such as climate, geography, or healthcare access, may play a crucial role in malaria transmission dynamics (Figure 7).
A pivotal change appears to have occurred between 2019 and 2020, with a substantial reduction in high-incidence areas. This shift could be attributed to intensified malaria control efforts, improvements in healthcare infrastructure, or changes in reporting practices. The more recent years (2021-2023) display a more homogeneous distribution of incidence rates, with many chiefdoms falling into the 50-250 per 1000 range, indicating a general stabilization of malaria incidence at lower levels compared to earlier years.
Despite the overall positive trend, some chiefdoms, particularly in the south and southeast, continue to show persistently higher incidence rates across all years. These areas likely require targeted interventions and focused resources to bring them in line with the national trend of decreasing incidence.
The 2023 detailed map provides a clear picture of the current situation, highlighting that while much of the country has achieved relatively low incidence rates, there remain pockets of higher transmission that warrant special attention. 
In conclusion, the crude incidence data from 2015 to 2023 demonstrates significant progress in reducing malaria incidence across Sierra Leone. However, the persistence of some higher-incidence areas underscores the need for continued efforts and targeted strategies (**Figure 7**).  

### Malaria incidence adjusted according to WHO methodology
The WHO incidence adjustment method has been used in several scientific publications.[3–5]  It has the advantage of being relatively easy to implement, and of allowing the correction of limitations linked to the health systems of sub-Saharan African countries (reporting, testing, Healthcare seeking rate).

### Malaria incidence adjusted for testing
To adjust the number of confirmed cases for the absence of testing in presumed-positive patients, the number of presumed cases was multiplied by the test positivity rate, and the resulting figure was added to the number of cases confirmed by microscopy and/or RDT. The previous result was then divided by the population to obtain the incidence adjusted for the testing rate (1st level of incidence adjustment according to WHO methodology) (**Figure 8**). 
The series of maps and charts depicting the incidence of malaria adjusted for testing rates in Sierra Leone from 2015 to 2023 reveals a complex and evolving landscape of malaria transmission across the country (Figure 8). The series of maps and accompanying bar graphs illustrate a notable transformation in the incidence patterns over time.


![incidence adjusted by TPR](https://github.com/user-attachments/assets/9775bb1a-57ca-4f0b-b02a-119cc6e3e992)


### Figure 8. Malaria incidence adjusted for testing
In the earlier years (2015-2019), the maps depict a highly heterogeneous distribution of malaria incidence across Sierra Leone's chiefdoms. Many areas, particularly in the central and eastern regions, showed high incidence rates, represented by orange and red colorations. The corresponding bar graphs for these years demonstrate a relatively even distribution across incidence categories, with significant representation in the higher brackets (**Figure 8**).
A marked shift becomes apparent from 2020 onwards. The maps for 2020-2023 display a substantial reduction in high-incidence areas, transitioning towards more moderate (yellow and light blue) and low (blue) incidence rates across numerous chiefdoms. This trend is mirrored in the bar graphs, which show a clear shift towards lower incidence categories, with the majority of chiefdoms falling into the 50-250 per 1000 range by 2023.
The detailed map for 2023 provides a granular view of the current situation. While it confirms the overall trend towards lower incidence rates across much of the country, it also highlights persistent pockets of higher incidence, particularly in the southern region. This nuanced picture underscores the importance of targeted interventions in these remaining high-incidence areas.

### Malaria incidence adjusted for testing and reporting
The numerator used for the first level of WHO incidence adjustment was divided by the reporting rate. This was done to take into account the variable reporting rates in different chiefdoms, and to obtain a figure close to reality if the reporting rate were 100%. The figure obtained was divided by the population to produce the adjusted incidence for testing and reporting (2nd level of incidence adjustment according to WHO methodology) (**Figure 9**).

![incidence adjusted-active hf](https://github.com/user-attachments/assets/6760a66d-b716-4ffd-b897-68a579a826a9)

#### Figure 9. Malaria incidence adjusted for testing and reporting rate




The visualization in Figure 9 offers a refined perspective on malaria incidence in Sierra Leone from 2015 to 2023, incorporating adjustments for both testing and reporting rates. Examining the chronological progression of maps and their accompanying bar graphs reveals a complex evolution of malaria incidence patterns. The period from 2015 to 2019 is characterized by a heterogeneous distribution of incidence rates across Sierra Leone's chiefdoms. During these initial years, numerous areas, particularly in the central and eastern regions, exhibited elevated incidence rates, visually represented by orange and red hues on the maps. A notable shift in this pattern emerges from 2020 onwards. The maps for the years 2020-2023 illustrate a marked decline in high-incidence areas, with a transition towards more moderate (yellow and light blue) and low (dark blue) incidence rates across a significant number of chiefdoms. This trend is mirrored in the accompanying bar graphs, which depict a clear migration towards lower incidence categories. By 2023, an increasing proportion of chiefdoms fall within the 50-250 per 1000 population range. The detailed map for 2023 provides a granular view of the current malaria situation in Sierra Leone. While it confirms a general trend towards lower incidence rates across much of the country, it also highlights the persistence of higher incidence pockets, particularly in some southern regions.  

 A comparison between the first and second levels of adjustment reveals significant insights into Sierra Leone's malaria landscape. The second-level adjustment, which accounts for both testing and reporting rates, generally indicates higher incidence rates across all years, suggesting a more substantial malaria burden than initially apparent. While both sets of maps demonstrate similar overall trends, the second-level adjustment exposes more areas with higher incidence rates, particularly in earlier years, indicating that underreporting may have obscured the true extent of malaria transmission in certain regions. Although both adjustments show a general decline in incidence over time, the second-level adjustment suggests this decline may be less pronounced than originally thought, with a more evident persistence of higher incidence areas, especially in southern regions. The bar graphs for the second-level adjustment depict a more gradual shift towards lower incidence categories over time, implying a more nuanced progression in malaria control efforts. This refined adjustment, incorporating both testing and reporting rates, offers a more accurate representation of malaria incidence in Sierra Leone, uncovering a higher overall burden and emphasizing the importance of addressing potential underreporting. Such a detailed picture is invaluable for guiding targeted interventions and optimizing resource allocation in the country's ongoing battle against malaria.

### Malaria incidence adjusted for testing, reporting and healthcare use
**Figure 10** illustrates the results of the third level of incidence adjustment according to WHO methodology, which accounts for care-seeking behavior in Sierra Leone from 2015 to 2023. This adjustment, which considers the use of private healthcare facilities and cases where individuals do not seek formal medical care, reveals a more comprehensive picture of malaria incidence across the country.
Assumptions:  i)The routine data available for this analysis is reported only by public health facilities, ii) The care seeking rate between 2015 and 2023 is the same as the recorded in the DHS 2019, iii) The care seeking behavior patterns in children is similar to that in adults, iv)The TPR among fevers who seek care in the private sector or who did not seek care is approximately the same as for those who seek care from the public sector.


![care seeking active hf](https://github.com/user-attachments/assets/695f3870-24a8-481a-8002-cfe8f1cbc3c9)

#### Figure 10. Malaria incidence adjusted for testing, reporting and care seeking rate

---


The third level of adjustment provides the most comprehensive view of the malaria situation to date. From 2015 to 2019, the maps show a widespread high incidence of malaria across many chiefdoms, with large areas colored in orange and red. However, a notable shift occurs from 2020 onwards, with a general reduction in high-incidence areas and a transition towards more moderate (yellow) and low (blue) incidence rates across numerous chiefdoms. The bar graphs corroborate this trend, showing a gradual increase in the proportion of chiefdoms falling into lower incidence categories over time. The 2023 map reveals that while many areas now experience lower incidence rates, some pockets of higher incidence persist, particularly in the southern and eastern regions of the country (Figure 10).

This third-level adjustment generally shows higher incidence rates across all years compared to both the first and second levels. The inclusion of care-seeking behavior in the calculation reveals an even greater burden of malaria than previously indicated. The spatial patterns in these maps show more extensive areas of high incidence, especially in the earlier years, suggesting that barriers to care-seeking may have masked the true extent of malaria transmission in certain regions. While all three levels of adjustment demonstrate a general decline in incidence over time, this third level suggests that the decline may be less pronounced than initially thought. The persistence of higher incidence areas is more evident, particularly in the southern and eastern regions. The bar graphs for this third-level adjustment show a more gradual and less dramatic shift towards lower incidence categories over time compared to the previous adjustments. This implies a more complex progression in malaria control efforts, highlighting the challenges in improving care-seeking behavior alongside other interventions.

### Summary of crude and adjusted incidence values according to WHO methodology

The set of maps in **Figure** 11 provides a summary of crude and adjusted incidence according to WHO methodology. These maps reveal progression of malaria incidence estimates in Sierra Leone from 2015 to 2023, showcasing the impact of various adjustment factors on our understanding of the malaria burden.

![combine incidence maps](https://github.com/user-attachments/assets/79bbee2d-1577-4080-a2e9-5178b71612fe) 

#### Figure 11. Summary of crude and adjusted incidence values according to WHO methodology

---

The crude incidence maps in the top row show a relatively optimistic picture, with many areas appearing to have low to moderate incidence rates, particularly in later years. However, as we move down through the subsequent rows of adjusted maps, we see a dramatic shift in the perceived malaria landscape. The second row, adjusted for testing rates, reveals a higher incidence across most chiefdoms. The third row, incorporating both testing and reporting rate adjustments, further intensifies the picture, with more areas showing elevated incidence levels. The final row, which adds care-seeking behavior to the adjustments, presents the most concerning view, with widespread high incidence rates across much of the country, especially in earlier years (Figure 11).

A key observation is the persistence of high-incidence areas in the southern and eastern regions across all adjustment levels, even as other parts of the country show improvement over time. The progression from crude to fully adjusted maps underscore the critical importance of accounting for testing rates, reporting practices, and care-seeking behaviors in accurately assessing the true burden of malaria. It highlights that reliance on unadjusted data may significantly underestimate the scale of the malaria challenge in Sierra Leone. While all map series show some degree of improvement from 2015 to 2023, the adjusted maps indicate that progress may be slower and less extensive than crude data suggest. This comprehensive view is essential for informing effective policy-making, resource allocation, and intervention strategies in the ongoing fight against malaria in Sierra Leone.


### Use of healthcare services in the Sierra Leone
The results shown in Figure 12, aggregated by administrative region (adm1), are derived from the latest DHS survey conducted in 2019 in Sierra Leone. They reveal significant heterogeneity in care-seeking rates across provinces and variations in the sectors utilized for care. The data indicate that public sector utilization is relatively high in certain regions, while private sector care-seeking remains low across most areas. These findings underscore the need to enhance case management at the community health worker (CHW) level and consider these disparities when planning prevention and management interventions at the community level (**Figure 12**).


![Untitled presentation (6)](https://github.com/user-attachments/assets/0718876a-c77a-41c9-924a-f48464370172)



![Untitled presentation (7)](https://github.com/user-attachments/assets/5ea37a64-0f67-49c2-aa40-bf4dea694b33)



![Untitled presentation (8)](https://github.com/user-attachments/assets/c7a60bcb-6ac5-4ad8-9f56-0c2cbe4a0ec3)


![image_85](https://github.com/user-attachments/assets/33609d4d-7f3e-4503-b077-cea4b48a9fb1)


#### Figure 12. Care-seeking rate in Sierra Leone

---
### Prevalence of Plasmodium falciparum 
The SLMIS study conducted in 2021 determined the prevalence of Plasmodium falciparum by microscopy and RDT in children. Findings suggested significant regional variations (Figure 13). The northern and eastern provinces exhibit consistently higher malaria prevalence rates across both age groups and diagnostic methods, while the southern and western provinces tend to have lower prevalence rates. Notably, there is a discrepancy in prevalence rates detected by Rapid Diagnostic Tests (RDTs) versus microscopy, with RDTs generally indicating higher rates of detection. District-level prevalence shows that RDT-detected malaria rates in children aged 6-59 months are equal to or higher than those in children aged 5-9 years across all districts. Conversely, microscopy-detected malaria prevalence in children aged 6-59 months is lower than in those aged 5-9 years in all districts (Figure 13).  

![Untitled presentation (12)](https://github.com/user-attachments/assets/f0abc089-26ce-4c79-a284-8d048af04936)


![Untitled presentation (13)](https://github.com/user-attachments/assets/4a6bc759-e3d0-4a5d-859b-367b050650ab)

#### Figure 13. Prevalence of Plasmodium falciparum (SLMIS 2021)

---

### All-cause mortality in children under five 
District-level estimates of all-cause u5 mortality rates were obtained from the SLDHS 2019 (Figure 14). 

In the absence of reliable community-level malaria mortality but when malaria is a key contributor to child mortality, the spatial distribution of AU5MR can be used as a proxy of the distribution of malaria mortality to guide decisions (Figure 14). In Sierra Leone, the under-five mortality rates vary by district, with the highest rates in Port Loko, Kenema, Moyamba, and Western Rural; moderate rates in Kambia, Bo, and Karene; and the lowest rates in Bonthe and Falaba. Districts with high under-five mortality rates should be targeted with enhanced healthcare and social support, strengthening health systems, monitoring data, addressing social determinants, and engaging communities in preventive practices.


![Untitled presentation (14)](https://github.com/user-attachments/assets/b0a1ceb8-fead-4ec2-8c2c-b89f0bd0f953)

#### Figure 14. Under-five mortality rate, all causes from SLDHS 2019
---

### Median malaria incidence between 2019-2023
To synthesize the incidence data observed over the past five years, we calculated the median values of both crude and adjusted incidences for the 2019-2023 period (Figure 15). The median incidence over these five years, adjusted for testing and reporting rates, was identified as the most appropriate metric to represent malaria transmission patterns in the community and to guide decision-making (Figure 15).

![Untitled presentation (15)](https://github.com/user-attachments/assets/f95c27dc-747d-4048-8691-eefaf28c3136)

#### Figure 15. Median Incidence 2019-2023 adjusted for testing and reporting rates 

---

### Final malaria epidemiological stratification map 

In order to obtain a final map that best represents the current epidemiology of malaria in Sierra Leone, the median value of incidence adjusted for reporting and testing (the second level of adjustment according to WHO methodology) between 2019-2023 was chosen (Figure 16).


![Untitled presentation (16)](https://github.com/user-attachments/assets/f7e85688-a1f8-4606-aef1-e308349c8f35)

#### Figure 16. final maps for risk estimation 

---
The use of the median incidence value leverages the richness of the available time series data (60 months of data for each chiefdom) to produce a central trend value per chiefdom that is not sensitive to extreme values. Moreover, taking five years of data allows us to cover the years before and after COVID-19. This approach best represents the annual incidence in each geographical unit. This comprehensive approach ensures a more accurate representation of malaria risk, informing targeted interventions and resource allocation to areas with the highest need (Figure 16).

### Case management 
Access to care
The distribution of health facilities in Sierra Leone, their 5km radius coverage areas, and population density are illustrated in four maps presented in Figure 17. This visual analysis is crucial for understanding healthcare accessibility across the country.


![Untitled presentation (18)](https://github.com/user-attachments/assets/a0524c6e-e186-4acd-a3c3-cd8931592e8a)
![Untitled presentation (19)](https://github.com/user-attachments/assets/d7c0c7b7-6827-41f9-a85f-6284a666f955)

#### Figure 17. Map for access to care decision-making
---
There are noticeable gaps in the 5km coverage areas, especially in the northern and eastern regions of the country. The western region, appears to have better coverage, while rural and more remote areas in the northern and eastern seem underserved (Figure 17).


### CHW density

A map illustrating CHW density in relation to healthcare access would be helpful for better targeting community case management expansion (Figure 18).

![Untitled presentation (20)](https://github.com/user-attachments/assets/45a2265b-d281-4321-bf45-bcd115beeba7)
#### Figure 18. CHW density

---
### CHW and access
Two key metrics are illustrated in the map presented in Figure 19: (1) the proportion of the population residing beyond a 5km radius from the nearest health facility, and (2) the number of Community Health Workers (CHWs) per 1,000 people within this underserved population.

![Untitled presentation (21)](https://github.com/user-attachments/assets/1b5fa490-ca1a-4bf1-8aa8-2e2cda56fbb0)

#### Figure 19. CHW and access
---
### Care-seeking behavior patterns

Nationally, there were little variations between children living in rural or urban areas, in different wealth quintiles or by mother’s education status (Figure 20).


![Untitled presentation (22)](https://github.com/user-attachments/assets/9ec46754-09c2-42cb-95d5-38de8127905f)

#### Figure 20. Care-seeking behavior
---
### PHUs and Hospital density per population
The distribution of hospitals across districts in Sierra Leone varies significantly. Only four districts - Western Urban, Rural, Bonthe, and Bombali - have more than one hospital per 100,000 population. Five districts fall into the category of having 0.6 to 1 hospital per 100,000 population, while six districts have a lower ratio of 0.1 to 0.5 hospitals per 100,000 population. Notably, the district of Falaba, with a population of 251,608, does not have any hospital at all, highlighting significant disparities in healthcare infrastructure across the country (Figure 21).

![Untitled presentation (24)](https://github.com/user-attachments/assets/f7d77dde-c31e-4bab-8c80-1e964e86bad2)

#### Figure 21. Health facilities density per population
---

### Uncomplicated case management – Testing rates

The proportion of children with fever who underwent testing during the Sierra Leone Demographic and Health Survey 2019 (SLDHS2019) is depicted in the figure below (Figure 22).

![Untitled presentation (25)](https://github.com/user-attachments/assets/bc806e19-5161-46bd-88ed-b89ee8e13328)

![Untitled presentation (26)](https://github.com/user-attachments/assets/6e296618-c051-44d4-9499-4bdd60b5484d)

![Untitled presentation (27)](https://github.com/user-attachments/assets/b03f4ade-3898-4ce0-99a8-8b0717fd0993)

#### Figure 22. Testing rate (DHS 2019)
---

### Uncomplicated malaria case management at HFs – Testing rates
Testing rates appear to have decreased across all age groups over the years, which may indicate a data quality issue. In 2023, the chiefdoms with testing rates below 75% were similar across all age groups. While the distribution of testing rates by age group is generally consistent across chiefdoms, the number of chiefdoms achieving testing rates above 95% is highest among 5-14-year-olds.
It is recommended that this information be reviewed regularly to identify chiefdoms with persistently poor performance in malaria case management. Such identification should prompt an investigation followed by an appropriate response (Figure 23).

![Untitled presentation (28)](https://github.com/user-attachments/assets/5d8bf2a4-f56b-46bd-b4c2-676481c0f043)
#### Figure 23. Testing rates for uncomplicated malaria in health facilities
---

### Uncomplicated malaria case management at HFs – Treatment rates
High treatment rates and presumptive treatment (indicated by green chiefdoms) are more commonly observed in children under 5 years old. Presumptive treatment (shown in dark green) became more prevalent in 2022 and 2023. However, a substantial number of chiefdoms still show treatment rates below 95% among confirmed patients. To address these issues, it is crucial to routinely review this information. This review should aim to identify chiefdoms with consistently poor performance in malaria case management, prompting investigations and appropriate responses where necessary (Figure 24).


![Untitled presentation (29)](https://github.com/user-attachments/assets/2b8eb7d0-e0ab-4da3-a6d0-3bca54b58015)

#### Figure 24. Treatment rates for uncomplicated malaria in health facilities

### Uncomplicated malaria case management at HFs – Presumed cases
Across time, higher numbers of presumed cases are consistently observed in the same chiefdoms, irrespective of population density (Figure 25).
The maps reveal consistent population patterns across Sierra Leone from 2020 to 2023, with fluctuations in presumed malaria cases, persistent high burdens in certain chiefdoms, and clear geographical disparities in malaria case distribution, even in areas with similar population densities. 
To reduce the malaria burden, it is recommended that, interventions be targeted in high-case chiefdoms, strengthen malaria surveillance, focus on community-based health efforts, allocate resources based on population density and burden, and maintain year-round monitoring to respond to possible increases in malaria case incidences.

![Untitled presentation (30)](https://github.com/user-attachments/assets/7c418bea-d878-44e4-bc45-36c02d7e0d1a)

#### Figure 25. Presumed cases

#### Uncomplicated malaria case management among CHWs – Testing rates

Data from CHWs gradually improved over the years but in 2023, there were several chiefdoms with <75% testing rates (Figure 26)
According to the NMCP Program, the CHW policy was revised in 2021 to capture educational level, gender, and easy- and hard-to-reach areas. This followed the revision of the data collection and reporting tools, and CHWs started using the revised tools effectively in 2023. The low testing rate is largely due to errors in the indicator definition on the numerator and denominator of the testing by CHWs.
According to the revised policy, only hard-to-reach CHWs are allowed to suspect and test using RDTs to confirm malaria before treatment. Ease-to-reach CHWs only suspect fever cases for malaria and refer. They are not allowed to test, confirm, or treat malaria cases, but their suspected fever cases are part of the denominator, which affects the testing rate at the community level. 

NMCP has identified this error and is working with DPPI to review the data collection and reporting tools. However, gaps remain in some northern and eastern regions, with notable regional variability in the testing rates.

![Untitled presentation (31)](https://github.com/user-attachments/assets/e9698c69-1c61-4cdb-9315-d99706c84b43)

#### Figure 26. CHWs malaria testing rates
---
### Uncomplicated case management among CHWs – Treatment rates
The quality of data from Community Health Workers (CHWs) has shown improvement over the years. In 2023 several chiefdoms report treatment rates below 75% (indicated in orange). Additionally, some chiefdoms continue to rely on presumptive treatments (shown in dark green), suggesting that diagnostic practices may not be uniformly implemented across all regions (Figure 27). 

![Untitled presentation (32)](https://github.com/user-attachments/assets/7a63843f-0555-4816-99c6-f41025ae16af)

#### Figure 27. CHW malaria treatment rates
---
### Severe case management – Hospital malaria mortality ratios
The Hospital malaria mortality ratios for the period from 2015 to 2023 are depicted in Figure 28. 


A consistently low hospital malaria mortality ratios is observed in the younger age groups, though with higher vulnerability, regional disparities in healthcare quality, particularly in northern and eastern regions, and an overall improvements in mortality ratios over time.
To further reduce malaria mortality, focus should be laid on improving care for these age groups, address the regional disparities through strengthened healthcare quality of services, ensure continuous monitoring, and engage communities in education about early treatment seeking.

![image_88](https://github.com/user-attachments/assets/eee1ecae-e1c6-48ee-ada0-de3619bf785a)

#### Figure 28. Hospital malaria mortality ratios
---

#### Case management – RDT stockouts
There are a few chiefdoms with health facilities that experienced stock-outs >10% of the HF-months per year. Some of these chiefdoms repeatedly have stock-outs for several years in a row (Figure 29). To ensure consistent RDT availability, targeted interventions, improved supply chain management, and regular monitoring are recommended in these high-stockout areas.

![Untitled presentation (34)](https://github.com/user-attachments/assets/9f5b3d7b-c4e6-42cc-a5b2-dc4476ad025b)

#### Figure 29. RDT stockouts per year

---
### Case management- Antimalarial stockouts
The stock-outs of injectable Artemether and Artesunate are illustrated in Figure 30. The maps reveal persistent stockouts of antimalarial drugs across various chiefdoms from 2020 to 2023, with many regions experiencing high stockout rates. To address these issues, it is recommended to enhance supply chain management, improve forecasting and distribution strategies, and strengthen monitoring and accountability mechanisms to ensure consistent drug availability and support malaria control efforts.

![Untitled presentation (35)](https://github.com/user-attachments/assets/d9e301dd-1975-4678-9b74-36f4c80500ab)

#### Figure 30. Antimalarial stock outs

---

The stock-outs of ACTs are illustrated in **Figure 31**. There were stockouts of Artemether & Lumefantrine (ACT) treatment doses across various chiefdoms from 2020 to 2023, with some chiefdoms experiencing high stockout rates, especially for the 12-tab and 24-tab formulations. To address these challenges, it is recommended to improve supply chain infrastructure, forecasting, and inventory management, as well as enhance monitoring and support for chiefdoms with ongoing stockout issues to ensure the continuous availability of ACTs.

![Untitled presentation (36)](https://github.com/user-attachments/assets/84f5f7ff-3513-4804-b9c2-a0d9368e58e2)

#### Figure 31. ACT stock-outs

---

### Vector control

#### Routine ITN distributions through EPI (Penta 3 & ANC visit)

In previous years, the reported operational coverage exceeded 100% (shown in yellow), indicating potential data issues. The 2023 data shows much lower operational coverage, which may reflect improved data quality. However, this also reveals that coverage requires significant improvement across nearly all districts in the country, which needs to be addressed through improved last-mile supply chain, data collection, validation, and reporting (**Figure 32**).

![Untitled presentation (37)](https://github.com/user-attachments/assets/2301c640-d2d4-45b9-8a51-29d6b0d617f9)

#### Figure 32. Coverage of ITN distribution through antenatal care visits
---
### Mass ITN campaigns
The ITN coverage by district for the 2017, 2020 and 2023 mass campaigns is shown in Figure 33. The ITN coverage data from 2017 to 2023 indicates significant improvements, with many districts reaching high coverage levels. However, some areas still have coverage below 75%, suggesting a need for intensified efforts, equitable distribution, and targeted interventions to ensure universal ITN coverage and effective malaria prevention. Digitalization of mass ITN campaigns is one of the strategies to improve universal coverage of ITNs as demonstrated in the 2023 mass campaign.

![image_86](https://github.com/user-attachments/assets/5e653dd3-be1b-49fc-a355-ce461e4b0d52)
#### Figure 33. Coverage of mass ITN distribution  
---
### School-based ITN campaigns

The chiedoms where ITN distribution in schools is currently carried out, as well as those where it will be conducted in the future, are shown on the map in Figure 34. The pilot of  School-Based Distribution (SBD) of ITNs in Sierra Leone was done in all 14 chiefdoms in Kono district. The planned expansion now covers five districts (Kambia, Tonkolili, Pujehun, Koinadugu and Bonthe). To ensure effective implementation, it is recommended that, adequate resources be provided, improve community engagement, and conduct evaluation to assess the impact of the SBD compared to non-SBD districts.

![image_40](https://github.com/user-attachments/assets/cc88c71d-cd04-451f-8ec3-605ea492af3b)


#### Figure 34. targeting of school-based ITN distribution (SBD)
---
### Household access

While access to at least one net was >60% in nearly all households in the country, only up to 50% of households had one net for every two people in 2019. Access was lower when evaluated in 2021. From 2019 to 2021, improvements in household ITN ownership in Sierra Leone are evident, with more districts achieving higher coverage levels. However, gaps remain in the adequacy of net distribution, with some districts still lacking enough nets to cover every individual, highlighting the need for continued efforts to both increase net availability and ensure sufficient coverage (Figure 35).

![image_5](https://github.com/user-attachments/assets/ac2ce0d5-45e8-4668-9631-5a2f2a53f49c)

Figure 35. Household ITN access (map)
In 2019, ITN access is generally lower in urban areas, the poorest and wealthiest populations. The bar charts below show that while rural households in Sierra Leone consistently have higher ITN ownership than urban households, with the gap narrowing recently, disparities persist, particularly in urban areas. Additionally, although ITN ownership has increased across all wealth quintiles, wealthier households generally have higher coverage, indicating the need for targeted interventions and outreach programs to ensure equitable ITN distribution and access for all socioeconomic groups (Figure 36).

![image_25](https://github.com/user-attachments/assets/b4533547-9f3a-437a-b4e2-a31d33dbe477)

#### Figure 36. Household ITN access (plot)
---

### Population ITN use

The population-level usage of nets is generally <70% in Sierra Leone. Among the households with at least one net, usage increases to >60% everywhere in the country, with some districts recording lower use than others. In total, access is a key determinant for ITN use in Sierra Leone, SBCC messages to maximize use-given-access can be targeted to areas with high access but low use of ITNs (Figure 37).

![image_28](https://github.com/user-attachments/assets/aaf0f5c3-82ab-43fe-b1db-5b7bf8d9f921)

#### Figure 37. Population ITN use

### Pregnant women ITN use

The usage of ITNs among pregnant women is generally <70% in Sierra Leone except for a few districts.  Among the households with at least one ITN, usage increases to >70% everywhere in the country, with some districts recording lower use than others. Thus, access is a key determinant for ITN use in Sierra Leone, SBCC messages to maximize use-given-access can be targeted to areas with high access but low ITN use (Figure 38).

![image_80](https://github.com/user-attachments/assets/e769086e-ebb2-4c3b-bdaa-61a5581182c1)

#### Figure 38. Pregnant women ITN use
---
### Population-level ITN use

In 2019, bed net use is slightly lower in urban areas, among men, wealthier individuals and individuals with primary or secondary education. The ITN usage is higher among rural residents, wealthier quintiles, and individuals with higher education, with overall improvements in usage over time but persistent disparities based on location, socioeconomic status, and education. Recommendations include targeted distribution and education campaigns in underserved areas and among lower wealth quintiles, with a focus on consistent ITN use, especially for vulnerable groups like pregnant women, to achieve universal coverage and enhance malaria prevention (**Figure 39**).

![image_28](https://github.com/user-attachments/assets/95886be4-75fd-4041-b850-b7ff467c76a7)

#### Figure 39. Population-level ITN use
---
### Net durability studies
This study was conducted in the districts of Bo and Moyamba seven months after the 2020 ITN mass campaign by PMI – VectorLink (Figure 40). 

![image_62](https://github.com/user-attachments/assets/61c519db-a4c1-4d9d-adeb-daaae6a773a9)

#### Figure 40. Net durability 
---
### Net use: 
Cohort ITNs were rarely used by children alone (<10% in both sites) and patterns of use with adults varied between sites, with nets more commonly shared by children and adults in Moyamba (54%) than Bo (43%). 
ITN survivorship: 
ITN survivorship combines the two aspects of durability (attrition and physical integrity) and is defined as the proportion of cohort ITNs originally received that are still in the possession of the household and in serviceable condition. 
Nets given away to others or lost for other or unknown reasons are excluded from this calculation.
Seven months following the campaign distribution, the proportion of surviving cohort ITNs was 92% in Bo and 85% in Moyamba (p=0.018). The lower level of survivorship for Olyset Plus ITNs in Moyamba district reflects the higher level of “torn” ITNs in this site.
When considering determinants of durability, Moyamba had higher levels of household risk factors for damaged nets, though a higher proportion of respondents reported seeing rodents in the last six months in Bo (Figure 40). 


### Indoor Residual Spraying (IRS)
The chiefdoms where IRS is implemented along with the most recent coverages are shown in Figure 41. 

![image_14](https://github.com/user-attachments/assets/c4a2ad9e-f1fb-45aa-83b7-675ebdf708f0)

#### Figure 41. IRS implementation and coverage

 ### IPTp operational coverage out of ANC1

The assessment of IPTp operational coverage is substantially affected by data quality issues (coverage >100% in several chiefdoms). Special efforts should be made to achieve near 100% coverage in all chiefdoms where coverage is currently <100% (Figure 42).

![image_46](https://github.com/user-attachments/assets/cc4abc0e-3631-439d-b1c1-69e8b355bd51)

#### Figure 42. IPTp operational coverage out of ANC1  

 ### IPTp effective coverage (DHS 2019)

In 2019, there were no significant socio-demographic differences that affected IPTp coverage nationally (Figure 43).

![image_77](https://github.com/user-attachments/assets/4e9f11ed-a4bd-43dd-9690-c63261ffc7bc)

#### Figure 43. IPTp effective coverage (DHS 2019)    
---
### IPTi (PMC) coverage out of target population
The assessment of IPTi is substantially affected by data quality issues (coverage >100% in most chiefdoms). Special efforts should be made to achieve near 100% coverage in all chiefdoms where coverage is currently <100% (Figure 44).

![image_95](https://github.com/user-attachments/assets/ea9e8d35-4879-4a06-94f4-4abd1af0ef9f)

#### Figure 44. IPTi (PMC) Coverage out of target population  
---
### Malaria vaccine plans for 2024

Latest scale-up plans submitted to GAVI includes all chiefdoms in the country except for Western urban. Among the selected chiefdoms for scale-up, 85% may end up being supported by GAVI (pending communication from them) (Figure 45). 

![image_63](https://github.com/user-attachments/assets/a74d95c0-d376-45e4-bd54-d1b4964f70cf)

#### Figure 45. chiefdoms where malaria vaccination is conducted
---
### Entomology
#### Insecticide resistance
The map below shows areas where insecticide resistance is monitored, insectariums are located, and entomological surveillance is carried out (Figure 46).

![image_15](https://github.com/user-attachments/assets/62652bbd-c4e5-4897-b1e3-6dc1e0bde3c1)

#### Figure 46. Location of entomological surveillance sites
---
### Malaria seasonality
---
#### Seasonality analysis

Seasonality can be explored for various purposes and through different approaches. In this analysis, confirmed malaria cases in children under-five and among all-ages from routine reported data, along with mean rainfall estimates per chiefdom from CHIRPS’ satellite imagery, were used to determine the seasonality of malaria transmission (Figure 47). Key questions explored include whether there are any districts in Sierra Leone with seasonal patterns indicating that SMC could be an effective strategy and when the rainfall and malaria case seasonality peaks in Sierra Leone occur, to be considered for implementation to maximize the effectiveness of interventions (Figure 47).

![image_29](https://github.com/user-attachments/assets/8880e0b9-02c5-4c80-828c-c23e11b07cde)

#### Figure 47. Rainfall vs cases (all ages and u5) for seasonality analysis
---
#### Profiling seasonality for SMC

To determine seasonality for SMC, data from January 2015 to December 2023 were analyzed, encompassing a total of 108 months of rainfall and malaria case data (Figure 48) This dataset was divided into 96 month-blocks, each representing a continuous 12-month period. For each month-block, the seasonality rule was applied to identify periods of high malaria transmission. This rule tests whether the sum of rainfall or malaria cases over any four consecutive months constitutes at least 60% of the sum over the corresponding 12-month period. If this condition is met for one or more consecutive month-blocks, a seasonality peak is identified. A district is classified as a seasonal district if it exhibits a consistent number of seasonality peaks over the evaluation period. 


![image_64](https://github.com/user-attachments/assets/663002b0-17cc-4bb7-afce-4f7bc525b089)

#### Figure 48. Profiling seasonality for SMC targeting

By using this methodology, we can accurately profile the seasonality of malaria transmission in Sierra Leone. This profiling is crucial for optimizing the timing and effectiveness of SMC interventions. Figure 49 shows the chiefdoms found to have a seasonal pattern.


![image_89](https://github.com/user-attachments/assets/94a24fe3-8d3e-4e60-ab71-49df14029ff9)
 
#### Figure 49. Seasonality map based on rainfall vs case peaks
----
Sierra Leone exhibits a very marked rainfall seasonality that is crucial for targeting SMC, a pattern not fully captured when solely exploring trends in malaria cases (Figure 49). The case data can be influenced by several factors, including the quality and completeness of reporting, the impact of other interventions occurring before the rainy season, and changes in care-seeking behaviour patterns, particularly if these behaviours are seasonal.

### Seasonality for implementation purposes – Rainfall
For implementation purposes, the rainfall peak period was identified for each district. This corresponds to the month in which the percentage change in rainfall compared with the previous month is the highest (Figure 50).

![image_47](https://github.com/user-attachments/assets/c74e4bb7-2b85-44da-b911-9bc517c2bc7f)

#### Figure 50. Rainfall peak detection (example of BO) 

The maps below show the beginning and the end of the rainy season, together with the peak rainfall, are shown in figure 51 and will be used to determine the beginning, end and number of SMC cycles to be carried out by chiefdom.

![image_6](https://github.com/user-attachments/assets/4a56ba2a-46cd-44e7-bbcc-8a98204ac3e4)

#### Figure 51. The onset of end and peak of the rainy season
---
### Seasonality for implementation purposes – Cases

The figure below identifies 4-month or 5-month periods that account for 50% to 60% of annual malaria cases (Figure 52). This highlights districts in Sierra Leone with concentrated malaria case peaks over 4 to 5 months, with varying peak periods from April to November, while some areas have more evenly distributed cases throughout the year.
It is recommended that malaria prevention efforts are tailored to align with peak transmission periods in each chiefdom/district, focusing resources on areas with the longest peak periods, maintaining year-round interventions in areas with evenly distributed cases, and regularly update strategies based on current data to adapt to shifts in transmission patterns.

![image_30](https://github.com/user-attachments/assets/fa0d1874-f81b-4a81-80da-f25943fc0056)

#### Figure 52. Seasonality for implementation purposes using cases

### Next steps

With the completion of malaria risk stratification and analysis of its determinants, our next steps focus on targeting malaria control interventions. This targeting will be based on WHO-defined criteria and consensus reached at the national level in Sierra Leone. We will then determine the optimal mix of interventions for each chiefdom in the country. The potential impact of implementing this tailored intervention package will be evaluated using mathematical modeling techniques. These models will also aid in budget optimization and resource prioritization.
This process will continue over the coming weeks. We will regularly update this report to reflect ongoing analyses, new findings, and the progress of our discussions. This iterative approach ensures that our strategies remain responsive to emerging data and stakeholder input.

### Conclusion

Epidemiological stratification and targeting of malaria control interventions in the light of WHO recommendations is an essential exercise in updating the national strategic plan and submitting funding applications to various funders. The current document, which is a preliminary version, summarizes the results obtained to date. This document is intended to be modified according to the amendments made by the various stakeholders and can in no way be considered as the final and official version of the Sierra Leone 2024 SNT. 


### References
1. 	World malaria report 2023 [Internet]. [cited 2024 Jan 8]; Available from: https://www.who.int/teams/global-malaria-programme/reports/world-malaria-report-2023
2. 	Sierra Leone Demographic and Health Survey 2019. 
3. 	Cibulskis RE, Aregawi M, Williams R, Otten M, Dye C. Worldwide Incidence of Malaria in 2009: Estimates, Time Trends, and a Critique of Methods. PLOS Medicine 2011;8(12):e1001142. 
4. 	Weiss D.J., Bertozzi-Villa A., Rumisha S.F., Amratia P., Arambepola R., Battle K.E., et al. Indirect effects of the COVID-19 pandemic on malaria intervention coverage, morbidity, and mortality in Africa: a geospatial modelling analysis. Lancet Infect Dis 2021;21(1):59–69. 
5. 	Battle KE, Lucas TCD, Nguyen M, Howes RE, Nandi AK, Twohig KA, et al. Mapping the global endemicity and clinical burden of Plasmodium vivax, 2000-17: a spatial and temporal modelling study. Lancet 2019;394(10195):332–43. 


### Appendices
Appendix 1: WHO incidence adjustment methodology

![image_65](https://github.com/user-attachments/assets/6eed0045-9bf7-4ea6-916a-91f99ea14cab)

Appendix 2: Seasonality per chiefdom

![image_7](https://github.com/user-attachments/assets/441aac88-0d2b-41cc-91ff-4672c365855d)

![image_18](https://github.com/user-attachments/assets/25c137c9-8da4-4153-b964-09b20efd702e)

![image_19](https://github.com/user-attachments/assets/807f9e18-ca79-4112-8ec4-b8106d2ba7a4)

![image_31](https://github.com/user-attachments/assets/4a5eb7df-bb1e-4c5f-b917-6bdc4f54e450)

![image_32](https://github.com/user-attachments/assets/6de612a3-a651-416e-91a3-11d49863b0a0)

![image_48](https://github.com/user-attachments/assets/98fca9b5-2aac-474e-96b0-1de73adf7469)

![image_49](https://github.com/user-attachments/assets/849b9ceb-1bea-4de5-a728-dee117cbc736)

![image_50](https://github.com/user-attachments/assets/4ee71c83-a81d-428c-bfa4-6cc221101645)

![image_66](https://github.com/user-attachments/assets/3c9ec195-233f-4888-b22a-3af233142556)

![image_67](https://github.com/user-attachments/assets/7fad971b-11c3-40c5-93c7-3f20f9261ef0)

![image_78](https://github.com/user-attachments/assets/54359687-fd52-48c5-a429-c068994fe9c4)

![image_81](https://github.com/user-attachments/assets/68da4c29-711f-4158-b65b-01e5bf8a3742)

![image_87](https://github.com/user-attachments/assets/00ea097f-219f-4371-98b1-711f1df22c96)

![image_96](https://github.com/user-attachments/assets/e0db9cc9-cf9c-4089-92f6-e951e357bac6)


### Data Management




```python

This script is designed to import multiple Excel files from a specified directory, check that the column names match across all the files, and then concatenate them into a single DataFrame if the columns are consistent. Here’s a step-by-step explanation of the code:

### Step 1: Import Necessary Libraries
```python
import pandas as pd
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import geopandas as gpd
from tqdm import tqdm
import dataframe_image as dfi
import datetime
```
- **pandas (`pd`)**: Used for data manipulation and analysis.
- **pathlib**: Provides a way to work with file paths, making it easier to locate files in a directory.
- **numpy (`np`)**: Useful for numerical operations, though not directly used in this script.
- **matplotlib (`plt`)** and **seaborn (`sns`)**: Used for creating plots and visualizations, though not directly used in this snippet.
- **geopandas (`gpd`)**: For working with geospatial data, not directly used here.
- **tqdm**: A library for displaying progress bars, not used in this snippet.
- **dataframe_image (`dfi`)**: Used for saving DataFrames as images, not used here.
- **datetime**: Provides classes for manipulating dates and times.

### Step 2: Define Directory and Load Files
```python
district_data_dir = './/data//Updated_Epi_Data_By_District_2015-2023'
input_files = [p for p in pathlib.Path(district_data_dir).iterdir() if p.is_file()]
sheets = {f: 'Sheet1' for f in input_files}
```
- **district_data_dir**: Specifies the directory where the Excel files are stored.
- **input_files**: Uses `pathlib.Path()` to iterate over the files in the directory. `iterdir()` lists all items in the directory, and `if p.is_file()` ensures only files (not subdirectories) are selected.
- **sheets**: A dictionary mapping each file path to the sheet name `'Sheet1'`, assuming all files have data in the same sheet.

### Step 3: Load Data from Excel Files into DataFrames
```python
raw_dfs = [pd.read_excel(file, sheet_name=sheets[file]) for file in input_files]
```
- **raw_dfs**: A list comprehension is used to read each Excel file into a DataFrame using `pd.read_excel()`. Each DataFrame is stored in a list called `raw_dfs`.

### Step 4: Check Column Names Consistency
```python
diff = []
for i in raw_dfs:
    for j in raw_dfs:
        if set(i.columns) == set(j.columns):
            diff.append(True)
        else:
            diff.append(False)
```
- **diff**: This empty list will store `True` or `False` values based on whether the columns match.
- **Nested Loop**: The outer loop (`for i in raw_dfs`) iterates over each DataFrame, and the inner loop (`for j in raw_dfs`) compares the columns of every other DataFrame to the current one.
  - **set(i.columns) == set(j.columns)**: Converts the columns of DataFrames `i` and `j` into sets and checks if they are equal. If they match, `True` is appended to `diff`; otherwise, `False` is appended.

### Step 5: Concatenate DataFrames If Columns Match
```python
if all(diff):
    raw0 = pd.concat(raw_dfs)
else:
    print('Check column names are all the same between files before concatenating')
```
- **all(diff)**: Checks if all elements in the `diff` list are `True`, meaning all files have consistent columns.
  - If `True`, `pd.concat(raw_dfs)` is used to concatenate all the DataFrames into a single DataFrame (`raw0`).
  - If `False`, an error message is printed, alerting you to check the column names.

### Step 6: Clear Memory
```python
raw_dfs = []
```
- **raw_dfs = []**: This clears the list of DataFrames (`raw_dfs`) to free up memory after the concatenation process is complete.

### Summary
This script is useful when you have multiple Excel files with similar structures that you want to combine into one. It ensures that the files have consistent column names before merging them, preventing potential data integrity issues. If the columns don't match, it will prompt you to review and correct the discrepancies.

```
### Full code
```python
import pandas as pd
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import geopandas as gpd
from tqdm import tqdm
import dataframe_image as dfi
import datetime

district_data_dir = './/data//Updated_Epi_Data_By_District_2015-2023'

input_files = [p for p in pathlib.Path(district_data_dir).iterdir() if p.is_file()]
sheets = {f: 'Sheet1' for f in input_files}

# gather all dataframes first to check column names
raw_dfs = [pd.read_excel(file, sheet_name = sheets[file]) for file in input_files]

# check that all columns names match between files, concatenate all files if so
diff = []
for i in raw_dfs:
    for j in raw_dfs:
        if set(i.columns) == set(j.columns):
            diff.append(True)
        else:
            diff.append(False)

if all(diff):
    raw0 = pd.concat(raw_dfs)
else:
    print('Check column names are all the same between files before concatenating')
    
# Clear memory
raw_dfs = []


```





















































































 


































 




 















 






















