"""Sample corpus: Ley Federal del Trabajo (subset for MVP slice — área laboral).

Source: Diario Oficial de la Federación (DOF). Text trimmed/paraphrased for
demo purposes — replace with full official text + real DOF citations before
production ingestion.
"""

LABORAL_CORPUS = [
    {
        "id": "lft-art-47",
        "law_name": "Ley Federal del Trabajo",
        "jurisdiction": "federal",
        "article_number": "47",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf",
        "area": "laboral",
        "text": (
            "Artículo 47. Son causas de rescisión de la relación de trabajo, "
            "sin responsabilidad para el patrón: engañar el trabajador al "
            "patrón con certificados falsos; incurrir el trabajador durante "
            "sus labores en faltas de probidad u honradez, actos de violencia, "
            "amagos, injurias o malos tratamientos contra el patrón; ocasionar "
            "perjuicios materiales de manera intencional; comprometer la "
            "seguridad del establecimiento por negligencia grave; cometer "
            "actos inmorales en el establecimiento; revelar secretos de "
            "fabricación; tener más de tres faltas de asistencia injustificadas "
            "en un periodo de treinta días; desobedecer al patrón sin causa "
            "justificada; negarse a adoptar medidas de seguridad; y "
            "concurrir al trabajo en estado de embriaguez o bajo influencia "
            "de drogas, salvo prescripción médica."
        ),
    },
    {
        "id": "lft-art-48",
        "law_name": "Ley Federal del Trabajo",
        "jurisdiction": "federal",
        "article_number": "48",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf",
        "area": "laboral",
        "text": (
            "Artículo 48. El trabajador podrá solicitar ante la autoridad "
            "laboral, a su elección, que se le reinstale en el trabajo que "
            "desempeñaba, o que se le indemnice con el importe de tres meses "
            "de salario, si el patrón despide injustificadamente al "
            "trabajador. Si en el juicio correspondiente no se prueba la "
            "causa de la rescisión, el trabajador tendrá derecho a las "
            "indemnizaciones que correspondan, además del pago de salarios "
            "vencidos desde la fecha del despido hasta que se cumplimente el "
            "laudo, hasta por un periodo máximo de doce meses."
        ),
    },
    {
        "id": "lft-art-162",
        "law_name": "Ley Federal del Trabajo",
        "jurisdiction": "federal",
        "article_number": "162",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf",
        "area": "laboral",
        "text": (
            "Artículo 162. Los trabajadores de planta tienen derecho a una "
            "prima de antigüedad, que consiste en el pago de doce días de "
            "salario por cada año de servicios. La prima se paga a los "
            "trabajadores que se separen voluntariamente de su empleo, "
            "siempre que hayan cumplido quince años de servicios; a los que "
            "se separen por causa justificada y a los que sean separados de "
            "su empleo, independientemente de la justificación o "
            "injustificación del despido."
        ),
    },
    {
        "id": "lft-art-989",
        "law_name": "Ley Federal del Trabajo",
        "jurisdiction": "federal",
        "article_number": "989",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf",
        "area": "laboral",
        "text": (
            "Artículo 989. El patrón que despida a un trabajador deberá "
            "darle aviso escrito de la fecha y causa o causas del despido. "
            "El aviso deberá hacerse del conocimiento del trabajador en el "
            "momento mismo del despido, o bien, comunicarlo a la Junta de "
            "Conciliación y Arbitraje dentro de los cinco días hábiles "
            "siguientes, en cuyo caso se le deberá proporcionar domicilio "
            "del trabajador para que sea notificado personalmente. La falta "
            "de aviso al trabajador o a la Junta, por sí sola, bastará para "
            "considerar que el despido fue injustificado."
        ),
    },
    {
        "id": "lft-art-76",
        "law_name": "Ley Federal del Trabajo",
        "jurisdiction": "federal",
        "article_number": "76",
        "effective_date": "2024-01-01",
        "source_url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf",
        "area": "laboral",
        "text": (
            "Artículo 76. Los trabajadores que tengan más de un año de "
            "servicios disfrutarán de un periodo anual de vacaciones "
            "pagadas, que en ningún caso podrá ser inferior a doce días "
            "laborables, y que aumentará en dos días laborables, hasta "
            "llegar a veinte, por cada año subsecuente de servicios. "
            "Después del cuarto año, el periodo de vacaciones aumentará en "
            "dos días por cada cinco años de servicios."
        ),
    },
]
