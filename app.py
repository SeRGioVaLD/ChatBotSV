from flask import Flask, request
import sett 
import services

app = Flask(__name__)

@app.route('/bienvenido', methods=['GET'])
def  bienvenido():
    return 'Hola mundo bigdateros, desde Flask'

@app.route('/webhook', methods=['GET'])
def verificar_token():
    print("VERIFICACION DE TOKEN")
    try:
        token = request.args.get('hub.verify_token')
        
        print("TOKEN___:", token)
        challenge = request.args.get('hub.challenge')
        
        print("challenge: ",challenge)

        if token == sett.token and challenge != None:
            print("TOKEN VERIFICADO")
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return e,403
    
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from'] # services.replace_start(message['from'])
        print("NUMERO QUE HABLA: ",number)
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)

        services.administrar_chatbot(text, number,messageId,name)
        return 'enviado'
    except Exception as e:
        print("Mensaje no enviado")
        return 'no enviado ' + str(e)

if __name__ == '__main__':
    app.run(debug=True)