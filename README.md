# P-Value Calculator for PPC

This project was inspired by something I made on Excel a while ago as a PPC Manager. It automatically calculates the P-Value of hundreds of A/B tests and returns the ones that have reached statistical significance. I did this to practice coding with SQLite, Pandas, and a few other libraries.

## Context : 
  In PPC (Pay Per Click), an important part of the job consists in writing online ads and testing their effectiveness against one-another (known as 'A/B testing'). One common way to do this is to group them in pairs in different ad groups. Upon being triggered by a Google user, that ad group will then randomly pick one ad and show it to the user who will then decide to click on it, or not. The amount of times an ad gets shown ("impression") and clicked is recorded, and after a while we get to see which ad was the most enticing, i.e which one was the best at generating clicks. 
  
  The problem usually comes with interpreting the results. 
  
  For example, if Ad_1 has 3 clicks for 12 impressions (or a ratio of 25%), and Ad_2 has 6 clicks for 25 impressions (24%), it looks like Ad_1 is performing better than Ad_2, but a single extra click on Ad_2 would have massively tipped the balance (now 25% vs 28%), so how can we make sure that our results are due to one ad truely performing better than the other, rather than pure randomness? One method is to simply wait a certain amount of time, or wait until we reach a certain amount of total clicks or impressions, then pick a winner. A much better method is to calculate a p-value for our test, and only consider the results valid if the p-value is under a certain threshold (called "alpha", usually 0.05 in social sciences). 
  
  In the example above (6/25 vs 3/12), we get a P-Value of 0.47, meaning *if there was no real difference in effectiveness between the two ads*, Ad_1 would have a 47% chance (nearly a flip-coin) of outperforming Ad_2 by at least that kind a margin. That result is far above 0.05 (5%), therefore the test is not statistically significant.

PS: For the maths enthusiasts among you, those p-values were calculated by:
1. Considering each results as a binomial distribution, we can calculate their mean (μ, which is basically clicks/impressions). Once we have that, we are able to calculate their standard deviation (σ = sqrt(μ*(1-μ)), [find out why here](https://youtu.be/ry81_iSHt6E)) and with that standard deviation, we calculate the standard error of mean, which in this case is SEM = σ/sqrt(n).
2. With those numbers, we can then run a welch t-test, using t = (μ1 - μ2) / sqrt(SEM1^2 + SEM2^2)
3. And all that's left is to calculate the cumulative density function of that t-test. For that I simply used stats.norm.cdf from the scipy library.

For more information on how p-values of a/b tests work, please check [this article](https://towardsdatascience.com/the-math-behind-a-b-testing-with-example-code-part-1-of-2-7be752e1d06f), by mnguyenngo


## How it works: 
  This project uses data that I extracted from one of my PPC accounts (Ad_Report2.csv), 
  - create_table2.py will extract the headers from my csv file and use them to create a couple of tables on a new database.
  - fill_tables.py will upload the content of the csv file into those tables.
  - p-value2 will analyse each pair of ads within the same ad group and compare their results. Only the tests that have reached a low enough p-value will be shown in terminal. 


### To try it for yourself, simply open "create_tables2.py" and follow the instructions. 
 

