# Epidemiological stratification and subnational targeting (SNT) of malaria control interventions in Sierra Leone
![Sierra Leone Map](https://github.com/user-attachments/assets/1ce28ecc-191b-4f2d-bbfc-8944223bc993)

### Table of Contents
- [Summary](#summary)
- [Acknowledgement](#acknowledgement)


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
NMCP: 
Mr Musa Sillah-Kanu (NMCP-M&E unit, musasillahkanu1@gmail.com)
Dr Mac-Abdul Falama (NMCP-PM, abdulmac14@yahoo.com)
CHAI: 
Mr Victor Olayemi (volayemi@clintonhealthaccess.org)
Dr Valérian Turbé (vturbe@clintonhealthaccess.org)
Dr Celestin Danwang (cdanwang@clintonhealthaccess.org)
WHO: 
Mr Mohamed Sillah Kanu (sillahmohamedkanu@gmail.com)
Dr Omoniwa Omowunmi Fiona (omoniwao@who.int)
Dr Beatriz Galatas (galatasb@who.int)


### Step by Step explanation of the code

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

![IRS IMAGE](https://github.com/user-attachments/assets/fb500ea3-05a0-46d1-b002-9b032cd2633d)












