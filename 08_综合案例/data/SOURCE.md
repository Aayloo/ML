# Default of Credit Card Clients — data source

- Repository: UCI Machine Learning Repository
- Dataset: Default of Credit Card Clients (ID 350)
- Dataset page: https://archive.ics.uci.edu/dataset/350/default
- DOI: https://doi.org/10.24432/C55S3H
- License: CC BY 4.0
- Original file: `default of credit card clients.xls`
- Local teaching copy: `default_of_credit_card_clients.csv`

The local CSV is a mechanical conversion of the official XLS workbook:

1. the second workbook row is used as the header;
2. the target column is renamed from `default payment next month` to
   `default_payment_next_month`;
3. no observation is filtered or otherwise modified.

Validation at conversion time:

- rows: 30,000;
- columns: 25 (including `ID` and the target);
- missing cells: 0;
- target counts: class 0 = 23,364; class 1 = 6,636.
