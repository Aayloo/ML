# Data policy

The default demo runs entirely offline on deterministic synthetic market data. It exists to make the research pipeline reproducible in CI and on a fresh clone.

For real research, replace the demo loader with a licensed public data source and document:

- the provider and license;
- adjustment and corporate-action treatment;
- point-in-time universe membership;
- publication timestamps for fundamentals or alternative data;
- the exact download date and schema.

The repository does not claim that demo data represents live market performance.
