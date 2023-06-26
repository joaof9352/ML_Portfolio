import pandas as pd

#pip install xlrd

dfs = []
for year in range(2001,2024):
    print(f'{year}')
    dfs.append(pd.read_excel("http://www.tennis-data.co.uk/"+str(year)+"/"+str(year)+".xlsx"))
    
df_final = pd.concat(dfs)
df_final = df_final.reset_index(drop=True) 
df_final.to_csv('tenis_dataset.csv', index=False)
