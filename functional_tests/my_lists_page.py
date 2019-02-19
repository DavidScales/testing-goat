class MyListsPage(object):

  def __init__(self, test):
    # verify that this is my_lists page?
    # https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#page-object-design-pattern
    self.test = test

  def go_to_my_lists_page(self):
    self.test.browser.get(self.test.live_server_url)
    self.test.browser.find_element_by_link_text('My lists').click()
    self.test.wait_for(lambda: self.test.assertEqual(
      self.test.browser.find_element_by_tag_name('h1').text,
      'My Lists'
    ))
    return self