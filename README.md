# README
## INTRO
**To display LaTeX equations in this doc, I suggest either installing [Chrome Extension:MathJax Plugin for Github](https://chrome.google.com/webstore/detail/mathjax-plugin-for-github/ioemnmodlmafdkllaclgeombjnmnbima) or downloading this doc**

to be continued
<br>

## DEFINITION
to be continued
<br>

## DENOTATION
1. $Day_{t}$ : initial day is denoted as $Day_{0}$,$Day_{t}$ is the day t days after $Day_{0}$
2. $DAU_{t}$ : daily active users on $Day_{t}$
3. $DNU_{t}$ : daily new users on $Day_{t}$
4. $R_{t}^{s}$: users who are active on $Day_{s}$ but also active on $Day_{s+t}$
<br>

## ASSUMPTION
- DAU and DNU are respectively homogenous as a group
  - a strong assumption, in fact DNU are different in properties in terms of their register day
- For each user, their activity is independent in terms of days
- Active users who are active in the days before $Day_{0}$ but are not active in $Day_{0}$ are considered as **lost users**(users that would not be active during the whole prediction period)
  -  corollary: $DAU_{0}$ and $DNU_{t}(t = 1,2,...,n)$ are heterogenous, since $DAU_{0}$ are not influenced by events during the prediction period
  -  other than innate inaccuracy of the model, this assumption also causes inaccuracy by excluding the possibility that so-called lost users will return during the prediction period, but is still accepted due to its convenience
- All metrics increase in a linear way, i.e. the increasing speed remains constant (a strong assumption, hopefully be solved in a more precise way in future versions)
<br>

## Theory
- Firstly, we define three states of activity: lost, survived and active. 
  - lost users will never return to the product again
  - survived users are not lost but not active on certain day
  - active users are the same as we normally refer to
  - Note：To become an active user one needs to become a survived user first. Being active is dependent on being survived. Therefore, in fact there are only two mutual independent and exclusive states： lost and survived
- Users' state on certain day is random variable denoted as X, X conforms to Bernouli Distribution,while
$$
\begin{equation} P(X) =
\begin{cases}
1-p & \text{X=lost}\\
p & \text{X=survived}
\end{cases}
\end{equation}
$$
Therefore,$p$ stands for the probability of being active on certain day
- A techinical assumption to deal with being survived and being active
  - For survived users, we can imagine it on the edge of being active, which will easily turn to active users under probability
$$
\begin{equation}
P( active | survived) = 1 - \epsilon 
\end{equation}
$$
  - Because $\epsilon \rightarrow 0^{+}$,
  suppose a $DAU_{t}$ has become active for m times, then the probability equals to $p^{t}(1-\epsilon)^{m}$(the one must survive all the time before $Day_{t}$)
  - Another technical assumption:
$$
\begin{equation}
(1-\epsilon)^{n} \to 1^{-}  
\end{equation}
$$
  - Then in this way, $p^{t}(1-\epsilon)^{m} \to p^{t}$
- Based on the assumption and corollary above, $DAU_{n}$ comes from two parts of users: 
  - $DAU_{0}$ who are also active on $Day_{n}$ 
  - $DNU_{t}(t = 1,2,...,n)$ who are also active on $Day_{n}$
- Formula:
$$
\begin{align}
DAU_{n} &= DAU_{0}     \cdot p^{n} + \sum_{t=1}^{n} DNU_{t} \cdot p^{n-t} \\
&= DAU_{0}     \cdot p^{n} + \overline{DNU}\cdot\sum_{t=1}^{n}  p^{n-t}\\
&= DAU_{0}     \cdot p^{n} + \overline{DNU}\cdot \frac{1-p^{t}}{1-p}\\
\end{align}
$$
  - Note: here $\overline{DNU}$ is a kind of weighted mean of DNU during the whole prediction period, by rigorous tests it is found that $\overline{DNU}$ can be approximately seen as the **arithmetic mean**
<br>

## MEASUREMENT
### 1. To measure p
if one is active on $Day_{t}$, the one must be the retained users on $Day_{t}$
and thus linear regression model is applicable in this case
$$
\begin{equation}
R_{t} = p^{t}  \Longleftrightarrow
ln(R_{t}) = ln(p) \cdot t + \epsilon_{t}
\end{equation}
$$
Because $DAU$ and $DNU$ are heterogenous, their "p" must be measured separately by their own retention rate
### 2. To deal with data production lag
Most of the time $R_{1}^{0}$,$R_{7}^{0}$,$R_{30}^{0}$ have time lag before its production due to their definition,so the latest available $R_{1}^{0}$,$R_{7}^{0}$,$R_{30}^{0}$ are required, See DAUPrediction.Model.get_paras
### 3. To exclude the seasonal influence
Normally, all metrics are seasonal with period of 7 days in real-world business. So 7-day average method is applied to calculate metrics of certain day.See DAUPrediction.Model.get_paras
<br>

## USAGE
1. Without machine learning:
Model.DAUPredictor provides method to estimate $DAU_{n}$.

>class DAUPredictor(t_end,dau0,avg_dnu,r1NU,r7NU,r30NU,r1AU,r7AU,r30AU,r1NUGo
al,r7NUGoal,r30NUGoal,r1AUGoal,r7AUGoal,r30AUGoal) 

| Parameters | Descriptions |
| ---- | ---- |
| t_end | integer, length of prediction period |
| dau0 | $DAU_{0}$ |
| avg_dnu| $\frac{1}{t_{end}}\sum_{t=1}^{t_{end}} DNU_{t}$, arithmetic mean of DNU during prediction period|
|r1NU,r7NU,r30NU| $R_{1}^{0}$,$R_{7}^{0}$,$R_{30}^{0}$ for $DNU$|
|r1AU,r7AU,r30AU|$R_{1}^{0}$,$R_{7}^{0}$,$R_{30}^{0}$ for $DAU$|
|r1NUGoal,r7NUGoal,r30NUGoal|expected $R_{1}^{t_{end}}$,$R_{7}^{t_{end}}$,$R_{30}^{t_{end}}$ for $DNU$|
|r1AUGoal,r7AUGoal,r30AUGoal|expected $R_{1}^{t_{end}}$,$R_{7}^{t_{end}}$,$R_{30}^{t_{end}}$ for $DAU$|
<br>

| Methods | Descriptions |
| ----| ---- |
| output() | to estimate $DAU_{t_{end}}$ based on input, return $DAU_{t_{end}}$,first addend of formula,second addend of formula,r1NU ,r7NU ,r30NU ,r1AU ,r7AU ,r30AU at the end of prediction period|
<br>

Due to the previously mentioned consideration, the model output is stable but there is fixed gap between predicted value and real value, in regard to prediction period. Thus a method is suggested: 
since gap is fixed and related to prediction period , we can use history data to predict dau on a known day,then calculate
$$
\begin{equation}
\beta_{t_{end}} = \frac{DAU_{t_{end}}}{\widehat{DAU_{t_{end}}}}
\end{equation}
$$
Then, $\beta$, partly accounted by  can be applied to adjust model output.

2. With machine learning
First let's define 
$$
\begin{equation}
DAU_{pre} = DAU_{0} \cdot p^{n}
\end{equation}

\\

\begin{equation}
DAU_{t} = \sum_{t=1}^{n} DNU_{t} \cdot p^{n-t}
\end{equation}
$$
Another method utilizes machine learning by learning from history data the same as  <code>sample.csv</code>
> sample.csv must satisfy the following requirement: 
> 

Two adjusting models are used:
> $$ \begin{equation}DAU_{adjusted} = b*DAU_{pre} + DAU_{t}\end{equation} $$
> $$ \begin{equation}DAU_{adjusted} = (a \cdot t + b)DAU_{pre} + DAU_{t}\end{equation} $$

class
DAUAdjustment.DAUAdjustor provides method to estimate $DAU_{n}$ in machine learning way.

> class DAUAdjustor(t_end,dau0,avg_dnu,r1NU,r7NU,r30NU,r1AU,r7AU,r30AU,r1NUGo
al,r7NUGoal,r30NUGoal,r1AUGoal,r7AUGoal,r30AUGoal) 

| Parameters | Descriptions |
| ---- | ---- |
| Day0 | 8-digit integer, e.g. 20210302 ｜
| period | integer, length of prediction period |
| expected_average_dnu| $\frac{1}{t_{end}}\sum_{t=1}^{t_{end}} DNU_{t}$, arithmetic mean of DNU during prediction period|
|r1NUGoal,r7NUGoal,r30NUGoal|expected $R_{1}^{t_{end}}$,$R_{7}^{t_{end}}$,$R_{30}^{t_{end}}$ for $DNU$|
|r1AUGoal,r7AUGoal,r30AUGoal|expected $R_{1}^{t_{end}}$,$R_{7}^{t_{end}}$,$R_{30}^{t_{end}}$ for $DAU$|
<br>

| Methods | Descriptions |
| ----| ---- |
| insertDatacase(database) | insert history data,database must be converted into pandas.DataFrame first, no return|
| buildTrainingSet(learning period) | build training set,learning period(integer) is required to longer than $\frac{period}{2}$ and 40 days, which count backwards from $Day_{0}$(not included)  |
| adjustDAU() | start adjustment process, the adjusted result is stored in <code>adjusted result.csv</code>  |
<br>
One experiment: $R^{2} = 0.8516$


## APPENDIX
### Time Series Decomposition
- test data is generated using time series decomposition
- time series is generated in the following way:
$$
\begin{equation}
y_{t} = T_{t} + S_{t} + I_{t}
\end{equation}
$$
- $T_{t}$,trend is generated by function $ y = ax+bx^{2}+c$
- $S_{t}$,seasonality is generated by Fourier series function $y=s_{1}sin(2\pi t)+s_{2}cos(2\pi t)+s_{3}sin(4\pi t)+s_{4}cos(4\pi t)+s_{5}$
- $I_{t}$, noise is generated by Gauss Distribution $N(0,\sigma^{2})$
<br>

## REFERENCE
1. Wikipedia contributors, "Decomposition of time series," Wikipedia, The Free Encyclopedia, https://en.wikipedia.org/w/index.php?title=Decomposition_of_time_series&oldid=1030301808 (accessed November 18, 2021).
2. "Simulating Electricity Prices with Mean-Reversion and Jump-Diffusion",MathWorks,https://www.mathworks.com/help/fininst/simulating-electricity-prices-with-mean-reversion-and-jump-diffusion.html
