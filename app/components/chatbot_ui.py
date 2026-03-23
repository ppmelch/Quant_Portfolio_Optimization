import streamlit as st

def chatbot_ui(chatbot):

    st.markdown("### 🤖 Quant Assistant")

    context = chatbot.build_context()

    # memoria
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # mostrar historial
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # input
    prompt = st.chat_input("Ask about your portfolio...")

    if prompt:

        # guardar usuario
        st.session_state.chat_messages.append({
            "role": "user",
            "content": prompt
        })

        # construir mensajes
        messages = [
            {"role": "system", "content": context}
        ] + st.session_state.chat_messages[-6:]

        # respuesta
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chatbot.get_response(messages)
                st.write(reply)

        # guardar respuesta
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": reply
        })