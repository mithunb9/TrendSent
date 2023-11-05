CREATE MODEL trendsentbias
PREDICT analysis
USING
  engine = 'openai',
  max_tokens = 300,
  temperature = 0.75,
  api_key =   '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',
  model_name = 'gpt-3.5-turbo', -- you can also use 'text-davinci-003' or 'gpt-3.5-turbo'
 prompt_template = 'You are a high level company evaluator who is experienced in evaluating how various public sentiments would effect a company evaluation. 

Table input:
 
|Time      | company.       |forecasteddcf|
|mm/dd/yyyy|(company ticker)|dcf double         |

{{companyTable}}

Bias:{{bias}}

In less than 200 characters, use the companys forecasted discounted cashflow{{dcfdouble}}, which is a is a type of financial model that determines whether an investment is worthwhile based on future cash flows, and then use the sentiment analysis ( a percentage of how people feel about the company, the higher the percetage the better the general sentiment, the lower the percentage the worse the general sentiment) to analyze how the sentiment would effect the companies forecasted discounted cashflow.Provide general company advice based on the Sentiment and predicted DCF. Also talk about reasonable competitors and how their state in the market would effect the company';

DROP MODEL trendsentbias;

-- SELECT analysis 
--     FROM trendsentbias
--   WHERE companyTable = 'EOG'
--   AND dcfdouble = (SELECT forecasteddcf FROM display_name.EOG)
--   AND bias = (SELECT sentiment FROM display_name.sentiment WHERE comp = 'EOG');

CREATE TABLE display_name.WFCanalysis 
(SELECT analysis FROM trendsentbias WHERE companyTable = 'WFC' 
AND dcfdouble = (SELECT forecasteddcf FROM display_name.WFC) 
AND bias = (SELECT sentiment FROM display_name.sentiment WHERE comp = 'WFC'));


