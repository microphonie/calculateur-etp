import streamlit as st

st.set_page_config(page_title="Calculateur ETP")

st.title("Calculateur d'heures ETP - Convention ECLAT")
st.write("Cet outil vous permet de vérifier les données affichées sur votre fiche de paie, à partir de vos heures réalisées sur l'année (septembre à août).")

heures_reelles = st.number_input(
    "Heures réelles réalisées (septembre à août) :",
    min_value=0.0,
    step=0.5,
    format="%.2f"
)

def heures_mensuelles_lissees(heures):
    return (heures + (heures * 0.10)) / 12

def heures_hebdo_lissees(heures_mensuelles):
    return heures_mensuelles / (52 / 12)

def heures_mensuelles_ETP(heures_hebdo):
    return (heures_hebdo * 151.67) / 24

if heures_reelles > 0:
    hm = heures_mensuelles_lissees(heures_reelles)
    hh = heures_hebdo_lissees(hm)
    etp = heures_mensuelles_ETP(hh)

    st.success(f"Heures mensuelles lissées : **{hm:.2f} h**")
    st.info(f"Heures hebdomadaires lissées : **{hh:.2f} h**")
    st.write(f"Heures mensuelles ETP (affichées sur la fiche de paie) : **{etp:.2f} h**")

    st.caption("Calcul basé sur la convention ECLAT, IDCC 1518, ETP enseignant-e-s (24h hebdomadaires).")
