def capitalize_column(df):
    df.columns = [cols.replace("_" , " ").title() for cols in df.columns]