import streamlit as st

st.set_page_config(page_title="Calculateur ETP", page_icon="logo_mustang.png")
st.image("logo_mustang.png", width=400)
st.title("Calculateur d'heures ETP - Convention ECLAT")
st.write("Cet outil vous permet de vérifier les données affichées sur votre fiche de paie, à partir de vos heures réalisées sur l'année (septembre à août).")

mode = st.radio(
    "Type de conversion",
    ("Conversion heures réelles ➝ ETP", "Conversion ETP ➝ heures réelles")
)

valpoint = 7.15
coeff = 362.03

def heures_mensuelles_lissees(heures):
    return (heures * 1.10) / 12

def heures_hebdo_lissees(heures_mensuelles):
    return heures_mensuelles / (52 / 12)

def heures_mensuelles_ETP(heures_hebdo):
    return (heures_hebdo * 151.67) / 24

def etp_vers_heures_reelles(etp):
    h_hebdo = (etp * 24) / 151.67
    h_mensuelles = h_hebdo * (52 / 12)
    heures_reelles = (h_mensuelles * 12) / 1.10
    return heures_reelles

def salaire_brut(heures_hebdo, valpoint, coeff):
    return (heures_hebdo * valpoint * coeff) / 24

def taux_horaire(salaire_brut, heures_reelles):
    return salaire_brut / heures_reelles


if mode == "Conversion heures réelles ➝ ETP":
    heures_reelles = st.number_input(
        "Heures réelles réalisées sur l'année (de septembre à août) :",
        min_value=0.0, step=0.5, format="%.2f"
    )
    if heures_reelles > 0:
        hm = heures_mensuelles_lissees(heures_reelles)
        hh = heures_hebdo_lissees(hm)
        etp = etp_vers_heures_reelles(hm)
        sb = salaire_brut(hh, valpoint, coeff)
        th = taux_horaire(sb, heures_reelles)

        st.success(f"Heures mensuelles lissées : **{hm:.2f} h**")
        st.info(f"Heures hebdomadaires lissées : **{hh:.2f} h**")
        st.write(f"Heures mensuelles ETP (affichées sur la fiche de paie) : **{etp:.2f} h**")
        st.info(f"Salaire brut mensuel correspondant : **{sb:.2f} h**")
        st.info(f"Taux horaire : **{th:.2f} h**")
        st.caption("Calcul basé sur la convention ECLAT, IDCC 1518, ETP enseignant·e·s (24h hebdomadaires).")

else:
    etp = st.number_input(
        "Heures ETP affichées sur votre fiche de paie :",
        min_value=0.0, step=0.5, format="%.2f"
    )
    if etp > 0:
        hh, hm, heures_reelles = etp_vers_heures_reelles(etp)
        st.success(f"📊 Heures réelles annuelles (de septembre à août) : **{heures_reelles:.2f} h**")

        st.caption("Calcul basé sur la convention ECLAT, IDCC 1518, ETP enseignant·e·s (24h hebdomadaires).")