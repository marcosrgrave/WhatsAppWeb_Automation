from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time


def open_link(driver, link: str, timer: int):
    """This function opens a website if the browser is already open.\n
Driver Example: driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')"""
    driver.get(link)
    time.sleep(timer)


def find_class_timer_click(driver, class_name: str, timer: int):
    element = driver.find_element_by_class_name(class_name)
    time.sleep(timer)
    element.click()


def find_xpath_timer_click(driver, xpath_type: str, button: str, timer: int):
    """xpath_type = data-icon, title, etc.\n
       button = send, menu, etc."""
    element = driver.find_element_by_xpath(f"//span[@{xpath_type}={button}]")
    time.sleep(timer)
    element.click()


class WhatsAppBot:

    def __init__(self) -> None:
        # chrome_options = webdriver.ChromeOptions().add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(
            executable_path=r'./chromedriver.exe'
        )

    def create_new_group(self, group_name: str, participants: list):
        """O foda é ter certeza que só tem um participante com esse nome.
        Quando é feita a pesquisa do nome, ele puxa o primeiro.
        """

        open_link(
            driver=self.driver,
            link="https://web.whatsapp.com/",
            timer=10
        )

        self.btn_3dots = find_xpath_timer_click(
            driver=self.driver,
            xpath_type="data-icon",
            button="menu",
            timer=.5
        )
        self.btn_new_group = find_class_timer_click(
            driver=self.driver,
            class_name="_2oldI dJxPU",
            timer=.5
        )

        # escrever nomes unicos e exatos de quem participará do grupo
        self.names_field = self.driver.find_element_by_class_name(name="etp_f")
        for name in participants:
            self.names_field.send_keys(value=name)
            self.names_field.send_keys(value=Keys.RETURN)

        self.btn_next = find_class_timer_click(
            driver=self.driver,
            class_name="_165_h",
            timer=.5
        )

        self.group_subject = find_class_timer_click(
            driver=self.driver,
            class_name="_1UWac Z2O8p",
            timer=.5
        )
        self.group_subject.send_keys(value=group_name)

        self.btn_finish = find_class_timer_click(
            driver=self.driver,
            class_name="_165_h",
            timer=.5
        )

    def send_group_message(self, attendant_name: str, company_name: str, groups_names: list, people_names: list):
        """Função que envia a mesma mensagem para chats já existentes.\n
        Os nomes dos grupos precisam ser idênticos ao que aparece no WhatsApp (Recomendo copiar e colar).\n
        O nome dos zeladores precisam estar na mesma ordem do nome dos grupos.
        """

        open_link(
            driver=self.driver,
            link="https://web.whatsapp.com/",
            timer=2
        )

        # para cada grupo na lista informada, faça:
        for person_name, group_name in zip(people_names, groups_names):

            # encontrando o nome do grupo no whats e clicando nele
            group_name_search_element = self.driver.find_element_by_xpath(
                f"//span[@title='{group_name}']")
            # adicionando uma pausa antes de clicar para evitar erros
            time.sleep(.5)
            group_name_search_element.click()

            # mensagem padrão enviada nos grupos com os zeladores
            message_template = f"""
                Olá, {person_name}! Tudo bem?
                Meu nome é {attendant_name.strip()} e trabalho na {company_name}. Estou aqui para tal e tal coisa...
            """

            # clicando no chat e escrevendo a mensagem
            chat_element = self.driver.find_element_by_class_name(
                '_13mgZ')  # elements busca uma lista
            time.sleep(.5)
            chat_element.click()
            chat_element.send_keys(message_template)

            # clicando no botão de enviar
            btn_send_element = self.driver.find_element_by_xpath(
                "//span[@data-icon='send']")
            time.sleep(.5)
            btn_send_element.click()

    def send_private_message(self, users_no: list, message: str):
        """Envia a mesma mensagem nos numeros indicados.\n
        *IMPORTANTE: Os números precisam conter a identificação 
        do país (Brasil: 55) e do DDD (SC: 48)"""

        # https://www.youtube.com/watch?v=wrxrpC5Yeac

        import urllib

        # codificando a mensagem para a URL
        message = urllib.parse.quote(message)

        time.sleep(1)
        for number in users_no:
            link = f"https://web.whatsapp.com/send?phone={number}&text={message}"
            self.driver.get(link)
            time.sleep(1)
            Keys.RETURN
