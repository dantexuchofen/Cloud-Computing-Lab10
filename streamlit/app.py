import pandas as pd
import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

# ---------------------------------
# MONGODB
# ---------------------------------

client = MongoClient(
    "mongodb://mongo:27017/"
)

db = client["demo_db"]

libros = db["libros"]

# ---------------------------------
# UI
# ---------------------------------

st.set_page_config(
    page_title="Biblioteca CRUD",
    layout="wide"
)

st.title("📚 Streamlit + MongoDB")

# =================================
# CREATE
# =================================

st.header("➕ Registrar libro")

with st.form("crear_libro"):

    titulo = st.text_input("Título")

    autor = st.text_input("Autor")

    anio = st.number_input(
        "Año",
        min_value=1900,
        max_value=2100,
        step=1
    )

    disponible = st.checkbox(
        "Disponible"
    )

    submitted = st.form_submit_button(
        "Guardar"
    )

    if submitted:

        libros.insert_one({
            "titulo": titulo,
            "autor": autor,
            "anio": int(anio),
            "disponible": disponible
        })

        st.success("Libro registrado")

st.divider()

# =================================
# READ
# =================================

st.header("📋 Lista de libros")

data = list(
    libros.find()
)

if data:

    for item in data:
        item["_id"] = str(item["_id"])

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.info(
        "No hay libros registrados"
    )

st.divider()

# =================================
# UPDATE
# =================================

st.header("✏️ Actualizar libro")

book_id = st.text_input(
    "ID del libro"
)

nuevo_titulo = st.text_input(
    "Nuevo título"
)

nuevo_autor = st.text_input(
    "Nuevo autor"
)

nuevo_anio = st.number_input(
    "Nuevo año",
    min_value=1900,
    max_value=2100,
    step=1,
    key="nuevo_anio"
)

nuevo_disponible = st.checkbox(
    "Disponible",
    key="nuevo_disponible"
)

if st.button("Actualizar"):

    try:

        libros.update_one(
            {
                "_id": ObjectId(book_id)
            },
            {
                "$set": {
                    "titulo": nuevo_titulo,
                    "autor": nuevo_autor,
                    "anio": int(nuevo_anio),
                    "disponible": nuevo_disponible
                }
            }
        )

        st.success(
            "Libro actualizado"
        )

    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

# =================================
# DELETE
# =================================

st.header("🗑️ Eliminar libro")

delete_id = st.text_input(
    "ID a eliminar",
    key="delete"
)

if st.button("Eliminar"):

    try:

        libros.delete_one({
            "_id": ObjectId(delete_id)
        })

        st.warning(
            "Libro eliminado"
        )

    except Exception as e:
        st.error(f"Error: {e}")