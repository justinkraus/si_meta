import pandas as pd
import re

df = pd.read_csv("si_topic_map.csv")
print("done reading!")


pattern_t = r"<topic>(.*?)</topic>"
pattern_l = r"<language>(.*?)</language>"
pattern_c = r"<culture>(.*?)</culture>"
pattern_p = r"<place>(.*?)</place>"
pattern_n = r"<name>(.*?)</name>"

df['mapped_topics'] = df['replacewith'].str.findall(pattern_t)
df['language'] = df['replacewith'].str.findall(pattern_l)
df['culture'] = df['replacewith'].str.findall(pattern_c)
df['place'] = df['replacewith'].str.findall(pattern_p)
df['name'] = df['replacewith'].str.findall(pattern_n)

# df['topics_all'] = df[['mapped_topics', 'language', 'culture', 'place', 'name']].values.tolist()
df['topics_all'] = df['mapped_topics'] + df['language'] + df['culture'] + df['place'] + df['name']

print(df.head(20))

df['topics_all_str'] = [', '.join(map(str, l)) for l in df['topics_all']]

print(df.head(20))


df.to_csv('si_topics_mapped_all.csv', mode='a', encoding = 'utf-8')