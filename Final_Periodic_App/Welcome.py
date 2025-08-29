import streamlit as st
from PIL import Image
from auth_utils import require_auth, get_user_info

sys.path.append(os.path.dirname(os.path.dirname(__file__)))



st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)


# This will check authentication and redirect if not logged in
if require_auth("Your Page Title"):
    # Your protected page content goes here
    user_info = get_user_info()
    
    #image = Image.open('Final_Periodic_App/Stax_Banner.png')
    
    #st.image(image)
    
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
