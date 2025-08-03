import pandas as pd

def rename_columns(df):
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df = df.rename(columns={'st':'state'})
    return df

def clean_education(df):
    df['education'] = df['education'].replace('Bachelors', 'Bachelor')
    return df

def clean_gender(df):
    gender_map = {
        "F": "F", "Femal": "F", "Female": "F", "female": "F",
        "M": "M", "Male": "M", "male": "M"
    }
    df["gender"] = df["gender"].map(gender_map)
    return df

def clean_state(df):
    state_map = {"AZ": "Arizona", "Cali": "California", "WA": "Washington"}
    df["state"] = df["state"].replace(state_map)
    return df

def clean_customer_lifetime_value(df):
    def remove_percentage(x):
        if isinstance(x, str) and '%' in x:
            return x.replace('%', '')
        return x

    df["customer_lifetime_value"] = df["customer_lifetime_value"].apply(remove_percentage)
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')
    return df

def clean_number_of_open_complaints(df):
    def extract_middle_number(x):
        if isinstance(x,str):
            parts = x.split('/')
            if len(parts) == 3:
                return parts[1]
            else:
                return x
        return x
    df['number_of_open_complaints'] =df['number_of_open_complaints'].apply(extract_middle_number)
    df['number_of_open_complaints'] =pd.to_numeric(df['number_of_open_complaints'], errors='coerce')
    return df

def clean_null_values(df):
    df =df.dropna(axis=0, how='all')
    df = df.dropna(subset=['customer_lifetime_value'])
    filing_value = df['gender'].mode()[0]
    df['gender'] = df['gender'].fillna(filing_value)
    return df

def remove_duplates(df):
    df = df.drop_duplicates(subset=['customer'], keep='first').reset_index(drop=True)
    return df

def clean_data(df):
    df = rename_columns(df)
    df = clean_gender(df)
    df = clean_customer_lifetime_value(df)
    df = clean_education(df)
    df = clean_number_of_open_complaints(df)
    df = clean_state(df)
    df = clean_null_values(df)
    df = remove_duplates(df)
    return df


