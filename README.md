# Special-sections-of-programming

## What

Study work in Jupyter Notebook about data analysis with Python.

- `Coursework/курсова.ipynb` - coursework "Data analysis with Python and Pandas".
  It uses the Pokemon dataset. It checks missing values (NaN), fills them,
  builds charts (line, bar, histogram, heatmap) and counts the Pearson correlation for each pair of columns.
- `лаб 4 (2).ipynb` - lab about NumPy arrays and Pandas DataFrames.
  The same queries run on both, and `timeit` measures the time.
  It uses the "Individual household electric power consumption" and Iris datasets.

## How to run

You need Python 3.11 and Jupyter.

```bash
pip install pandas numpy matplotlib seaborn plotly numba jupyter
jupyter notebook
```

Data is not in the repo. Download it and put it in the `data/` folder:

- Pokemon.csv - https://www.kaggle.com/datasets/abcsds/pokemon
- household_power_consumption.txt - https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption
- Iris loads from the internet, you do not need to download it.

## Results

- Coursework: NaN values are found and filled, charts are built, and the most correlated columns are found.
- Lab 4: the notebook compares the time of NumPy and Pandas for the same tasks.
