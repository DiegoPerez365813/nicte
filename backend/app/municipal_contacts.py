"""Contactos municipales por ciudad.

Para cada municipio relevante se proporciona:
  - urgencias: número local de emergencias (además del 911 nacional)
  - contraloria: Contraloría / Asuntos Internos para quejas contra policía municipal
  - dif: DIF municipal (protección de menores, violencia familiar, alimentos)
  - juzgado_civico: Juzgado Cívico (infracciones, faltas administrativas)
  - proteccion_civil: Protección Civil Municipal
  - atencion_ciudadana: línea o portal de atención ciudadana / denuncia
  - reglamento_nota: nota sobre el reglamento municipal aplicable

La información de contacto es orientativa — se recomienda verificar en el
sitio oficial del municipio ya que números y áreas cambian con cada administración.
El 911 aplica en todo el territorio nacional.
"""

MUNICIPAL_CONTACTS: dict[str, dict[str, str]] = {

    # ── CIUDAD DE MÉXICO (Alcaldías) ──────────────────────────────────────
    "Benito Juárez": {
        "estado": "Ciudad de México",
        "urgencias": "911 / 55 5658-1111 (Alcaldía Benito Juárez)",
        "contraloria": "Contraloría Interna de la Alcaldía Benito Juárez — 55 5658-1111 ext. contraloría",
        "dif": "DIF Alcaldía Benito Juárez — 55 5658-1111",
        "juzgado_civico": "Juzgado Cívico de la Alcaldía Benito Juárez",
        "proteccion_civil": "Protección Civil CDMX — 55 5683-2222",
        "atencion_ciudadana": "QUEJATEL CDMX: 55 5658-1111 / app 'CDMX' / alcaldiabenitojuarez.gob.mx",
        "reglamento_nota": "Aplica el Reglamento de Policía y Buen Gobierno de la CDMX y los Lineamientos de la Alcaldía.",
    },
    "Cuauhtémoc": {
        "estado": "Ciudad de México",
        "urgencias": "911 / SSPCDMX: 55 5242-5100",
        "contraloria": "Contraloría Interna Alcaldía Cuauhtémoc — alcaldiacuauhtemoc.gob.mx",
        "dif": "DIF Alcaldía Cuauhtémoc — 55 5130-1300",
        "juzgado_civico": "Juzgado Cívico de la Alcaldía Cuauhtémoc",
        "proteccion_civil": "Protección Civil CDMX — 55 5683-2222",
        "atencion_ciudadana": "Portal alcaldiacuauhtemoc.gob.mx / QUEJATEL: 800 890-5400",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de la CDMX.",
    },
    "Miguel Hidalgo": {
        "estado": "Ciudad de México",
        "urgencias": "911 / SSP CDMX: 55 5242-5100",
        "contraloria": "Contraloría Interna Alcaldía Miguel Hidalgo — miguelhidalgo.gob.mx",
        "dif": "DIF Alcaldía Miguel Hidalgo — 55 5093-2800",
        "juzgado_civico": "Juzgado Cívico Alcaldía Miguel Hidalgo",
        "proteccion_civil": "Protección Civil CDMX — 55 5683-2222",
        "atencion_ciudadana": "miguelhidalgo.gob.mx / QUEJATEL CDMX: 800 890-5400",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de la CDMX.",
    },
    "Iztapalapa": {
        "estado": "Ciudad de México",
        "urgencias": "911 / Alcaldía Iztapalapa: 55 5686-3700",
        "contraloria": "Contraloría Interna Alcaldía Iztapalapa — iztapalapa.gob.mx",
        "dif": "DIF Iztapalapa — 55 5686-3700",
        "juzgado_civico": "Juzgado Cívico Iztapalapa",
        "proteccion_civil": "Protección Civil CDMX — 55 5683-2222",
        "atencion_ciudadana": "iztapalapa.gob.mx / App CDMX / QUEJATEL: 800 890-5400",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de la CDMX.",
    },
    "Tlalpan": {
        "estado": "Ciudad de México",
        "urgencias": "911 / Alcaldía Tlalpan: 55 5573-4422",
        "contraloria": "Contraloría Interna Alcaldía Tlalpan — tlalpan.gob.mx",
        "dif": "DIF Tlalpan — 55 5573-4422",
        "juzgado_civico": "Juzgado Cívico Tlalpan",
        "proteccion_civil": "Protección Civil CDMX — 55 5683-2222",
        "atencion_ciudadana": "tlalpan.gob.mx / QUEJATEL: 800 890-5400",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de la CDMX.",
    },
    "Coyoacán": {
        "estado": "Ciudad de México",
        "urgencias": "911 / Alcaldía Coyoacán: 55 5659-0408",
        "contraloria": "Contraloría Interna Alcaldía Coyoacán — coyoacan.gob.mx",
        "dif": "DIF Coyoacán — 55 5659-0408",
        "juzgado_civico": "Juzgado Cívico Coyoacán",
        "proteccion_civil": "Protección Civil CDMX — 55 5683-2222",
        "atencion_ciudadana": "coyoacan.gob.mx / QUEJATEL: 800 890-5400",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de la CDMX.",
    },

    # ── JALISCO ───────────────────────────────────────────────────────────
    "Guadalajara": {
        "estado": "Jalisco",
        "urgencias": "911 / Policía Guadalajara: 33 3668-0800",
        "contraloria": "Contraloría Municipal de Guadalajara — 33 3837-8000 / guadalajara.gob.mx",
        "dif": "DIF Guadalajara — 33 3030-0099",
        "juzgado_civico": "Juzgado Municipal de Guadalajara — 33 3837-8000",
        "proteccion_civil": "Protección Civil Guadalajara — 33 3619-5241",
        "atencion_ciudadana": "guadalajara.gob.mx / App 'GDL Denuncia' / Línea de denuncia: 33 3837-8000",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Guadalajara. Las infracciones menores se resuelven ante el Juez Municipal.",
    },
    "Zapopan": {
        "estado": "Jalisco",
        "urgencias": "911 / Seguridad Zapopan: 33 3818-2200",
        "contraloria": "Contraloría Municipal Zapopan — 33 3818-2200 ext. contraloría / zapopan.gob.mx",
        "dif": "DIF Zapopan — 33 3110-0600",
        "juzgado_civico": "Juzgado Municipal Zapopan",
        "proteccion_civil": "Protección Civil Zapopan — 33 3818-2200",
        "atencion_ciudadana": "zapopan.gob.mx / Línea ciudadana: 33 3818-2200",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de Zapopan.",
    },
    "Tlaquepaque": {
        "estado": "Jalisco",
        "urgencias": "911 / Seguridad Tlaquepaque: 33 3837-0700",
        "contraloria": "Contraloría Municipal Tlaquepaque — tlaquepaque.gob.mx",
        "dif": "DIF Tlaquepaque — 33 3837-0700",
        "juzgado_civico": "Juzgado Municipal Tlaquepaque",
        "proteccion_civil": "Protección Civil Tlaquepaque — 33 3837-0700",
        "atencion_ciudadana": "tlaquepaque.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de Tlaquepaque.",
    },
    "Tonalá": {
        "estado": "Jalisco",
        "urgencias": "911 / Seguridad Tonalá: 33 3683-0200",
        "contraloria": "Contraloría Municipal Tonalá — tonala.gob.mx",
        "dif": "DIF Tonalá — 33 3683-0200",
        "juzgado_civico": "Juzgado Municipal Tonalá",
        "proteccion_civil": "Protección Civil Tonalá — 33 3683-0200",
        "atencion_ciudadana": "tonala.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de Tonalá.",
    },

    # ── NUEVO LEÓN ────────────────────────────────────────────────────────
    "Monterrey": {
        "estado": "Nuevo León",
        "urgencias": "911 / Seguridad Monterrey: 81 2020-2020",
        "contraloria": "Contraloría Municipal Monterrey — 81 2020-2020 / monterrey.gob.mx",
        "dif": "DIF Monterrey — 81 2020-3000",
        "juzgado_civico": "Juzgado Municipal Monterrey — Palacio Municipal",
        "proteccion_civil": "Protección Civil Monterrey — 81 2020-2020",
        "atencion_ciudadana": "monterrey.gob.mx / App 'Monterrey Ciudad' / Denuncia: 81 2020-2020",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Monterrey.",
    },
    "San Nicolás de los Garza": {
        "estado": "Nuevo León",
        "urgencias": "911 / Seguridad San Nicolás: 81 8040-4040",
        "contraloria": "Contraloría Municipal San Nicolás — snnl.gob.mx",
        "dif": "DIF San Nicolás — 81 8040-4040",
        "juzgado_civico": "Juzgado Municipal San Nicolás de los Garza",
        "proteccion_civil": "Protección Civil San Nicolás — 81 8040-4040",
        "atencion_ciudadana": "snnl.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de San Nicolás de los Garza.",
    },
    "Guadalupe": {
        "estado": "Nuevo León",
        "urgencias": "911 / Seguridad Guadalupe NL: 81 8153-4800",
        "contraloria": "Contraloría Municipal Guadalupe NL — guadalupe.gob.mx",
        "dif": "DIF Guadalupe NL — 81 8153-4800",
        "juzgado_civico": "Juzgado Municipal Guadalupe NL",
        "proteccion_civil": "Protección Civil Guadalupe NL — 81 8153-4800",
        "atencion_ciudadana": "guadalupe.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Guadalupe.",
    },
    "San Pedro Garza García": {
        "estado": "Nuevo León",
        "urgencias": "911 / Seguridad San Pedro: 81 8114-1100",
        "contraloria": "Contraloría Municipal San Pedro Garza García — sanpedro.gob.mx",
        "dif": "DIF San Pedro — 81 8114-1100",
        "juzgado_civico": "Juzgado Municipal San Pedro Garza García",
        "proteccion_civil": "Protección Civil San Pedro — 81 8114-1100",
        "atencion_ciudadana": "sanpedro.gob.mx / Denuncia anónima: 81 8114-1111",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de San Pedro Garza García.",
    },

    # ── ESTADO DE MÉXICO ──────────────────────────────────────────────────
    "Ecatepec": {
        "estado": "Estado de México",
        "urgencias": "911 / Seguridad Ecatepec: 55 2169-4000",
        "contraloria": "Contraloría Municipal Ecatepec — ecatepec.gob.mx",
        "dif": "DIF Ecatepec — 55 2169-4000",
        "juzgado_civico": "Juzgado Municipal Ecatepec de Morelos",
        "proteccion_civil": "Protección Civil Ecatepec — 55 2169-4000",
        "atencion_ciudadana": "ecatepec.gob.mx / denuncia ciudadana: 55 2169-4000",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Ecatepec de Morelos.",
    },
    "Naucalpan": {
        "estado": "Estado de México",
        "urgencias": "911 / Seguridad Naucalpan: 55 5358-7000",
        "contraloria": "Contraloría Municipal Naucalpan — naucalpan.gob.mx",
        "dif": "DIF Naucalpan — 55 5358-7000",
        "juzgado_civico": "Juzgado Municipal Naucalpan de Juárez",
        "proteccion_civil": "Protección Civil Naucalpan — 55 5358-7000",
        "atencion_ciudadana": "naucalpan.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de Naucalpan.",
    },
    "Toluca": {
        "estado": "Estado de México",
        "urgencias": "911 / Seguridad Toluca: 722 213-1200",
        "contraloria": "Contraloría Municipal Toluca — toluca.gob.mx",
        "dif": "DIF Toluca — 722 213-1200",
        "juzgado_civico": "Juzgado Municipal Toluca",
        "proteccion_civil": "Protección Civil Toluca — 722 213-1200",
        "atencion_ciudadana": "toluca.gob.mx / denuncia: 722 213-1200",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Toluca.",
    },
    "Nezahualcóyotl": {
        "estado": "Estado de México",
        "urgencias": "911 / Seguridad Neza: 55 5793-0055",
        "contraloria": "Contraloría Municipal Nezahualcóyotl — nezahualcoyotl.gob.mx",
        "dif": "DIF Nezahualcóyotl — 55 5793-0055",
        "juzgado_civico": "Juzgado Municipal Nezahualcóyotl",
        "proteccion_civil": "Protección Civil Neza — 55 5793-0055",
        "atencion_ciudadana": "nezahualcoyotl.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de Nezahualcóyotl.",
    },

    # ── BAJA CALIFORNIA ───────────────────────────────────────────────────
    "Tijuana": {
        "estado": "Baja California",
        "urgencias": "911 / Policía Tijuana: 664 973-7000",
        "contraloria": "Contraloría Municipal Tijuana — 664 973-7000 / tijuana.gob.mx",
        "dif": "DIF Tijuana — 664 684-2400",
        "juzgado_civico": "Juzgado Municipal Tijuana",
        "proteccion_civil": "Protección Civil Tijuana — 664 681-1100",
        "atencion_ciudadana": "tijuana.gob.mx / denuncia anónima: 089",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Tijuana.",
    },
    "Mexicali": {
        "estado": "Baja California",
        "urgencias": "911 / Policía Mexicali: 686 558-1000",
        "contraloria": "Contraloría Municipal Mexicali — mexicali.gob.mx",
        "dif": "DIF Mexicali — 686 558-1000",
        "juzgado_civico": "Juzgado Municipal Mexicali",
        "proteccion_civil": "Protección Civil Mexicali — 686 558-1000",
        "atencion_ciudadana": "mexicali.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Mexicali.",
    },
    "Ensenada": {
        "estado": "Baja California",
        "urgencias": "911 / Policía Ensenada: 646 176-4700",
        "contraloria": "Contraloría Municipal Ensenada — ensenada.gob.mx",
        "dif": "DIF Ensenada — 646 176-4700",
        "juzgado_civico": "Juzgado Municipal Ensenada",
        "proteccion_civil": "Protección Civil Ensenada — 646 176-4700",
        "atencion_ciudadana": "ensenada.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Ensenada.",
    },

    # ── PUEBLA ────────────────────────────────────────────────────────────
    "Puebla": {
        "estado": "Puebla",
        "urgencias": "911 / Policía Puebla: 222 303-6000",
        "contraloria": "Contraloría Municipal Puebla — 222 303-6000 / pueblacapital.gob.mx",
        "dif": "DIF Puebla — 222 303-6000",
        "juzgado_civico": "Juzgado Municipal de Puebla",
        "proteccion_civil": "Protección Civil Puebla — 222 303-6000",
        "atencion_ciudadana": "pueblacapital.gob.mx / Línea ciudadana: 222 303-6000",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Puebla.",
    },
    "San Andrés Cholula": {
        "estado": "Puebla",
        "urgencias": "911 / Seguridad San Andrés Cholula: 222 261-8100",
        "contraloria": "Contraloría Municipal San Andrés Cholula — sanandrescholula.gob.mx",
        "dif": "DIF San Andrés Cholula — 222 261-8100",
        "juzgado_civico": "Juzgado Municipal San Andrés Cholula",
        "proteccion_civil": "Protección Civil San Andrés Cholula — 222 261-8100",
        "atencion_ciudadana": "sanandrescholula.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de San Andrés Cholula.",
    },

    # ── CHIHUAHUA ─────────────────────────────────────────────────────────
    "Ciudad Juárez": {
        "estado": "Chihuahua",
        "urgencias": "911 / Policía Juárez: 656 649-3400",
        "contraloria": "Contraloría Municipal Juárez — juarez.gob.mx",
        "dif": "DIF Juárez — 656 649-3400",
        "juzgado_civico": "Juzgado Municipal Ciudad Juárez",
        "proteccion_civil": "Protección Civil Juárez — 656 649-3400",
        "atencion_ciudadana": "juarez.gob.mx / denuncia anónima: 089",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Juárez.",
    },
    "Chihuahua": {
        "estado": "Chihuahua",
        "urgencias": "911 / Policía Chihuahua: 614 429-3300",
        "contraloria": "Contraloría Municipal Chihuahua — municipiochihuahua.gob.mx",
        "dif": "DIF Chihuahua — 614 429-3300",
        "juzgado_civico": "Juzgado Municipal Chihuahua",
        "proteccion_civil": "Protección Civil Chihuahua — 614 429-3300",
        "atencion_ciudadana": "municipiochihuahua.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Chihuahua.",
    },

    # ── COAHUILA ──────────────────────────────────────────────────────────
    "Saltillo": {
        "estado": "Coahuila",
        "urgencias": "911 / Policía Saltillo: 844 412-7373",
        "contraloria": "Contraloría Municipal Saltillo — saltillo.gob.mx",
        "dif": "DIF Saltillo — 844 412-7373",
        "juzgado_civico": "Juzgado Municipal Saltillo",
        "proteccion_civil": "Protección Civil Saltillo — 844 412-7373",
        "atencion_ciudadana": "saltillo.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Saltillo.",
    },
    "Torreón": {
        "estado": "Coahuila",
        "urgencias": "911 / Policía Torreón: 871 719-0000",
        "contraloria": "Contraloría Municipal Torreón — torreon.gob.mx",
        "dif": "DIF Torreón — 871 719-0000",
        "juzgado_civico": "Juzgado Municipal Torreón",
        "proteccion_civil": "Protección Civil Torreón — 871 719-0000",
        "atencion_ciudadana": "torreon.gob.mx / denuncia: 871 719-0000",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Torreón.",
    },

    # ── SONORA ────────────────────────────────────────────────────────────
    "Hermosillo": {
        "estado": "Sonora",
        "urgencias": "911 / Policía Hermosillo: 662 289-6700",
        "contraloria": "Contraloría Municipal Hermosillo — hermosillo.gob.mx",
        "dif": "DIF Hermosillo — 662 289-6700",
        "juzgado_civico": "Juzgado Municipal Hermosillo",
        "proteccion_civil": "Protección Civil Hermosillo — 662 289-6700",
        "atencion_ciudadana": "hermosillo.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Hermosillo.",
    },
    "Nogales": {
        "estado": "Sonora",
        "urgencias": "911 / Policía Nogales: 631 312-0018",
        "contraloria": "Contraloría Municipal Nogales — nogales.gob.mx",
        "dif": "DIF Nogales — 631 312-0018",
        "juzgado_civico": "Juzgado Municipal Nogales",
        "proteccion_civil": "Protección Civil Nogales — 631 312-0018",
        "atencion_ciudadana": "nogales.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Nogales.",
    },

    # ── SINALOA ───────────────────────────────────────────────────────────
    "Culiacán": {
        "estado": "Sinaloa",
        "urgencias": "911 / Policía Culiacán: 667 716-1070",
        "contraloria": "Contraloría Municipal Culiacán — culiacan.gob.mx",
        "dif": "DIF Culiacán — 667 716-1070",
        "juzgado_civico": "Juzgado Municipal Culiacán",
        "proteccion_civil": "Protección Civil Culiacán — 667 716-1070",
        "atencion_ciudadana": "culiacan.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Culiacán.",
    },
    "Mazatlán": {
        "estado": "Sinaloa",
        "urgencias": "911 / Policía Mazatlán: 669 981-2900",
        "contraloria": "Contraloría Municipal Mazatlán — mazatlan.gob.mx",
        "dif": "DIF Mazatlán — 669 981-2900",
        "juzgado_civico": "Juzgado Municipal Mazatlán",
        "proteccion_civil": "Protección Civil Mazatlán — 669 981-2900",
        "atencion_ciudadana": "mazatlan.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Mazatlán.",
    },

    # ── TAMAULIPAS ────────────────────────────────────────────────────────
    "Tampico": {
        "estado": "Tamaulipas",
        "urgencias": "911 / Policía Tampico: 833 212-6900",
        "contraloria": "Contraloría Municipal Tampico — tampico.gob.mx",
        "dif": "DIF Tampico — 833 212-6900",
        "juzgado_civico": "Juzgado Municipal Tampico",
        "proteccion_civil": "Protección Civil Tampico — 833 212-6900",
        "atencion_ciudadana": "tampico.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Tampico.",
    },
    "Reynosa": {
        "estado": "Tamaulipas",
        "urgencias": "911 / Policía Reynosa: 899 921-1000",
        "contraloria": "Contraloría Municipal Reynosa — reynosa.gob.mx",
        "dif": "DIF Reynosa — 899 921-1000",
        "juzgado_civico": "Juzgado Municipal Reynosa",
        "proteccion_civil": "Protección Civil Reynosa — 899 921-1000",
        "atencion_ciudadana": "reynosa.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Reynosa.",
    },
    "Nuevo Laredo": {
        "estado": "Tamaulipas",
        "urgencias": "911 / Policía Nuevo Laredo: 867 711-0000",
        "contraloria": "Contraloría Municipal Nuevo Laredo — nuevolaredo.gob.mx",
        "dif": "DIF Nuevo Laredo — 867 711-0000",
        "juzgado_civico": "Juzgado Municipal Nuevo Laredo",
        "proteccion_civil": "Protección Civil Nuevo Laredo — 867 711-0000",
        "atencion_ciudadana": "nuevolaredo.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Nuevo Laredo.",
    },

    # ── GUANAJUATO ────────────────────────────────────────────────────────
    "León": {
        "estado": "Guanajuato",
        "urgencias": "911 / Policía León: 477 710-1000",
        "contraloria": "Contraloría Municipal León — leon.gob.mx",
        "dif": "DIF León — 477 710-1000",
        "juzgado_civico": "Juzgado Municipal León",
        "proteccion_civil": "Protección Civil León — 477 710-1000",
        "atencion_ciudadana": "leon.gob.mx / App 'León Ciudadano' / denuncia: 477 710-1000",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de León.",
    },
    "Irapuato": {
        "estado": "Guanajuato",
        "urgencias": "911 / Policía Irapuato: 462 624-0100",
        "contraloria": "Contraloría Municipal Irapuato — irapuato.gob.mx",
        "dif": "DIF Irapuato — 462 624-0100",
        "juzgado_civico": "Juzgado Municipal Irapuato",
        "proteccion_civil": "Protección Civil Irapuato — 462 624-0100",
        "atencion_ciudadana": "irapuato.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Irapuato.",
    },

    # ── QUERÉTARO ─────────────────────────────────────────────────────────
    "Querétaro": {
        "estado": "Querétaro",
        "urgencias": "911 / Policía Querétaro: 442 192-8000",
        "contraloria": "Contraloría Municipal Querétaro — queretaro.gob.mx",
        "dif": "DIF Querétaro — 442 192-8000",
        "juzgado_civico": "Juzgado Municipal Querétaro",
        "proteccion_civil": "Protección Civil Querétaro — 442 192-8000",
        "atencion_ciudadana": "queretaro.gob.mx / denuncia ciudadana: 442 192-8000",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Querétaro.",
    },

    # ── VERACRUZ ──────────────────────────────────────────────────────────
    "Veracruz": {
        "estado": "Veracruz",
        "urgencias": "911 / Policía Veracruz: 229 989-4545",
        "contraloria": "Contraloría Municipal Veracruz — veracruz.gob.mx",
        "dif": "DIF Veracruz — 229 989-4545",
        "juzgado_civico": "Juzgado Municipal Veracruz",
        "proteccion_civil": "Protección Civil Veracruz — 229 989-4545",
        "atencion_ciudadana": "veracruz.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Puerto de Veracruz.",
    },
    "Xalapa": {
        "estado": "Veracruz",
        "urgencias": "911 / Policía Xalapa: 228 812-3700",
        "contraloria": "Contraloría Municipal Xalapa — xalapa.gob.mx",
        "dif": "DIF Xalapa — 228 812-3700",
        "juzgado_civico": "Juzgado Municipal Xalapa",
        "proteccion_civil": "Protección Civil Xalapa — 228 812-3700",
        "atencion_ciudadana": "xalapa.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Xalapa.",
    },
    "Coatzacoalcos": {
        "estado": "Veracruz",
        "urgencias": "911 / Policía Coatzacoalcos: 921 211-7600",
        "contraloria": "Contraloría Municipal Coatzacoalcos — coatzacoalcos.gob.mx",
        "dif": "DIF Coatzacoalcos — 921 211-7600",
        "juzgado_civico": "Juzgado Municipal Coatzacoalcos",
        "proteccion_civil": "Protección Civil Coatzacoalcos — 921 211-7600",
        "atencion_ciudadana": "coatzacoalcos.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno de Coatzacoalcos.",
    },

    # ── YUCATÁN ───────────────────────────────────────────────────────────
    "Mérida": {
        "estado": "Yucatán",
        "urgencias": "911 / Policía Mérida: 999 942-0060",
        "contraloria": "Contraloría Municipal Mérida — merida.gob.mx",
        "dif": "DIF Mérida — 999 942-0060",
        "juzgado_civico": "Juzgado Municipal Mérida",
        "proteccion_civil": "Protección Civil Mérida — 999 942-0060",
        "atencion_ciudadana": "merida.gob.mx / App 'Mérida Ciudad' / denuncia: 999 942-0060",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Mérida.",
    },

    # ── QUINTANA ROO ──────────────────────────────────────────────────────
    "Cancún": {
        "estado": "Quintana Roo",
        "urgencias": "911 / Policía Benito Juárez (Cancún): 998 884-1913",
        "contraloria": "Contraloría Municipal Benito Juárez — municipiobenitojuarez.gob.mx",
        "dif": "DIF Benito Juárez (Cancún) — 998 884-1913",
        "juzgado_civico": "Juzgado Municipal Benito Juárez (Cancún)",
        "proteccion_civil": "Protección Civil Cancún — 998 884-1913",
        "atencion_ciudadana": "municipiobenitojuarez.gob.mx / denuncia: 998 884-1913",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio Benito Juárez (Cancún).",
    },
    "Playa del Carmen": {
        "estado": "Quintana Roo",
        "urgencias": "911 / Policía Solidaridad (Playa del Carmen): 984 873-0093",
        "contraloria": "Contraloría Municipal Solidaridad — solidaridad.gob.mx",
        "dif": "DIF Solidaridad — 984 873-0093",
        "juzgado_civico": "Juzgado Municipal Solidaridad (Playa del Carmen)",
        "proteccion_civil": "Protección Civil Solidaridad — 984 873-0093",
        "atencion_ciudadana": "solidaridad.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Solidaridad.",
    },

    # ── MICHOACÁN ─────────────────────────────────────────────────────────
    "Morelia": {
        "estado": "Michoacán",
        "urgencias": "911 / Policía Morelia: 443 113-0000",
        "contraloria": "Contraloría Municipal Morelia — morelia.gob.mx",
        "dif": "DIF Morelia — 443 113-0000",
        "juzgado_civico": "Juzgado Municipal Morelia",
        "proteccion_civil": "Protección Civil Morelia — 443 113-0000",
        "atencion_ciudadana": "morelia.gob.mx / denuncia: 443 113-0000",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Morelia.",
    },

    # ── AGUASCALIENTES ────────────────────────────────────────────────────
    "Aguascalientes": {
        "estado": "Aguascalientes",
        "urgencias": "911 / Policía Aguascalientes: 449 910-9800",
        "contraloria": "Contraloría Municipal Aguascalientes — aguascalientes.gob.mx",
        "dif": "DIF Aguascalientes — 449 910-9800",
        "juzgado_civico": "Juzgado Municipal Aguascalientes",
        "proteccion_civil": "Protección Civil Aguascalientes — 449 910-9800",
        "atencion_ciudadana": "aguascalientes.gob.mx / denuncia: 449 910-9800",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Aguascalientes.",
    },

    # ── GUERRERO ──────────────────────────────────────────────────────────
    "Acapulco": {
        "estado": "Guerrero",
        "urgencias": "911 / Policía Acapulco: 744 484-4500",
        "contraloria": "Contraloría Municipal Acapulco — acapulco.gob.mx",
        "dif": "DIF Acapulco — 744 484-4500",
        "juzgado_civico": "Juzgado Municipal Acapulco",
        "proteccion_civil": "Protección Civil Acapulco — 744 484-4500",
        "atencion_ciudadana": "acapulco.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Acapulco.",
    },

    # ── CHIAPAS ───────────────────────────────────────────────────────────
    "Tuxtla Gutiérrez": {
        "estado": "Chiapas",
        "urgencias": "911 / Policía Tuxtla: 961 602-0260",
        "contraloria": "Contraloría Municipal Tuxtla Gutiérrez — tuxtlagutierrez.gob.mx",
        "dif": "DIF Tuxtla Gutiérrez — 961 602-0260",
        "juzgado_civico": "Juzgado Municipal Tuxtla Gutiérrez",
        "proteccion_civil": "Protección Civil Tuxtla — 961 602-0260",
        "atencion_ciudadana": "tuxtlagutierrez.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Tuxtla Gutiérrez.",
    },
    "Tapachula": {
        "estado": "Chiapas",
        "urgencias": "911 / Policía Tapachula: 962 625-2000",
        "contraloria": "Contraloría Municipal Tapachula — tapachula.gob.mx",
        "dif": "DIF Tapachula — 962 625-2000",
        "juzgado_civico": "Juzgado Municipal Tapachula",
        "proteccion_civil": "Protección Civil Tapachula — 962 625-2000",
        "atencion_ciudadana": "tapachula.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Tapachula.",
    },

    # ── OAXACA ────────────────────────────────────────────────────────────
    "Oaxaca": {
        "estado": "Oaxaca",
        "urgencias": "911 / Policía Oaxaca: 951 502-0100",
        "contraloria": "Contraloría Municipal Oaxaca — oaxaca.gob.mx",
        "dif": "DIF Oaxaca — 951 502-0100",
        "juzgado_civico": "Juzgado Municipal Oaxaca de Juárez",
        "proteccion_civil": "Protección Civil Oaxaca — 951 502-0100",
        "atencion_ciudadana": "oaxaca.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Oaxaca de Juárez. Nota: Oaxaca tiene municipios con sistemas normativos indígenas (usos y costumbres) reconocidos — en esas comunidades aplican sus propias autoridades y reglamentos internos.",
    },

    # ── SAN LUIS POTOSÍ ───────────────────────────────────────────────────
    "San Luis Potosí": {
        "estado": "San Luis Potosí",
        "urgencias": "911 / Policía SLP: 444 826-0035",
        "contraloria": "Contraloría Municipal SLP — sanluispotosi.gob.mx",
        "dif": "DIF San Luis Potosí — 444 826-0035",
        "juzgado_civico": "Juzgado Municipal San Luis Potosí",
        "proteccion_civil": "Protección Civil SLP — 444 826-0035",
        "atencion_ciudadana": "sanluispotosi.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de San Luis Potosí.",
    },

    # ── TABASCO ───────────────────────────────────────────────────────────
    "Villahermosa": {
        "estado": "Tabasco",
        "urgencias": "911 / Policía Villahermosa: 993 358-1500",
        "contraloria": "Contraloría Municipal Centro (Villahermosa) — centrotabasco.gob.mx",
        "dif": "DIF Centro Tabasco — 993 358-1500",
        "juzgado_civico": "Juzgado Municipal Centro (Villahermosa)",
        "proteccion_civil": "Protección Civil Villahermosa — 993 358-1500",
        "atencion_ciudadana": "centrotabasco.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Centro (Villahermosa).",
    },

    # ── HIDALGO ───────────────────────────────────────────────────────────
    "Pachuca": {
        "estado": "Hidalgo",
        "urgencias": "911 / Policía Pachuca: 771 713-5500",
        "contraloria": "Contraloría Municipal Pachuca — pachuca.gob.mx",
        "dif": "DIF Pachuca — 771 713-5500",
        "juzgado_civico": "Juzgado Municipal Pachuca de Soto",
        "proteccion_civil": "Protección Civil Pachuca — 771 713-5500",
        "atencion_ciudadana": "pachuca.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Pachuca de Soto.",
    },

    # ── MORELOS ───────────────────────────────────────────────────────────
    "Cuernavaca": {
        "estado": "Morelos",
        "urgencias": "911 / Policía Cuernavaca: 777 329-2300",
        "contraloria": "Contraloría Municipal Cuernavaca — cuernavaca.gob.mx",
        "dif": "DIF Cuernavaca — 777 329-2300",
        "juzgado_civico": "Juzgado Municipal Cuernavaca",
        "proteccion_civil": "Protección Civil Cuernavaca — 777 329-2300",
        "atencion_ciudadana": "cuernavaca.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Cuernavaca.",
    },

    # ── DURANGO ───────────────────────────────────────────────────────────
    "Durango": {
        "estado": "Durango",
        "urgencias": "911 / Policía Durango: 618 137-0000",
        "contraloria": "Contraloría Municipal Durango — durango.gob.mx",
        "dif": "DIF Durango — 618 137-0000",
        "juzgado_civico": "Juzgado Municipal Durango",
        "proteccion_civil": "Protección Civil Durango — 618 137-0000",
        "atencion_ciudadana": "durango.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Durango.",
    },

    # ── NAYARIT ───────────────────────────────────────────────────────────
    "Tepic": {
        "estado": "Nayarit",
        "urgencias": "911 / Policía Tepic: 311 213-6060",
        "contraloria": "Contraloría Municipal Tepic — tepic.gob.mx",
        "dif": "DIF Tepic — 311 213-6060",
        "juzgado_civico": "Juzgado Municipal Tepic",
        "proteccion_civil": "Protección Civil Tepic — 311 213-6060",
        "atencion_ciudadana": "tepic.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Tepic.",
    },

    # ── TLAXCALA ──────────────────────────────────────────────────────────
    "Tlaxcala": {
        "estado": "Tlaxcala",
        "urgencias": "911 / Policía Tlaxcala: 246 462-0000",
        "contraloria": "Contraloría Municipal Tlaxcala — tlaxcala-gobierno.gob.mx",
        "dif": "DIF Tlaxcala — 246 462-0000",
        "juzgado_civico": "Juzgado Municipal Tlaxcala",
        "proteccion_civil": "Protección Civil Tlaxcala — 246 462-0000",
        "atencion_ciudadana": "tlaxcala-gobierno.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Tlaxcala.",
    },

    # ── ZACATECAS ─────────────────────────────────────────────────────────
    "Zacatecas": {
        "estado": "Zacatecas",
        "urgencias": "911 / Policía Zacatecas: 492 922-0180",
        "contraloria": "Contraloría Municipal Zacatecas — zacatecas.gob.mx",
        "dif": "DIF Zacatecas — 492 922-0180",
        "juzgado_civico": "Juzgado Municipal Zacatecas",
        "proteccion_civil": "Protección Civil Zacatecas — 492 922-0180",
        "atencion_ciudadana": "zacatecas.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Zacatecas.",
    },

    # ── COLIMA ────────────────────────────────────────────────────────────
    "Colima": {
        "estado": "Colima",
        "urgencias": "911 / Policía Colima: 312 313-0272",
        "contraloria": "Contraloría Municipal Colima — colima.gob.mx",
        "dif": "DIF Colima — 312 313-0272",
        "juzgado_civico": "Juzgado Municipal Colima",
        "proteccion_civil": "Protección Civil Colima — 312 313-0272",
        "atencion_ciudadana": "colima.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Colima.",
    },
    "Manzanillo": {
        "estado": "Colima",
        "urgencias": "911 / Policía Manzanillo: 314 332-1004",
        "contraloria": "Contraloría Municipal Manzanillo — manzanillo.gob.mx",
        "dif": "DIF Manzanillo — 314 332-1004",
        "juzgado_civico": "Juzgado Municipal Manzanillo",
        "proteccion_civil": "Protección Civil Manzanillo — 314 332-1004",
        "atencion_ciudadana": "manzanillo.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Manzanillo.",
    },

    # ── CAMPECHE ──────────────────────────────────────────────────────────
    "Campeche": {
        "estado": "Campeche",
        "urgencias": "911 / Policía Campeche: 981 811-9500",
        "contraloria": "Contraloría Municipal Campeche — campeche.gob.mx",
        "dif": "DIF Campeche — 981 811-9500",
        "juzgado_civico": "Juzgado Municipal Campeche",
        "proteccion_civil": "Protección Civil Campeche — 981 811-9500",
        "atencion_ciudadana": "campeche.gob.mx",
        "reglamento_nota": "Reglamento de Policía y Buen Gobierno del Municipio de Campeche.",
    },
}


# Aliases para detectar el municipio desde texto libre
MUNICIPAL_ALIASES: dict[str, list[str]] = {
    "Benito Juárez": ["benito juarez", "colonia del valle", "narvarte", "insurgentes sur"],
    "Cuauhtémoc": ["cuauhtemoc cdmx", "centro historico cdmx", "tepito", "doctores"],
    "Miguel Hidalgo": ["miguel hidalgo", "polanco", "lomas de chapultepec", "santa fe cdmx"],
    "Iztapalapa": ["iztapalapa", "ciudad nezahualcoyotl", "iztapalapa cdmx"],
    "Tlalpan": ["tlalpan"],
    "Coyoacán": ["coyoacan", "pedregal", "san angel"],
    "Guadalajara": ["guadalajara", "gdl"],
    "Zapopan": ["zapopan"],
    "Tlaquepaque": ["tlaquepaque", "san pedro tlaquepaque"],
    "Tonalá": ["tonala jalisco"],
    "Monterrey": ["monterrey", "mty"],
    "San Nicolás de los Garza": ["san nicolas de los garza", "san nicolas nl"],
    "Guadalupe": ["guadalupe nl", "guadalupe nuevo leon"],
    "San Pedro Garza García": ["san pedro garza garcia", "san pedro nl", "garza garcia"],
    "Ecatepec": ["ecatepec", "ecatepec de morelos"],
    "Naucalpan": ["naucalpan", "naucalpan de juarez"],
    "Toluca": ["toluca"],
    "Nezahualcóyotl": ["nezahualcoyotl", "neza", "ciudad neza"],
    "Tijuana": ["tijuana"],
    "Mexicali": ["mexicali"],
    "Ensenada": ["ensenada bc"],
    "Puebla": ["puebla capital", "puebla de zaragoza", "heroica puebla"],
    "San Andrés Cholula": ["san andres cholula", "cholula"],
    "Ciudad Juárez": ["ciudad juarez", "cd juarez", "juarez chihuahua"],
    "Chihuahua": ["chihuahua capital", "chihuahua ciudad"],
    "Saltillo": ["saltillo"],
    "Torreón": ["torreon", "la laguna"],
    "Hermosillo": ["hermosillo"],
    "Nogales": ["nogales sonora"],
    "Culiacán": ["culiacan", "culiacan sinaloa"],
    "Mazatlán": ["mazatlan"],
    "Tampico": ["tampico"],
    "Reynosa": ["reynosa"],
    "Nuevo Laredo": ["nuevo laredo"],
    "León": ["leon guanajuato", "leon gto"],
    "Irapuato": ["irapuato"],
    "Querétaro": ["queretaro capital", "queretaro ciudad", "santiago de queretaro"],
    "Veracruz": ["veracruz puerto", "puerto de veracruz", "boca del rio"],
    "Xalapa": ["xalapa", "jalapa"],
    "Coatzacoalcos": ["coatzacoalcos"],
    "Mérida": ["merida", "merida yucatan"],
    "Cancún": ["cancun", "cancun quintana roo"],
    "Playa del Carmen": ["playa del carmen", "playacar"],
    "Morelia": ["morelia"],
    "Aguascalientes": ["aguascalientes capital", "aguascalientes ciudad"],
    "Acapulco": ["acapulco", "acapulco guerrero"],
    "Tuxtla Gutiérrez": ["tuxtla gutierrez", "tuxtla"],
    "Tapachula": ["tapachula"],
    "Oaxaca": ["oaxaca capital", "oaxaca de juarez", "oaxaca ciudad"],
    "San Luis Potosí": ["san luis potosi capital", "san luis potosi ciudad", "slp capital"],
    "Villahermosa": ["villahermosa", "centro tabasco"],
    "Pachuca": ["pachuca", "pachuca de soto"],
    "Cuernavaca": ["cuernavaca"],
    "Durango": ["durango capital", "victoria de durango"],
    "Tepic": ["tepic"],
    "Tlaxcala": ["tlaxcala capital", "tlaxcala ciudad"],
    "Zacatecas": ["zacatecas capital", "zacatecas ciudad"],
    "Colima": ["colima capital", "colima ciudad"],
    "Manzanillo": ["manzanillo colima"],
    "Campeche": ["campeche capital", "campeche ciudad", "san francisco de campeche"],
}


import re
import unicodedata

_STRIP = re.compile(r"[^a-z0-9\s]")


def _norm(text: str) -> str:
    d = unicodedata.normalize("NFKD", text.lower())
    s = "".join(c for c in d if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", _STRIP.sub(" ", s)).strip()


# Comisión Estatal de Derechos Humanos por estado — la vía estatal para
# quejas de abuso de autoridad cuando el municipio no tiene datos curados.
CEDH_BY_STATE: dict[str, str] = {
    "Aguascalientes": "Comisión de Derechos Humanos del Estado de Aguascalientes (CDHEA)",
    "Baja California": "Comisión Estatal de los Derechos Humanos de Baja California",
    "Baja California Sur": "Comisión Estatal de los Derechos Humanos de BCS",
    "Campeche": "Comisión de Derechos Humanos del Estado de Campeche (CODHECAM)",
    "Chiapas": "Comisión Estatal de los Derechos Humanos de Chiapas (CEDH)",
    "Chihuahua": "Comisión Estatal de los Derechos Humanos de Chihuahua (CEDH)",
    "Coahuila": "Comisión de los Derechos Humanos del Estado de Coahuila (CDHEC)",
    "Colima": "Comisión de Derechos Humanos del Estado de Colima (CDHEC)",
    "Ciudad de México": "Comisión de Derechos Humanos de la Ciudad de México (CDHCM)",
    "Durango": "Comisión Estatal de Derechos Humanos de Durango (CEDH)",
    "Estado de México": "Comisión de Derechos Humanos del Estado de México (CODHEM)",
    "Guanajuato": "Procuraduría de los Derechos Humanos del Estado de Guanajuato",
    "Guerrero": "Comisión de los Derechos Humanos del Estado de Guerrero (CODDEHUM)",
    "Hidalgo": "Comisión de Derechos Humanos del Estado de Hidalgo (CDHEH)",
    "Jalisco": "Comisión Estatal de Derechos Humanos Jalisco (CEDHJ)",
    "Michoacán": "Comisión Estatal de los Derechos Humanos de Michoacán (CEDH)",
    "Morelos": "Comisión de Derechos Humanos del Estado de Morelos (CDHEM)",
    "Nayarit": "Comisión de Defensa de los Derechos Humanos para el Estado de Nayarit",
    "Nuevo León": "Comisión Estatal de Derechos Humanos de Nuevo León (CEDHNL)",
    "Oaxaca": "Defensoría de los Derechos Humanos del Pueblo de Oaxaca (DDHPO)",
    "Puebla": "Comisión de Derechos Humanos del Estado de Puebla (CDH Puebla)",
    "Querétaro": "Defensoría de los Derechos Humanos de Querétaro (DDHQ)",
    "Quintana Roo": "Comisión de los Derechos Humanos del Estado de Quintana Roo (CDHEQROO)",
    "San Luis Potosí": "Comisión Estatal de Derechos Humanos de San Luis Potosí (CEDH)",
    "Sinaloa": "Comisión Estatal de los Derechos Humanos de Sinaloa (CEDH)",
    "Sonora": "Comisión Estatal de Derechos Humanos de Sonora (CEDH)",
    "Tabasco": "Comisión Estatal de los Derechos Humanos de Tabasco (CEDH)",
    "Tamaulipas": "Comisión de Derechos Humanos del Estado de Tamaulipas (CODHET)",
    "Tlaxcala": "Comisión Estatal de Derechos Humanos de Tlaxcala (CEDH)",
    "Veracruz": "Comisión Estatal de Derechos Humanos de Veracruz (CEDH)",
    "Yucatán": "Comisión de Derechos Humanos del Estado de Yucatán (CODHEY)",
    "Zacatecas": "Comisión de Derechos Humanos del Estado de Zacatecas (CDHEZ)",
}


def _slugify_domain(municipality: str) -> str:
    """Best-effort guess of the municipality's official domain. Most Mexican
    municipalities publish at <nombre>.gob.mx. It's a heuristic, not a
    guarantee — the generic block tells the user to verify it."""
    base = _norm(municipality).replace(" ", "")
    return f"{base}.gob.mx"


def detect_municipality(text: str) -> str | None:
    """Returns curated canonical municipality name if mentioned, else None.
    Only matches the ~65 municipalities with hand-verified contact data."""
    normalized = _norm(text)
    for municipality, aliases in MUNICIPAL_ALIASES.items():
        for alias in sorted(aliases, key=len, reverse=True):
            if re.search(rf"\b{re.escape(alias)}\b", normalized):
                return municipality
    return None


# Patterns that introduce a municipality name in free text: "municipio de X",
# "en el municipio de X", "soy de X", "vivo en X", "aquí en X". Captures the
# name that follows, up to a delimiter.
_MUNI_PATTERNS = [
    re.compile(r"municipio de ([a-zñáéíóú][a-zñáéíóú\s]{2,40}?)(?:[,.;]|$| en | del | de la )", re.IGNORECASE),
    re.compile(r"(?:soy|vivo|radico|estoy|resido|aqui) (?:de|en|por) ([a-zñáéíóú][a-zñáéíóú\s]{2,40}?)(?:[,.;]|$| en | del )", re.IGNORECASE),
]

# Words that are NOT municipality names even if they follow the pattern.
_MUNI_STOPWORDS = {
    "mi", "la", "el", "un", "una", "aqui", "alla", "casa", "trabajo",
    "mexico", "cdmx", "aca", "este", "ese", "esta",
}


def extract_municipality_name(text: str) -> str | None:
    """Pulls a plausible municipality name out of free text using surface
    patterns, for the ~2,400 municipalities without curated contacts. Returns
    the name in title case, or None. This is intentionally loose — a wrong
    guess just produces a generic 'verify locally' block, never bad legal info."""
    for pattern in _MUNI_PATTERNS:
        m = pattern.search(text)
        if m:
            candidate = m.group(1).strip()
            if _norm(candidate) in _MUNI_STOPWORDS or len(candidate) < 3:
                continue
            # Title-case each word, keep it short (max 4 words)
            words = candidate.split()[:4]
            return " ".join(w.capitalize() for w in words)
    return None


def get_municipal_contacts(municipality: str) -> dict[str, str] | None:
    return MUNICIPAL_CONTACTS.get(municipality)


def _generic_municipal_block(municipality: str, state: str | None) -> str:
    """Builds a valid contact block for ANY of Mexico's 2,478 municipalities/
    alcaldías from naming conventions that hold nationwide, even without a
    curated entry. Every Mexican municipality has a Contraloría, a DIF, a
    Juez Cívico/Municipal, and Protección Civil; every state has a CEDH."""
    domain = _slugify_domain(municipality)
    cedh = CEDH_BY_STATE.get(state or "", "la Comisión Estatal de Derechos Humanos de tu estado")
    state_label = f" ({state})" if state else ""

    is_cdmx = state == "Ciudad de México"
    org_word = "Alcaldía" if is_cdmx else "Municipio"
    reglamento = (
        "Reglamento de Policía y Buen Gobierno / Ley de Cultura Cívica de la CDMX"
        if is_cdmx
        else f"Reglamento de Policía y Buen Gobierno / Bando de Policía del Municipio de {municipality}"
    )

    lines = [
        f"\nCONTACTOS PARA {municipality.upper()}{state_label.upper()}:",
        "(Datos construidos con la estructura estándar de los municipios "
        "mexicanos — verifica el teléfono exacto en el sitio oficial, pues "
        "cambia con cada administración.)",
        "• Emergencias: 911 (nacional, cubre todo el territorio)",
        "• Denuncia anónima: 089 (nacional)",
        f"• Quejas contra policía municipal / abuso de autoridad: Contraloría "
        f"Interna del {org_word} de {municipality}, en el Palacio Municipal / "
        f"Presidencia Municipal. También la {cedh}.",
        f"• Atención a familia, menores y violencia familiar: Sistema DIF "
        f"del {org_word} de {municipality}.",
        f"• Infracciones y faltas administrativas: Juzgado Cívico / Juez "
        f"Calificador del {org_word} de {municipality}.",
        f"• Protección Civil del {org_word} de {municipality}.",
        f"• Sitio oficial probable: {domain} (verifícalo; si no existe, "
        f"busca '{municipality} {state or ''} gobierno municipal').",
        f"• Normativa local aplicable: {reglamento}.",
        "",
        "Da estos contactos de forma útil según el caso del usuario. Sé claro "
        "en que el teléfono debe confirmarlo en el sitio oficial.",
        "",
    ]
    return "\n".join(lines)


def municipal_contacts_block(municipality: str, state: str | None = None) -> str:
    """Formatted block to inject into the LLM prompt. Uses curated data when
    available, otherwise builds a valid generic block from the municipality
    name + state so all 2,478 municipalities are covered."""
    data = get_municipal_contacts(municipality)
    if not data:
        return _generic_municipal_block(municipality, state)
    lines = [
        f"\nCONTACTOS MUNICIPALES — {municipality.upper()} ({data['estado'].upper()}):",
        f"• Urgencias: {data['urgencias']} | 911 (nacional)",
        f"• Quejas contra policía / abuso: {data['contraloria']}",
        f"• Atención familiar y menores: {data['dif']}",
        f"• Infracciones y faltas admin: {data['juzgado_civico']}",
        f"• Protección Civil: {data['proteccion_civil']}",
        f"• Denuncia ciudadana: {data['atencion_ciudadana']}",
        f"• Nota normativa: {data['reglamento_nota']}",
        "• Denuncia anónima nacional: 089",
        "",
        "Usa estos contactos en tu respuesta cuando el caso lo requiera.",
        "",
    ]
    return "\n".join(lines)
