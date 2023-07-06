import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


df = pd.read_csv("autoscout24.csv")

def start():
    st.title("Datenanalyse")


    st.info("In diesem Projekt wurden die Daten von der Webseite 'AutoScout24' analysiert.  \n\nDas Dataset findet man unter folgendem [Link](https://www.kaggle.com/datasets/ander289386/cars-germany).")


    st.header("Wie viele Autos wurden verkauft?  Über welchen Zeitraum?  Welche Marken sind erfasst?")
    auto_count = df.shape[0]
    min_year = df["year"].min()
    max_year = df["year"].max()
    car_brands = ", ".join(df["make"].unique())
    st.write(f"{auto_count} Autos wurden von {min_year} bis {max_year} verkauft.  \n\n**Folgende Automarken wurden verkauft:**  \n{car_brands}")


    st.header("Existieren Korrelationen zwischen den (numerischen) Features?")
    fig = plt.figure()
    numeric_df = df.select_dtypes(include=[np.number])
    correlation_matrix = numeric_df.corr()
    sns.heatmap(correlation_matrix, annot=True)
    st.pyplot(fig)


    st.success("Der Preis korreliert sehr stark mit PS und Kilometerstand korreliert ziemlich stark mit dem Registrierungsjahr, was auch logisch ist: je länger ein Auto registriert ist, desto mehr ist es gefahren.")


    st.header("Gibt es Veränderungen über die Jahre?")
    all_mean_prices = []
    for year in range(2011, 2022):
        new_df = df[df["year"] == year]
        price_mean = new_df["price"].mean().round(2)
        all_mean_prices.append(price_mean)

    fig, ax = plt.subplots()
    ax.plot(range(2011, 2022), all_mean_prices, ".r-")
    ax.set_title("Veränderung der Durchschnittspreise")
    ax.set_xlabel("Jahr")
    ax.set_ylabel("Durchschnittspreis")

    for year, price in zip(range(2011, 2022), all_mean_prices):
        ax.text(year-0.2, price, str(price)+"€", ha="right", va="center")

    st.pyplot(fig)


    st.header("Wie korreliert der Preis mit dem Jahr der Registrierung für verschiedene Marken?")
    st.write("Es gibt viel zu viele Marken, deswegen plotten wir nur die, die mehr als 1000 Mal verkauft wurden.")
    all_brands = df["make"].unique()
    all_brands_more_1000 = []
    for brand in all_brands:
        brand_count = df[df["make"] == brand].shape[0]
        if brand_count > 1000:
            all_brands_more_1000.append(brand)

    all_mean_prices_for_brands = {} 
    for brand in all_brands_more_1000:
        new_df = df[df["make"] == brand]
        all_prices = []
        for year in range(2011, 2022):
            new_df_year = new_df[new_df["year"] == year]
            price_mean = new_df_year["price"].mean()
            if price_mean is not None:
                price_mean = round(price_mean, 2)
            all_prices.append(price_mean)
            
        all_mean_prices_for_brands[brand] = all_prices

    fig, ax = plt.subplots()
    colors = ['#014526', '#6a479b', '#3c8f7e', '#a6b541', '#c12589', '#00a8e8', '#e61b64', '#ffa602', '#b76e79', '#ff488e', '#891b14', '#4f5d6e', '#82532b', '#27747b']
    for i, (key, value) in enumerate(all_mean_prices_for_brands.items()):
        ax.plot(range(2011, 2022), value, color=colors[i], marker='o', label=key)

    ax.set_title("Durchschnittspreise der Marken nach Registrierungsjahren")
    ax.set_xlabel("Jahr")
    ax.set_ylabel("Durchschnittspreis")
    ax.legend()
    st.pyplot(fig)


    st.header("Wie korreliert der Preis mit dem Kilometerstand für verschiedene Marken?")
    all_mean_prices_for_brands_and_mil = {} 
    for brand in all_brands_more_1000:
        new_df = df[df["make"] == brand]
        all_prices = []
        for mileage in range(0, 300000, 1000):
            new_df_mil = new_df[new_df["mileage"] >= mileage]
            price_mean = new_df_mil["price"].mean()
            if price_mean is not None:
                price_mean = round(price_mean, 2)
            all_prices.append(price_mean)
            
        all_mean_prices_for_brands_and_mil[brand] = all_prices

    fig, ax = plt.subplots()
    for i, (key, value) in enumerate(all_mean_prices_for_brands_and_mil.items()):
        ax.plot(range(0, 300000, 1000), value, color=colors[i], marker='.', label=key)

    ax.set_title("Durchschnittspreise der Marken nach Kilometerzahl")
    ax.set_xlabel("Kilometerzahl")
    ax.set_ylabel("Durchschnittspreis")
    ax.legend()
    st.pyplot(fig)
