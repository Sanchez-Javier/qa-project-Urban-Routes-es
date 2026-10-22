import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    blanket_and_handkerchiefs = (By.XPATH,"//div[@class='r-sw-label'][text() = 'Manta y pañuelos']/..//span[@class='slider round']")
    blanket_and_handkerchiefs_is_active = (By.XPATH, "//div[@class='r-sw-label'][text() = 'Manta y pañuelos']/following-sibling::div[@class='r-sw']//input[@class='switch-input']")
    icecream_chocolate = (By.XPATH, "//div[@class='r-counter-label'][text() = 'Chocolate']/..//div[@class='counter-plus']")
    icecream_counts = (By.XPATH, "//div[@class='r-counter-label'][text() = 'Chocolate']/..//div[@class='counter-value']")
    request_taxi = (By.CLASS_NAME,'smart-button')
    search_car = (By.CLASS_NAME,'order-header-title')
    driver_modal = (By.CLASS_NAME,'order-number')
    wait_car = (By.CLASS_NAME,'order-header-title')

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
        return self.driver.find_element(*self.tarif_comfort).text

    def click_phone(self):
        self.driver.find_element(*self.phone_button).click()

    def set_phone(self, phone):
        self.driver.find_element(*self.phone_field).send_keys(phone)

    def get_phone(self):
        return self.driver.find_element(*self.phone_field).get_attribute('value')

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

    def get_card_number(self):
        return self.driver.find_element(*self.card_number_field).get_attribute('value')

    def get_code_card_number(self):
        return self.driver.find_element(*self.code_card_number_field).get_attribute('value')

    def click_out_place(self):
        self.driver.find_element(*self.out_place).click()

    def click_add_card(self):
        self.click_out_place()
        self.driver.find_element(*self.btn_add).click()

    def close_popup(self):
        self.driver.find_element(*self.btn_close).click()

    def set_message(self, message):
        self.driver.find_element(*self.message).send_keys(message)

    def get_message(self):
        return self.driver.find_element(*self.message).get_attribute('value')

    def active_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.blanket_and_handkerchiefs).click()

    def is_active_blanket_and_handkerchiefs(self):
        return self.driver.find_element(*self.blanket_and_handkerchiefs_is_active).is_selected()

    def add_icecream_chocolate(self,cantidad):
        if(cantidad>0):
            for i in range(cantidad):
                self.driver.find_element(*self.icecream_chocolate).click()
        else:
            print('Por favor ingresa al menos un número del 1 al infinito')

    def count_icecream(self):
        return int(self.driver.find_element(*self.icecream_counts).text)

    def request_one_taxi(self):
        self.driver.find_element(*self.request_taxi).click()

    def get_search_car(self):
        return self.driver.find_element(*self.search_car).text

    def wait_driver_modal(self):
        WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located(self.driver_modal))

    def get_car_model(self):
        return self.driver.find_element(*self.wait_car).text

class TestUrbanRoutes:

    driver = None

    def setup_method(self):
        options = Options()
        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)

    def test_set_route(self):
        #Agregando datos a las variables
        address_from = data.address_from
        address_to = data.address_to

        #Ejecutando proceso para ingresar datos en los campos desde y hasta
        self.routes_page.set_route(address_from, address_to)

        #Prubas
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    def add_adress(self):
        # Agrega las Direcciones
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        #Ejecuta pedir un Taxi
        self.routes_page.order_transport()

    def test_select_comfort(self):
        #Agrega las Direcciones
        self.add_adress()

        # Elije la tarifa del Taxi
        self.routes_page.choose_tarif()

        assert self.routes_page.get_tarif() == "Comfort"

    def test_add_phone(self):
        # Agrega las Direcciones
        self.add_adress()

        # Abre el modal de ingresar telefono y coloca el código de confirmación.
        number_phone = data.phone_number
        self.routes_page.click_phone()
        self.routes_page.set_phone(number_phone)
        self.routes_page.btn_next()
        code = retrieve_phone_code(self.driver)
        self.routes_page.set_code(code)
        self.routes_page.confirm_phone()

        assert self.routes_page.get_phone() == number_phone

    def test_add_card(self):
        # Agrega las Direcciones
        self.add_adress()

        # Abre el modal de ingresar el metodo de pago y lo cierra.
        number_card = data.card_number
        code_card = data.card_code
        self.routes_page.click_mtd_pay_button()
        self.routes_page.click_add_card_button()
        self.routes_page.set_card_number(number_card)
        self.routes_page.set_code_card_number(code_card)
        self.routes_page.click_add_card()
        self.routes_page.close_popup()

        assert self.routes_page.get_card_number() == number_card
        assert self.routes_page.get_code_card_number() == code_card

    def test_message_driver(self):
        # Agrega las Direcciones
        self.add_adress()

        # Escribiendo un mensaje para el conductor
        comment = data.message_for_driver
        self.routes_page.set_message(comment)

        assert self.routes_page.get_message() == comment

    def test_blanket(self):
        # Agrega las Direcciones
        self.add_adress()

        # Elije la tarifa del Taxi
        self.routes_page.choose_tarif()

        # Poner manta y pañuelos
        self.routes_page.active_blanket_and_handkerchiefs()

        assert self.routes_page.is_active_blanket_and_handkerchiefs() == True

    def test_ice_cream(self):
        # Agrega las Direcciones
        self.add_adress()

        # Elije la tarifa del Taxi
        self.routes_page.choose_tarif()

        # Agregar helado de chocolate
        cantidad_helados = 2
        self.routes_page.add_icecream_chocolate(cantidad_helados)

        assert self.routes_page.count_icecream() == cantidad_helados

    def test_search_taxi(self):
        # Agrega las Direcciones
        self.add_adress()

        # Elije la tarifa del Taxi
        self.routes_page.choose_tarif()

        # Abre el modal de ingresar telefono y coloca el código de confirmación.
        number_phone = data.phone_number
        self.routes_page.click_phone()
        self.routes_page.set_phone(number_phone)
        self.routes_page.btn_next()
        code = retrieve_phone_code(self.driver)
        self.routes_page.set_code(code)
        self.routes_page.confirm_phone()

        # Abre el modal de ingresar el metodo de pago y lo cierra.
        number_card = data.card_number
        code_card = data.card_code
        self.routes_page.click_mtd_pay_button()
        self.routes_page.click_add_card_button()
        self.routes_page.set_card_number(number_card)
        self.routes_page.set_code_card_number(code_card)
        self.routes_page.click_add_card()
        self.routes_page.close_popup()

        # Escribiendo un mensaje para el conductor
        comment = data.message_for_driver
        self.routes_page.set_message(comment)

        # Poner manta y pañuelos
        self.routes_page.active_blanket_and_handkerchiefs()

        # Agregar helado de chocolate
        cantidad_helados = 2
        self.routes_page.add_icecream_chocolate(cantidad_helados)

        # Solicitar el taxi
        self.routes_page.request_one_taxi()

        assert self.routes_page.get_search_car() == "Buscar automóvil"

    def test_driver_info(self):
        # Agrega las Direcciones
        self.add_adress()

        # Elije la tarifa del Taxi
        self.routes_page.choose_tarif()

        # Abre el modal de ingresar telefono y coloca el código de confirmación.
        number_phone = data.phone_number
        self.routes_page.click_phone()
        self.routes_page.set_phone(number_phone)
        self.routes_page.btn_next()
        code = retrieve_phone_code(self.driver)
        self.routes_page.set_code(code)
        self.routes_page.confirm_phone()

        # Abre el modal de ingresar el metodo de pago y lo cierra.
        number_card = data.card_number
        code_card = data.card_code
        self.routes_page.click_mtd_pay_button()
        self.routes_page.click_add_card_button()
        self.routes_page.set_card_number(number_card)
        self.routes_page.set_code_card_number(code_card)
        self.routes_page.click_add_card()
        self.routes_page.close_popup()

        # Escribiendo un mensaje para el conductor
        comment = data.message_for_driver
        self.routes_page.set_message(comment)

        # Poner manta y pañuelos
        self.routes_page.active_blanket_and_handkerchiefs()

        # Agregar helado de chocolate
        cantidad_helados = 2
        self.routes_page.add_icecream_chocolate(cantidad_helados)

        # Solicitar el taxi
        self.routes_page.request_one_taxi()

        # Esperando datos del conductor
        self.routes_page.wait_driver_modal()

        assert "El conductor llegará" in self.routes_page.get_car_model()

    def teardown_method(self):
        self.driver.quit()