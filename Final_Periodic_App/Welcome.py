import streamlit as st
from PIL import Image
from auth_utils import require_auth, get_user_info, init_authenticator
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

# Initialize authenticator
authenticator = init_authenticator()

# Show login form
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    # Show logout button in sidebar
    authenticator.logout('Logout', 'sidebar')

    st.write("# Welcome to Stax Periodic Reviews")

    st.markdown(
        """
        These 3 Apps allow us to review transaction data directly from
        connectlite
    
        **👈 Select an app from the sidebar** to get started
    
        If an app isn't working correctly, reach out to Ryan Nolan on
        Slack or email ryan.nolan@fattmerchant.com
    
    
        ### Want to learn more?
        - Check out [SOP: Periodic Reviews](https://docs.google.com/document/d/14lSfkcIyaf7uZmkqRcoLKfCopqSWRzcnSh3I_gM4K2Q/edit)
        """
    )

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
