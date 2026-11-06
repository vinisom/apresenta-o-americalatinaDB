from base_dashboard import run
VIEWS = [f'vw_argentina_2025_{suffix}' for suffix in [
'atacantes', 'centroavantes', 'consolidada', 'goleiros', 'laterais',
'meias_centrais', 'meias_laterais', 'meias_ofensivos', 'pontas',
'volantes', 'zagueiros']]
run('Argentina', 'stg', VIEWS)
