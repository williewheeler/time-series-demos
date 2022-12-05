# time-series-demos

Jupyter notebooks containing various time series analysis demos. Some of the demos are in Python and some are in R.
I probably should have separated them out or just picked a language but I didn't. :)

Some of the demos have corresponding blog posts:

- adf-demo: https://medium.com/wwblog/stationarity-testing-using-the-augmented-dickey-fuller-test-8cf7f34f4844
- hampel: https://medium.com/wwblog/clean-up-your-time-series-data-with-a-hampel-filter-58b0bb3ebb04
- imputation-experiments: https://medium.com/wwblog/clean-up-your-time-series-data-with-a-hampel-filter-58b0bb3ebb04
- removing-outliers-from-time-series: https://medium.com/wwblog/clean-up-your-time-series-data-with-a-hampel-filter-58b0bb3ebb04

# Setup

Install `pipenv` using

```
$ brew install pipenv
```

# Running

Enter the `pipenv` shell:

```
$ pipenv shell
```

Install the dependencies and sources

```
$ pipenv install
$ pipenv install -e .
```

Then start JuypterLab:

```
$ jupyter lab
```
