import pandas as pd
df = pd.read_csv('orders.csv')
df1 = df.copy()
df1['client_clean'] = df1['client'].str.strip().str.title()
df1['city_clean'] = df1['city'].str.strip().str.title()
df1['category_clean'] = df1['category'].str.strip().str.lower()
df1['product_clean'] = df1['product'].str.strip().str.upper()
df1['revenue'] = (df1['qty'] * df1['price'] * (1 - df1['discount'])).round(2)



df2 = df1.copy()
df2['revenue_rank'] = df2['revenue'].rank(method='dense', ascending=False).astype(int)
df2 = df2.sort_values(by=['revenue', 'order_date'], ascending=[False, True])



df3 = df2.copy()
df3['order_date'] = pd.to_datetime(df3['order_date'])
df3['order_year'] = df3['order_date'].dt.year
df3['order_month'] = df3['order_date'].dt.month
df3['order_quarter'] = df3['order_date'].dt.quarter
df3['order_weekday'] = df3['order_date'].dt.day_name()
df3['is_weekend'] = df3['order_date'].dt.day_of_week >= 5
df3['delivery_date'] = df3['order_date'] + pd.to_timedelta(df3['delivery_days'], unit='D')
df3['days_to_month_end'] = df3['order_date'].dt.days_in_month - df3['order_date'].dt.day



df4 = df3.copy()
cols = ['client_clean', 'order_date', 'product_clean']
df4['duplicate_group_flag'] = df4.duplicated(subset=cols, keep=False)
df4 = df4.sort_values(by='revenue', ascending=False).drop_duplicates(subset=cols, keep='first')
df4 = df4.sort_values(by='order_id', ascending=True)



df5 = df4.copy()
bins = [0, 1000, 5000, 20000, float('inf')]
labels = ['low', 'medium', 'high', 'vip']
df5['revenue_segment'] = pd.cut(df5['revenue'], bins=bins, labels=labels, right=False)
status_dict = {
    'new': 'новый',
    'paid': 'оплачен',
    'shipped': 'отправлен',
    'cancelled': 'отменён',
    'returned': 'возврат'
}
df5['status_ru'] = df5['status'].map(status_dict)
df5['promo_used'] = df5['promo_code'] != 'NO_PROMO'



df6 = df5.copy()
def get_priority(row):
    if row['status'] in ['cancelled', 'returned']:
        return 'archive'
    elif row['revenue'] >= 20000 and row['delivery_days'] <= 3:
        return 'A'
    elif row['revenue'] >= 5000:
        return 'B'
    else:
        return 'C'
df6['priority'] = df6.apply(get_priority, axis=1)
df6['manager_email'] = df6['manager'].str.strip().str.lower().str.replace(' ', '.') + '@shop.ru'
df6['final_comment'] = df6.apply(
    lambda row: f"{row['client_clean']}: {row['priority']}, {row['revenue_segment']}",
    axis=1
)
df6.to_csv('orders_final.csv', index=False)