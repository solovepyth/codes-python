with a as (
    select  callingpartynumber as msisdn,cast(sum(mainaccountvaluebeforecall - mainaccountvalueaftercall) as bigint) as ca
    from dwh_billing.dbo.dwh_fact_outgoing with (nolock)
    where fk_date_si>={{liste[0]}} and fk_date_si<={{liste[1]}}
    and fk_dedicatednumber_si > 0 and (mainaccountvaluebeforecall - mainaccountvalueaftercall) > 0 and fk_datatype_si = 1
    and right(callingpartynumber,9)='{{liste[4]}}'
    group by callingpartynumber)
,b as (
    select  callingpartynumber as msisdn,cast(sum(chargeableamount_i)*1.2 as bigint) as ca 
    from [dwh_billing].[dbo].[dwh_fact_outgoing] d   with (nolock)         
    where fk_date_si>={{liste[0]}} and fk_date_si<={{liste[1]}}
    and d.fk_dedicatednumber_si = 0 and fk_datatype_si = 1 and chargeableduration_i > 0
    and right(callingpartynumber,9)='{{liste[4]}}' 
    group by callingpartynumber)
,c as (
    select  subscribernumber as msisdn,cast(sum(Cost) as bigint) as ca 
    from [dwh_billing].[dbo].[dwh_fact_achat_bundle] a  with (nolock)
    inner join [dwh_billing].[dbo].[dwh_dim_dedicatednumber] d with (nolock) on a.dedicatedaccountid_1 = d.sk_dedicatednumber_si         
    where [day]>='{{liste[2]}}' and [day]<='{{liste[3]}}'
    and (unitType_v = 'Money' or offerName_v like '%Time%' or OfferDataType_v = 'Voice')
    and right(subscribernumber,9)='{{liste[4]}}'
    group by subscribernumber)

select msisdn,cast(sum(ca) as bigint) ca{{ liste[0]|replace("-","_") }}
    from (
    select msisdn,ca from a
    union all 
    select msisdn,ca from b
    union all 
    select msisdn,ca from c) sq
    group by msisdn