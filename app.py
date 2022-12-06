import joblib

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
import Levenshtein
import pandas as pd

train_df = pd.read_csv('train.csv', index_col=0)
test_df = pd.read_csv('test.csv', index_col=0)
model = joblib.load('model.joblib')

permutations = list()
for col in train_df:
    if not '_' in col and col.isupper() and 0 < len(col) < 4:
        permutations.append(col)
BASE = 'VPVNPEPDATSVENVALKTGSGDSQSDPIKADLEVKGQSALPFDVDCWAILCKGAPNVLQRVNEKTKNSNRDRSGANKGPFKDPQKWGIKALPPKNPSWSAQDFKSPEEYAFASSLQGGTNAILAPVNLASQNSQGGVLNGFYSANKVAQFDPSKPQQTKGTWFQITKFTGAAGPYCKALGSNDKSVCDKNKNIAGDWGFDPAKWAYQYDEKNNKFNYVGK'
terminology_map = {"replace":"substitution", "insert":"insertion", "delete":"deletion"}


st.set_page_config(layout="centered", page_icon="🧬", page_title="Enzyme Thermal Stability")
st.title("Enzyme Thermal Stability Prediction")

st.write(
    "Predict properties of protein sequences based on component amino acids"
)

left, right = st.columns(2)

right.write("")

right.image("img.png", width=300)

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
# template = env.get_template("template.html")


left.write("Input data for prediction:")
form = left.form("template_form")
# custom = form.text_input("Input Custom Sequence")
select = form.selectbox(
    "Choose mutation",
    test_df['protein_sequence'].tolist(),
    index=0,
)
pH = form.slider("pH", 0, 30, 7)
submit = form.form_submit_button("Generate Prediction")

if submit:
    relevant_line = test_df.loc[test_df['protein_sequence'] == select,:]
    relevant_line['pH'] = pH
    relevant_line = relevant_line.drop(columns=[col for col in relevant_line if relevant_line[col].dtype not in ['int64','float64']])
    relevant_line = relevant_line.drop(columns=['sub_score'])
    pred = model.predict(relevant_line)
    # pred_df['tm'] = pred


    right.success(f"Prediction Completed: Tm = {pred}")

    # right.download_button(
    #     pred_df,
    #     "⬇️ Download CSV",
    #     'text/csv',
    # )
    # right.download_button(
    #     "⬇️ Download CSV",
    #     csv,
    #     'text/csv',
    # )