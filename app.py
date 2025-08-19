import feedparser
from transformers import pipeline
import streamlit as st
import yfinance as yf



# Streamlit UI
st.title("📈 StockLens AI")
st.write("Enter a stock ticker and keyword to filter financial news articles and analyze their sentiment.")

# Inputs from user
ticker = st.text_input("Enter stock ticker symbol (e.g., AAPL)", value="AAPL")
keyword = st.text_input("Enter keyword to filter news articles (No need if you are analyzing earnings)", value="")
max_articles = st.number_input("How many articles should be displayed? (min 1 - max 10)(No need if you are analyzing earnings)", min_value=1, max_value=10, value=5)


# Load model
@st.cache_resource
def load_model():
    return pipeline("text-classification", model="ProsusAI/finbert")

pipe = load_model()



if st.button("Analyze News"):
    rss_url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
    feed = feedparser.parse(rss_url)

    total = 0
    num = 0
    results = []

    for entry in feed.entries:
        if keyword.lower() not in entry.title.lower():
            continue

        sentiment = pipe(entry.summary)[0]

        if sentiment['label'] == 'positive':
            total += sentiment['score']
            num += 1
        elif sentiment['label'] == 'negative':
            total -= sentiment['score']
            num += 1

        results.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "sentiment": sentiment['label'],
            "score": sentiment['score']
        })

    average_score = total / num if num > 0 else 0

    # Filter high-confidence articles
    st.subheader("📰 Filtered Articles ")
    displayed = 0
    for r in results:
        if r["score"] >= 0.70:
            st.markdown(f"### [{r['title']}]({r['link']})")
            st.write(r["summary"])
            st.write(f"**Sentiment:** {r['sentiment']} | **Score:** {r['score']:.4f}")
            st.markdown("---")
            displayed += 1
            if displayed >= max_articles:
                break



if st.button("Past EPS Scores and Estimates (Earning per share)", key="eps_button_1"):
    ticker_data = yf.Ticker(ticker)
    earnings = ticker_data.earnings_history

    if earnings is not None and not earnings.empty:
        st.subheader("📅 Earnings History")
        st.dataframe(earnings)
    else:
        st.write("No earnings history data available for this ticker.", key="qtr_income_btn_1")

if st.button("Show Quarterly Income Statement"):
        ticker_data1 = yf.Ticker(ticker)
        income_statement = ticker_data1.quarterly_income_stmt
        if income_statement is not None and not income_statement.empty:
            st.subheader("💰 Quarterly Income Statement")
            st.dataframe(income_statement.applymap(lambda x: f"${x:,.0f}"))
        else:
            st.write("No quarterly income statement data available for this ticker.")

if st.button("Quarterly Balance sheet"):
    ticker_data2 = yf.Ticker(ticker)
    balance = ticker_data2.quarterly_balancesheet
    st.subheader("🏦 Balance Sheet")
    st.dataframe(balance.applymap(lambda x: f"${x:,.0f}"))
    if balance is None or balance.empty:
        st.write("No balance sheet data available for this ticker.")



st.title("📈 Simple Stock Chart Viewer")

# User input for ticker
options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]

if ticker:
    # Download historical data
    stock = yf.Ticker(ticker)
    timestamps = st.selectbox("Select Time Period for Chart:", options, index=5)  
    hist = stock.history(period=timestamps)  # last 1 year of data

    if not hist.empty:
        # Show stock info
        st.subheader(f"{ticker.upper()} - Company Info")
        st.write(stock.info.get("longName", "No company name found"))
        st.write(f"Sector: {stock.info.get('sector', 'N/A')}")
        st.write(f"Industry: {stock.info.get('industry', 'N/A')}")

        # Show chart
        st.subheader("Stock Price Chart")
        st.line_chart(hist["Close"])

        # Show data table
        st.subheader("Historical Data")
        st.dataframe(hist)

    else:
        st.error("No data found for this ticker.")
