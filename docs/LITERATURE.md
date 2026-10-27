# Literature synthesis and source register

Reviewed source scope: bibliographic records, accessible abstracts and relevant method descriptions; this is not a claim that all papers were independently replicated or fully reviewed by any student. No literature score is treated as a result from our code. Sources checked 2026-10-26; brief pre-reads and flow/simulation sources added 2026-10-27.

| Source | Method / relevance | Limits for our study | Evidence inspected |
| --- | --- | --- | --- |
| Breiman (2001), Random Forests | Randomized tree ensembles motivate our independent-sensor forest; averaging provides a simple regression reference. | General algorithm paper, not a METR-LA benchmark; its standard OOB discussion does not replace chronological validation here. | [Author manuscript](https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf), abstract and method introduction |
| Chen and Guestrin (2016), XGBoost: A Scalable Tree Boosting System | Boosted trees and efficient sparse-data handling motivate tabular forecasting from causal features. | Algorithmic scalability does not guarantee our model's accuracy; our parameter budget and data differ. | [Author arXiv record](https://arxiv.org/abs/1603.02754), abstract/bibliographic metadata; official API documentation |
| Williams and Hoel (2003), Modeling and Forecasting Vehicular Traffic Flow as a Seasonal ARIMA Process | Seasonal univariate traffic modeling supports including temporal structure and simple historical references. | Different traffic streams and model family; ARIMA is not implemented or numerically compared here. | [Paper copy](https://www3.nd.edu/~busiforc/handouts/ARIMA%20Engineering%20Article.pdf), abstract/front page |
| Castro-Neto et al. (2009), Online-SVR for short-term traffic flow prediction under typical and atypical traffic conditions | Distinguishing typical/atypical conditions motivates period-specific error analysis. | Predicts traffic flow in a different setting; not evidence of the speed-only benchmark performance of our trees. | [Author institution record](https://www.researchwithrutgers.org/en/publications/online-svr-for-short-term-traffic-flow-prediction-under-typical-a/), abstract/metadata |
| Hyndman and Koehler (2006), Another look at measures of forecast accuracy | Metric degeneracy motivates explicit masks and considering multiple error measures. | Does not make MAPE universally valid; MASE is discussed by the paper but not an implemented project metric. | [Author publication page](https://otext.robjhyndman.com/publications/another-look-at-measures-of-forecast-accuracy/) |
| Li et al. (2018), Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic Forecasting | Directed-network temporal forecasting supplies benchmark provenance and future spatial-model motivation. | Deep learning is deferred. Different splits/masks mean published scores are not an apples-to-apples leaderboard against our purged prototype. | [Author arXiv record](https://arxiv.org/abs/1707.01926) and [code/data instructions](https://github.com/liyaguang/DCRNN) |
| Veličković et al. (2018), Graph Attention Networks | Pre-read named in the project brief. Attention over graph neighbours is the planned Phase 2 model for using upstream/downstream sensors. | Evaluated on citation/protein graphs, not traffic; no Phase 1 result depends on it. | [arXiv:1710.10903](https://arxiv.org/abs/1710.10903), abstract and method |
| Zhang et al. (2019), CityFlow: A Multi-Agent Reinforcement Learning Environment for Large Scale City Traffic Scenario | Pre-read named in the project brief (listed there as "Zheng et al."; the paper's first author is Huichu Zhang). Simulator for the optional, simulated-only signal-control experiment. | A simulator, not a forecasting method; not used in Phase 1. | [arXiv:1905.05217](https://arxiv.org/abs/1905.05217), WWW 2019, DOI 10.1145/3308558.3314139 |
| Lighthill and Whitham (1955); Richards (1956), LWR kinematic-wave traffic model | Explains why congestion travels along roads, motivating neighbour information. | Needs flow/density, which METR-LA does not measure; no LWR calibration is done. | Bibliographic records and abstracts |
| Lopez et al. (2018), Microscopic Traffic Simulation using SUMO | Simulator named in the project brief for optional simulation. | Not used in Phase 1. | ITSC 2018, DOI 10.1109/ITSC.2018.8569938 |

## Synthesis

Classical traffic forecasting establishes a role for temporal regularity; tree ensembles offer nonlinear feature-based models without neural architectures. Evaluating only overall error can obscure atypical/peak conditions. Metric definitions and time partitioning matter as much as the estimator. Our experiment therefore compares temporal, independent-sensor trees with persistence and historical averages on a common masked grid. It leaves spatial graph forecasting as a future hypothesis, not a confirmed improvement.

## Verified identifiers

- Breiman: Machine Learning 45, 5-32 (2001), DOI 10.1023/A:1010933404324.
- Chen and Guestrin: KDD 2016, DOI 10.1145/2939672.2939785.
- Williams and Hoel: Journal of Transportation Engineering 129(6), 664-672 (2003), DOI 10.1061/(ASCE)0733-947X(2003)129:6(664).
- Castro-Neto, Jeong, Jeong and Han: Expert Systems with Applications 36(3), 6164-6173 (2009), DOI 10.1016/j.eswa.2008.07.069.
- Hyndman and Koehler: International Journal of Forecasting 22(4), 679-688 (2006), DOI 10.1016/j.ijforecast.2006.03.001.
- Li, Yu, Shahabi and Liu: ICLR 2018, arXiv:1707.01926.
- Veličković, Cucurull, Casanova, Romero, Liò and Bengio: ICLR 2018, arXiv:1710.10903.
- Zhang, Feng, Liu, Ding, Zhu, Zhou, Zhang, Yu, Jin and Li: WWW 2019, DOI 10.1145/3308558.3314139.
- Lighthill and Whitham: Proc. R. Soc. Lond. A 229(1178), 317-345 (1955). Richards: Operations Research 4(1), 42-51 (1956).
- Lopez et al.: IEEE ITSC 2018, 2575-2582, DOI 10.1109/ITSC.2018.8569938.

## Implementation references

[Random Forest regressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html), [multi-output example](https://scikit-learn.org/stable/auto_examples/ensemble/plot_random_forest_regression_multioutput.html), [XGBoost objectives](https://xgboost.readthedocs.io/en/stable/parameter.html). Runtime package versions, rather than the current website version, are pinned in requirements.txt.
