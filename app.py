from collections.abc import Iterable
import os

from dotenv import load_dotenv
import httpx
import streamlit as st


def generate_dropdowns(
    dropdown_header: str,
    choices: Iterable[str],
):
    st.subheader(dropdown_header)
    return st.selectbox(
        f'Select {dropdown_header.lower().title()}',
        choices,
        index=None,
        placeholder='Choose an option',
    )


def generate_payload(
    weather_conditions: dict[str, Iterable[str]],
    conditions: list[str],
) -> dict[str, str]:
    return {
        w.lower(): c
        for w, c in zip(
            weather_conditions.keys(),
            conditions,
        )
    }


def fetch_live_prediction(
    uri: str,
    data: dict[str, str],
    headers: dict[str, str],
) -> httpx.Response:
    return httpx.post(url=uri, json=data, headers=headers)


if __name__ == '__main__':
    load_dotenv()

    model_version = os.environ.get('MDL_VERSION')
    app_port = os.environ.get('APPPORT')
    app_host = os.environ.get('APPHOST')

    st.title('Tennis Playability')
    st.write(
        """
        *Is it possible to play tennis during the below weather conditions*
        ## Please choose the appropriate weather conditions from below
        """
    )

    weather_conditions = {
        'OUTLOOK': ('overcast', 'rain', 'sunny'),
        'TEMPERATURE': ('cool', 'hot', 'mild'),
        'HUMIDITY': ('high', 'normal'),
        'WIND': ('strong', 'weak'),
    }

    conditions = []
    for condition, options in weather_conditions.items():
        w_cond = generate_dropdowns(dropdown_header=condition, choices=options)
        st.write('You selected:', w_cond)
        conditions.append(w_cond)

    if st.button('Validate'):
        try:
            assert all(
                bool(cond) for cond in conditions
            ), 'All weather conditions should be selected a value'
            st.success('Options Selected:')
            st.table(data=generate_payload(weather_conditions, conditions))
        except AssertionError as err:
            st.error(str(err))

    if st.button('Check Playability'):
        try:
            assert all(
                bool(cond) for cond in conditions
            ), 'All weather conditions should be selected a value'
            # send the request
            uri = f'http://{app_host}:{app_port}/infer/live/{model_version}'
            payload = generate_payload(weather_conditions, conditions)
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            }
            resp = fetch_live_prediction(
                uri=uri,
                data=payload,
                headers=headers,
            )
            if resp.status_code == 200:
                st.success(resp.json()['description'])
                if resp.json()['can_play']:
                    st.balloons()
            else:
                msg = resp.json()['detail'][0]['msg']
                st.error(f'Returned with {resp.status_code} error: {msg}')
        except AssertionError as err:
            st.error(str(err))
        except httpx.HTTPError as err:
            st.error(str(err))
