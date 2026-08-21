# Data Science and Machine Learning — Learning Repository

This repository is currently a **public learning scaffold**.

At the time of this README revision, the public `main` branch contains only this README and does **not** contain committed datasets, notebooks, model code, metrics, trained artifacts or reproducible experiments.

That limitation is stated explicitly because a repository title is not evidence of completed machine-learning work.

## Current evidence status

| Item | Status |
|---|---|
| Public README | present |
| Data provenance | not yet committed |
| Executable analysis code | not yet committed |
| Train/validation/test protocol | not yet committed |
| Model metrics | not yet committed |
| Reproducible environment | not yet committed |
| Automated tests / CI | not yet committed |
| Model card / limitations | not yet committed |

Therefore this repository should be read as **learning / work-in-progress**, not as evidence of a completed ML research pipeline.

## Rigor standard for future additions

A project added here should ideally contain the full chain:

```text
problem definition
→ data provenance
→ target / feature definitions
→ train-validation-test split
→ preprocessing fitted without leakage
→ baseline
→ model
→ metrics + uncertainty
→ diagnostics
→ robustness / sensitivity
→ interpretation
→ limitations
→ reproducible code
```

## Minimum project template

```text
project-name/
├── README.md
├── data/
│   └── SOURCE.md              # provenance, license, access date, definitions
├── notebooks/                 # exploration only
├── src/                       # reusable implementation
├── tests/                     # unit / regression tests
├── outputs/                   # machine-readable metrics / figures
├── requirements.txt / pyproject.toml
└── MODEL_CARD.md              # intended use, metrics, limitations
```

## Evaluation requirements

For supervised-learning work, the README should report at minimum:

- target definition;
- sample size and data source;
- split strategy;
- baseline model;
- preprocessing rules;
- primary and secondary metrics;
- class balance where relevant;
- confidence intervals or resampling uncertainty where appropriate;
- leakage controls;
- error analysis;
- sensitivity to important modeling choices;
- limitations and out-of-distribution risks.

For unsupervised work, the repository should avoid presenting clusters as natural or causal categories without stability and domain validation.

## Scientific-integrity rules

1. **Accuracy alone is not a model evaluation.** Use metrics appropriate to the task and decision cost.
2. **Test data are not tuning data.** Preserve an honest final evaluation set when possible.
3. **Preprocessing can leak information.** Fit transformations on training data only unless the method justifies otherwise.
4. **Association is not causation.** Predictive importance does not imply intervention effect.
5. **A notebook is not a reproducible pipeline.** Reusable code, environment information and tests should accompany mature work.
6. **A high metric is not external validity.** Document population, time, geography and distribution limits.

## Planned role in the portfolio

This repository will be promoted from a learning scaffold to an evidence-bearing portfolio component only after at least one project includes:

- committed source/data provenance;
- executable code;
- deterministic or controlled experiments;
- evaluation outputs;
- documented assumptions and limitations;
- reproducible execution instructions.

Until then, the main GitHub profile labels this repository as a **learning archive / scaffold** rather than using it as evidence of completed machine-learning research.

## Related evidence-bearing work

For current public computational evidence, see:

- [Mathematical Research Portfolio](https://github.com/Dossiya-SE/dossiya-se.github.io)
- [Africa Energy Dignity](https://github.com/Dossiya-SE/africa-energy-dignity)
- [Financial Engineering Models](https://github.com/Dossiya-SE/dossiyadakou-mac-project)
- [Python for Rapid Engineering Solutions](https://github.com/Dossiya-SE/Python-for-rapid-engineering-solution)

---

**Repository rule:** future claims will be proportional to committed evidence, not to the repository name.
