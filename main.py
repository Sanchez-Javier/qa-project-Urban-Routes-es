import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    tarif_comfort = (By.XPATH,"//div[contains(@class,'tcard')]//div[@class='tcard-title'] [text() = 'Comfort']")
    save_taxi = (By.CSS_SELECTOR,'.button.round')
    phone_button = (By.CLASS_NAME,"np-text")
    phone_field = (By.ID, 'phone')
    code_field = (By.ID,'code')
    button_next = (By.XPATH,"//button[@class='button full'][text()='Siguiente']")
    btn_confirm = (By.XPATH,"//button[@class='button full'][text()='Confirmar']")
    mtd_pay_button = (By.CSS_SELECTOR,'.pp-button.filled')
    add_card_button = (By.CSS_SELECTOR,'.pp-row.disabled')
    card_number_field = (By.ID,'number')
    code_card_number_field = (By.CSS_SELECTOR,'#code.card-input')
    btn_add = (By.XPATH, "//button[@class='button full'][text()='Agregar']")
    out_place = (By.CLASS_NAME,'plc')
    btn_close = (By.XPATH, "//div[@class='head'][text() = 'Método de pago']/..//button[@class='close-button section-close']")
    message = (By.ID,'comment')
    blanket_and_handkerchiefs = (By.XPATH, "//div[@class='r-sw-label'][text() = 'Manta y pañuelos']/..//span[@class='slider round']")
    icecream_chocolate = (By.XPATH, "//div[@class='r-counter-label'][text() = 'Chocolate']/..//div[@class='counter-plus']")
    request_taxi = (By.CLASS_NAME,'smart-button')
    driver_modal = (By.CLASS_NAME,'order-number')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.from_field))
        self.set_from(address_from)
        self.set_to(address_to)

    def order_transport(self):
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.save_taxi))
        self.driver.find_element(*self.save_taxi).click()

    def choose_tarif(self):
        self.driver.find_element(*self.tarif_comfort).click()

    def get_tarif(self):
        return self.driver.find_element(*self.tarif_comfort).find_element(By.XPATH,"..").get_attribute("class")

    def click_phone(self):
        self.driver.find_element(*self.phone_button).click()

    def set_phone(self, phone):
        self.driver.find_element(*self.phone_field).send_keys(phone)

    def set_code(self,code):
        self.driver.find_element(*self.code_field).send_keys(code)

    def btn_next(self):
        self.driver.find_element(*self.button_next).click()

    def confirm_phone(self):
        self.driver.find_element(*self.btn_confirm).click()

    def click_mtd_pay_button(self):
        self.driver.find_element(*self.mtd_pay_button).click()

    def click_add_card_button(self):
        self.driver.find_element(*self.add_card_button).click()

    def set_card_number(self, number):
        self.driver.find_element(*self.card_number_field).send_keys(number)

    def set_code_card_number(self, code):
        self.driver.find_element(*self.code_card_number_field).send_keys(code)

    def click_out_place(self):
        self.driver.find_element(*self.out_place).click()

    def click_add_card(self):
        self.click_out_place()
        self.driver.find_element(*self.btn_add).click()

    def close_popup(self):
        self.driver.find_element(*self.btn_close).click()

    def set_message(self, message):
        self.driver.find_element(*self.message).send_keys(message)

    def active_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.blanket_and_handkerchiefs).click()

    def add_icecream_chocolate(self,cantidad):
        if(cantidad>0):
            for i in range(cantidad):
                self.driver.find_element(*self.icecream_chocolate).click()
        else:
            print('Por favor ingresa al menos un número del 1 al infinito')

    def request_one_taxi(self):
        self.driver.find_element(*self.request_taxi).click()

    def wait_driver_modal(self):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.driver_modal))

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = webdriver.ChromeOptions()
        capabilities.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        #Agregando datos a las variables
        address_from = data.address_from
        address_to = data.address_to
        number_phone = data.phone_number
        comment = data.message_for_driver

        #Ejecutando proceso para ingresar datos en los campos desde y hasta
        routes_page.set_route(address_from, address_to)

        #Ejecuta pedir un Taxi
        routes_page.order_transport()

        #Elije la tarifa del Taxi
        routes_page.choose_tarif()

        #Abre el modal de ingresar telefono y coloca el código de confirmación.
        routes_page.click_phone()
        routes_page.set_phone(number_phone)
        routes_page.btn_next()
        code = retrieve_phone_code(self.driver)
        routes_page.set_code(code)
        routes_page.confirm_phone()

        #Abre el modal de ingresar el metodo de pago y lo cierra.
        routes_page.click_mtd_pay_button()
        routes_page.click_add_card_button()
        routes_page.set_card_number(data.card_number)
        routes_page.set_code_card_number(data.card_code)
        routes_page.click_add_card()
        routes_page.close_popup()

        #Escribiendo un mensaje para el conductor
        routes_page.set_message(comment)

        #Poner manta y pañuelos
        routes_page.active_blanket_and_handkerchiefs()

        #Agregar helado de chocolate
        routes_page.add_icecream_chocolate(2)

        #Solicitar el taxi
        routes_page.request_one_taxi()

        #Esperando datos del conductor
        routes_page.wait_driver_modal()

        #Prubas
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        assert routes_page.get_tarif() == "tcard active"


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
