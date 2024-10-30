import streamlit as st
import boto3
import json


user_avatar = r""C:\Users\alerii\Desktop\chat_bot.png""
ai_avatar   = r""C:\Users\alerii\Desktop\chat_bot.png""

temperature = 0.1
max_token   = 2048



# Funzione che si occupa di chiamare la Lambda e restituire l'output
def invoke_lambda(user_prompt, max_tokens, temperature):
    # Creazione client per Lambda
    client = boto3.client('lambda')

    # Preparare il payload per Lambda
    payload = {
        'user_prompt': user_prompt,
        'max_tokens' : max_tokens,
        'temperature': temperature
    }

    # Chiamata alla Lambda
    response = client.invoke(
        FunctionName   ='text-to-sql-bedrock-kb',
        InvocationType ='RequestResponse',
        Payload        = json.dumps(payload)
    )

    # Lettura del payload di risposta
    response_payload = json.loads(response['Payload'].read())
    return response_payload



# Funzione che si occupa della formattazione della history della chat
def chat_history():
  if "messages" not in st.session_state:
    st.session_state.messages = []
  
  if "id" not in st.session_state:
    st.session_state.id = ""
  
  for message in st.session_state.messages:
    avatar = ""
    if str(message["role"]) == "user":
      avatar = user_avatar
    else:
      avatar = ai_avatar

    with st.chat_message(message["role"], avatar = avatar):
      st.markdown(message["content"], unsafe_allow_html = True)



# Funzione che si occupa di gestire a livello grafico il prompt e la risposta del chatbot
def center_prompt():
    prompt = st.chat_input('Ask me a question')
    
    if prompt:
        formatted_prompt = f"<i>{prompt}</i>"
        st.session_state.messages.append({"role": "user", "content": formatted_prompt})
        
        with st.chat_message("user", avatar = user_avatar):
            st.markdown(formatted_prompt, unsafe_allow_html = True)
    
        with st.chat_message("assistant", avatar = ai_avatar):
            message_placeholder = st.empty()
            message_placeholder.write("...")
            result = invoke_lambda(prompt, max_token, temperature)
            
        if result:
            sql_query = result['sql_string']
            answer    = result['body']
            formatted_message = f"""
                <p style="color: #a2a4ba; font-style: italic;">Query SQL generata:</p>
                <p>{sql_query}</p>
                <hr style="border-color: #a2a4ba;">
                <p style="color: #a2a4ba; font-style: italic;">Risposta in linguaggio naturale:</p>
                <p>{answer}</p>
            """
            
            st.session_state.messages.append({"role": "assistant", "content": formatted_message})
            message_placeholder.empty()
            st.markdown(formatted_message, unsafe_allow_html = True)



# Funzione principale
def main():
    st.set_page_config(
    page_title            = "Virtual Assistant",
    page_icon             = "🤖",
    layout                = "centered",
    initial_sidebar_state = "expanded",
)

    st.markdown("<h2 style='text-align: center; font-family: Poppins, sans-serif;'>Welcome to your virtual assistant &#128516;</h2>", unsafe_allow_html=True)
    st.markdown("""<h3 style='text-align: center; font-family: Montserrat, sans-serif;'>Try to ask a question about your database!</h3>
        <hr style="border:1px solid; border-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet) 1;">""", unsafe_allow_html=True)
    chat_history()
    center_prompt()


# Chiamata alla funzione principale
main()