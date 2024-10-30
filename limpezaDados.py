# Imports

# Chamando a API pela url
# Precisamos chamar as APIs separadas ou as informações se misturam
url_pregao = "https://pncp.gov.br/api/search/?tipos_documento=edital&ordenacao=-data&pagina=1&tam_pagina=15&status=recebendo_proposta&q=comprasnet&tipos=1"
url_dispensa = "https://pncp.gov.br/api/search/?tipos_documento=edital&ordenacao=-data&pagina=1&tam_pagina=15&status=recebendo_proposta&tipos=2"

# Determinando a quantidade de páginas
n_pagina = int(input("Páginas necessárias: "))

# Update the URLs with the new tam_pagina value
endpoint_url_pregao = url_pregao.replace("tam_pagina=15", f"tam_pagina={n_pagina}")
endpoint_url_dispensa = url_dispensa.replace("tam_pagina=15", f"tam_pagina={n_pagina}")
