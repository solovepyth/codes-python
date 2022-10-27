{%- if (liste[0]=='plage') and (liste[1]=='dwh_billing') -%}
	select sk_date_si,date_d
	from dwh_billing.dbo.dwh_dim_date
	where date_d>='{{liste[2]}}' and date_d<='{{liste[3]}}'
{%- elif (liste[0]=='plage') and (liste[1]=='dwh_utiba') -%}
	select pk_dateid_si,date_d
	from dwh_utiba.dbo.dwh_dim_date
	where date_d>='{{liste[2]}}' and date_d<='{{liste[3]}}'
{%- endif -%}

