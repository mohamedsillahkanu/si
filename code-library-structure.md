# Getting Started with the Subnational Tailoring Code Library

This guide will help you understand the structure of our Quarto website-based code library for subnational tailoring, set up your environment, and begin analyzing the Sierra Leone example data.

## Library Structure

The SNT code library is organized as a multilingual Quarto website with comprehensive resources in English, French, and Portuguese:

```
project/
├── _quarto.yml           # Quarto website configuration
├── docs/                 # Generated website (do not edit)
├── english.qmd           # English homepage
├── french.qmd            # French homepage
├── portuguese.qmd        # Portuguese homepage
├── styles.css            # Custom CSS styles
├── ahadi_logo_blue.png   # Logo file
├── english/              # English content
│   └── library/          # Main library content
│       ├── data/         # Data management resources
│       ├── stratification/ # Stratification resources
│       └── interventions/  # Intervention analysis
├── french/               # French content (similar structure)
├── portuguese/           # Portuguese content (similar structure)
└── data/                 # Example datasets
    ├── raw/              # Original data
    └── processed/        # Cleaned data
```

## Key Components

The library is organized into major thematic sections across three languages:

1. **Data Assembly and Management**
   - Shapefiles
   - Health facilities
   - Routine cases
   - DHS data
   - Population data
   - Climate data
   - LMIS data
   - Modeled data

2. **Epidemiological Stratification**
   - Reporting analysis
   - Incidence calculation
   - Prevalence estimation
   - Risk categorization

3. **Stratification of Other Determinants**

4. **Review of Past Interventions**
   - Various intervention types (IPTp, IPTi, Routine ITN, Mass ITN, Malaria Vaccine, ANC, SMC, IRS etc)
   - Case management quality assessment

5. **Targeting of Interventions**

6. **Retrospective Analysis**

7. **Urban Microstratification**

## Prerequisites

### Required R Packages

The following packages are required before getting started:

- **tidyverse**: For data manipulation and visualization
- **here**: For project-relative file paths
- **janitor**: For data cleaning
- **readxl**: For reading Excel files
- **sf**: For spatial data handling
- **lubridate**: For date manipulation
- **scales**: For better plot scales
- **RColorBrewer**: For color palettes
- **quarto**: For rendering the website

### Required Software

- **RStudio**: Latest version recommended
- **Quarto**: Must be installed (comes with recent RStudio versions)

## Setting Up Your Environment

1. Clone or download the code library repository

2. Open the project in RStudio:
   - Navigate to the project folder
   - Open the .Rproj file (this activates the project environment)

3. Install the required packages if you haven't already

4. Preview the website:
   - In RStudio, use the "Render" button to preview the website locally
   - Alternatively, run `quarto preview` in the terminal

## The Power of the {here} Package

The `here` package helps you build file paths relative to the **project root**, making your code more **reproducible** and **portable**.

* `here()` always starts at the project root (usually where your `.Rproj` file lives)
* It avoids the need to call `setwd()`, which changes the working directory and can break your code on other machines
* Works seamlessly across scripts, folders, and collaborators

Instead of:

```
setwd("C:/Users/mohamed/Documents/project")
rio::import("data/dhis2.csv")
```

Use:

```
rio::import(here::here("data", "dhis2.csv"))
```

This ensures your file paths are consistent no matter where or how the script is run. For example, even if one collaborator's project is in `C:/Users/mohamed/Documents/project/` and another's is in `/Users/jane/work/dhis_project/`, the code using `here()` will still correctly locate `data/dhis2.csv` as long as both have the same folder structure within their project root.

## Downloading and Setting Up the Example Data

1. For each section, a link will be provided to download example data.

2. Extract the contents of the zipped folder

3. Move the extracted folder to your project's data/raw directory

4. Follow the instructions in the relevant data processing documents

## Navigating the Code Library

1. Choose your preferred language (English, French, or Portuguese) from the navigation bar
2. The sidebar contains all major sections of the code library
3. Each section contains detailed documentation and code examples
4. Code chunks in each document can be run interactively in RStudio
5. You can expand/collapse sections as needed using the sidebar controls

## Working with the Code Library

1. **Browse relevant sections**: Find the documentation related to your specific analysis needs
2. **Copy code examples**: Adapt the provided code to your specific data and context
3. **Connect with data**: Use the example data to practice before working with your own datasets
4. **Contribute**: Use the GitHub links to contribute improvements or new code examples

## Best Practices

1. **Use the here package**: Ensure file paths are consistent across environments
2. **Version control**: Consider using Git to track your adaptations
3. **Modularize your code**: Break complex operations into functions

## Troubleshooting Common Issues

- **File path errors**: Always use `here()` instead of absolute paths
- **Rendering issues**: Ensure Quarto is properly installed and updated
- **Data loading issues**: Check that the data is in the expected location and format
- **Working directory problems**: Make sure you're opening the R project file (.Rproj) directly

## Next Steps

After setting up your environment and downloading the example data:

1. Browse the Data Assembly and Management section to learn how to prepare your data
2. Explore the Epidemiological Stratification section to classify areas by malaria burden
3. Review the interventions section to analyze past intervention performance
4. Use these insights to develop tailored subnational strategies

The code library provides a comprehensive collection of tools and methods to support evidence-based decision-making for malaria control and elimination efforts.
