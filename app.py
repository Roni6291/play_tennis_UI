import requests
import streamlit as st

st.title("# Tennis Playability")
st.write(
    """
    *Can we play tennis on the below weather conditions*

    ## Please choose the appropriate weather conditions from below
    """
)

st.subheader("OUTLOOK")
outlook = st.selectbox(
    "Select Outlook",
    ("overcast", "rain", "sunny"),
    index=None,
    placeholder="Choose an option",
)
st.write("You selected:", outlook)

st.subheader("TEMPERATURE")
temp = st.selectbox(
    "Select Temperatue",
    ("cool", "hot", "mild"),
    index=None,
    placeholder="Choose an option",
)
st.write("You selected:", temp)

st.subheader("HUMIDITY")
humid = st.selectbox(
    "Select Humidity",
    ("high", "normal"),
    index=None,
    placeholder="Choose an option",
)
st.write("You selected:", humid)

st.subheader("WIND")
wind = st.selectbox(
    "Select Wind",
    ("strong", "weak"),
    index=None,
    placeholder="Choose an option",
)
st.write("You selected:", wind)


if st.button("Check Playability"):
    try:
        assert all(
            [
                True if cond else False
                for cond in (
                    outlook,
                    temp,
                    humid,
                    wind,
                )
            ]
        ), "All weather conditions should be selected a value"
        # send the request
        uri = "http://127.0.0.1:8000/infer/live/0.1.0"
        payload = {
            "outlook": outlook,
            "temperature": temp,
            "humidity": humid,
            "wind": wind,
        }
        resp = requests.post(url=uri, data=payload)
        if resp.status_code == 200:
            st.success(resp.json()["description"])
        else:
            st.error(f"Returned with {resp.status_code} error: {resp.content}")
    except AssertionError as err:
        st.error(str(err))
    except requests.exceptions.RequestException as err:
        st.error(str(err))
