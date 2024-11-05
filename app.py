import streamlit as st
import hashlib
from data_loader import load_data, load_description_options
from datetime import datetime

# Lista de usuários permitidos com senhas em hash
USERS = {
    "joao@contajá.com.br": hashlib.sha256("9uM2£g55V>~|".encode()).hexdigest(),
    "livia@contaja.com.br": hashlib.sha256("6\'=9xU1[DpS".encode()).hexdigest(),
    "hudson@contaja.com.br": hashlib.sha256(":r)&526Q5rG-".encode()).hexdigest(),
    "rafael@contaja.com.br": hashlib.sha256("naa8}3Uy8Sq~".encode()).hexdigest(),
    "daniele@contaja.com.br": hashlib.sha256("naa8}3Uy8Sq~".encode()).hexdigest()

}

# Função de autenticação
def authenticate(email, password):
    if email in USERS:
        return USERS[email] == hashlib.sha256(password.encode()).hexdigest()
    return False

# Controle de sessão para manter o login do usuário
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Interface de login
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if authenticate(email, password):
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
        else:
            st.error("Email ou senha incorretos.")
else:
    # Interface principal do aplicativo
    st.sidebar.header("Filtros")
    start_date = st.sidebar.date_input("Data de início", value=None)
    end_date = st.sidebar.date_input("Data de término", value=None)
    user_app_hash = st.sidebar.text_input("Usuário (user_app_hash)")

    # Dropdown para "Assistente" com as opções do campo "description"
    description_options = [""] + load_description_options()  
    description = st.sidebar.selectbox("Assistente (description)", options=description_options)

    # Controle de paginação
    items_per_page = st.sidebar.selectbox("Itens por página", options=[10, 20, 50, 100], index=1)
    page_number = st.sidebar.number_input("Página", min_value=1, step=1, value=1)
    offset = (page_number - 1) * items_per_page

    # Botão para aplicar filtros
    if st.sidebar.button("OK"):
        df = load_data(
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None,
            user_app_hash=user_app_hash if user_app_hash else None,
            description=description if description else None,
            limit=items_per_page,
            offset=offset
        )
    else:
        df = load_data(limit=items_per_page, offset=offset)

    # Exibição das Conversas
    latest_messages = df.sort_values('created_at').groupby('thread_ID').last().reset_index()
    latest_messages = latest_messages.sort_values('created_at', ascending=False)

    st.title("Todas as Conversas")

    for _, row in latest_messages.iterrows():
        thread_id = row['thread_ID']
        last_update = row['created_at']
        user_app_hash = row['user_app_hash']
        description = row['description']
        
        st.markdown(
            f"### Hash do Usuário: {user_app_hash}  <br>"
            f"Assistente: {description}  <br>"
            f"Última interação: {last_update.strftime('%d/%m/%Y %H:%M')}",
            unsafe_allow_html=True
        )
        
        thread_df = df[df['thread_ID'] == thread_id].sort_values('created_at')
        
        for _, msg_row in thread_df.iterrows():
            role = "Usuário" if msg_row['role'] == 'user' else "Assistente"
            st.markdown(f"**{role}**: {msg_row['text']}")
        
        st.markdown("---")

    # Botão de logout
    if st.button("Sair"):
        st.session_state.logged_in = False
