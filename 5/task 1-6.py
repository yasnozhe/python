print("1 номер")
import os
import time
import json
import pandas as pd
df = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'name': ['Ivan', 'Anna', 'Petr', 'Elena', 'Sergey', 'Maria', 'Dmitry', 'Olga'],
    'age': [28, 34, 25, 41, 30, 29, 37, 26],
    'salary': [120000.0, 155000.0, 95000.0, 180000.0, 130000.0, 140000.0, 165000.0, 110000.0],
    'department': ['IT', 'Analytics', 'IT', 'Management', 'Analytics', 'HR', 'IT', 'Analytics'],
    'hiredate': pd.to_datetime([
        '2021-03-15', '2019-07-01', '2023-01-10', '2017-11-20',
        '2020-05-12', '2022-09-01', '2018-04-25', '2024-02-01'
    ]),
    'is_active': [True, True, True, True, False, True, True, True]
})
print(df.dtypes)


print("\n2 номер")
df.to_csv('data_with_index.csv')
df.to_csv('data_no_index.csv', index=False)
df_csv = pd.read_csv('data_no_index.csv')
print(df_csv.dtypes)
print("С индексом:", os.path.getsize('data_with_index.csv'), "байт")
print("Без индекса:", os.path.getsize('data_no_index.csv'), "байт")
df_csv_opt = pd.read_csv(
    'data_no_index.csv',
    dtype={
        'id': 'int64',
        'name': 'string',
        'age': 'int64',
        'salary': 'float64',
        'department': 'category',
        'is_active': 'bool'
    },
    parse_dates=['hiredate'],
    usecols=['id', 'name', 'salary', 'department', 'hiredate']
)
print(df_csv_opt.dtypes)


print("\n3 номер")
df_skills = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Ivan', 'Anna', 'Petr'],
    'skills': [
        ['Python', 'SQL'],
        ['Pandas', 'PowerBI', 'SQL'],
        ['Excel', 'Python']
    ],
    'profile': [
        {'role': 'analyst', 'remote': True},
        {'role': 'lead', 'remote': True},
        {'role': 'intern', 'remote': False}
    ]
})
for orient in ['records', 'columns', 'index', 'split']:
    filename = f'skills_{orient}.json'
    df_skills.to_json(filename, orient=orient, indent=2)
    print(f"{filename}: {os.path.getsize(filename)} байт")
with open('skills_records.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)
df_normalized = pd.json_normalize(raw_data)
print(df_normalized)


print("\n4 номер")
for codec in ['snappy', 'gzip', 'brotli']:
    df.to_parquet(f'data_{codec}.parquet', compression=codec, index=False)
for codec in ['snappy', 'gzip', 'brotli']:
    print(f"Parquet ({codec}): {os.path.getsize(f'data_{codec}.parquet')} байт")
t0 = time.perf_counter()
_ = pd.read_csv('data_no_index.csv')
print("CSV read (мс):", round((time.perf_counter() - t0) * 1000, 3))
t0 = time.perf_counter()
df_pq = pd.read_parquet('data_snappy.parquet')
print("Parquet read (мс):", round((time.perf_counter() - t0) * 1000, 3))
df_pq_cols = pd.read_parquet('data_snappy.parquet', columns=['name', 'salary'])
print(df_pq_cols)
print(df_pq.dtypes)


print("\n5 номер")
df_dept = df.groupby('department', as_index=False)['salary'].mean()
with pd.HDFStore('store_fixed.h5', mode='w') as store:
    store.put('employees', df, format='fixed', track_times=False)
    store.put('dept_salary', df_dept, format='fixed', track_times=False)
df_emp = pd.read_hdf('store_fixed.h5', key='employees')
with pd.HDFStore('store_table.h5', mode='w') as store:
    store.put('employees', df, format='table', data_columns=['department', 'salary'], track_times=False)
df_filtered = pd.read_hdf(
    'store_table.h5',
    key='employees',
    where="department == 'IT' & salary > 100000"
)
print(df_filtered)
print("HDF5 fixed:", os.path.getsize('store_fixed.h5'), "байт")
print("HDF5 table:", os.path.getsize('store_table.h5'), "байт")


print("\n6 номер")
records = []
t0 = time.perf_counter()
df.to_csv('bench.csv', index=False)
w_csv = (time.perf_counter() - t0) * 1000
t0 = time.perf_counter()
_ = pd.read_csv('bench.csv')
r_csv = (time.perf_counter() - t0) * 1000
records.append({
    'format': 'CSV',
    'size_bytes': os.path.getsize('bench.csv'),
    'write_ms': round(w_csv, 3),
    'read_ms': round(r_csv, 3)
})
t0 = time.perf_counter()
df.to_json('bench.json', orient='records', date_format='iso')
w_json = (time.perf_counter() - t0) * 1000
t0 = time.perf_counter()
_ = pd.read_json('bench.json', orient='records')
r_json = (time.perf_counter() - t0) * 1000
records.append({
    'format': 'JSON',
    'size_bytes': os.path.getsize('bench.json'),
    'write_ms': round(w_json, 3),
    'read_ms': round(r_json, 3)
})
report_df = pd.DataFrame(records)
print(report_df)