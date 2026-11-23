import pandas as pd
import numpy as np
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['IT', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR'],
    'salary': [80000, 60000, 90000, 75000, np.nan, 85000, 70000, 62000],
    'bonus': [5000, 3000, np.nan, 4000, 2000, 6000, 3500, np.nan],
    'hire_date': pd.to_datetime(['2020-01-15', '2019-03-22', '2021-07-01', '2018-11-05',
                                 '2022-02-10', '2020-09-30', '2019-12-12', '2021-05-20'])
}