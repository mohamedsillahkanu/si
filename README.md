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
  - [Indoor Residual Spray](#indoor-residual-spray)




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









 






















### Indoor Residual Spray 1

#### Step by Step explanation of the code

```python
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
```
- **Imports necessary libraries**:
  - `pandas` is for data manipulation.
  - `geopandas` is for working with geospatial data.
  - `matplotlib.pyplot` is for creating plots.
  - `ListedColormap` is used to create custom color maps.
  - `numpy` is imported but not used in the code (could be removed).

```python
shapefile_path = '/content/Chiefdom 2021.shp'
excel_file_path = '/content/irs_data.xlsx'
chiefdom_data_file = '/content/Chiefdom_data.xlsx'
```
- **Defines file paths** for the shapefile and two Excel files that will be used in the analysis.

```python
gdf = gpd.read_file(shapefile_path)
```
- **Reads the shapefile** into a GeoDataFrame (`gdf`), which contains the geographical boundaries and attributes for chiefdoms.

```python
df0 = pd.read_excel(excel_file_path)
df1 = pd.read_excel(chiefdom_data_file)
```
- **Reads the Excel files** into two separate DataFrames (`df0` and `df1`).

```python
df_merged = df0.merge(df1, how='left', on='adm3', validate='1:1')
```
- **Merges the two DataFrames (`df0` and `df1`)** on the column `'adm3'` using a left join. The `validate='1:1'` argument ensures that the merge is one-to-one, meaning each row in `df0` should match exactly one row in `df1`.

```python
gdf_merged = gdf.merge(df_merged, how='left', on=['FIRST_DNAM', 'FIRST_CHIE'], validate='1:1')
```
- **Merges the GeoDataFrame (`gdf`) with the merged DataFrame (`df_merged`)** on the columns `'FIRST_DNAM'` and `'FIRST_CHIE'` using a left join. This combines the geographical data with the attributes from the Excel files.

```python
bins_itn_cov = [75, 85, 95, 100]
labels_itn_cov = ['75-84', '85-94', '95-100']
```
- **Defines bins and labels** for categorizing IRS coverage percentages:
  - `bins_itn_cov` specifies the cutoff points for the categories.
  - `labels_itn_cov` assigns labels to each bin.

```python
colors = ['orange', 'green', 'yellow']
missing_color = 'gray'
```
- **Defines colors** to be used for the categories:
  - `colors` is a list of colors corresponding to the `labels_itn_cov`.
  - `missing_color` is the color used for missing data.

```python
cmap_itn_cov = ListedColormap(colors)
```
- **Creates a custom color map (`cmap_itn_cov`)** using the specified colors.

```python
gdf_merged['category'] = pd.cut(gdf_merged['irs_cov'], bins=[0] + bins_itn_cov, labels=['NA'] + labels_itn_cov, right=False, include_lowest=True)
```
- **Categorizes the IRS coverage data (`irs_cov`)**:
  - `pd.cut` segments the `irs_cov` data into bins and labels them.
  - Bins are defined with `[0] + bins_itn_cov` and labeled with `['NA'] + labels_itn_cov`.
  - `right=False` means the bins are left-inclusive.
  - `include_lowest=True` ensures that the lowest value is included in the first bin.

```python
fig, ax = plt.subplots(figsize=(6, 6))
```
- **Creates a figure and axes object** for plotting, setting the figure size to 6x6 inches.

```python
gdf_merged['color'] = gdf_merged['category'].map(dict(zip(labels_itn_cov, colors)))
gdf_merged['color'] = gdf_merged['color'].fillna(missing_color)
```
- **Maps categories to colors**:
  - `gdf_merged['category'].map(...)` assigns colors based on the `category`.
  - `fillna(missing_color)` fills in missing values with the `missing_color`.

```python
gdf_merged.plot(color=gdf_merged['color'], ax=ax, legend=False)
```
- **Plots the GeoDataFrame (`gdf_merged`)** using the colors assigned to each category.

```python
ax.set_axis_off()
```
- **Turns off the axis** so that no axis lines, ticks, or labels are displayed.

```python
gdf.boundary.plot(ax=ax, color='black', linewidth=1)
```
- **Plots the boundary of the original GeoDataFrame (`gdf`)** on top of the map with black lines and a line width of 1.

```python
gdf.dissolve(by='FIRST_DNAM').boundary.plot(ax=ax, color='white', linewidth=1)
```
- **Dissolves the GeoDataFrame (`gdf`) by `'FIRST_DNAM'`** and plots its boundary with white lines to highlight the chiefdom divisions.

```python
handles = []
for label, color in zip(['NA'] + labels_itn_cov, [missing_color] + colors):
    handles.append(plt.Line2D([0, 1], [0, 0], color=color, linewidth=10, label=label))
```
- **Creates custom legend handles**:
  - For each category (`label`) and corresponding `color`, a `Line2D` object is created to be used in the legend.
  - `linewidth=10` ensures the legend items are thick enough to be easily visible.

```python
fig.legend(handles=handles, title='2024 IRS coverage (%) at chiefdom-level in SL', loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=len(labels_itn_cov)+1, frameon=False)
```
- **Creates a custom legend** for the map:
  - `handles` are used for the legend items.
  - `title` sets the legend title.
  - `loc` and `bbox_to_anchor` position the legend.
  - `ncol` sets the number of columns in the legend.
  - `frameon=False` removes the border around the legend.

```python
plt.tight_layout()
plt.savefig('itn3.png', bbox_inches='tight')
plt.show()
```
- **Finalizes the plot**:
  - `plt.tight_layout()` adjusts the spacing to fit everything nicely.
  - `plt.savefig()` saves the plot as a PNG file.
  - `plt.show()` displays the plot.
 

### Full code

```python
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# File paths for shapefile and Excel data
shapefile_path = '/content/Chiefdom 2021.shp'
excel_file_path = '/content/irs_data.xlsx'
chiefdom_data_file = '/content/Chiefdom_data.xlsx'

# Read the shapefile into a GeoDataFrame
gdf = gpd.read_file(shapefile_path)

# Read the Excel files into DataFrames
df0 = pd.read_excel(excel_file_path)
df1 = pd.read_excel(chiefdom_data_file)

# Merge the two DataFrames on the 'adm3' column
df_merged = df0.merge(df1, how='left', on='adm3', validate='1:1')

# Merge the GeoDataFrame with the merged DataFrame on 'FIRST_DNAM' and 'FIRST_CHIE'
gdf_merged = gdf.merge(df_merged, how='left', on=['FIRST_DNAM', 'FIRST_CHIE'], validate='1:1')

# Define bins and labels for IRS coverage categories
bins_itn_cov = [75, 85, 95, 100]
labels_itn_cov = ['75-84', '85-94', '95-100']

# Define colors for the categories and for missing data
colors = ['orange', 'green', 'yellow']
missing_color = 'gray'

# Create a custom colormap using the defined colors
cmap_itn_cov = ListedColormap(colors)

# Categorize the 'irs_cov' column into bins and assign labels
gdf_merged['category'] = pd.cut(gdf_merged['irs_cov'], bins=[0] + bins_itn_cov, 
                                labels=['NA'] + labels_itn_cov, right=False, include_lowest=True)

# Create a figure and axis for the plot
fig, ax = plt.subplots(figsize=(6, 6))

# Map the categories to colors and fill missing values with the defined missing color
gdf_merged['color'] = gdf_merged['category'].map(dict(zip(labels_itn_cov, colors)))
gdf_merged['color'] = gdf_merged['color'].fillna(missing_color)

# Plot the merged GeoDataFrame with the assigned colors
gdf_merged.plot(color=gdf_merged['color'], ax=ax, legend=False)

# Turn off the axis
ax.set_axis_off()

# Plot the boundary of the original GeoDataFrame with black lines
gdf.boundary.plot(ax=ax, color='black', linewidth=1)

# Dissolve the GeoDataFrame by 'FIRST_DNAM' and plot its boundary with white lines
gdf.dissolve(by='FIRST_DNAM').boundary.plot(ax=ax, color='white', linewidth=1)

# Create custom legend handles
handles = []
for label, color in zip(['NA'] + labels_itn_cov, [missing_color] + colors):
    handles.append(plt.Line2D([0, 1], [0, 0], color=color, linewidth=10, label=label))

# Create a custom legend and position it above the map
fig.legend(handles=handles, title='2024 IRS coverage (%) at chiefdom-level in SL', 
           loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=len(labels_itn_cov)+1, frameon=False)

# Adjust layout, save the plot, and display it
plt.tight_layout()
plt.savefig('itn3.png', bbox_inches='tight')
plt.show()

```
[Download data used for generating the map below](https://worldhealthorg.sharepoint.com/:x:/r/sites/GMPSUR/Shared%20Documents/Country_Analytical_Support/Countries/SLE/WHO_SLE/2024_SNT/Analysis_Mohamed/Final%20Databases%20for%20modelers/intervention_data_stockout.xlsx?d=wd124fdd8e0c24ed6a177f34c5f5c630e&csf=1&web=1&e=3uztZ4)

![IRS IMAGE](https://github.com/user-attachments/assets/fb500ea3-05a0-46d1-b002-9b032cd2633d)
















