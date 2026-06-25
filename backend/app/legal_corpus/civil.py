"""Sample corpus: Código Civil Federal — área civil general (subset).

Demo corpus — paraphrased excerpts, replace with verified official DOF text
before production ingestion.
"""

CIVIL_CORPUS = [
    {
        "id": "ccf-art-1796",
        "law_name": "Código Civil Federal",
        "jurisdiction": "federal",
        "article_number": "1796",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CCF.pdf",
        "area": "civil",
        "text": (
            "Artículo 1796. Los contratos se perfeccionan por el mero "
            "consentimiento, salvo aquellos que deban revestir una forma "
            "establecida por la ley. Desde que se perfeccionan, obligan a "
            "los contratantes no solo al cumplimiento de lo expresamente "
            "pactado, sino también a las consecuencias que, según su "
            "naturaleza, son conformes a la buena fe, al uso o a la ley."
        ),
    },
    {
        "id": "ccf-art-2398",
        "law_name": "Código Civil Federal",
        "jurisdiction": "federal",
        "article_number": "2398",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CCF.pdf",
        "area": "civil",
        "text": (
            "Artículo 2398. El arrendamiento es un contrato por el cual "
            "una persona concede a otra el uso o goce temporal de un bien, "
            "mediante el pago de un precio cierto. El arrendador está "
            "obligado a entregar el bien en condiciones de servir para el "
            "uso convenido y a mantenerlo en ese estado durante la "
            "vigencia del contrato."
        ),
    },
    {
        "id": "ccf-art-1602",
        "law_name": "Código Civil Federal",
        "jurisdiction": "federal",
        "article_number": "1602",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CCF.pdf",
        "area": "civil",
        "text": (
            "Artículo 1602. La herencia comprende todos los bienes, "
            "derechos y obligaciones del autor de la sucesión que no se "
            "extinguen por la muerte. Los herederos legítimos suceden en "
            "el orden que marca la ley cuando no existe testamento válido; "
            "el cónyuge, los descendientes y los ascendientes tienen "
            "derecho preferente frente a otros parientes colaterales."
        ),
    },
]
