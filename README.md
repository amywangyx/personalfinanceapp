# personalfinanceapp
## how to run it
Updated ---
the app is deployed at https://personal-budgeting-analysis.herokuapp.com/
feel free to check it out

instructions (to make sure the analysis part is running):
1. check the agreement and add some numbers for bank account
2. in the add new data section, please add at least one line of income(>0), and one line of expense\
so that budgeting page will not report error(logic: you must have income to get your budget working) \
3. in the budgeting section, add one section (not n/a) to show you have budgeted couple things\
4. then congrats, in the run analysis section, you can see how you've done compared with what you should've done!

_____________________________________

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

next step improvements to make: 

algorithms to predict how much you spent this month( abnormal / normal) \
better visualization for categorizing changes and tagging 