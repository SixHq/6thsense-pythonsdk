import base64
from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

# We take the token from the command line
import sys
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJhdXRoLmdldGJyYXNzLmNvIiwiZXhwIjoxNjkxMjExNjU2LCJpYXQiOjE2OTEyMDgwNTYsIm5iZiI6MTY5MTIwODA1NiwiYXBpX2NsaWVudCI6ImFwcF8xVk45eFhJUFpIVXN5MVdGVmQwRnU2IiwiY3VzdG9tZXIiOiJjdXNfNzd1d0hRd0UyeEdWS1QwVTZibHRLWSIsInVzZXIiOiJ1c3Jfd2dvUlZJcnpablNiWDk0ZU5WWkhlIiwiaXNfdGVtcG9yYXJ5Ijp0cnVlLCJwYXlyb2xsX2N1c3RvbWVyX3Byb2ZpbGUiOm51bGx9.sUNU0TshcypQvAnljep12ima20hxN21dTtWFrXPDGbICBoT_oLOGwFlqR8pRd_cjoYlXFyOMSvmU1KXqi9-dqgsCVGPZBoWn_budjEhgKZd-mRtXjX-TRzPVdHbuoQcB7_pdAZZV7FbnNXus7-QDFQctea2eL52Nfg7yEY_FOzw"

# We split the token to get the data to digest and the signature
parts = token.split('.')
data = f"{parts[0]}.{parts[1]}".encode('utf-8')
signature_b64 = parts[2]

# We compute the digest
digest = sha256(data).digest()

# We create an ECDSA signature from the JWT signature
signature_bytes = base64.urlsafe_b64decode(signature_b64 + "==")

# Recover the public key
backend = default_backend()
public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), signature_bytes)

# Get the public key in PEM format
pem_key = public_key.public_bytes(
    encoding=ec.EllipticCurvePublicNumbers.Format.PEM,
    format=ec.EllipticCurvePublicNumbers.PublicFormat.SubjectPublicKeyInfo
)
