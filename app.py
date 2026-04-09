import io
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Data Transformer",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded",
)

IDENTITY_COLUMNS = ["PartNumber", "CompanyName"]
CONCAT_SOURCE_COLUMNS = [
    "ZFeatureName",
    "Value",
    "ApprovalStatus",
    "IsBackup",
    "CorrectValue",
    "SourceURL",
    "Comment",
    "Note",
]
REVERSE_OUTPUT_COLUMNS = [
    "PartNumber",
    "CompanyName",
    "ZFeatureName",
    "Value",
    "ApprovalStatus",
    "IsBackup",
    "CorrectValue",
    "SourceURL",
    "Comment",
    "Note",
]


def _to_excel_bytes(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return buffer.getvalue()


def concatenate_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = [col for col in IDENTITY_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    available_source_cols = [col for col in CONCAT_SOURCE_COLUMNS if col in df.columns]
    if not available_source_cols:
        raise ValueError(
            "No feature columns found. Expected one or more of: "
            f"{', '.join(CONCAT_SOURCE_COLUMNS)}"
        )

    transformed_rows = []
    grouped = df.groupby(IDENTITY_COLUMNS, dropna=False, sort=False)

    for (part_number, company_name), group in grouped:
        row_data = {
            "PartNumber": part_number,
            "CompanyName": company_name,
        }

        for idx, (_, source_row) in enumerate(group.iterrows(), start=1):
            feature_values = []
            for source_col in available_source_cols:
                value = source_row.get(source_col, "")
                if pd.isna(value) or str(value).strip() == "":
                    continue
                feature_values.append(str(value).strip())

            row_data[f"Feature{idx}"] = " | ".join(feature_values)

        transformed_rows.append(row_data)

    if not transformed_rows:
        return pd.DataFrame(columns=IDENTITY_COLUMNS)

    transformed_df = pd.DataFrame(transformed_rows)

    max_features = max(max(len(row) - len(IDENTITY_COLUMNS), 0) for row in transformed_rows)
    for idx in range(1, max_features + 1):
        feature_col = f"Feature{idx}"
        if feature_col not in transformed_df.columns:
            transformed_df[feature_col] = ""

    ordered_columns = IDENTITY_COLUMNS + [f"Feature{idx}" for idx in range(1, max_features + 1)]
    return transformed_df[ordered_columns]


def reverse_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = [col for col in IDENTITY_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    feature_columns = [col for col in df.columns if col not in IDENTITY_COLUMNS]
    if not feature_columns:
        raise ValueError("No Feature columns found to reverse.")

    reversed_rows = []

    for _, row in df.iterrows():
        for feature_col in feature_columns:
            feature_value = row.get(feature_col, "")
            if pd.isna(feature_value) or str(feature_value).strip() == "":
                continue

            parts = [part.strip() for part in str(feature_value).split("|")]

            reversed_row = {
                "PartNumber": row["PartNumber"],
                "CompanyName": row["CompanyName"],
            }

            for idx, out_col in enumerate(REVERSE_OUTPUT_COLUMNS[2:]):
                reversed_row[out_col] = parts[idx] if idx < len(parts) and parts[idx] else None

            reversed_rows.append(reversed_row)

    return pd.DataFrame(reversed_rows, columns=REVERSE_OUTPUT_COLUMNS)


def render_concat_tool() -> None:
    st.subheader("📊 Concatenate Data")
    with st.expander("Tool info", expanded=False):
        st.write("Upload an Excel file and transform grouped rows into Feature columns.")
        st.markdown(
            """
            - Groups by PartNumber + CompanyName
            - Concatenates with `|` delimiter
            - Skips blank cells
            - Preserves explicit `N/A` text
            """
        )

    uploaded_file = st.file_uploader(
        "Upload input Excel file",
        type=["xlsx", "xls"],
        key="concat_file",
    )

    if uploaded_file is None:
        st.caption("Upload a file to start concatenation.")
        return

    try:
        input_df = pd.read_excel(uploaded_file, keep_default_na=False, na_values=[""])
    except Exception as exc:
        st.error(f"Could not read file: {exc}")
        return

    st.write(f"Loaded {len(input_df)} rows and {len(input_df.columns)} columns.")

    if all(col in input_df.columns for col in IDENTITY_COLUMNS):
        unique_groups = input_df.groupby(IDENTITY_COLUMNS, dropna=False).ngroups
        st.metric("Unique PartNumber + CompanyName groups", unique_groups)

    with st.expander("Input preview", expanded=False):
        st.dataframe(input_df.head(10), use_container_width=True)

    if st.button("Run Concatenation", key="run_concat", use_container_width=True, type="primary"):
        try:
            with st.spinner("Transforming data..."):
                output_df = concatenate_data(input_df)

            st.session_state.concat_result = output_df
            output_name = f"concatenated_{Path(uploaded_file.name).stem}_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
            st.session_state.concat_result_name = output_name
            st.success(f"Transformation complete. Output rows: {len(output_df)}")
        except Exception as exc:
            st.error(f"Concatenation failed: {exc}")

    if st.session_state.get("concat_result") is not None:
        result_df = st.session_state.concat_result
        file_name = st.session_state.get("concat_result_name", "concatenated_output.xlsx")
        st.download_button(
            label="Download concatenated file",
            data=_to_excel_bytes(result_df),
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
        with st.expander("Output preview", expanded=False):
            st.dataframe(result_df.head(10), use_container_width=True)


def render_reverse_tool() -> None:
    st.subheader("↩️ Reverse Transformation")
    with st.expander("Tool info", expanded=False):
        st.write("Split Feature columns back into the original row-based structure.")
        st.markdown(
            """
            - Splits feature values using `|`
            - Restores original feature columns
            - Creates multiple rows per group when needed
            - Preserves data integrity
            """
        )

    uploaded_file = st.file_uploader(
        "Upload concatenated Excel file",
        type=["xlsx", "xls"],
        key="reverse_file",
    )

    if uploaded_file is None:
        st.caption("Upload a concatenated file to start reverse transformation.")
        return

    try:
        input_df = pd.read_excel(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read file: {exc}")
        return

    st.write(f"Loaded {len(input_df)} rows and {len(input_df.columns)} columns.")

    with st.expander("Input preview", expanded=False):
        st.dataframe(input_df.head(10), use_container_width=True)

    if st.button("Run Reverse", key="run_reverse", use_container_width=True, type="primary"):
        try:
            with st.spinner("Reversing transformation..."):
                output_df = reverse_data(input_df)

            st.session_state.reverse_result = output_df
            output_name = f"reversed_{Path(uploaded_file.name).stem}_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
            st.session_state.reverse_result_name = output_name
            st.success(f"Reverse transformation complete. Output rows: {len(output_df)}")
        except Exception as exc:
            st.error(f"Reverse transformation failed: {exc}")

    if st.session_state.get("reverse_result") is not None:
        result_df = st.session_state.reverse_result
        file_name = st.session_state.get("reverse_result_name", "reversed_output.xlsx")
        st.download_button(
            label="Download reversed file",
            data=_to_excel_bytes(result_df),
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
        with st.expander("Output preview", expanded=False):
            st.dataframe(result_df.head(10), use_container_width=True)


st.markdown(
    """
<style>
    .block-container {
        padding-top: 0.9rem;
    }
    .main-header {
        font-size: 1.75rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.1rem;
        color: var(--text-color) !important;
    }
    .sub-header {
        font-size: 0.88rem;
        text-align: center;
        margin-bottom: 0.4rem;
        color: var(--text-color) !important;
        opacity: 0.7;
    }
    div[data-testid="stTabs"] {
        margin-top: 0.25rem;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        font-weight: 700;
        border-radius: 10px 10px 0 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        padding: 0.7rem;
        font-weight: 700;
    }
</style>
""",
    unsafe_allow_html=True,
)

if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "Concatenate Data"

st.markdown(
    "<h1 class='main-header'>Data Transformer</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='sub-header'>Concatenate or reverse your Excel data.</p>",
    unsafe_allow_html=True,
)

st.markdown("---")
tab_concat, tab_reverse = st.tabs(["📊 Concatenate", "↩️ Reverse"])

with tab_concat:
    render_concat_tool()

with tab_reverse:
    render_reverse_tool()

st.markdown("---")
st.markdown(
    "<p style='text-align: center; opacity: 0.75;'>Built with Streamlit • Data processing tool</p>",
    unsafe_allow_html=True,
)
