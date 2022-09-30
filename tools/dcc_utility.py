import requests, json, os, shutil
from base64 import b64decode, b64encode
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime
from tools.config import config
from asn1crypto.cms import ContentInfo
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

def decode_rawData(rawData):
    if rawData != None:
        cert = x509.load_der_x509_certificate(b64decode(rawData))
        return cert 
    else:
        return None

def delete_certificate(kid):
    location = config()['Main_Location']
    folder = f"{location}/dsc/{kid}"
    cert = x509.load_pem_x509_certificate(open(f"{folder}/dsc.crt", 'rb').read())
    sign_cert = x509.load_pem_x509_certificate(
        open(f"{location}/cert/upload.pem", "rb").read())
    sign_key = serialization.load_pem_private_key(
        open(f"{location}/cert/key_upload.pem", "rb").read(), None)
    data = cert.public_bytes(serialization.Encoding.DER)
    options = [serialization.pkcs7.PKCS7Options.Binary]
    builder = serialization.pkcs7.PKCS7SignatureBuilder().set_data(data)
    signed = builder.add_signer(sign_cert, sign_key, hash_algorithm=hashes.SHA256()).sign(
        encoding=serialization.Encoding.DER, options=options)

    cms = b64encode(signed)
    authCert = f"{location}/cert/auth.pem"
    authKey = f"{location}/cert/key_auth.pem"
    headers = {'Content-Type': 'application/cms',
               'Content-Transfer-Encoding': 'base64'}
    response = requests.delete(
        f"{config()['Gateway_Url']}/signerCertificate", data=cms, headers=headers, cert=(authCert, authKey))
    print(response.status_code)
    print(response.text)
    shutil.rmtree(folder)

def create_certificate(timestamp, expiryDate):
    print(timestamp, expiryDate)
    timestamp = datetime.combine(timestamp, datetime.now().time())
    expiryDate = datetime.combine(expiryDate, datetime.now().time())
    location = config()['Main_Location']
    country = config()['Country_Name']
    csca_cert = x509.load_pem_x509_certificate(
        open(f"{location}/cert/csca.pem", "rb").read())
    csca_key = serialization.load_pem_private_key(
        open(f"{location}/cert/key_csca.pem", "rb").read(), None)
    key = ec.generate_private_key(ec.SECP256R1())
    issuer = csca_cert.issuer
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME,
                           u"T-Systems International"),
        x509.NameAttribute(NameOID.COMMON_NAME,
                           u"CWA Test Team"),
    ])
    certBuilder = x509.CertificateBuilder()
    certBuilder = certBuilder.subject_name(subject)
    certBuilder = certBuilder.issuer_name(issuer)
    certBuilder = certBuilder.public_key(key.public_key())
    certBuilder = certBuilder.serial_number(x509.random_serial_number())
    certBuilder = certBuilder.not_valid_before(timestamp)
    certBuilder = certBuilder.not_valid_after(expiryDate)
    cert = certBuilder.sign(csca_key, hashes.SHA256())

    fingerprint = cert.fingerprint(hashes.SHA256())
    kid = b64encode(fingerprint[:8]).decode('utf-8')
    folder = f"{location}/dsc/{kid}"
    if not os.path.exists(folder):
        os.mkdir(folder)
        print(kid)
        print('Writing dsc.crt')
        with open(f"{folder}/dsc.crt", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        print('Writing dsc.key')
        with open(f"{folder}/dsc.key", "wb") as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),))
    else:
        print("Certificate already exists.")
        return None
    upload_certificate(kid)

def upload_certificate(kid):
    location = config()['Main_Location']
    cert = x509.load_pem_x509_certificate(open(f"{location}/dsc/{kid}/dsc.crt", "rb").read())
    sign_cert = x509.load_pem_x509_certificate(
        open(f"{location}/cert/upload.pem", "rb").read())
    sign_key = serialization.load_pem_private_key(
        open(f"{location}/cert/key_upload.pem", "rb").read(), None)
    options = [serialization.pkcs7.PKCS7Options.Binary]
    data = cert.public_bytes(serialization.Encoding.DER)
    builder = serialization.pkcs7.PKCS7SignatureBuilder().set_data(data)
    signed = builder.add_signer(sign_cert, sign_key, hash_algorithm=hashes.SHA256()).sign(
        encoding=serialization.Encoding.DER, options=options)

    cms = b64encode(signed)
    authCert = f"{location}/cert/auth.pem"
    authKey = f"{location}/cert/key_auth.pem"
    headers = {'Content-Type': 'application/cms',
               'Content-Transfer-Encoding': 'base64'}
    response = requests.post(url=f"{config()['Gateway_Url']}/signerCertificate", data=cms, headers=headers, cert=(authCert, authKey))
    print(response.status_code, response.text)

def download_trustlist():
    response = requests.get(url = 
        f"{config()['Gateway_Url']}/trustList", 
        cert=(config()['Auth_Cert'], config()['Auth_Key']),
        headers={"If-Modified-Since":config()['Last_Updated_Tl']})
    return response

def download_countrylist():
    response = requests.get(url = 
        f"{config()['Gateway_Url']}/countrylist", 
        cert=(config()['Auth_Cert'], config()['Auth_Key']))
    return response.json()

def download_revocationlist():
    response = requests.get(url = 
        f"{config()['Gateway_Url']}/revocation-list", 
        cert=(config()['Auth_Cert'], config()['Auth_Key']),
        headers={"If-Modified-Since":config()['Last_Updated_Rl']})
    config_data = config()
    config_data['Last_Updated_Rl'] = datetime.now().replace(microsecond=0).isoformat()+"+02:00"
    with open (f"{config()['Main_Location']}/config.json", "w") as c:
        json.dump(config_data, c, indent = 4)
        c.close()
    return response

def compare_dateTime(dt):
    days_date1 = datetime.strptime(dt, "%Y-%m-%d")
    days_date2 = datetime.strptime(str(datetime.now().isoformat()).split("T")[0], "%Y-%m-%d")
    return (days_date1 - days_date2).days

def update_validationRules():
    print("Updating ValidationRules.")
    response = requests.get(url = 
    f"{config()['Gateway_Url']}/rules/{config()['Country_Name']}", 
    cert=(config()['Auth_Cert'], config()['Auth_Key']))
    with open (f"{config()['Main_Location']}/data/validationRules.json", "w") as c:
        json.dump(response.json(), c, indent = 4)
        c.close()

def open_validationRules():
    with open (f"{config()['Main_Location']}/data/validationRules.json", "r") as c:
        data = json.load(c)
        c.close()
        return data

def decode_cms(rule):
    cms = b64decode(rule['cms'])
    signedData = ContentInfo.load(cms)
    rule = signedData['content']['encap_content_info']['content'].native
    ruleJson = json.loads(rule.decode('utf-8'))
    return ruleJson

#def update_revocationList():
#    response = requests.get(url = 
#    f"{config()['Gateway_Url']}/revocation-list", 
#    cert=(config()['Auth_Cert'], config()['Auth_Key']),
#    headers={"If-Modified-Since":config()['Last_Updated_Rl']})
#    if response.text:
#        print("Updating RevocationList...")
#        response = requests.get(url = 
#        f"{config()['Gateway_Url']}/revocation-list", 
#        cert=(config()['Auth_Cert'], config()['Auth_Key']))
#        with open (f"{config()['Main_Location']}/data/revocationList.json", "w") as c:
#            json.dump(response.json(), c, indent = 4)
#            c.close()
#        config_data = config()
#        config_data['Last_Updated_Rl'] = datetime.now().replace(microsecond=0).isoformat()+"+02:00"
#        with open (f"{config()['Main_Location']}/config.json", "w") as c:
#            json.dump(config_data, c, indent = 4)
#            c.close()
    
    
