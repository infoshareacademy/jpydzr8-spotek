import pandas as pd
from pandas.core.array_algos.putmask import setitem_datetimelike_compat

df_awiza = pd.read_csv(r'C:\Users\tomas\PycharmProjects\jpydzr8-spotek\archive\pre-advice.csv')
df_users = pd.read_csv(r'C:\Users\tomas\PycharmProjects\jpydzr8-spotek\db\users.csv')
df_type_delivery = pd.read_csv(r'C:\Users\tomas\PycharmProjects\jpydzr8-spotek\db\type_delivery.csv')
df_bp = pd.read_csv(r'C:\Users\tomas\PycharmProjects\jpydzr8-spotek\db\bp.csv')
df_type_hu = pd.read_csv(r'C:\Users\tomas\PycharmProjects\jpydzr8-spotek\db\type_hu.csv')

print(f'\n {df_awiza}')
print(f'\n --------------')
print(f'\n {df_users}')
print(f'\n --------------')
print(f'\n {df_type_delivery}')
print(f'\n --------------')
print(f'\n {df_bp}')
print(f'\n --------------')
print(f'\n {df_type_hu}')
print(f'\n --------------')