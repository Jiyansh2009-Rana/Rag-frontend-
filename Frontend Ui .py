import streamlit as st
import requests
import mimetypes
Base_url = "https://rag-backend-kpyv.vercel.app"

st.set_page_config (page_title = "Rag Based llm for (pdf Data)",layout = "wide")


st.title("📋 Rag Based llm and Upload (Pdf Data) 📝")
st.markdown ("Power By Groq llm As a llm ,,  Jina-embeddings-v3 As a Embedding  Model And SupaBase As a Vector DB")


with st.sidebar:
    st.header ("Upload Data In format 'Pdf' ")
    uploaded_file = st.file_uploader ("Choose your Pdf Data", type =[ "pdf","csv","xlsx","txt","docx"])
    
                mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    
    if st.button ("upload your Data"):
        if uploaded_file is not None:
            with st.spinner ("proceesing pdf..."):
                files = {
                            "file" : (
                            uploaded_file.name,
                             uploaded_file.getvalue(),                                 mime_type
                             )
                            }
                           
                response = requests.post(f"{Base_url}/upload", files = files)
                
                if response.status_code == 200:
                    st.success(response.json().get("message"))
                else:
                    st.error(f"Error: {response.text}")
        else:
            st.warning("Please select a file first.")


st.header("💬 Ask Your Qusention Related Data And Other what you want 🌐")

sys_prompt = st.text_area("Enter your System Prompt Here (What Should be  Work LLM ? )",value = "Answer Accrding To The PDF If Answer Is Not Avalible In DB So Find On Authencat Soures Of Internet Or Resoures")

user_query = st.text_input("Enter your Question Here")

language = st.selectbox(
    "Select Answer Language",
    ["English", "Hindi", "French", "German", "Italian"]
)

if st.button("Ask AI"):
    if not user_query:
        st.warning("Please enter your question.")
    else:
        with st.spinner("Searching and generating answer..."):

            question = {
                "system_prompt": sys_prompt,
                "user_query": user_query,
                "language": language
            }

            response = requests.post(
                f"{Base_url}/Query",
                json=question
            )

            if response.status_code == 200:
                result = response.json()

                st.subheader("Answer:")
                st.write(result.get("answer"))

                with st.expander("View Related Content"):
                    related = result.get("sources", [])
                    if related:
                        for item in set(related):
                            st.info(f"Related Content: {item}")
                    else:
                        st.write("No specific content found.")
            else:
                st.error(f"Error: {response.text}")