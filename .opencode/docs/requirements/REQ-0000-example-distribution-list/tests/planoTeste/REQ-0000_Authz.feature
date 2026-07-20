Feature: Distribution List authorization
  As a security control
  I want unauthorized calls rejected
  So that only operators manage lists

  Scenario: Non-operator cannot create
    Given I am not an operator
    When I POST to /lists
    Then the response status is 403
