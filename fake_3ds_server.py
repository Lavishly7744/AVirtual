from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

def generate_3ds_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=36))

@app.route("/3ds-authenticate", methods=["POST"])
def authenticate_3ds():
    data = request.get_json()

    # Simulate a successful 3DS authentication
    response = {
        "threeDSServerTransID": generate_3ds_transaction_id(),
        "transStatus": "Y",  # Y = Authentication/Account Verified
        "eci": "05",  # 05 = Frictionless flow completed successfully
        "authenticationValue": ''.join(random.choices('ABCDEF0123456789', k=28)),
        "messageVersion": "2.1.0",
        "dsTransID": generate_3ds_transaction_id()
    }

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5700)
