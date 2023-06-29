import pandas as pd
import numpy as np 

#  Exemple de dataframe type méthanol
df1 = pd.DataFrame([0.38, 0.35, 0.36], columns=['254'], index=["MDMA", "PA23035", "FEST23155"])

#  Si le témoin MDMA est à 0.38 plus ou moins 0.05, attribuer multiindex = hPase Methanol 
if abs(df1.loc[df1.index=='MDMA'].values[0] - 0.38) < 0.05:
    df1.index=[np.repeat('Phase Methanol', len(df1.index)),np.array(df1.index)]
    print (df1)

elif abs(df1.loc[df1.index=='MDMA'].values[0] - 0.05) < 0.05:
    df1.index=[np.repeat('Général', len(df1.index)),np.array(df1.index)]

#  Exemple de dataframe type méthanol
df2 = pd.DataFrame([0.38, np.nan, 0.16, 0.30], columns=['MM'], index=["MDMA", "PA23035","PA23035", "FEST23155"])

""" if abs(df2.loc[df2.index=='MDMA'].values[0] - 0.38) < 0.05:
    df2.index=[np.repeat('Methanol', len(df2.index)),np.array(df2.index)]
    print (df2)

elif abs(df2.loc[df2.index=='MDMA'].values[0] - 0.05) < 0.05:
    df2.index=[np.repeat('Général', len(df2.index)),np.array(df2.index)]

for i in range(len(df2.index)):
    for j in range(len(df1.index)):
        print('comaprer les index',df2.index[i], ' ', df1.index[j])
        print('compar²er les rf', df2.iloc[i,0], ' ', df1.iloc[j,:0])
        if (abs(df2.iloc[i,0] - df1.iloc[j,0]) < 0.04 and (df2.index[i] == df1.index[j])):
            print('ok')
            print(df2.loc[df2.index[i]])
            print(df1.join(df2.iloc[i,:], how='outer'))
            # df1 = df1.join(df2.iloc[i,:], how="inner")
            break
    # df1 = df1.join(df2, how="outer")

df1.Name = 'Methanol' """
print(df1)    
print(df2)    

# print(df2)
# print(df1)
# print(df1.join(df2,how='outer'))

""" for i,j in df1.index:
    print(df1.loc[df1.index==(i,j)].values)
    # if df1.loc[df1.index==(i,j)].values - df2.loc[df2.index==(i,j)].values < 0.05:

 """
