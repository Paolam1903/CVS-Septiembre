import pandas as pd

# =====================
# REGLA DE DISTRIBUCIÓN
# =====================
def calcular_distribucion(n_asesores, cvs, nombre=None, rol=None):

    cvs = str(cvs).upper()
    nombre = str(nombre).upper() if nombre else ""
           
    # ==================================================
    # 🔴 REGLA ESPECIAL FRONTINO Y SEGOVIA
    # ==================================================
    if cvs in ["FRONTINO", "SEGOVIA"]:
        if rol == "LIDER":
            return 0.50
        else:
            return 0.50

    # ==================================================
    # EL BAGRE
    # ==================================================

    if cvs == "EL BAGRE":

        # Líder
        if rol == "LIDER":
            return 936 / 3500

        # Darly
        elif "DARLY" in nombre:
            return 1161 / 3500

        # Jeider
        elif "JEIDER" in nombre:
            return 1403 / 3500

    # ==================================================
    # METRO EST. SAN ANTONIO
    # ==================================================

    if cvs == "METRO EST. SAN ANTONIO":

        # Líder
        if rol == "LIDER":
            return 770 / 1000

        # Daniel
        elif "DANIEL" in nombre:
            return 92 / 1000

        # Jeider
        elif "JEIDER" in nombre:
            return 138 / 1000            

    # ==================================================
    # JUNIN
    # ==================================================

    if cvs == "JUNIN":

        # Líder
        if rol == "LIDER":
            return 575.1 / 6800

        # Nasly Johanna
        elif "NASLY" in nombre:
            return 1813.3 / 6800

        # Jessica
        elif "JESSICA" in nombre:
            return 1813.3 / 6800

        # Sandra Milena
        elif "SANDRA" in nombre:
            return 1813.3 / 6800

        # Yuliana
        elif "YULIANA" in nombre:
            return 785 / 6800

    # ==================================================
    # SABANETA
    # ==================================================

    if cvs == "SABANETA":

        # LÃ­der Sandra - 40%
        if rol == "LIDER":
            return 1040 / 2600

        # Andrea
        elif "ANDREA" in nombre:
            return 480 / 2600

        # Luz
        elif "LUZ" in nombre:
            return 120 / 2600

        # Elizabeth
        elif "ELIZABETH" in nombre:
            return 960 / 2600

        

    # ==================================================
    # ENVIGADO
    # ==================================================

    if cvs == "ENVIGADO":

        # Líder
        if rol == "LIDER":
            return 915.5 / 3500

        # Yessica
        elif "YESSICA" in nombre:
            return 1373 / 3500

        # Luz Enith
        elif "LUZ" in nombre:
            return 1211.5 / 3500

    # ==================================================
    # BELLO
    # ==================================================

    if cvs == "BELLO":

        # Líder
        if rol == "LIDER":
            return 713 / 2850

        # Cristian
        elif "CRISTIAN" in nombre:
            return 1069 / 2850

        # Elizabeth
        elif "ELIZABETH" in nombre:
            return 411 / 2850

        # Diana
        elif "DIANA" in nombre:
            return 658 / 2850

    # ==================================================
    # ITAGUI
    # ==================================================

    if cvs == "ITAGUI":

        # Líder
        if rol == "LIDER":
            return 625 / 2500

        # Dailyn
        elif "DAILYN" in nombre:
            return 938 / 2500

        # Diana
        elif "DIANA" in nombre:
            return 361 / 2500

        # Andrea
        elif "ANDREA" in nombre:
            return 577 / 2500

    
    # ==================================================
    # 🔴 REGLAS NORMALES
    # ==================================================

    # Si no hay asesores
    if n_asesores == 0:
        return 1.0

    if rol == "LIDER":

        if n_asesores == 1:
            return 0.40
        elif n_asesores == 2:
            return 0.25
        elif n_asesores >= 3:
            return 0.20

    else:

        if n_asesores == 1:
            return 0.60
        elif n_asesores == 2:
            return 0.375
        elif n_asesores >= 3:
            return 0.266

    return 1.0


# =================================================
# META GENERAL + EJECUCIÓN (RESUMEN POR CVS)
# =================================================
def resumen_meta_general_por_cvs(df):
    resultados = []

    for sucursal, grupo in df.groupby("Sucursal"):
        meta_total = grupo["Meta_General"].iloc[0]

        n_asesores = grupo[grupo["Rol"] == "ASESOR"]["Cedula_Vendedor"].nunique()
        pct_lider, pct_asesores = calcular_distribucion(n_asesores, sucursal)


        puntos_lider = grupo[grupo["Rol"] == "LIDER"]["Puntos"].sum()
        puntos_asesores = grupo[grupo["Rol"] == "ASESOR"]["Puntos"].sum()

        resultados.append({
            "Sucursal": sucursal,
            "Estructura": f"1 Líder + {n_asesores} Asesor(es)",

            "Meta CVS": meta_total,

            "Meta Líder": meta_total * pct_lider,
            "Ejecutado Líder": puntos_lider,
            "Cumplimiento Líder %": round(
                (puntos_lider / (meta_total * pct_lider)) * 100, 2
            ) if meta_total * pct_lider > 0 else 0,

            "Meta Asesores": meta_total * pct_asesores,
            "Ejecutado Asesores": puntos_asesores,
            "Cumplimiento Asesores %": round(
                (puntos_asesores / (meta_total * pct_asesores)) * 100, 2
            ) if meta_total * pct_asesores > 0 else 0,
        })

    return pd.DataFrame(resultados)


# =================================================
# KPI POR PRODUCTO + EJECUCIÓN (RESUMEN POR CVS)
# =================================================
def resumen_kpi_producto_por_cvs(df):
    resultados = []

    for (sucursal, producto), grupo in df.groupby(["Sucursal", "Producto"]):
        meta_producto = grupo["Meta_Producto"].iloc[0]

        n_asesores = grupo[grupo["Rol"] == "ASESOR"]["Cedula_Vendedor"].nunique()
        pct_lider, pct_asesores = calcular_distribucion(n_asesores, sucursal)


        puntos_lider = grupo[grupo["Rol"] == "LIDER"]["Puntos"].sum()
        puntos_asesores = grupo[grupo["Rol"] == "ASESOR"]["Puntos"].sum()

        resultados.append({
            "Sucursal": sucursal,
            "Producto": producto,

            "Meta Producto": meta_producto,

            "Meta Líder": meta_producto * pct_lider,
            "Ejecutado Líder": puntos_lider,
            "Cumplimiento Líder %": round(
                (puntos_lider / (meta_producto * pct_lider)) * 100, 2
            ) if meta_producto * pct_lider >= 0 else 0,

            "Meta Asesores": meta_producto * pct_asesores,
            "Ejecutado Asesores": puntos_asesores,
            "Cumplimiento Asesores %": round(
                (puntos_asesores / (meta_producto * pct_asesores)) * 100, 2
            ) if meta_producto * pct_asesores >= 0 else 0,
        })

    return pd.DataFrame(resultados)
