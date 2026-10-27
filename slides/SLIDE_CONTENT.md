# Phase 1 presentation: speaker guide

The deck is [phase1_presentation.pptx](phase1_presentation.pptx): 10 slides, built in Canva on 2026-10-27 and exported to PowerPoint. All numbers match the [report](../report/phase1_report.pdf) and the full run in `verification/full-phase1-20261026/`.

Slides 3 to 7 each cover one module, so every member presents their own part. The slides themselves carry no names. The module owners below come from the team's handoff split (see `docs/handoffs/`); change the speaker order if the team prefers.

| Slide | Title | Module (presenter) | Chart |
| --- | --- | --- | --- |
| 1 | Predicting Traffic Speed on a Road Network | Title, team | - |
| 2 | The Problem | Anyone | - |
| 3 | The Data and How We Checked It | Dataset loading and checks (Rudraksh) | Congestion map |
| 4 | Cleaning the Data and Building Features | Masking, splits, features (Vridhi) | - |
| 5 | What the Data Shows | EDA (Anshuman) | Weekday/weekend speed by hour |
| 6 | Simple Baselines and Random Forest | Baselines and Random Forest (Bineet) | - |
| 7 | XGBoost and How We Measure Error | XGBoost and evaluation (Kavya) | - |
| 8 | Results | Anyone | Results table |
| 9 | Where the Models Still Fail | Error analysis (Bineet or Anshuman) | XGBoost error map |
| 10 | Next Steps and Thank You | Anyone | - |

## Speaker notes

**1. Title.** Introduce the team. Phase 1 is the machine-learning part of Project 4.

**2. The problem.** Jams start on one road and spread. We predict the speed at every sensor 15, 30 and 60 minutes ahead. In Phase 1 each sensor gets its own model; Phase 2 adds a graph model that can look at neighbouring roads. Signal control is only ever simulated.

**3. The data and how we checked it.** METR-LA has 207 sensors on Los Angeles highways, one reading every 5 minutes from March to June 2012. Our loader checks the size, the 5-minute steps and that the sensor order matches the road map. We rebuilt the road map from road distances and it matches the published one. The map shows each sensor coloured by its average speed: red means slow (downtown). The data has speed only, no vehicle counts or occupancy. *Possible viva questions: why read the file with PyTables? Why is 0 mph treated as missing? How is the road map built (Gaussian kernel of road distance)?*

**4. Cleaning the data and building features.** 8.1% of readings are missing. A reading of 0 mph means the sensor sent nothing, so it is ignored, never used as a real speed or as an answer. We split by time: train on the first 70%, tune on the next 10%, test on the last 20%; never randomly, otherwise the model would see the future. We also leave a small gap at each boundary so training answers never overlap the next block. Each example has 38 features: the last 12 speeds, short averages, missing flags, and time of day and week as sin/cos so 11:55 pm sits next to midnight. *Possible viva questions: what is the purge gap? Why no scaling for tree models? Why sin and cos?*

**5. What the data shows.** On weekdays speeds drop around 8 to 9 am and around 5:30 pm; weekends have no morning rush. Some days the whole network is offline and some sensors are off for days. Downtown roads are slowest. This is why we added time features and report rush hour separately. *Possible viva question: why is EDA done on training data only?*

**6. Simple baselines and Random Forest.** Persistence says the speed stays the same; historical average uses the usual speed for that time of the week. Random Forest builds many decision trees on random samples and averages them. One forest per sensor predicts all 12 future steps at once. It makes the fewest very big mistakes (lowest RMSE). *Possible viva questions: what is bagging? Why does averaging reduce variance? Why does the forest drop rows with a missing future value?*

**7. XGBoost and how we measure error.** XGBoost adds trees one after another, each fixing the last one's mistakes. We train one model per sensor and per future step. Settings were chosen on the tuning block only. MAE is the average error in mph, RMSE punishes big misses more, MAPE is the error as a percentage. These are errors, not accuracy. *Possible viva questions: boosting vs bagging? Why did the absolute-error objective win (lower MAE)?*

**8. Results.** Both learned models beat both baselines at every horizon. XGBoost has the lowest average error: 2.92 / 3.38 / 3.87 mph at 15 / 30 / 60 minutes, 16% to 27% better than persistence. Random Forest has the lowest RMSE.

**9. Where the models still fail.** Rush-hour errors are about twice the normal errors, and at 60 minutes in rush hour Random Forest beats XGBoost (5.95 vs 6.31 mph). The map shows the biggest errors sit together on the same roads. A sensor's own past cannot warn it about a jam that starts on a nearby road, which is the gap Phase 2 will address.

**10. Next steps.** Phase 2: a Graph Attention Network on the same road map, with the same splits and 1-hour history, checking whether it helps most at rush hour and on the worst roads. Optionally, test a signal-timing idea in a simulator (SUMO or CityFlow), never on real roads.
