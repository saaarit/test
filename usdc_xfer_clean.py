import requests
import base64
import json
import datetime
import ecdsa
import hashlib

access_token = ""
private_key_file = "private.pem"
request_json = {
    "signer_type": "api_signer",
    "type": "evm_transaction",
    "details": {
        "type": "evm_transfer",
        "gas": {
            "type": "priority",
            "priority_level": "medium"
        },
        "to": "0x8BFCF9e2764BC84DE4BBd0a0f5AAF19F47027A73", #Dan's vault
        "value": {
            "type": "value",
            "value": "100000"
        },
        "asset_identifier": {
            "type": "evm",
            "details": {
                "type": "erc20",
                "token": {
                    "chain": "evm_base_mainnet",
                    "hex_repr": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  #USDC base contract
                }
            }
        }
    },
    "note": "Transferring USDC",
    "vault_id": "330a2616-f0b3-469d-964c-213e4ecc635e"
}

path = "/api/v1/transactions"
timestamp = datetime.datetime.now().strftime("%s")
request_body = json.dumps(request_json)
payload = f"{path}|{timestamp}|{request_body}"

with open(private_key_file, "r") as f:
    signing_key = ecdsa.SigningKey.from_pem(f.read())
    print("🚀 Starting USDC transfer...")
    
    print("🕓 Timestamp:", timestamp)
    print("📤 Request Body:", json.dumps(request_json, indent=2))

    signature = signing_key.sign(
        data=payload.encode(),
        hashfunc=hashlib.sha256,
        sigencode=ecdsa.util.sigencode_der
    )

    print("🕓 Authorization:", access_token)
    print("🕓 x-signature:", signature)
    print("🕓 x-timestamp:", timestamp)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "x-signature": base64.b64encode(signature).decode("utf-8"),
        "x-timestamp": timestamp,
        #"x-idempotence-id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"
    }

    response = requests.post(
        f"https://api.fordefi.com{path}",
        headers=headers,
        data=request_body
    )

    print("📬 Response Code:", response.status_code)
    try:
        print("📩 Response:", json.dumps(response.json(), indent=2))
    except Exception:
        print("Raw Response:", response.text)
