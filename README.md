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
  def filtIndivisual(vector):
      for i in range(8*8):
          vector[i] = max(-30,min(30,vector[i]))
```
2. 敵(enemy)としてベクトルをランダムに一つ選び、全てのベクトルと順番にオセロで対戦させる。
3. 順番に対戦したベクトルは、結果のスコア(自分の色のマス+空白のマス)と自分のベクトル内で一番スコアが高かったものと比較し、それよりも高かった場合はp_bestを更新してそのベクトルをp_best_vectorとして記録する。
4. 結果のスコア(自分の色のマス+空白のマス)と全部のベクトルの中で一番スコアが高かったものとも比較し、それよりも高ければg_bestを更新してそのベクトルをg_best_vectorとして記録する。
```python
  def CalcScores(self):
          enemy = np.random.randint(0,self.n_swarm,1)
          for i in range(self.n_swarm):
              new_score = EvalIndivisual(self.vectors[i],self.vectors[enemy])
              if new_score > self.p_best_scores[i]:
                  self.p_best_scores[i] = new_score
                  self.p_best_vectors[i] = np.copy(self.vectors[i])
              if new_score > self.g_best_score:
                  self.g_best_score = new_score
                  self.g_best_vector = np.copy(self.vectors[i])
              self.scores[i] = new_score
```
5. ベクトルの移動速度を求め、ベクトルを移動させる
   - ベクトルの移動速度は、もとの速度・p_best_vectorと現在のベクトルとの距離・g_best_vectorと現在のベクトルとの距離に重みを付けて足し合わせる。
```python
  def UpdateVectors(self):
          for i in range(self.n_swarm):
              r1 = np.random.uniform(0,1,self.vectors[0].shape)
              r2 = np.random.uniform(0,1,self.vectors[0].shape)
              self.speeds[i] = self.w*self.speeds[i]+r1*(self.p_best_vectors[i]-self.vectors[i])+r2*(self.g_best_vector-self.vectors[i])
              self.vectors[i] = self.vectors[i] + self.speeds[i]
```
6. 2~5を繰り返し、最終的にはg_best_vectorの価値マップとそのときのスコアを出力する。(基本使うのは価値マップだけ)
```python
    n_indivisuals = 150  #ベクトル(価値マップ)の数 (=n_iter)
    n_iters = 10　       #ベクトルの更新回数

    def Run(self):
        for i in range(self.n_iter):
            self.CalcScores()
            self.UpdateVectors()
        return self.g_best_score,self.g_best_vector
```
