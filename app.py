import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Prosegur Alarmas - Chatbot Facturación",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --bg: #0d0d0d;
        --panel: #171717;
        --panel-soft: #1e1e1e;
        --yellow: #f5c400;
        --yellow-soft: #ffde59;
        --text: #f5f5f5;
        --muted: #cfcfcf;
        --border: rgba(245, 196, 0, 0.25);
        --shadow: rgba(0, 0, 0, 0.28);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0d0d0d 0%, #141414 40%, #1a1a1a 100%);
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: #111111;
        border-right: 1px solid var(--border);
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .brand-box {
        background: linear-gradient(135deg, #f5c400 0%, #ffd84d 100%);
        color: #111111;
        border-radius: 18px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 12px 30px var(--shadow);
        border: 1px solid rgba(17, 17, 17, 0.15);
    }

    .brand-box h1 {
        margin: 0;
        font-size: 2.2rem;
        line-height: 1.1;
        font-weight: 800;
    }

    .brand-box p {
        margin: 0.35rem 0 0 0;
        font-size: 0.92rem;
        color: #1a1a1a;
        font-weight: 600;
    }

    .info-card {
        background: rgba(24, 24, 24, 0.9);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }

    .yellow-title {
        color: var(--yellow-soft);
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .chat-container {
        background: rgba(25, 25, 25, 0.82);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.8rem;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.2);
    }

    .stChatMessage {
        border-radius: 14px;
    }

    .stFileUploader > div {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid var(--border);
        border-radius: 14px;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--yellow) 0%, #ffd437 100%);
        color: #111111;
        font-weight: 700;
        border: none;
        border-radius: 12px;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #ffd437 0%, var(--yellow) 100%);
        color: #111111;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

QUESTIONS = [
    "¿Cuál es el proceso para validar un excel de facturación?",
    "¿Qué errores revisan al cargar archivos de facturación?",
    "¿Dónde subo el archivo para validar la facturación?",
    "¿Qué información necesito revisar antes de enviar el excel?",
    "¿Qué pasa si faltan columnas o datos en el archivo?",
    "¿Cómo se identifican errores de clientes o servicios?",
    "¿Qué es lo más importante para evitar rechazos?",
    "¿Cuáles son las validaciones principales del equipo?",
    "¿Qué hago si el sistema devuelve errores en la carga?",
    "¿Cuánto tarda la validación de un archivo?"
]

ANSWERS = [
    "El proceso comienza con la carga del Excel, revisión de columnas obligatorias, validación de datos y comparación con el sistema de facturación para detectar inconsistencias antes del envío.",
    "Los errores más comunes son columnas faltantes, servicios no activos, números de cliente duplicados, montos inconsistentes, fechas fuera de rango y campos vacíos o mal formateados.",
    "Podés subir el archivo desde el panel de carga de adjuntos de esta app. Allí se registran los documentos y se puede revisar la información antes de continuar con la validación.",
    "Antes de enviar, revisá que el archivo tenga cliente, servicio, periodo, importe, fechas y estado correctamente completados y con formato uniforme.",
    "Si faltan columnas o datos relevantes, el sistema suele devolver un error de validación y te obliga a corregir la información antes de continuar con la carga.",
    "Los errores de cliente o servicio se detectan al cruzar la información del Excel con la base operativa: nombres, códigos, estados activa/inactiva y datos asociados al contrato.",
    "Lo más importante es mantener la estructura del archivo, revisar campos obligatorios y confirmar que los importes, servicios y clientes coincidan con la información del sistema.",
    "Las validaciones principales incluyen formato de archivo, columnas obligatorias, datos duplicados, importes, fechas, estado del servicio y consistencia entre clientes, facturas y servicios.",
    "Si el sistema devuelve errores, revisá el detalle del problema, corrige el Excel y volvé a cargarlo. En muchos casos la solución es ajustar un dato puntual o completar una columna faltante.",
    "La validación suele depender del volumen del archivo, pero en general el flujo es rápido cuando el Excel está bien estructurado y no presenta inconsistencias relevantes."
]

@st.cache_resource
def prepare_chatbot():
    vectorizer = CountVectorizer(lowercase=True)
    question_vectors = vectorizer.fit_transform(QUESTIONS)
    return vectorizer, question_vectors

vectorizer, question_vectors = prepare_chatbot()


def get_response(user_input: str, threshold: float = 0.22) -> str:
    user_vector = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vector, question_vectors)[0]
    best_index = similarities.argmax()
    best_score = similarities[best_index]

    if best_score < threshold:
        return (
            "No tengo una respuesta exacta para esa consulta en este momento. "
            "Podés consultar por validaciones de Excel, errores de carga, datos faltantes, \n"
            "clientes, servicios, importes o el proceso de revisión del equipo de facturación."
        )

    return ANSWERS[best_index]


def show_brand_header():
    st.markdown(
        """
        <div class="brand-box">
            <h1>PROSEGUR<br>ALARMAS</h1>
            <p>Facturación · Validación · Control de Excel</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


show_brand_header()

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

left_col, right_col = st.columns([1.8, 1])
with left_col:
    st.markdown(
        """
        <div class='info-card'>
            <div class='yellow-title'>Avance de información</div>
            <p style='margin-top: 0.8rem; color: #f5f5f5; line-height: 1.7;'>
                El equipo de facturación trabaja con validaciones de información, revisión de archivos Excel,
                control de inconsistencias y seguimiento de errores detectados por otros sistemas.
                El objetivo es asegurar que la carga de datos sea correcta, completa y compatible con la operación del negocio.
            </p>
            <ul style='color: #f5f5f5; line-height: 1.8; margin: 0.5rem 0 0 1.2rem;'>
                <li>Control de datos y estructura del Excel.</li>
                <li>Revisión de clientes, servicios y montos.</li>
                <li>Detección de errores de validación y omisiones.</li>
                <li>Procesamiento y corrección antes del cierre.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    st.image(
        "https://images.unsplash.com/photo-1556157382-97eda2d62296?auto=format&fit=crop&w=900&q=80",
        caption="Facturación y control operativo",
        use_container_width=True,
    )

with st.sidebar:
    st.markdown("<div class='yellow-title' style='font-size: 0.8rem; margin-bottom: 0.6rem;'>Panel del equipo</div>", unsafe_allow_html=True)
    st.write("• Validación de facturación")
    st.write("• Control de Excel")
    st.write("• Detección de errores")
    st.write("• Revisión de clientes y servicios")
    st.write("• Seguimiento operativo")

    st.markdown("<hr style='border: 1px solid rgba(245,196,0,0.2); margin: 1rem 0;'>", unsafe_allow_html=True)

    st.subheader("Flujo de trabajo")
    st.write("1. Carga del archivo")
    st.write("2. Validación de columnas")
    st.write("3. Revisión de inconsistencias")
    st.write("4. Corrección y reenvío")

    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

st.subheader("📎 Carga de archivos y adjuntos")
uploaded_files = st.file_uploader(
    "Subí el Excel o archivo que necesites revisar",
    type=["xlsx", "xls", "csv", "txt"],
    accept_multiple_files=True,
)

if uploaded_files:
    st.success(f"Se cargaron {len(uploaded_files)} archivo(s):")
    for file in uploaded_files:
        st.write(f"- {file.name}")

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! Soy el asistente del equipo de facturación de Prosegur Alarmas. ¿Querés revisar un archivo, validar inconsistencias o consultar el proceso de carga?"
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribí tu consulta sobre facturación o validación..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = get_response(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("</div>", unsafe_allow_html=True)
