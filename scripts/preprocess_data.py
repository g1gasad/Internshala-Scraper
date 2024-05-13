from datetime import datetime

custom_order = {'1 day ago':3, 'Just now':0, 'Today':2, '1 week ago':10, 'Few hours ago':1,
                '4 days ago':6, '2 days ago':4, '3 days ago':5, '5 days ago':7,'7 days ago':9,
                '6 days ago':8, '2 weeks ago':11, '3 weeks ago':12, '4 weeks ago':13, '5 weeks ago':14}

def preprocessor(df):
    df['sorted_order'] = df['Status'].map(custom_order)
    df = df.sort_values(by='sorted_order').drop('sorted_order', axis=1)
    date_variable = datetime.today().date()
    return df, date_variable