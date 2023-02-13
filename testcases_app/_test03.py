# coding: utf-8

import pytest
import allure


class TestClass():
    
    @allure.title("用例11")
    @pytest.mark.parametrize("uuid", ["000003f70f0d364e", "WQCDU19C03004911"])  
    def test_11(self, uuid):
        print(f"我是测试11: {uuid}")
    
    @allure.title("用例12")
    @pytest.mark.parametrize("uuid", ["000003f70f0d364e", "WQCDU19C03004911"])  
    def test_12(self, uuid):
        print(f"我是测试11: {uuid}")