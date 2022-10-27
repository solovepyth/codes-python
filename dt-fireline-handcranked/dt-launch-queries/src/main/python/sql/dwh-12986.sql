select 
    subscribernumber,
    count(*) as nb
from 
    [dwh_billing].[dbo].[dwh_fact_achat_bundle_dfg] a  with (nolock)
inner join 
    [dwh_billing].[dbo].[dwh_dim_dedicatednumber] d with (nolock) on a.dedicatedaccountid_1 = d.sk_dedicatednumber_si         
where 
    [day]>='{{liste[0]}}' and [day]<='{{liste[1]}}'
and
({% for d in liste[2] %} dedicatedaccountid_1={{d}} {% if not loop.last %} or {% endif %}{% endfor%})
group by
    subscribernumber

