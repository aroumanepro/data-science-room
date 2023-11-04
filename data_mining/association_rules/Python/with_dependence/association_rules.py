# flake8: noqa
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth, association_rules


dataset = [
    ['Lait', 'Moutarde'],
    ['Pain', 'Oignons'],
    ['Steak', 'Pain', 'Oignons', 'Moutarde'],
    ['Lait', 'Oignons', 'Moutarde'],
    ['Pain', 'Oignons', 'Moutarde'],
    ['Steak', 'Pain', 'Oignons', 'Moutarde']
]

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)

frequent_itemsets = fpgrowth(df, min_support=0.6, use_colnames=True)
rules = association_rules(
    frequent_itemsets, metric="confidence", min_threshold=0.7)
