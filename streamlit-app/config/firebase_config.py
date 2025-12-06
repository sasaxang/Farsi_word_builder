import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

def initialize_firebase():
    """
    Initialize Firebase Admin SDK.
    Supports both Streamlit Cloud secrets and local credentials file.
    """
    if not firebase_admin._apps:
        try:
            # Try loading from Streamlit secrets (for production)
            try:
                if hasattr(st, 'secrets') and 'firebase' in st.secrets:
                    cred_dict = dict(st.secrets['firebase'])
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred)
                    print("✅ Firebase initialized from Streamlit secrets")
                    return firestore.client()
            except Exception:
                pass  # Fall through to local file
            
            # Fall back to local credentials file (for development)
            if os.path.exists('config/firebase-credentials.json'):
                cred = credentials.Certificate('config/firebase-credentials.json')
                firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized from local credentials")
                return firestore.client()
            else:
                raise FileNotFoundError(
                    "Firebase credentials not found. "
                    "Please add firebase-credentials.json to config/ directory "
                    "or configure Streamlit secrets."
                )
        except Exception as e:
            st.error(f"❌ Failed to initialize Firebase: {e}")
            return None
    
    return firestore.client()

def get_db():
    """Get Firestore database instance"""
    return firestore.client()
