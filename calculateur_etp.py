import streamlit as st

st.set_page_config(page_title="Calculateur ETP", page_icon="logo_mustang.png")
st.image("logo_mustang.png", width=400)
st.title("Calculateur d'heures ETP - Convention ECLAT")
st.write("Cet outil vous permet de vérifier les données affichées sur votre fiche de paie, à partir de vos heures réalisées sur l'année (septembre à août).")

mode = st.radio(
    "Type de conversion",
    ("Conversion heures réelles annuelles ➝ ETP", "Conversion heures réelles hebdomadaires ➝ ETP", "Conversion ETP ➝ heures réelles")
)

valpoint = 7.15
coeff = 362.03

def heures_mensuelles_lissees(heures):
    return (heures * 1.10) / 12

def heures_hebdo_lissees(heures_mensuelles):
    return heures_mensuelles / (52 / 12)

def heures_mensuelles_ETP(heures_hebdo):
    return (heures_hebdo * ((35 * 52)/12)) / 24

def etp_vers_heures_reelles(etp):
    h_hebdo = (etp * 24) / ((35 * 52)/12)
    h_mensuelles = h_hebdo * (52 / 12)
    heures_reelles = (h_mensuelles * 12) / 1.10
    return heures_reelles

def salaire_brut(heures_hebdo, valpoint, coeff):
    return (heures_hebdo * valpoint * coeff) / 24

def taux_horaire(salaire_brut, heures_mensuelles_lissees):
    return salaire_brut / heures_mensuelles_lissees


if mode == "Conversion heures réelles annuelles ➝ ETP":
    heures_reelles = st.number_input(
        "Heures réelles réalisées sur l'année (de septembre à août) :",
        min_value=0.0, step=0.5, format="%.2f"
    )
    if heures_reelles > 0:
        hm = heures_mensuelles_lissees(heures_reelles)
        hh = heures_hebdo_lissees(hm)
        etp = etp_vers_heures_reelles(hm)
        sb = salaire_brut(hh, valpoint, coeff)
        th = taux_horaire(sb, hm)

        st.info(f"Heures mensuelles lissées : **{hm:.2f} h**")
        st.info(f"Heures hebdomadaires lissées : **{hh:.2f} h**")
        st.success(f"Heures mensuelles ETP (affichées sur la fiche de paie) : **{etp:.2f} h**")
        st.info(f"Salaire brut mensuel correspondant : **{sb:.2f} €**")
        st.info(f"Taux horaire : **{th:.2f} €/h**")
        st.caption("Calcul basé sur la convention ECLAT, IDCC 1518, ETP enseignant·e·s (24h hebdomadaires). Valeur du point d'indice au 1er janvier 2025 : 7,15€.")

elif mode == "Conversion heures réelles hebdomadaires ➝ ETP":
    heures_hebdo_reelles = st.number_input(
        "Nombre d'heures travaillées par semaine :",
        min_value=0.0, step=0.5, format="%.2f"
    )
    semaines_travaillees = 33  # calendrier Musiques Tangentes
    if heures_hebdo_reelles > 0:
        heures_annuelles_reelles = heures_hebdo_reelles * semaines_travaillees
        hm = heures_mensuelles_lissees(heures_annuelles_reelles)
        hh = heures_hebdo_lissees(hm)
        etp = etp_vers_heures_reelles(hm)
        sb = salaire_brut(hh, valpoint, coeff)
        th = taux_horaire(sb, hm)

        st.info(f"Heures réelles annuelles (basées sur {semaines_travaillees} semaines travaillées) : **{heures_annuelles_reelles:.2f} h**")
        st.success(f"Heures mensuelles ETP (affichées sur la fiche de paie) : **{etp:.2f} h**")
        st.info(f"Salaire brut mensuel correspondant : **{sb:.2f} €**")
        st.info(f"Taux horaire : **{th:.2f} €/h**")
        st.caption(f"Calcul basé sur {semaines_travaillees} semaines travaillées (zone C). Vacances scolaires non comptées. // Convention ECLAT, IDCC 1518, ETP enseignant·e·s (24h hebdomadaires). Valeur du point d'indice au 1er janvier 2025 : 7,15€.")

elif mode == "Conversion ETP ➝ heures réelles":
    etp = st.number_input(
        "Heures ETP affichées sur votre fiche de paie :",
        min_value=0.0, step=0.5, format="%.2f"
    )
    if etp > 0:
        heures_reelles = etp_vers_heures_reelles(etp)
        heures_hebdo_reelles = heures_reelles / 33
        hm = heures_mensuelles_lissees(heures_reelles)
        hh = heures_hebdo_lissees(hm)
        sb = salaire_brut(hh, valpoint, coeff)
        th = taux_horaire(sb, hm)
        st.success(f"Heures réelles hebdomadaires : **{heures_hebdo_reelles:.2f} h**")
        st.info(f"Heures réelles annuelles (de septembre à août) : **{heures_reelles:.2f} h**")
        st.info(f"Salaire brut mensuel correspondant : **{sb:.2f} €**")
        st.info(f"Taux horaire : **{th:.2f} €/h**")
        st.caption("Calcul basé sur la convention ECLAT, IDCC 1518, ETP enseignant·e·s (24h hebdomadaires).")