import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------
# Configuración de la aplicación
# ---------------------------------------------------------
st.set_page_config(
    page_title="Chatbot de Atención al Público",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------------------------------------
# Base de conocimiento: preguntas frecuentes y respuestas
# ---------------------------------------------------------
QUESTIONS = [
    "¿Cuál es el horario de atención?",
    "¿Dónde está ubicada la tienda?",
    "¿Cuáles son los métodos de pago disponibles?",
    "¿Tienen envíos a todo el país?",
    "¿Qué productos tienen en stock?",
    "¿Cómo puedo hacer una devolución?"
]

ANSWERS = [
    "Nuestro horario de atención es de lunes a viernes, de 9:00 AM a 6:00 PM.",
    "Nuestra tienda está ubicada en Calle Ficticia 123, Ciudad Ficticia.",
    "Aceptamos pagos con tarjeta de crédito, débito, PayPal y transferencia bancaria.",
    "Sí, realizamos envíos a todo el país.",
    "Tenemos una amplia variedad de productos. Consulta nuestro catálogo online.",
    "Para hacer una devolución, por favor contáctanos dentro de los 30 días después de la compra."
]

# ---------------------------------------------------------
# Preparación del modelo de similitud
# ---------------------------------------------------------
@st.cache_resource
def prepare_chatbot():
    vectorizer = CountVectorizer(lowercase=True)
    question_vectors = vectorizer.fit_transform(QUESTIONS)
    return vectorizer, question_vectors

vectorizer, question_vectors = prepare_chatbot()


def get_response(user_input: str, threshold: float = 0.20) -> str:
    """Devuelve la respuesta asociada a la FAQ más similar."""
    user_vector = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vector, question_vectors)[0]

    best_index = similarities.argmax()
    best_score = similarities[best_index]

    if best_score < threshold:
        return (
            "Lo siento, todavía no tengo información suficiente para responder "
            "esa consulta. Puedes preguntarme sobre horarios, ubicación, pagos, "
            "envíos, stock o devoluciones."
        )

    return ANSWERS[best_index]


# ---------------------------------------------------------
# Interfaz
# ---------------------------------------------------------
st.title("🤖 Chatbot de Atención al Público")
st.caption("Asistente para responder preguntas frecuentes de clientes.")

with st.sidebar:
    st.subheader("Temas disponibles")
    st.write("• Horario de atención")
    st.write("• Ubicación")
    st.write("• Métodos de pago")
    st.write("• Envíos")
    st.write("• Stock")
    st.write("• Devoluciones")

    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! Soy el chatbot de atención al público. ¿En qué puedo ayudarte hoy?"
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    response = get_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
