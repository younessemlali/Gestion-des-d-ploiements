import streamlit as st
import pandas as pd
from datetime import datetime
import json
import plotly.graph_objects as go
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Gestion des Déploiements - Randstad",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    /* Thème principal */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Titre principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Boutons personnalisés */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des états de session
if 'deployments' not in st.session_state:
    st.session_state.deployments = []

# Configuration des plateformes et modules
PLATFORMS = {
    "Temporaris": {"color": "#FF6B6B", "modules": ["Commandes", "Contrats", "Heures", "Factures"]},
    "Baps": {"color": "#4ECDC4", "modules": ["Commandes", "Heures", "RAV", "Factures"]},
    "Pilott": {"color": "#45B7D1", "modules": ["Contrats", "Heures", "RA", "Factures"]},
    "Pixid": {"color": "#96CEB4", "modules": ["Commandes", "Contrats", "RAV", "RA"]},
    "PeoPulse": {"color": "#FECA57", "modules": ["Heures", "RAV", "RA", "Factures"]},
    "Fieldglass": {"color": "#FD79A8", "modules": ["Commandes", "Contrats", "Heures", "Factures"]},
    "Beeline": {"color": "#A29BFE", "modules": ["Commandes", "Heures", "RA", "Factures"]},
    "Instant": {"color": "#74B9FF", "modules": ["Contrats", "Heures", "RAV", "Factures"]}
}

# Fonction pour générer l'email
def generate_email(platform, client, siret, modules):
    modules_str = ", ".join(modules)
    email_content = f"""
Objet: Déploiement {platform} - {client}

Bonjour,

Nous vous confirmons le déploiement de la plateforme {platform} pour le client suivant :

**Informations client :**
- Nom : {client}
- SIRET : {siret}

**Modules à déployer :**
{modules_str}

**Prochaines étapes :**
1. Création des accès utilisateurs
2. Configuration des modules sélectionnés
3. Formation des utilisateurs
4. Tests de validation

L'équipe de déploiement se tient à votre disposition pour toute question.

Cordialement,
L'équipe Déploiement Randstad
    """
    return email_content

# Interface principale
st.markdown('<div class="main-header"><h1>🚀 Gestion des Déploiements</h1><p>Plateforme de génération automatique de documents</p></div>', unsafe_allow_html=True)

# Sidebar avec les statistiques
with st.sidebar:
    st.markdown("### 📊 Tableau de Bord")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Déploiements", len(st.session_state.deployments), "+2")
    with col2:
        st.metric("En cours", "3", "-1")
    
    st.markdown("---")
    
    # Graphique des plateformes
    if st.session_state.deployments:
        platform_counts = pd.DataFrame(st.session_state.deployments)['platform'].value_counts()
        fig = px.pie(values=platform_counts.values, names=platform_counts.index, 
                     title="Répartition par Plateforme")
        st.plotly_chart(fig, use_container_width=True)

# Formulaire principal
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Nouveau Déploiement")
    
    platform = st.selectbox(
        "**Plateforme**",
        options=list(PLATFORMS.keys()),
        help="Sélectionnez la plateforme à déployer"
    )
    
    st.markdown(f"**Modules disponibles pour {platform}:**")
    available_modules = PLATFORMS[platform]["modules"]
    
    modules = st.multiselect(
        "**Modules souhaités**",
        options=available_modules,
        default=available_modules[:2],
        help="Sélectionnez les modules à déployer"
    )
    
    col_client1, col_client2 = st.columns(2)
    with col_client1:
        client_name = st.text_input(
            "**Nom du Client**",
            placeholder="Ex: Randstad France",
            help="Entrez le nom complet du client"
        )
    
    with col_client2:
        siret = st.text_input(
            "**SIRET**",
            placeholder="Ex: 123 456 789 00012",
            max_chars=17,
            help="Numéro SIRET du client"
        )

with col2:
    st.markdown("### 🎯 Actions")
    
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: {PLATFORMS[platform]['color']};">Résumé du déploiement</h4>
        <p><b>Plateforme:</b> {platform}</p>
        <p><b>Client:</b> {client_name if client_name else 'Non renseigné'}</p>
        <p><b>Modules:</b> {len(modules)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📧 Générer Email", use_container_width=True):
        if client_name and siret and modules:
            email_content = generate_email(platform, client_name, siret, modules)
            st.session_state.email_content = email_content
            st.session_state.deployments.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "platform": platform,
                "client": client_name,
                "siret": siret,
                "modules": modules
            })
            st.success("✅ Email généré avec succès!")
        else:
            st.error("⚠️ Veuillez remplir tous les champs")
    
    # Note temporaire
    st.info("📄 La génération PDF sera disponible prochainement")

# Zone d'affichage des résultats
st.markdown("---")

# Affichage de l'email
if 'email_content' in st.session_state:
    st.markdown("### 📧 Email Généré")
    st.text_area("Contenu de l'email", st.session_state.email_content, height=400)
    st.code(st.session_state.email_content, language=None)

# Historique des déploiements
if st.session_state.deployments:
    st.markdown("---")
    st.markdown("### 📜 Historique des Déploiements")
    
    df = pd.DataFrame(st.session_state.deployments)
    df['modules'] = df['modules'].apply(lambda x: ', '.join(x))
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "date": st.column_config.TextColumn("Date", width="medium"),
            "platform": st.column_config.TextColumn("Plateforme", width="medium"),
            "client": st.column_config.TextColumn("Client", width="large"),
            "siret": st.column_config.TextColumn("SIRET", width="medium"),
            "modules": st.column_config.TextColumn("Modules", width="large"),
        }
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; padding: 2rem;">
    <p>Développé par l'équipe IT Randstad | Support: support@randstad.fr</p>
</div>
""", unsafe_allow_html=True)
