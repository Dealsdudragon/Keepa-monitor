
import streamlit as st
import requests
import datetime

API_KEY = "3alpvklfibkh1f9qkdsvkiargusk4d9n8odr4h92itg30i512s9chgmngvokv882"
DOMAIN = 3  # 3 = Amazon.ca

def get_product_data(asin):
    url = f"https://api.keepa.com/product?key={API_KEY}&domain={DOMAIN}&asin={asin}&buybox=1&history=1"
    r = requests.get(url)
    return r.json()

def extract_price_data(product):
    title = product['title']
    img = "https://images-na.ssl-images-amazon.com/images/I/" + product['imagesCSV'].split(',')[0]
    amazon_prices = product['data']['amazon']
    valid_prices = [p for p in amazon_prices if p > 0]
    current_price = amazon_prices[-1] / 100 if amazon_prices[-1] > 0 else None
    lowest_price = min(valid_prices) / 100 if valid_prices else None
    reduction = None
    if current_price and lowest_price and current_price < lowest_price:
        reduction = 100 - (current_price / lowest_price * 100)
    return title, img, current_price, lowest_price, reduction

st.title("Keepa Monitor - Amazon CA")
st.write("Entrez un ASIN Amazon pour voir son historique de prix :")

asin_input = st.text_input("ASIN", "B08N5WRWNW")

if asin_input:
    result = get_product_data(asin_input)
    if "products" in result and len(result["products"]) > 0:
        product = result["products"][0]
        title, img, current_price, lowest_price, reduction = extract_price_data(product)

        st.image(img, width=300)
        st.subheader(title)
        if current_price:
            st.markdown(f"**Prix actuel :** {current_price:.2f} $ CAD")
        if lowest_price:
            st.markdown(f"**Prix le plus bas (historique) :** {lowest_price:.2f} $ CAD")
        if reduction:
            st.markdown(f"**Réduction historique :** {reduction:.1f}%")
        st.markdown(f"[Lien Amazon](https://www.amazon.ca/dp/{asin_input}/?tag=tonid-20)")
    else:
        st.error("Produit introuvable.")
