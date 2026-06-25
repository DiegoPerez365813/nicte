"""Sample corpus: Código Civil Federal — área familiar (subset).

Source: Diario Oficial de la Federación (DOF). Text trimmed/paraphrased for
demo purposes — replace with full official text + real DOF citations before
production ingestion. Family law in Mexico is mostly state-level (each state
has its own Código Civil/Familiar); this federal corpus is a stand-in until
state-specific ingestion is added.
"""

FAMILIAR_CORPUS = [
    {
        "id": "ccf-art-303",
        "law_name": "Código Civil Federal",
        "jurisdiction": "federal",
        "article_number": "303",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CCF.pdf",
        "area": "familiar",
        "text": (
            "Artículo 303. Los padres están obligados a dar alimentos a "
            "sus hijos. A falta o por imposibilidad de los padres, la "
            "obligación recae en los demás ascendientes por ambas líneas "
            "que estuvieren más próximos en grado. La obligación de dar "
            "alimentos a los hijos no se extingue por la disolución del "
            "matrimonio o por la falta de reconocimiento voluntario de la "
            "paternidad; puede exigirse judicialmente."
        ),
    },
    {
        "id": "ccf-art-388",
        "law_name": "Código Civil Federal",
        "jurisdiction": "federal",
        "article_number": "388",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CCF.pdf",
        "area": "familiar",
        "text": (
            "Artículo 388. El hijo puede reclamar su filiación paterna o "
            "materna en cualquier tiempo, ya sea por reconocimiento "
            "voluntario o mediante juicio de reconocimiento de paternidad. "
            "Acreditada la filiación, el padre queda obligado a las "
            "consecuencias legales correspondientes, incluyendo la "
            "obligación alimentaria y los derechos sucesorios del hijo."
        ),
    },
    {
        "id": "ccf-art-444",
        "law_name": "Código Civil Federal",
        "jurisdiction": "federal",
        "article_number": "444",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CCF.pdf",
        "area": "familiar",
        "text": (
            "Artículo 444. La patria potestad se pierde por resolución "
            "judicial cuando medie violencia familiar hacia el menor, "
            "abandono, o cuando quien la ejerza sea condenado dos o más "
            "veces por delito grave cometido contra el menor. La pérdida "
            "de la patria potestad no extingue la obligación alimentaria."
        ),
    },
    {
        "id": "lgamvlv-art-8",
        "law_name": "Ley General de Acceso de las Mujeres a una Vida Libre de Violencia",
        "jurisdiction": "federal",
        "article_number": "8",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/LGAMVLV.pdf",
        "area": "familiar",
        "text": (
            "Artículo 8 (extracto, LGAMVLV). Las órdenes de protección son "
            "personalísimas e intransferibles, de emergencia o preventivas, "
            "y deben otorgarse de manera inmediata por la autoridad "
            "competente en cuanto conozca de hechos que lo justifiquen, "
            "garantizando la integridad de las víctimas de violencia "
            "familiar o de género."
        ),
    },
]
