import pandas as pd

df = [[56.0, 'aids'], [50.0, 'dr'], [45.0, 'sss'], [44.0, 'piss']]
df = pd.DataFrame(df, columns=['ItemPrice', 'ItemDescription'])
df['GiftCardName'] = ''


df = df.loc[:, ['GiftCardName', 'ItemDescription', 'ItemPrice']]
df['GiftCardName'] = 'nig'
print(df)
