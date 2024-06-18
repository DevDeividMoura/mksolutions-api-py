from bs4 import BeautifulSoup

def _extract_error_message_from_html(html_text: str) -> str:
    """
    Extrai a mensagem de erro de um HTML.

    :param html_text: O texto HTML da resposta.
    :return: A mensagem de erro extraída.
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        message = p.find('b', string=lambda x: x and 'Message' in x)
        if message: return p.text.strip()
    return html_text.strip()