{% set lstparam=liste %}
select top ({{liste[5]}}) *
from {{lstparam[0]}}.dbo.{{lstparam[1]}} with (nolock)
where {{lstparam[2]}}={%- if lstparam[3] is number -%}{{lstparam[3]}}{%- else -%}'{{lstparam[3]}}'{%- endif -%}
