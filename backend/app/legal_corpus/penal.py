"""Sample corpus: Código Penal Federal (subset — área penal).

Source: Diario Oficial de la Federación (DOF). Text trimmed/paraphrased for
demo purposes — replace with full official text + real DOF citations before
production ingestion. Article numbering follows the Código Penal Federal;
several states have their own penal codes with different numbering — a
production system must select the corpus by jurisdiction.
"""

PENAL_CORPUS = [
    {
        "id": "cpf-art-261",
        "law_name": "Código Penal Federal",
        "jurisdiction": "federal",
        "article_number": "261",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPF.pdf",
        "area": "penal",
        "text": (
            "Artículo 261. Comete el delito de abuso sexual quien, sin "
            "consentimiento de una persona y sin el propósito de llegar a "
            "la cópula, ejecute en ella un acto sexual, la obligue a "
            "observarlo o ejecutarlo, o la haga ejecutarlo. Si la persona "
            "ofendida es menor de quince años o no tiene capacidad para "
            "comprender el significado del hecho, se aplicará una pena "
            "agravada, sin que sea necesario acreditar violencia física."
        ),
    },
    {
        "id": "cpf-art-262",
        "law_name": "Código Penal Federal",
        "jurisdiction": "federal",
        "article_number": "262",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPF.pdf",
        "area": "penal",
        "text": (
            "Artículo 262 (estupro). Al que tenga cópula con persona mayor "
            "de quince y menor de dieciocho años, obteniendo su "
            "consentimiento por medio de engaño, se le aplicará pena "
            "privativa de la libertad. El consentimiento de un menor de "
            "edad no exime de responsabilidad cuando medie engaño o abuso "
            "de la confianza; cada entidad federativa puede establecer "
            "edades y supuestos distintos en su código penal local, por lo "
            "que es indispensable revisar la legislación del estado "
            "correspondiente."
        ),
    },
    {
        "id": "cpf-art-265",
        "law_name": "Código Penal Federal",
        "jurisdiction": "federal",
        "article_number": "265",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPF.pdf",
        "area": "penal",
        "text": (
            "Artículo 265 (violación). Comete el delito de violación quien "
            "por medio de la violencia física o moral realice cópula con "
            "persona de cualquier sexo. Se equipara a este delito la "
            "introducción de cualquier elemento o instrumento distinto al "
            "miembro viril, por vía vaginal o anal, con fines sexuales. Las "
            "penas se agravan cuando la víctima sea menor de edad."
        ),
    },
    {
        "id": "cpf-art-21const",
        "law_name": "Constitución Política de los Estados Unidos Mexicanos",
        "jurisdiction": "federal",
        "article_number": "21",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf",
        "area": "penal",
        "text": (
            "Artículo 21 (extracto). La investigación de los delitos "
            "corresponde al Ministerio Público y a las policías, las "
            "cuales actuarán bajo la conducción y mando de aquél. Toda "
            "persona puede presentar una denuncia ante el Ministerio "
            "Público cuando tenga conocimiento de la comisión de un delito, "
            "incluyendo delitos sexuales cometidos contra menores de edad."
        ),
    },
]
