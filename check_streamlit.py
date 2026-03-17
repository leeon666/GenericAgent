import streamlit as st
print(f"Streamlit version: {st.__version__}")
print(f"Has fragment attribute: {hasattr(st, 'fragment')}")
