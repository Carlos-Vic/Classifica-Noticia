import streamlit as st
from database import db
import pandas as pd
import plotly.express as px  # type: ignore[import-untyped]  # pyright: ignore[reportMissingTypeStubs]

vies_geral = db.mostra_total_vies()
vies_portal = db.mostra_vies_por_portal()
portais_sem_scraper = db.mostra_portal_sem_scraper()

df_vies_geral = pd.DataFrame(vies_geral, columns=['vies', 'total_de_artigos'])
df_vies_portal = pd.DataFrame(vies_portal, columns=['vies', 'portal', 'total_de_artigos'])

fig_vies_total = px.bar(df_vies_geral, x='vies', y='total_de_artigos', 
                labels={'vies': 'Viés', 'total_de_artigos':'Total de Artigos'},
                color='vies',
                color_discrete_map={'Esquerda': 'tomato', 'Direita': 'steelblue'},
                title='Total de Artigos por Viés')

fig_vies_portal = px.bar(df_vies_portal, x='portal', y='total_de_artigos', 
                               color='vies',
                               barmode='group',
                               labels={'vies': 'Viés', 'portal': 'Portal', 'total_de_artigos': 'Total de Artigos'},
                               color_discrete_map={'Esquerda': 'tomato', 'Direita': 'steelblue'},
                               height=400,
                               title='Total de Artigos por Portal e Viés')

st.metric(label='Total de artigos cadastrados', value=df_vies_geral['total_de_artigos'].sum())
st.plotly_chart(fig_vies_total)
st.divider()
st.plotly_chart(fig_vies_portal)
st.divider()


if portais_sem_scraper:
    df_portal_sem_scraper = pd.DataFrame(
        portais_sem_scraper, columns=["portal_sem_cadastro", "total_links"]
    ).sort_values(by=["total_links"], ascending=True)

    fig_portal_sem_scraper = px.bar(df_portal_sem_scraper, x="total_links", y="portal_sem_cadastro",
                                    labels={"portal_sem_cadastro": "Portal sem cadastro", "total_links": "Total de Links"},
                                    orientation='h',
                                    title='Portais sem cadastro que mais apareceram').update_xaxes(dtick=1)

    st.plotly_chart(fig_portal_sem_scraper)
