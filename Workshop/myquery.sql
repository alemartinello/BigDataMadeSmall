with experiments as (
    select t.id as infector_id, t.test_time as infector_test_time
        , tt.transaction_time as infector_transaction_time, tt.shop
        , date_sub('days', t.test_time, tt.transaction_time) as infector_days_to_test
        , row_number() over() as experiment_number
    from read_parquet('../data/tests.parquet') as t
    inner join read_parquet('../data/transactions.parquet') as tt
        on tt.id=t.id 
        and date_sub('days', t.test_time, tt.transaction_time) between -5 and -2
    where t.positive=1
    -- a small number to test it out
    limit $nlimit
) 
select e.*
, t2.id as exposed_id, t2.transaction_time as exposed_transaction_time
, date_sub('minutes', t2.transaction_time, e.infector_transaction_time) as minutes_apart
, case when date_sub('minutes', t2.transaction_time, e.infector_transaction_time) between -5 and +5 then 1 
    when date_sub('minutes', t2.transaction_time, e.infector_transaction_time) between -30 and -16 then 0
    else NULL end as treat
from experiments as e
inner join read_parquet('../data/transactions.parquet') as t2
    -- in the same shop
    on t2.shop=e.shop
    -- I do not want the infector transactions there!
    and t2.id!=e.infector_id
    --order by experiment_number, exposed_transaction_time
    and t2.transaction_time between
        e.infector_transaction_time - interval 30 minutes
        and e.infector_transaction_time + interval 30 minutes