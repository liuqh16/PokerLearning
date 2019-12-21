# CFR 算法概述

## 不完美信息下的扩展式博弈问题（Imperfect-information extensive-form game)

该博弈问题可由五元组定义: $\{\mathcal{N},\mathcal{H},P(\cdot),f_c(\cdot),u_i(\cdot)\}$

* $\mathcal{N}$: 有限玩家集合
  * 例如对于两人博弈问题，$\mathcal{N}=\{1,2\}$。
* $\mathcal{H}$: 历史集合
  * 任一历史$h$(也被称为node)是由玩家们以及随机事件(chance)的行动$a$组成的序列，可记作$h=(a_0,a_1,...,a_n)$。
  * 定义可选行动集合: $A(h)=\{a:(h,a)\in\mathcal{H}\}, \forall h\in \mathcal{H}$。
  * 定义前缀历史(可达性): 若 $\exist a\in A(h')$ 使得 $(h',a)=h$，则称$h'\subset{h}$；若$h''\subset{h'},\ h'\subset{h}$，则$h''\subset{h}$。
  * 定义空历史: $\varnothing$，$\forall h\in \mathcal{H}, \varnothing\subset h$。
  * 定义末端历史集合: $\mathcal{Z}=\{z\in\mathcal{H}:\forall{h}\in\mathcal{H},h\neq{z},\ z\nsubseteq{h}\}$。
  * 任一历史$h$是当前状态下的所有信息的汇总，包括仅有某一玩家了解的私有信息。
* $P(\cdot)$: 指派函数
  * 从历史集合到玩家集合的一个映射: $\mathcal{H}\rightarrow\mathcal{N}\cup\{c\}$。
  * $P(h)$表示在历史$h$之后应该做出行动的玩家。
  * 若$P(h)=c$，则代表由随机事件做出行动。
* $f_c(\cdot)$: 随机函数
  * 对于由随机事件做出行动的历史，给出该历史下所有可能行动的概率分布。
  * $\forall{h}\in\{h:P(h)=c\}, \ f_c(\cdot\mid{h}):A(h)\rightarrow(0,1)且\sum_{A(h)}f_c(\cdot\mid{h})=1$
* $u_i(\cdot)$: 效用函数(回报)
  * 对于任一玩家$i\in\mathcal{N}$，从末端历史到实数集合的一个映射: $\mathcal{Z}\rightarrow\mathbb{R}$
  * 若$\mathcal{N}=\{1,2\},\ u_1\equiv{u_2}$，则称为两人零和博弈
  * 定义玩家$i$效用函数的范围: $\Delta_{u,i}=\max_zu_i(z)-\min_zu_i(z)$

### 信息集与信息分割

* 信息集(Information Set)是历史的集合，即$I\subseteq\mathcal{H}$，对于属于玩家$i$的任一信息集$I_i$，其中的任意两个历史$h,h'$对于该玩家而言都是无法区分的，也是应当被该玩家同等对待的。
* $\forall{h}\in{I_i},\ A(h)\equiv{A(I_i)},\ P(h)\equiv{P(I_i)}$
* 信息分割(Information Partition)是信息集的集合，记作$\mathcal{I}_i$，包含属于玩家$i$的所有信息集。
* 实际上，对于任一非末端历史$h\notin\mathcal{Z}$，每个玩家$i$的信息分割中都有且仅有一个$I_i\in\mathcal{I}_i$，满足$h\in{I_i}$。
* 定义信息集$I$的可达末端历史集合: $Z_I=\{z\in\mathcal{Z}:\exist{h}\in{I},\ h\subset{z}\}$，相应的历史$h$记作$z[I]$。

### 策略

* $\sigma_i(\cdot)$: 玩家$i$的策略是可选行动的概率分布
  $$\forall{I_i}\in\mathcal{I}_i,\ \sigma_i(\cdot\mid{I_i}):A(I_i)\rightarrow(0,1)且\sum_{A(I_i)}\sigma_i(\cdot\mid{I_i})=1$$
  * $\Sigma_i$: 玩家$i$的所有策略集合
  * $\sigma$: 策略组，包含所有玩家的策略，$\sigma=\{\sigma_i, \ \forall{i}\in\mathcal{N}\}$
  * $\sigma_{-i}$: 除了玩家$i$以外的其他玩家的策略组
* $\pi^\sigma(h)$: 历史$h$的抵达概率，每个玩家都按照策略组$\sigma$进行博弈
  $$\pi^\sigma(h)=\prod_{(h',a)\subseteq{h}}\sigma_{P(h')}(a\mid{h'})=\prod_{i\in\mathcal{N}\cup\{c\}}\prod_{(h',a)\subseteq{h}}\sigma_{P(h')=i}(a\mid{h'})=\prod_{i\in\mathcal{N}\cup\{c\}}\pi_i^\sigma(h)=\pi_i^\sigma(h)\cdot\pi_{-i}^\sigma(h)$$
  * $\pi_i^\sigma(h)$: 玩家$i$对于该抵达概率的贡献。
  * $\pi_{-i}^\sigma(h)$: 除玩家$i$以外的玩家(包括随机事件$c$)对该抵达概率的贡献。
  * $\pi^\sigma(I_i)=\sum_{h\in{I_i}}\pi^\sigma(h)$: 信息$I_i$的抵达概率，类似可以定义$\pi_i^\sigma(I_i),\ \pi_{-i}^\sigma(I_i)$。
  * $\pi^\sigma(h\rightarrow{z})=\prod_{(h',a)\subseteq{z},(h',a)\nsubseteq{h}}\sigma_{P(h')}(a\mid{h'})$: 从当前历史$h$抵达某一末端历史$z$的概率。
  $${\rm{if}}\ h\ {\rm{is\ finite\ sequence,\ }}\sum_{z\in\mathcal{Z}}\pi^\sigma(h\rightarrow{z})=1$$
* $u_i(\sigma)$: 玩家$i$在策略组$\sigma$下的期望回报
  $$u_i(\sigma)=\sum_{z\in\mathcal{Z}}\pi^\sigma(z){u_i(z)}$$

### 纳什均衡

* $BR(\sigma_{-i})$: 给定策略组$\sigma$，玩家$i$的最佳响应策略(Best response)
  $$u_i(BR(\sigma_{-i}),\sigma_{-i})\ge\max_{\sigma_i\in\Sigma_i}u_i(\sigma_i,\sigma_{-i})$$
* $\sigma^{NE}$: 纳什均衡(策略组)，每一位玩家都采用最佳响应策略
  $$\forall{i\in\mathcal{N}},\ u_i(\sigma_i^{NE},\sigma_{-i}^{NE})\ge\max_{\sigma_i\in\Sigma_i}u_i(\sigma_i,\sigma_{-i}^{NE})即\sigma_i^{NE}=BR(\sigma_{-i})$$
* $\sigma^{\epsilon}$: $\epsilon$-纳什均衡，对纳什均衡策略的一个近似
  $$\exist\epsilon>0,\forall{i\in\mathcal{N}},\ u_i(\sigma_i^\epsilon,\sigma_{-i}^\epsilon)+\epsilon\ge\max_{\sigma_i\in\Sigma_i}u_i(\sigma_i,\sigma_{-i}^\epsilon)$$

## CFR算法

假设总计进行了$T$轮重复的博弈，考虑某一玩家$i$及属于该玩家的某一信息集$I_i$，记$\sigma^t$为第$t$轮的策略组。

* $R_i^T$: 整体平均后悔值——玩家对于所用策略的后悔程度
  $$R_i^T=\frac{1}{T}\max_{\sigma_i^*\in\Sigma_i}\sum_{t=1}^{T}(u_i(\sigma_i^*,\sigma_{-i}^t)-u_i(\sigma^t))$$
* $\bar{\sigma}_i^T$: $T$轮迭代后玩家$i$的平均策略
  $$\forall{I_i}\in\mathcal{I}_i,\forall{a}\in{I_i},\ \ \bar{\sigma}_i^T(a\mid{I_i})=\frac{\sum_{t=1}^T\pi_i^{\sigma^t}(I_i)\sigma^t(a\mid{I_i})}{\sum_{t=1}^T\pi_i^{\sigma^t}(I_i)}$$
* $u_i(\sigma,I_i)$: 反事实回报——除了玩家$i$以外的所有玩家按照策略$\sigma$行动并抵达信息集$I_i$后，玩家$i$的期望回报
  $$u_i(\sigma,I_i)=\frac{\sum_{h\in{I_i}}\{\pi_{-i}^\sigma(h)\cdot\sum_{z\in\mathcal{Z}}\pi^\sigma(h\rightarrow{z}){u_i}(z)\}}{\pi_{-i}^\sigma(I_i)}$$
* $\sigma\vert_{I_i\rightarrow{a}}$: 与策略组$\sigma$完全相同，除了玩家$i$在信息集$I_i$下只会采取行动$a\in{I_i}$
  $$\sigma_i\vert_{I_i\rightarrow{a}}(a^*\mid{I_i})=\mathbb{I}_{(a^*=a)},\ \forall a^* \in A(I_i)$$
* $R_{i,{\rm{imm}}}^T(I_i)$: 即时反事实后悔值——玩家对于某一信息集$I_i$下曾采取的行动的后悔程度，不难看出是通过“反事实回报”进行衡量的。
  $$R_{i,{\rm{imm}}}^T(I_i)=\frac{1}{T} \max_{a\in A(I_i)}\sum_{t=1}^T\pi_{-i}^{\sigma^t}(I_i)\Big(u_i(\sigma^t\vert_{I_i \rightarrow a},I_i)-u_i(\sigma^t,I_i)\Big)$$
  $$R_{i,{\rm{imm}}}^{T,+}(I_i)=\max\Big(R_{i,{\rm{imm}}}^T(I_i),\ 0\Big)$$
> ${\rm{Theory:}}\quad R_i^T\leq\sum_{I_i\in\mathcal{I}_i}R_{i,{\rm{imm}}}^{T,+}(I_i)$，可以通过最小化$R_{i,{\rm{imm}}}^{T,+}(I_i)$来最小化$R_i^T$

**算法关键**：固定信息集$I_i$，通过更新$\sigma_i(\cdot\mid I_i)$来分别最小化$R_{i,{\rm{imm}}}^{T,+}(I_i)$。

1. 已知前$T$轮迭代策略$\sigma^t(t=1,\cdots,T)$，计算当前信息集下每个行动的后悔值：

  $$\forall a\in A(I_i),\quad R_i^T(a\mid I_i)=\frac{1}{T}\sum_{t=1}^T\pi_{-i}^{\sigma^t}(I_i)\Big(u_i(\sigma^t\vert_{I_i\rightarrow a},I_i)-u_i(\sigma^t,I_i)\Big)$$
  $$R_i^{T,+}(a\mid I_i)=\max\Big(R_i^T(a\mid I_i), \ 0\Big)$$

2. 计算第$T+1$轮在该信息集下的迭代策略：

  $$\forall a\in A(I_i),\quad \sigma_i^{T+1}(a\mid I_i)=\begin{cases}
      \frac{R_i^{T,+}(a\mid I_i)}{\sum_{a\in A(I_i)}R_i^{T,+}(a\mid I_i)} &{\rm{if}}\;\sum_{a\in A(I_i)}R_i^{T,+}(a\mid I_i)>0 \\
      \frac{1}{|A(I_i)|} &{\rm{otherwise.}}
  \end{cases}$$

> $\rm{Theory:\quad}$若玩家$i$按照上述算法计算策略，则有$R_{i,{\rm{imm}}}^T(I_i)\leq\Delta_{u,i}\sqrt{\frac{|A_i|}{T}}$，进而有$R_i^T\leq\Delta_{u,i}|\mathcal{I}_i|\sqrt{\frac{|A_i|}{T}}$，其中$|A_i|=\max\limits_{h\in\mathcal{H},P(h)=i}|A(h)|$。

## Deep CFR

TODO：