# 🔍🌍 Econoscope: Forecasting Unemployment Rates


## 📑Table of Contents
- 📖[Project Overview](#project-overview)
- 🛠[Installation](#installation)
- 📊 [Dataset Creation](#dataset-creation)
- 🤖[Models](#models)
- 🚀[Usage & deployment](#usage)
- 📁[Files](#files)

## 📖Project Overview

**Econoscope** is a robust project aimed at analyzing and forecasting unemployment rates using cutting-edge machine learning techniques and time series analysis. The project leverages datasets from global organizations to provide insights into employment trends and predict future unemployment rates.

✨ Key Features:

- **Accurate Forecasts:** Utilizes advanced machine learning models to predict unemployment rates with high accuracy.
- **Interactive Visualizations:** Provides interactive charts and graphs to visualize historical and forecasted data.
- **User-Friendly Interface:** Easy-to-navigate interface for exploring forecasts and historical data.
- **Customizable Predictions:** Allows users to input custom parameters for tailored forecasts.
- **Comprehensive Data:** Leverages extensive datasets from global organizations for robust analysis.


## 🛠Installation

Clone repository:
```bash
git clone https://github.com/sofibrezden/econoscope.git
```

Create a Virtual Environment:
```
python -m venv .venv 
```
On Linux:
```
source .venv/bin/activate  
```
On Windows:
```
.venv\Scripts\activate
```

## **For backend:**

Install dependencies:
```
pip install -r .\app\requirements.txt
```
Run Flask server:
```
flask run
```

## For frontend:

Open a new terminal or use an existing one after activating the backend. Navigate to the frontend directory:
```
cd your-repo-name/frontend
```
Install dependencies using npm:
```
npm install
```
Start the React application:
```
npm start
```
## For visualization server:

Open a new terminal or use an existing one.

Navigate to the visualization directory:
```
cd your-repo-name/graphs
```
Install the required packages from the `requirements.txt` file:
```
pip install -r requirements.txt
```
Start the server:
```
python main.py
```
The application will be available on http://localhost:3000. Ready to use!

# 📊Dataset Creation
To analyze labor market trends and unemployment rates, two datasets were utilized:

### 🗂**ILOSTAT Dataset**
Provides unemployment rates globally, categorized by gender, age groups, and years (2000-2023). Key features include:

- **Value:** Unemployment rate.
- **Sex:** Male, female, and total.
- **Age:** Age groups.
- **Country:** Country name.
- **Year:** Year of data.

### 🗂**Kaggle "Global Unemployment Data" Dataset**
Contains annual unemployment rates (2014-2024) for countries worldwide, categorized by demographics such as gender and age groups. Key features include:

- **Country Name:** Country.
- **Indicator Name:** Type of unemployment indicator.
- **Age Categories:** Demographics by age.
- **Annual Rates:** Unemployment rates for years 2014-2024.

Additionally, the **Country-Continents Dataset** was used to add a "Continent" feature, enabling analysis at both country and continental levels. The datasets were merged to provide comprehensive data on unemployment rates across genders, age groups, countries, and continents.

### 🧹 **Handling Missing Data**
- Missing values were filled using averages for each country and year.
- Linear extrapolation was applied to estimate missing data for certain countries.
- Countries with insufficient data were excluded to ensure dataset reliability.

### ⚖️ **Balancing**
- The "Sex" column was balanced by computing missing "Total" values as averages of "Male" and "Female."

### 📈**Enhancements**
- Monthly unemployment data was calculated using labor force data from ILOSTAT, improving granularity for 27 countries.
- OECD data added monthly unemployment data for 24 more countries.

The final dataset contains **1,477 rows** and **16 columns**, ready for advanced analysis and forecasting.

# 🤖Models

Econoscope employs multiple machine learning models to forecast unemployment rates:

- **ARIMA:** A time series model combining autoregression, integration, and moving average components. It captures short-term dependencies and long-term trends, suitable for stable trends without seasonal effects.

- **SARIMA:** Extends ARIMA by including seasonal components. Effective for datasets with significant seasonal patterns, such as annual labor market cycles.

- **XGBoost:** A powerful gradient boosting algorithm that handles nonlinear relationships and multi-factor data. Ideal for capturing complex interactions but requires careful feature engineering for time-series tasks.

Each model is evaluated using key metrics such as **MSE**, **RMSE**, and **MAPE**.


# 🚀Usage
The Econoscope website is deployed and accessible via this link: 👉 **[Econoscope Live Website](https://econoscope.vercel.app/)**.

- The **backend** and **visualization server** are hosted on the **Render platform**, while the **frontend** is deployed on **Vercel**.
- The **PostgreSQL database** is also hosted on Render’s cloud infrastructure.

**Note:** Due to the free subscription plan on Render, requests to the backend and visualization server may experience delays of up to 50 seconds. This is expected behavior under the free-tier plan and does not impact the accuracy or functionality of the application.

To explore the forecasts and insights, simply visit the website and interact with the intuitive interface.

# 📁Files
- **app/:** Backend Flask application files.
- **frontend/:** React-based frontend files.
- **datasets/:** Dataset files used for analysis and forecasting.
- **graphs/:** Visualization server files.
- **notebooks/:** Jupyter notebooks for exploratory analysis and forecasting, including:

  - **creating_new_dataset&EDA.ipynb:** Covers dataset creation and EDA. Combines data from multiple sources (e.g., Kaggle, ILOSTAT), adds continent info, cleans data, analyzes trends, and explores correlations between unemployment, age, sex, and region.

  - **forecast_2025.ipynb :**  A notebook for forecasting unemployment rates for 2025. Evaluates model performance and visualizes forecasts.

  - **forecast_2026.ipynb :**  A notebook for forecasting unemployment rates for 2026. Evaluates model performance and visualizes forecasts.

  - **forecast_2027.ipynb :**  A notebook for forecasting unemployment rates for 2027. Evaluates model performance and visualizes forecasts.

# 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.