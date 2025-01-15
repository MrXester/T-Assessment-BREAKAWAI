# ML Engineering and Clustering Process

## Preprocessing
- Each column in the dataset was carefully prepared for clustering:
  - **One-hot encoding** was applied to categorical columns;
  - **Timestamp transformation**: Starting and completion timestamps were used to calculate the time to complete (in minutes). The start timestamp was replaced by the number of days since the beginning of the dataset;
  - **Normalization**: The resulting columns were normalized for uniformity;

## Correlation Analysis
- A correlation matrix was computed and [visualized](/05_IMAGES/Correlation_Matrix.png) for insights;

## Dimensionality Reduction
- Data dimensionality was reduced to 2D for visualization:
  - **T-SNE**: Used initially to uncover hidden patterns;
  - **UMAP**: Applied subsequently for more distinct cluster separation;

## Clustering
- **K-Means Clustering**:
  - Initial clusters were visible in the reduced space;
  - However, trivial clusters emerged, primarily due to simple binary splits (e.g., start date > 0.5);
  
## Enhanced Clustering with PCA
- PCA was applied to force the clustering to incorporate multiple features:
  - Primary component vectors were [saved](/01_CSV/out-PCA-variance.csv) as well as the [elbow plot](/05_IMAGES/elbow_plot.png);
  - This adjustment improved cluster diversity and produced satisfying [results](/05_IMAGES/PCA_plot.png);

## Interpretability with Decision Tree
- A [decision tree](/05_IMAGES/Decision_tree_plot.png) was created using the original data and the k-means clusters combined with PCA:
  - Highlighted patterns:
    - Clusters segmented by the service age, completion time, and invoice value;
    - Correlation observed between time to completion and the supplier's role;

## Key Observations
- The clusters revealed meaningful groupings and patterns:
  - A clear relationship between completion time and supplier role usually related to the last phases of an order;
  - Additional insights emerged, suggesting opportunities for further analysis;