from decouple import config
import requests
import json


def make_paypal_payment(amount, currency, return_url, cancel_url):
    # Set up PayPal API credentials
    client_id = config("PAYPAL_ID")
    secret = config("PAYPAL_SECRET")
    url = config("PAYPAL_BASE_URL")
    # Set up API endpoints
    base_url = url
    token_url = base_url + "/v1/oauth2/token"
    payment_url = base_url + "/v1/payments/payment"

    # Request an access token
    token_payload = {"grant_type": "client_credentials"}
    token_headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    token_response = requests.post(
        token_url, auth=(client_id, secret), data=token_payload, headers=token_headers
    )

    if token_response.status_code != 200:
        # Log the error for debugging
        print(
            f"PayPal API authentication failed: {token_response.status_code} - {token_response.text}"
        )
        return False, "Failed to authenticate with PayPal API", None

    try:
        access_token = token_response.json()["access_token"]
    except KeyError:
        print(
            f"Failed to get access token from PayPal API response: {token_response.text}"
        )
        return False, "Failed to get access token", None

    # Create payment payload
    payment_payload = {
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [
            {
                "amount": {"total": str(amount), "currency": currency},
                "description": "Donación para Chambalabamba",  # Updated description
            }
        ],
        "redirect_urls": {"return_url": return_url, "cancel_url": cancel_url},
    }

    # Create payment request
    payment_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    payment_response = requests.post(
        payment_url, data=json.dumps(payment_payload), headers=payment_headers
    )
    print(
        f"PayPal payment creation response: {payment_response.text}"
    )  # Log the full response

    if payment_response.status_code != 201:
        print(
            f"Failed to create PayPal payment: {payment_response.status_code} - {payment_response.text}"
        )
        return False, "Failed to create PayPal payment.", None

    try:
        payment_id = payment_response.json()["id"]
        approval_url = next(
            link["href"]
            for link in payment_response.json()["links"]
            if link["rel"] == "approval_url"
        )
    except (KeyError, StopIteration):
        print(
            f"Failed to extract approval URL from PayPal payment response: {payment_response.text}"
        )
        return False, "Failed to get approval URL", None

    return True, payment_id, approval_url
