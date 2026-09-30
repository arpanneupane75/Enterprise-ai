
import os
import requests
import streamlit as st


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/ask",
)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="EnterpriseRAG",
    page_icon="📚",
    layout="wide",
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📚 EnterpriseRAG")

st.caption(
    "Conversational Retrieval-Augmented Generation "
    "for grounded enterprise document search"
)

st.divider()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("About EnterpriseRAG")

    st.write(
        """
        EnterpriseRAG combines semantic retrieval,
        query transformation, CrossEncoder reranking,
        context expansion, and LLM generation to answer
        questions from enterprise documents.
        """
    )

    st.subheader("RAG Pipeline")

    st.markdown(
        """
        1. 🔎 Query Transformation
        2. 🧠 Dense Retrieval
        3. 📊 CrossEncoder Reranking
        4. 🔗 Context Expansion
        5. 🤖 Groq LLM
        6. 📑 Source Attribution
        """
    )

    st.divider()

    st.caption("Backend: FastAPI")
    st.caption("Vector Store: ChromaDB")
    st.caption("LLM: Groq")

    st.divider()

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


# --------------------------------------------------
# Conversation History
# --------------------------------------------------

if st.session_state.messages:

    st.subheader("Conversation")

    for message in st.session_state.messages:

        role = message["role"]

        if role == "user":

            with st.chat_message("user"):
                st.write(message["content"])

        elif role == "assistant":

            with st.chat_message("assistant"):

                st.write(message["content"])

                sources = message.get(
                    "sources",
                    [],
                )

                if sources:

                    with st.expander(
                        f"📚 Sources ({len(sources)})"
                    ):

                        for index, source in enumerate(
                            sources,
                            start=1,
                        ):

                            source_name = source.get(
                                "source",
                                "Unknown document",
                            )

                            page = source.get(
                                "page",
                                "N/A",
                            )

                            chunk_id = source.get(
                                "chunk_id",
                                "N/A",
                            )

                            st.markdown(
                                f"""
                                **{index}. 📄 {source_name}**

                                Page: {page}  
                                Chunk: `{chunk_id}`
                                """
                            )


# --------------------------------------------------
# Question Input
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about the enterprise handbook..."
)


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

if question:

    question = question.strip()

    if not question:

        st.warning("Please enter a question.")

    else:

        # ----------------------------------------------
        # Display current user message
        # ----------------------------------------------

        with st.chat_message("user"):

            st.write(question)

        # ----------------------------------------------
        # Build history BEFORE adding current question
        # ----------------------------------------------

        history = [
            {
                "role": message["role"],
                "content": message["content"],
            }
            for message in st.session_state.messages
        ]

        # ----------------------------------------------
        # Call RAG API
        # ----------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching documents and generating answer..."
            ):

                try:

                    response = requests.post(
                        API_URL,
                        json={
                            "question": question,
                            "history": history,
                        },
                        timeout=120,
                    )

                    response.raise_for_status()

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer returned.",
                    )

                    sources = data.get(
                        "sources",
                        [],
                    )

                    # ----------------------------------
                    # Display Answer
                    # ----------------------------------

                    st.write(answer)

                    # ----------------------------------
                    # Display Sources
                    # ----------------------------------

                    if sources:

                        with st.expander(
                            f"📚 Sources ({len(sources)})"
                        ):

                            for index, source in enumerate(
                                sources,
                                start=1,
                            ):

                                source_name = source.get(
                                    "source",
                                    "Unknown document",
                                )

                                page = source.get(
                                    "page",
                                    "N/A",
                                )

                                chunk_id = source.get(
                                    "chunk_id",
                                    "N/A",
                                )

                                st.markdown(
                                    f"""
                                    **{index}. 📄 {source_name}**

                                    Page: {page}  
                                    Chunk: `{chunk_id}`
                                    """
                                )

                                evidence = source.get(
                                    "evidence"
                                )

                                if evidence:

                                    st.info(
                                        evidence
                                    )

                    else:

                        st.info(
                            "No source information was returned."
                        )

                    # ----------------------------------
                    # Save Conversation
                    # ----------------------------------

                    st.session_state.messages.append(
                        {
                            "role": "user",
                            "content": question,
                        }
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "The request timed out. "
                        "Please try again."
                    )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to the RAG API. "
                        f"Make sure FastAPI is running at "
                        f"`{API_URL}`."
                    )

                except requests.exceptions.HTTPError as e:

                    st.error(
                        f"RAG API returned an error: {e}"
                    )

                except ValueError:

                    st.error(
                        "The API returned an invalid response."
                    )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Could not connect to the RAG API: {e}"
                    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "EnterpriseRAG • FastAPI + LangChain + ChromaDB + Groq"
)

