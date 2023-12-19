# オセロ
### 更新したらキャッシュをクリアする！
[https://ntaku256.github.io/AI/](https://ntaku256.github.io/AI/)

# PSO(粒子群最適化)
- 群知能の一種で、生物の群れを粒子として模倣している
- 昆虫の群れなどにおいては，適当な経路を発見した一匹に残りの群れが素早く追従することができるが，これを多次元空間において位置と速度を持つ粒子群でモデル化したもの

https://qiita.com/opticont/items/04a5b4ff41483966987f

# オセロAI
### 価値マップ
- マップに価値をつけ、おける場所の中からvalueが高い場所を選択する。
- 裏返したマスの価値の総和が最大となる手を選択してゆく。
- アルゴリズムでは、この価値マップをオセロで多くの駒をとれるように何度も試行錯誤して値を変えていく。
<img src="https://github.com/ntaku256/AI/blob/main/Source/StoneMap.png" width="50%">

### スコアの計算
- 左の図の例では、右の図のような場所を選択するとvalueが (-3) + (-1) + (-1) = -5 になる。
<img src="https://github.com/ntaku256/AI/blob/main/Source/OseroMap.png" width="100%">

```
置ける場所とvalue
  [2][5].value = -1
  [4][5].value = -1
  [5][5].value = -1
  [6][3].value = -1
  [6][4].value = -3
  [6][5].value = -1
  [7][1].value = -5

  ※同じ値では上から選ばれるので、今回は[2][5]が選ばれる
```
### PSO
1. それぞれのベクトルに、各マスのvalueが-30~30の価値マップをランダムに生成する。
```python
  def InitIndivisual():
    #8*8のマスそれぞれに-30 ~ 30 の価値を付与する。
    return np.random.uniform(-30,30,(8*8))
```
- 評価マップ
```
[  24.50813671  -29.2878167     9.04794791  -20.67778499    9.04018821   -2.40647408   -8.3115887    27.01061412
   -5.23585605  -10.35255287  -22.7822244    16.51181067  -15.84991705    6.78862383  -21.22315287   -7.65030773
  -27.69997706   22.56736182  -14.53154593   19.6416465     9.66053401   10.03510166  -27.20319744   -1.45975759
   29.59072925   25.34566733  -27.62213873   22.82363253   28.25320931    6.08110748  -13.87657254   13.78007481
  -20.27975359   -8.29864857   21.10178124   29.11842049   -6.60816536    9.95253957    8.94232069   25.37094617
    7.3748964    -7.15071738   10.60151921    5.9180152    15.87395565   -1.39311164  -17.46658634   26.40022369
   10.29530317   29.42593735  -14.95372671  -28.78418615   19.09774394  -16.58776741  -20.73929498    7.31926295
   17.8158737    24.30464656   22.28706443    8.22550678   24.77724914    5.77699278  -26.36270084    1.7537956 ]
```
2. 敵(enemy)としてベクトルをランダムに一つ選び、全てのベクトルと順番にオセロで対戦させる。
3. 順番に対戦したベクトルは、結果のスコア(自分の色のマス+空白のマス)と自分のベクトル内で一番スコアが高かったものと比較し、それよりも高かった場合はp_bestを更新してそのベクトルをp_best_vectorとして記録する。
4. 結果のスコア(自分の色のマス+空白のマス)と全部のベクトルの中で一番スコアが高かったものとも比較し、それよりも高ければg_bestを更新してそのベクトルをg_best_vectorとして記録する。
```python
  def CalcScores(self):
          #対戦する相手をランダムに決める
          enemy = np.random.randint(0,self.n_swarm,1)

          #決まったベクトルと全部のベクトルをそれぞれ対戦させる
          for i in range(self.n_swarm):
              new_score = EvalIndivisual(self.vectors[i],self.vectors[enemy])

              #自身のベクトルのベストスコアと比較し、大きければ更新、評価マップを保存
              if new_score > self.p_best_scores[i]:
                  self.p_best_scores[i] = new_score
                  self.p_best_vectors[i] = np.copy(self.vectors[i])

              #全ベクトルのベストスコアと比較し、大きければ更新、評価マップを保存
              if new_score > self.g_best_score:
                  self.g_best_score = new_score
                  self.g_best_vector = np.copy(self.vectors[i])
```
```
  スコア : (オセロの結果=自分の色があるマス+開いているマス)
  p_best_score[12] = 40 : 12番目のベクトル内の自己ベストが40 
  g_best_score = 50 : 全ベクトルの中でベストスコアが50
```
- 外部モジュール
```python
  # min から max までの整数をランダムに n 回とる
  np.random.randint(mini,max,n)

  # 型、値など全てを複製
  np.copy()

  # min から max までの少数をランダムに 8*8=64 回とる
  np.random.uniform(min,max,(8*8))
```
5. ベクトルの移動速度を求め、ベクトルを移動させる
   - ベクトルの移動速度は、もとの速度・p_best_vectorと現在のベクトルとの距離・g_best_vectorと現在のベクトルとの距離に重みを付けて足し合わせる。
```python
  def UpdateVectors(self):
          #全ベクトルの位置をそれぞれ更新する。
          for i in range(self.n_swarm):
              #p_best(自己ベストスコア)の重みをランダムにつける。
              r1 = np.random.uniform(0,1,self.vectors[0].shape)
              #g_best(全ベストスコア)の重みをランダムにつける。
              r2 = np.random.uniform(0,1,self.vectors[0].shape)

              #最適解(p_best,g_best)に近づくようにベクトルの移動速度を計算する。
              self.speeds[i] = self.w*self.speeds[i]+r1*(self.p_best_vectors[i]-self.vectors[i])+r2*(self.g_best_vector-self.vectors[i])

              #ベクトルの位置を更新する。
              self.vectors[i] = self.vectors[i] + self.speeds[i]
```
6. 2~5を繰り返し、最終的にはg_best_vectorの価値マップとそのときのスコアを出力する。(基本使うのは価値マップだけ)
```python
    n_indivisuals = 150  #ベクトル(価値マップ)の数 (=n_iter)
    n_iters = 10　       #ベクトルの更新回数

    def Run(self):
        for i in range(self.n_iter):
            #スコア計算
            self.CalcScores()
            #ベクトル位置更新
            self.UpdateVectors()
        #ベストスコアを出力する。
        return self.g_best_score,self.g_best_vector
```

# Instagram Algorithm
1. 初期化
```python
  def InitFlies(self):
          #ベクトル(評価マップ)を初期化
          self.vectors = np.array([InitIndivisual() for _ in range(self.n_flies)])

          #方針決定確率を初期化
          self.strategies = np.zeros([self.n_flies, 3])
          for i in range(self.n_flies):
              randoms = np.random.uniform(1, 100, 3)
              for j in range(3):
                  self.strategies[i][j] = randoms[j]/sum(randoms)

          self.likes = np.zeros(self.n_flies)
          self.best_fly_indices = np.zeros(self.n_clusters)
```
2. 敵(enemy)としてベクトルをランダムに一つ選び、全てのベクトルと順番にオセロで対戦させる。
```python
    def EvaluateLikes(self):
        #対戦する相手をランダムに決める
        enemy = np.random.randint(0,self.n_flies,1)

        #決まったベクトルと全部のベクトルをそれぞれ対戦させる
        for i in range(self.n_flies):
            self.likes[i] = EvalIndivisual(self.vectors[i],self.vectors[enemy])
        
```
3.
```python
    def Clustering(self):
        if self.centers is None:
            model = KMeans(n_clusters=self.n_clusters)
            result = model.fit(self.vectors)
            self.centers = result.cluster_centers_
        else:
            model = KMeans(n_init=1,n_clusters=self.n_clusters,init=self.centers)
            result = model.fit(self.vectors)
        self.labels = result.labels_
        self.center_speeds = result.cluster_centers_ - self.centers
        self.centers = result.cluster_centers_

        # best flies in each cluster
        best = np.zeros(self.n_clusters)
        self.cluster_like_average = np.zeros(self.n_clusters)
        for i in range(self.n_flies):
            label = self.labels[i]
            if (self.likes[i] > best[label]):
                best[label] = self.likes[i]
                self.best_fly_indices[label] = i

        # like average in each cluster
        for i in range(self.n_clusters):
            self.cluster_like_average[i] = np.mean(
                    [self.likes[j] for j in range(self.n_flies) if self.labels[j] == i])

        # average dist between each cluster
        self.center_dist_average = np.zeros_like(self.vectors[0])
        for i in range(self.n_clusters):
            for j in range(i+1,self.n_clusters):
                self.center_dist_average += (self.centers[i]-self.centers[j])
        self.center_dist_average /= sum(range(1,self.n_clusters))
```
4. d
```python
    def UpdateMaster(self, vector, label):
        index_table = [i for i in range(self.n_flies) if(self.labels[i]==label)]
        table = [self.likes[i] for i in index_table]
        target_fly_index = index_table[roulett(table)]
        center = self.centers[label]
        center_vector = (center - vector)*np.random.uniform(0,1)
        target_vector = (self.vectors[target_fly_index] - vector)*np.random.uniform(0,1)
        center_speed_vector = self.center_speeds[label]*np.random.uniform(0,1)
        return vector+center_vector+target_vector+center_speed_vector

```
5. s
```python
    def Run(self):
        fig = plt.figure()
        imgs = []
        for i in range(self.n_iters):
            self.EvaluateLikes()
            self.Clustering()
            self.UpdateFlieVector()
        self.EvaluateLikes()
        best_arg = np.argmax(self.likes)
        return self.likes[best_arg],self.vectors[best_arg]
```
