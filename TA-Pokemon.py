import pandas as pd
import py_stringmatching as sm
import fuzzy
import re

soundex = fuzzy.Soundex(10)
tok = sm.QgramTokenizer(qval=4)

names = pd.read_csv("TA_names.csv")
#names["name"] = names["name"].apply(lambda x: x.split(" ")[0])
names["ta_qgrams"] = names["name"].apply(tok.tokenize)
names["soundex_name"] = names["name"].apply(lambda x: fuzzy.nysiis(x))
names["ta_soundex_qgrams"] = names["soundex_name"].apply(tok.tokenize)

pokemon = pd.read_csv("pokemon.csv")
pokemon = pokemon[["Name"]]
pokemon["Name"] = pokemon["Name"].apply(lambda x: re.sub('[^a-zA-Z]', '', x))
print(pokemon.head(10))

pokemon["pokemon_qgrams"] = pokemon["Name"].apply(tok.tokenize)
pokemon["soundex_name"] = pokemon["Name"].apply(lambda x: fuzzy.nysiis(x))
pokemon["pokemon_soundex_qgrams"] = pokemon["soundex_name"].apply(tok.tokenize)

merged = names.merge(pokemon, how="cross")
print("done with merge")
jac = sm.Jaccard()
merged["jaccard_score"] = merged.apply(lambda x: jac.get_raw_score(x["ta_qgrams"], x["pokemon_qgrams"]), axis=1)
merged["soundex_jaccard_score"] = merged.apply(lambda x: jac.get_raw_score(x["ta_soundex_qgrams"], x["pokemon_soundex_qgrams"]), axis=1)
s = sm.Soundex()
merged["soundex_score"] = merged.apply(lambda x: s.get_raw_score(x["name"], x["Name"]), axis=1)
gen_jac = sm.GeneralizedJaccard()
merged["gen_jac_score"] = merged.apply(lambda x: gen_jac.get_raw_score(x["ta_qgrams"], x["pokemon_qgrams"]), axis=1)
affine = sm.Affine()
merged["affine_score"] = merged.apply(lambda x: affine.get_raw_score(x["name"], x["Name"]), axis=1)
merged = merged.sort_values(by="jaccard_score", ascending=False)
merged.to_csv("merged2.csv")
print("Done")