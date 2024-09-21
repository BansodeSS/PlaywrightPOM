import re
from playwright.sync_api import Playwright, sync_playwright, expect


def test_login_standard_user(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_text("login").click()
    product_header = page.locator("span.title")
    expect(product_header).to_have_text("Products")

    # ---------------------
    context.close()
    browser.close()

def test_login_invalid_user(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret123_sauce")
    page.get_by_text("login").click()
    expected_fail_message = "Epic sadface: Username and password do not match any user in this service"
    err_msg = page.locator("//h3[@data-test='error']")
    expect(err_msg).to_contain_text(expected_fail_message)

    # ---------------------
    context.close()
    browser.close()

def test_login_with_no_credentials(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standard_user")
    # page.get_by_placeholder("Password").fill("secret123_sauce")
    page.get_by_text("login").click()
    expected_fail_message = "Epic sadface: Username is required"
    err_msg = page.locator("//h3[@data-test='error']")
    expect(err_msg).to_contain_text(expected_fail_message)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    test_login_standard_user(playwright)
    # test_login_invalid_user(playwright)
