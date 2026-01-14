import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

os.chdir(r'c:\Users\MMO\desktop\Ethereum-Fraud-Detection-Using-AI\Assignment_02')

# Load data
df = pd.read_csv('Cleaned_Ethereum_Fraud_Detection.csv')

# 1. Class Distribution Plot
plt.figure(figsize=(8, 6))
sns.countplot(x='FLAG', data=df, palette='Set2')
plt.title('Class Distribution (FLAG)', fontsize=14, fontweight='bold')
plt.xlabel('FLAG', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.tight_layout()
plt.savefig('class_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: class_distribution.png")

# 2. Feature Distribution Histograms
plt.figure(figsize=(15, 12))
df.hist(figsize=(15, 12))
plt.tight_layout()
plt.savefig('feature_distributions.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: feature_distributions.png")

# 3. Boxplot for Outliers
plt.figure(figsize=(14, 6))
sns.boxplot(data=df.select_dtypes(include=np.number), orient='h')
plt.xlabel('Value', fontsize=12)
plt.tight_layout()
plt.savefig('boxplot_outliers.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: boxplot_outliers.png")

# 4. Correlation Heatmap
numeric_df = df.select_dtypes(include=['int64', 'float64'])
plt.figure(figsize=(16, 12))
sns.heatmap(numeric_df.corr(), cmap='coolwarm', linewidths=0.5, cbar_kws={'label': 'Correlation'})
plt.title("Correlation Heatmap (Numeric Features Only)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: correlation_heatmap.png")

# 5. Scatter Plot - Relationship Analysis
plt.figure(figsize=(10, 7))
sns.scatterplot(x='total transactions (including tnx to create contract', 
                y='total ether received',
                hue='FLAG',
                data=df,
                alpha=0.6,
                s=50,
                palette=['#1f77b4', '#ff7f0e'])
plt.title("Total Transactions vs Total Ether Received", fontsize=14, fontweight='bold')
plt.xlabel('Total Transactions (including tnx to create contract)', fontsize=11)
plt.ylabel('Total Ether Received', fontsize=11)
plt.legend(title='FLAG', labels=['Legitimate (0)', 'Fraud (1)'])
plt.tight_layout()
plt.savefig('relationship_scatter.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: relationship_scatter.png")

print("\nAll visualization images saved successfully!")
