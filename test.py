import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Importing TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchWindowException
@pytest.mark.usefixtures("driver")
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Change to your desired browser
    yield driver
    driver.quit()

def search(driver, search_query):
    driver.get("http://watchplace.great-site.net/brand-manager.php")
    time.sleep(3)
    search_box = driver.find_element(By.NAME, "brand-search")
    search_box.send_keys(search_query + Keys.RETURN)
    time.sleep(3)  # Chờ kết quả tìm kiếm

    try:
        # Chờ danh sách thương hiệu hiển thị
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr[1]/td[2]"))  #Lấy tên cần tìm
        )

        # Lấy danh sách các thương hiệu tìm được
        brands = driver.find_elements(By.XPATH, "//tr[contains(@id, 'BR')]")  # Chọn các dòng thương hiệu
        print(f"Số lượng thương hiệu tìm được: {len(brands)}")

        # Trả về danh sách tên thương hiệu
        result = [brand.find_element(By.XPATH, ".//td[1]").text for brand in
                  brands]  # Giả sử tên thương hiệu nằm trong cột đầu tiên
        return result
    except TimeoutException:
        print("Fail: Không tìm thấy thương hiệu.")
        return []
#brand_search_01
#pass
def test_timkiem_kytu_hople(driver):
    search_query = "Seiko"
    result = search(driver, search_query)
    assert len(result) > 0, f"Test failed: Không tìm thấy thương hiệu với từ khóa '{search_query}'."

#brand_search_02
#pass
def test_timkiem_kytu_khonghople(driver):
    search_query = "khongbiet"

    # Thực hiện tìm kiếm với từ khóa không hợp lệ
    result = search(driver, search_query)  # Giả sử hàm này thực hiện tìm kiếm thương hiệu
    assert len(result) == 0, f"Test failed: Không tìm thấy thương hiệu với từ khóa '{search_query}'."

    # Kiểm tra thông báo không có thương hiệu nào (Không tìm thấy kết quả)
    no_brands_message = "Không có thương hiệu nào để hiển thị!"
    assert no_brands_message in driver.page_source

#brand_search_03
#fail
def test_timkiem_kytu_rong(driver):
    search_query = ""
    result = search(driver, search_query)
    assert len(result) == 0, f"Test failed: Không tìm thấy thương hiệu với từ khóa '{search_query}'."

#brand_search_04
#pass
def test_timkiem_kytu_dacbiet(driver):
    search_query = "!@#$%"
    result = search(driver, search_query)
    assert len(result) == 0, f"Test failed: Không tìm thấy thương hiệu với từ khóa '{search_query}'."


#brand_search_05
#pass
def test_timkiem_kytu_inhoa(driver):
    search_query = "SEIKO"

    # Thực hiện tìm kiếm với từ khóa viết hoa
    result = search(driver, search_query)

    # Kiểm tra xem có ít nhất một kết quả tìm kiếm không
    assert len(result) > 0, f"Test failed: Không tìm thấy thương hiệu với từ khóa '{search_query}'."

#brand_search_06
#pass
def test_timkiem_kytu_khoangtrang(driver):
    search_query = "  Seiko  "
    # Thực hiện tìm kiếm với từ khóa viết hoa
    result = search(driver, search_query)

    # Kiểm tra xem có ít nhất một kết quả tìm kiếm không
    assert len(result) == 0, f"Test failed: Không tìm thấy thương hiệu với từ khóa '{search_query}'."
    # Kiểm tra thông báo không có thương hiệu nào (Không tìm thấy kết quả)
    no_brands_message = "Không có thương hiệu nào để hiển thị!"
    assert no_brands_message in driver.page_source

def them_thuonghieu(driver, name, description, status):
    driver.get("http://watchplace.great-site.net/brand-manager.php")
    time.sleep(3)

    # Click the "Add Brand" button
    add_brand_button = driver.find_element(By.CLASS_NAME, "brand-header__insert")
    add_brand_button.click()
    time.sleep(1)

    # Fill in brand information
    driver.find_element(By.NAME, "brand-name").send_keys(name)
    driver.find_element(By.NAME, "brand-desc").send_keys(description)
    driver.find_element(By.NAME, "status").send_keys(status)
    time.sleep(1)

    # Submit the form
    submit_button = driver.find_element(By.NAME, "submit")
    submit_button.click()
    time.sleep(1)

    # Handle the first alert (confirming the brand was added)
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert1 = driver.switch_to.alert
    alert1_message = alert1.text
    print(alert1_message)  # Print the alert message to the console
    alert1.accept()  # Accept the alert

    # Handle the second alert (confirmation or further instructions)
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert2 = driver.switch_to.alert
    alert2_message = alert2.text
    print(alert2_message)  # Print the second alert message
    alert2.accept()  # Accept the second alert


    # Find the brand table
    brand_name = driver.find_element(By.CLASS_NAME, "brand__table")
    rows = brand_name.find_elements(By.TAG_NAME, "tr")

    # Check if the brand is added by looking for the brand in the table rows
    for row in rows[1:]:  # Skip the header row
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) > 0 and name in cells[1].text:  # Assuming the brand name is in the second column
            print(f"Brand '{name}' was successfully added.")
            return True
    print(f"Brand '{name}' not found after checking all pages.")
    return False

#Add_brand_01
#pass
def test_add_thuonghieu_hople(driver):
    name = "Đồng hồ áldkjasd"
    des = "Đồng hồ áldkjasd"
    # value = 0 : ngừng hoạt động ; value = 1: hoạt động
    status = "1"
    them_thuonghieu(driver, name, des, status)

#Add_brand_02
#Fail
#fail_vì khi add kí hiệu đặc hiệu không có thông báo sai
def test_add_thuonghieu_kytu_dacbiet(driver):
    name = "@@@@"  # Tên thương hiệu không hợp lệ
    des = "@@@"    # Mô tả không hợp lệ
    status = "0"   # Trạng thái không hoạt động

    # Gọi hàm để thêm thương hiệu
    them_thuonghieu(driver, name, des, status)

    # Kiểm tra xem thương hiệu không được thêm vào danh sách
    assert them_thuonghieu is False, f"Thương hiệu '{name}' không nên được thêm vào, nhưng lại đã được thêm."

#Add_brand_03
#pass

def test_add_brand_same_data(driver):
    name = "Đồng hồ áldkjasd"
    description = "Đồng hồ áldkjasd"
    # value = 0 : ngừng hoạt động ; value = 1: hoạt động
    status = "1"

    # Gọi hàm thêm thương hiệu
    them_thuonghieu(driver, name, description, status)

    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        assert "Thêm thất bại!" in alert_text
        alert.accept()
    except TimeoutException:
        print("Alert không xuất hiện!")

def sua_thuonghieu(driver, id, new_name, new_des):
    # Truy cập vào trang quản lý thương hiệu
    driver.get("http://watchplace.great-site.net/brand-manager.php")
    time.sleep(3)

    # Tìm bảng danh sách thương hiệu
    brand_table = driver.find_element(By.CLASS_NAME, "brand__table")
    rows = brand_table.find_elements(By.TAG_NAME, "tr")

    # Duyệt qua các dòng trong bảng để tìm thương hiệu cần chỉnh sửa
    found_before_edit = False
    for row in rows:
        if id in row.text:
            found_before_edit = True
            edit_button = row.find_element(By.CSS_SELECTOR, ".brand-table__edit.material-symbols-outlined")
            edit_button.click()  # Click vào nút sửa
            time.sleep(5)
            break

    if not found_before_edit:
        print("Không tìm thấy thể loại cần sửa.")
        return

    # Điền thông tin mới vào các trường tương ứng
    driver.find_element(By.NAME, "brand-name").clear()  # Xóa trường tên cũ
    driver.find_element(By.NAME, "brand-name").send_keys(new_name)  # Nhập tên mới

    driver.find_element(By.NAME, "brand-desc").clear()  # Xóa mô tả cũ
    driver.find_element(By.NAME, "brand-desc").send_keys(new_des)  # Nhập mô tả mới

    submit_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-brand-container-content__btn.edit"))
    )
    submit_button.click()
    time.sleep(4)

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert1 = driver.switch_to.alert
    alert1.accept()  # Acc
    time.sleep(2)

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert2 = driver.switch_to.alert
    alert2.accept()  # Acc
    time.sleep(2)

    # Kiểm tra sau khi chỉnh sửa
    table = driver.find_element(By.CLASS_NAME, "brand__table")
    rows_after_edit = table.find_elements(By.TAG_NAME, "tr")
    found_after_edit = False

    for row in rows_after_edit:
        if new_name in row.text:
            found_after_edit = True
            break

    if found_after_edit:
        print("Sửa thành công!")
    else:
        print("Lỗi: Không thể sửa thể loại.")

#Edit_brand_01
#pass
def test_sua_thongtin_thuonghieu(driver):
    id = "BR022"
    new_name = "sửa thử"
    des = "sửa thử"
    sua_thuonghieu(driver, id, new_name, des)

#Edit_brand_01
#pass
def edit_brand_and_cancel(driver, id, new_name, new_des):
    # Truy cập vào trang quản lý thương hiệu
    driver.get("http://watchplace.great-site.net/brand-manager.php")
    time.sleep(3)

    # Tìm bảng danh sách thương hiệu
    brand_table = driver.find_element(By.CLASS_NAME, "brand__table")
    rows = brand_table.find_elements(By.TAG_NAME, "tr")

    # Duyệt qua các dòng trong bảng để tìm thương hiệu cần chỉnh sửa
    original_name = ""
    original_desc = ""
    found = False

    for row in rows:
        if id in row.text:
            found = True
            cells = row.find_elements(By.TAG_NAME, "td")
            original_name = cells[1].text  # Giả định cột 2 là tên thương hiệu
            original_desc = cells[2].text  # Giả định cột 3 là mô tả thương hiệu

            edit_button = row.find_element(By.CSS_SELECTOR, ".brand-table__edit.material-symbols-outlined")
            edit_button.click()  # Click vào nút sửa
            time.sleep(3)
            break

    if not found:
        print("Không tìm thấy thương hiệu cần sửa.")
        return

    # Điền thông tin mới vào các trường tương ứng
    driver.find_element(By.NAME, "brand-name").clear()
    driver.find_element(By.NAME, "brand-name").send_keys(new_name)

    driver.find_element(By.NAME, "brand-desc").clear()
    driver.find_element(By.NAME, "brand-desc").send_keys(new_des)

    # Bấm nút xác nhận sửa đổi nhưng hủy alert đầu tiên
    submit_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-brand-container-content__btn.edit"))
    )
    submit_button.click()
    time.sleep(2)

    # Hủy xác nhận trong alert
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert1 = driver.switch_to.alert
    print("Alert text:", alert1.text)  # In nội dung của alert
    alert1.dismiss()  # Hủy thao tác (Dismiss)
    time.sleep(2)

    # Kiểm tra dữ liệu gốc không bị thay đổi
    driver.refresh()  # Tải lại trang để kiểm tra
    time.sleep(3)
    rows_after_cancel = driver.find_elements(By.CSS_SELECTOR, ".brand__table tr")

    data_unchanged = False
    for row in rows_after_cancel:
        if id in row.text and original_name in row.text and original_desc in row.text:
            data_unchanged = True
            break

    if data_unchanged:
        print("Hủy thao tác thành công, dữ liệu không thay đổi.")
    else:
        print("Lỗi: Dữ liệu đã bị thay đổi sau khi hủy thao tác.")

#Edit_brand_02
#pass
def test_edit_brand_and_cancel(driver):
    id = "BR022"
    new_name = "sửa thử (hủy)"
    new_des = "mô tả thử (hủy)"
    edit_brand_and_cancel(driver, id, new_name, new_des)

def filter(driver, start, end, order_status=None):
    driver.get("http://watchplace.great-site.net/order-manager.php?")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/form/div[1]/input[1]")))

    # Nhập ngày bắt đầu
    start_date_el = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/form/div[1]/input[1]")
    start_date_el.clear()
    start_date_el.send_keys(start)

    # Nhập ngày kết thúc
    end_date_el = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/form/div[1]/input[2]")
    end_date_el.clear()
    end_date_el.send_keys(end)
    time.sleep(3)
    # Chọn trạng thái đơn hàng nếu có
    if order_status:
        status_select = driver.find_element(By.NAME, "order-status")
        for option in status_select.find_elements(By.TAG_NAME, "option"):
            if option.text == order_status:
                option.click()
                break
    time.sleep(3)
    # Nhấn nút xác nhận
    confirm_button = driver.find_element(By.NAME, "submit")
    confirm_button.click()

    # B1 Kiểm tra thông báo lỗi
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return f"Lỗi: {alert_text}"
    except Exception:
        pass  # B2 Không có alert, tiếp tục xử lý

    # B3 Kiểm tra nếu không nhập ngày thì trả về thông báo lỗi
    if not start and not end:
        return "Vui lòng nhập ngày bắt đầu và kết thúc"

    # B4 Lấy thông tin từ bảng
    try:
        info_date_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "order__table"))
        )
        rows = info_date_el.find_elements(By.TAG_NAME, "tr")
        results = [
            (cols[0].text, cols[1].text, cols[6].text)
            for row in rows[1:]  # Bỏ qua hàng tiêu đề
            if (cols := row.find_elements(By.TAG_NAME, "td")) and len(cols) >= 7
        ]
        return results
    except Exception as e:
        return f"Có lỗi xảy ra: {str(e)}"

#filter_01
#pass
def test_filter_thoigian_hople(driver):
    start_valid = "01/07/2024"
    end_valid = "12/07/2024"
    results_valid = filter(driver, start_valid, end_valid)
    assert isinstance(results_valid, list) and len(results_valid) > 0, "Không có kết quả cho ngày hợp lệ"


#filter_02
#pass
def test_filter_thoigian_Khople(driver):
    start_invalid = "01/01/01"
    end_invalid = "02/02/02"
    result = filter(driver, start_invalid, end_invalid)
    assert len(result) == 0
    alert_text = "Không có đơn hàng nào để hiển thị!"
    assert  alert_text in driver.page_source


#filter_03
#pass
def test_filter_khongnhap_ngayloc(driver):
    results_no_date = filter(driver, "", "")
    assert "Vui lòng nhập" in results_no_date, \
        "Kỳ vọng có thông báo lỗi khi không nhập ngày, nhưng không nhận được"

#filter_04
#pass
def test_filter_ngay_batdau(driver):
    start = "01/07/2024"
    results_start_only = filter(driver, start, "")
    assert "" in results_start_only, \
        "Kỳ vọng có thông báo lỗi khi chỉ nhập ngày bắt đầu, nhưng không nhận được"

#filter_05
#pass
def test_filter_Startdates_bigger_finishdates(driver):
    start_later = "15/07/2024"
    end_earlier = "10/07/2024"
    results_later = filter(driver, start_later, end_earlier)
    assert "Lỗi" in results_later, "Kỳ vọng có thông báo lỗi, nhưng nhận được kết quả hợp lệ"

#filter_06
#pass
def test_filter_trangthai_donhang(driver):
    start_date = "01/07/2024"
    end_date = "12/07/2024"
    order_status = "Đã giao hàng"  # Chọn trạng thái nào đó từ danh sách

    results = filter(driver, start_date, end_date, order_status)

    # Kiểm tra rằng kết quả không trống
    assert len(results) > 0, "Kỳ vọng có kết quả, nhưng không có kết quả nào được trả về"
    

