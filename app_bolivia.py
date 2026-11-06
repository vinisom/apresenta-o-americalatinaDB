from base_dashboard import run
VIEWS = [f'vw_bolivia_2025_{suffix}' for suffix in [
'atacantes', 'centroavantes', 'consolidada', 'goleiros', 'laterais',
'meias_centrais', 'meias_laterais', 'meias_ofensivos',
'oportunidades_zagueiros', 'pontas', 'sem_classificacao', 'volantes', 'zagueiros']]
run('Bolívia', 'stg', VIEWS)
