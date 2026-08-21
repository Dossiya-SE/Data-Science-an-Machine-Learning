# Data Science and Machine Learning — Learning Repository

<p align="center"><img src="assets/ml-evidence-pipeline.svg" width="100%" alt="Machine learning evidence pipeline" /></p>

**Current status: learning scaffold.** The visual is a **quality contract for future projects**, not evidence that a model has already been trained or validated here.

## Mathematical standard for future work

```math
\theta^*=\arg\min_\theta\sum_i \ell(f_\theta(x_i),y_i)+\lambda\Omega(\theta),
\qquad
\widehat R_{test}=n_{test}^{-1}\sum_i\ell(f_\theta(x_i),y_i).
```

A mature project must expose:

`data provenance → honest split → leakage-safe preprocessing → baseline → model → out-of-sample metric → uncertainty → sensitivity → bounded interpretation`

## Promotion gate

This repository becomes evidence-bearing only when at least one project contains executable source, environment/dependencies, data/source documentation, controlled experiments, reproducible outputs, evaluation metrics, uncertainty/sensitivity analysis and explicit limitations.

## Scientific rules

- accuracy alone is not evaluation;
- test data are not tuning data;
- predictive importance is not causal effect;
- preprocessing can leak information;
- a notebook alone is not a reproducible pipeline;
- a high metric does not establish external validity.

Current evidence-bearing work is in the [Mathematical Research Portfolio](https://github.com/Dossiya-SE/dossiya-se.github.io), [Africa Energy Dignity](https://github.com/Dossiya-SE/africa-energy-dignity), [Financial Engineering Models](https://github.com/Dossiya-SE/dossiyadakou-mac-project) and [Python for Rapid Engineering Solutions](https://github.com/Dossiya-SE/Python-for-rapid-engineering-solution).
