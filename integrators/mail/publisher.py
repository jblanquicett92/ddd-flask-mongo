from __future__ import annotations

from integrators.mail.client import EmailClient


def post_email_message(attached_file_path, text_msg):
    email_client = EmailClient()

    success_response = email_client.send_email(attached_file_path, text_msg)

    return success_response


if __name__ == '__main__':

    # Create the plain-text and HTML version of your message
    msg_text = """\
               Hola!,
               Te informamos que la generación de códigos QRCode para usuarios ha sido creado en un archivo PDF
               en Digitalización.

               Valida la información en el archivo adjunto.

               Puedes informar cualquier inconsistencia al equipo de Innovation.

               organization Innovation!
               """

    # Attach
    file_path_to_attach = '../integrators/prueba.pdf'

    print(f'Email Response: {post_email_message(file_path_to_attach, msg_text)}')
