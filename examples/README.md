# Examples

This directory contains example scripts and notebooks demonstrating how to use the pb-aesa package.

## basic_usage.py

Python script demonstrating the basic workflow:
- Setting up LCIA methods for planetary boundaries
- Running a MultiLCA assessment
- Calculating exploitation of Safe Operating Space
- Visualizing results

To run this example:
```bash
python basic_usage.py
```

## lcia_example.ipynb

Interactive Jupyter notebook with a comprehensive tutorial:
- Installing pb-aesa LCIA methods to Brightway
- Running single and multi-LCA analyses
- Displaying and interpreting LCIA results
- Calculating exploitation of Safe Operating Space
- Visualizing planetary boundary impacts
- Comparing multiple processes (template included)

To use this notebook:
```bash
jupyter notebook lcia_example.ipynb
```

## Requirements

To run these examples, you need:
1. A Brightway25 project with ecoinvent data
2. The pb-aesa package installed
3. Required dependencies (bw2data, bw2calc, pandas, matplotlib, etc.)
4. For the notebook: Jupyter notebook or JupyterLab

**Note:** Make sure to adjust the project name and database names to match your setup.
