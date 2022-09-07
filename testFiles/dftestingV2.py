import pandas as pd
init = pd.read_csv('someNumbers.csv')


init.set_index('GiftCardName', inplace=True)
#print(init)
penis = 'Dan'
Dan = init.loc[penis, :]
Dan.reset_index(inplace=True, drop=True)
print(Dan)

#print(len(init.index))
#for x in range(len(init.index)):
    #print(init.index[x])
#index = init.index
#print(index)

#print(init.loc['Dan',0][0])














#init.set_index('GiftCardNames')

#print(init)
#gc_names = init['GiftCardName'].copy()

#gc_names = gc_names.drop_duplicates()
#gc_names = gc_names.to_frame()
#gc_names.reset_index(inplace=True, drop=True)

#print(gc_names)
#print(len(gc_names.index))
#for i in range(len(gc_names.index)):
    #print(str(gc_names.loc[i, 'GiftCardName']))

#print(init.loc['Dan'])




