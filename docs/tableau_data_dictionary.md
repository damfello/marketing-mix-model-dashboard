# Tableau data dictionary

Monetary values are totals over the full modeling period unless the column starts with `annual_`.
"Revenue" is incremental revenue (incremental conversions x revenue per conversion), not profit.
`roi_*` columns follow Meridian's naming but measure incremental ROAS (revenue / spend).
Credible intervals (`_ci_lo`, `_ci_hi`) are 90%.

| File | Grain | Use |
|---|---|---|
| dashboard_kpis.csv | 1 row | Header KPIs |
| channel_scorecard.csv | 1 row per channel | Channel metrics, recommendation, confidence |
| budget_allocation.csv | channel x allocation | Current vs recommended spend |
| budget_scenarios.csv | budget level x allocation x channel | Budget what-if scenarios |
| response_curves.csv | channel x spend multiplier | Diminishing-returns curves |
| roi_posterior_draws.csv | channel x draw | ROAS / mROAS distributions |
| weekly_model_fit.csv | week | Actual vs predicted revenue |
| weekly_channel_contribution.csv | week x channel | Contribution over time |
| model_quality.csv | check | Model diagnostics |
| sensitivity_roi.csv | spec x channel | ROAS under alternative specs |

## Key columns (channel_scorecard.csv)

- `roi_median`, `roi_ci_lo`, `roi_ci_hi`: incremental ROAS over the period.
- `mroi_median`, `return_per_100_next_unit`: return of the next unit of spend (ratio / per 100).
- `plus20_return_per_100`, `minus20_revenue_lost_per_100`: return of a +/-20% spending tranche.
- `recommended_spend_change`, `recommended_revenue_change`, `recommended_return_per_100`: the optimizer's
  move for the channel (signed; negative for cuts).
- `p_roi_gt_1`, `p_mroi_gt_1`, `p_best_mroi`: posterior probabilities.
- `spend_change_pct`, `action`: recommended change at fixed budget (bounded to +/-30%).
- `worth_new_budget`: True only if P(mROI > 1) > 0.5.
- `confidence_tier`: High / Medium / Low.

## Tableau notes

- Filter `allocation` before summing `spend` in budget_allocation.csv and budget_scenarios.csv.
- `total_*` columns repeat on every row of a scenario: aggregate with MIN or ATTR, never SUM.
