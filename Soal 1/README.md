# Data Transformation and Anomaly Detection

## Prompt and Results

![image](https://github.com/user-attachments/assets/53886c4d-dbb5-46cc-bf01-c609062b0947)

Here's the GPT Prompt that I've put on ChatGPT, below are the result of the prompt:

![image](https://github.com/user-attachments/assets/55e8076c-527b-4ae1-b95c-6c7b5061a2e4)
![image](https://github.com/user-attachments/assets/ad899ee7-4325-449f-913e-3275e77be7ac)
![image](https://github.com/user-attachments/assets/45ef9410-5011-44a5-b20c-fe73440b2eaa)

---

## Overview

This project focuses on transforming and analyzing transaction data to uncover trends and anomalies (unexpected behaviors or patterns). It includes multiple scenarios that address data quality issues, enhance readability, and improve the detection of unusual transaction patterns. The transformations are focused on improving data aggregation (combining data into summary form), formatting, and visualizations for effective business insights.

---

## Data Transformation Process

1. **Handle Missing or Invalid Values:**
   - Replace values like `(not set)` with `NaN` or appropriate values depending on the context for better aggregation and analysis.

2. **Date Column Conversion:**
   - Convert the date column to a `datetime` type for easier manipulation and time-based analysis.

3. **Numeric Conversion:**
   - Convert relevant columns, such as `totalTransactionRevenue` and `productPrice`, to numeric formats to enable arithmetic operations and aggregation.

---

## Scenarios

### Scenario 1: Daily Total Transaction Revenue by Product

#### Problem:
The initial code provided by ChatGPT visualization displayed all products and their total daily transaction revenue, which resulted in an unreadable x-axis. Additionally, transaction amounts were displayed without specifying the currency.

#### Solution:
- Group data by `date` and `v2ProductName` to calculate the total revenue per product each day.
- Sort the data by `totalTransactionRevenue` and select the **top 10 products** for better readability.
- Format the revenue in **billions** and display the currency.

#### Process:
1. **Grouping by Date and Product:**
   - Aggregate revenue data on a daily basis for each product.
   
2. **Selecting Top 10 Products:**
   - Sort the aggregated data by `totalTransactionRevenue` and select the top 10 products.
   
3. **Currency Formatting:**
   - Convert revenue to billions and format with two decimal places: `apply(lambda x: f'${x/1e9:.2f}B')`.
   
4. **Visualization:**
   - Update the y-axis and plot title to indicate revenue in **USD billions**.

#### Outcome:
A bar chart displaying the **top 10 products** by total daily transaction revenue in **billions of USD** for better readability.

---

### Scenario 2: Anomaly Detection in Transaction Data for "Sport Bag"

#### Problem:
Anomalies were detected across all products, without focusing on a specific product or establishing a threshold for detecting significant changes.

#### Solution:
- Filter the data to focus on transactions for **"Sport Bag"**.
- Establish a **50% threshold** for detecting anomalies based on the previous day's transaction amount.

#### Process:
1. **Filtering Data for "Sport Bag":**
   - Analyze the transactions of the "Sport Bag" product specifically.
   
2. **Grouping by Date:**
   - Group the filtered data by date and calculate the total number of transactions for each day.
   
3. **Percentage Change Calculation:**
   - Calculate the percentage change in daily transactions using `.pct_change()` to track sharp increases or decreases.
   
4. **Anomaly Detection:**
   - Define thresholds to flag sharp increases (≥ 50%) and sharp decreases (≤ -50%) in transaction amounts.
   
5. **Visualization:**
   - Highlight anomalies with red dots on the transaction trend plot.

#### Outcome:
A line chart showing daily transaction trends for "Sport Bag" with anomalies visually highlighted. The output lists dates when anomalies occurred, marked by sharp increases or decreases in transactions.

---

### Scenario 3: Top 10 Cities by Total Transaction Revenue

#### Problem:
Many entries in the `city` column were either null or unspecified, and the most profitable city was labeled as "no name."

#### Solution:
- Rank cities from **2 to 11**, excluding "no name" entries.

#### Process:
1. **Grouping by City:**
   - Group data by city and calculate the `totalTransactionRevenue` for each city.
   
2. **Sorting by Revenue:**
   - Sort the cities in descending order based on total revenue.
   
3. **Selecting Top 10 Cities:**
   - Select the **top 10 cities** (excluding cities with missing or invalid names).
   
4. **Formatting Revenue:**
   - Format the revenue in billions using `set_yticklabels([f'${x/1e9:.2f}B' for x in plt.gca().get_yticks()])`.

5. **Visualization:**
   - Generate a bar chart showing the **top 10 most profitable cities**, with revenues displayed in billions of USD.

#### Outcome:
A bar chart displaying the top 10 cities by transaction revenue in **billions of USD**, excluding "no name" entries.

---

## Edge Case Handling

- **Missing Revenue Data:**
  - Filter or impute reasonable default values for cities and products with zero or missing revenue.
  
- **Duplicate Transactions:**
  - Handle potential duplicate transactions using the `transactionId` field to ensure data accuracy.

---
