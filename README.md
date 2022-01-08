Stooqifier
====
[![Pylint](https://github.com/f-teruhisa/stooqifier/actions/workflows/pylint.yml/badge.svg)](https://github.com/f-teruhisa/stooqifier/actions/workflows/pylint.yml)
[![pytest](https://github.com/f-teruhisa/stooqifier/actions/workflows/pytest.yml/badge.svg)](https://github.com/f-teruhisa/stooqifier/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/gh/f-teruhisa/stooqifier/branch/master/graph/badge.svg?token=WSFICC2GBH)](https://codecov.io/gh/f-teruhisa/stooqifier)

Stooqifier is an automatic stock price [Slack](https://slack.com/intl/en-in/) notification with chart image script that with [pandas-datareader](https://github.com/pydata/pandas-datareader) call [Stooq.com](https://stooq.com/) API.

![example](/images/example.png)

(ex. [6095.JP](https://stooq.com/q/?s=6095.JP)'s stock price configured)

## Description

![architecture](/images/architecture.png)

- Notification script written in Python 3.9 that runs on [Google Cloud Functions](https://cloud.google.com/functions)
- This script can be executed periodically by setting up with [Google Cloud Scheduler](https://cloud.google.com/scheduler).
- Can freely set the stock code and the Slack channel to be notified
- The stock price update timing depends on [Stooq.com](https://stooq.com/)
    - As of January 2021, stock prices up to the previous day can be obtained in most cases

※日本語解説記事はこちら(Japanese Description is here 👉): https://zenn.dev/t_fukumoto/articles/e5e0fe753d5726

## Install

```
$ git clone git@github.com:f-teruhisa/stooqifier.git
```

## Usage
### Deploy to Google Cloud Functions
- Deploy to Cloud Functions in project root with [gcloud](https://cloud.google.com/sdk/gcloud/reference/functions/deploy) command

```
$ gcloud functions deploy #{FUNCTION_NAME} --entry-point main --project #{PROJECT_ID} --region #{REGION} --runtime python39 --trigger-topic #{PUBUSB_TOPIC_NAME}
```

### Set some variables in `.env`

![set_env_variables](/images/set_env_variables.png)

- Change the file name of `.sample.env` to `.env`
- Create Bots with [Slack Bots](https://api.slack.com/bot-users) and generate `SLACK_API_TOKEN`
- `SLACK_CHANNEL ID` is being shown via the web browser of Slack

```
# .sample.env => .env
STOCK_CODE=
SLACK_API_TOKEN=
SLACK_CHANNEL_ID=
```

Then, the function test will pass.

### Set up scheduled execution in Cloud Scheduler
- Configure the periodic execution settings in Cloud Scheduler
- Specify `#{TOPIC_NAME}` which was created in [Deploy to Google Cloud Functions](https://github.com/f-teruhisa/stooqifier/new/master?readme=1#deploy-to-google-cloud-functions), as the topic
- Official documentation: https://cloud.google.com/scheduler/docs/quickstart#create_a_job

## Requirement
- pandas-datareader: https://github.com/pydata/pandas-datareader
  - To request API of [Stooq.com](https://stooq.com/)
- mplfinance: https://github.com/matplotlib/mplfinance
  - To generate price chart image

## Contribution
1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[f-teruhisa](https://github.com/f-teruhisa)
