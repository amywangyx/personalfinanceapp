# personalfinanceapp
## how to run it

Run following code other than anaconda installed: 
```
pip install streamlit
pip install plotly
streamlit run app_test.py
```
plotly might need to updated in the conda instruction, so check their official websites \
You might need to change the directory path to make sure the directory is correctly saved \
(subject to fix the problem) 

Warning: 
due to the characteristics of caching in streamlit, \
after you finish to run analysis - i.e. finish everything, don't return back to adding data directly\
clear cache and rerun the entire thing in the upper right corner\
otherwise this time's data will be lost \
\
alternative way:\
please copy paste the myrecord.csv file to make sure your data is okay 

next step improvements to make: \

algorithms to predict how much you spent this month( abnormal / normal) \
better visualization for categorizing changes and tagging 