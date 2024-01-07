## Home Pricing Insights from Treasury and Index Fund Data

This project aims to predict median home sale prices in the United States by analyzing data from Treasury Securities Holdings, Morningstar Index Funds, and Zillow Median Home Sale Prices. The project uses various machine learning models to analyze the impact of economic indicators on the U.S. housing market.

### Key Features

- **Data Sources**: Utilizes data from Treasury Securities Holdings, Morningstar Index Funds, and Zillow.
- **Machine Learning Models**: Employs models like KNN Regression, Gradient Boosted Trees, Random Forest, and Support Vector Regression.
- **Data Preprocessing and Feature Selection**: Ensures data consistency and relevance by selecting impactful features.
- **Model Comparison and Tuning**: Evaluates models based on performance metrics and tunes them for optimal results.

### Dependencies

- Scikit-learn
- Pandas
- Numpy
- Matplotlib
- Seaborn

### Implementation

#### Data Collection and Preprocessing

1. **Data Integration**: Combines datasets from different sources with varying inception dates.
2. **Normalization**: Standardizes features using Scikit-learn's StandardScaler.

   ```python
   # StandardScaler implementation
   ```

#### Machine Learning Models

1. Multiple machine learning models are employed for analysis.
2. Hyperparameter tuning is done using GridSearchCV for optimal model performance.

   ```python
   # Example model implementation
   ```

#### Insights and Analysis

- Analyzing the feature importance across models to understand the economic indicators' impact on housing prices.
- Includes a detailed comparison of model performances before and after tuning.

### Results

- Gradient Boosted Regressor emerged as the most effective model.
- The project provides valuable insights for investors, policymakers, and industry practitioners.

### Figures and Visualizations

- Include figures and visualizations relevant to the project. (Upload images to GitHub and link them here)

![Figure 1: Data Consolidation](https://github.com/danielarodval/resume/blob/main/Python/Home%20Pricing%20Insights%20from%20Treasury%20and%20Index%20Funds/plots/Correlation%20Pre%20Feature%20Selection.png)

![Figure 2: Data Consolidation](https://github.com/danielarodval/resume/blob/main/Python/Home%20Pricing%20Insights%20from%20Treasury%20and%20Index%20Funds/plots/Correlation%20Post%20Feature%20Selection.png)

![Figure 3: Feature Importance 1 of 4](https://github.com/danielarodval/resume/blob/main/Python/Home%20Pricing%20Insights%20from%20Treasury%20and%20Index%20Funds/plots/Feature%20Importance%20GBT.png)

### Conclusion

- Discusses the practical implications of the findings.
- Suggests avenues for further enhancement like deep learning approaches and efficiency tuning.

### References

- Morningstar US Large Cap: [Link](https://indexes.morningstar.com/indexes/details/morningstar-us-large-capFSUSA00KH5)
- Zillow Research Data: [Link](https://www.zillow.com/research/data/)
- Other relevant references.

---

**Note**: Replace `link-to-figure-1`, `link-to-figure-2`, etc., with actual URLs of the images once they are uploaded to your GitHub repository. This README provides a comprehensive overview of your project and can be placed in the respective project directory on GitHub.