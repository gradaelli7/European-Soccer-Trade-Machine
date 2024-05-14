import streamlit as st

def main():
    st.set_page_config(page_title="European Soccer Trade Machine")

    st.markdown(
        """
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                color: rgb(32, 8, 62);
            }
            header {
                background-color: #2c9dba;
                color: #f9f9f9;
                padding: 20px 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            .container {
                max-width: 700px;
                padding: 20px;
                border: 1px solid #070707; /* Add a border */
            }
            .btn {
                background-color: #2c9dba;
                color: #f9f9f9;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 10px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .btn:hover {
                background-color: #45a049;
            }
            .dropdown select {
                padding: 10px;
                font-size: 16px;
            }
            .budget {
                margin-top: 10px; /* Add space between team selection dropdown and transfer budget textbox */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.header("European Soccer Trade Machine")

    st.markdown(
        """
        <div class="container">
            <!-- Introduction -->
            <section id="introduction">
                <h2>Welcome to the European Soccer Trade Machine!</h2>
                <p>Your go-to resource for making informed transfer decisions in the highly competitive world of professional soccer. Our platform offers a comprehensive toolset designed to assist general managers and front office staff in navigating the complexities of player trades across various European leagues.</p>
                <!-- Add rest of your HTML content here -->
            </section>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()