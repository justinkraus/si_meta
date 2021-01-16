import pandas as pd

##merge relevant columns (done once)

df = pd.read_csv("./si_combined.csv")
df2 = pd.read_csv("./si_combined_viz2.csv")

print("done reading!")

print(df.info(verbose=True))
print(df2.info(verbose=True, null_counts=True))

#drop extras from df
df = df.drop(columns=[
				'title_sort',
				'identifier',
				'guid',
				'object_type',
				'medium',
				'setName'])
print("done dropping!")

print(df.info(verbose=True))

#merge columns

dfv1 = pd.merge(df,df2[['record_ID', 'topics', 'name_label', 'name_content']],left_on='record_ID', right_on='record_ID', how='left',left_index=True).drop_duplicates(subset=['record_ID'])

print("done merging!")

dfv1.to_csv('si_combinedv1.csv', encoding='utf-8')
