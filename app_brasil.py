from base_dashboard import run
VIEWS = [
'vw_brasileirao_2025_atacantes_analise',
'vw_brasileirao_2025_centroavantes_analise',
'vw_brasileirao_2025_laterais',
'vw_brasileirao_2025_meias_centrais',
'vw_brasileirao_2025_meias_ofensivos',
'vw_brasileirao_2025_metricas_90',
'vw_brasileirao_2025_pontas_direitas_analise',
'vw_brasileirao_2025_pontas_esquerdas_analise',
'vw_brasileirao_2025_ranking_mercado',
'vw_brasileirao_2025_volantes',
'vw_brasileirao_2025_zagueiros'
]
run('Brasil', 'analytics', VIEWS)
