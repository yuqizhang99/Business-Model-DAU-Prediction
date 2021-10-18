# Business Model DAU prediction

## Problems
Normally,when we are optimizing performance of certain products, the unknown impact of recent variation of DAU, DNU or retention rate will impede our decision to some extent. Although A/B test can be used to deal with this problem, whether the effect analyzed through the test will show up again or at least reappear similarly is indeed affected by various controllable and uncontrollable factors. Therefore, a more general model is required.

## Definition
- DAU: abbr., daily active users, amount of users who log in and engage with your product on a daily basis,See Reference[1].
- DNU: abbr., daily new users, amount of users who

## Reference
-[1][DAU definition](https://www.profitwell.com/recur/all/daily-active-users/)
-[2][]

我们的问题
● 我们常常会存在此类疑问：
	○ 如果我提高今天或者近期的DNU、DAU、留存率，会对未来的DAU有何种影响？解决此问题可以采用A/B test，但是A/B test 是过去一段时间的策略效果，可能存在时间固定效应使得用于预测不够准确，并且A/B test可能受到样本偏差的影响。因此，我们希望存在一个可以直接估计未来DAU的模型。本文便是对这个模型的一次探索。
● 时间跨度：
	○ 我们希望测算模型的时间跨度可以尽可能长，现阶段采用30天为测试阶段的预测周期。
● 模型变量：
	○ 输入外生变量：第0天的DAU，第0天的活跃/新增用户 次日留存率、7日留存率和30日留存率，预测周期（第1天至第n天）的平均DNU，平均DNU采用预测周期的DNU的等权重平均
