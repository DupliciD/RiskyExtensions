import os

import matplotlib.pyplot as plt
import pandas as pd

csv_folder = os.path.join(os.environ['HOME'], 'csvs')
csv_dumps = os.listdir(csv_folder)

full_csv = pd.concat(
    [pd.read_csv(os.path.join(csv_folder, csv_name)) for csv_name in csv_dumps]
).sort_values(
    by=['extension_id', 'name'], ascending=True
).drop_duplicates(
    ['extension_id', 'name']
)

# # Save top 1000 by risk
# full_csv.sort_values(by=['total_risk', 'extension_id', 'name'], ascending=False).drop_duplicates(
#     ['extension_id', 'name']
# ).head(1000).to_csv(os.path.join(csv_folder, 'top1000risk.csv'), index=False, encoding='utf-8')
#
# # Save top 1000 by users
# full_csv.sort_values(by=['users', 'extension_id', 'name'], ascending=False).drop_duplicates(
#     ['extension_id', 'name']
# ).head(1000).to_csv(os.path.join(csv_folder, 'top1000users.csv'), index=False, encoding='utf-8')
#
# # Save top 1000 by number of ratings
# full_csv.sort_values(by=['rating_users', 'extension_id', 'name'], ascending=False).drop_duplicates(
#     ['extension_id', 'name']
# ).head(1000).to_csv(os.path.join(csv_folder, 'top1000ratings.csv'), index=False, encoding='utf-8')
#
# # Save the full csv
# full_csv.sort_values(by=['extension_id', 'name'], ascending=True).drop_duplicates(
#     ['extension_id', 'name']
# ).to_csv(os.path.join(csv_folder, 'total.csv'), index=False, encoding='utf-8')

total_risk = full_csv.dropna(subset=['total_risk'])['total_risk']
# Risk score distribution histogram - uses logarithmic values for Y because of tendency towards low risk.
plt.figure()
total_risk.plot.hist(
    bins=10, logy=True, title='Risk score distribution of all extensions (LogY)'
).figure.savefig(
    os.path.join(os.environ['HOME'], 'RiskHist.png')
)
plt.close('all')

# Reviewed the numbers and found that there are only 3 extensions with risk scores above 4000, so those were removed.
plt.figure()
total_risk.sort_values(ascending=False).iloc[3:].plot.hist(
    bins=5, logy=True, title='Risk score distribution of all extensions with scores below 4000. (LogY)'
).figure.savefig(
    os.path.join(os.environ['HOME'], 'RiskHistNoOutliers.png')
)
plt.close('all')

# RiskHist for the top 1000 by risk
plt.figure()
total_risk.sort_values(ascending=False).iloc[:1000].plot.hist(
    bins=20, logy=True, title='Risk score distribution of top 1000 riskiest. (LogY)'
).figure.savefig(
    os.path.join(os.environ['HOME'], 'RiskHistTop1000.png')
)
plt.close('all')
