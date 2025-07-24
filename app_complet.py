import streamlit as st
import pandas as pd
from datetime import datetime
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from io import BytesIO
import base64
from PIL import Image as PILImage
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
    
    /* Selectbox styling */
    .stSelectbox > label {
        color: #4a5568;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Success/Error messages */
    .success-message {
        background-color: #48bb78;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f7fafc;
    }
    
    /* Platform cards */
    .platform-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: 600;
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

ALL_MODULES = ["Commandes", "Contrats", "Heures", "RAV", "RA", "Factures"]

# Fonctions utilitaires
def generate_email(platform, client, siret, modules):
    """Génère le contenu de l'email de déploiement"""
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

def generate_pdf(platform, client, siret, modules):
    """Génère un PDF de procédure de déploiement"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Titre
    story.append(Paragraph(f"Procédure de Déploiement {platform}", title_style))
    story.append(Spacer(1, 20))
    
    # Informations client
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12
    )
    
    story.append(Paragraph("<b>Informations Client</b>", styles['Heading2']))
    story.append(Paragraph(f"<b>Nom:</b> {client}", info_style))
    story.append(Paragraph(f"<b>SIRET:</b> {siret}", info_style))
    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}", info_style))
    story.append(Spacer(1, 20))
    
    # Modules
    story.append(Paragraph("<b>Modules à Déployer</b>", styles['Heading2']))
    modules_data = [["Module", "Status", "Responsable"]]
    for module in modules:
        modules_data.append([module, "À déployer", "À assigner"])
    
    modules_table = Table(modules_data, colWidths=[200, 150, 150])
    modules_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(modules_table)
    story.append(Spacer(1, 30))
    
    # Étapes de déploiement
    story.append(Paragraph("<b>Étapes de Déploiement</b>", styles['Heading2']))
    steps = [
        "1. Vérification des prérequis techniques",
        "2. Création des environnements (Test/Production)",
        "3. Configuration des modules sélectionnés",
        "4. Import des données initiales",
        "5. Création des comptes utilisateurs",
        "6. Tests de validation",
        "7. Formation des utilisateurs clés",
        "8. Mise en production",
        "9. Support post-déploiement (2 semaines)"
    ]
    
    for step in steps:
        story.append(Paragraph(step, info_style))
    
    story.append(PageBreak())
    
    # Checklist
    story.append(Paragraph("<b>Checklist de Déploiement</b>", styles['Heading2']))
    checklist_data = [
        ["Tâche", "Complété", "Date", "Responsable"],
        ["Environnement de test créé", "☐", "", ""],
        ["Modules configurés", "☐", "", ""],
        ["Données importées", "☐", "", ""],
        ["Utilisateurs créés", "☐", "", ""],
        ["Tests validés", "☐", "", ""],
        ["Formation effectuée", "☐", "", ""],
        ["Go-Live approuvé", "☐", "", ""],
    ]
    
    checklist_table = Table(checklist_data, colWidths=[200, 60, 100, 140])
    checklist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(checklist_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# Interface principale
st.markdown('<div class="main-header"><h1>🚀 Gestion des Déploiements</h1><p>Plateforme de génération automatique de documents</p></div>', unsafe_allow_html=True)

# Sidebar avec les statistiques
with st.sidebar:
    st.markdown("### 📊 Tableau de Bord")
    
    # Métriques
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
    
    # Sélection de la plateforme
    platform = st.selectbox(
        "**Plateforme**",
        options=list(PLATFORMS.keys()),
        help="Sélectionnez la plateforme à déployer"
    )
    
    # Affichage des modules disponibles pour la plateforme
    st.markdown(f"**Modules disponibles pour {platform}:**")
    available_modules = PLATFORMS[platform]["modules"]
    
    modules = st.multiselect(
        "**Modules souhaités**",
        options=available_modules,
        default=available_modules[:2],
        help="Sélectionnez les modules à déployer"
    )
    
    # Informations client
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
    
    # Carte de prévisualisation
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: {PLATFORMS[platform]['color']};">Résumé du déploiement</h4>
        <p><b>Plateforme:</b> {platform}</p>
        <p><b>Client:</b> {client_name if client_name else 'Non renseigné'}</p>
        <p><b>Modules:</b> {len(modules)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Boutons d'action
    if st.button("📧 Générer Email", use_container_width=True):
        if client_name and siret and modules:
            email_content = generate_email(platform, client_name, siret, modules)
            st.session_state.email_content = email_content
            st.success("✅ Email généré avec succès!")
        else:
            st.error("⚠️ Veuillez remplir tous les champs")
    
    if st.button("📄 Générer PDF", use_container_width=True):
        if client_name and siret and modules:
            pdf_buffer = generate_pdf(platform, client_name, siret, modules)
            st.session_state.pdf_buffer = pdf_buffer
            
            # Ajouter au historique
            st.session_state.deployments.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "platform": platform,
                "client": client_name,
                "siret": siret,
                "modules": modules
            })
            
            st.success("✅ PDF généré avec succès!")
        else:
            st.error("⚠️ Veuillez remplir tous les champs")

# Zone d'affichage des résultats
st.markdown("---")

col_results1, col_results2 = st.columns([1, 1])

# Affichage de l'email
with col_results1:
    if 'email_content' in st.session_state:
        st.markdown("### 📧 Email Généré")
        st.text_area("Contenu de l'email", st.session_state.email_content, height=400)
        
        # Bouton pour copier
        st.code(st.session_state.email_content, language=None)

# Téléchargement du PDF
with col_results2:
    if 'pdf_buffer' in st.session_state:
        st.markdown("### 📄 Document PDF")
        
        # Aperçu (simulé)
        st.info("📋 Le PDF contient:\n- Page de garde\n- Informations client\n- Liste des modules\n- Procédure détaillée\n- Checklist de validation")
        
        # Bouton de téléchargement
        st.download_button(
            label="⬇️ Télécharger le PDF",
            data=st.session_state.pdf_buffer,
            file_name=f"deploiement_{platform}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

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
