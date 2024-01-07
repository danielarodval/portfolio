using CSV
using DataFrames
using Plots
using Statistics

#1. Data Loading:
df = DataFrame(CSV.File("iris.csv"))

#2. Exploratory Data Analysis (EDA):
# Display the first few rows of the dataset.
println(first(df, 5))
# Provide summary statistics of the dataset.
println(describe(df))
# Check for missing values in the dataset.
missing_columns = names(df)[map(x -> any(ismissing, df[!, x]), names(df))]
println(missing_columns)
#3. Data Manipulation:
# Create a new DataFrame containing only the columns "SepalLength" and "SepalWidth."
new_df = select(df, [:"sepal.length", :"sepal.width"])
println(new_df)
# Calculate the mean and standard deviation of each column in the new DataFrame.
println(mean(new_df[!, :"sepal.length"]))
println(std(new_df[!, :"sepal.length"]))

println(mean(new_df[!, :"sepal.width"]))
println(std(new_df[!, :"sepal.width"]))
#4. Data Visualization:
scatter(new_df[!, :"sepal.length"], new_df[!, :"sepal.width"], xlabel="Sepal Length", ylabel="Sepal Width", title="Sepal Length v Sepal Width")
#5. Conclusion:
