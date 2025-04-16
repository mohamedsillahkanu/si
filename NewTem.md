---
title: "Processing Routine Malaria Data"
weight: 1
order: 1
format: 
  html:
    toc: true
    toc-depth: 4
---

[[Back to Data Processing](../data-processing.qmd)]{.aside}

## Overview

In malaria surveillance, routine data from health facilities is crucial for monitoring disease burden, tracking intervention effectiveness, and identifying outbreak hotspots. This guide walks through processing routine malaria data files for use in surveillance, no-transmission (SNT) analysis.

The process involves importing multiple Excel files containing facility-level data, combining them, standardizing variable names, creating derived indicators, and aggregating to different administrative levels for analysis and visualization.

::: {.callout-note title="Objectives" appearance="\"simple"}
- Import and combine multiple Excel files containing routine malaria data
- Standardize variable names according to country data dictionaries
- Create derived indicators by combining related variables
- Reshape and aggregate data to different administrative levels
- Export processed data for further analysis
:::

## Step-by-Step: Processing Routine Malaria Data

### Step 1: Install required packages

First, we need to install packages that support data manipulation, reading and writing Excel files:

```r
# install or load relevant packages
pacman::p_load(
  dplyr,     # for data manipulation
  tidyr,     # for reshaping and tidying data
  writexl,   # for writing to Excel files
  readxl     # for reading Excel files
)

# Alternative installation approach without pacman
# install.packages("dplyr")
# install.packages("tidyr")
# install.packages("writexl")
# install.packages("readxl")
```

### Step 2: Load packages

Load the installed libraries to make their functions available in the current session:

```r
library(dplyr)
library(tidyr)
library(writexl)
library(readxl)
```

### Step 3: Set up your working environment

#### Step 3.1: Download the source data files

The file below is a zip file. Download and then extract it to a location on your computer:
[routine data](https://github.com/ahadi-analytics/snt-data-files/raw/99c7f670f38e46d6e872c941e45e11dd68844d4b/Routine%20data.zip)

#### Step 3.2: Set the working directory

Specify the folder location where the Excel files are stored so R can access them easily:

```r
# Replace with your actual file path
setwd("C:/Users/User/Downloads/routine data") 
```

::: {.callout-tip title="Working with File Paths"}
When specifying file paths in R:
- Use forward slashes (`/`) or double backslashes (`\\`) instead of single backslashes
- You can use `getwd()` to see your current working directory
- Consider using projects in RStudio for better path management
:::

### Step 4: Create a list of Excel files

Create a list of all Excel file paths in the working directory:

```r
file_paths <- list.files(pattern = "\\.xlsx$", full.names = TRUE)
```

### Step 5: Import data files into R

Use `lapply()` to read each file and store them in a list:

```r
data_files <- lapply(file_paths, read_excel)
```

### Step 6: Combine all data frames

Combine all individual data frames into one unified dataset:

```r  
df <- bind_rows(data_files)
```

### Step 7: Examine the combined dataset

Check the structure of the combined dataset by viewing the first few rows:

```r
print(head(df))
```

### Step 8: Standardize column names

Rename columns to follow a consistent naming convention based on country data dictionary:

```r
df <- df %>%
  rename(
    adm0 = orgunitlevel1,
    adm1 = orgunitlevel2,
    adm2 = orgunitlevel3,
    adm3 = orgunitlevel4,
    hf   = organisationunitname,
    allout_u5   = `OPD (New and follow-up curative) 0-59m_X`,
    allout_ov5  = `OPD (New and follow-up curative) 5+y_X`
    # Additional columns to be renamed...
  )
```

::: {.callout-note title="Variable Naming Conventions"}
This example uses a Sierra Leone data dictionary for malaria indicators. Naming conventions include:
- Administrative levels (adm0, adm1, adm2, adm3)
- Age groups in variable suffixes (u5 = under 5, ov5 = over 5, 5_14 = 5-14 years)
- Service delivery points (hf = health facility, com = community)
- Variables for confirmed cases (conf), suspected cases (susp), testing (test), etc.
:::

### Step 9: Process date information

Split the period name column into separate year and month columns:

```r
df <- separate(df, col = periodname, into = c("month", "year"), sep = " ")
```

### Step 10: Convert month names to numeric values

Convert month names to standardized numeric format:

```r
df$month <- recode(df$month, 
  "January" = "01",
  "February" = "02",
  "March" = "03",
  "April" = "04",
  "May" = "05",
  "June" = "06",
  "July" = "07",
  "August" = "08",
  "September" = "09",
  "October" = "10",
  "November" = "11",
  "December" = "12"
)
```

### Step 11: Create a standardized date column

Combine year and month into a standardized date format:

```r
df <- df %>%
  unite("date", year, month, sep = "-", remove = FALSE)
```

### Step 12: Create derived indicators

Calculate aggregate indicators by combining related variables:

```r
# Calculate total outpatient visits (all ages)
df$allout <- rowSums(df[c("allout_u5", "allout_ov5")], na.rm = TRUE)

# Calculate total suspected malaria cases (all ages, all sources)
df$susp <- rowSums(df[c(
  "susp_u5_hf", "susp_5_14_hf", "susp_ov15_hf",
  "susp_u5_com", "susp_5_14_com", "susp_ov15_com"
)], na.rm = TRUE)

# Additional derived indicators can be created similarly
```

::: {.callout-tip title="Working with NA Values"}
The `na.rm = TRUE` argument in `rowSums()` ensures that missing values (NAs) don't cause the entire sum to be NA. This is important when dealing with routine data that often has missing values.
:::

### Step 13: Aggregate data monthly at adm3 level

Create a monthly summary dataset at the administrative level 3:

```r
monthly_adm3_data <- df %>%
  group_by(adm1, adm2, adm3, year, month, date) %>%
  summarise(across(-c(adm1, adm2, adm3, year, month, date), sum, na.rm = TRUE), 
            .groups = "drop")
```

### Step 14: Export monthly aggregated data

Save the monthly aggregated dataset to Excel and CSV formats:

```r
# Replace with your desired output path
write_xlsx(monthly_adm3_data, "output/aggregated_data_monthly_adm3.xlsx")
write_csv(monthly_adm3_data, "output/aggregated_data_monthly_adm3.csv")
```

### Step 15: Aggregate data yearly at adm3 level

Create a yearly summary dataset at the administrative level 3:

```r
yearly_adm3_data <- df %>%
  group_by(adm1, adm2, adm3, year) %>%
  summarise(across(-c(adm1, adm2, adm3, year, month, date), sum, na.rm = TRUE), 
            .groups = "drop")
```

### Step 16: Export yearly aggregated data

Save the yearly aggregated dataset to Excel and CSV formats:

```r
# Replace with your desired output path
write_xlsx(yearly_adm3_data, "output/aggregated_data_yearly_adm3.xlsx")
write_csv(yearly_adm3_data, "output/aggregated_data_yearly_adm3.csv")
```

## Next Steps

Once your data is processed and aggregated:

1. **Validate the data** by checking for extreme values, missing data patterns, and temporal trends
2. **Visualize key indicators** using time series plots or choropleth maps
3. **Join with population data** to calculate rates and risk metrics
4. **Analyze trends** to identify hotspots or areas of concern

## Complete Code Reference

For reference, here's the complete code for processing routine malaria data:

```r
# Install required packages (if needed)
pacman::p_load(
  dplyr,
  tidyr,
  writexl,
  readxl
)

# Load libraries
library(dplyr)
library(tidyr)
library(writexl)
library(readxl)

# Set working directory
setwd("path/to/your/directory") 

# Get list of Excel files
file_paths <- list.files(pattern = "\\.xlsx$", full.names = TRUE)

# Read all files into a list
data_files <- lapply(file_paths, read_excel)

# Combine all data frames
df <- bind_rows(data_files)

# View combined data structure
print(head(df))

# Rename columns
df <- df %>%
  rename(
    adm0 = orgunitlevel1,
    adm1 = orgunitlevel2,
    adm2 = orgunitlevel3,
    adm3 = orgunitlevel4,
    hf   = organisationunitname,
    allout_u5   = `OPD (New and follow-up curative) 0-59m_X`,
    allout_ov5  = `OPD (New and follow-up curative) 5+y_X`,
    # Add other column renames as needed
    maladm_u5   = `Admission - Child with malaria 0-59 months_X`,
    maladm_5_14 = `Admission - Child with malaria 5-14 years_X`,
    maladm_ov15 = `Admission - Malaria 15+ years_X`
    # Additional columns as needed
  )

# Split period column
df <- separate(df, col = periodname, into = c("month", "year"), sep = " ")

# Convert month names to numeric format
df$month <- recode(df$month, 
  "January" = "01",
  "February" = "02",
  "March" = "03",
  "April" = "04",
  "May" = "05",
  "June" = "06",
  "July" = "07",
  "August" = "08",
  "September" = "09",
  "October" = "10",
  "November" = "11",
  "December" = "12"
)

# Create date column
df <- df %>%
  unite("date", year, month, sep = "-", remove = FALSE)

# Create derived indicators
df$allout <- rowSums(df[c("allout_u5", "allout_ov5")], na.rm = TRUE)
df$susp <- rowSums(df[c(
  "susp_u5_hf", "susp_5_14_hf", "susp_ov15_hf",
  "susp_u5_com", "susp_5_14_com", "susp_ov15_com"
)], na.rm = TRUE)

# Add other derived indicators as needed

# Aggregate monthly data
monthly_adm3_data <- df %>%
  group_by(adm1, adm2, adm3, year, month, date) %>%
  summarise(across(-c(adm1, adm2, adm3, year, month, date), sum, na.rm = TRUE), 
            .groups = "drop")

# Export monthly data
write_xlsx(monthly_adm3_data, "output/aggregated_data_monthly_adm3.xlsx")
write_csv(monthly_adm3_data, "output/aggregated_data_monthly_adm3.csv")

# Aggregate yearly data
yearly_adm3_data <- df %>%
  group_by(adm1, adm2, adm3, year) %>%
  summarise(across(-c(adm1, adm2, adm3, year, month, date), sum, na.rm = TRUE), 
            .groups = "drop")

# Export yearly data
write_xlsx(yearly_adm3_data, "output/aggregated_data_yearly_adm3.xlsx")
write_csv(yearly_adm3_data, "output/aggregated_data_yearly_adm3.csv")
```
